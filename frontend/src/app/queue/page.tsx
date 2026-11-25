"use client";

import QueueStats from "@/components/queue/QueueStats";
import QueueTable from "@/components/queue/QueueTable";

import { useQueue } from "@/hooks/useQueue";
import { useQueueStats } from "@/hooks/useQueueStats";
import { PageSkeleton } from "@/components/ui/Skeleton";

export default function QueuePage() {
  const queue =
    useQueue();

  const stats =
    useQueueStats();

  if (
    queue.isLoading ||
    stats.isLoading
  ) {
    return <PageSkeleton />;
  }

  if (queue.isError || stats.isError || !stats.data) {
    return (
      <p role="alert" className="text-red-700 dark:text-red-300">
        Your queue could not be loaded.
      </p>
    );
  }

  return (
    <div className="space-y-6">
      <header className="page-header">
        <h1 className="page-title">My Queue</h1>
        <p className="page-description">
          Your assigned records and annotation progress, all in one place.
        </p>
      </header>

      <QueueStats
        stats={stats.data}
      />

      <QueueTable
        records={queue.data ?? []}
      />
    </div>
  );
}