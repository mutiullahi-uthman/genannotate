"use client";

import { toast } from "sonner";
import DataTable, {
  type DataTableColumn,
} from "@/components/ui/DataTable";
import RoleGuard from "@/components/auth/RoleGuard";
import { useAuth } from "@/providers/AuthProvider";
import { useUpdateUser, useUsers } from "@/hooks/useUsers";
import type { ManagedUser } from "@/services/users";
import type { UserRole, UserStatus } from "@/services/auth";

const roles: UserRole[] = [
  "ADMIN",
  "SUPERVISOR",
  "RESEARCH_LEAD",
  "ANNOTATOR",
];
const statuses: UserStatus[] = ["ACTIVE", "INACTIVE", "SUSPENDED"];

export default function UsersPage() {
  const { profile } = useAuth();
  const { data: users, isLoading, isError } = useUsers(
    profile?.role === "ADMIN",
  );
  const updateUser = useUpdateUser();

  const columns: DataTableColumn<ManagedUser>[] = [
    {
      key: "name",
      header: "User",
      render: (user) => (
        <div>
          <p className="font-medium">{user.full_name}</p>
          <p className="text-xs text-slate-500">{user.email}</p>
        </div>
      ),
    },
    {
      key: "role",
      header: "Role",
      render: (user) => (
        <select
          aria-label={`Role for ${user.full_name}`}
          value={user.role ?? ""}
          disabled={updateUser.isPending || user.id === profile?.id}
          onChange={(event) =>
            updateUser.mutate(
              {
                userId: user.id,
                ...(event.target.value
                  ? { role: event.target.value as UserRole }
                  : { membership_active: false }),
              },
              {
                onSuccess: () => toast.success("User role updated."),
              },
            )
          }
          className="rounded border border-slate-300 bg-white px-2 py-1 dark:border-slate-700 dark:bg-slate-900"
        >
          {!user.role && <option value="">Not a project member</option>}
          {roles.map((role) => (
            <option key={role} value={role}>
              {role.replaceAll("_", " ")}
            </option>
          ))}
        </select>
      ),
    },
    {
      key: "project-access",
      header: "Project access",
      render: (user) => (
        <select
          aria-label={`Project access for ${user.full_name}`}
          value={
            user.membership_active === true
              ? "active"
              : user.membership_active === false
                ? "inactive"
                : "none"
          }
          disabled={
            updateUser.isPending ||
            user.id === profile?.id ||
            !user.role
          }
          onChange={(event) =>
            updateUser.mutate(
              {
                userId: user.id,
                membership_active: event.target.value === "active",
              },
              {
                onSuccess: () => toast.success("Project access updated."),
              },
            )
          }
          className="rounded border border-slate-300 bg-white px-2 py-1 dark:border-slate-700 dark:bg-slate-900"
        >
          <option value="active">Active</option>
          <option value="inactive">Inactive</option>
          <option value="none">Not a member</option>
        </select>
      ),
    },
    {
      key: "status",
      header: "Status",
      render: (user) => (
        <select
          aria-label={`Status for ${user.full_name}`}
          value={user.status}
          disabled={updateUser.isPending || user.id === profile?.id}
          onChange={(event) =>
            updateUser.mutate(
              { userId: user.id, status: event.target.value as UserStatus },
              {
                onSuccess: () => toast.success("User status updated."),
              },
            )
          }
          className="rounded border border-slate-300 bg-white px-2 py-1 dark:border-slate-700 dark:bg-slate-900"
        >
          {statuses.map((status) => (
            <option key={status} value={status}>
              {status}
            </option>
          ))}
        </select>
      ),
    },
  ];

  return (
    <RoleGuard roles={["ADMIN"]}>
      <div className="space-y-6">
        <header>
          <h1 className="text-3xl font-bold">User management</h1>
          <p className="mt-2 text-sm text-slate-500">
            Manage roles and project membership for registered users. Account status applies across projects.
          </p>
        </header>
        <DataTable
          rows={users}
          columns={columns}
          rowKey={(user) => user.id}
          isLoading={isLoading}
          hasError={isError}
          emptyMessage="No users have registered yet."
        />
      </div>
    </RoleGuard>
  );
}
