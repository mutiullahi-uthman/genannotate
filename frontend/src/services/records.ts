import { api } from "./api";

export async function getRecord(
  recordId: string
) {
  const response = await api.get(
    `/records/${recordId}`
  );

  return response.data;
}
