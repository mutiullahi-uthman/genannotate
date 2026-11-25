import Link from "next/link";
import DataTable, {
  type DataTableColumn,
} from "@/components/ui/DataTable";
import type { QueueRecord } from "@/services/queue";

export default function QueueTable({
  records,
}: {
  records: QueueRecord[];
}) {
  const columns: DataTableColumn<QueueRecord>[] = [
    {
      key: "record",
      header: "Record",
      render: (record) => record.record_id,
    },
    {
      key: "language",
      header: "Language",
      render: (record) => record.language,
    },
    {
      key: "status",
      header: "Status",
      render: (record) => record.state,
    },
    {
      key: "open",
      header: "",
      render: (record) => (
        <Link
          href={`/queue/${record.id}`}
          className="font-medium text-blue-700 hover:underline dark:text-blue-300"
        >
          Open
        </Link>
      ),
    },
  ];

  return (
    <DataTable
      rows={records}
      columns={columns}
      rowKey={(record) => record.id}
      emptyMessage="No records are assigned to you."
    />
  );
}
