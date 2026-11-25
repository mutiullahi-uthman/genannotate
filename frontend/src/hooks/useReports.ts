import { useQuery } from "@tanstack/react-query";

import {
  getDashboardStats,
  getLanguageStats,
} from "@/services/reports";

export function useReports() {
  return useQuery({
    queryKey: ["reports"],
    queryFn: getDashboardStats,
  });
}

export function useLanguageStats() {
  return useQuery({
    queryKey: ["reports", "languages"],
    queryFn: getLanguageStats,
  });
}