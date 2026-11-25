"use client";

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useSyncExternalStore,
} from "react";

type ThemeContextValue = {
  resolvedTheme: "light" | "dark";
  toggleTheme: () => void;
};

const ThemeContext = createContext<ThemeContextValue>({
  resolvedTheme: "light",
  toggleTheme: () => undefined,
});

const THEME_EVENT = "genannotate-theme-change";

function getSnapshot(): "light" | "dark" {
  const savedTheme = window.localStorage.getItem("genannotate-theme");
  if (savedTheme === "light" || savedTheme === "dark") {
    return savedTheme;
  }
  return window.matchMedia("(prefers-color-scheme: dark)").matches
    ? "dark"
    : "light";
}

function getServerSnapshot(): "light" | "dark" {
  return "light";
}

function subscribe(onChange: () => void) {
  const media = window.matchMedia("(prefers-color-scheme: dark)");
  window.addEventListener("storage", onChange);
  window.addEventListener(THEME_EVENT, onChange);
  media.addEventListener("change", onChange);
  return () => {
    window.removeEventListener("storage", onChange);
    window.removeEventListener(THEME_EVENT, onChange);
    media.removeEventListener("change", onChange);
  };
}

export function ThemeProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  const resolvedTheme = useSyncExternalStore(
    subscribe,
    getSnapshot,
    getServerSnapshot,
  );

  useEffect(() => {
    document.documentElement.classList.toggle(
      "dark",
      resolvedTheme === "dark",
    );
  }, [resolvedTheme]);

  const toggleTheme = useCallback(() => {
    const nextTheme = resolvedTheme === "dark" ? "light" : "dark";
    window.localStorage.setItem("genannotate-theme", nextTheme);
    window.dispatchEvent(new Event(THEME_EVENT));
  }, [resolvedTheme]);

  const value = useMemo(
    () => ({ resolvedTheme, toggleTheme }),
    [resolvedTheme, toggleTheme],
  );

  return (
    <ThemeContext.Provider value={value}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  return useContext(ThemeContext);
}
