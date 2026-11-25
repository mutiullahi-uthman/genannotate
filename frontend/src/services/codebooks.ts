import { api } from "@/services/api";

export type CodebookLabel = {
  id: string;
  codebook_id: string;
  label_name: string;
  definition: string;
  inclusion_guidance: string | null;
  exclusion_guidance: string | null;
  examples: string | null;
};

export type Codebook = {
  id: string;
  name: string;
  version: string;
  status: "DRAFT" | "PUBLISHED" | "ARCHIVED";
  published_by_id: string | null;
  labels: CodebookLabel[];
};

export type CodebookLabelPayload = {
  label_name: string;
  definition: string;
  inclusion_guidance?: string;
  exclusion_guidance?: string;
  examples?: string;
};

export async function getCodebooks() {
  const response = await api.get<Codebook[]>("/codebooks");
  return response.data;
}

export async function createCodebook(payload: {
  name: string;
  version: string;
}) {
  const response = await api.post<Codebook>("/codebooks", payload);
  return response.data;
}

export async function updateCodebook({
  codebookId,
  ...payload
}: Partial<Pick<Codebook, "name" | "version" | "status">> & {
  codebookId: string;
}) {
  const response = await api.patch<Codebook>(
    `/codebooks/${codebookId}`,
    payload,
  );
  return response.data;
}

export async function createCodebookLabel({
  codebookId,
  ...payload
}: CodebookLabelPayload & { codebookId: string }) {
  const response = await api.post<CodebookLabel>(
    `/codebooks/${codebookId}/labels`,
    payload,
  );
  return response.data;
}

export async function updateCodebookLabel({
  codebookId,
  labelId,
  ...payload
}: Partial<CodebookLabelPayload> & {
  codebookId: string;
  labelId: string;
}) {
  const response = await api.patch<CodebookLabel>(
    `/codebooks/${codebookId}/labels/${labelId}`,
    payload,
  );
  return response.data;
}

export async function deleteCodebookLabel({
  codebookId,
  labelId,
}: {
  codebookId: string;
  labelId: string;
}) {
  await api.delete(`/codebooks/${codebookId}/labels/${labelId}`);
}
