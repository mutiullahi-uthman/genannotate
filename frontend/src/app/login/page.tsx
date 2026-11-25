"use client";

import {
  GoogleAuthProvider,
  signInWithPopup,
} from "firebase/auth";
import { ArrowRight, Leaf, ShieldCheck } from "lucide-react";
import { toast } from "sonner";

import { getFirebaseAuth } from "@/lib/firebase";

import { useRouter } from "next/navigation";

export default function LoginPage() {
  const router = useRouter();

  async function signIn() {
    try {
      const provider = new GoogleAuthProvider();
      await signInWithPopup(getFirebaseAuth(), provider);
      router.push("/dashboard");
    } catch (error) {
      toast.error(
        error instanceof Error
          ? error.message
          : "Sign-in failed. Please try again.",
      );
    }
  }

  return (
    <main className="flex min-h-screen items-center justify-center bg-background px-4 py-12">
      <section className="surface-card w-full max-w-md p-7 sm:p-10">
        <div className="mb-8 grid size-12 place-items-center rounded-xl bg-brand-100 text-brand-700">
          <Leaf size={22} aria-hidden="true" />
        </div>
        <p className="text-sm font-semibold text-accent-500">GenAnnotate workspace</p>
        <h1 className="mt-2 text-3xl font-bold tracking-tight">
          A workspace for careful annotation.
        </h1>
        <p className="mt-3 text-sm leading-6 text-slate-500 dark:text-slate-400">
          Organize datasets, annotate records, and review work together.
        </p>
        <button
          type="button"
          onClick={signIn}
          className="button-primary mt-8 w-full"
        >
          <svg
            aria-hidden="true"
            viewBox="0 0 24 24"
            className="size-[18px] shrink-0 rounded-full bg-white p-0.5"
          >
            <path
              fill="#4285F4"
              d="M23.49 12.27c0-.78-.07-1.54-.2-2.27H12v4.51h6.44c-.28 1.45-1.12 2.68-2.4 3.51v2.92h3.89c2.28-2.1 3.56-5.19 3.56-8.67z"
            />
            <path
              fill="#34A853"
              d="M12 24c3.24 0 5.95-1.08 7.93-2.93l-3.89-2.92c-1.08.72-2.46 1.15-4.04 1.15-3.11 0-5.74-2.1-6.68-4.93H1.3v3.01C3.28 21.31 7.31 24 12 24z"
            />
            <path
              fill="#FBBC05"
              d="M5.32 14.27c-.24-.72-.38-1.48-.38-2.27s.14-1.55.38-2.27V6.72H1.3C.47 8.37 0 10.12 0 12s.47 3.63 1.3 5.28l4.02-3.01z"
            />
            <path
              fill="#EA4335"
              d="M12 4.77c1.77 0 3.35.61 4.6 1.8l3.44-3.44C17.95 1.19 15.24 0 12 0 7.31 0 3.28 2.69 1.3 6.72l4.02 3.01C6.26 6.9 8.89 4.77 12 4.77z"
            />
          </svg>
          Continue with Google
          <ArrowRight size={17} aria-hidden="true" />
        </button>
        <p className="mt-5 flex items-center justify-center gap-2 text-center text-xs text-slate-500 dark:text-slate-400">
          <ShieldCheck size={15} aria-hidden="true" className="text-accent-500" />
          Secure sign-in for your research workspace
        </p>
      </section>
    </main>
  );
}