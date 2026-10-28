"""Render the illustrations of the README into docs/readme/ (run from the repository root)."""
import os, base64, re
from playwright.sync_api import sync_playwright

SVG, OUT = "svg", "docs/readme"
INK, PAPER, AMBER, GRAY, LIGHT = "#111111", "#FFFFFF", "#F5A623", "#555555", "#E8E8E5"
os.makedirs(OUT, exist_ok=True)


def uri(name):
    return "data:image/svg+xml;base64," + base64.b64encode(open(os.path.join(SVG, name), "rb").read()).decode()


def ratio(name):
    m = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', open(os.path.join(SVG, name)).read())
    return float(m.group(1)) / float(m.group(2))


FONT = "font-family:Outfit,sans-serif"
FONT_FACE = ("<style>@font-face{font-family:Outfit;src:url(data:font/ttf;base64,"
             + base64.b64encode(open("fonts/Outfit-Variable.ttf", "rb").read()).decode()
             + ") format('truetype');font-weight:100 900}</style>")


def shot(page, html, w, h, name, transparent=False):
    page.set_viewport_size({"width": w, "height": h})
    page.set_content(f"<html><head>{FONT_FACE}</head><body style='margin:0'>{html}</body></html>")
    page.wait_for_timeout(80)
    page.screenshot(path=os.path.join(OUT, name), omit_background=transparent,
                    clip={"x": 0, "y": 0, "width": w, "height": h})


def tile(logo, bg, w, h, logo_w, label=None, fg=None):
    lab = (f"<div style='position:absolute;left:28px;bottom:22px;{FONT};font-size:22px;letter-spacing:.08em;"
           f"color:{fg}'>{label}</div>") if label else ""
    return (f"<div style='position:relative;width:{w}px;height:{h}px;background:{bg};display:flex;"
            f"align-items:center;justify-content:center'><img src='{uri(logo)}' style='width:{logo_w}px'>{lab}</div>")


with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page()

    # Hero: the vertical logo on its preferred black, wide
    shot(pg, tile("farstudio-logo-vertical-color-on-dark.svg", INK, 1600, 760, 620), 1600, 760, "hero.png")

    # The four color variants, each on the background it is meant for
    variants = [("color-on-dark", INK, "#9a9a9a", "color-on-dark  ·  preferred"),
                ("color-on-light", PAPER, GRAY, "color-on-light"),
                ("mono-black", LIGHT, GRAY, "mono-black"),
                ("mono-white", "#2f4a5c", "#c9d3da", "mono-white")]
    for v, bg, fg, label in variants:
        shot(pg, tile(f"farstudio-logo-horizontal-{v}.svg", bg, 800, 360, 560, label, fg), 800, 360, f"variant-{v}.png")

    # The four pieces, on black, same height so they compare
    pieces = [("logo-vertical", 420, "Vertical · primary"), ("logo-horizontal", 640, "Horizontal · secondary"),
              ("symbol", 240, "Symbol"), ("wordmark-white", 560, "Wordmark")]
    for name, lw, label in pieces:
        f = f"farstudio-{name}{'' if name.startswith('wordmark') else '-color-on-dark'}.svg"
        shot(pg, tile(f, INK, 800, 460, lw, label, "#9a9a9a"), 800, 460, f"piece-{name.replace('-white', '')}.png")

    # Clear space and minimum sizes, on the horizontal logo
    name = "farstudio-logo-horizontal-color-on-light.svg"
    lw = 1100
    lh = lw / ratio(name)
    svg_txt = open(os.path.join(SVG, name)).read()
    vw, vh = map(float, re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg_txt).groups())
    X = 70.3 * lw / vw
    W, H = 1400, int(lh + 260)
    ox, oy = (W - lw) / 2, 90
    mark = f"position:absolute;{FONT};font-size:28px;color:{AMBER};font-weight:600;"
    html = (f"<div style='position:relative;width:{W}px;height:{H}px;background:{PAPER}'>"
            f"<div style='position:absolute;left:{ox}px;top:{oy}px;width:{lw}px;height:{lh}px;"
            f"background:repeating-linear-gradient(45deg,rgba(245,166,35,.13) 0 10px,transparent 10px 20px)'></div>"
            f"<div style='position:absolute;left:{ox + X}px;top:{oy + X}px;width:{lw - 2 * X}px;height:{lh - 2 * X}px;"
            f"background:{PAPER};outline:2px dashed {AMBER}'></div>"
            f"<img src='{uri(name)}' style='position:absolute;left:{ox}px;top:{oy}px;width:{lw}px'>"
            f"<div style='position:absolute;left:{ox}px;top:{oy}px;width:{lw}px;height:{lh}px;outline:2px solid {AMBER}'></div>"
            f"<div style='{mark}left:{ox + X / 2 - 8}px;top:{oy - 52}px'>X</div>"
            f"<div style='position:absolute;left:{ox}px;top:{oy - 12}px;width:{X}px;height:2px;background:{AMBER}'></div>"
            f"<div style='position:absolute;left:{ox}px;top:{oy + lh + 40}px;width:{lw}px;{FONT};font-size:26px;color:{GRAY};"
            f"text-align:center'>Clear space X = the height of the capitals, already inside every file. "
            f"Minimum: vertical 120 px · horizontal 140 px · symbol 16 px.</div></div>")
    shot(pg, html, W, H, "clear-space.png")

    # Palette
    sw = [("Ink", INK, "#111111", PAPER), ("Paper", PAPER, "#FFFFFF", INK), ("Lighthouse light", AMBER, "#F5A623", INK),
          ("Text gray", GRAY, "#555555", PAPER), ("Light gray", LIGHT, "#E8E8E5", INK)]
    cells = "".join(f"<div style='flex:1;background:{c};color:{t};padding:26px 24px;display:flex;flex-direction:column;"
                    f"justify-content:flex-end;{FONT}'><div style='font-size:24px;font-weight:600'>{n}</div>"
                    f"<div style='font-size:20px;opacity:.8;letter-spacing:.06em'>{h}</div></div>" for n, c, h, t in sw)
    shot(pg, f"<div style='display:flex;width:1600px;height:260px;outline:1px solid {LIGHT}'>{cells}</div>",
         1600, 260, "palette.png")

    # Typeface
    html = (f"<div style='width:1600px;height:360px;background:{PAPER};display:flex;flex-direction:column;"
            f"justify-content:center;padding-left:90px;box-sizing:border-box;{FONT};color:{INK}'>"
            f"<div style='font-size:96px;letter-spacing:.22em'><b style='font-weight:600'>FAR</b>"
            f"<span style='font-weight:300'>STUDIO</span></div>"
            f"<div style='font-size:26px;color:{GRAY};margin-top:26px'>Outfit · FAR 600 · STUDIO 300 · capitals · "
            f"letter spacing 0.22 em · supporting text 400</div></div>")
    shot(pg, html, 1600, 360, "typeface.png")
    b.close()
print("ok")
