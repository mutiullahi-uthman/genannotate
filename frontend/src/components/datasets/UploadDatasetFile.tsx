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
    <div className="space-y-3 rounded-lg border border-slate-200 p-4 dark:border-slate-700">
      <input
        type="file"
        disabled={uploading}
        onChange={(e) =>
          setFile(
            e.target.files?.[0] ?? null
          )
        }
      />

      <button
        type="button"
        onClick={upload}
        disabled={!file || uploading}
        className="ml-4 rounded-lg bg-slate-900 px-4 py-2 text-white disabled:opacity-50 dark:bg-white dark:text-slate-900"
      >
        {uploading ? "Uploading…" : "Upload and import"}
      </button>
      {errorMessage && (
        <p role="alert" className="whitespace-pre-wrap text-sm text-red-700 dark:text-red-300">
          {errorMessage}
        </p>
      )}
    </div>
  );
}