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
      className="block rounded-lg border p-4"
    >
      <h3 className="font-semibold">
        {dataset.name}
      </h3>

      <p className="text-sm text-slate-500">
        Version: {dataset.version}
      </p>

      <p className="text-sm text-slate-500">
        Status: {dataset.status}
      </p>
    </Link>
  );
}