import { useQuery } from "@tanstack/react-query";

import {
  getExportHistory,
} from "@/services/exports";

export function useExports(enabled = true) {
  return useQuery({
    queryKey: ["exports"],
    queryFn: getExportHistory,
    enabled,
    refetchInterval: (query) =>
      query.state.data?.some(
        (item) =>
          item.status === "PENDING" ||
          item.status === "GENERATING",
      )
        ? 2000
        : false,
  });
}