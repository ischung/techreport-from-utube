import { defineConfig, devices } from "@playwright/test";

/**
 * Playwright E2E config — issue #9 (CI-9).
 *
 * The test points at whatever URL `PLAYWRIGHT_BASE_URL` resolves to,
 * defaulting to the docker-compose frontend (http://localhost:80). The
 * GH Actions job in `.github/workflows/e2e.yml` brings the compose stack
 * up before invoking Playwright.
 *
 * Locally you can either
 *   (a) `docker compose up -d && pnpm --dir frontend test:e2e`
 *   (b) `pnpm --dir frontend dev` + point PLAYWRIGHT_BASE_URL at :5173
 */
export default defineConfig({
  testDir: "./tests/e2e",
  timeout: 30_000,
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 1 : 0,
  reporter: process.env.CI ? [["list"], ["html", { open: "never" }]] : "list",
  use: {
    baseURL: process.env.PLAYWRIGHT_BASE_URL ?? "http://localhost",
    trace: "retain-on-failure",
    screenshot: "only-on-failure",
  },
  projects: [
    {
      name: "chromium",
      use: { ...devices["Desktop Chrome"] },
    },
  ],
});
