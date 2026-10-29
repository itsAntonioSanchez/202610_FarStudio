"""Timelines for the rotate and blink animations, long and short, as keyframes.

Every one plays once and ends on the static logo. The short ones last 1.5 s, counting the still
pause at the end. Keys are (time in ms, values, ease to the next key):
"hold" keeps the value and jumps at the next key, a list is a CSS cubic-bezier, None ends the track.
"""

TOTAL = 1500
IO, OUT, SOFT, SOFTER, SYM = [.45, 0, .55, 1], [.22, 1, .36, 1], [.4, 0, .2, 1], [.35, 0, .15, 1], [.42, 0, .58, 1]
H = "hold"


def beam(on, sx=None):
    return {"opacity": on, "scaleX": on if sx is None else sx}


def glow(o, s):
    return {"opacity": o, "scale": s}


def ignite(flashes, dark_end, lamp_end, beams_start, beams_end, halo):
    lamp = [(0, {"opacity": .12}, H)]
    beams = [(0, beam(0, 1), H)]
    for s, d, level in flashes:
        lamp += [(s, {"opacity": level}, H), (s + d, {"opacity": .12}, H)]
        beams += [(s, beam(round(level / 2, 3), 1), H), (s + d, beam(0, 1), H)]
    lamp += [(dark_end, {"opacity": .12}, SOFT), (lamp_end, {"opacity": 1}, None)]
    beams += [(beams_start, beam(0, .1), SOFTER), (beams_end, beam(1), None)]
    gs, gp, ge = halo
    g = [(0, glow(0, .6), H), (gs, glow(0, .6), SYM), (gp, glow(.5, 1), SYM), (ge, glow(0, 1), None)]
    return {"lamp": lamp, "beam-l": beams, "beam-r": beams, "glow": g}


def blink(offs):
    keys = [(0, {"opacity": 1}, H)]
    for s, e in offs:
        keys += [(s, {"opacity": .12}, H), (e, {"opacity": 1}, H)]
    return {"light": keys}


# name -> (what it does, ms until the logo is still, tracks)
SHORT = {
    "rotate-short-a": ("Half turn: right, towards you (flash), left, then both beams open.", 1100, {
        "beam-r": [(0, beam(1), IO), (350, beam(0), H), (700, beam(0), OUT), (1100, beam(1), None)],
        "beam-l": [(0, beam(0), H), (350, beam(0), IO), (700, beam(1), None)],
        "glow": [(0, glow(0, .6), H), (170, glow(0, .6), SYM), (350, glow(1, 1), SYM), (600, glow(0, 1), None)],
    }),
    "rotate-short-b": ("One fast full turn, then both beams open.", 1150, {
        "beam-r": [(0, beam(1), IO), (225, beam(0), H), (675, beam(0), IO), (900, beam(1), None)],
        "beam-l": [(0, beam(0), H), (225, beam(0), IO), (450, beam(1), IO), (675, beam(0), H), (900, beam(0), OUT), (1150, beam(1), None)],
        "lamp": [(0, {"opacity": 1}, H), (450, {"opacity": 1}, SYM), (675, {"opacity": .45}, SYM), (900, {"opacity": 1}, None)],
        "glow": [(0, glow(0, .6), H), (110, glow(0, .6), SYM), (225, glow(1, 1), SYM), (380, glow(0, 1), None)],
    }),
    "blink-short-a": ("Two short blackouts, like the long blink.", 730, blink([(450, 530), (650, 730)])),
    "blink-short-b": ("Three blackouts closer together, like a lighthouse signal.", 680, blink([(300, 360), (460, 520), (620, 680)])),
    "ignite-short-a": ("Three flashes getting brighter, a moment in the dark, then the light comes up.", 1150,
                       ignite([(60, 70, .35), (190, 70, .6), (330, 80, 1.0)], 600, 1000, 620, 1150, (850, 1000, 1150))),
    "ignite-short-b": ("The five flashes of the long ignite, compressed, with almost no pause.", 1100,
                       ignite([(40, 50, .3), (130, 45, .45), (225, 55, .6), (320, 45, .8), (410, 55, 1.0)], 620, 980, 640, 1100, (820, 960, 1100))),
}

# The long versions: same pace as the original loops, played once.
LONG = {
    "rotate": ("The beam sweeps around once: right, towards you (flash), left, behind (dim), then both beams open.", 5500, {
        "beam-r": [(0, beam(1), IO), (1500, beam(0), H), (4500, beam(0), OUT), (5500, beam(1), None)],
        "beam-l": [(0, beam(0), H), (1500, beam(0), IO), (3000, beam(1), IO), (4500, beam(0), OUT), (5500, beam(1), None)],
        "lamp": [(0, {"opacity": 1}, H), (3000, {"opacity": 1}, SYM), (4500, {"opacity": .45}, SYM), (5500, {"opacity": 1}, None)],
        "glow": [(0, glow(0, .6), H), (750, glow(0, .6), SYM), (1500, glow(1, 1), SYM), (2250, glow(0, 1), None)],
    }),
    "blink": ("The light is on and gives two short flashes off, like a lighthouse signal, then stays on.", 1340,
              blink([(600, 760), (1180, 1340)])),
}

TARGET = {"lamp": ".fs-lamp", "beam-l": ".fs-beam-l", "beam-r": ".fs-beam-r", "glow": ".fs-glow", "light": ".fs-light"}


def _pct(t, total):
    return f"{t * 100 / total:.3f}".rstrip("0").rstrip(".") + "%"


def _decl(vals):
    out = [f"opacity:{vals['opacity']}"]
    if "scaleX" in vals:
        out.append(f"transform:scaleX({vals['scaleX']})")
    if "scale" in vals:
        out.append(f"transform:scale({vals['scale']})")
    return ";".join(out)


def css(name):
    """CSS for one animation, scoped to its svg class (fs-<name>)."""
    if name in LONG:
        _, total, tracks = LONG[name]
    else:
        total, tracks = TOTAL, SHORT[name][2]
    out = []
    for track, keys in tracks.items():
        frames = []
        for i, (t, vals, ease) in enumerate(keys):
            d = _decl(vals)
            if ease == H:
                d += ";animation-timing-function:steps(1,end)"
            elif ease:
                d += ";animation-timing-function:cubic-bezier({},{},{},{})".format(*ease)
            at = _pct(t, total) + (",100%" if i == len(keys) - 1 and t < total else "")
            frames.append(f"{at}{{{d}}}")
        kf = f"fs-{name}-{track}"
        out.append(f".fs-{name} {TARGET[track]}{{animation:{kf} {total}ms linear 1 both}}")
        out.append(f"@keyframes {kf}{{{''.join(frames)}}}")
    return "\n" + "\n".join(out) + "\n"
