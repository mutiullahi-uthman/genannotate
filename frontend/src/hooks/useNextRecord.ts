import { useQuery } from "@tanstack/react-query";

import { getNextRecord } from "@/services/queue";

export function useNextRecord() {
  return useQuery({
    queryKey: ["next-record"],

    queryFn: getNextRecord,
  });
}