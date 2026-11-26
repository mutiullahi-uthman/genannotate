import { api } from "./api";

export type WorkspaceRecord = {
  id: string;
  dataset_id: string;
  dataset_version_id: string;
  record_id: string;
  language: string;
  instrument: string;
  item_id: string;
  item_text: string | null;
  transcript: string;
  audio_link: string | null;
  state: string;
};

export async function getRecord(recordId: string) {
  const response = await api.get<WorkspaceRecord>(`/records/${recordId}`);
  return response.data;
}
