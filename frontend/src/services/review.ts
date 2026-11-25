import { api } from "./api";
import type { QueueRecord } from "./queue";

export async function getReviewQueue() {
  const response = await api.get<QueueRecord[]>(
    "/review/queue"
  );

  return response.data;
}

export async function approveRecord(
  recordId: string
) {
  const response = await api.post(
    "/review/approve",
    {
      record_id: recordId,
    }
  );

  return response.data;
}

export async function returnRecord(
  payload: {
    record_id: string;
    comments: string;
    reason_for_change: string;
  }
) {
  const response = await api.post(
    "/review/return",
    payload
  );

  return response.data;
}