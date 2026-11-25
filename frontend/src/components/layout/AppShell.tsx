"use client";

import { usePathname } from "next/navigation";
import ProtectedRoute from "@/components/auth/ProtectedRoute";
import Sidebar from "@/components/layout/Sidebar";

export default function AppShell({
  children,
}: {
  children: React.ReactNode;
}) {
  const pathname = usePathname();

  if (pathname === "/login") {
    return children;
  }

  return (
    <ProtectedRoute>
      <div className="flex min-h-screen">
        <Sidebar />
        <main className="min-w-0 flex-1 p-5 sm:p-8">{children}</main>
      </div>
    </ProtectedRoute>
  );
}
