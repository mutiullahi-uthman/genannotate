type Props = {
  stats: {
    assigned: number;
    in_progress: number;
    submitted: number;
    returned: number;
    flagged: number;
  };
};

export default function QueueStats({
  stats,
}: Props) {
  return (
    <div className="grid grid-cols-2 gap-3 sm:grid-cols-3 sm:gap-4 xl:grid-cols-5">
      <Stat
        label="Assigned"
        value={stats.assigned}
      />

      <Stat
        label="In Progress"
        value={stats.in_progress}
      />

      <Stat
        label="Submitted"
        value={stats.submitted}
      />

      <Stat
        label="Returned"
        value={stats.returned}
      />

      <Stat
        label="Flagged"
        value={stats.flagged}
      />
    </div>
  );
}

function Stat({
  label,
  value,
}: {
  label: string;
  value: number;
}) {
  return (
    <div className="surface-card min-w-0 p-4 sm:p-5">
      <div className="truncate text-xs font-medium text-slate-500 sm:text-sm dark:text-slate-400">
        {label}
      </div>

      <div className="mt-2 text-2xl font-bold tracking-tight tabular-nums sm:text-3xl">
        {value}
      </div>
    </div>
  );
}