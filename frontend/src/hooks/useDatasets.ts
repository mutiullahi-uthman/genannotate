import { useQuery } from "@tanstack/react-query";

import { getDatasets } from "@/services/datasets";

export function useDatasets() {
  return useQuery({
    queryKey: ["datasets"],
    queryFn: getDatasets,
  });
}
