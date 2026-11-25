"use client";

import Link from "next/link";
import { signOut } from "firebase/auth";
import { usePathname, useRouter } from "next/navigation";
import { toast } from "sonner";
import { getFirebaseAuth } from "@/lib/firebase";
import { useAuth } from "@/providers/AuthProvider";
import type { UserRole } from "@/services/auth";
import ThemeToggle from "@/components/layout/ThemeToggle";

export default function Sidebar() {
  const pathname = usePathname();
  const router = useRouter();
  const { profile } = useAuth();
  const links = [
    { label: "Dashboard", href: "/dashboard" },
    { label: "Datasets", href: "/datasets" },
    { label: "Queue", href: "/queue" },
    { label: "Review", href: "/review" },
    {
      label: "Reports",
      href: "/reports",
      roles: ["ADMIN", "SUPERVISOR", "RESEARCH_LEAD"] as UserRole[],
    },
    { label: "Exports", href: "/exports" },
    {
      label: "Codebooks",
      href: "/codebooks",
      roles: ["ADMIN", "SUPERVISOR", "RESEARCH_LEAD"] as UserRole[],
    },
    {
      label: "Users",
      href: "/users",
      roles: ["ADMIN"] as UserRole[],
    },
  ];

  async function handleSignOut() {
    try {
      await signOut(getFirebaseAuth());
      router.replace("/login");
    } catch {
      toast.error("Could not sign out. Please try again.");
    }
  }

  return (
    <aside className="flex w-64 shrink-0 flex-col border-r border-slate-200 bg-white p-4 dark:border-slate-800 dark:bg-slate-950">
      <div className="mb-8 px-3 text-xl font-bold">GenAnnotate</div>
      <nav className="flex-1 space-y-1" aria-label="Main navigation">
        {links
          .filter((link) => !link.roles || link.roles.includes(profile?.role ?? "ANNOTATOR"))
          .map((link) => {
            const active =
              pathname === link.href || pathname.startsWith(`${link.href}/`);
            return (
              <Link
                key={link.href}
                href={link.href}
                aria-current={active ? "page" : undefined}
                className={`block rounded-lg px-3 py-2 text-sm font-medium ${
                  active
                    ? "bg-slate-900 text-white dark:bg-white dark:text-slate-900"
                    : "text-slate-600 hover:bg-slate-100 dark:text-slate-300 dark:hover:bg-slate-800"
                }`}
              >
                {link.label}
              </Link>
            );
          })}
      </nav>
      <div className="space-y-2 border-t border-slate-200 pt-4 dark:border-slate-800">
        <p className="truncate px-3 text-xs text-slate-500">
          {profile?.full_name} · {profile?.role.replaceAll("_", " ")}
        </p>
        <ThemeToggle />
        <button
          type="button"
          onClick={handleSignOut}
          className="w-full rounded-lg px-3 py-2 text-left text-sm text-slate-600 hover:bg-slate-100 dark:text-slate-300 dark:hover:bg-slate-800"
        >
          Sign out
        </button>
      </div>
    </aside>
  );
}
