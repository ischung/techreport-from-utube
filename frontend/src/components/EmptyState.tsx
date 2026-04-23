import { SearchX } from "lucide-react";

interface EmptyStateProps {
  keyword: string;
  onRetry: () => void;
}

export function EmptyState({ keyword, onRetry }: EmptyStateProps) {
  return (
    <section
      className="mx-auto flex w-full max-w-xl flex-col items-center gap-4 rounded-lg border border-dashed border-border bg-bg-subtle p-10 text-center"
      data-testid="empty-state"
    >
      <span className="grid h-12 w-12 place-items-center rounded-full bg-fg-muted/10 text-fg-muted">
        <SearchX size={22} aria-hidden />
      </span>
      <div className="space-y-1">
        <h3 className="text-base font-medium text-fg">검색 결과가 없어요</h3>
        <p className="text-sm text-fg-muted">
          <span className="font-mono text-fg">"{keyword}"</span> 관련 최근 1개월 이내 영상을 찾지
          못했어요.
        </p>
        <p className="text-sm text-fg-muted">키워드를 바꿔서 다시 시도해보세요.</p>
      </div>
      <button
        type="button"
        onClick={onRetry}
        className="rounded-md border border-border bg-bg-card px-4 py-2 text-sm font-medium text-fg hover:bg-bg-subtle"
        data-testid="empty-state-retry"
      >
        다른 키워드로 검색
      </button>
    </section>
  );
}
