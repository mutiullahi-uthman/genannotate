import { useMutation } from "@tanstack/react-query";
import { useQueryClient } from "@tanstack/react-query";

import { createDataset } from "@/services/datasets";

export function useCreateDataset() {
  const queryClient =
    useQueryClient();

  return useMutation({
    mutationFn: createDataset,

    onSuccess() {
      queryClient.invalidateQueries({
        queryKey: ["datasets"],
      });
    },
  });
}