import pw from '/opt/node22/lib/node_modules/playwright/index.js';
import fs from 'fs';
const { chromium } = pw;
const B = '/home/user/booksafe-app/design/presse-onepager';
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 900, height: 1200 }, deviceScaleFactor: 3 });
await page.goto(`file://${B}/onepager.html`);
await page.evaluate(() => document.fonts.ready);
await page.waitForTimeout(800);

// Passt der Inhalt aufs Blatt?
const fit = await page.evaluate(() => {
  const s = document.querySelector('.sheet');
  const b = document.querySelector('.body');
  const f = document.querySelector('footer');
  return {
    sheetH: Math.round(s.getBoundingClientRect().height),
    inhaltH: Math.round(b.scrollHeight + document.querySelector('.masthead').getBoundingClientRect().height),
    ueberlauf: Math.round(b.scrollHeight - b.clientHeight),
    fussUnterkante: Math.round(f.getBoundingClientRect().bottom - s.getBoundingClientRect().top),
    saira: document.fonts.check('800 38px Saira'),
    sans: document.fonts.check('400 16px "Source Sans 3"'),
  };
});
console.log('Passung:', JSON.stringify(fit));

await page.locator('.sheet').screenshot({ path: `${B}/BookSafe-Presse-Onepager.png` });
await page.pdf({ path: `${B}/BookSafe-Presse-Onepager.pdf`, format: 'A4', printBackground: true, preferCSSPageSize: true });
await browser.close();

for (const f of ['BookSafe-Presse-Onepager.png', 'BookSafe-Presse-Onepager.pdf']) {
  console.log(f, (fs.statSync(`${B}/${f}`).size / 1024).toFixed(0), 'KB');
}
const pdf = fs.readFileSync(`${B}/BookSafe-Presse-Onepager.pdf`).toString('latin1');
console.log('PDF-Seiten:', (pdf.match(/\/Type\s*\/Page[^s]/g) || []).length);
