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
      <div className="flex min-h-screen items-center justify-center">
        <div className="h-8 w-8 animate-spin rounded-full border-2 border-slate-300 border-t-slate-900 dark:border-slate-700 dark:border-t-white" />
      </div>
    );
  }

  if (!user) {
    redirect("/login");
  }

  if (!profile) {
    return (
      <div className="flex min-h-screen flex-col items-center justify-center gap-4 p-6 text-center">
        <p role="alert" className="text-red-700 dark:text-red-300">
          {error}
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