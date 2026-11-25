import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { getUsers, updateUser } from "@/services/users";

export function useUsers(enabled = true) {
  return useQuery({
    queryKey: ["users"],
    queryFn: getUsers,
    enabled,
  });
}

export function useUpdateUser() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: updateUser,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["users"] }),
  });
}
