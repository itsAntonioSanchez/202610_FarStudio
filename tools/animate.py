"""Build the animated FarStudio masters from the static colour SVGs.

Three animations of the lighthouse light, all pure SVG + CSS (no JavaScript):
  rotate  The beam sweeps around the lantern: right, towards you (flash), left, behind (dim).
  blink   The light stays on and gives two short flashes off, like a lighthouse signal.
  ignite  Plays once: the lamp flickers on and off, then slowly comes on fully and stays lit.

Usage: python3 tools/animate.py svg svg/animated
"""
import os, sys

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
    "rotate": """
.fs-rotate .fs-beam-r{animation:fs-rot-r 6s cubic-bezier(.45,0,.55,1) infinite}
.fs-rotate .fs-beam-l{animation:fs-rot-l 6s cubic-bezier(.45,0,.55,1) infinite}
.fs-rotate .fs-lamp{animation:fs-rot-lamp 6s ease-in-out infinite}
.fs-rotate .fs-glow{animation:fs-rot-glow 6s ease-in-out infinite}
@keyframes fs-rot-r{0%{transform:scaleX(1);opacity:1}25%,75%{transform:scaleX(0);opacity:0}100%{transform:scaleX(1);opacity:1}}
@keyframes fs-rot-l{0%,25%{transform:scaleX(0);opacity:0}50%{transform:scaleX(1);opacity:1}75%,100%{transform:scaleX(0);opacity:0}}
@keyframes fs-rot-lamp{0%,50%,100%{opacity:1}25%{opacity:1}75%{opacity:.45}}
@keyframes fs-rot-glow{0%,12%,38%,100%{opacity:0;transform:scale(.6)}25%{opacity:1;transform:scale(1)}}
""",
    "blink": """
.fs-blink .fs-light{animation:fs-blink 3.2s linear infinite}
@keyframes fs-blink{0%,54%{opacity:1}57%,62%{opacity:.12}65%,72%{opacity:1}75%,80%{opacity:.12}83%,100%{opacity:1}}
""",
    "ignite": """
.fs-ignite .fs-lamp{animation:fs-ign-lamp 4.5s linear 1 both}
.fs-ignite .fs-beam{animation:fs-ign-beam 4.5s linear 1 both}
.fs-ignite .fs-glow{animation:fs-ign-glow 4.5s ease-in-out 1 both}
@keyframes fs-ign-lamp{0%{opacity:.12}3%{opacity:1}6%{opacity:.12}9%{opacity:.85}11%{opacity:.12}15%{opacity:1}18%{opacity:.12}30%{opacity:.12;animation-timing-function:ease-in-out}75%,100%{opacity:1}}
@keyframes fs-ign-beam{0%{opacity:0;transform:scaleX(1)}3%{opacity:.5}6%{opacity:0}9%{opacity:.4}11%{opacity:0}15%{opacity:.5}18%{opacity:0;transform:scaleX(1)}40%{opacity:0;transform:scaleX(.15);animation-timing-function:cubic-bezier(.3,0,.2,1)}100%{opacity:1;transform:scaleX(1)}}
@keyframes fs-ign-glow{0%,70%{opacity:0;transform:scale(.6)}88%{opacity:.6;transform:scale(1)}100%{opacity:0;transform:scale(1)}}
""",
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
