"use client";

import { useExports } from "@/hooks/useExports";
import DataTable, {
  type DataTableColumn,
} from "@/components/ui/DataTable";
import type { ExportHistoryItem } from "@/services/exports";
import { getExportDownloadUrl } from "@/services/exports";
import { toast } from "sonner";
import RoleGuard from "@/components/auth/RoleGuard";
import { useAuth } from "@/providers/AuthProvider";

export default function ExportsPage() {
  const { profile } = useAuth();
  const canViewExports =
    profile?.role === "ADMIN" ||
    profile?.role === "SUPERVISOR" ||
    profile?.role === "RESEARCH_LEAD";
  const { data, isLoading, isError } = useExports(canViewExports);

  async function downloadExport(exportId: string) {
    try {
      const { download_url } = await getExportDownloadUrl(exportId);
      const link = document.createElement("a");
      link.href = download_url;
      link.rel = "noopener noreferrer";
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      toast.error(
        error instanceof Error
          ? error.message
          : "The export could not be downloaded.",
      );
    }
  }

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
    {
      key: "download",
      header: "File",
      render: (item) => (
        <button
          type="button"
          disabled={item.status !== "COMPLETED"}
          onClick={() => void downloadExport(item.id)}
          className="button-secondary min-h-9 px-3 py-1 text-xs"
        >
          Download
        </button>
      ),
    },
  ];

  return (
    <RoleGuard roles={["ADMIN", "SUPERVISOR", "RESEARCH_LEAD"]}>
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
    </RoleGuard>
  );
}