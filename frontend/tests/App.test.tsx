import App from "@/App";
import { useAppStore } from "@/store/useAppStore";
import { render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it } from "vitest";

describe("App / AppShell", () => {
  beforeEach(() => {
    useAppStore.getState().reset();
  });

  it("renders the brand title and starts in keyword-input phase", () => {
    render(<App />);
    expect(screen.getAllByText(/TechReport/).length).toBeGreaterThan(0);
    expect(screen.getByTestId("keyword-input")).toBeInTheDocument();
  });

  it("shows the health status dot eventually turning to Online", async () => {
    render(<App />);
    const dot = screen.getByTestId("status-dot");
    expect(dot).toBeInTheDocument();
    await waitFor(() => {
      expect(dot.getAttribute("data-status")).toBe("up");
    });
    expect(screen.getByText("Online")).toBeInTheDocument();
  });
});
