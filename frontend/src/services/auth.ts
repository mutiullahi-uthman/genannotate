import { api } from "@/services/api";

export type UserRole =
  | "ADMIN"
  | "ANNOTATOR"
  | "SUPERVISOR"
  | "RESEARCH_LEAD";

export type UserStatus = "ACTIVE" | "INACTIVE" | "SUSPENDED";

export type AccountProfile = {
  id: string;
  firebase_uid: string;
  email: string;
  full_name: string;
  status: UserStatus;
};

export async function syncCurrentUser() {
  await api.post("/auth/sync-user");
}

export async function getCurrentUser() {
  const response = await api.get<AccountProfile>("/auth/me");
  return response.data;
}
