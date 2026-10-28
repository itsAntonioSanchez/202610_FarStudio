"""Build the FarStudio vector masters: text converted to outlines, no font needed."""
import os, sys
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

FONT = sys.argv[1]
OUT = sys.argv[2]
os.makedirs(OUT, exist_ok=True)

INK, PAPER, AMBER = "#111111", "#FFFFFF", "#F5A623"
TRACK = 0.22

fonts = {}
for w in (300, 600):
    f = TTFont(FONT)
    fonts[w] = instantiateVariableFont(f, {"wght": w})

UPM = fonts[600]["head"].unitsPerEm
CAP = fonts[600]["OS/2"].sCapHeight / UPM  # cap height in em


def text_paths(parts, size):
    """parts: [(text, weight)] -> (svg path markup, width, cap height) with baseline at y=0."""
    s = size / UPM
    x = 0.0
    out = []
    for i, (txt, w) in enumerate(parts):
        f = fonts[w]
        gs = f.getGlyphSet()
        cmap = f.getBestCmap()
        hmtx = f["hmtx"]
        for j, ch in enumerate(txt):
            gname = cmap[ord(ch)]
            pen = SVGPathPen(gs)
            tp = TransformPen(pen, (s, 0, 0, -s, x, 0))
            gs[gname].draw(tp)
            d = pen.getCommands()
            if d:
                out.append(d)
            adv = hmtx[gname][0] * s
            last = (i == len(parts) - 1 and j == len(txt) - 1)
            x += adv + (0 if last else TRACK * size)
    return " ".join(out), x, CAP * size


def symbol(fill, light="gradient", uid="a"):
    """The lighthouse in a 100x100 box. light: 'gradient' (brand), 'solid' (one ink)."""
    struct = (f'<g fill="{fill}"><polygon points="40,22 60,22 50,13"/>'
              '<polygon points="40,34 60,34 62.22,54 37.78,54"/>'
              '<polygon points="36.89,62 63.11,62 66,88 34,88"/>'
              '<rect x="26" y="89" width="48" height="4" rx="2"/></g>')
    if light == "gradient":
        defs = (f'<defs><linearGradient id="L{uid}" gradientUnits="userSpaceOnUse" x1="42" y1="0" x2="8" y2="0">'
                f'<stop offset="0" stop-color="{AMBER}"/><stop offset="1" stop-color="{AMBER}" stop-opacity="0.15"/></linearGradient>'
                f'<linearGradient id="R{uid}" gradientUnits="userSpaceOnUse" x1="58" y1="0" x2="92" y2="0">'
                f'<stop offset="0" stop-color="{AMBER}"/><stop offset="1" stop-color="{AMBER}" stop-opacity="0.15"/></linearGradient></defs>')
        lightg = (f'<rect x="42" y="23" width="16" height="8" fill="{AMBER}"/>'
                  f'<polygon points="42,24 8,16 8,34 42,29" fill="url(#L{uid})"/>'
                  f'<polygon points="58,24 92,16 92,34 58,29" fill="url(#R{uid})"/>')
        return defs, struct + lightg
    lightg = (f'<g fill="{fill}"><rect x="42" y="23" width="16" height="8"/>'
              '<polygon points="42,24 8,16 8,34 42,29"/><polygon points="58,24 92,16 92,34 58,29"/></g>')
    return "", struct + lightg


# Symbol bounding box inside its 100 box (for tight framing)
SYM_BOX = (8, 13, 92, 93)  # x0, y0, x1, y1


def svg_doc(w, h, body, defs="", bg=None):
    bgr = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.2f} {h:.2f}" width="{w:.2f}" height="{h:.2f}">'
            f'{defs}{bgr}{body}</svg>')


def write(name, txt):
    with open(os.path.join(OUT, name), "w") as fh:
        fh.write(txt)


VARIANTS = {
    # name: (structure/text color, light mode)
    "color-on-light": (INK, "gradient"),
    "color-on-dark": (PAPER, "gradient"),
    "mono-black": (INK, "solid"),
    "mono-white": (PAPER, "solid"),
}

F = 100.0  # wordmark size unit for masters
word_d, word_w, cap = text_paths([("FAR", 600), ("STUDIO", 300)], F)
X = cap  # clear space unit: the cap height of the wordmark

for vname, (col, mode) in VARIANTS.items():
    uid = vname.replace("-", "")
    # --- Symbol alone: tight box plus 8% margin
    defs, sym = symbol(col, mode, uid)
    x0, y0, x1, y1 = SYM_BOX
    sw, sh = x1 - x0, y1 - y0
    m = 0.08 * max(sw, sh)
    W, H = sw + 2 * m, sh + 2 * m
    body = f'<g transform="translate({m - x0:.3f} {m - y0:.3f})">{sym}</g>'
    write(f"farstudio-symbol-{vname}.svg", svg_doc(W, H, body, defs))

    # --- Wordmark alone, with clear space X
    word = f'<path d="{word_d}" fill="{col}"/>'
    W, H = word_w + 2 * X, cap + 2 * X
    write(f"farstudio-wordmark-{'black' if col == INK else 'white'}.svg",
          svg_doc(W, H, f'<g transform="translate({X:.3f} {X + cap:.3f})">{word}</g>'))

    # --- Horizontal lockup: [symbol] | NAME
    S = 2.4 * F                     # symbol height (100-box scaled)
    k = S / 100.0
    sym_w = (x1 - x0) * k
    gap1 = 0.55 * F
    sep_w = 0.07 * F
    gap2 = 0.65 * F
    sep_h = 1.5 * F
    content_w = sym_w + gap1 + sep_w + gap2 + word_w
    content_h = (y1 - y0) * k
    W, H = content_w + 2 * X, content_h + 2 * X
    cy = X + content_h / 2
    sym_g = f'<g transform="translate({X - x0 * k:.3f} {X - y0 * k:.3f}) scale({k:.5f})">{sym}</g>'
    sep_x = X + sym_w + gap1
    sep = f'<rect x="{sep_x:.3f}" y="{cy - sep_h / 2:.3f}" width="{sep_w:.3f}" height="{sep_h:.3f}" fill="{col}"/>'
    tx = sep_x + sep_w + gap2
    word_g = f'<g transform="translate({tx:.3f} {cy + cap / 2:.3f})">{word}</g>'
    write(f"farstudio-logo-horizontal-{vname}.svg", svg_doc(W, H, sym_g + sep + word_g, defs))

    # --- Vertical lockup: symbol over NAME
    S = 4.2 * F
    k = S / 100.0
    sym_w, sym_h = (x1 - x0) * k, (y1 - y0) * k
    gap = 0.6 * F
    content_w = max(sym_w, word_w)
    content_h = sym_h + gap + cap
    W, H = content_w + 2 * X, content_h + 2 * X
    sx = X + (content_w - sym_w) / 2
    sym_g = f'<g transform="translate({sx - x0 * k:.3f} {X - y0 * k:.3f}) scale({k:.5f})">{sym}</g>'
    wx = X + (content_w - word_w) / 2
    word_g = f'<g transform="translate({wx:.3f} {X + sym_h + gap + cap:.3f})">{word}</g>'
    write(f"farstudio-logo-vertical-{vname}.svg", svg_doc(W, H, sym_g + word_g, defs))

# --- App icon and avatar: ink background, white structure, amber light
defs, sym = symbol(PAPER, "gradient", "icon")
for name, scale, shape in (("farstudio-app-icon", 0.74, "square"), ("farstudio-avatar", 0.62, "square")):
    W = H = 1024
    k = W * scale / 100.0
    x0, y0, x1, y1 = SYM_BOX
    ox = (W - (x1 - x0) * k) / 2 - x0 * k
    oy = (H - (y1 - y0) * k) / 2 - y0 * k
    body = f'<g transform="translate({ox:.3f} {oy:.3f}) scale({k:.5f})">{sym}</g>'
    write(f"{name}.svg", svg_doc(W, H, body, defs, INK))

# Rounded app icon and round avatar (transparent corners)
W = 1024
k = W * 0.74 / 100.0
ox = (W - 84 * k) / 2 - 8 * k
oy = (W - 80 * k) / 2 - 13 * k
write("farstudio-app-icon-rounded.svg", svg_doc(W, W,
      f'<rect width="{W}" height="{W}" rx="{W * 0.2237:.2f}" fill="{INK}"/>'
      f'<g transform="translate({ox:.3f} {oy:.3f}) scale({k:.5f})">{sym}</g>', defs))
k = W * 0.62 / 100.0
ox = (W - 84 * k) / 2 - 8 * k
oy = (W - 80 * k) / 2 - 13 * k
write("farstudio-avatar-circle.svg", svg_doc(W, W,
      f'<circle cx="{W / 2}" cy="{W / 2}" r="{W / 2}" fill="{INK}"/>'
      f'<g transform="translate({ox:.3f} {oy:.3f}) scale({k:.5f})">{sym}</g>', defs))

print("cap", cap, "word_w", word_w)
