"""Render the preview images shown in README.md (docs/preview/), from the SVG masters.

python3 tools/previews.py      (run from the repository root; needs Playwright + Chromium)
"""
import base64, os
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SVG = os.path.join(ROOT, "svg")
OUT = os.path.join(ROOT, "docs", "preview")
os.makedirs(OUT, exist_ok=True)

INK, PAPER, AMBER, GRAY, LIGHT = "#111111", "#FFFFFF", "#F5A623", "#555555", "#E8E8E5"
FONT = base64.b64encode(open(os.path.join(ROOT, "fonts", "Outfit-Variable.ttf"), "rb").read()).decode()
W = 900  # CSS width; rendered at 2x


def svg(name):
    return "data:image/svg+xml;base64," + base64.b64encode(open(os.path.join(SVG, name), "rb").read()).decode()


def png(rel):
    return "data:image/png;base64," + base64.b64encode(open(os.path.join(ROOT, rel), "rb").read()).decode()


CSS = f"""
@font-face {{ font-family: Outfit; src: url(data:font/ttf;base64,{FONT}); font-weight: 100 900; }}
* {{ box-sizing: border-box; margin: 0; }}
body {{ width: {W}px; font-family: Outfit; color: {INK}; background: {PAPER}; }}
.sheet {{ padding: 28px; background: #F4F4F2; }}
.grid {{ display: grid; gap: 16px; }}
.card {{ border-radius: 14px; overflow: hidden; background: {PAPER}; border: 1px solid {LIGHT}; display: flex; flex-direction: column; }}
.art {{ flex: 1; display: flex; align-items: center; justify-content: center; padding: 22px; }}
.cap {{ padding: 12px 16px 14px; border-top: 1px solid {LIGHT}; background: {PAPER}; }}
.cap b {{ display: block; font-weight: 600; font-size: 15px; letter-spacing: .02em; }}
.cap span {{ font-size: 13px; color: {GRAY}; }}
code {{ font-family: ui-monospace, Menlo, monospace; font-size: 12px; }}
"""


def card(art, title, sub, bg=PAPER, h=None):
    style = f"background:{bg};" + (f"height:{h}px;" if h else "")
    return (f'<div class="card"><div class="art" style="{style}">{art}</div>'
            f'<div class="cap"><b>{title}</b><span>{sub}</span></div></div>')


def img(src, w=None, h=None, extra=""):
    size = (f"width:{w}px;" if w else "") + (f"height:{h}px;" if h else "")
    return f'<img src="{src}" style="display:block;{size}{extra}">'


PAGES = {}

# Pieces: which logo for which space
PAGES["pieces"] = f"""<div class="sheet"><div class="grid" style="grid-template-columns: 1.15fr 1.6fr;">
{card(img(svg("farstudio-logo-vertical-color-on-light.svg"), h=190), "Vertical · primary", "Credits, splash, posters, press kit", h=250)}
{card(img(svg("farstudio-logo-horizontal-color-on-light.svg"), w=380), "Horizontal · secondary", "Headers, footers, signatures, watermarks", h=250)}
</div><div class="grid" style="grid-template-columns: 1fr 1.6fr; margin-top:16px">
{card(img(svg("farstudio-symbol-color-on-light.svg"), h=110), "Symbol", "Square or under 32 px: icons, avatars, favicon", h=160)}
{card(img(svg("farstudio-wordmark-black.svg"), w=330), "Wordmark", "Only with the lighthouse already nearby", h=160)}
</div></div>"""

# Color variants, each on its background
PAGES["variants"] = f"""<div class="sheet"><div class="grid" style="grid-template-columns: 1fr 1fr;">
{card(img(svg("farstudio-logo-horizontal-color-on-dark.svg"), w=330), "color-on-dark · preferred", "On black or dark backgrounds", bg=INK, h=170)}
{card(img(svg("farstudio-logo-horizontal-color-on-light.svg"), w=330), "color-on-light", "On white or light backgrounds", h=170)}
{card(img(svg("farstudio-logo-horizontal-mono-black.svg"), w=330), "mono-black", "One-color print, stamps, black and white", bg=LIGHT, h=170)}
{card(img(svg("farstudio-logo-horizontal-mono-white.svg"), w=330), "mono-white", "Over photos or color where amber can't read", bg="linear-gradient(135deg,#3E5C76,#7A6C8F)", h=170)}
</div></div>"""

# Icons and avatars
fav = "".join(
    f'<div style="text-align:center">{img(png(f"png/favicon/favicon-{s}x{s}.png"), w=s, h=s, extra="margin:0 auto 8px;image-rendering:pixelated")}'
    f'<span style="font-size:12px;color:{GRAY}">{s} px</span></div>' for s in (48, 32, 16))
PAGES["icons"] = f"""<div class="sheet"><div class="grid" style="grid-template-columns: repeat(4, 1fr);">
{card(img(svg("farstudio-app-icon.svg"), w=150), "App icon · square", "Stores (they round it)", h=200)}
{card(img(svg("farstudio-app-icon-rounded.svg"), w=150), "App icon · rounded", "Web, docs, mockups", h=200)}
{card(img(svg("farstudio-avatar-circle.svg"), w=150), "Avatar", "YouTube, Steam, social", h=200)}
{card(f'<div style="display:flex;gap:22px;align-items:flex-end">{fav}</div>', "Favicon", "Real size, still readable", h=200)}
</div></div>"""

# Colors
sw = [(INK, "Ink", "Lighthouse, name, dark backgrounds", PAPER),
      (PAPER, "Paper", "Backgrounds, logo on dark", INK),
      (AMBER, "Lighthouse light", "Only the lantern and beams", INK),
      (GRAY, "Text gray", "Secondary text", PAPER),
      (LIGHT, "Light gray", "Supporting backgrounds, dividers", INK)]
PAGES["colors"] = '<div class="sheet"><div class="grid" style="grid-template-columns: repeat(5, 1fr);">' + "".join(
    f'<div class="card"><div style="height:150px;background:{c};padding:14px;color:{t};font-weight:600;font-size:15px;'
    f'{"border-bottom:1px solid " + LIGHT if c == PAPER else ""}">{c}</div>'
    f'<div class="cap"><b>{n}</b><span>{u}</span></div></div>' for c, n, u, t in sw) + "</div></div>"

# Clear space and minimum sizes
PAGES["rules"] = f"""<div class="sheet"><div class="grid" style="grid-template-columns: 1.5fr 1fr;">
{card(f'<div style="position:relative;outline:1.5px dashed {AMBER};outline-offset:0">{img(svg("farstudio-logo-horizontal-color-on-light.svg"), w=360)}'
      f'<span style="position:absolute;bottom:-26px;left:0;font-size:12px;color:{GRAY}">dashed line = file edge · X (cap height of the name) on every side</span></div>',
      "Clear space", "Built into every file: never crop it", h=290)}
{card(f'<div style="display:flex;flex-direction:column;gap:14px;align-items:flex-start">'
      f'<div style="display:flex;align-items:center;gap:12px">{img(svg("farstudio-logo-vertical-color-on-light.svg"), w=120)}<span style="font-size:13px">vertical · 120 px</span></div>'
      f'<div style="display:flex;align-items:center;gap:12px">{img(svg("farstudio-logo-horizontal-color-on-light.svg"), w=140)}<span style="font-size:13px">horizontal · 140 px</span></div>'
      f'<div style="display:flex;align-items:center;gap:12px">{img(svg("farstudio-symbol-color-on-light.svg"), w=16)}<span style="font-size:13px">symbol · 16 px</span></div></div>',
      "Minimum sizes", "Shown at their real size", h=290)}
</div></div>"""

with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page(device_scale_factor=2, viewport={"width": W, "height": 400})
    for name, body in PAGES.items():
        page.set_content(f"<html><head><style>{CSS}</style></head><body>{body}</body></html>")
        page.wait_for_timeout(150)
        page.locator(".sheet").screenshot(path=os.path.join(OUT, f"{name}.png"))
    b.close()
print("previews in", OUT)
