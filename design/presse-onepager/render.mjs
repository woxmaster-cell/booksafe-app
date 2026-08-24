import pw from '/opt/node22/lib/node_modules/playwright/index.js';
import fs from 'fs';
const { chromium } = pw;
const B = '/home/user/booksafe-app/design/presse-onepager';
const jobs = [
  { src: 'onepager.html',    out: 'BookSafe-Presse-Onepager' },
  { src: 'onepager-en.html', out: 'BookSafe-Press-Onepager' },
];
const browser = await chromium.launch();
let alleOk = true;
for (const j of jobs) {
  const page = await browser.newPage({ viewport: { width: 900, height: 1300 }, deviceScaleFactor: 3 });
  await page.goto(`file://${B}/${j.src}`);
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(700);
  const m = await page.evaluate(() => {
    const sheet = document.querySelector('.sheet').getBoundingClientRect();
    const note = document.querySelector('.note').getBoundingClientRect();
    const foot = document.querySelector('footer').getBoundingClientRect();
    return {
      passt: Math.round(foot.bottom - sheet.top) <= Math.round(sheet.height),
      reserve: Math.round(foot.top - note.bottom),
      saira: document.fonts.check('800 38px Saira'),
      sans: document.fonts.check('400 16px "Source Sans 3"'),
    };
  });
  await page.locator('.sheet').screenshot({ path: `${B}/${j.out}.png` });
  await page.pdf({ path: `${B}/${j.out}.pdf`, format: 'A4', printBackground: true, preferCSSPageSize: true });
  await page.close();

  const pdf = fs.readFileSync(`${B}/${j.out}.pdf`).toString('latin1');
  const seiten = (pdf.match(/\/Type\s*\/Page[^s]/g) || []).length;
  const ok = m.passt && seiten === 1 && m.saira && m.sans;
  alleOk &&= ok;
  console.log(`${ok ? 'OK  ' : 'FEHLER'} ${j.out}  Seiten:${seiten}  Reserve:${m.reserve}px  ` +
              `PNG:${(fs.statSync(`${B}/${j.out}.png`).size/1024).toFixed(0)}KB  PDF:${(fs.statSync(`${B}/${j.out}.pdf`).size/1024).toFixed(0)}KB`);
}
await browser.close();
if (!alleOk) process.exit(1);
