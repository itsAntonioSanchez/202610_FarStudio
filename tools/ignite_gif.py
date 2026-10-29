"""Record the ignite animation as a GIF for the README, frame by frame in headless Chromium.

Usage: python3 tools/ignite_gif.py svg/animated/farstudio-logo-vertical-color-on-dark-ignite.svg docs/readme/ignite.gif
"""
import io, os, sys
from PIL import Image
from playwright.sync_api import sync_playwright

import ignite_timeline as tl

SRC, OUT = sys.argv[1], sys.argv[2]
W, H = 720, 500
STEP = 30     # ms per frame
HOLD = 2000   # the lit logo stays on screen before the GIF starts over

svg = open(SRC).read()
html = (f'<html><body style="margin:0;background:#111111;width:{W}px;height:{H}px;display:flex;'
        f'align-items:center;justify-content:center">'
        f'<div style="width:{int(W * 0.7)}px">{svg.replace("<svg ", "<svg style=\'width:100%;height:auto;display:block\' ", 1)}</div></body></html>')

frames = []
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ.get("CHROMIUM") or None)
    page = b.new_page(viewport={"width": W, "height": H})
    page.set_content(html)
    for t in range(0, tl.DURATION + 1, STEP):
        page.evaluate("t => document.getAnimations().forEach(a => { a.pause(); a.currentTime = t; })", min(t, tl.DURATION))
        frames.append(Image.open(io.BytesIO(page.screenshot())).convert("RGB"))
    b.close()

# One shared palette keeps the amber steady from frame to frame.
picks = frames[:: max(1, len(frames) // 12)] + [frames[-1]]
sheet = Image.new("RGB", (W * len(picks), H))
for i, f in enumerate(picks):
    sheet.paste(f, (i * W, 0))
palette = sheet.quantize(colors=160, method=Image.Quantize.MEDIANCUT)
gif = [f.quantize(palette=palette, dither=Image.Dither.NONE) for f in frames]
durations = [STEP] * (len(gif) - 1) + [HOLD]
os.makedirs(os.path.dirname(OUT), exist_ok=True)
gif[0].save(OUT, save_all=True, append_images=gif[1:], duration=durations, loop=0, optimize=True, disposal=1)
print(OUT, len(gif), "frames", os.path.getsize(OUT) // 1024, "KB")
