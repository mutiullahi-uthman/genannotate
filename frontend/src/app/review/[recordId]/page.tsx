"use client";

import { useParams } from "next/navigation";

import {
  approveRecord,
} from "@/services/review";
import { toast } from "sonner";

export default function ReviewDetailPage() {
  const params =
    useParams();

  const recordId =
    params.recordId as string;

  async function approve() {
    await approveRecord(
      recordId
    );

    toast.success("Annotation approved.");
  }

  return (
    <div className="mx-auto max-w-5xl space-y-6">
      <header className="page-header">
        <p className="mb-2 text-xs font-semibold uppercase tracking-[0.16em] text-brand-700 dark:text-brand-100">
          Annotation quality
        </p>
        <h1 className="page-title">Review record</h1>
        <p className="page-description">
          Check the annotation carefully before approving it.
        </p>
      </header>

      <div className="surface-card min-h-48 p-5 sm:p-8">
        Annotation Review Data
      </div>

      <button
        onClick={approve}
        className="button-primary button-primary-accent"
      >
        Approve
      </button>
    </div>
  );
}