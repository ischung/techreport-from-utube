import { EmptyState } from "@/components/EmptyState";
import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

describe("EmptyState", () => {
  it("renders the keyword in the message", () => {
    render(<EmptyState keyword="zzzxxxyyy" onRetry={() => {}} />);
    expect(screen.getByText(/검색 결과가 없어요/)).toBeInTheDocument();
    expect(screen.getByText(/zzzxxxyyy/)).toBeInTheDocument();
  });

  it("calls onRetry when the retry button is clicked", () => {
    const onRetry = vi.fn();
    render(<EmptyState keyword="zzz" onRetry={onRetry} />);
    fireEvent.click(screen.getByTestId("empty-state-retry"));
    expect(onRetry).toHaveBeenCalledTimes(1);
  });
});
