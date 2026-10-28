"""Render the FarStudio masters to PNG at every size, with headless Chromium."""
import os, re, sys, base64
from playwright.sync_api import sync_playwright

SVG = sys.argv[1]
OUT = sys.argv[2]


def svg_size(path):
    t = open(path).read()
    m = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', t)
    return float(m.group(1)), float(m.group(2))


SIZES = {
    "symbol": [3840, 2048, 1024, 512, 256, 128, 64, 32, 16],
    "logo-horizontal": [3840, 2560, 1920, 1280, 1024, 512, 256],
    "logo-vertical": [3840, 2560, 1920, 1280, 1024, 512, 256],
    "wordmark": [3840, 1920, 1024, 512, 256],
    "app-icon": [1024, 512, 256, 192, 180, 167, 152, 128, 120, 96, 87, 80, 76, 64, 58, 48, 40, 32, 29, 20, 16],
    "avatar": [2048, 1024, 800, 512, 400, 256, 128, 64],
}

INK, PAPER = "#111111", "#FFFFFF"


def data_uri(path):
    return "data:image/svg+xml;base64," + base64.b64encode(open(path, "rb").read()).decode()


def shot(page, html, w, h, out, transparent=True):
    page.set_viewport_size({"width": int(w), "height": int(h)})
    page.set_content(f'<html><body style="margin:0;background:transparent">{html}</body></html>')
    page.wait_for_timeout(30)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    page.screenshot(path=out, omit_background=transparent, clip={"x": 0, "y": 0, "width": int(w), "height": int(h)})


def place(path, w, h):
    return f'<img src="{data_uri(path)}" style="display:block;width:{w}px;height:{h}px">'


with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page()
    count = 0
    for fn in sorted(os.listdir(SVG)):
        if not fn.endswith(".svg"):
            continue
        base = fn[:-4]
        path = os.path.join(SVG, fn)
        vw, vh = svg_size(path)
        kind = next(k for k in SIZES if base.startswith("farstudio-" + k))
        folder = os.path.join(OUT, kind, base.replace("farstudio-" + kind, "").strip("-") or "square")
        for s in SIZES[kind]:
            # s is the longest side
            if vw >= vh:
                w, h = s, round(s * vh / vw)
            else:
                w, h = round(s * vw / vh), s
            shot(page, place(path, w, h), w, h, os.path.join(folder, f"{base}-{w}x{h}.png"))
            count += 1

    # Favicons and touch icon, from the rounded app icon
    icon = os.path.join(SVG, "farstudio-app-icon-rounded.svg")
    sq = os.path.join(SVG, "farstudio-app-icon.svg")
    fav = os.path.join(OUT, "favicon")
    for s in (16, 32, 48, 192, 512):
        shot(page, place(icon, s, s), s, s, os.path.join(fav, f"favicon-{s}x{s}.png"))
    shot(page, place(sq, 180, 180), 180, 180, os.path.join(fav, "apple-touch-icon-180x180.png"), transparent=False)

    # Banners and screens, composed on ink or paper
    def compose(name, W, H, logo, logo_w=None, logo_h=None, bg=INK, caption=None):
        lw, lh = svg_size(os.path.join(SVG, logo))
        if logo_w:
            w, h = logo_w, logo_w * lh / lw
        else:
            w, h = logo_h * lw / lh, logo_h
        img = place(os.path.join(SVG, logo), round(w), round(h))
        html = (f'<div style="width:{W}px;height:{H}px;background:{bg};display:flex;align-items:center;'
                f'justify-content:center">{img}</div>')
        shot(page, html, W, H, os.path.join(OUT, "banners", f"{name}-{W}x{H}.png"), transparent=False)

    compose("youtube-banner", 2560, 1440, "farstudio-logo-horizontal-color-on-dark.svg", logo_w=1200)
    compose("store-feature-graphic", 1024, 500, "farstudio-logo-horizontal-color-on-dark.svg", logo_w=700)
    compose("social-header", 1500, 500, "farstudio-logo-horizontal-color-on-dark.svg", logo_w=900)
    compose("link-preview", 1200, 630, "farstudio-logo-vertical-color-on-dark.svg", logo_h=420)
    for W, H in ((3840, 2160), (2560, 1440), (1920, 1080), (1280, 720)):
        compose("splash-dark", W, H, "farstudio-logo-vertical-color-on-dark.svg", logo_h=round(H * 0.42))
        compose("splash-light", W, H, "farstudio-logo-vertical-color-on-light.svg", logo_h=round(H * 0.42), bg=PAPER)
    b.close()
    print("rendered", count, "logo files")
