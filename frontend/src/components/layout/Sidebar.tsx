"use client";

import Link from "next/link";
import {
  BookOpen,
  ChartColumnIncreasing,
  ClipboardCheck,
  Database,
  Download,
  LayoutDashboard,
  LogOut,
  Leaf,
  ListChecks,
  Plus,
  Users,
  X,
  type LucideIcon,
} from "lucide-react";
import { signOut } from "firebase/auth";
import { usePathname, useRouter } from "next/navigation";
import { useState, type FormEvent } from "react";
import { toast } from "sonner";
import { getFirebaseAuth } from "@/lib/firebase";
import { useAuth } from "@/providers/AuthProvider";
import type { UserRole } from "@/services/auth";
import ThemeToggle from "@/components/layout/ThemeToggle";

type NavigationLink = {
  label: string;
  href: string;
  icon: LucideIcon;
  roles?: readonly UserRole[];
};

const navigationSections: {
  label: string;
  links: readonly NavigationLink[];
}[] = [
  {
    label: "Workspace",
    links: [
      { label: "Dashboard", href: "/dashboard", icon: LayoutDashboard },
      { label: "Datasets", href: "/datasets", icon: Database },
      { label: "Queue", href: "/queue", icon: ClipboardCheck },
      {
        label: "Assignments",
        href: "/assignments",
        icon: ListChecks,
        roles: ["ADMIN", "SUPERVISOR"],
      },
      {
        label: "Review",
        href: "/review",
        icon: ChartColumnIncreasing,
        roles: ["ADMIN", "SUPERVISOR"],
      },
    ],
  },
  {
    label: "Manage",
    links: [
      {
        label: "Reports",
        href: "/reports",
        icon: ChartColumnIncreasing,
        roles: ["ADMIN", "SUPERVISOR", "RESEARCH_LEAD"],
      },
      {
        label: "Exports",
        href: "/exports",
        icon: Download,
        roles: ["ADMIN", "SUPERVISOR", "RESEARCH_LEAD"],
      },
      {
        label: "Codebooks",
        href: "/codebooks",
        icon: BookOpen,
        roles: ["ADMIN", "SUPERVISOR", "RESEARCH_LEAD"],
      },
      {
        label: "Users",
        href: "/users",
        icon: Users,
        roles: ["ADMIN"],
      },
    ],
  },
];

export default function Sidebar({
  mobileMenuOpen,
  onClose,
}: {
  mobileMenuOpen: boolean;
  onClose: () => void;
}) {
  const pathname = usePathname();
  const router = useRouter();
  const {
    profile,
    projects,
    activeProject,
    selectProject,
    createProject,
  } = useAuth();
  const [projectName, setProjectName] = useState("");
  const [projectError, setProjectError] = useState<string | null>(null);

  async function handleSignOut() {
    try {
      await signOut(getFirebaseAuth());
      onClose();
      router.replace("/login");
    } catch {
      toast.error("Could not sign out. Please try again.");
    }
  }

  async function handleCreateProject(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    try {
      await createProject(projectName.trim());
      setProjectName("");
      setProjectError(null);
      onClose();
      toast.success("Project created.");
    } catch (error) {
      setProjectError(
        error instanceof Error ? error.message : "Could not create project.",
      );
    }
  }

  return (
    <aside
      id="main-sidebar"
      className={`fixed inset-y-0 left-0 z-50 flex w-72 max-w-[calc(100vw-2rem)] flex-col border-r border-border bg-surface p-4 shadow-2xl transition-transform duration-300 lg:sticky lg:top-0 lg:h-screen lg:shrink-0 lg:translate-x-0 lg:shadow-none ${
        mobileMenuOpen ? "translate-x-0" : "-translate-x-full"
      }`}
    >
      <div className="flex h-12 items-center justify-between px-2">
        <Link
          href="/dashboard"
          onClick={onClose}
          className="flex items-center gap-3 font-semibold tracking-tight"
        >
          <span className="grid size-9 place-items-center rounded-xl bg-accent-50 text-accent-500">
            <Leaf size={18} aria-hidden="true" />
          </span>
          <span className="text-base">GenAnnotate</span>
        </Link>
        <button
          type="button"
          onClick={onClose}
          aria-label="Close navigation"
          className="grid size-9 place-items-center rounded-lg text-slate-500 transition hover:bg-slate-100 dark:hover:bg-slate-800 lg:hidden"
        >
          <X size={18} aria-hidden="true" />
        </button>
      </div>

      {activeProject && (
        <label className="mb-5 block px-1">
          <span className="mb-2 block text-[11px] font-semibold uppercase tracking-[0.14em] text-slate-400">
            Project
          </span>
          <select
            aria-label="Active project"
            value={activeProject.id}
            onChange={(event) => selectProject(event.target.value)}
            disabled={projects.length < 2}
            className="min-h-11 w-full rounded-xl border border-border bg-surface px-3 text-sm font-medium disabled:opacity-80"
          >
            {projects.map((project) => (
              <option key={project.id} value={project.id}>
                {project.name}
              </option>
            ))}
          </select>
        </label>
      )}
      {profile?.role === "ADMIN" && (
        <form onSubmit={handleCreateProject} className="mb-5 space-y-2 px-1">
          <label className="block text-[11px] font-semibold uppercase tracking-[0.14em] text-slate-400">
            New project
            <input
              value={projectName}
              onChange={(event) => setProjectName(event.target.value)}
              minLength={2}
              maxLength={255}
              required
              placeholder="Project name"
              className="mt-2 min-h-10 w-full px-3 text-sm font-normal normal-case tracking-normal"
            />
          </label>
          <button type="submit" className="button-secondary min-h-9 w-full px-3 py-1 text-xs">
            <Plus size={14} aria-hidden="true" />
            Create project
          </button>
          {projectError && (
            <p role="alert" className="text-xs text-red-700 dark:text-red-300">
              {projectError}
            </p>
          )}
        </form>
      )}

      <div className="my-6 rounded-xl border border-border bg-surface-muted p-4">
        <p className="text-xs font-semibold uppercase tracking-[0.12em] text-accent-500">
          Made for careful work
        </p>
        <p className="mt-2 text-sm leading-5 text-slate-600 dark:text-slate-300">
          A steady place to organize research and annotation.
        </p>
      </div>

      <nav className="flex-1 space-y-7 overflow-y-auto" aria-label="Main navigation">
        {navigationSections.map((section) => (
          <div key={section.label}>
            <p className="mb-2 px-3 text-[11px] font-semibold uppercase tracking-[0.14em] text-slate-400">
              {section.label}
            </p>
            <ul className="space-y-1">
              {section.links
                .filter(
                  (link) =>
                    !link.roles ||
                    link.roles.includes(profile?.role ?? "ANNOTATOR"),
                )
                .map((link) => {
                  const active =
                    pathname === link.href ||
                    pathname.startsWith(`${link.href}/`);
                  const Icon = link.icon;
                  return (
                    <li key={link.href}>
                      <Link
                        href={link.href}
                        onClick={onClose}
                        aria-current={active ? "page" : undefined}
                        className={`group flex min-h-11 items-center gap-3 rounded-xl px-3 text-sm font-medium transition ${
                          active
                            ? "bg-accent-50 text-accent-500 dark:bg-accent-500/15"
                            : "text-slate-600 hover:bg-slate-100 hover:text-slate-950 dark:text-slate-300 dark:hover:bg-slate-800 dark:hover:text-white"
                        }`}
                      >
                        <Icon
                          size={18}
                          aria-hidden="true"
                          className={
                            active
                              ? "text-accent-500"
                              : "text-slate-400 transition group-hover:text-slate-600 dark:group-hover:text-slate-200"
                          }
                        />
                        {link.label}
                        {active && (
                          <span className="ml-auto size-1.5 rounded-full bg-accent-500" />
                        )}
                      </Link>
                    </li>
                  );
                })}
            </ul>
          </div>
        ))}
      </nav>

      <div className="mt-5 space-y-2 border-t border-slate-200 pt-4 dark:border-slate-800">
        <div className="flex min-w-0 items-center gap-3 px-2 py-2">
          <span className="grid size-10 shrink-0 place-items-center rounded-full bg-slate-100 text-sm font-semibold text-slate-600 dark:bg-slate-800 dark:text-slate-200">
            {profile?.full_name?.trim().charAt(0).toUpperCase() ?? "U"}
          </span>
          <div className="min-w-0">
            <p className="truncate text-sm font-medium">
              {profile?.full_name ?? "Your account"}
            </p>
            <p className="truncate text-xs capitalize text-slate-500 dark:text-slate-400">
              {profile?.role.replaceAll("_", " ").toLowerCase()}
            </p>
          </div>
        </div>
        <ThemeToggle />
        <button
          type="button"
          onClick={handleSignOut}
          className="flex min-h-11 w-full items-center gap-3 rounded-xl px-3 text-sm font-medium text-slate-600 transition hover:bg-slate-100 hover:text-slate-950 dark:text-slate-300 dark:hover:bg-slate-800 dark:hover:text-white"
        >
          <LogOut size={18} aria-hidden="true" className="text-slate-400" />
          Sign out
        </button>
      </div>
    </aside>
  );
}
