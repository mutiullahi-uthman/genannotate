import { useQuery } from "@tanstack/react-query";
import { getDatasetImportJobs } from "@/services/imports";

export function useDatasetImportJobs(datasetId: string) {
  return useQuery({
    queryKey: ["imports", datasetId],
    queryFn: () => getDatasetImportJobs(datasetId),
    enabled: Boolean(datasetId),
    refetchInterval: (query) =>
      query.state.data?.some(
        (job) =>
          job.status === "PENDING" ||
          job.status === "QUEUED" ||
          job.status === "VALIDATING" ||
          job.status === "IMPORTING",
      )
        ? 2000
        : false,
  });
}
