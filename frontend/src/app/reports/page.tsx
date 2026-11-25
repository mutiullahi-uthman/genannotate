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
      <header className="page-header">
        <h1 className="page-title">Reports</h1>
        <p className="page-description">
          A clear overview of annotation activity across your workspace.
        </p>
      </header>

      <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 xl:grid-cols-3">
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
    <div className="surface-card p-5 sm:p-6">
      <p className="text-sm font-medium text-slate-500 dark:text-slate-400">
        {title}
      </p>

      <h2 className="mt-3 text-3xl font-bold tracking-tight tabular-nums">
        {value}
      </h2>
    </div>
  );
}