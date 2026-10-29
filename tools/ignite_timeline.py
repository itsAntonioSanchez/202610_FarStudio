"""The ignite animation as data: the single source for the animated SVGs and the implementation kit.

Times are in milliseconds from the start. Each key holds its values until the next key, eased by
"ease": "hold" jumps at the next key (a flash), a list is a CSS cubic-bezier (x1, y1, x2, y2).
After the last key the values stay as they are: the animation plays once and the light stays on.
"""

DURATION = 4000
OFF = 0.12  # lamp opacity while the light is off

# (start, length, lamp opacity): each flash brighter than the last
FLASHES = [(100, 100, 0.30), (310, 90, 0.45), (540, 120, 0.60), (760, 90, 0.80), (990, 100, 1.00)]

LAMP_ON = (2090, 3350, [0.4, 0, 0.2, 1])     # slow switch-on after a second in the dark
BEAMS_OPEN = (2150, 4000, [0.35, 0, 0.15, 1])  # beams grow out of the lantern
GLOW = (3040, 3600, 4000, 0.6, [0.42, 0, 0.58, 1])  # start, peak, end, peak opacity, curve


def _flash_keys(value, extra):
    keys = [dict(t=0, **value(OFF, 0), **extra, ease="hold")]
    for start, length, level in FLASHES:
        keys.append(dict(t=start, **value(level, round(level / 2, 3)), **extra, ease="hold"))
        keys.append(dict(t=start + length, **value(OFF, 0), **extra, ease="hold"))
    return keys


def tracks():
    lamp = _flash_keys(lambda l, b: {"opacity": l}, {})
    s, e, curve = LAMP_ON
    lamp += [dict(t=s, opacity=OFF, ease=curve), dict(t=e, opacity=1)]

    beams = _flash_keys(lambda l, b: {"opacity": b}, {"scaleX": 1})
    s, e, curve = BEAMS_OPEN
    beams += [dict(t=s, opacity=0, scaleX=0.1, ease=curve), dict(t=e, opacity=1, scaleX=1)]

    s, p, e, peak, curve = GLOW
    glow = [dict(t=0, opacity=0, scale=0.6, ease="hold"), dict(t=s, opacity=0, scale=0.6, ease=curve),
            dict(t=p, opacity=peak, scale=1, ease=curve), dict(t=e, opacity=0, scale=1)]
    return {"lamp": lamp, "beams": beams, "glow": glow}


def _pct(t):
    return f"{t * 100 / DURATION:.3f}".rstrip("0").rstrip(".") + "%"


def _css_keys(keys, props):
    out = []
    for i, k in enumerate(keys):
        decl = ";".join(props(k))
        if "ease" in k:
            fn = "steps(1,end)" if k["ease"] == "hold" else "cubic-bezier({},{},{},{})".format(*k["ease"])
            decl += f";animation-timing-function:{fn}"
        at = _pct(k["t"]) + (",100%" if i == len(keys) - 1 and k["t"] < DURATION else "")
        out.append(f"{at}{{{decl}}}")
    return "".join(out)


def css():
    tr = tracks()
    lamp = _css_keys(tr["lamp"], lambda k: [f"opacity:{k['opacity']}"])
    beams = _css_keys(tr["beams"], lambda k: [f"opacity:{k['opacity']}", f"transform:scaleX({k['scaleX']})"])
    glow = _css_keys(tr["glow"], lambda k: [f"opacity:{k['opacity']}", f"transform:scale({k['scale']})"])
    d = f"{DURATION / 1000:g}s"
    return f"""
.fs-ignite .fs-lamp{{animation:fs-ign-lamp {d} linear 1 both}}
.fs-ignite .fs-beam{{animation:fs-ign-beam {d} linear 1 both}}
.fs-ignite .fs-glow{{animation:fs-ign-glow {d} linear 1 both}}
@keyframes fs-ign-lamp{{{lamp}}}
@keyframes fs-ign-beam{{{beams}}}
@keyframes fs-ign-glow{{{glow}}}
"""
