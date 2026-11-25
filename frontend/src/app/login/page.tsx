"use client";

import {
  GoogleAuthProvider,
  signInWithPopup,
} from "firebase/auth";
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
    <main className="flex min-h-screen items-center justify-center">
      <button
        type="button"
        onClick={signIn}
        className="rounded-lg bg-slate-900 px-6 py-3 text-white dark:bg-white dark:text-slate-900"
      >
        Sign In With Google
      </button>
    </main>
  );
}