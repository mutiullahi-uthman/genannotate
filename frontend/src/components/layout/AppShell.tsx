"use client";

import { Menu } from "lucide-react";
import { useState } from "react";
import { usePathname } from "next/navigation";
import ProtectedRoute from "@/components/auth/ProtectedRoute";
import Sidebar from "@/components/layout/Sidebar";
import ThemeToggle from "@/components/layout/ThemeToggle";

export default function AppShell({
  children,
}: {
  children: React.ReactNode;
}) {
  const pathname = usePathname();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  if (pathname === "/login") {
    return children;
  }

  function closeMobileMenu() {
    setMobileMenuOpen(false);
  }

  return (
    <ProtectedRoute>
      <div className="flex min-h-screen bg-slate-50 text-slate-900 dark:bg-slate-950 dark:text-slate-100">
        {mobileMenuOpen && (
          <button
            type="button"
            aria-label="Close navigation"
            onClick={closeMobileMenu}
            className="fixed inset-0 z-40 bg-slate-950/50 backdrop-blur-sm lg:hidden"
          />
        )}
        <Sidebar
          mobileMenuOpen={mobileMenuOpen}
          onClose={closeMobileMenu}
        />
        <div className="flex min-h-screen min-w-0 flex-1 flex-col">
          <header className="sticky top-0 z-30 flex h-16 items-center justify-between border-b border-border bg-surface/95 px-4 sm:px-6 lg:hidden">
            <div className="flex items-center gap-3">
              <button
                type="button"
                aria-label="Open navigation"
                aria-controls="main-sidebar"
                aria-expanded={mobileMenuOpen}
                onClick={() => setMobileMenuOpen(true)}
                className="grid size-10 place-items-center rounded-xl border border-slate-200 text-slate-600 transition hover:bg-slate-100 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 dark:border-slate-700 dark:text-slate-300 dark:hover:bg-slate-800"
              >
                <Menu size={19} aria-hidden="true" />
              </button>
              <span className="font-semibold tracking-tight">GenAnnotate</span>
            </div>
            <ThemeToggle compact />
          </header>

          <main className="mx-auto w-full max-w-[1600px] flex-1 px-4 py-6 sm:px-6 sm:py-8 lg:px-8 lg:py-10">
            {children}
          </main>
          <footer className="hidden border-t border-slate-200/80 px-8 py-4 text-xs text-slate-400 dark:border-slate-800 sm:block">
            GenAnnotate <span aria-hidden="true">·</span> Collaborative annotation workspace
          </footer>
        </div>
      </div>
    </ProtectedRoute>
  );
}
