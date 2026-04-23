import { LogStream } from "@/components/LogStream";
import { ProgressBar } from "@/components/ProgressBar";
import { analyzeVideo } from "@/lib/api";
import { useAppStore } from "@/store/useAppStore";
import { Loader } from "lucide-react";
import { useEffect, useRef } from "react";

interface Step {
  /** at what progress % the message should appear */
  atPct: number;
  /** after which delay (ms from phase entry) to push the message */
  atMs: number;
  message: string;
}

const STEPS: Step[] = [
  { atMs: 0, atPct: 5, message: "파이프라인 시작" },
  { atMs: 600, atPct: 25, message: "자막 가져오는 중…" },
  { atMs: 2200, atPct: 50, message: "Claude Sonnet 으로 한국어 구조화 중…" },
  { atMs: 4500, atPct: 75, message: "마크다운으로 렌더링 중…" },
  { atMs: 6500, atPct: 90, message: "./reports 디렉토리에 저장 중…" },
];

export function AnalyzingView() {
  const { videos, selectedVideoId, statusLog, setReport, setError, backToList, pushLog } =
    useAppStore();
  const video = videos.find((v) => v.videoId === selectedVideoId);
  const startedRef = useRef(false);
  const progressRef = useRef(5);

  useEffect(() => {
    if (!video || startedRef.current) return;
    startedRef.current = true;

    const timers: ReturnType<typeof setTimeout>[] = [];
    for (const step of STEPS) {
      timers.push(
        setTimeout(() => {
          pushLog(step.message, "info");
          progressRef.current = step.atPct;
        }, step.atMs),
      );
    }

    analyzeVideo({
      videoId: video.videoId,
      title: video.title,
      url: video.url,
      publishedAt: video.publishedAt,
    })
      .then((report) => {
        pushLog(`저장 완료: ${report.savedPath}`, "success");
        setReport(report);
      })
      .catch((err: { code?: string; message?: string; retryable?: boolean }) => {
        const message = err.message ?? "분석 중 문제가 생겼어요.";
        pushLog(message, "error");
        setError({
          code: err.code ?? "ANALYSIS_FAILED",
          message,
          retryable: err.retryable ?? true,
        });
        backToList();
      });

    return () => {
      for (const t of timers) clearTimeout(t);
    };
  }, [video, setReport, setError, backToList, pushLog]);

  const progress = statusLog.length === 0 ? 5 : Math.max(progressRef.current, 10);

  return (
    <section className="mx-auto w-full max-w-2xl space-y-6" data-testid="analyzing-view">
      <header className="flex items-start gap-3">
        <div className="grid h-12 w-12 place-items-center rounded-full bg-warn/10 text-warn">
          <Loader size={22} className="animate-spin" aria-hidden />
        </div>
        <div>
          <h2 className="text-lg font-medium">분석 중…</h2>
          <p className="mt-1 text-sm text-fg-muted">
            <span className="font-mono">{video?.title ?? ""}</span>
          </p>
        </div>
      </header>

      <ProgressBar value={progress} label="Pipeline" />

      <LogStream entries={statusLog} />

      <p className="font-mono text-[11px] text-fg-subtle">
        파이프라인 단계: 자막 수집 → LLM 구조화 → 마크다운 렌더링 → 파일 저장 · 최대 3분 소요
      </p>
    </section>
  );
}
