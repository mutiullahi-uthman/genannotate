"use client";

import DatasetCard from "@/components/datasets/DatasetCard";
import CreateDatasetDialog from "@/components/datasets/CreateDatasetDialog";

import { useDatasets } from "@/hooks/useDatasets";
import { PageSkeleton } from "@/components/ui/Skeleton";

export default function DatasetsPage() {
  const { data, isLoading, isError } =
    useDatasets();

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
    <div>
      <h1 className="mb-6 text-3xl font-bold">
        Datasets
      </h1>

      <CreateDatasetDialog />

      <div className="grid gap-4">
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