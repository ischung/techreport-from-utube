import type { HealthStatus } from "@/hooks/useHealth";
import { cn } from "@/lib/utils";

interface StatusDotProps {
  status: HealthStatus;
  label?: string;
  className?: string;
}

const COLOR_MAP: Record<HealthStatus, string> = {
  up: "bg-accent",
  degraded: "bg-warn",
  down: "bg-error",
  error: "bg-error",
  loading: "bg-fg-subtle animate-pulse",
};

const LABEL_MAP: Record<HealthStatus, string> = {
  up: "Online",
  degraded: "Degraded",
  down: "Offline",
  error: "Error",
  loading: "Checking…",
};

export function StatusDot({ status, label, className }: StatusDotProps) {
  return (
    <output
      className={cn("inline-flex items-center gap-2 text-xs font-mono", className)}
      aria-live="polite"
      data-testid="status-dot"
      data-status={status}
    >
      <span aria-hidden="true" className={cn("h-2 w-2 rounded-full", COLOR_MAP[status])} />
      <span className="text-fg-muted">{label ?? LABEL_MAP[status]}</span>
    </output>
  );
}
