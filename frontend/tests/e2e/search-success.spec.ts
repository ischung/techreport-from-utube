import { expect, test } from "@playwright/test";
import { ANALYZE_OK, FIVE_VIDEOS } from "./fixtures";

test("search → pick → report Happy Path (mocked API)", async ({ page }) => {
  await page.route("**/api/search", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify(FIVE_VIDEOS),
    });
  });
  await page.route("**/api/analyze", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify(ANALYZE_OK),
    });
  });

  await page.goto("/");

  // Phase 1 — search
  await page.getByTestId("keyword-input").fill("react");
  await page.getByTestId("keyword-submit").click();

  // Phase 2 — video list
  const videoList = page.getByTestId("video-list");
  await expect(videoList).toBeVisible();
  const cards = page.getByTestId("video-card");
  await expect(cards).toHaveCount(5);

  // Phase 3 — pick one
  await cards.first().click();

  // Phase 4 — report lands (AnalyzingView transitions quickly because /analyze is mocked)
  const report = page.getByTestId("report-result");
  await expect(report).toBeVisible({ timeout: 15_000 });
  await expect(page.getByTestId("saved-path")).toContainText("2026-04-24-fixture-video-0.md");
  await expect(page.getByTestId("markdown-preview")).toContainText("# Fixture Video 0");
});
