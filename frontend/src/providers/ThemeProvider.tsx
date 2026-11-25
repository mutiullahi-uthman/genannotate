"use client";

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useSyncExternalStore,
} from "react";

export const themeOptions = [
  {
    id: "srhin-light",
    label: "SRHIN Light",
    description: "River blue and muted moss",
    mode: "light",
    group: "SRHIN",
  },
  {
    id: "srhin-dark",
    label: "SRHIN Dark",
    description: "Soft blue and lichen on pine",
    mode: "dark",
    group: "SRHIN",
  },
  {
    id: "midnight",
    label: "Stone",
    description: "Warm charcoal and quiet olive",
    mode: "dark",
    group: "More themes",
  },
  {
    id: "forest",
    label: "Forest",
    description: "Deep pine and soft leaf",
    mode: "dark",
    group: "More themes",
  },
] as const;

export type ThemeId = (typeof themeOptions)[number]["id"];
export type ThemeMode = (typeof themeOptions)[number]["mode"];

type ThemeContextValue = {
  theme: ThemeId;
  resolvedTheme: ThemeMode;
  setTheme: (theme: ThemeId) => void;
  toggleTheme: () => void;
};

const ThemeContext = createContext<ThemeContextValue>({
  theme: "srhin-light",
  resolvedTheme: "light",
  setTheme: () => undefined,
  toggleTheme: () => undefined,
});

const THEME_KEY = "genannotate-theme";
const THEME_EVENT = "genannotate-theme-change";

function isThemeId(value: string | null): value is ThemeId {
  return themeOptions.some((option) => option.id === value);
}

function getSnapshot(): ThemeId {
  const savedTheme = window.localStorage.getItem(THEME_KEY);
  if (isThemeId(savedTheme)) {
    return savedTheme;
  }

  if (savedTheme === "light") {
    return "srhin-light";
  }
  if (savedTheme === "dark") {
    return "srhin-dark";
  }

  return window.matchMedia("(prefers-color-scheme: dark)").matches
    ? "srhin-dark"
    : "srhin-light";
}

function getServerSnapshot(): ThemeId {
  return "srhin-light";
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
  const theme = useSyncExternalStore(
    subscribe,
    getSnapshot,
    getServerSnapshot,
  );
  const selectedTheme = themeOptions.find((option) => option.id === theme)!;

  useEffect(() => {
    document.documentElement.dataset.theme = theme;
    document.documentElement.classList.toggle(
      "dark",
      selectedTheme.mode === "dark",
    );
  }, [selectedTheme.mode, theme]);

  const setTheme = useCallback((nextTheme: ThemeId) => {
    window.localStorage.setItem(THEME_KEY, nextTheme);
    window.dispatchEvent(new Event(THEME_EVENT));
  }, []);

  const toggleTheme = useCallback(() => {
    setTheme(selectedTheme.mode === "dark" ? "srhin-light" : "srhin-dark");
  }, [selectedTheme.mode, setTheme]);

  const value = useMemo(
    () => ({
      theme,
      resolvedTheme: selectedTheme.mode,
      setTheme,
      toggleTheme,
    }),
    [selectedTheme.mode, setTheme, theme, toggleTheme],
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
