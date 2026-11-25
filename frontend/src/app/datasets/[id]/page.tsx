"use client";

import {
  useParams,
} from "next/navigation";

import {
  useDataset,
} from "@/hooks/useDataset";

import UploadDatasetFile
from "@/components/datasets/UploadDatasetFile";

import ImportJobsTable
from "@/components/datasets/ImportJobsTable";
import { PageSkeleton } from "@/components/ui/Skeleton";

export default function DatasetDetailPage() {
  const params =
    useParams();

  const datasetId =
    params.id as string;

  const { data, isLoading, isError } =
    useDataset(
      datasetId
    );

  if (isLoading) {
    return <PageSkeleton />;
  }

  if (isError || !data) {
    return (
      <p role="alert" className="text-red-700 dark:text-red-300">
        Dataset details could not be loaded.
      </p>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">
          {data.name}
        </h1>

        <p>
          Version: {data.version}
        </p>
      </div>

      <UploadDatasetFile
        datasetId={datasetId}
      />

      <ImportJobsTable datasetId={datasetId} />
    </div>
  );
}