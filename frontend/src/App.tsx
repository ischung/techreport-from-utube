import { AppShell } from "@/components/AppShell";
import { ErrorBanner } from "@/components/ErrorBanner";
import { KeywordInputView } from "@/components/KeywordInputView";
import { VideoListView } from "@/components/VideoListView";
import { useAppStore } from "@/store/useAppStore";

export default function App() {
  const { phase, error, setError } = useAppStore();

  return (
    <AppShell>
      {error ? (
        <div className="mb-6">
          <ErrorBanner error={error} onRetry={() => setError(null)} />
        </div>
      ) : null}

      {phase === "input" ? <KeywordInputView /> : null}
      {phase === "list" ? <VideoListView /> : null}
      {phase === "analyzing" ? (
        <p className="text-center text-sm text-fg-muted">분석 UI는 #13에서 구현됩니다.</p>
      ) : null}
    </AppShell>
  );
}
