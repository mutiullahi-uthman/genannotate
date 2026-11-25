import DataTable, {
  type DataTableColumn,
} from "@/components/ui/DataTable";
import { useDatasetImportJobs } from "@/hooks/useDatasetImportJobs";
import type { ImportJob } from "@/services/imports";

export default function ImportJobsTable({
  datasetId,
}: {
  datasetId: string;
}) {
  const { data: jobs, isLoading, isError } =
    useDatasetImportJobs(datasetId);

  const columns: DataTableColumn<ImportJob>[] = [
    {
      key: "id",
      header: "Job",
      render: (job) => job.id.slice(0, 8),
    },
    {
      key: "status",
      header: "Status",
      render: (job) => (
        <div>
          <span className="inline-flex items-center gap-2">
            {["PENDING", "QUEUED", "VALIDATING", "IMPORTING"].includes(
              job.status,
            ) && (
              <span className="h-2 w-2 animate-pulse rounded-full bg-blue-500" />
            )}
            {job.status.replaceAll("_", " ")}
          </span>
          {job.error_message && (
            <p className="mt-1 max-w-xs whitespace-pre-wrap text-xs text-red-700 dark:text-red-300">
              {job.error_message}
            </p>
          )}
        </div>
      ),
    },
    {
      key: "progress",
      header: "Progress",
      render: (job) => {
        const processed = job.valid_rows + job.invalid_rows;
        const active = [
          "PENDING",
          "QUEUED",
          "VALIDATING",
          "IMPORTING",
        ].includes(job.status);
        const percent = job.status === "COMPLETED" ? 100 : 0;
        return (
          <div className="min-w-32">
            <progress
              value={active ? undefined : percent}
              max={100}
              aria-label={
                active ? `${job.status.toLowerCase()} in progress` : `${percent}% complete`
              }
              className="h-2 w-full accent-blue-600"
            />
            <p className="mt-1 text-xs text-slate-500">
              {job.total_rows
                ? `${processed.toLocaleString()} validated / ${job.total_rows.toLocaleString()} rows`
                : active
                  ? "Processing"
                  : `${percent}%`}
            </p>
          </div>
        );
      },
    },
  ];

  return (
    <section className="space-y-3">
      <div>
        <h2 className="text-lg font-semibold">Import jobs</h2>
        <p className="text-sm text-slate-500">
          Active imports refresh automatically every two seconds.
        </p>
      </div>
      <DataTable
        rows={jobs}
        columns={columns}
        rowKey={(job) => job.id}
        isLoading={isLoading}
        hasError={isError}
        emptyMessage="No import jobs for this dataset."
      />
    </section>
  );
}