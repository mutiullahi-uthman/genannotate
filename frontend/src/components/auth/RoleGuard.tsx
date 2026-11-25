"use client";

import type { UserRole } from "@/services/auth";
import { useAuth } from "@/providers/AuthProvider";

export default function RoleGuard({
  roles,
  children,
}: {
  roles: readonly UserRole[];
  children: React.ReactNode;
}) {
  const { profile } = useAuth();

  if (!profile || !roles.includes(profile.role)) {
    return (
      <section className="rounded-lg border border-amber-300 bg-amber-50 p-6 text-amber-950 dark:border-amber-800 dark:bg-amber-950 dark:text-amber-100">
        <h1 className="text-xl font-semibold">Access restricted</h1>
        <p className="mt-2 text-sm">
          Your account does not have permission to view this page.
        </p>
      </section>
    );
  }

  return children;
}
