"use client";

export default function ErrorPage({
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <main className="mx-auto flex min-h-[50vh] max-w-xl flex-col items-center justify-center gap-4 text-center">
      <h1 className="text-2xl font-bold">Something went wrong</h1>
      <p className="text-slate-600 dark:text-slate-300">
        The page could not be loaded. Please try again.
      </p>
      <button
        type="button"
        onClick={reset}
        className="rounded-lg bg-slate-900 px-4 py-2 text-white dark:bg-white dark:text-slate-900"
      >
        Try again
      </button>
    </main>
  );
}
