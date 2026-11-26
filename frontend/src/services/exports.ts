import { api } from "./api";

export type ExportHistoryItem = {
  id: string;
  export_identifier: string;
  export_format: "CSV" | "JSON";
  status: "PENDING" | "GENERATING" | "COMPLETED" | "FAILED";
  record_count: number;
};

export async function getExportHistory() {
  const response = await api.get<ExportHistoryItem[]>(
    "/exports/history"
  );

  return response.data;
}

export async function getExportDownloadUrl(exportId: string) {
  const response = await api.get<{
    download_url: string;
    expires_in_seconds: number;
  }>(`/exports/${exportId}/download`);
  return response.data;
}