import pw from '/opt/node22/lib/node_modules/playwright/index.js';
import fs from 'fs';
const { chromium } = pw;
const A = '/home/user/booksafe-app/assets';
const B = '/home/user/booksafe-app/design/og-card';
const jobs = [
  ['de-today.jpg', 'shot-today-de.jpg', 440],
  ['de-watch.jpg', 'shot-watch-de.jpg', 440],
  ['en-today.jpg', 'shot-today-en.jpg', 440],
  ['en-watch.jpg', 'shot-watch-en.jpg', 440],
];
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto('about:blank');
for (const [src, out, w] of jobs) {
  const dataUri = `data:image/jpeg;base64,${fs.readFileSync(`${A}/${src}`).toString('base64')}`;
  const b64 = await page.evaluate(async ({ dataUri, w }) => {
    const img = new Image(); img.src = dataUri; await img.decode();
    const s = Math.min(1, w / img.width);
    const c = document.createElement('canvas');
    c.width = Math.round(img.width * s); c.height = Math.round(img.height * s);
    const ctx = c.getContext('2d');
    ctx.imageSmoothingQuality = 'high';
    ctx.drawImage(img, 0, 0, c.width, c.height);
    return c.toDataURL('image/jpeg', 0.82).split(',')[1];
  }, { dataUri, w });
  fs.writeFileSync(`${B}/${out}`, Buffer.from(b64, 'base64'));
  console.log(`${src} -> ${out}  ${(fs.statSync(`${B}/${out}`).size/1024).toFixed(1)} KB`);
}
await browser.close();
