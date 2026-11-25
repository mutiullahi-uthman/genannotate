import Link from "next/link";
import type { Dataset } from "@/services/datasets";

type Props = {
  dataset: Dataset;
};

export default function DatasetCard({
  dataset,
}: Props) {
  return (
    <Link
      href={`/datasets/${dataset.id}`}
      className="surface-card group block p-5 transition-colors hover:border-brand-600/50 hover:bg-surface-muted focus-visible:outline-2 focus-visible:outline-brand-600"
    >
      <div className="flex items-start justify-between gap-4">
        <div className="min-w-0">
          <h3 className="truncate text-base font-semibold tracking-tight group-hover:text-brand-700 dark:group-hover:text-brand-100">
            {dataset.name}
          </h3>

          <p className="mt-2 text-sm text-slate-500 dark:text-slate-400">
            Version {dataset.version}
          </p>
        </div>

        <span className="shrink-0 rounded-full bg-accent-50 px-2.5 py-1 text-xs font-semibold text-accent-500">
          {dataset.status.replaceAll("_", " ")}
        </span>
      </div>
    </Link>
  );
}