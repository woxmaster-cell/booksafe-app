import pw from '/opt/node22/lib/node_modules/playwright/index.js';
import fs from 'fs';
import path from 'path';
const { chromium } = pw;
const A = '/home/user/booksafe-app/assets';

const quellen = fs.readdirSync(A).filter(f => /^(de|en)-.*\.jpg$/.test(f)).sort();
quellen.push('app-icon.png');

const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto('about:blank');

let vorher = 0, nachher = 0;
for (const src of quellen) {
  const buf = fs.readFileSync(path.join(A, src));
  const mime = src.endsWith('.png') ? 'image/png' : 'image/jpeg';
  const dataUri = `data:${mime};base64,${buf.toString('base64')}`;
  const r = await page.evaluate(async ({ dataUri }) => {
    const img = new Image(); img.src = dataUri; await img.decode();
    const c = document.createElement('canvas');
    c.width = img.naturalWidth; c.height = img.naturalHeight;
    c.getContext('2d').drawImage(img, 0, 0);
    // 0.82 traf im Vergleich den Punkt, an dem die Schrift in den Screenshots
    // noch sauber steht; darunter franst der 11-px-Text in den Listen aus.
    return { d: c.toDataURL('image/webp', 0.82).split(',')[1], w: c.width, h: c.height };
  }, { dataUri });
  const out = path.join(A, src.replace(/\.(jpg|png)$/, '.webp'));
  fs.writeFileSync(out, Buffer.from(r.d, 'base64'));
  const a = buf.length, b = fs.statSync(out).size;
  vorher += a; nachher += b;
  console.log(`${src.padEnd(22)} ${r.w}x${r.h}  ${(a/1024).toFixed(0).padStart(4)} KB -> ${(b/1024).toFixed(0).padStart(4)} KB  (${(100-b/a*100).toFixed(0)}% weniger)`);
}

// apple-touch-icon: 180x180, aus der 1024er Fassung
const icon = fs.readFileSync(path.join(A, 'app-icon-1024.png'));
const t = await page.evaluate(async ({ d }) => {
  const img = new Image(); img.src = d; await img.decode();
  const c = document.createElement('canvas');
  c.width = 180; c.height = 180;
  const ctx = c.getContext('2d');
  ctx.imageSmoothingQuality = 'high';
  ctx.drawImage(img, 0, 0, 180, 180);
  return c.toDataURL('image/png').split(',')[1];
}, { d: `data:image/png;base64,${icon.toString('base64')}` });
fs.writeFileSync(path.join(A, 'apple-touch-icon.png'), Buffer.from(t, 'base64'));
console.log(`\napple-touch-icon.png    180x180  ${(fs.statSync(path.join(A,'apple-touch-icon.png')).size/1024).toFixed(0)} KB`);
console.log(`\nSumme Bilder: ${(vorher/1024).toFixed(0)} KB -> ${(nachher/1024).toFixed(0)} KB  (${(100-nachher/vorher*100).toFixed(0)}% weniger)`);
await browser.close();
