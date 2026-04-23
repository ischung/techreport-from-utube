import { KeywordInputView } from "@/components/KeywordInputView";
import { useAppStore } from "@/store/useAppStore";
import { fireEvent, render, screen } from "@testing-library/react";
import { beforeEach, describe, expect, it } from "vitest";

describe("KeywordInputView", () => {
  beforeEach(() => {
    useAppStore.getState().reset();
  });

  it("disables submit when keyword is too short", () => {
    render(<KeywordInputView />);
    const submit = screen.getByTestId("keyword-submit");
    expect(submit).toBeDisabled();

    fireEvent.change(screen.getByTestId("keyword-input"), { target: { value: "r" } });
    expect(submit).toBeDisabled();
  });

  it("enables submit when keyword is ≥2 chars", () => {
    render(<KeywordInputView />);
    fireEvent.change(screen.getByTestId("keyword-input"), { target: { value: "react" } });
    expect(screen.getByTestId("keyword-submit")).not.toBeDisabled();
  });

  it("trims whitespace-only input", () => {
    render(<KeywordInputView />);
    fireEvent.change(screen.getByTestId("keyword-input"), { target: { value: "   " } });
    expect(screen.getByTestId("keyword-submit")).toBeDisabled();
  });
});
