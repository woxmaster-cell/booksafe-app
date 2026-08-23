import pw from '/opt/node22/lib/node_modules/playwright/index.js';
import fs from 'fs';
const { chromium } = pw;
const B = '/home/user/booksafe-app/design/og-card';
const browser = await chromium.launch();
let ok = true;
for (const code of ['de', 'en']) {
  // 1200 x 630 ist das Sollmass; deviceScaleFactor 2 liefert es scharf,
  // JPEG statt PNG, weil Vorschaubilder sonst unnoetig gross werden.
  // Genau 1200 x 630 ausgeben, nicht 2x: die og:image:width/height-Angaben im
  // HTML muessen zur Datei passen, sonst rechnen Scraper mit falschen Massen.
  const page = await browser.newPage({ viewport: { width: 1200, height: 630 }, deviceScaleFactor: 1 });
  await page.goto(`file://${B}/card-${code}.html`);
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(600);
  const m = await page.evaluate(() => {
    const c = document.querySelector('.card').getBoundingClientRect();
    const h1 = document.querySelector('h1').getBoundingClientRect();
    const sub = document.querySelector('.sub').getBoundingClientRect();
    const url = document.querySelector('.url').getBoundingClientRect();
    return {
      groesse: `${Math.round(c.width)}x${Math.round(c.height)}`,
      saira: document.fonts.check('800 68px Saira'),
      // nichts darf unten oder rechts aus der Karte laufen
      textPasst: sub.bottom < url.top && h1.right < c.right && sub.right < c.right,
      zeilen: Math.round(h1.height / (68 * 1.03)),
    };
  });
  const out = `${B}/og-${code}.jpg`;
  await page.locator('.card').screenshot({ path: out, type: 'jpeg', quality: 88 });
  await page.close();
  const kb = (fs.statSync(out).size / 1024).toFixed(0);
  const gut = m.groesse === '1200x630' && m.saira && m.textPasst && m.zeilen === 2;
  ok &&= gut;
  console.log(`${gut ? 'OK  ' : 'FEHLER'} og-${code}.jpg  ${m.groesse}  ${kb}KB  Schlagzeile:${m.zeilen} Zeilen  Saira:${m.saira}  Text passt:${m.textPasst}`);
}
await browser.close();
if (!ok) process.exit(1);
