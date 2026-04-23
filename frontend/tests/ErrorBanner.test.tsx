import { ErrorBanner } from "@/components/ErrorBanner";
import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

describe("ErrorBanner", () => {
  it("renders as a warning for NO_TRANSCRIPT and shows the friendly CTA", () => {
    const onRetry = vi.fn();
    render(
      <ErrorBanner
        error={{ code: "NO_TRANSCRIPT", message: "자막이 없어요.", retryable: false }}
        onRetry={onRetry}
      />,
    );
    const banner = screen.getByTestId("error-banner");
    expect(banner.getAttribute("data-variant")).toBe("warning");

    const cta = screen.getByRole("button", { name: "다른 영상 선택" });
    fireEvent.click(cta);
    expect(onRetry).toHaveBeenCalledTimes(1);
  });

  it("renders as an error for retryable network failures", () => {
    render(
      <ErrorBanner
        error={{ code: "YOUTUBE_API_ERROR", message: "접속 불가.", retryable: true }}
        onRetry={() => {}}
      />,
    );
    const banner = screen.getByTestId("error-banner");
    expect(banner.getAttribute("data-variant")).toBe("error");
    expect(screen.getByRole("button", { name: "다시 시도" })).toBeInTheDocument();
  });

  it("hides the retry button when the error is neither a warning nor retryable", () => {
    render(
      <ErrorBanner error={{ code: "SAVE_FAILED", message: "저장 실패.", retryable: false }} />,
    );
    expect(screen.queryByRole("button")).toBeNull();
  });
});
