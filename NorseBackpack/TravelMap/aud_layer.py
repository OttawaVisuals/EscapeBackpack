"""Draw the designer's symbol layer onto Aud's printed sheet.

`aud_features.json` stores PAGE POINTS, not coordinates, so it is only valid at the frame it was
drawn against -- `export_aud_base.py`'s ZOOM_FRAME, which is what `TRAILS["aud"]["frame"]` now is.
Change that frame and the coastline slides out from under every symbol; `assert_frame` makes that
fail loudly instead of quietly producing a wrong sheet.

Appearance is ported from Aud_Map_Designer.html so the sheet matches what you drew. When a symbol
changes there it has to change here too -- there is no shared source, because one side is SVG in a
browser and the other is ReportLab.
"""
import json
import math
from pathlib import Path

from reportlab.lib.colors import HexColor

HERE = Path(__file__).resolve().parent
LAYER = HERE / "aud_features.json"

# Mirrors SYMBOLS in Aud_Map_Designer.html.
LINE = {
    "hedge":   dict(color="#4A6B3A", w=1.4, smooth=True),
    "wall":    dict(color="#6E6A5E", w=1.1, smooth=False),
    "road":    dict(color="#8A5A32", w=2.6, smooth=True),
    "track":   dict(color="#B08A5A", w=1.0, dash=(3.2, 2.2), smooth=True),
    "path":    dict(color="#9A8A6A", w=0.9, dash=(1.2, 2.2), smooth=True),
    "river":   dict(color="#2F7775", w=1.6, smooth=True),
    "stream":  dict(color="#2F7775", w=0.8, smooth=True),
    "ditch":   dict(color="#6B7A6B", w=0.9, smooth=False),
    "contour": dict(color="#A9895E", w=0.5, smooth=True),
}
AREA = {
    "wood":  dict(color="#4A6B3A", fill="#CBD9BE"),
    "marsh": dict(color="#6F8070", fill="#D9DDD0"),
    "lake":  dict(color="#2F7775", fill="#DCE7E4"),
    "field": dict(color="#B08A5A", fill="#F0E7CE"),
    "moor":  dict(color="#8A7A5E", fill="#E8DFC6"),
}
# Ordinary landmarks stay visible but intentionally recede. Crossings are the puzzle's
# countable events, so they get the strongest ink weight on the sheet.
LANDMARK = "#806F96"
CROSSING = "#523A70"
POINT_COLOR = {"marker": "#B56A2A", "bridge": CROSSING, "gate": CROSSING,
               "ford": "#216866", "text": "#283B34"}
PURPLE = LANDMARK


def load(path=None):
    d = json.loads(Path(path or LAYER).read_text(encoding="utf-8"))
    return d["frame"], d["features"]


def assert_frame(frame, cfg_frame, key="aud"):
    """The export is page points, so it only means anything at the frame it was drawn against."""
    want = (round(frame["lon0"], 4), round(frame["lon1"], 4),
            round(frame["lat0"], 4), round(frame["lat1"], 4))
    got = tuple(round(v, 4) for v in cfg_frame)
    if want != got:
        raise ValueError(
            "%s: aud_features.json was drawn against frame %s but the sheet is being built at %s. "
            "The layer stores page points, not coordinates, so the coastline would slide out from "
            "under every symbol. Re-run export_aud_base.py and redraw, or restore the frame."
            % (key, want, got))


def _catmull(pts, closed):
    """Same curve the designer uses, so a smoothed line prints as it was drawn."""
    if len(pts) < 3:
        return None
    p = ([pts[-1]] + list(pts) + [pts[0], pts[1]]) if closed else \
        ([pts[0]] + list(pts) + [pts[-1]])
    out = [("m", pts[0][0], pts[0][1])]
    for i in range(1, len(p) - 2):
        p0, p1, p2, p3 = p[i - 1], p[i], p[i + 1], p[i + 2]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6.0, p1[1] + (p2[1] - p0[1]) / 6.0)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6.0, p2[1] - (p3[1] - p1[1]) / 6.0)
        out.append(("c", c1[0], c1[1], c2[0], c2[1], p2[0], p2[1]))
    return out


def _path(c, f, closed, smooth):
    segs = _catmull(f["pts"], closed) if (smooth and len(f["pts"]) > 2) else None
    p = c.beginPath()
    if segs:
        p.moveTo(segs[0][1], segs[0][2])
        for s in segs[1:]:
            p.curveTo(*s[1:])
    else:
        p.moveTo(*f["pts"][0])
        for q in f["pts"][1:]:
            p.lineTo(*q)
    if closed:
        p.close()
    return p


def _sample(f, closed, smooth, step=1.0):
    """Points along the drawn shape, for scattering hedge blobs and wall ticks."""
    segs = _catmull(f["pts"], closed) if (smooth and len(f["pts"]) > 2) else None
    pts = []
    if segs:
        cur = (segs[0][1], segs[0][2])
        pts.append(cur)
        for s in segs[1:]:
            x1, y1, x2, y2, x3, y3 = s[1:]
            n = 12
            for k in range(1, n + 1):
                t = k / n
                mt = 1 - t
                x = (mt ** 3) * cur[0] + 3 * (mt ** 2) * t * x1 + 3 * mt * (t ** 2) * x2 + (t ** 3) * x3
                y = (mt ** 3) * cur[1] + 3 * (mt ** 2) * t * y1 + 3 * mt * (t ** 2) * y2 + (t ** 3) * y3
                pts.append((x, y))
            cur = (x3, y3)
    else:
        pts = [tuple(q) for q in f["pts"]]
        if closed:
            pts.append(pts[0])
    out, acc = [], 0.0
    for a, b in zip(pts, pts[1:]):
        d = math.hypot(b[0] - a[0], b[1] - a[1])
        if d == 0:
            continue
        while acc < d:
            t = acc / d
            out.append((a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t,
                        math.atan2(b[1] - a[1], b[0] - a[0])))
            acc += step
        acc -= d
    return out


def _offset_feature(f, delta):
    """Return a shallow feature copy offset locally from its centre line."""
    pts = f["pts"]
    shifted = []
    for i, p in enumerate(pts):
        a = pts[max(0, i - 1)]
        b = pts[min(len(pts) - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        mag = math.hypot(dx, dy) or 1.0
        shifted.append([p[0] - dy / mag * delta, p[1] + dx / mag * delta])
    out = dict(f)
    out["pts"] = shifted
    return out


def _ornament(c, f, gate_gaps=None):
    """Draw line ornaments, leaving a true opening in walls wherever a gate sits."""
    kind = f["kind"]
    s = LINE[kind]
    step = 4.8 if kind == "hedge" else 6.0 if kind == "wall" else 6.5
    c.setFillColor(HexColor(s["color"]))
    c.setStrokeColor(HexColor(s["color"]))
    c.setLineWidth(0.55)
    for x, y, ang in _sample(f, False, f.get("smooth", s.get("smooth", False)), step):
        if kind == "wall" and any(math.hypot(x-gx, y-gy) < 8.5
                                  for gx, gy in (gate_gaps or ())):
            continue
        if kind == "hedge":
            c.circle(x, y, 1.7, stroke=0, fill=1)
        elif kind == "wall":
            # Option B: irregular linked stone blocks rather than survey divisions.
            ca, sa = math.cos(ang), math.sin(ang)
            na, nb = -sa, ca
            hw = 2.5
            hh = 1.35 if int((x + y) / step) % 2 else 1.7
            pts = [(x - ca*hw - na*hh, y - sa*hw - nb*hh),
                   (x + ca*hw - na*hh*.8, y + sa*hw - nb*hh*.8),
                   (x + ca*hw + na*hh, y + sa*hw + nb*hh),
                   (x - ca*hw + na*hh*.75, y - sa*hw + nb*hh*.75)]
            p = c.beginPath(); p.moveTo(*pts[0])
            for q in pts[1:]: p.lineTo(*q)
            p.close(); c.drawPath(p, stroke=1, fill=0)
        else:
            a = ang + math.pi / 2
            # Ditch: hachures stay on one side of the centre line.
            c.line(x, y, x + math.cos(a + .45) * 4.0, y + math.sin(a + .45) * 4.0)


def _area_texture(c, f):
    """Survey texture family: sparse, regular terrain marks."""
    kind = f["kind"]
    if kind not in ("wood", "marsh", "moor", "field", "lake"):
        return
    pts = f["pts"]
    x0, x1 = min(p[0] for p in pts), max(p[0] for p in pts)
    y0, y1 = min(p[1] for p in pts), max(p[1] for p in pts)
    c.saveState()
    c.clipPath(_path(c, f, True, f.get("smooth", False)), stroke=0, fill=0)
    c.setLineCap(1)
    texture = {"wood": "#547444", "marsh": "#758676", "moor": "#A39270",
               "field": "#B08A5A", "lake": "#4F8985"}[kind]
    c.setStrokeColor(HexColor(texture))
    c.setFillColor(HexColor(texture))
    c.setLineWidth(0.38)
    if hasattr(c, "setStrokeAlpha"):
        c.setStrokeAlpha(0.42)
    if kind == "wood":
        for col, x in enumerate(range(int(x0) - 8, int(x1) + 9, 20)):
            for y in range(int(y0) - 8, int(y1) + 9, 18):
                yy = y + (col % 2) * 5
                for dx, scale in ((-3.5, .8), (2.5, 1.0)):
                    c.line(x + dx, yy - 3, x + dx, yy + 1.5)
                    p = c.beginPath(); p.moveTo(x + dx - 2.7*scale, yy)
                    p.lineTo(x + dx, yy + 5*scale); p.lineTo(x + dx + 2.7*scale, yy)
                    c.drawPath(p, stroke=1, fill=0)
    elif kind == "marsh":
        for col, x in enumerate(range(int(x0) - 8, int(x1) + 9, 18)):
            for y in range(int(y0) - 6, int(y1) + 7, 15):
                yy = y + (col % 2) * 4
                c.line(x, yy - 2, x, yy + 3)
                c.line(x, yy + 1, x - 2, yy + 3)
                c.line(x, yy + 1, x + 2, yy + 3)
                c.line(x - 3.5, yy - 3.5, x + 3.5, yy - 3.5)
    elif kind == "moor":
        for x in range(int(x0) - 8, int(x1) + 9, 16):
            for y in range(int(y0) - 8, int(y1) + 9, 15):
                c.line(x, y - 2, x, y + 2)
                c.line(x, y, x - 2, y + 2)
                c.line(x, y, x + 2, y + 2)
    elif kind == "field":
        for x in range(int(x0) - 12, int(x1) + 12, 10):
            c.line(x - 8, y0 - 3, x + 8, y1 + 3)
    # Lake deliberately stays a flat wash with its stronger shoreline.
    c.restoreState()


def _draw_line_feature(c, f, road_pass=None, gate_gaps=None):
    """Draw one line feature in the selected survey family."""
    k = f["kind"]
    s = LINE[k]
    smooth = f.get("smooth", s.get("smooth", False))
    w = f.get("w") or s["w"]
    c.setLineCap(1); c.setLineJoin(1); c.setDash()
    c.setStrokeColor(HexColor(s["color"]))
    if k == "road":
        # All road casings are drawn before all road fills. At forks and crossings this makes
        # separate road features merge into one continuous carriageway instead of stacking.
        if road_pass in (None, "casing"):
            c.setLineWidth(w + 1.1)
            c.drawPath(_path(c, f, False, smooth), stroke=1, fill=0)
        if road_pass in (None, "fill"):
            c.setStrokeColor(HexColor("#F6EFDC")); c.setLineWidth(max(.2, w - .6))
            c.drawPath(_path(c, f, False, smooth), stroke=1, fill=0)
    elif k == "river":
        c.setStrokeColor(HexColor("#BFD7D2")); c.setLineWidth(w + 2.2)
        c.drawPath(_path(c, f, False, smooth), stroke=1, fill=0)
        c.setStrokeColor(HexColor(s["color"])); c.setLineWidth(w)
        c.drawPath(_path(c, f, False, smooth), stroke=1, fill=0)
    elif k == "stream":
        c.setLineWidth(.8); c.drawPath(_path(c, f, False, smooth), stroke=1, fill=0)
    elif k == "path":
        c.setLineWidth(1.0); c.setDash(3.0, 2.4)
        c.drawPath(_path(c, f, False, smooth), stroke=1, fill=0); c.setDash()
    elif k == "ditch":
        c.setLineWidth(.8); c.drawPath(_path(c, f, False, smooth), stroke=1, fill=0)
        _ornament(c, f)
    elif k in ("hedge", "wall"):
        _ornament(c, f, gate_gaps)
    else:
        c.setLineWidth(w)
        c.setDash(*s["dash"]) if s.get("dash") else c.setDash()
        c.drawPath(_path(c, f, False, smooth), stroke=1, fill=0)
        c.setDash()


TRACKS = {"path", "road", "track"}
BARRIERS = {"hedge", "wall", "ditch"}
WATERS = {"river", "stream"}


def _seg_dir(p, f):
    """Direction of the nearest segment of f to point p, and how far away it is."""
    best = (float("inf"), 0.0)
    for a, b in zip(f["pts"], f["pts"][1:]):
        dx, dy = b[0] - a[0], b[1] - a[1]
        L2 = dx * dx + dy * dy
        t = 0 if L2 == 0 else max(0.0, min(1.0, ((p[0]-a[0])*dx + (p[1]-a[1])*dy) / L2))
        d = math.hypot(p[0] - (a[0] + t*dx), p[1] - (a[1] + t*dy))
        if d < best[0]:
            best = (d, math.atan2(dy, dx))
    return best


def crossing_angles(features):
    """A bridge or ford lies along the route it carries; a gate sits in the line of its wall.

    Drawn unrotated they all point the same way regardless of what they cross, which is what made
    them read as wrong at a glance. Angles are normalised to the nearer horizontal so text-sized
    symbols never print upside down.
    """
    tracks = [f for f in features if f["kind"] in TRACKS and len(f["pts"]) > 1]
    barriers = [f for f in features if f["kind"] in BARRIERS and len(f["pts"]) > 1]
    waters = [f for f in features if f["kind"] in WATERS and len(f["pts"]) > 1]
    out = {}
    for i, f in enumerate(features):
        k = f["kind"]
        if k not in ("bridge", "ford", "gate") or len(f["pts"]) != 1:
            continue
        p = f["pts"][0]
        pool = barriers if k == "gate" else tracks
        if not pool:
            pool = waters or tracks
        best = min((_seg_dir(p, g) for g in pool), default=(float("inf"), 0.0))
        a = best[1]
        while a > math.pi / 2:
            a -= math.pi
        while a < -math.pi / 2:
            a += math.pi
        out[i] = math.degrees(a)
    return out


def _point(c, f, angle=0.0):
    """Ported from drawPoint() in the designer; keep the two in step."""
    x, y = f["pts"][0]
    k = f["kind"]
    col = HexColor(POINT_COLOR.get(k, PURPLE))
    rotated = abs(angle) > 0.01
    if rotated:
        c.saveState()
        c.translate(x, y)
        c.rotate(angle)
        c.translate(-x, -y)
    c.setStrokeColor(col)
    c.setFillColor(col)
    c.setLineWidth(0.9)

    def line(x1, y1, x2, y2, w=0.8):
        c.setLineWidth(w)
        c.line(x1, y1, x2, y2)

    def poly(points, w=0.9, fill=0, close=True):
        c.setLineWidth(w)
        p = c.beginPath()
        p.moveTo(*points[0])
        for q in points[1:]:
            p.lineTo(*q)
        if close:
            p.close()
        c.drawPath(p, stroke=1, fill=fill)

    if k == "farm":
        poly([(x - 8, y - 4), (x - 8, y + 1), (x - 3, y + 5),
              (x + 2, y + 1), (x + 2, y - 4)])
        c.rect(x + 4, y - 4, 6, 7, fill=0, stroke=1)
        line(x + 7, y - 4, x + 7, y + 3, .4)
    elif k == "church":
        poly([(x - 6, y - 5), (x - 6, y + 1), (x, y + 6),
              (x + 6, y + 1), (x + 6, y - 5)])
        line(x, y + 6, x, y + 11, 1.0)
        line(x - 2, y + 9, x + 2, y + 9, 1.0)
    elif k == "ruin":
        poly([(x - 7, y - 5), (x - 7, y + 2), (x, y + 7),
              (x + 7, y + 2), (x + 7, y - 1)], close=False)
        line(x - 7, y - 5, x - 1, y - 5, 1.0)
    elif k == "mill":
        poly([(x - 8, y - 5), (x - 8, y + 2), (x - 3, y + 6),
              (x + 2, y + 2), (x + 2, y - 5)], .8)
        c.setLineWidth(.9); c.circle(x + 3, y - 1, 5, stroke=1, fill=0)
        for i in range(4):
            a = i * math.pi / 4
            line(x + 3 - math.cos(a) * 5, y - 1 - math.sin(a) * 5,
                 x + 3 + math.cos(a) * 5, y - 1 + math.sin(a) * 5, .55)
    elif k == "cairn":
        for w, yy in ((14, -5), (10, -1), (6, 3)):
            c.rect(x - w/2, y + yy, w, 3.5, fill=0, stroke=1)
    elif k == "stone":
        poly([(x - 4, y - 6), (x - 3, y + 5), (x, y + 8),
              (x + 4, y + 4), (x + 5, y - 6)], fill=1)
        line(x - 6, y - 6, x + 7, y - 6, 0.8)
    elif k == "bridge":
        # A short, gently bowed deck follows the road direction. Three light cross-planks make
        # it read as a bridge without the rigid end bars used by the earlier options.
        for yy, bow in ((-3.4, -1.0), (3.4, 1.0)):
            p = c.beginPath(); p.moveTo(x - 8, y + yy)
            p.curveTo(x - 3, y + yy + bow, x + 3, y + yy + bow, x + 8, y + yy)
            c.setLineWidth(1.15); c.drawPath(p, stroke=1, fill=0)
        for xx in (-4, 0, 4):
            line(x + xx, y - 3.5, x + xx, y + 3.5, .55)
    elif k == "ford":
        # Original/current convention: three bed stones between two bank ticks.
        line(x - 5.5, y + 3, x - 5.5, y - 3, .8)
        line(x + 5.5, y + 3, x + 5.5, y - 3, .8)
        for xx in (-3, 0, 3):
            c.circle(x + xx, y, 1.05, stroke=0, fill=1)
    elif k == "gate":
        line(x - 7, y - 6, x - 7, y + 6, 1.3)
        line(x + 7, y - 6, x + 7, y + 6, 1.3)
        # Option B: one visibly open gate.
        line(x - 7, y - 3, x + 2, y + 5, 1.0)
        line(x - 7, y + 1, x + 1, y + 5, .8)
    elif k == "village":
        for hx, hy in ((x - 6, y + 1), (x + 2, y + 2), (x - 1, y - 4)):
            poly([(hx - 3, hy - 3), (hx - 3, hy), (hx, hy + 3),
                  (hx + 3, hy), (hx + 3, hy - 3)], .7, fill=1)
    elif k == "port":
        # Existing column: anchor.
        c.circle(x, y + 5.4, 1.5, stroke=1, fill=0)
        line(x, y + 3.9, x, y - 5.4, 1.0)
        line(x - 3.6, y + 2.2, x + 3.6, y + 2.2, .8)
        p = c.beginPath(); p.moveTo(x - 4.6, y - 1.6)
        p.curveTo(x - 4.2, y - 5.6, x + 4.2, y - 5.6, x + 4.6, y - 1.6)
        c.drawPath(p, stroke=1, fill=0)
    elif k == "cave":
        poly([(x - 9, y - 5), (x - 6, y + 2), (x, y + 7),
              (x + 7, y + 2), (x + 9, y - 5)], .9)
        p = c.beginPath(); p.moveTo(x - 4, y - 5)
        p.curveTo(x - 4, y + 3, x + 4, y + 3, x + 4, y - 5); p.close()
        c.drawPath(p, stroke=0, fill=1)
    elif k == "well":
        c.circle(x, y, 5, stroke=1, fill=0)
        c.circle(x, y, 1.5, stroke=0, fill=1)
    elif k == "marker":
        c.circle(x, y, 4.5, stroke=0, fill=1)
    if rotated:
        c.restoreState()


def draw(c, features, clip_rect=None):
    """Draw the whole layer. Call BEFORE the stop pins and labels: the base map's own labels
    must win any overlap, the way they do on a real map."""
    c.saveState()
    if clip_rect:
        p = c.beginPath()
        p.rect(clip_rect[0], clip_rect[1],
               clip_rect[2] - clip_rect[0], clip_rect[3] - clip_rect[1])
        c.clipPath(p, stroke=0, fill=0)

    for f in features:                                   # areas first, under everything
        if f["kind"] in AREA and len(f["pts"]) > 2:
            s = AREA[f["kind"]]
            c.setFillColor(HexColor(s["fill"]))
            c.setStrokeColor(HexColor(s["color"]))
            c.setLineWidth(0.7)
            c.drawPath(_path(c, f, True, f.get("smooth", False)), stroke=1, fill=1)
            _area_texture(c, f)

    # Non-road linework first, so roads remain clear over rivers and other terrain lines. Wall
    # blocks stop at gate posts rather than continuing visibly through the opening.
    gate_gaps = [f["pts"][0] for f in features if f["kind"] == "gate" and len(f["pts"]) == 1]
    for f in features:
        k = f["kind"]
        if k not in LINE or k == "road" or len(f["pts"]) < 2:
            continue
        _draw_line_feature(c, f, gate_gaps=gate_gaps)

    # Draw every casing first, then every fill, so forks and crossings merge naturally.
    roads = [f for f in features if f["kind"] == "road" and len(f["pts"]) > 1]
    for f in roads:
        _draw_line_feature(c, f, "casing")
    for f in roads:
        _draw_line_feature(c, f, "fill")

    angles = crossing_angles(features)
    # Ordinary landmarks first; countable crossings always sit in the foreground.
    for i, f in enumerate(features):
        if len(f["pts"]) == 1 and f["kind"] not in ("bridge", "ford", "gate"):
            _point(c, f, angles.get(i, 0.0))
    for i, f in enumerate(features):
        if len(f["pts"]) == 1 and f["kind"] in ("bridge", "ford", "gate"):
            _point(c, f, angles.get(i, 0.0))

    c.restoreState()


LEGEND_ORDER = [
    ("road", "Paved road"), ("track", "Track"), ("path", "Footpath"),
    ("river", "River"), ("stream", "Stream"), ("ditch", "Ditch"),
    ("hedge", "Hedge"), ("wall", "Stone wall"), ("contour", "Contour"),
    ("bridge", "Bridge"), ("ford", "Ford"), ("gate", "Gate"),
    ("wood", "Wood"), ("marsh", "Marsh"), ("moor", "Moor"),
    ("field", "Field"), ("lake", "Lake"),
    ("village", "Village"), ("farm", "Farm"), ("church", "Chapel"),
    ("mill", "Mill"), ("well", "Well"), ("port", "Landing"),
    ("cairn", "Cairn"), ("stone", "Standing stone"), ("ruin", "Ruin"),
    ("cave", "Cave"), ("marker", "Marker"),
]


def draw_legend(c, features, box, ink="#283B34", rule="#A99A7B", paper="#F4EEDD"):
    """A key for the symbols actually on this sheet -- listing ones that are not drawn would be
    worse than no legend at all. Sized to the entries it really needs."""
    present = {f["kind"] for f in features}
    rows = [(k, n) for k, n in LEGEND_ORDER if k in present]
    if not rows:
        return
    x0, y0, x1, y1 = box
    c.saveState()
    c.setFillColor(HexColor(paper))
    c.setStrokeColor(HexColor(rule))
    c.setLineWidth(0.7)
    c.rect(x0, y0, x1 - x0, y1 - y0, fill=1, stroke=1)

    c.setFillColor(HexColor(ink))
    c.setFont("Helvetica-Bold", 6.4)
    c.drawCentredString((x0 + x1) / 2, y1 - 11, "LEGEND")
    c.setStrokeColor(HexColor(rule))
    c.setLineWidth(0.5)
    c.line(x0 + 8, y1 - 15, x1 - 8, y1 - 15)

    cols = 2
    per = (len(rows) + cols - 1) // cols
    col_w = (x1 - x0 - 12) / cols
    top = y1 - 22
    row_h = min(12.5, (top - y0 - 8) / per)
    for i, (kind, name) in enumerate(rows):
        col, row = divmod(i, per)
        cx = x0 + 6 + col * col_w
        cy = top - row * row_h - row_h / 2
        sw = cx + 9                                   # swatch centre
        if kind in LINE:
            _draw_line_feature(c, {"kind": kind, "smooth": False,
                                   "pts": [[cx, cy], [cx + 18, cy]]})
        elif kind in AREA:
            s = AREA[kind]
            c.setFillColor(HexColor(s["fill"]))
            c.setStrokeColor(HexColor(s["color"]))
            c.setLineWidth(0.6)
            c.rect(cx, cy - 4, 18, 8, fill=1, stroke=1)
            _area_texture(c, {"kind": kind, "smooth": False,
                              "pts": [[cx, cy - 4], [cx + 18, cy - 4],
                                      [cx + 18, cy + 4], [cx, cy + 4]]})
        else:
            c.saveState()
            c.translate(sw, cy)
            c.scale(0.62, 0.62)                       # a full-size symbol overruns the row
            c.translate(-sw, -cy)
            _point(c, {"kind": kind, "pts": [[sw, cy]], "label": ""})
            c.restoreState()
        c.setFillColor(HexColor(ink))
        c.setFont("Helvetica", 5.0)
        c.drawString(cx + 22, cy - 1.8, name)
    c.restoreState()
