import axios from "axios";
import { toast } from "sonner";
import { getFirebaseAuth, isFirebaseConfigured } from "@/lib/firebase";

const configuredApiUrl =
  process.env.NEXT_PUBLIC_API_URL?.replace(/\/+$/, "") ?? "";
const apiBaseUrl = configuredApiUrl.endsWith("/api/v1")
  ? configuredApiUrl
  : `${configuredApiUrl}/api/v1`;

export const api = axios.create({
  baseURL: apiBaseUrl,
});

api.interceptors.request.use(async (config) => {
  if (typeof window !== "undefined") {
    const projectId = window.localStorage.getItem("active-project-id");
    if (projectId) {
      config.headers["X-Project-ID"] = projectId;
    }
  }
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