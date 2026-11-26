import { api } from "./api";

export type Dataset = {
  id: string;
  name: string;
  status: string;
  language_coverage: string[];
  created_by_id: string;
  created_at: string;
  updated_at: string;
  latest_version: DatasetVersion | null;
  versions: DatasetVersion[];
};

export type DatasetVersion = {
  id: string;
  version_number: number;
  label: string;
  imported_at: string;
};

export async function getDatasets() {
  const response = await api.get<Dataset[]>("/datasets");

  return response.data;
}

export async function getDataset(
  datasetId: string
) {
  const response = await api.get<Dataset>(
    `/datasets/${datasetId}`
  );

  return response.data;
}

export async function createDataset(
  payload: {
    name: string;
    language_coverage: string[];
  }
) {
  const response = await api.post<Dataset>(
    "/datasets",
    payload
  );

  return response.data;
}