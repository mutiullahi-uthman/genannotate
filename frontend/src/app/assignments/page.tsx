"use client";

import { useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { toast } from "sonner";
import RoleGuard from "@/components/auth/RoleGuard";
import { PageSkeleton } from "@/components/ui/Skeleton";
import { useDatasets } from "@/hooks/useDatasets";
import {
  assignSelectedRecords,
  distributeRecords,
  getProjectAnnotators,
  getUnassignedRecords,
} from "@/services/assignments";
import type { Dataset } from "@/services/datasets";

const EMPTY_VERSIONS: Dataset["versions"] = [];

export default function AssignmentsPage() {
  const queryClient = useQueryClient();
  const { data: datasets, isLoading: datasetsLoading } = useDatasets();
  const [datasetId, setDatasetId] = useState("");
  const [versionId, setVersionId] = useState("");
  const [selectedRecordIds, setSelectedRecordIds] = useState<string[]>([]);
  const [manualAssigneeId, setManualAssigneeId] = useState("");
  const [balancedAssigneeIds, setBalancedAssigneeIds] =
    useState<string[] | null>(null);
  const [limit, setLimit] = useState(100);

  const activeDatasetId =
    datasets?.some((dataset) => dataset.id === datasetId)
      ? datasetId
      : datasets?.[0]?.id ?? "";
  const selectedDataset = datasets?.find(
    (dataset) => dataset.id === activeDatasetId,
  );
  const versions = selectedDataset?.versions ?? EMPTY_VERSIONS;
  const activeVersionId =
    versions.some((version) => version.id === versionId)
      ? versionId
      : versions[versions.length - 1]?.id ?? "";

  const annotatorsQuery = useQuery({
    queryKey: ["project-annotators"],
    queryFn: getProjectAnnotators,
  });
  const annotators = annotatorsQuery.data ?? [];
  const defaultBalancedAssigneeIds = annotators.map(
    (annotator) => annotator.id,
  );
  const selectedBalancedAssigneeIds =
    balancedAssigneeIds ?? defaultBalancedAssigneeIds;
  const activeManualAssigneeId =
    manualAssigneeId || annotators[0]?.id || "";

  const recordsQuery = useQuery({
    queryKey: ["unassigned-records", activeDatasetId, activeVersionId],
    queryFn: () => getUnassignedRecords({
      datasetId: activeDatasetId,
      versionId: activeVersionId,
    }),
    enabled: Boolean(activeDatasetId && activeVersionId),
  });
  const records = recordsQuery.data ?? [];
  const recordIdSet = new Set(records.map((record) => record.id));
  const visibleSelectedIds = selectedRecordIds.filter((id) => recordIdSet.has(id));

  const refreshRecords = async () => {
    await queryClient.invalidateQueries({
      queryKey: ["unassigned-records", activeDatasetId, activeVersionId],
    });
    setSelectedRecordIds([]);
  };
  const manualMutation = useMutation({
    mutationFn: assignSelectedRecords,
    onSuccess: async ({ assigned_count }) => {
      toast.success(`${assigned_count} record${assigned_count === 1 ? "" : "s"} assigned.`);
      await refreshRecords();
    },
  });
  const balancedMutation = useMutation({
    mutationFn: distributeRecords,
    onSuccess: async ({ assigned_count }) => {
      toast.success(`${assigned_count} record${assigned_count === 1 ? "" : "s"} distributed.`);
      await refreshRecords();
    },
  });

  function toggleRecord(recordId: string) {
    setSelectedRecordIds((current) =>
      current.includes(recordId)
        ? current.filter((id) => id !== recordId)
        : [...current, recordId],
    );
  }

  function toggleAnnotator(annotatorId: string) {
    setBalancedAssigneeIds((current) => {
      const selected = current ?? defaultBalancedAssigneeIds;
      return selected.includes(annotatorId)
        ? selected.filter((id) => id !== annotatorId)
        : [...selected, annotatorId];
    });
  }

  if (datasetsLoading) return <PageSkeleton />;

  return (
    <RoleGuard roles={["ADMIN", "SUPERVISOR"]}>
      <div className="space-y-6">
        <header className="page-header">
          <h1 className="page-title">Record assignments</h1>
          <p className="page-description">
            Assign selected records to one annotator or distribute a dataset version evenly.
          </p>
        </header>

        <section className="surface-card grid gap-4 p-5 sm:grid-cols-2">
          <label className="space-y-2 text-sm font-medium">
            Dataset
            <select
              value={activeDatasetId}
              onChange={(event) => {
                setDatasetId(event.target.value);
                setVersionId("");
                setSelectedRecordIds([]);
              }}
              className="min-h-11 w-full rounded-lg border border-border bg-surface px-3"
            >
              {(datasets ?? []).map((dataset) => (
                <option key={dataset.id} value={dataset.id}>{dataset.name}</option>
              ))}
            </select>
          </label>
          <label className="space-y-2 text-sm font-medium">
            Imported version
            <select
              value={activeVersionId}
              onChange={(event) => {
                setVersionId(event.target.value);
                setSelectedRecordIds([]);
              }}
              disabled={!versions.length}
              className="min-h-11 w-full rounded-lg border border-border bg-surface px-3"
            >
              {versions.map((version) => (
                <option key={version.id} value={version.id}>{version.label}</option>
              ))}
            </select>
          </label>
        </section>

        <section className="surface-card space-y-4 p-5">
          <div>
            <h2 className="text-lg font-semibold">Balanced distribution</h2>
            <p className="mt-1 text-sm text-slate-500">
              Assign unassigned records round-robin across the selected project annotators.
            </p>
          </div>
          {annotatorsQuery.isError && (
            <p role="alert" className="text-sm text-red-700 dark:text-red-300">
              Annotators could not be loaded.
            </p>
          )}
          <div className="flex flex-wrap gap-3">
            {annotators.map((annotator) => (
              <label key={annotator.id} className="inline-flex items-center gap-2 text-sm">
                <input
                  type="checkbox"
                  checked={selectedBalancedAssigneeIds.includes(annotator.id)}
                  onChange={() => toggleAnnotator(annotator.id)}
                />
                {annotator.full_name}
              </label>
            ))}
            {!annotators.length && !annotatorsQuery.isLoading && (
              <p className="text-sm text-slate-500">No active annotators are members of this project.</p>
            )}
          </div>
          <div className="flex flex-col gap-3 sm:flex-row sm:items-end">
            <label className="space-y-2 text-sm font-medium">
              Maximum records
              <input
                type="number"
                min={1}
                max={5000}
                value={limit}
                onChange={(event) => {
                  const value = Number(event.target.value);
                  setLimit(Number.isFinite(value) ? value : 0);
                }}
                className="min-h-11 w-full rounded-lg border border-border bg-surface px-3 sm:w-40"
              />
            </label>
            <button
              type="button"
              disabled={!activeDatasetId || !activeVersionId || !selectedBalancedAssigneeIds.length || balancedMutation.isPending || !Number.isInteger(limit) || limit < 1 || limit > 5000}
              onClick={() => balancedMutation.mutate({
                datasetId: activeDatasetId,
                versionId: activeVersionId,
                assigneeIds: selectedBalancedAssigneeIds,
                limit,
              })}
              className="button-primary"
            >
              {balancedMutation.isPending ? "Distributing…" : "Distribute evenly"}
            </button>
          </div>
        </section>

        <section className="surface-card space-y-4 p-5">
          <div className="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
            <div>
              <h2 className="text-lg font-semibold">Manual assignment</h2>
              <p className="mt-1 text-sm text-slate-500">
                Select specific records and assign them to one annotator.
              </p>
            </div>
            <div className="flex flex-col gap-2 sm:flex-row">
              <select
                aria-label="Assign selected records to"
                value={activeManualAssigneeId}
                onChange={(event) => setManualAssigneeId(event.target.value)}
                className="min-h-11 rounded-lg border border-border bg-surface px-3 text-sm"
              >
                {annotators.map((annotator) => (
                  <option key={annotator.id} value={annotator.id}>
                    {annotator.full_name}
                  </option>
                ))}
              </select>
              <button
                type="button"
                disabled={!visibleSelectedIds.length || !activeManualAssigneeId || manualMutation.isPending}
                onClick={() => manualMutation.mutate({
                  recordIds: visibleSelectedIds,
                  assigneeId: activeManualAssigneeId,
                })}
                className="button-primary"
              >
                {manualMutation.isPending ? "Assigning…" : `Assign ${visibleSelectedIds.length} selected`}
              </button>
            </div>
          </div>
          {recordsQuery.isLoading ? (
            <p className="py-5 text-sm text-slate-500">Loading unassigned records…</p>
          ) : recordsQuery.isError ? (
            <p role="alert" className="py-5 text-sm text-red-700 dark:text-red-300">
              Unassigned records could not be loaded.
            </p>
          ) : records.length === 0 ? (
            <p className="py-5 text-sm text-slate-500">
              No unassigned records in this dataset version.
            </p>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full min-w-[42rem] text-left text-sm">
                <thead className="border-b border-border text-xs uppercase text-slate-500">
                  <tr>
                    <th className="w-12 py-3">
                      <input
                        type="checkbox"
                        aria-label="Select all visible records"
                        checked={records.every((record) => selectedRecordIds.includes(record.id))}
                        onChange={(event) => setSelectedRecordIds(
                          event.target.checked ? records.map((record) => record.id) : [],
                        )}
                      />
                    </th>
                    <th className="py-3">Record</th>
                    <th className="py-3">Language</th>
                    <th className="py-3">Instrument</th>
                    <th className="py-3">Item</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-border">
                  {records.map((record) => (
                    <tr key={record.id}>
                      <td className="py-3">
                        <input
                          type="checkbox"
                          aria-label={`Select record ${record.record_id}`}
                          checked={selectedRecordIds.includes(record.id)}
                          onChange={() => toggleRecord(record.id)}
                        />
                      </td>
                      <td className="py-3 font-medium">{record.record_id}</td>
                      <td className="py-3">{record.language}</td>
                      <td className="py-3">{record.instrument}</td>
                      <td className="py-3">{record.item_id}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </section>
      </div>
    </RoleGuard>
  );
}
