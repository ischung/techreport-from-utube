import App from "@/App";
import { render, screen, waitFor } from "@testing-library/react";
import { describe, expect, it } from "vitest";

describe("App / AppShell", () => {
  it("renders the brand title and header", () => {
    render(<App />);
    expect(screen.getAllByText(/TechReport/).length).toBeGreaterThan(0);
    expect(screen.getByText("Hello Dashboard")).toBeInTheDocument();
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
