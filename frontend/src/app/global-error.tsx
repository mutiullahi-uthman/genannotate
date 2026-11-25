"use client";

import "./globals.css";

export default function GlobalError({
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <html lang="en">
      <body>
        <main className="flex min-h-screen flex-col items-center justify-center gap-4 p-6 text-center">
          <h1 className="text-2xl font-bold">Application error</h1>
          <p>The application encountered an unexpected error.</p>
          <button
            type="button"
            onClick={reset}
            className="rounded-lg bg-slate-900 px-4 py-2 text-white"
          >
            Try again
          </button>
        </main>
      </body>
    </html>
  );
}
