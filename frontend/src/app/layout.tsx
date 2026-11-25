import { Suspense } from "react";
import "./globals.css";

import type { Metadata } from "next";
import Providers from "@/providers";
import AppShell from "@/components/layout/AppShell";
import { PageSkeleton } from "@/components/ui/Skeleton";

export const metadata: Metadata = {
  title: "GenAnnotate",
  description: "Collaborative annotation workspace",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>
        <Providers>
          <Suspense fallback={<PageSkeleton />}>
            <AppShell>{children}</AppShell>
          </Suspense>
        </Providers>
      </body>
    </html>
  );
}