"""Build the animated FarStudio masters from the static colour SVGs.

Three animations of the lighthouse light, all pure SVG + CSS (no JavaScript). Each plays once and
ends on the static logo:
  rotate  The beam sweeps around once: right, towards you (flash), left, behind (dim), then both beams open.
  blink   The light gives two short flashes off, like a lighthouse signal, then stays on.
  ignite  The lamp flickers, each flash brighter than the last, stays dark for a second, then slowly comes on fully and stays lit.

Plus short versions of the three (tools/short_timelines.py): 1.5 s each including the still pause at the end,
two options of each (…-rotate-short-a.svg, …-blink-short-b.svg and so on).

Usage: python3 tools/animate.py svg svg/animated
"""
import os, sys

import ignite_timeline
import short_timelines

SRC = sys.argv[1]
OUT = sys.argv[2]
os.makedirs(OUT, exist_ok=True)

AMBER = "#F5A623"
PIECES = ("symbol", "logo-vertical", "logo-horizontal")
VARIANTS = ("color-on-dark", "color-on-light")

LAMP = f'<rect x="42" y="23" width="16" height="8" fill="{AMBER}"/>'

# Animation rules are scoped to the svg class so several logos can share one page.
# Shared by every animation. Beams scale from the lantern edge; with reduced motion
# the logo stays exactly as the static master.
BASE_CSS = """
.fs-lamp,.fs-beam,.fs-glow{transform-box:fill-box}
.fs-beam-l{transform-origin:right center}
.fs-beam-r{transform-origin:left center}
.fs-glow{transform-origin:center;opacity:0}
@media (prefers-reduced-motion:reduce){.fs-anim *{animation:none!important}.fs-glow{opacity:0!important}}
"""

CSS = {
    "rotate": short_timelines.css("rotate"),
    "blink": short_timelines.css("blink"),
    "ignite": ignite_timeline.css(),
    **{name: short_timelines.css(name) for name in short_timelines.SHORT},
}


def animate(svg, anim, uid):
    lid = f"L{uid}"
    rid = f"R{uid}"
    beam_l = f'<polygon points="42,24 8,16 8,34 42,29" fill="url(#{lid})"/>'
    beam_r = f'<polygon points="58,24 92,16 92,34 58,29" fill="url(#{rid})"/>'
    light = LAMP + beam_l + beam_r
    assert light in svg, "lantern markup not found"
    glow_id = f"G{uid}{anim}"

    # Unique gradient ids so several animated logos can be inlined in one page.
    svg = svg.replace(f'id="{lid}"', f'id="{lid}{anim}"').replace(f'id="{rid}"', f'id="{rid}{anim}"')
    light_new = (
        f'<g class="fs-light">'
        f'<rect class="fs-lamp" x="42" y="23" width="16" height="8" fill="{AMBER}"/>'
        f'<polygon class="fs-beam fs-beam-l" points="42,24 8,16 8,34 42,29" fill="url(#{lid}{anim})"/>'
        f'<polygon class="fs-beam fs-beam-r" points="58,24 92,16 92,34 58,29" fill="url(#{rid}{anim})"/>'
        f'</g>'
    )
    svg = svg.replace(light, light_new)

    # Soft halo behind the tower, only visible when the light faces the viewer.
    glow = f'<circle class="fs-glow" cx="50" cy="27" r="14" fill="url(#{glow_id})"/>'
    tower = '<g fill="'
    i = svg.index(tower)
    svg = svg[:i] + glow + svg[i:]
    grad = (
        f'<radialGradient id="{glow_id}"><stop offset="0" stop-color="{AMBER}" stop-opacity=".9"/>'
        f'<stop offset=".35" stop-color="{AMBER}" stop-opacity=".35"/>'
        f'<stop offset="1" stop-color="{AMBER}" stop-opacity="0"/></radialGradient>'
    )
    style = "<style>" + (BASE_CSS + CSS[anim]).replace("\n", "") + "</style>"
    svg = svg.replace("<defs>", "<defs>" + grad, 1)
    svg = svg.replace("</defs>", "</defs>" + style, 1)
    svg = svg.replace("<svg ", f'<svg class="fs-anim fs-{anim}" ', 1)
    return svg


for piece in PIECES:
    for variant in VARIANTS:
        with open(os.path.join(SRC, f"farstudio-{piece}-{variant}.svg")) as f:
            src = f.read()
        uid = variant.replace("-", "")
        for anim in CSS:
            name = f"farstudio-{piece}-{variant}-{anim}.svg"
            with open(os.path.join(OUT, name), "w") as f:
                f.write(animate(src, anim, uid))
            print(name)
