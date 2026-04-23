import { searchVideos } from "@/lib/api";
import { useAppStore } from "@/store/useAppStore";
import { Search } from "lucide-react";
import { type FormEvent, useState } from "react";

export function KeywordInputView() {
  const [value, setValue] = useState("");
  const { setKeyword, setVideos, setError, setLoading, isLoading } = useAppStore();
  const trimmed = value.trim();
  const canSubmit = trimmed.length >= 2 && trimmed.length <= 100 && !isLoading;

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!canSubmit) return;
    setLoading(true);
    setError(null);
    setKeyword(trimmed);
    try {
      const videos = await searchVideos(trimmed);
      setVideos(videos);
    } catch (err) {
      const e = err as { code?: string; message?: string; retryable?: boolean };
      setError({
        code: e.code ?? "NETWORK",
        message: e.message ?? "검색 중 문제가 생겼어요. 잠시 후 다시 시도해주세요.",
        retryable: e.retryable ?? true,
      });
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="mx-auto w-full max-w-2xl space-y-6">
      <div>
        <h2 className="text-lg font-medium">키워드 검색</h2>
        <p className="mt-1 text-sm text-fg-muted">
          최근 1개월 이내 YouTube 영상 5개를 찾아드릴게요.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="flex items-center gap-2">
        <label htmlFor="keyword" className="sr-only">
          검색어
        </label>
        <div className="relative flex-1">
          <Search
            size={16}
            className="absolute left-3 top-1/2 -translate-y-1/2 text-fg-subtle"
            aria-hidden
          />
          <input
            id="keyword"
            name="keyword"
            data-testid="keyword-input"
            value={value}
            onChange={(e) => setValue(e.target.value)}
            placeholder='예) "OpenAI Harness Engineering"'
            minLength={2}
            maxLength={100}
            className="w-full rounded-md border border-border bg-bg-subtle py-2 pl-9 pr-3 text-sm placeholder:text-fg-subtle focus:border-accent focus:outline-none"
          />
        </div>
        <button
          type="submit"
          disabled={!canSubmit}
          data-testid="keyword-submit"
          className="rounded-md border border-border bg-bg-card px-4 py-2 text-sm font-medium text-fg hover:bg-bg-subtle disabled:cursor-not-allowed disabled:opacity-50"
        >
          {isLoading ? "검색 중…" : "검색"}
        </button>
      </form>

      <p className="font-mono text-xs text-fg-subtle">
        2–100자 · Enter 로 제출 · 최근 30일 이내 업로드만 노출
      </p>
    </section>
  );
}
