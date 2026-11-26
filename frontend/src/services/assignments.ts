import { api } from "@/services/api";

export type AssignmentCandidate = {
  id: string;
  record_id: string;
  language: string;
  instrument: string;
  item_id: string;
  item_text: string | null;
};

export type ProjectAnnotator = {
  id: string;
  full_name: string;
  email: string;
};

export async function getProjectAnnotators() {
  const response = await api.get<ProjectAnnotator[]>("/assignments/annotators");
  return response.data;
}

export async function getUnassignedRecords({
  datasetId,
  versionId,
}: {
  datasetId: string;
  versionId: string;
}) {
  const response = await api.get<AssignmentCandidate[]>(
    "/assignments/unassigned",
    {
      params: {
        dataset_id: datasetId,
        dataset_version_id: versionId,
      },
    },
  );
  return response.data;
}

export async function assignSelectedRecords({
  recordIds,
  assigneeId,
}: {
  recordIds: string[];
  assigneeId: string;
}) {
  const response = await api.post<{ assigned_count: number }>(
    "/assignments/manual-bulk",
    { record_ids: recordIds, assignee_id: assigneeId },
  );
  return response.data;
}

export async function distributeRecords({
  datasetId,
  versionId,
  assigneeIds,
  limit,
}: {
  datasetId: string;
  versionId: string;
  assigneeIds: string[];
  limit: number;
}) {
  const response = await api.post<{ assigned_count: number }>(
    "/assignments/bulk",
    {
      dataset_id: datasetId,
      dataset_version_id: versionId,
      assignee_ids: assigneeIds,
      limit,
    },
  );
  return response.data;
}
