import { analyzeVideo } from "@/lib/api";
import { useAppStore } from "@/store/useAppStore";
import { Loader } from "lucide-react";
import { useEffect, useRef } from "react";

export function AnalyzingView() {
  const { videos, selectedVideoId, setReport, setError, setLoading, backToList } = useAppStore();
  const video = videos.find((v) => v.videoId === selectedVideoId);
  const startedRef = useRef(false);

  useEffect(() => {
    if (!video || startedRef.current) return;
    startedRef.current = true;
    setLoading(true);
    setError(null);

    analyzeVideo({
      videoId: video.videoId,
      title: video.title,
      url: video.url,
      publishedAt: video.publishedAt,
    })
      .then((report) => setReport(report))
      .catch((err: { code?: string; message?: string; retryable?: boolean }) => {
        setError({
          code: err.code ?? "ANALYSIS_FAILED",
          message: err.message ?? "분석 중 문제가 생겼어요.",
          retryable: err.retryable ?? true,
        });
        backToList();
      })
      .finally(() => setLoading(false));
  }, [video, setReport, setError, setLoading, backToList]);

  return (
    <section
      className="mx-auto w-full max-w-2xl space-y-6 text-center"
      data-testid="analyzing-view"
    >
      <div className="mx-auto grid h-12 w-12 place-items-center rounded-full bg-warn/10 text-warn">
        <Loader size={22} className="animate-spin" aria-hidden />
      </div>
      <div>
        <h2 className="text-lg font-medium">분석 중…</h2>
        <p className="mt-1 text-sm text-fg-muted">
          <span className="font-mono">"{video?.title ?? ""}"</span>
        </p>
        <p className="mt-3 font-mono text-xs text-fg-subtle">
          자막 수집 → LLM 구조화 → 마크다운 렌더링 → 파일 저장 (최대 3분)
        </p>
      </div>
    </section>
  );
}
