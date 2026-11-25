"use client";

import { useState } from "react";
import axios from "axios";
import { useQueryClient } from "@tanstack/react-query";
import { toast } from "sonner";
import { api } from "@/services/api";

export default function UploadDatasetFile({
  datasetId,
}: {
  datasetId: string;
}) {
  const [file, setFile] =
    useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const queryClient = useQueryClient();

  async function upload() {
    if (!file || uploading) return;

    const formData =
      new FormData();

    formData.append(
      "file",
      file
    );

    setUploading(true);
    setErrorMessage(null);
    try {
      const uploadResponse = await api.post<{ id: string }>(
        `/uploads/datasets/${datasetId}`,
        formData,
      );
      const jobResponse = await api.post<{ job_id: string }>(
        `/imports/datasets/${datasetId}/files/${uploadResponse.data.id}`,
      );
      const validationResponse = await api.post<{
        success: boolean;
        errors: string[];
      }>(`/imports/${jobResponse.data.job_id}/validate`);

      await queryClient.invalidateQueries({
        queryKey: ["imports", datasetId],
      });

      if (!validationResponse.data.success) {
        setErrorMessage(
          validationResponse.data.errors.join("\n") ||
            "The uploaded file did not pass validation.",
        );
        return;
      }

      await api.post(`/imports/${jobResponse.data.job_id}/execute`);
      await queryClient.invalidateQueries({
        queryKey: ["imports", datasetId],
      });
      setFile(null);
      toast.success("Import started. Progress will update automatically.");
    } catch (error) {
      await queryClient.invalidateQueries({
        queryKey: ["imports", datasetId],
      });
      const detail = axios.isAxiosError(error)
        ? error.response?.data?.detail
        : null;
      const message =
        typeof detail === "string"
          ? detail
          : "Upload or import failed. Please try again.";
      setErrorMessage(message);
    } finally {
      setUploading(false);
    }
  }

  return (
    <section className="surface-card space-y-4 p-5 sm:p-6">
      <div>
        <h2 className="text-base font-semibold">Upload source file</h2>
        <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">
          Add a CSV, XLSX, or JSON file to validate and import.
        </p>
      </div>
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center">
        <input
          type="file"
          accept=".csv,.xlsx,.json"
          disabled={uploading}
          onChange={(e) =>
            setFile(
              e.target.files?.[0] ?? null
            )
          }
          className="min-h-11 w-full min-w-0 text-sm file:mr-3 file:rounded-lg file:border-0 file:bg-brand-50 file:px-3 file:py-2 file:text-sm file:font-semibold file:text-brand-700 dark:file:text-brand-100 sm:flex-1"
        />

        <button
          type="button"
          onClick={upload}
          disabled={!file || uploading}
          className="button-primary w-full sm:w-auto"
        >
          {uploading ? "Uploading…" : "Upload and import"}
        </button>
      </div>
      {errorMessage && (
        <p role="alert" className="whitespace-pre-wrap rounded-xl bg-red-50 p-3 text-sm text-red-700 dark:bg-red-950/40 dark:text-red-300">
          {errorMessage}
        </p>
      )}
    </section>
  );
}