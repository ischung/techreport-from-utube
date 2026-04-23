import "@testing-library/jest-dom";
import { vi } from "vitest";

// Default axios mock — individual tests override via vi.mocked / vi.doMock
vi.mock("axios", () => {
  return {
    default: {
      create: () => ({
        get: vi.fn().mockResolvedValue({
          data: { ok: true, data: { status: "up", llmProvider: "claude", version: "0.1.0" } },
        }),
      }),
    },
  };
});
