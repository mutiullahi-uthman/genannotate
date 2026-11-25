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

const chartColors = ["#2563eb", "#0d9488", "#f59e0b", "#8b5cf6", "#ef4444"];

export default function DashboardPage() {
  const { profile } = useAuth();
  const canViewReports =
    profile?.role === "ADMIN" ||
    profile?.role === "SUPERVISOR" ||
    profile?.role === "RESEARCH_LEAD";

  if (!canViewReports) {
    return (
      <section className="space-y-4">
        <h1 className="text-3xl font-bold">Dashboard</h1>
        <p className="text-slate-600 dark:text-slate-300">
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
      <p role="alert" className="text-red-700 dark:text-red-300">
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
    <div className="space-y-8">
      <header>
        <h1 className="text-3xl font-bold">Dashboard</h1>
        <p className="mt-2 text-slate-500">
          Current dataset and annotation activity.
        </p>
      </header>

      <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
        <MetricCard title="Total records" value={stats.total_records} />
        <MetricCard title="Assigned" value={stats.assigned_records} />
        <MetricCard title="In progress" value={stats.in_progress_records} />
        <MetricCard title="Submitted" value={stats.submitted_records} />
        <MetricCard title="Approved" value={stats.approved_records} />
        <MetricCard title="Flagged" value={stats.flagged_records} />
      </section>

      <section className="grid gap-6 xl:grid-cols-2">
        <div className="rounded-xl border border-slate-200 p-5 dark:border-slate-700">
          <h2 className="mb-4 text-lg font-semibold">Record workflow</h2>
          <div className="h-72">
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

        <div className="rounded-xl border border-slate-200 p-5 dark:border-slate-700">
          <h2 className="mb-4 text-lg font-semibold">Records by language</h2>
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={languages.data}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="language" />
                <YAxis allowDecimals={false} />
                <Tooltip />
                <Bar dataKey="count" fill="#2563eb" radius={[4, 4, 0, 0]} />
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
    <article className="rounded-xl border border-slate-200 p-5 dark:border-slate-700">
      <p className="text-sm text-slate-500">{title}</p>
      <p className="mt-2 text-3xl font-semibold">{value.toLocaleString()}</p>
    </article>
  );
}