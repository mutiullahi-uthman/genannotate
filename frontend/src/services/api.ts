import axios from "axios";
import { toast } from "sonner";
import { getFirebaseAuth, isFirebaseConfigured } from "@/lib/firebase";

export const api = axios.create({
  baseURL:
    process.env.NEXT_PUBLIC_API_URL,
});

api.interceptors.request.use(async (config) => {
  if (isFirebaseConfigured()) {
    const user = getFirebaseAuth().currentUser;
    if (user) {
      config.headers.Authorization = `Bearer ${await user.getIdToken()}`;
    }
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error: unknown) => {
    if (axios.isCancel(error)) {
      return Promise.reject(error);
    }

    if (axios.isAxiosError(error)) {
      const detail = error.response?.data?.detail;
      const message =
        typeof detail === "string"
          ? detail
          : error.message || "The request could not be completed.";
      toast.error(message);
    } else {
      toast.error("An unexpected error occurred.");
    }

    return Promise.reject(error);
  },
);