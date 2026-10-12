import { mkdirSync, readFileSync } from "fs";
import { spawn } from "child_process";
import { createRequire } from "module";
import path from "path";
import { fileURLToPath, pathToFileURL } from "url";

const playwrightBin = process.env.PLAYWRIGHT ?? "/Users/dayu/Library/pnpm/playwright";
const shim = readFileSync(playwrightBin, "utf8");
const rel = shim.match(/"(\$basedir\/[^"]+\/playwright)\/cli\.js"/);
if (!rel) {
  console.error(`cannot locate playwright package from ${playwrightBin}`);
  process.exit(1);
}
const pkg = rel[1].replace("$basedir", path.dirname(playwrightBin));
const { chromium } = createRequire(import.meta.url)(pkg);

const outDir = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../out");

const htmlArg = process.argv[2];
if (!htmlArg) {
  console.error("usage: node print-png.mjs <html-file>");
  process.exit(1);
}

const htmlFile = path.resolve(htmlArg);
const stem = path.parse(htmlFile).name;
const pdfPath = path.join(outDir, `${stem}.pdf`);
const pngPattern = path.join(outDir, `${stem}-%02d.png`);

mkdirSync(outDir, { recursive: true });

const browser = await chromium.launch();
try {
  const page = await browser.newPage();
  try {
    await page.goto(pathToFileURL(htmlFile).href, {
      waitUntil: "networkidle",
      timeout: 30000,
    });
    await page.evaluate(() => document.fonts.ready);
    await page.pdf({
      path: pdfPath,
      format: "A4",
      printBackground: true,
      preferCSSPageSize: true,
    });
    console.log(pdfPath);
  } finally {
    await page.close();
  }
} finally {
  await browser.close();
}

await new Promise((resolve, reject) => {
  const child = spawn(
    "magick",
    [
      "-density",
      "300",
      pdfPath,
      "-background",
      "white",
      "-alpha",
      "remove",
      "-scene",
      "1",
      pngPattern,
    ],
    { stdio: "inherit" },
  );
  child.on("error", reject);
  child.on("close", (code) => {
    if (code === 0) resolve();
    else reject(new Error(`magick exited with code ${code}`));
  });
});

console.log(outDir);
