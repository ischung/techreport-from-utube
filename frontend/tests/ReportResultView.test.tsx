import { ReportResultView } from "@/components/ReportResultView";
import { useAppStore } from "@/store/useAppStore";
import { render, screen } from "@testing-library/react";
import { beforeEach, describe, expect, it } from "vitest";

describe("ReportResultView", () => {
  beforeEach(() => {
    useAppStore.getState().reset();
  });

  it("shows a placeholder when there is no report", () => {
    render(<ReportResultView />);
    expect(screen.getByText(/보고서가 준비되지 않았습니다/)).toBeInTheDocument();
  });

  it("renders saved path + markdown body once the report is set", () => {
    useAppStore.getState().setReport({
      videoId: "abc",
      title: "테스트 보고서",
      sourceUrl: "https://yt/x",
      publishedAt: "2026-04-15T00:00:00Z",
      generatedAt: "2026-04-24T08:00:00Z",
      llmProvider: "claude",
      sections: {
        overview: "overview",
        coreConcepts: ["a"],
        detailedContent: "body",
        lectureTips: "tips",
        references: [],
      },
      markdown: "# Test\n\nBody text.",
      savedPath: "./reports/2026-04-24-test.md",
    });

    render(<ReportResultView />);
    expect(screen.getByText("테스트 보고서")).toBeInTheDocument();
    expect(screen.getByText("./reports/2026-04-24-test.md")).toBeInTheDocument();
    expect(screen.getByTestId("markdown-preview").textContent).toContain("# Test");
    expect(screen.getByText(/llm=claude/)).toBeInTheDocument();
  });
});
