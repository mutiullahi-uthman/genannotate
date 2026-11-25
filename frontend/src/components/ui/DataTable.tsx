import type { ReactNode } from "react";

export type DataTableColumn<T> = {
  key: string;
  header: string;
  render: (row: T) => ReactNode;
};

type DataTableProps<T> = {
  rows: readonly T[] | undefined;
  columns: readonly DataTableColumn<T>[];
  rowKey: (row: T) => string;
  isLoading?: boolean;
  hasError?: boolean;
  errorMessage?: string;
  emptyMessage?: string;
};

export default function DataTable<T>({
  rows,
  columns,
  rowKey,
  isLoading = false,
  hasError = false,
  errorMessage = "Unable to load records.",
  emptyMessage = "No records found.",
}: DataTableProps<T>) {
  return (
    <div className="surface-card overflow-x-auto">
      <table className="w-full min-w-[36rem] text-left text-sm">
        <thead className="bg-surface-muted text-slate-600 dark:text-slate-300">
          <tr>
            {columns.map((column) => (
              <th key={column.key} scope="col" className="px-4 py-3 font-semibold">
                {column.header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="divide-y divide-border">
          {isLoading ? (
            Array.from({ length: 4 }, (_, row) => (
              <tr key={row} aria-label="Loading row">
                {columns.map((column) => (
                  <td key={column.key} className="px-4 py-4">
                    <span className="block h-4 animate-pulse rounded bg-slate-200 dark:bg-slate-700" />
                  </td>
                ))}
              </tr>
            ))
          ) : hasError ? (
            <tr>
              <td
                colSpan={columns.length}
                role="alert"
                className="px-4 py-10 text-center text-red-700 dark:text-red-300"
              >
                {errorMessage}
              </td>
            </tr>
          ) : rows?.length ? (
            rows.map((row) => (
              <tr
                key={rowKey(row)}
                className="bg-surface transition-colors hover:bg-surface-muted"
              >
                {columns.map((column) => (
                  <td key={column.key} className="px-4 py-3">
                    {column.render(row)}
                  </td>
                ))}
              </tr>
            ))
          ) : (
            <tr>
              <td
                colSpan={columns.length}
                className="px-4 py-10 text-center text-slate-500"
              >
                {emptyMessage}
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}
