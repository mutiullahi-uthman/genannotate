import { api } from "@/services/api";

export type ImportJob = {
  id: string;
  status:
    | "PENDING"
    | "QUEUED"
    | "VALIDATING"
    | "VALIDATION_FAILED"
    | "VALIDATED"
    | "IMPORTING"
    | "COMPLETED"
    | "FAILED";
  total_rows: number;
  valid_rows: number;
  invalid_rows: number;
  error_message: string | null;
};

export async function getDatasetImportJobs(datasetId: string) {
  const response = await api.get<ImportJob[]>(
    `/imports/datasets/${datasetId}`,
  );
  return response.data;
}
