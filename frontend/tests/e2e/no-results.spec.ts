import { expect, test } from "@playwright/test";
import { ZERO_VIDEOS } from "./fixtures";

test("zero results → EmptyState + retry CTA", async ({ page }) => {
  await page.route("**/api/search", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify(ZERO_VIDEOS),
    });
  });

  await page.goto("/");
  await page.getByTestId("keyword-input").fill("zzzxxxyyy");
  await page.getByTestId("keyword-submit").click();

  const empty = page.getByTestId("empty-state");
  await expect(empty).toBeVisible();
  await expect(empty).toContainText("검색 결과가 없어요");
  await expect(empty).toContainText("zzzxxxyyy");

  // Retry CTA returns the user to the keyword input view
  await page.getByTestId("empty-state-retry").click();
  await expect(page.getByTestId("keyword-input")).toBeVisible();
});
