import { useAppStore } from "@/store/useAppStore";
import { Check, Copy, FileText } from "lucide-react";
import { useState } from "react";

export function ReportResultView() {
  const { report, reset } = useAppStore();
  const [copied, setCopied] = useState(false);

  if (!report) {
    return <p className="text-center text-sm text-fg-muted">보고서가 준비되지 않았습니다.</p>;
  }

  async function handleCopyPath() {
    if (!report) return;
    try {
      await navigator.clipboard.writeText(report.savedPath);
      setCopied(true);
      setTimeout(() => setCopied(false), 1500);
    } catch {
      // no-op — clipboard may be blocked in test envs
    }
  }

  return (
    <section className="mx-auto w-full max-w-3xl space-y-6" data-testid="report-result">
      <header className="flex items-start justify-between gap-4">
        <div>
          <h2 className="text-lg font-medium">기술보고서</h2>
          <p className="mt-1 text-sm text-fg-muted">
            <span className="font-mono">{report.title}</span>
          </p>
        </div>
        <button
          type="button"
          onClick={reset}
          className="font-mono text-xs text-fg-subtle hover:text-fg"
        >
          ← 새 검색
        </button>
      </header>

      <div
        className="flex items-center gap-3 rounded-md border border-border bg-bg-card p-4"
        data-testid="saved-path"
      >
        <FileText size={16} className="text-accent" aria-hidden />
        <code className="flex-1 truncate font-mono text-xs text-fg">{report.savedPath}</code>
        <button
          type="button"
          onClick={handleCopyPath}
          className="flex items-center gap-1 rounded border border-border px-2 py-1 text-xs hover:bg-bg-subtle"
        >
          {copied ? <Check size={12} aria-hidden /> : <Copy size={12} aria-hidden />}
          {copied ? "복사됨" : "경로 복사"}
        </button>
      </div>

      <pre
        className="max-h-[60vh] overflow-auto rounded-lg border border-border bg-bg-card p-5 font-mono text-xs leading-relaxed text-fg"
        data-testid="markdown-preview"
      >
        {report.markdown}
      </pre>

      <p className="font-mono text-[11px] text-fg-subtle">
        llm={report.llmProvider} · generated={report.generatedAt}
      </p>
    </section>
  );
}
