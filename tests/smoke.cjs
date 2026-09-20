const { chromium } = require(process.env.PLAYWRIGHT_PACKAGE);
const path = require("path");

(async () => {
  const baseUrl = process.env.LESSON_URL;
  const screenshotDir = process.env.SCREENSHOT_DIR;
  if (!baseUrl || !screenshotDir) throw new Error("LESSON_URL and SCREENSHOT_DIR are required");

  const browser = await chromium.launch({ headless: true });
  const errors = [];

  async function check(viewport, filename) {
    const page = await browser.newPage({ viewportSize: viewport });
    page.on("console", message => {
      if (message.type() === "error" && !message.text().includes("Failed to load resource")) errors.push(message.text());
    });
    page.on("response", response => {
      if (response.status() >= 400 && !/\/assets\/slides\/slide_\d{3}_v2\.png$/.test(response.url())) {
        errors.push(response.status() + " " + response.url());
      }
    });
    page.on("pageerror", error => errors.push(error.message));
    const response = await page.goto(baseUrl, { waitUntil: "networkidle" });
    if (!response || !response.ok()) throw new Error("Page HTTP status is not OK");
    const facts = await page.evaluate(() => ({
      title: document.title,
      sections: document.querySelectorAll("main section").length,
      interactives: document.querySelectorAll(".interactive").length,
      slideDecks: document.querySelectorAll("[data-slide-range]").length,
      teacherNotes: document.querySelectorAll(".teacher-note").length,
      downloads: document.querySelectorAll("a.download").length,
      brokenImages: Array.from(document.images).filter(image => image.complete && image.naturalWidth === 0).length,
      horizontalOverflow: document.documentElement.scrollWidth > document.documentElement.clientWidth + 2
    }));
    await page.click("#teacherToggle");
    facts.teacherMode = await page.evaluate(() => document.body.classList.contains("teacher-mode"));
    await page.click("#sixGates [data-start]");
    await page.waitForTimeout(120);
    facts.gateStarted = await page.locator("#sixGates .route-step.active").count() > 0;
    await page.click("#deepfakeScenario [data-choice='known']");
    facts.deepfakeFeedback = await page.locator("#deepfakeScenario .feedback").textContent();
    await page.click("[data-slide-range='1-7'] [data-next]");
    await page.waitForTimeout(150);
    facts.placeholderAfterNext = await page.locator("[data-slide-range='1-7'] .slide-placeholder").count() === 1;
    await page.screenshot({ path: path.join(screenshotDir, filename), fullPage: true });
    await page.close();
    return facts;
  }

  const desktop = await check({ width: 1440, height: 1000 }, "dpo14-desktop.png");
  const mobile = await check({ width: 390, height: 844 }, "dpo14-mobile.png");
  await browser.close();

  if (desktop.interactives !== 10 || desktop.slideDecks !== 4 || desktop.downloads !== 4) {
    throw new Error("Required components are missing: " + JSON.stringify(desktop));
  }
  if (desktop.horizontalOverflow || mobile.horizontalOverflow) {
    throw new Error("Horizontal overflow detected: " + JSON.stringify({ desktop, mobile }));
  }
  if (!desktop.teacherMode || !desktop.gateStarted || !desktop.placeholderAfterNext || !desktop.deepfakeFeedback.includes("Верно")) {
    throw new Error("Interactive behavior failed: " + JSON.stringify(desktop));
  }
  if (errors.length) throw new Error("Browser errors: " + errors.join(" | "));
  console.log(JSON.stringify({ desktop, mobile, errors }, null, 2));
})();
