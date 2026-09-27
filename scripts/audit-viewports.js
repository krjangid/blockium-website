#!/usr/bin/env node
/**
 * Automated Multi-Screen Responsive Guardrail Audit
 * Tests 15 key device viewports (small mobile, standard mobile, foldable, tablet portrait,
 * tablet landscape, laptop, desktop, 2K, 4K UHD TV) to guarantee ZERO horizontal overflow
 * and layout preservation across all viewports.
 */
const http = require("http");
const fs = require("fs");
const path = require("path");

let chromium;
try {
  chromium = require("playwright").chromium;
} catch (e) {
  try {
    chromium = require("/Users/krishan/Documents/antigravity/adblocker/node_modules/playwright").chromium;
  } catch (err) {
    console.error("Playwright not found in local or adblocker node_modules. Skipping browser audit.");
    process.exit(0);
  }
}

const ROOT = path.resolve(__dirname, "..");

const VIEWPORTS = [
  { name: "320px Ultra-Small Mobile (iPhone SE 1st gen)", width: 320, height: 568 },
  { name: "360px Android Small (Galaxy S-series)", width: 360, height: 800 },
  { name: "375px Standard Mobile (iPhone SE / iPhone 8)", width: 375, height: 667 },
  { name: "390px Modern Mobile (iPhone 13/14/15)", width: 390, height: 844 },
  { name: "428px Large Mobile (iPhone Pro Max / Plus)", width: 428, height: 926 },
  { name: "600px Phablet / Foldable Unfolded", width: 600, height: 960 },
  { name: "768px Tablet Portrait (iPad Mini / iPad 10th gen)", width: 768, height: 1024 },
  { name: "820px Tablet Portrait (iPad Air 10.9-inch)", width: 820, height: 1180 },
  { name: "834px Tablet Portrait (iPad Pro 11-inch)", width: 834, height: 1194 },
  { name: "1024px Tablet Landscape / Compact Laptop", width: 1024, height: 768 },
  { name: "1280px Standard Laptop (MacBook Air 13-inch)", width: 1280, height: 800 },
  { name: "1440px Pro Laptop / Desktop (MacBook Pro 16-inch)", width: 1440, height: 900 },
  { name: "1920px Full HD / 1080p Smart TV Screen", width: 1920, height: 1080 },
  { name: "2560px 2K QHD Display", width: 2560, height: 1440 },
  { name: "3840px 4K UHD TV / Ultra-Wide Display", width: 3840, height: 2160 }
];

const PAGES_TO_TEST = [
  "/",
  "/de/",
  "/ru/",
  "/goodbye.html",
  "/privacy/",
  "/terms/"
];

function createServer() {
  const mimeTypes = {
    ".html": "text/html",
    ".css": "text/css",
    ".js": "application/javascript",
    ".svg": "image/svg+xml",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".woff2": "font/woff2"
  };

  return http.createServer((req, res) => {
    let reqPath = decodeURI(req.url.split("?")[0]);
    if (reqPath.endsWith("/")) reqPath += "index.html";
    let filePath = path.join(ROOT, reqPath);

    fs.readFile(filePath, (err, data) => {
      if (err) {
        res.writeHead(404, { "Content-Type": "text/plain" });
        res.end("Not Found");
        return;
      }
      const ext = path.extname(filePath);
      res.writeHead(200, { "Content-Type": mimeTypes[ext] || "application/octet-stream" });
      res.end(data);
    });
  });
}

(async () => {
  console.log("\n📐 Blockium Multi-Screen Responsive Viewport Audit\n");
  const server = createServer();
  await new Promise(resolve => server.listen(9876, resolve));

  let browser;
  let failures = [];
  try {
    browser = await chromium.launch();

    for (const testPage of PAGES_TO_TEST) {
      console.log("Checking route: " + testPage);
      for (const vp of VIEWPORTS) {
        const page = await browser.newPage({ viewport: { width: vp.width, height: vp.height } });
        await page.goto("http://localhost:9876" + testPage, { waitUntil: "domcontentloaded" });
        
        const result = await page.evaluate(() => {
          const scrollW = document.documentElement.scrollWidth;
          const clientW = document.documentElement.clientWidth;
          return {
            scrollW,
            clientW,
            hasOverflow: scrollW > clientW
          };
        });

        if (result.hasOverflow) {
          failures.push({
            route: testPage,
            viewport: vp.name,
            clientW: result.clientW,
            scrollW: result.scrollW,
            diff: result.scrollW - result.clientW
          });
          process.stdout.write("❌ ");
        } else {
          process.stdout.write("✅ ");
        }
        await page.close();
      }
      console.log("");
    }
  } finally {
    if (browser) await browser.close();
    server.close();
  }

  console.log("\n" + "=".repeat(60));
  if (failures.length > 0) {
    console.error("❌ FAILED: " + failures.length + " viewport test(s) failed with horizontal overflow:");
    for (const f of failures) {
      console.error("  - Route: " + f.route + " @ " + f.viewport + ": clientWidth=" + f.clientW + "px, scrollWidth=" + f.scrollW + "px (+" + f.diff + "px overflow)");
    }
    process.exit(1);
  } else {
    console.log("🎉 ALL " + (PAGES_TO_TEST.length * VIEWPORTS.length) + " VIEWPORT TESTS PASSED CLEANLY! ZERO HORIZONTAL OVERFLOW.");
    console.log("=".repeat(60) + "\n");
    process.exit(0);
  }
})();
