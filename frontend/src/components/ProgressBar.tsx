import { cn } from "@/lib/utils";

interface ProgressBarProps {
  value: number;
  label?: string;
  className?: string;
}

export function ProgressBar({ value, label, className }: ProgressBarProps) {
  const pct = Math.max(0, Math.min(100, value));
  return (
    <div className={cn("space-y-1", className)} data-testid="progress-bar">
      <div className="flex justify-between font-mono text-[11px] text-fg-subtle">
        <span>{label ?? "진행률"}</span>
        <span>{pct.toFixed(0)}%</span>
      </div>
      <div className="h-1.5 w-full overflow-hidden rounded-full bg-bg-card">
        <div
          className="h-full rounded-full bg-warn transition-[width] duration-500 ease-out"
          style={{ width: `${pct}%` }}
          aria-valuenow={pct}
          aria-valuemin={0}
          aria-valuemax={100}
          aria-label={label ?? "Analysis progress"}
        />
      </div>
    </div>
  );
}
