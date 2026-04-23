import { cn } from "@/lib/utils";
import type { StatusLogEntry } from "@/store/useAppStore";
import { useEffect, useRef } from "react";

interface LogStreamProps {
  entries: StatusLogEntry[];
  className?: string;
}

const LEVEL_COLOR: Record<StatusLogEntry["level"], string> = {
  info: "text-fg-muted",
  success: "text-accent",
  error: "text-error",
};

function formatTime(): string {
  return new Date().toISOString().slice(11, 19);
}

export function LogStream({ entries, className }: LogStreamProps) {
  const ref = useRef<HTMLDivElement>(null);

  const length = entries.length;
  useEffect(() => {
    const el = ref.current;
    if (el && length > 0) {
      el.scrollTop = el.scrollHeight;
    }
  }, [length]);

  return (
    <div
      ref={ref}
      data-testid="log-stream"
      aria-live="polite"
      className={cn(
        "h-48 overflow-auto rounded-md border border-border bg-bg-subtle p-3 font-mono text-[13px] leading-relaxed",
        className,
      )}
    >
      {entries.length === 0 ? (
        <p className="text-fg-subtle">대기 중…</p>
      ) : (
        entries.map((entry) => (
          <div key={entry.id} className="flex gap-2">
            <span className="shrink-0 text-fg-subtle">{formatTime()}</span>
            <span className={LEVEL_COLOR[entry.level]}>{entry.message}</span>
          </div>
        ))
      )}
    </div>
  );
}
