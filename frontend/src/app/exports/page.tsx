"use client";

import { useExports } from "@/hooks/useExports";
import DataTable, {
  type DataTableColumn,
} from "@/components/ui/DataTable";
import type { ExportHistoryItem } from "@/services/exports";

export default function ExportsPage() {
  const { data, isLoading, isError } = useExports();
  const columns: DataTableColumn<ExportHistoryItem>[] = [
    {
      key: "identifier",
      header: "Export",
      render: (item) => item.export_identifier,
    },
    {
      key: "format",
      header: "Format",
      render: (item) => item.export_format,
    },
    {
      key: "status",
      header: "Status",
      render: (item) => (
        <span className="inline-flex items-center gap-2">
          {(item.status === "PENDING" || item.status === "GENERATING") && (
            <span className="h-2 w-2 animate-pulse rounded-full bg-brand-600" />
          )}
          {item.status}
        </span>
      ),
    },
    {
      key: "records",
      header: "Records",
      render: (item) => item.record_count.toLocaleString(),
    },
  ];

  return (
    <div className="space-y-6">
      <header className="page-header">
        <h1 className="page-title">Export history</h1>
        <p className="page-description">
          Track generated files and monitor active exports. Progress refreshes automatically.
        </p>
      </header>
      <DataTable
        rows={data}
        columns={columns}
        rowKey={(item) => item.id}
        isLoading={isLoading}
        hasError={isError}
        emptyMessage="No exports have been created."
      />
    </div>
  );
}