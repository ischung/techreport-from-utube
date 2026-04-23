import { expect, test } from "@playwright/test";
import { FIVE_VIDEOS, NO_TRANSCRIPT_ERROR } from "./fixtures";

test("video without transcript → warning ErrorBanner + back-to-list CTA", async ({ page }) => {
  await page.route("**/api/search", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify(FIVE_VIDEOS),
    });
  });
  await page.route("**/api/analyze", async (route) => {
    await route.fulfill({
      status: 422,
      contentType: "application/json",
      body: JSON.stringify(NO_TRANSCRIPT_ERROR),
    });
  });

  await page.goto("/");
  await page.getByTestId("keyword-input").fill("react");
  await page.getByTestId("keyword-submit").click();
  await page.getByTestId("video-card").first().click();

  const banner = page.getByTestId("error-banner");
  await expect(banner).toBeVisible({ timeout: 15_000 });
  await expect(banner).toHaveAttribute("data-variant", "warning");
  await expect(banner).toContainText("자막을 제공하지 않아");

  // "다른 영상 선택" dismisses the banner and keeps the user on the list
  await page.getByRole("button", { name: "다른 영상 선택" }).click();
  await expect(page.getByTestId("video-list")).toBeVisible();
});
