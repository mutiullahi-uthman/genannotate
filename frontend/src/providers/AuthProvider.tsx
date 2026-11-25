"use client";

import {
  User,
  onAuthStateChanged,
  type Auth as FirebaseAuth,
} from "firebase/auth";

import {
  createContext,
  useContext,
  useEffect,
  useState,
} from "react";

import { getFirebaseAuth, isFirebaseConfigured } from "@/lib/firebase";
import {
  getCurrentUser,
  syncCurrentUser,
  type UserProfile,
} from "@/services/auth";

type AuthContextType = {
  user: User | null;
  profile: UserProfile | null;
  loading: boolean;
  error: string | null;
  refreshProfile: () => void;
};

const AuthContext =
  createContext<AuthContextType>({
    user: null,
    profile: null,
    loading: true,
    error: null,
    refreshProfile: () => undefined,
  });

export function AuthProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  const [user, setUser] =
    useState<User | null>(null);

  const [profile, setProfile] =
    useState<UserProfile | null>(null);

  const [loading, setLoading] =
    useState(isFirebaseConfigured());

  const [profileError, setProfileError] =
    useState<string | null>(null);

  useEffect(() => {
    let firebaseAuth: FirebaseAuth;
    try {
      firebaseAuth = getFirebaseAuth();
    } catch {
      queueMicrotask(() => setLoading(false));
      return;
    }

    const unsubscribe = onAuthStateChanged(
      firebaseAuth,
      async (firebaseUser) => {
        setUser(firebaseUser);
        if (!firebaseUser) {
          setProfile(null);
          setProfileError(null);
          setLoading(false);
          return;
        }

        setLoading(true);
        setProfileError(null);
        try {
          await syncCurrentUser();
          setProfile(await getCurrentUser());
        } catch (error) {
          setProfile(null);
          setProfileError(
            error instanceof Error
              ? error.message
              : "Your account profile could not be loaded.",
          );
        } finally {
          setLoading(false);
        }
      }
    );

    return () => unsubscribe();
  }, []);

  const refreshProfile = () => {
    if (user) {
      setLoading(true);
      setProfileError(null);
      void syncCurrentUser()
        .then(getCurrentUser)
        .then(setProfile)
        .catch((error: unknown) => {
          setProfile(null);
          setProfileError(
            error instanceof Error
              ? error.message
              : "Your account profile could not be loaded.",
          );
        })
        .finally(() => setLoading(false));
    }
  };

  const error = profileError;

  return (
    <AuthContext.Provider
      value={{
        user,
        profile,
        loading,
        error,
        refreshProfile,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}