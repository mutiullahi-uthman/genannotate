import { useQuery } from "@tanstack/react-query";

import {
  getExportHistory,
} from "@/services/exports";

export function useExports() {
  return useQuery({
    queryKey: ["exports"],
    queryFn: getExportHistory,
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