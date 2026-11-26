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
import { api } from "@/services/api";
import { useQueryClient } from "@tanstack/react-query";
import { toast } from "sonner";
import { useState } from "react";
import axios from "axios";
import { useAuth } from "@/providers/AuthProvider";

export default function DatasetDetailPage() {
  const params =
    useParams();

  const datasetId =
    params.id as string;

  const { data, isLoading, isError } =
    useDataset(
      datasetId
    );
  const [exporting, setExporting] = useState<"CSV" | "JSON" | null>(null);
  const queryClient = useQueryClient();
  const { profile } = useAuth();
  const canManageDataset =
    profile?.role === "ADMIN" ||
    profile?.role === "SUPERVISOR" ||
    profile?.role === "RESEARCH_LEAD";
  const canExport = canManageDataset;

  async function requestExport(format: "CSV" | "JSON") {
    setExporting(format);
    try {
      await api.post(`/exports/${format.toLowerCase()}/${datasetId}`);
      await queryClient.invalidateQueries({ queryKey: ["exports"] });
      toast.success(`${format} export queued.`);
    } catch (error) {
      const detail = axios.isAxiosError(error)
        ? error.response?.data?.detail
        : null;
      toast.error(
        typeof detail === "string"
          ? detail
          : "The export could not be queued.",
      );
    } finally {
      setExporting(null);
    }
  }

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
            <p className="page-description">
              {data.latest_version
                ? `Latest imported version ${data.latest_version.label}`
                : "No successful imports yet"}
            </p>
          </div>
          <span className="w-fit rounded-full bg-accent-50 px-3 py-1.5 text-xs font-semibold text-accent-500">
            {data.status.replaceAll("_", " ")}
          </span>
        </div>
      </header>

      {canManageDataset && (
        <UploadDatasetFile datasetId={datasetId} />
      )}

      {canExport && data.versions.length > 0 && (
        <section className="surface-card flex flex-col gap-3 p-5 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <h2 className="font-semibold">Export annotations</h2>
            <p className="mt-1 text-sm text-slate-500">
              Generate a private, temporary-download CSV or JSON artifact.
            </p>
          </div>
          <div className="flex flex-col gap-2 sm:flex-row">
            {(["CSV", "JSON"] as const).map((format) => (
              <button
                key={format}
                type="button"
                disabled={exporting !== null}
                onClick={() => void requestExport(format)}
                className="button-secondary"
              >
                {exporting === format ? "Queueing…" : `Export ${format}`}
              </button>
            ))}
          </div>
        </section>
      )}

      <ImportJobsTable datasetId={datasetId} />
    </div>
  );
}