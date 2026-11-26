"use client";

import { useAuth } from "@/providers/AuthProvider";

import { redirect } from "next/navigation";

export default function ProtectedRoute({
  children,
}: {
  children: React.ReactNode;
}) {
  const { user, profile, loading, error, refreshProfile } =
    useAuth();

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-background">
        <div
          role="status"
          aria-label="Loading your workspace"
          className="h-9 w-9 animate-spin rounded-full border-2 border-brand-100 border-t-brand-600"
        />
      </div>
    );
  }

  if (!user) {
    redirect("/login");
  }

  if (!profile) {
    return (
      <div className="flex min-h-screen flex-col items-center justify-center gap-4 bg-background p-6 text-center">
        <p role="alert" className="text-red-700 dark:text-red-300">
          {error ??
            "Your account is not currently a member of an active project. Contact a project administrator for access."}
        </p>
        <button
          type="button"
          onClick={refreshProfile}
          className="rounded-lg bg-slate-900 px-4 py-2 text-white dark:bg-white dark:text-slate-900"
        >
          Retry
        </button>
      </div>
    );
  }

  return children;
}