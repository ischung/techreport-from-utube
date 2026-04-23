import { VideoCard } from "@/components/VideoCard";
import { useAppStore } from "@/store/useAppStore";

export function VideoListView() {
  const { keyword, videos, selectedVideoId, selectVideo, reset } = useAppStore();

  return (
    <section className="mx-auto w-full max-w-3xl space-y-6">
      <header className="flex items-baseline justify-between">
        <div>
          <h2 className="text-lg font-medium">검색 결과</h2>
          <p className="mt-1 text-sm text-fg-muted">
            <span className="font-mono text-fg">"{keyword}"</span> 관련 최근 1개월 영상{" "}
            <span className="font-mono text-fg">{videos.length}</span> 건
          </p>
        </div>
        <button
          type="button"
          onClick={reset}
          className="font-mono text-xs text-fg-subtle hover:text-fg"
        >
          ← 다른 키워드로 검색
        </button>
      </header>

      <ul className="grid gap-3" data-testid="video-list">
        {videos.map((video) => (
          <li key={video.videoId}>
            <VideoCard
              video={video}
              selected={video.videoId === selectedVideoId}
              onSelect={selectVideo}
            />
          </li>
        ))}
      </ul>

      <p className="font-mono text-[11px] text-fg-subtle">
        영상을 하나 선택하면 다음 단계(분석)로 진행됩니다. (#12 에서 구현)
      </p>
    </section>
  );
}
