import type { ApiError } from "@/lib/types";
import { AlertCircle } from "lucide-react";

interface ErrorBannerProps {
  error: ApiError;
  onRetry?: () => void;
}

export function ErrorBanner({ error, onRetry }: ErrorBannerProps) {
  return (
    <div
      role="alert"
      data-testid="error-banner"
      className="mx-auto flex w-full max-w-2xl items-start gap-3 rounded-md border border-error/40 bg-error/10 p-4"
    >
      <AlertCircle size={18} className="mt-0.5 shrink-0 text-error" aria-hidden />
      <div className="flex-1 text-sm">
        <p className="font-medium text-error">{error.message}</p>
        <p className="mt-1 font-mono text-[11px] text-fg-muted">code: {error.code}</p>
      </div>
      {onRetry && error.retryable ? (
        <button
          type="button"
          onClick={onRetry}
          className="rounded border border-error/40 px-3 py-1 text-xs text-error hover:bg-error/20"
        >
          다시 시도
        </button>
      ) : null}
    </div>
  );
}
