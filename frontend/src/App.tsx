import { AppShell } from "@/components/AppShell";

export default function App() {
  return (
    <AppShell>
      <section className="space-y-4">
        <h2 className="text-lg font-medium">Hello Dashboard</h2>
        <p className="max-w-2xl text-sm text-fg-muted">
          Phase 0-C Walking Skeleton. 사이드바 하단의 상태 도트가{" "}
          <span className="font-mono text-accent">emerald</span> 이면 백엔드{" "}
          <code className="rounded bg-bg-card px-1.5 py-0.5 font-mono text-xs">/api/health</code> 가
          응답하고 있다는 뜻입니다. 이후 Phase 1 (#11, #12, #13) 에서 키워드 입력 → 영상 리스트 →
          분석 보고서 흐름이 이 자리에 렌더링됩니다.
        </p>

        <dl className="grid max-w-md grid-cols-[auto_1fr] gap-x-6 gap-y-2 rounded-lg border border-border bg-bg-card p-5 text-sm">
          <dt className="text-fg-muted">Phase</dt>
          <dd className="font-mono">0-C · Walking Skeleton</dd>
          <dt className="text-fg-muted">Issue</dt>
          <dd className="font-mono">#7 (CI-7)</dd>
          <dt className="text-fg-muted">Backend</dt>
          <dd className="font-mono text-accent">/api/health → 200</dd>
        </dl>
      </section>
    </AppShell>
  );
}
