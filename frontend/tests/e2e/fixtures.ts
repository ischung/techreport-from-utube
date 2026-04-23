/**
 * Response fixtures for Playwright route mocks.
 *
 * We intercept /api/* in the browser rather than hitting the real services
 * so the E2E suite stays deterministic, zero-cost, and <5 min.
 */

export const FIVE_VIDEOS = {
  ok: true,
  data: {
    videos: Array.from({ length: 5 }, (_, i) => ({
      videoId: `fxvid${i}`,
      title: `Fixture Video ${i} — LLM Deep Dive`,
      url: `https://www.youtube.com/watch?v=fxvid${i}`,
      publishedAt: "2026-04-15T10:00:00Z",
      channelTitle: `Engineering Talks ${i}`,
    })),
  },
};

export const ZERO_VIDEOS = {
  ok: true,
  data: { videos: [] },
};

export const NO_TRANSCRIPT_ERROR = {
  detail: {
    code: "NO_TRANSCRIPT",
    message: "해당 영상은 자막을 제공하지 않아 분석할 수 없어요. 다른 영상을 선택해주세요.",
    retryable: false,
  },
};

export const ANALYZE_OK = {
  ok: true,
  data: {
    videoId: "fxvid0",
    title: "Fixture Video 0 — LLM Deep Dive",
    sourceUrl: "https://www.youtube.com/watch?v=fxvid0",
    publishedAt: "2026-04-15T10:00:00Z",
    generatedAt: "2026-04-24T08:00:00Z",
    llmProvider: "claude",
    sections: {
      overview: "개요 문장.",
      coreConcepts: ["개념 A", "개념 B"],
      detailedContent: "상세 본문 Markdown.",
      lectureTips: "강의 팁.",
      references: ["https://example.com/ref"],
    },
    markdown:
      "# Fixture Video 0 — LLM Deep Dive\n\n## 개요\n\n개요 문장.\n\n## 핵심 개념\n\n- 개념 A\n- 개념 B\n",
    savedPath: "./reports/2026-04-24-fixture-video-0.md",
  },
};
