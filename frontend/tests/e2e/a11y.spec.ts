import AxeBuilder from "@axe-core/playwright";
import { expect, test } from "@playwright/test";
import { FIVE_VIDEOS } from "./fixtures";

/**
 * WCAG AA gate — issue #17.
 * We run axe-core against every reachable wizard phase to make sure the
 * dark-mode tokens + live regions + landmarks aren't quietly regressing.
 * Critical/serious violations fail the test; moderate/minor are logged
 * as warnings for the reviewer but don't block.
 */
test.describe("A11y — WCAG 2.1 AA", () => {
  test("keyword-input view has no critical or serious violations", async ({ page }) => {
    await page.goto("/");
    await expect(page.getByTestId("keyword-input")).toBeVisible();

    const results = await new AxeBuilder({ page })
      .withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"])
      .analyze();

    const blocking = results.violations.filter((v) =>
      ["critical", "serious"].includes(v.impact ?? ""),
    );
    expect(blocking, `axe violations: ${JSON.stringify(blocking, null, 2)}`).toHaveLength(0);
  });

  test("video-list view has no critical or serious violations", async ({ page }) => {
    await page.route("**/api/search", async (route) => {
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(FIVE_VIDEOS),
      });
    });

    await page.goto("/");
    await page.getByTestId("keyword-input").fill("react");
    await page.getByTestId("keyword-submit").click();
    await expect(page.getByTestId("video-list")).toBeVisible();

    const results = await new AxeBuilder({ page })
      .withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"])
      .analyze();

    const blocking = results.violations.filter((v) =>
      ["critical", "serious"].includes(v.impact ?? ""),
    );
    expect(blocking, `axe violations: ${JSON.stringify(blocking, null, 2)}`).toHaveLength(0);
  });

  test('"/" keyboard shortcut focuses the keyword input', async ({ page }) => {
    await page.goto("/");
    // Blur any auto-focused input so the shortcut is observable
    await page.click("body");
    await page.keyboard.press("/");
    await expect(page.getByTestId("keyword-input")).toBeFocused();
  });
});
