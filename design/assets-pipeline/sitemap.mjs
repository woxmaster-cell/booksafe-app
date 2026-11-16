// Erzeugt sitemap.xml. Das <lastmod> jeder Seite kommt aus dem letzten Commit,
// der den Inhalt dieser Datei geaendert hat. Reine Meta-Tags und der Footer
// zaehlen nicht: eine kuerzere Description oder ein zusaetzlicher Footer-Link
// hebt das Datum nicht an. So stehen dort echte Daten statt eines Stands,
// den jemand von Hand nachziehen muesste.
//
//   node design/assets-pipeline/sitemap.mjs
//
// Danach `git diff sitemap.xml` ansehen: aendert sich nichts, war nichts noetig.
//
// Die Seiten werden gesucht, nicht aufgezaehlt: jede index.html ausserhalb von
// design/ kommt hinein, ausser sie traegt noindex. Eine feste Liste war hier
// schon einmal veraltet (es fehlten 1.8, Archiv, Ratgeber, Autoren, Android-
// Support) und haette beim naechsten Lauf Seiten aus der Sitemap geloescht.
// Die Sprachpaare stehen in jeder Seite selbst (<link rel="alternate" hreflang>)
// und werden von dort uebernommen, damit Seite und Sitemap nie auseinanderlaufen.

import { execFileSync } from 'child_process';
import fs from 'fs';
import path from 'path';

const WURZEL = path.resolve(import.meta.dirname, '../..');
const BASIS = 'https://booksafe.app';
const AUSGESCHLOSSEN = new Set(['design', 'assets', 'node_modules', '.git']);

const versionsSeite = /^\/(?:neu-in|en\/whats-new)-(\d+)-(\d+)\/$/;

// Prioritaeten nach Seitenart. Die zwei neuesten Versionsseiten zaehlen mehr,
// aeltere treten zurueck — das muss beim naechsten Release niemand nachziehen.
const prioritaet = (url, neuesteVersionen) => {
  if (url === '/' || url === '/en/') return '1.0';
  const v = url.match(versionsSeite);
  if (v) return neuesteVersionen.includes(`${v[1]}.${v[2]}`) ? '0.8' : '0.5';
  if (url === '/presse/' || url === '/en/press/') return '0.8';
  if (url === '/versionen/' || url === '/en/versions/') return '0.7';
  if (/^\/ratgeber\/.+\//.test(url)) return '0.5';
  return '0.6';
};

const seitenDateien = (ordner = '') => {
  const treffer = [];
  for (const eintrag of fs.readdirSync(path.join(WURZEL, ordner), { withFileTypes: true })) {
    if (eintrag.isDirectory()) {
      if (!AUSGESCHLOSSEN.has(eintrag.name)) treffer.push(...seitenDateien(path.join(ordner, eintrag.name)));
    } else if (eintrag.name === 'index.html') {
      treffer.push(path.join(ordner, eintrag.name));
    }
  }
  return treffer;
};

// Meta-Tags (description, Open Graph, Twitter) und der ganze Footer. Alles
// andere — auch JSON-LD, Ueberschriften und der Fliesstext — bleibt Inhalt.
const ohneMetaUndFooter = (html) => html
  .replace(/<meta\b[^>]*>\n?/gi, '')
  .replace(/<footer\b[^>]*>[\s\S]*?<\/footer>\n?/gi, '');

const dateiInhalt = (rev, datei) => {
  try {
    return execFileSync('git', ['show', `${rev}:${datei}`], { cwd: WURZEL, encoding: 'utf8' });
  } catch {
    return null;
  }
};

const commitDatum = (datei) => {
  const log = execFileSync('git', ['log', '--format=%H %cs', '--', datei],
                           { cwd: WURZEL, encoding: 'utf8' }).trim();
  if (!log) throw new Error(`Kein Commit-Datum fuer ${datei} — noch nicht eingecheckt?`);
  const eintraege = log.split('\n').map((zeile) => {
    const leer = zeile.indexOf(' ');
    return { hash: zeile.slice(0, leer), datum: zeile.slice(leer + 1) };
  });
  for (const { hash, datum } of eintraege) {
    if (!/^\d{4}-\d{2}-\d{2}$/.test(datum)) {
      throw new Error(`Kein Commit-Datum fuer ${datei} (${hash})`);
    }
    const nachher = dateiInhalt(hash, datei);
    const vorher = dateiInhalt(`${hash}^`, datei);
    // Die Datei entsteht in diesem Commit, oder der Inhalt ausserhalb von
    // Meta-Tags und Footer hat sich geaendert.
    if (vorher === null || ohneMetaUndFooter(vorher) !== ohneMetaUndFooter(nachher)) return datum;
  }
  return eintraege[eintraege.length - 1].datum;
};

const seiten = [];
for (const datei of seitenDateien()) {
  const html = fs.readFileSync(path.join(WURZEL, datei), 'utf8');
  if (/<meta\s+name="robots"\s+content="[^"]*noindex/i.test(html)) continue;
  const url = '/' + path.dirname(datei).replace(/^\.$/, '').split(path.sep).filter(Boolean).map((t) => t + '/').join('');
  // Die kanonische Adresse muss die eigene sein — sonst meldet Google die Seite
  // als Duplikat oder Weiterleitung, und in die Sitemap gehoert sie dann nicht.
  const kanonisch = html.match(/<link\s+rel="canonical"\s+href="([^"]+)"/i)?.[1];
  if (kanonisch !== BASIS + url) {
    throw new Error(`${datei}: canonical ist ${kanonisch ?? '(fehlt)'}, erwartet ${BASIS + url}`);
  }
  const alternativen = [...html.matchAll(/<link\s+rel="alternate"\s+hreflang="([^"]+)"\s+href="([^"]+)"/gi)]
    .map(([, sprache, href]) => ({ sprache, href }));
  seiten.push({ datei, url, alternativen, lastmod: commitDatum(datei) });
}

const versionen = [...new Set(seiten.map((s) => s.url.match(versionsSeite)).filter(Boolean)
  .map((m) => `${m[1]}.${m[2]}`))]
  .sort((a, b) => { const [a1, a2] = a.split('.').map(Number), [b1, b2] = b.split('.').map(Number); return b1 - a1 || b2 - a2; });
const neuesteVersionen = versionen.slice(0, 2);

// Reihenfolge: Startseiten, dann der Rest alphabetisch, englische Fassung direkt hinter der deutschen.
const sortierSchluessel = (s) => {
  if (s.url === '/' || s.url === '/en/') return `0|${s.url === '/en/' ? 1 : 0}`;
  const de = s.alternativen.find((a) => a.sprache === 'de')?.href.replace(BASIS, '') ?? s.url;
  const v = de.match(/^\/neu-in-(\d+)-(\d+)\/$/);
  const basis = v ? `2-${String(99 - v[1]).padStart(2, '0')}-${String(99 - v[2]).padStart(2, '0')}` : `1-${de}`;
  return `${basis}|${s.url.startsWith('/en/') ? 1 : 0}`;
};
seiten.sort((a, b) => sortierSchluessel(a).localeCompare(sortierSchluessel(b)));

const zeilen = [
  '<?xml version="1.0" encoding="UTF-8"?>',
  '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
  '        xmlns:xhtml="http://www.w3.org/1999/xhtml">',
];
for (const s of seiten) {
  zeilen.push('  <url>', `    <loc>${BASIS}${s.url}</loc>`);
  for (const sprache of ['de', 'en', 'x-default']) {
    const alt = s.alternativen.find((a) => a.sprache === sprache);
    if (alt) zeilen.push(`    <xhtml:link rel="alternate" hreflang="${sprache}" href="${alt.href}"/>`);
  }
  zeilen.push(`    <lastmod>${s.lastmod}</lastmod>`,
              `    <priority>${prioritaet(s.url, neuesteVersionen)}</priority>`,
              '  </url>');
}
zeilen.push('</urlset>');

fs.writeFileSync(path.join(WURZEL, 'sitemap.xml'), zeilen.join('\n') + '\n');
console.log(`sitemap.xml: ${seiten.length} Seiten (neueste Versionen: ${neuesteVersionen.join(', ')})`);
for (const s of seiten) console.log(`  ${s.url.padEnd(48)} ${s.lastmod}  ${prioritaet(s.url, neuesteVersionen)}`);
