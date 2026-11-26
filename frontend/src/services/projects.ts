import { api } from "@/services/api";
import type { UserRole } from "@/services/auth";

export type ProjectMembership = {
  id: string;
  name: string;
  slug: string;
  role: UserRole;
};

export type Project = Pick<ProjectMembership, "id" | "name" | "slug">;

export async function getMyProjects() {
  const response = await api.get<ProjectMembership[]>("/projects/mine");
  return response.data;
}

export async function createProject(name: string) {
  const response = await api.post<Project>("/projects", { name });
  return response.data;
}
