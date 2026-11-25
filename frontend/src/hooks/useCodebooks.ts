import {
  useMutation,
  useQuery,
  useQueryClient,
} from "@tanstack/react-query";
import {
  createCodebook,
  createCodebookLabel,
  deleteCodebookLabel,
  getCodebooks,
  updateCodebook,
  updateCodebookLabel,
} from "@/services/codebooks";

export function useCodebooks() {
  return useQuery({
    queryKey: ["codebooks"],
    queryFn: getCodebooks,
  });
}

function useInvalidateCodebooks() {
  const queryClient = useQueryClient();
  return () => queryClient.invalidateQueries({ queryKey: ["codebooks"] });
}

export function useCreateCodebook() {
  const invalidate = useInvalidateCodebooks();
  return useMutation({
    mutationFn: createCodebook,
    onSuccess: invalidate,
  });
}

export function useUpdateCodebook() {
  const invalidate = useInvalidateCodebooks();
  return useMutation({
    mutationFn: updateCodebook,
    onSuccess: invalidate,
  });
}

export function useCreateCodebookLabel() {
  const invalidate = useInvalidateCodebooks();
  return useMutation({
    mutationFn: createCodebookLabel,
    onSuccess: invalidate,
  });
}

export function useUpdateCodebookLabel() {
  const invalidate = useInvalidateCodebooks();
  return useMutation({
    mutationFn: updateCodebookLabel,
    onSuccess: invalidate,
  });
}

export function useDeleteCodebookLabel() {
  const invalidate = useInvalidateCodebooks();
  return useMutation({
    mutationFn: deleteCodebookLabel,
    onSuccess: invalidate,
  });
}
