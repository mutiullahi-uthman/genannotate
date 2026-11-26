import { api } from "@/services/api";
import type { UserRole, UserStatus } from "@/services/auth";

export type ManagedUser = {
  id: string;
  firebase_uid: string;
  email: string;
  full_name: string;
  role: UserRole | null;
  membership_active: boolean | null;
  status: UserStatus;
};

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
  membership_active?: boolean;
  status?: UserStatus;
}) {
  const response = await api.patch<ManagedUser>(
    `/users/${userId}`,
    payload,
  );
  return response.data;
}
