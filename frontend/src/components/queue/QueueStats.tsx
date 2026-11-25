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
    <div className="grid grid-cols-5 gap-4">
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
    <div className="rounded-lg border p-4">
      <div className="text-sm text-slate-500">
        {label}
      </div>

      <div className="text-2xl font-bold">
        {value}
      </div>
    </div>
  );
}