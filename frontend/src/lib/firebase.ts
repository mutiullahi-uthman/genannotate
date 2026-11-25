import { getApps, initializeApp, type FirebaseOptions } from "firebase/app";
import { getAuth, type Auth } from "firebase/auth";

const firebaseConfig: FirebaseOptions = {
  apiKey: process.env.NEXT_PUBLIC_FIREBASE_API_KEY,
  authDomain: process.env.NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN,
  projectId: process.env.NEXT_PUBLIC_FIREBASE_PROJECT_ID,
  storageBucket: process.env.NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET,
  messagingSenderId:
    process.env.NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID,
  appId: process.env.NEXT_PUBLIC_FIREBASE_APP_ID,
};

const requiredConfig = [
  ["NEXT_PUBLIC_FIREBASE_API_KEY", firebaseConfig.apiKey],
  ["NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN", firebaseConfig.authDomain],
  ["NEXT_PUBLIC_FIREBASE_PROJECT_ID", firebaseConfig.projectId],
  ["NEXT_PUBLIC_FIREBASE_APP_ID", firebaseConfig.appId],
] as const;

export function isFirebaseConfigured() {
  return requiredConfig.every(([, value]) => Boolean(value));
}

export function getFirebaseAuth(): Auth {
  const missingKeys = requiredConfig
    .filter(([, value]) => !value)
    .map(([key]) => key);
  if (missingKeys.length > 0) {
    throw new Error(
      `Firebase configuration is missing: ${missingKeys.join(", ")}`,
    );
  }

  const app =
    getApps().find((existingApp) => existingApp.name === "[DEFAULT]") ??
    initializeApp(firebaseConfig);
  return getAuth(app);
}
