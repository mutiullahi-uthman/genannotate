import { useQuery } from "@tanstack/react-query";

import { getQueue } from "@/services/queue";

export function useQueue() {
  return useQuery({
    queryKey: ["queue"],

    queryFn: getQueue,
  });
}