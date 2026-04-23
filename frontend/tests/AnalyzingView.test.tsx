import { AnalyzingView } from "@/components/AnalyzingView";
import { useAppStore } from "@/store/useAppStore";
import { act, render, screen } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

describe("AnalyzingView", () => {
  beforeEach(() => {
    useAppStore.getState().reset();
    vi.useFakeTimers();
    // Seed the store with a video + selection so AnalyzingView has something to render
    useAppStore.setState({
      phase: "analyzing",
      videos: [
        {
          videoId: "abc",
          title: "Demo Video",
          url: "https://yt/x",
          publishedAt: "2026-04-15T00:00:00Z",
          channelTitle: "Demo",
        },
      ],
      selectedVideoId: "abc",
    });
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  it("renders spinner + video title + empty log placeholder at start", () => {
    render(<AnalyzingView />);
    expect(screen.getByText("분석 중…")).toBeInTheDocument();
    expect(screen.getByText("Demo Video")).toBeInTheDocument();
    expect(screen.getByTestId("progress-bar")).toBeInTheDocument();
    expect(screen.getByTestId("log-stream")).toBeInTheDocument();
  });

  it("pushes at least 3 log lines over time", () => {
    render(<AnalyzingView />);
    act(() => {
      vi.advanceTimersByTime(3_000);
    });
    const entries = useAppStore.getState().statusLog;
    expect(entries.length).toBeGreaterThanOrEqual(3);
    expect(entries[0].message).toContain("파이프라인");
  });
});
