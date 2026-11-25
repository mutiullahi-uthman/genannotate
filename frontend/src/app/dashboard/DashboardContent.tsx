"use client";

import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Legend,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { useReports, useLanguageStats } from "@/hooks/useReports";
import { useAuth } from "@/providers/AuthProvider";
import { PageSkeleton } from "@/components/ui/Skeleton";

const chartColors = [
  "var(--brand)",
  "var(--accent)",
  "#e9a23b",
  "#8b79c7",
  "#d76b70",
];

export default function DashboardContent() {
  const { profile } = useAuth();
  const canViewReports =
    profile?.role === "ADMIN" ||
    profile?.role === "SUPERVISOR" ||
    profile?.role === "RESEARCH_LEAD";

  if (!canViewReports) {
    return (
      <section className="space-y-3">
        <h1 className="page-title">Dashboard</h1>
        <p className="page-description">
          Your annotation queue and assigned work are available from the Queue page.
        </p>
      </section>
    );
  }

  return <ReportDashboard />;
}

function ReportDashboard() {
  const summary = useReports();
  const languages = useLanguageStats();

  if (summary.isLoading || languages.isLoading) {
    return <PageSkeleton />;
  }

  if (summary.isError || languages.isError || !summary.data || !languages.data) {
    return (
      <p role="alert" className="surface-card p-5 text-red-700 dark:text-red-300">
        Dashboard metrics could not be loaded. Please try again later.
      </p>
    );
  }

  const stats = summary.data;
  const states = [
    { name: "Assigned", value: stats.assigned_records },
    { name: "In progress", value: stats.in_progress_records },
    { name: "Submitted", value: stats.submitted_records },
    { name: "Approved", value: stats.approved_records },
    { name: "Flagged", value: stats.flagged_records },
  ];

  return (
    <div className="space-y-7">
      <header className="page-header">
        <p className="mb-2 text-xs font-semibold uppercase tracking-[0.16em] text-brand-700 dark:text-brand-100">
          Workspace overview
        </p>
        <h1 className="page-title">Dashboard</h1>
        <p className="page-description">
          A real-time view of your dataset and annotation activity.
        </p>
      </header>

      <section className="grid grid-cols-1 gap-3 sm:grid-cols-2 sm:gap-4 xl:grid-cols-3">
        <MetricCard title="Total records" value={stats.total_records} />
        <MetricCard title="Assigned" value={stats.assigned_records} />
        <MetricCard title="In progress" value={stats.in_progress_records} />
        <MetricCard title="Submitted" value={stats.submitted_records} />
        <MetricCard title="Approved" value={stats.approved_records} />
        <MetricCard title="Flagged" value={stats.flagged_records} />
      </section>

      <section className="grid gap-4 xl:grid-cols-2">
        <div className="surface-card min-w-0 p-4 sm:p-6">
          <div className="mb-5">
            <h2 className="text-base font-semibold">Record workflow</h2>
            <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">
              Current status across assigned records
            </p>
          </div>
          <div className="h-64 min-w-0 sm:h-72">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={states}
                  dataKey="value"
                  nameKey="name"
                  outerRadius={95}
                  label
                >
                  {states.map((state, index) => (
                    <Cell
                      key={state.name}
                      fill={chartColors[index % chartColors.length]}
                    />
                  ))}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="surface-card min-w-0 p-4 sm:p-6">
          <div className="mb-5">
            <h2 className="text-base font-semibold">Records by language</h2>
            <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">
              Distribution across your dataset
            </p>
          </div>
          <div className="h-64 min-w-0 sm:h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={languages.data}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="language" />
                <YAxis allowDecimals={false} />
                <Tooltip />
                <Bar dataKey="count" fill="var(--brand)" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </section>
    </div>
  );
}

function MetricCard({ title, value }: { title: string; value: number }) {
  return (
    <article className="surface-card min-w-0 p-4 sm:p-5">
      <p className="truncate text-sm font-medium text-slate-500 dark:text-slate-400">{title}</p>
      <p className="mt-2 text-2xl font-semibold tracking-tight tabular-nums sm:text-3xl">
        {value.toLocaleString()}
      </p>
    </article>
  );
}