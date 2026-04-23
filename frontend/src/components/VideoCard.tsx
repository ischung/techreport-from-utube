import type { VideoSearchResult } from "@/lib/types";
import { cn } from "@/lib/utils";
import { Clock, PlayCircle } from "lucide-react";

interface VideoCardProps {
  video: VideoSearchResult;
  selected?: boolean;
  onSelect?: (videoId: string) => void;
}

function formatDate(iso: string): string {
  try {
    return new Date(iso).toISOString().slice(0, 10);
  } catch {
    return iso.slice(0, 10);
  }
}

export function VideoCard({ video, selected = false, onSelect }: VideoCardProps) {
  return (
    <button
      type="button"
      data-testid="video-card"
      data-video-id={video.videoId}
      onClick={() => onSelect?.(video.videoId)}
      className={cn(
        "group flex w-full items-start gap-4 rounded-lg border bg-bg-card p-4 text-left transition",
        selected
          ? "border-accent shadow-[0_0_0_2px_rgba(34,197,94,0.3)]"
          : "border-border hover:border-fg-subtle",
      )}
    >
      <span className="mt-0.5 grid h-9 w-9 shrink-0 place-items-center rounded-md bg-error/10 text-error">
        <PlayCircle size={18} aria-hidden />
      </span>
      <div className="min-w-0 flex-1 space-y-1">
        <h3 className="truncate text-sm font-medium text-fg">{video.title}</h3>
        <p className="truncate font-mono text-xs text-fg-muted">{video.channelTitle}</p>
        <p className="flex items-center gap-1 font-mono text-[11px] text-fg-subtle">
          <Clock size={11} aria-hidden />
          {formatDate(video.publishedAt)}
        </p>
      </div>
    </button>
  );
}
