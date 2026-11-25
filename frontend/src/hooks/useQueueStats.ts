import { useQuery } from "@tanstack/react-query";

import { getQueueStats } from "@/services/queue";

export function useQueueStats() {
  return useQuery({
    queryKey: ["queue-stats"],

    queryFn: getQueueStats,
  });
}