"use client";

import { Check, Palette } from "lucide-react";
import { useRef } from "react";
import { themeOptions, useTheme } from "@/providers/ThemeProvider";

export default function ThemeToggle({
  compact = false,
}: {
  compact?: boolean;
}) {
  const { theme, setTheme } = useTheme();
  const detailsRef = useRef<HTMLDetailsElement>(null);
  const activeTheme = themeOptions.find((option) => option.id === theme);

  return (
    <details ref={detailsRef} className="group relative">
      <summary
        aria-label={`Color theme: ${activeTheme?.label ?? "SRHIN Light"}`}
        title={`Color theme: ${activeTheme?.label ?? "SRHIN Light"}`}
        className={`flex min-h-11 cursor-pointer list-none items-center gap-3 rounded-xl text-sm font-medium text-slate-600 transition hover:bg-slate-100 hover:text-slate-950 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-brand-600 dark:text-slate-300 dark:hover:bg-slate-800 dark:hover:text-white [&::-webkit-details-marker]:hidden ${
          compact ? "size-10 justify-center" : "w-full px-3"
        }`}
      >
        <Palette
          size={18}
          aria-hidden="true"
          className="shrink-0 text-brand-600 dark:text-brand-100"
        />
        {!compact && (
          <>
            <span>Appearance</span>
            <span className="ml-auto truncate text-xs text-slate-400">
              {activeTheme?.label}
            </span>
          </>
        )}
      </summary>
      <div
        className={`absolute bottom-full z-[60] mb-2 w-[min(18rem,calc(100vw-2rem))] rounded-2xl border border-border bg-surface p-2 shadow-xl shadow-black/10 ${
          compact ? "right-0" : "left-0"
        }`}
      >
        <p className="px-3 pb-2 pt-2 text-xs font-semibold uppercase tracking-[0.12em] text-slate-400">
          Color theme
        </p>
        <div role="radiogroup" aria-label="Color themes">
          {["SRHIN", "More themes"].map((group) => (
            <div key={group} className="py-1">
              {group === "More themes" && (
                <p className="px-3 pb-1 pt-2 text-[11px] font-medium text-slate-400">
                  {group}
                </p>
              )}
              {themeOptions
                .filter((option) => option.group === group)
                .map((option) => {
                  const selected = theme === option.id;
                  return (
                    <button
                      key={option.id}
                      type="button"
                      role="radio"
                      aria-checked={selected}
                      onClick={() => {
                        setTheme(option.id);
                        detailsRef.current?.removeAttribute("open");
                      }}
                      className={`flex min-h-12 w-full items-center gap-3 rounded-xl px-3 text-left transition focus-visible:outline-2 focus-visible:outline-offset-[-2px] focus-visible:outline-brand-600 ${
                        selected
                          ? "bg-brand-50 text-brand-700 dark:bg-brand-600/15 dark:text-brand-100"
                          : "text-slate-700 hover:bg-slate-50 dark:text-slate-200 dark:hover:bg-slate-800"
                      }`}
                    >
                      <span
                        aria-hidden="true"
                        className={`size-3 shrink-0 rounded-full ring-2 ring-offset-2 ring-offset-[var(--surface)] ${
                          option.id === "srhin-light"
                            ? "bg-[#486f79] ring-[#d9ded5]"
                            : option.id === "srhin-dark"
                              ? "bg-[#86aeb7] ring-[#a6b285]"
                              : option.id === "midnight"
                                ? "bg-[#c3a97b] ring-[#a1ae7c]"
                                : "bg-[#9bb18a] ring-[#b1aa76]"
                        }`}
                      />
                      <span className="min-w-0 flex-1">
                        <span className="block text-sm font-medium">
                          {option.label}
                        </span>
                        <span className="block text-xs text-slate-500 dark:text-slate-400">
                          {option.description}
                        </span>
                      </span>
                      {selected && (
                        <Check
                          size={16}
                          aria-hidden="true"
                          className="shrink-0 text-brand-600 dark:text-brand-100"
                        />
                      )}
                    </button>
                  );
                })}
            </div>
          ))}
        </div>
      </div>
    </details>
  );
}
