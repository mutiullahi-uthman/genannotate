"use client";

import Link from "next/link";
import DataTable, {
  type DataTableColumn,
} from "@/components/ui/DataTable";
import { PageSkeleton } from "@/components/ui/Skeleton";
import { useReviewQueue } from "@/hooks/useReviewQueue";
import type { QueueRecord } from "@/services/queue";

export default function ReviewPage() {
  const { data, isLoading, isError } = useReviewQueue();

  if (isLoading) {
    return <PageSkeleton />;
  }

  const columns: DataTableColumn<QueueRecord>[] = [
    {
      key: "record",
      header: "Record",
      render: (record) => record.record_id,
    },
    {
      key: "language",
      header: "Language",
      render: (record) => record.language,
    },
    {
      key: "status",
      header: "Status",
      render: (record) => record.state,
    },
    {
      key: "review",
      header: "",
      render: (record) => (
        <Link
          href={`/review/${record.id}`}
          className="font-medium text-blue-700 hover:underline dark:text-blue-300"
        >
          Review
        </Link>
      ),
    },
  ];

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Review Queue</h1>
      <DataTable
        rows={data}
        columns={columns}
        rowKey={(record) => record.id}
        hasError={isError}
        emptyMessage="No records are waiting for review."
      />
    </div>
  );
}
