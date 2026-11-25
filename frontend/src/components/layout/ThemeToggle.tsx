"use client";

import { Moon, Sun } from "lucide-react";
import { useTheme } from "@/providers/ThemeProvider";

export default function ThemeToggle() {
  const { resolvedTheme, toggleTheme } = useTheme();
  const nextTheme = resolvedTheme === "dark" ? "light" : "dark";

  return (
    <button
      type="button"
      onClick={toggleTheme}
      className="flex w-full items-center gap-3 rounded-lg px-3 py-2 text-sm text-slate-600 hover:bg-slate-100 dark:text-slate-300 dark:hover:bg-slate-800"
      aria-label={`Switch to ${nextTheme} mode`}
    >
      {resolvedTheme === "dark" ? <Sun size={18} /> : <Moon size={18} />}
      <span>{nextTheme === "dark" ? "Dark mode" : "Light mode"}</span>
    </button>
  );
}
