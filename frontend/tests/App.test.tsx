import App from "@/App";
import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

describe("App", () => {
  it("renders brand title", () => {
    render(<App />);
    expect(screen.getByText("TechReport from YouTube")).toBeInTheDocument();
  });

  it("shows scaffolding status hint", () => {
    render(<App />);
    expect(screen.getByText(/Monorepo scaffolding complete/i)).toBeInTheDocument();
  });
});
