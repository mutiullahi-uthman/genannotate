import { useQuery } from "@tanstack/react-query";

import { getDataset } from "@/services/datasets";

export function useDataset(
  datasetId: string
) {
  return useQuery({
    queryKey: [
      "dataset",
      datasetId,
    ],

    queryFn: () =>
      getDataset(datasetId),

    enabled: !!datasetId,
  });
}