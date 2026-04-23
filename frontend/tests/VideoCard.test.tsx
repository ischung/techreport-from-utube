import { VideoCard } from "@/components/VideoCard";
import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

const sampleVideo = {
  videoId: "abc123",
  title: "OpenAI Harness Engineering Deep Dive",
  url: "https://www.youtube.com/watch?v=abc123",
  publishedAt: "2026-04-15T10:00:00Z",
  channelTitle: "Engineering Talks",
};

describe("VideoCard", () => {
  it("renders title, channel and formatted date", () => {
    render(<VideoCard video={sampleVideo} />);
    expect(screen.getByText(sampleVideo.title)).toBeInTheDocument();
    expect(screen.getByText(sampleVideo.channelTitle)).toBeInTheDocument();
    expect(screen.getByText(/2026-04-15/)).toBeInTheDocument();
  });

  it("calls onSelect with videoId when clicked", () => {
    const onSelect = vi.fn();
    render(<VideoCard video={sampleVideo} onSelect={onSelect} />);
    fireEvent.click(screen.getByTestId("video-card"));
    expect(onSelect).toHaveBeenCalledWith("abc123");
  });
});
