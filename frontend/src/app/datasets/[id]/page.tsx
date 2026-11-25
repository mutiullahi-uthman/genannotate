"use client";

import Link from "next/link";
import { ArrowLeft } from "lucide-react";
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
    <div className="space-y-7">
      <header className="page-header">
        <Link
          href="/datasets"
          className="mb-4 inline-flex min-h-10 items-center gap-2 rounded-lg text-sm font-medium text-slate-500 transition hover:text-brand-700 dark:text-slate-400 dark:hover:text-brand-100"
        >
          <ArrowLeft size={16} aria-hidden="true" />
          All datasets
        </Link>
        <div className="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <h1 className="page-title">{data.name}</h1>
            <p className="page-description">Dataset version {data.version}</p>
          </div>
          <span className="w-fit rounded-full bg-accent-50 px-3 py-1.5 text-xs font-semibold text-accent-500">
            {data.status.replaceAll("_", " ")}
          </span>
        </div>
      </header>

      <UploadDatasetFile
        datasetId={datasetId}
      />

      <ImportJobsTable datasetId={datasetId} />
    </div>
  );
}