import pw from '/opt/node22/lib/node_modules/playwright/index.js';
const { chromium } = pw;
const S = '/tmp/claude-0/-home-user-booksafe-app/9799466c-a0b8-5488-9c9d-0d490bf9a8ca/scratchpad';
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1000, height: 620 }, deviceScaleFactor: 2 });
await page.setContent(`
<style>
 body{margin:0;background:#111;color:#eee;font:13px system-ui;display:flex;gap:12px;padding:12px}
 figure{margin:0;flex:1}
 figcaption{padding:6px 0}
 /* Ausschnitt der Listenzeilen: dort steht der kleinste Text (11 px im Original) */
 .crop{width:480px;height:520px;overflow:hidden;position:relative;border:1px solid #444}
 .crop img{position:absolute;left:-20px;top:-460px;width:960px;image-rendering:auto}
</style>
<figure><figcaption>JPEG · 146 KB</figcaption><div class="crop"><img src="file:///home/user/booksafe-app/assets/de-library.jpg"></div></figure>
<figure><figcaption>WebP · 53 KB</figcaption><div class="crop"><img src="file:///home/user/booksafe-app/assets/de-library.webp"></div></figure>
`);
await page.waitForTimeout(800);
await page.screenshot({ path: `${S}/webp-vergleich.png` });
await browser.close();
console.log('ok');
