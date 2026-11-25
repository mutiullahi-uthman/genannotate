type SkeletonProps = {
  className?: string;
};

export function Skeleton({ className = "" }: SkeletonProps) {
  return (
    <div
      aria-hidden="true"
      className={`animate-pulse rounded bg-slate-200 dark:bg-slate-700 ${className}`}
    />
  );
}

export function PageSkeleton() {
  return (
    <div className="space-y-6" aria-label="Loading page">
      <Skeleton className="h-9 w-56" />
      <Skeleton className="h-32 w-full" />
      <Skeleton className="h-64 w-full" />
    </div>
  );
}
