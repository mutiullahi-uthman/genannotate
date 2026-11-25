import { api } from "./api";

export type QueueRecord = {
  id: string;
  record_id: string;
  language: string;
  instrument: string;
  item_id: string;
  item_text: string | null;
  transcript: string;
  state: string;
};

export type QueueStats = {
  assigned: number;
  in_progress: number;
  submitted: number;
  returned: number;
  flagged: number;
};

export async function getQueue() {
  const response = await api.get<QueueRecord[]>("/queue");

  return response.data;
}

export async function getQueueStats() {
  const response = await api.get<QueueStats>(
    "/queue/my-stats"
  );

  return response.data;
}

export async function getNextRecord() {
  const response = await api.get(
    "/queue/next"
  );

  return response.data;
}