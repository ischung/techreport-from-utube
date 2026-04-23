import type { ApiError } from "@/lib/types";
import { cn } from "@/lib/utils";
import { AlertCircle, AlertTriangle } from "lucide-react";

interface ErrorBannerProps {
  error: ApiError;
  onRetry?: () => void;
}

/**
 * Error / warning banner. The variant is inferred from the error code so
 * that "user-recoverable" outcomes (e.g. NO_TRANSCRIPT) read as a warning
 * rather than a red-alert failure.
 */
function isWarning(code: string): boolean {
  return code === "NO_TRANSCRIPT";
}

export function ErrorBanner({ error, onRetry }: ErrorBannerProps) {
  const warn = isWarning(error.code);
  const Icon = warn ? AlertTriangle : AlertCircle;

  return (
    <div
      role="alert"
      data-testid="error-banner"
      data-variant={warn ? "warning" : "error"}
      className={cn(
        "mx-auto flex w-full max-w-2xl items-start gap-3 rounded-md border p-4",
        warn ? "border-warn/40 bg-warn/10" : "border-error/40 bg-error/10",
      )}
    >
      <Icon
        size={18}
        className={cn("mt-0.5 shrink-0", warn ? "text-warn" : "text-error")}
        aria-hidden
      />
      <div className="flex-1 text-sm">
        <p className={cn("font-medium", warn ? "text-warn" : "text-error")}>{error.message}</p>
        <p className="mt-1 font-mono text-[11px] text-fg-muted">code: {error.code}</p>
      </div>
      {onRetry && (warn || error.retryable) ? (
        <button
          type="button"
          onClick={onRetry}
          className={cn(
            "rounded border px-3 py-1 text-xs",
            warn
              ? "border-warn/40 text-warn hover:bg-warn/20"
              : "border-error/40 text-error hover:bg-error/20",
          )}
        >
          {warn ? "다른 영상 선택" : "다시 시도"}
        </button>
      ) : null}
    </div>
  );
}
