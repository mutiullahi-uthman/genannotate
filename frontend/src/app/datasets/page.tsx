"use client";

import DatasetCard from "@/components/datasets/DatasetCard";
import CreateDatasetDialog from "@/components/datasets/CreateDatasetDialog";

import { useDatasets } from "@/hooks/useDatasets";
import { PageSkeleton } from "@/components/ui/Skeleton";
import { useAuth } from "@/providers/AuthProvider";

export default function DatasetsPage() {
  const { data, isLoading, isError } =
    useDatasets();
  const { profile } = useAuth();
  const canCreateDataset =
    profile?.role === "ADMIN" ||
    profile?.role === "SUPERVISOR" ||
    profile?.role === "RESEARCH_LEAD";

  if (isLoading) {
    return <PageSkeleton />;
  }

  if (isError || !data) {
    return (
      <p role="alert" className="text-red-700 dark:text-red-300">
        Datasets could not be loaded.
      </p>
    );
  }

  return (
    <div className="space-y-6">
      <header className="page-header flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <h1 className="page-title">Datasets</h1>
          <p className="page-description">
            Organize source files and keep each study’s annotation work in one place.
          </p>
        </div>
        {canCreateDataset && <CreateDatasetDialog />}
      </header>

      <div className="grid gap-4 sm:grid-cols-2 2xl:grid-cols-3">
        {data.map((dataset) => (
          <DatasetCard
            key={dataset.id}
            dataset={dataset}
          />
        ))}
      </div>
    </div>
  );
}