"""Build the ignite implementation kit: the timeline as JSON and the logo split into layers.

Every layer is a PNG the size of the whole logo, so they stack without offsets. The pivots in
the JSON say where the beams scale from and where the glow is centered.

Usage: python3 tools/ignite_kit.py svg/animated animation/ignite   (needs Playwright + Chromium)
"""
import base64, json, os, re, sys
from playwright.sync_api import sync_playwright

import ignite_timeline as tl

SRC = sys.argv[1]
OUT = sys.argv[2]
LONG_SIDE = 2048
PIECES = ("symbol", "logo-vertical", "logo-horizontal")

# In the lighthouse's own units (the symbol's 100 x 100 drawing grid).
PIVOTS = {"lamp": (50, 27), "beam-left": (42, 25), "beam-right": (58, 25), "glow": (50, 27)}


def split(svg):
    svg = re.sub(r"<style>.*?</style>", "", svg)
    head = svg[: svg.index("<defs>")]
    head = re.sub(r' class="[^"]*"', "", head, count=1)
    defs = re.search(r"<defs>.*?</defs>", svg).group(0)
    group = re.search(r'<g transform="([^"]*)">', svg)
    parts = {
        "glow": re.search(r'<circle class="fs-glow"[^>]*/>', svg).group(0),
        "lamp": re.search(r'<rect class="fs-lamp"[^>]*/>', svg).group(0),
        "beam-left": re.search(r'<polygon class="fs-beam fs-beam-l"[^>]*/>', svg).group(0),
        "beam-right": re.search(r'<polygon class="fs-beam fs-beam-r"[^>]*/>', svg).group(0),
    }
    base = svg.replace(parts["glow"], "")
    base = re.sub(r'<g class="fs-light">.*?</g>', "", base)
    base = re.sub(r' class="[^"]*"', "", base, count=1)
    layers = {"base": base}
    for name, el in parts.items():
        el = re.sub(r' class="[^"]*"', "", el)
        layers[name] = f'{head}{defs}<g transform="{group.group(1)}">{el}</g></svg>'
    return layers, group.group(1)


def to_canvas(transform, x, y):
    t = re.search(r"translate\(([-\d.]+) ([-\d.]+)\)", transform)
    s = re.search(r"scale\(([\d.]+)\)", transform)
    tx, ty = float(t.group(1)), float(t.group(2))
    k = float(s.group(1)) if s else 1.0
    return tx + k * x, ty + k * y


def view_box(svg):
    m = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg)
    return float(m.group(1)), float(m.group(2))


def png(page, svg, w, h, out):
    uri = "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()
    page.set_viewport_size({"width": w, "height": h})
    page.set_content(f'<html><body style="margin:0;background:transparent"><img src="{uri}" style="display:block;width:{w}px;height:{h}px"></body></html>')
    page.wait_for_timeout(30)
    page.screenshot(path=out, omit_background=True, clip={"x": 0, "y": 0, "width": w, "height": h})


os.makedirs(OUT, exist_ok=True)
info = {}
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ.get("CHROMIUM") or None)
    page = b.new_page()
    for piece in PIECES:
        folder = os.path.join(OUT, "layers", piece)
        os.makedirs(folder, exist_ok=True)
        for variant in ("color-on-dark", "color-on-light"):
            svg = open(os.path.join(SRC, f"farstudio-{piece}-{variant}-ignite.svg")).read()
            layers, transform = split(svg)
            vw, vh = view_box(svg)
            w, h = (LONG_SIDE, round(LONG_SIDE * vh / vw)) if vw >= vh else (round(LONG_SIDE * vw / vh), LONG_SIDE)
            png(page, layers["base"], w, h, os.path.join(folder, f"base-{variant}.png"))
            if variant == "color-on-dark":  # the light is the same amber on both backgrounds
                for name in PIVOTS:
                    png(page, layers[name], w, h, os.path.join(folder, f"{name}.png"))
                pivots = {}
                for name, (x, y) in PIVOTS.items():
                    cx, cy = to_canvas(transform, x, y)
                    pivots[name] = {"x": round(cx / vw, 4), "y_from_top": round(cy / vh, 4), "y_from_bottom": round(1 - cy / vh, 4)}
                info[piece] = {"size_px": [w, h], "pivots": pivots}
    b.close()

def portable(keys):
    """Engine-friendly keys: ease is "hold", "bezier" (with its four numbers) or "" on the last key."""
    out = []
    for k in keys:
        k = dict(k)
        e = k.pop("ease", "")
        if isinstance(e, list):
            k["ease"], k["bezier"] = "bezier", e
        else:
            k["ease"] = e
        out.append(k)
    return out


tracks = {name: portable(keys) for name, keys in tl.tracks().items()}
timeline = {
    "name": "FarStudio ignite",
    "duration_ms": tl.DURATION,
    "plays": "once; after the last key every value holds, so the logo stays lit",
    "ease": "each key's ease shapes the move to the next key: 'hold' keeps the value and jumps at the next key; 'bezier' eases with the CSS cubic-bezier in 'bezier' (x1, y1, x2, y2)",
    "layers_bottom_to_top": ["glow", "base", "lamp", "beam-left", "beam-right"],
    "tracks": {
        "lamp": {"layers": ["lamp"], "keys": tracks["lamp"]},
        "beams": {"layers": ["beam-left", "beam-right"], "scale_from": "each beam's pivot, scaleX only", "keys": tracks["beams"]},
        "glow": {"layers": ["glow"], "scale_from": "glow pivot, both axes", "keys": tracks["glow"]},
    },
    "pieces": info,
}
with open(os.path.join(OUT, "ignite-timeline.json"), "w") as f:
    json.dump(timeline, f, indent=2)
    f.write("\n")
print("ok", OUT)
