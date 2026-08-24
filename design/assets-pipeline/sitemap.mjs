// Erzeugt sitemap.xml. Das <lastmod> jeder Seite kommt aus dem letzten Commit,
// der genau diese Datei geaendert hat — damit stehen dort echte Daten statt
// eines Stands, den jemand von Hand nachziehen muesste.
//
//   node design/assets-pipeline/sitemap.mjs
//
// Danach `git diff sitemap.xml` ansehen: aendert sich nichts, war nichts noetig.

import { execFileSync } from 'child_process';
import fs from 'fs';
import path from 'path';

const WURZEL = path.resolve(import.meta.dirname, '../..');
const BASIS = 'https://booksafe.app';

// Jedes Paar ist dieselbe Seite in beiden Sprachen; die Prioritaet gilt fuer beide.
// x-default zeigt auf die deutsche Fassung: sie liegt unter der nackten URL und
// ist die Seite, die Besucher ohne passende Sprache bekommen sollen.
const PAARE = [
  { de: { pfad: 'index.html',            url: '/' },
    en: { pfad: 'en/index.html',         url: '/en/' },        prioritaet: '1.0' },
  { de: { pfad: 'presse/index.html',     url: '/presse/' },
    en: { pfad: 'en/press/index.html',   url: '/en/press/' },  prioritaet: '0.8' },
  { de: { pfad: 'support/index.html',    url: '/support/' },
    en: { pfad: 'en/support/index.html', url: '/en/support/' }, prioritaet: '0.6' },
];

const commitDatum = (datei) => {
  const d = execFileSync('git', ['log', '-1', '--format=%cs', '--', datei],
                         { cwd: WURZEL, encoding: 'utf8' }).trim();
  if (!/^\d{4}-\d{2}-\d{2}$/.test(d)) {
    throw new Error(`Kein Commit-Datum fuer ${datei} — noch nicht eingecheckt?`);
  }
  return d;
};

const zeilen = [
  '<?xml version="1.0" encoding="UTF-8"?>',
  '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
  '        xmlns:xhtml="http://www.w3.org/1999/xhtml">',
];

for (const { de, en, prioritaet } of PAARE) {
  for (const seite of [de, en]) {
    zeilen.push(
      '  <url>',
      `    <loc>${BASIS}${seite.url}</loc>`,
      `    <xhtml:link rel="alternate" hreflang="de" href="${BASIS}${de.url}"/>`,
      `    <xhtml:link rel="alternate" hreflang="en" href="${BASIS}${en.url}"/>`,
      `    <xhtml:link rel="alternate" hreflang="x-default" href="${BASIS}${de.url}"/>`,
      `    <lastmod>${commitDatum(seite.pfad)}</lastmod>`,
      `    <priority>${prioritaet}</priority>`,
      '  </url>',
    );
  }
}
zeilen.push('</urlset>');

fs.writeFileSync(path.join(WURZEL, 'sitemap.xml'), zeilen.join('\n') + '\n');
console.log(`sitemap.xml: ${PAARE.length * 2} Seiten`);
for (const { de, en } of PAARE) {
  console.log(`  ${de.url.padEnd(14)} ${commitDatum(de.pfad)}   ${en.url.padEnd(14)} ${commitDatum(en.pfad)}`);
}
