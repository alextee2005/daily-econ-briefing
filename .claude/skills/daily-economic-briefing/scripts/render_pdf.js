// Render the briefing HTML to PDF via Chromium print-to-PDF.
// Usage: node render_pdf.js briefing.html Daily_Economic_Briefing_2026-09-16.pdf
//
// Margins are set HERE ONLY — the HTML must not also carry a CSS @page margin
// block, or the two stack and silently double.
// Do not run `playwright install`; point at the Chromium already present.

const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const [htmlArg, pdfArg] = process.argv.slice(2);
if (!htmlArg || !pdfArg) {
  console.error('Usage: node render_pdf.js <input.html> <output.pdf>');
  process.exit(1);
}

// Resolve whichever Chromium build this environment ships.
function findChromium() {
  if (process.env.CHROMIUM_PATH) return process.env.CHROMIUM_PATH;
  const root = process.env.PLAYWRIGHT_BROWSERS_PATH || '/opt/pw-browsers';
  const candidates = fs.existsSync(root)
    ? fs.readdirSync(root)
        .filter((d) => d.startsWith('chromium-'))
        // Chrome-for-Testing builds (Playwright >= ~1.5x) unpack to
        // chrome-linux64/; older builds to chrome-linux/. Try both.
        .flatMap((d) =>
          ['chrome-linux64', 'chrome-linux'].map((sub) => path.join(root, d, sub, 'chrome'))
        )
        .filter((p) => fs.existsSync(p))
    : [];
  if (!candidates.length) {
    throw new Error(`No Chromium found under ${root}; set CHROMIUM_PATH.`);
  }
  return candidates[0];
}

(async () => {
  const browser = await chromium.launch({
    executablePath: findChromium(),
    args: ['--no-sandbox'],
  });
  const page = await browser.newPage();
  await page.goto('file://' + path.resolve(htmlArg), { waitUntil: 'networkidle' });
  await page.pdf({
    path: path.resolve(pdfArg),
    format: 'Letter',
    printBackground: true,
    margin: { top: '1in', bottom: '1in', left: '13mm', right: '13mm' },
  });
  await browser.close();
  console.log('wrote', pdfArg);
})();
