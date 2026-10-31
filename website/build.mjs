// Builds the FarStudio website into dist/. No dependencies: run `node build.mjs`.
//
// Content lives in src/: site.json (settings), i18n/<lang>.json (interface text),
// games/<slug>.json (one file per game), privacy/<lang>.html (the policy).
// Brand files (logos, favicons, link preview) are copied from ../branding.

import { readFileSync, writeFileSync, mkdirSync, rmSync, cpSync, existsSync, readdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = dirname(fileURLToPath(import.meta.url));
const SRC = join(ROOT, 'src');
const OUT = join(ROOT, 'dist');
const BRAND = join(ROOT, '..', 'branding');

const readJSON = (p) => JSON.parse(readFileSync(p, 'utf8'));
const site = readJSON(join(SRC, 'site.json'));
const LANGS = site.languages;
const DEFAULT = site.defaultLanguage;
const T = Object.fromEntries(LANGS.map((l) => [l, readJSON(join(SRC, 'i18n', `${l}.json`))]));
const games = readdirSync(join(SRC, 'games'))
  .filter((f) => f.endsWith('.json'))
  .map((f) => readJSON(join(SRC, 'games', f)))
  .sort((a, b) => (a.order ?? 99) - (b.order ?? 99));

// ---------- helpers ----------
const esc = (s = '') => String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);
// A localized field is either a plain string or { en: '...', es: '...' }; missing languages fall back to the default.
const loc = (v, lang) => (v && typeof v === 'object' && !Array.isArray(v) ? v[lang] ?? v[DEFAULT] ?? '' : v ?? '');
const url = (lang, path = '') => `/${lang}/${path}`;
const abs = (p) => site.domain.replace(/\/$/, '') + p;
const write = (rel, html) => {
  const file = join(OUT, rel);
  mkdirSync(dirname(file), { recursive: true });
  writeFileSync(file, html);
};

const ICONS = {
  appstore: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M16.4 12.6c0-2.4 2-3.5 2-3.6-1.1-1.6-2.8-1.8-3.4-1.8-1.4-.1-2.8.9-3.5.9s-1.8-.8-3-.8C6.9 7.3 5.4 8.2 4.6 9.6c-1.7 2.9-.4 7.2 1.2 9.6.8 1.2 1.7 2.4 3 2.4 1.2 0 1.6-.8 3.1-.8s1.8.8 3.1.8c1.3 0 2.1-1.2 2.9-2.3.9-1.3 1.3-2.6 1.3-2.7 0 0-2.5-1-2.8-4zM14.1 5.6c.6-.8 1.1-1.9 1-3-.9 0-2.1.6-2.7 1.4-.6.7-1.1 1.8-1 2.8 1 .1 2.1-.5 2.7-1.2z"/></svg>',
  googleplay: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 2.8v18.4c0 .6.6.9 1.1.6l10.7-9.2c.4-.3.4-.9 0-1.2L5.1 2.2C4.6 1.9 4 2.2 4 2.8z"/></svg>',
  steam: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 0 0-10 9.2l5.4 2.2a2.8 2.8 0 0 1 1.7-.5l2.4-3.5v-.1a3.8 3.8 0 1 1 3.8 3.8h-.1l-3.4 2.4v.2a2.9 2.9 0 0 1-5.7.6L2.3 15A10 10 0 1 0 12 2zm-4.3 15.2-1.2-.5a2.1 2.1 0 1 0 1.2-2.9l1.3.5a1.6 1.6 0 1 1-1.3 2.9zm7.5-5.6a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5z"/></svg>',
  web: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20zm6.9 6h-3a15.6 15.6 0 0 0-1.4-3.6A8 8 0 0 1 18.9 8zM12 4c.8 1.2 1.5 2.5 1.9 4h-3.8c.4-1.5 1.1-2.8 1.9-4zM4.3 14a8.2 8.2 0 0 1 0-4h3.4a16.5 16.5 0 0 0 0 4H4.3zm.8 2h3a15.6 15.6 0 0 0 1.4 3.6A8 8 0 0 1 5.1 16zm3-8h-3a8 8 0 0 1 4.4-3.6C8 5.5 7.6 6.7 8.1 8zM12 20c-.8-1.2-1.5-2.5-1.9-4h3.8c-.4 1.5-1.1 2.8-1.9 4zm2.3-6H9.7a14.7 14.7 0 0 1 0-4h4.6a14.7 14.7 0 0 1 0 4zm.3 5.6c.6-1.1 1.1-2.3 1.4-3.6h3a8 8 0 0 1-4.4 3.6zm1.7-5.6a16.5 16.5 0 0 0 0-4h3.4a8.2 8.2 0 0 1 0 4h-3.4z"/></svg>',
};
const STORE_NAMES = { appstore: 'App Store', googleplay: 'Google Play', steam: 'Steam', web: 'Web' };

function storeButton(store, t, primary) {
  const name = STORE_NAMES[store.id] ?? store.id;
  const icon = ICONS[store.id] ?? '';
  if (!store.url) {
    return `<span class="btn ${primary ? 'pri' : 'sec'} is-soon" aria-disabled="true">${icon}<span>${esc(name)}<small>${esc(t.game.soon)}</small></span></span>`;
  }
  return `<a class="btn ${primary ? 'pri' : 'sec'}" href="${esc(store.url)}" rel="noopener">${icon}<span>${esc(name)}</span></a>`;
}
const storeButtons = (g, t) => g.stores.map((s, i) => storeButton(s, t, i === 0)).join('');

function art(src, alt, cls, label) {
  if (src) return `<img class="${cls}" src="${esc(src)}" alt="${esc(alt)}" loading="lazy" decoding="async">`;
  return `<div class="${cls} ph" role="img" aria-label="${esc(alt)}"><span>${esc(label)}</span></div>`;
}
const gameAsset = (g, file) => (file ? `/assets/games/${g.slug}/${file}` : '');

// ---------- layout ----------
function head({ lang, t, title, description, path, noindex = false, image }) {
  const alternates = LANGS.map((l) => `<link rel="alternate" hreflang="${T[l].htmlLang}" href="${abs(url(l, path))}">`).join('\n  ');
  return `<!DOCTYPE html>
<html lang="${t.htmlLang}" class="lang-${lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>${esc(title)}</title>
  <meta name="description" content="${esc(description)}">
  ${noindex ? '<meta name="robots" content="noindex, follow">' : `<link rel="canonical" href="${abs(url(lang, path))}">
  ${alternates}
  <link rel="alternate" hreflang="x-default" href="${abs(url(DEFAULT, path))}">`}
  <meta name="theme-color" content="#111111">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="FarStudio">
  <meta property="og:title" content="${esc(title)}">
  <meta property="og:description" content="${esc(description)}">
  <meta property="og:url" content="${abs(url(lang, path))}">
  <meta property="og:image" content="${abs(image ?? '/assets/brand/link-preview-1200x630.png')}">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="/favicon.ico" sizes="48x48">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/brand/favicon-32x32.png">
  <link rel="icon" type="image/png" sizes="192x192" href="/assets/brand/favicon-192x192.png">
  <link rel="apple-touch-icon" href="/assets/brand/apple-touch-icon-180x180.png">
  <link rel="preload" href="/assets/fonts/outfit-latin.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="/assets/site.css">
</head>`;
}

function header(lang, t, path) {
  const other = LANGS.map(
    (l) => `<li><a href="${url(l, path)}" hreflang="${T[l].htmlLang}" lang="${T[l].htmlLang}"${l === lang ? ' aria-current="true"' : ''}>${esc(T[l].name)}</a></li>`,
  ).join('');
  return `<a class="skip" href="#main">${esc(t.nav.skip)}</a>
<header class="nav wrap">
  <a class="brand" href="${url(lang)}" aria-label="FarStudio, ${esc(t.nav.home)}"><img src="/assets/brand/logo-horizontal.svg" alt="FarStudio" width="145" height="40"></a>
  <nav class="links" aria-label="${esc(t.nav.main)}">
    <a href="${url(lang)}#games">${esc(t.nav.games)}</a>
    <a href="${url(lang, 'about/')}">${esc(t.nav.about)}</a>
  </nav>
  <details class="lang">
    <summary aria-label="${esc(t.nav.language)}"><span>${esc(t.short)}</span><svg viewBox="0 0 12 12" aria-hidden="true"><path d="M2 4l4 4 4-4" fill="none" stroke="currentColor" stroke-width="1.6"/></svg></summary>
    <ul>${other}</ul>
  </details>
</header>`;
}

function footer(lang, t, path) {
  const gameLinks = games.map((g) => `<li><a href="${url(lang, `games/${g.slug}/`)}">${esc(loc(g.name, lang))}</a></li>`).join('');
  const langLinks = LANGS.map((l) => `<li><a href="${url(l, path)}" hreflang="${T[l].htmlLang}" lang="${T[l].htmlLang}">${esc(T[l].name)}</a></li>`).join('');
  const youtube = site.youtube ? `<li><a href="${esc(site.youtube)}" rel="noopener">YouTube</a></li>` : '';
  return `<footer class="foot">
  <div class="wrap fcols">
    <div class="fbrand"><img src="/assets/brand/symbol.svg" alt="" width="40" height="38"><p>${esc(t.footer.tagline)}</p></div>
    <div><h2>${esc(t.footer.games)}</h2><ul>${gameLinks}</ul></div>
    <div><h2>${esc(t.footer.studio)}</h2><ul><li><a href="${url(lang, 'about/')}">${esc(t.nav.about)}</a></li>${youtube}<li><a href="${url(lang, 'about/')}#contact">${esc(t.footer.contact)}</a></li></ul></div>
    <div><h2>${esc(t.footer.language)}</h2><ul>${langLinks}</ul></div>
  </div>
  <div class="wrap fbottom"><span>© ${new Date().getFullYear()} FarStudio</span><a href="${url(lang, 'privacy/')}">${esc(t.footer.privacy)}</a></div>
</footer>`;
}

const page = (opts, body, extraScript = '') => `${head(opts)}
<body>
${header(opts.lang, opts.t, opts.path)}
<main id="main">
${body}
</main>
${footer(opts.lang, opts.t, opts.path)}
${extraScript}
</body>
</html>
`;

// ---------- pages ----------
function homePage(lang) {
  const t = T[lang];
  const featured = games.find((g) => g.featured) ?? games[0];
  const fName = loc(featured.name, lang);
  const cards = games
    .map((g) => {
      const name = loc(g.name, lang);
      return `<li class="card"><a href="${url(lang, `games/${g.slug}/`)}">
        ${art(gameAsset(g, g.art?.cover), name, 'cover', name)}
        <h3>${esc(name)}</h3><p>${esc(g.platforms.join(' · '))}</p></a></li>`;
    })
    .join('');
  const soon = `<li class="card soon"><div class="cover"><span>${esc(t.home.comingSoon)}</span></div><h3>${esc(t.home.nextGame)}</h3><p>${esc(t.home.inDevelopment)}</p></li>`;
  const body = `
<section class="hero wrap" aria-labelledby="hero-title">
  <div class="hero-art">${art(gameAsset(featured, featured.art?.key), fName, 'key', `${fName} · key art`)}</div>
  <div class="hero-copy">
    <p class="eyebrow">${esc(t.home.newGame)}</p>
    <h1 id="hero-title">${esc(fName)}</h1>
    <p class="muted">${esc(loc(featured.tagline, lang))}</p>
    <div class="btns">${storeButtons(featured, t)}<a class="btn ghost" href="${url(lang, `games/${featured.slug}/`)}">${esc(t.home.seeGame)}</a></div>
  </div>
</section>
<section class="block wrap" id="games" aria-labelledby="games-title">
  <div class="block-head"><h2 id="games-title">${esc(t.home.ourGames)}</h2></div>
  <ul class="cards">${cards}${soon}</ul>
</section>
<section class="wrap">
  <div class="studio">
    <img src="/assets/brand/symbol.svg" alt="" width="64" height="61">
    <div><h2>${esc(t.home.studioTitle)}</h2><p class="muted">${esc(t.home.studioText)}</p></div>
    <a class="btn sec" href="${url(lang, 'about/')}">${esc(t.nav.about)}</a>
  </div>
</section>`;
  return page({ lang, t, title: t.home.title, description: t.home.description, path: '' }, body);
}

function gamePage(lang, g) {
  const t = T[lang];
  const name = loc(g.name, lang);
  const path = `games/${g.slug}/`;
  const facts = [
    [t.game.platforms, g.platforms.join(', ')],
    [t.game.release, loc(g.release, lang)],
    [t.game.languages, (g.languages ?? []).join(', ')],
    [t.game.price, g.free ? t.game.free : loc(g.price, lang)],
  ]
    .filter(([, v]) => v)
    .map(([k, v]) => `<dt>${esc(k)}</dt><dd>${esc(v)}</dd>`)
    .join('');
  const shots = (g.art?.screenshots?.length ? g.art.screenshots : [null, null, null, null])
    .map((s, i) => `<li>${art(gameAsset(g, s), `${name} · ${t.game.screenshot} ${i + 1}`, 'shot', `${t.game.screenshot} ${i + 1}`)}</li>`)
    .join('');
  const feats = (g.features ?? [])
    .map((f, i) => `<li class="feat"><span class="n">${String(i + 1).padStart(2, '0')}</span><h3>${esc(loc(f.title, lang))}</h3><p>${esc(loc(f.text, lang))}</p></li>`)
    .join('');
  const trailer = g.trailer
    ? `<div class="trailer" data-yt="${esc(g.trailer)}">
        <img src="https://i.ytimg.com/vi/${esc(g.trailer)}/hqdefault.jpg" alt="" loading="lazy">
        <button type="button" class="play" aria-label="${esc(t.game.playTrailer)}"></button></div>`
    : `<div class="trailer ph"><span>${esc(t.game.trailerSoon)}</span></div>`;
  const firstLive = g.stores.find((s) => s.url);
  const others = games.filter((o) => o.slug !== g.slug);
  const body = `
<div class="game wrap">
  <aside class="side" aria-label="${esc(name)}">
    ${art(gameAsset(g, g.art?.icon), `${name} icon`, 'icon', '')}
    <h1>${esc(name)}</h1>
    <p class="muted">${esc(loc(g.tagline, lang))}</p>
    <div class="stack">${storeButtons(g, t)}</div>
    ${facts ? `<dl class="facts">${facts}</dl>` : ''}
    <p class="small"><a href="${url(lang, 'about/')}#contact">${esc(t.game.support)}</a> · <a href="${url(lang, 'privacy/')}#${g.slug}">${esc(t.footer.privacy)}</a></p>
  </aside>
  <div class="gmain">
    ${trailer}
    <h2 class="vh">${esc(t.game.screenshots)}</h2>
    <ul class="shots">${shots}</ul>
    <div class="desc">${(loc(g.description, lang) || '').split('\n\n').map((p) => `<p>${esc(p)}</p>`).join('')}</div>
    ${feats ? `<h2 class="vh">${esc(t.game.features)}</h2><ul class="feats">${feats}</ul>` : ''}
    <p class="sign"><img src="/assets/brand/symbol.svg" alt="" width="22" height="21">${esc(t.game.signature)}</p>
    ${others.length ? `<p class="more">${esc(t.game.moreGames)}: ${others.map((o) => `<a href="${url(lang, `games/${o.slug}/`)}">${esc(loc(o.name, lang))}</a>`).join(', ')}</p>` : ''}
  </div>
</div>
<div class="dlbar">${firstLive ? storeButton(firstLive, t, true) : `<span class="btn pri is-soon" aria-disabled="true"><span>${esc(t.game.soon)}</span></span>`}</div>`;
  const script = g.trailer ? `<script src="/assets/trailer.js" defer></script>` : '';
  const image = g.art?.share ? gameAsset(g, g.art.share) : undefined;
  return page({ lang, t, title: `${name} · FarStudio`, description: loc(g.tagline, lang), path, image }, body, script);
}

function aboutPage(lang) {
  const t = T[lang];
  const a = t.about;
  const team = (site.team ?? [])
    .map((m) => `<li>${art(m.photo, m.name, 'avatar', m.name.slice(0, 1))}<h3>${esc(m.name)}</h3><p>${esc(loc(m.role, lang))}</p></li>`)
    .join('');
  const body = `
<section class="wrap manifesto">
  <p class="eyebrow">${esc(a.eyebrow)}</p>
  <h1>${esc(a.statement)}</h1>
  <p class="lead muted">${esc(a.intro)}</p>
</section>
<section class="wrap" aria-label="${esc(a.valuesTitle)}">
  <ol class="values">${a.values.map((v, i) => `<li><span class="n">${String(i + 1).padStart(2, '0')}</span><h2>${esc(v.title)}</h2><p class="muted">${esc(v.text)}</p></li>`).join('')}</ol>
</section>
${team ? `<section class="block wrap" aria-labelledby="team-title"><div class="block-head"><h2 id="team-title">${esc(a.teamTitle)}</h2></div><ul class="team">${team}</ul></section>` : ''}
<section class="wrap" id="contact">
  <div class="studio contact">
    <div><h2>${esc(a.contactTitle)}</h2><p class="muted">${esc(a.contactText)}</p></div>
    <a class="btn pri" href="mailto:${esc(site.email)}">${esc(site.email)}</a>
  </div>
</section>`;
  return page({ lang, t, title: `${a.title} · FarStudio`, description: a.description, path: 'about/' }, body);
}

function privacyPage(lang) {
  const t = T[lang];
  const p = t.privacy;
  const file = join(SRC, 'privacy', `${lang}.html`);
  const html = readFileSync(existsSync(file) ? file : join(SRC, 'privacy', `${DEFAULT}.html`), 'utf8').replace(/<!--[\s\S]*?-->/g, '').trim();
  const strip = (s) => s.replace(/<[^>]+>/g, '');
  const toc = [...html.matchAll(/<h2 id="([^"]+)">(.*?)<\/h2>/g)].map(([, id, title]) => ({ id, title: strip(title) }));
  const gameIds = new Set(games.map((g) => g.slug));
  const general = toc.filter((x) => !gameIds.has(x.id));
  const perGame = toc.filter((x) => gameIds.has(x.id));
  const list = (items) => `<ul>${items.map((x) => `<li><a href="#${x.id}">${esc(x.title)}</a></li>`).join('')}</ul>`;
  const body = `
<div class="privacy wrap">
  <aside class="toc">
    <details open>
      <summary>${esc(p.toc)}</summary>
      ${list(general)}
      ${perGame.length ? `<p class="eyebrow">${esc(p.byGame)}</p>${list(perGame)}` : ''}
    </details>
  </aside>
  <article class="legal">
    <h1>${esc(p.title)}</h1>
    <p class="muted small">${esc(p.updated)}: <time datetime="${site.privacyUpdated}">${esc(site.privacyUpdated)}</time>${lang === DEFAULT ? '' : ` · ${esc(p.prevails)}`}</p>
    ${html.replaceAll('{{EMAIL}}', `<a href="mailto:${esc(site.email)}">${esc(site.email)}</a>`)}
  </article>
</div>`;
  return page({ lang, t, title: `${p.title} · FarStudio`, description: p.description, path: 'privacy/', noindex: true }, body);
}

// Root: send visitors to their browser's language, English otherwise.
function rootPage() {
  const map = Object.fromEntries(LANGS.map((l) => [l, T[l].match ?? [l]]));
  const links = LANGS.map((l) => `<li><a href="/${l}/" hreflang="${T[l].htmlLang}" lang="${T[l].htmlLang}">${esc(T[l].name)}</a></li>`).join('');
  const alternates = LANGS.map((l) => `<link rel="alternate" hreflang="${T[l].htmlLang}" href="${abs(`/${l}/`)}">`).join('\n  ');
  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>FarStudio</title>
  <link rel="canonical" href="${abs(`/${DEFAULT}/`)}">
  ${alternates}
  <link rel="alternate" hreflang="x-default" href="${abs(`/${DEFAULT}/`)}">
  <link rel="icon" href="/favicon.ico" sizes="48x48">
  <script>
  (function () {
    var map = ${JSON.stringify(map)}, prefs = navigator.languages || [navigator.language || ''];
    for (var i = 0; i < prefs.length; i++) {
      var p = String(prefs[i]).toLowerCase();
      for (var l in map) for (var j = 0; j < map[l].length; j++) {
        if (p === map[l][j] || p.indexOf(map[l][j] + '-') === 0) { location.replace('/' + l + '/' + location.hash); return; }
      }
    }
    location.replace('/${DEFAULT}/' + location.hash);
  })();
  </script>
  <noscript><meta http-equiv="refresh" content="0; url=/${DEFAULT}/"></noscript>
  <style>body{margin:0;background:#111;color:#f4f4f2;font:16px/1.5 system-ui,sans-serif;display:grid;place-items:center;min-height:100vh}a{color:#f5a623}</style>
</head>
<body><ul>${links}</ul></body>
</html>
`;
}

function notFound() {
  const t = T[DEFAULT];
  const body = `<section class="wrap manifesto"><p class="eyebrow">404</p><h1>${esc(t.notFound.title)}</h1><p class="muted">${esc(t.notFound.text)}</p><p><a class="btn pri" href="/">FarStudio</a></p></section>`;
  return page({ lang: DEFAULT, t, title: `404 · FarStudio`, description: t.notFound.title, path: '', noindex: true }, body);
}

function sitemap() {
  const paths = ['', 'about/', ...games.map((g) => `games/${g.slug}/`)];
  const urls = paths
    .flatMap((p) =>
      LANGS.map(
        (l) => `  <url><loc>${abs(url(l, p))}</loc>${LANGS.map((o) => `<xhtml:link rel="alternate" hreflang="${T[o].htmlLang}" href="${abs(url(o, p))}"/>`).join('')}</url>`,
      ),
    )
    .join('\n');
  return `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">
${urls}
</urlset>
`;
}

// ---------- build ----------
rmSync(OUT, { recursive: true, force: true });
mkdirSync(OUT, { recursive: true });

cpSync(join(ROOT, 'public'), join(OUT), { recursive: true });
cpSync(join(SRC, 'styles.css'), join(OUT, 'assets', 'site.css'));
cpSync(join(SRC, 'trailer.js'), join(OUT, 'assets', 'trailer.js'));
const brand = {
  'svg/farstudio-logo-horizontal-color-on-dark.svg': 'logo-horizontal.svg',
  'svg/farstudio-symbol-color-on-dark.svg': 'symbol.svg',
  'png/favicon/favicon-32x32.png': 'favicon-32x32.png',
  'png/favicon/favicon-192x192.png': 'favicon-192x192.png',
  'png/favicon/apple-touch-icon-180x180.png': 'apple-touch-icon-180x180.png',
  'png/banners/link-preview-1200x630.png': 'link-preview-1200x630.png',
};
for (const [from, to] of Object.entries(brand)) cpSync(join(BRAND, from), join(OUT, 'assets', 'brand', to));
cpSync(join(BRAND, 'png/favicon/favicon.ico'), join(OUT, 'favicon.ico'));
for (const g of games) {
  const dir = join(SRC, 'games', g.slug);
  if (existsSync(dir)) cpSync(dir, join(OUT, 'assets', 'games', g.slug), { recursive: true });
}

write('index.html', rootPage());
write('404.html', notFound());
write('sitemap.xml', sitemap());
write('robots.txt', `User-agent: *\nAllow: /\n\nSitemap: ${abs('/sitemap.xml')}\n`);
write('_headers', `/*/privacy/*\n  X-Robots-Tag: noindex\n\n/assets/*\n  Cache-Control: public, max-age=86400\n`);
for (const lang of LANGS) {
  write(`${lang}/index.html`, homePage(lang));
  write(`${lang}/about/index.html`, aboutPage(lang));
  write(`${lang}/privacy/index.html`, privacyPage(lang));
  for (const g of games) write(`${lang}/games/${g.slug}/index.html`, gamePage(lang, g));
}
console.log(`Built ${LANGS.length} languages, ${games.length} game(s) into dist/`);
