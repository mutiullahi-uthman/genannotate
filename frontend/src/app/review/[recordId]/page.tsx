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
    <div className="space-y-4">
      <h1 className="text-2xl font-bold">
        Review Record
      </h1>

      <div className="rounded border p-6">
        Annotation Review Data
      </div>

      <button
        onClick={approve}
        className="rounded bg-green-600 px-4 py-2 text-white"
      >
        Approve
      </button>
    </div>
  );
}