import { api } from "./api";

export type DashboardStats = {
  total_records: number;
  assigned_records: number;
  in_progress_records: number;
  submitted_records: number;
  approved_records: number;
  flagged_records: number;
};

export type LanguageStat = {
  language: string;
  count: number;
};

export async function getDashboardStats() {
  const response = await api.get<DashboardStats>(
    "/reports/dashboard"
  );

  return response.data;
}

export async function getAnnotatorStats() {
  const response = await api.get(
    "/reports/annotators"
  );

  return response.data;
}

export async function getDatasetStats() {
  const response = await api.get(
    "/reports/datasets"
  );

  return response.data;
}

export async function getLanguageStats() {
  const response = await api.get<LanguageStat[]>(
    "/reports/languages"
  );

  return response.data;
}