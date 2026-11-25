import { useQuery } from "@tanstack/react-query";

import { getReviewQueue } from "@/services/review";

export function useReviewQueue() {
  return useQuery({
    queryKey: ["review-queue"],
    queryFn: getReviewQueue,
  });
}