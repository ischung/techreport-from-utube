import { expect, test } from "@playwright/test";

test.describe("Walking Skeleton smoke", () => {
  test("dashboard loads and status dot turns online", async ({ page }) => {
    await page.goto("/");

    // Brand is visible — proves the SPA mounted
    await expect(page.getByText("TechReport").first()).toBeVisible();

    // The status dot eventually reports the backend as up ("Online")
    const dot = page.getByTestId("status-dot");
    await expect(dot).toBeVisible();
    await expect(dot).toHaveAttribute("data-status", "up", { timeout: 10_000 });
    await expect(dot).toContainText("Online");
  });
});
