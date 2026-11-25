import { api } from "@/services/api";
import type { UserProfile, UserRole, UserStatus } from "@/services/auth";

export type ManagedUser = UserProfile;

export async function getUsers() {
  const response = await api.get<ManagedUser[]>("/users");
  return response.data;
}

export async function updateUser({
  userId,
  ...payload
}: {
  userId: string;
  role?: UserRole;
  status?: UserStatus;
}) {
  const response = await api.patch<ManagedUser>(
    `/users/${userId}`,
    payload,
  );
  return response.data;
}
