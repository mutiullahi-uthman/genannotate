"use client";

import { useReports } from "@/hooks/useReports";
import { PageSkeleton } from "@/components/ui/Skeleton";

export default function ReportsPage() {
  const { data, isLoading, isError } =
    useReports();

  if (isLoading) {
    return <PageSkeleton />;
  }

  if (isError || !data) {
    return (
      <p role="alert" className="text-red-700 dark:text-red-300">
        Report metrics could not be loaded.
      </p>
    );
  }

  return (
    <div>
      <h1 className="mb-6 text-3xl font-bold">
        Reports
      </h1>

      <div className="grid grid-cols-3 gap-4">
        <Card
          title="Total Records"
          value={data.total_records}
        />

        <Card
          title="Assigned"
          value={data.assigned_records}
        />

        <Card
          title="Submitted"
          value={data.submitted_records}
        />

        <Card
          title="Approved"
          value={data.approved_records}
        />

        <Card
          title="Flagged"
          value={data.flagged_records}
        />
      </div>
    </div>
  );
}

function Card({
  title,
  value,
}: {
  title: string;
  value: number;
}) {
  return (
    <div className="rounded-lg border p-4">
      <p className="text-slate-500">
        {title}
      </p>

      <h2 className="text-3xl font-bold">
        {value}
      </h2>
    </div>
  );
}