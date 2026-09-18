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
    "marsh": dict(color="#2F7775", fill="#D5E2DC"),
    "lake":  dict(color="#2F7775", fill="#DCE7E4"),
    "field": dict(color="#B08A5A", fill="#F0E7CE"),
    "moor":  dict(color="#8A7A5E", fill="#E8DFC6"),
}
POINT_COLOR = {"marker": "#B56A2A", "ford": "#2F7775", "text": "#283B34"}
PURPLE = "#6D528B"


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


def _ornament(c, f):
    """Hedge blobs, wall and ditch ticks -- the detail an isolated icon could not carry."""
    kind = f["kind"]
    s = LINE[kind]
    step = 4.2 if kind == "hedge" else 5.0 if kind == "wall" else 7.0
    c.setFillColor(HexColor(s["color"]))
    c.setStrokeColor(HexColor(s["color"]))
    c.setLineWidth(0.55)
    for x, y, ang in _sample(f, False, f.get("smooth", s.get("smooth", False)), step):
        if kind == "hedge":
            c.circle(x, y, 1.5, stroke=0, fill=1)
        else:
            a = ang + math.pi / 2
            r = 1.6 if kind == "wall" else 2.0
            c.line(x - math.cos(a) * r, y - math.sin(a) * r,
                   x + math.cos(a) * r, y + math.sin(a) * r)


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

    if k in ("farm", "church", "ruin"):
        pts = [(x - 5, y - 4), (x - 5, y + 1), (x, y + 5), (x + 5, y + 1), (x + 5, y - 4)]
        poly(pts, close=(k != "ruin"))
        if k == "church":
            line(x, y + 5, x, y + 9, 0.9)
            line(x - 2, y + 7.5, x + 2, y + 7.5, 0.9)
        if k == "ruin":
            line(x - 5, y - 4, x + 1, y - 4, 0.9)
    elif k == "mill":
        poly([(x - 6, y - 4), (x - 6, y + 2), (x - 1, y + 6), (x + 1, y + 2), (x + 1, y - 4)])
        c.setLineWidth(0.8)
        c.circle(x + 4.5, y - 1, 4, stroke=1, fill=0)
        for i in range(4):
            a = i * math.pi / 4
            line(x + 4.5 - math.cos(a) * 4, y - 1 - math.sin(a) * 4,
                 x + 4.5 + math.cos(a) * 4, y - 1 + math.sin(a) * 4, 0.6)
    elif k == "cairn":
        poly([(x - 5, y - 4), (x, y + 6), (x + 5, y - 4)])
        line(x - 3, y - 0.5, x + 3, y - 0.5, 0.6)
        line(x - 4.2, y - 2.4, x + 4.2, y - 2.4, 0.6)
    elif k == "stone":
        poly([(x - 2.6, y - 5), (x - 2, y + 3), (x, y + 6), (x + 2, y + 2.5), (x + 2.6, y - 5)])
        line(x - 4, y - 5, x + 4, y - 5, 0.6)
    elif k == "bridge":
        c.setLineWidth(1.1)
        p = c.beginPath()
        p.moveTo(x - 6, y - 2)
        p.curveTo(x - 2, y + 3.3, x + 2, y + 3.3, x + 6, y - 2)
        c.drawPath(p, stroke=1, fill=0)
        line(x - 6, y - 4, x - 6, y - 1)
        line(x + 6, y - 4, x + 6, y - 1)
    elif k == "ford":
        line(x - 5.5, y + 3, x - 5.5, y - 3)
        line(x + 5.5, y + 3, x + 5.5, y - 3)
        for i in (-1, 0, 1):
            c.circle(x + i * 3, y, 1.05, stroke=0, fill=1)
    elif k == "gate":
        line(x - 4.5, y + 4, x - 4.5, y - 4, 0.9)
        line(x + 4.5, y + 4, x + 4.5, y - 4, 0.9)
        line(x - 4.5, y + 1.6, x + 4.5, y + 1.6, 0.7)
        line(x - 4.5, y - 1.6, x + 4.5, y - 1.6, 0.7)
    elif k == "village":
        for hx, hy, w in ((x - 4.2, y + 1.2, 3), (x + 3.4, y + 2.2, 2.6), (x - 0.4, y - 4.2, 3)):
            poly([(hx - w, hy - w), (hx - w, hy), (hx, hy + w * 0.9), (hx + w, hy), (hx + w, hy - w)], 0.8)
    elif k == "port":
        c.setLineWidth(0.8)
        c.circle(x, y + 5.4, 1.5, stroke=1, fill=0)
        line(x, y + 3.9, x, y - 5.4, 1.0)
        line(x - 3.6, y + 2.2, x + 3.6, y + 2.2, 0.8)
        c.setLineWidth(1.0)
        p = c.beginPath()
        p.moveTo(x - 4.6, y - 1.6)
        p.curveTo(x - 4.2, y - 5.6, x + 4.2, y - 5.6, x + 4.6, y - 1.6)
        c.drawPath(p, stroke=1, fill=0)
    elif k == "cave":
        c.setLineWidth(0.9)
        p = c.beginPath()
        p.moveTo(x - 5, y - 4)
        p.lineTo(x - 5, y - 1)
        p.curveTo(x - 5, y + 5.6, x + 5, y + 5.6, x + 5, y - 1)
        p.lineTo(x + 5, y - 4)
        p.close()
        c.drawPath(p, stroke=1, fill=1)
        line(x - 7.5, y - 4, x + 7.5, y - 4, 0.9)
    elif k == "well":
        c.setLineWidth(0.9)
        c.circle(x, y, 3.4, stroke=1, fill=0)
        c.circle(x, y, 1.2, stroke=0, fill=1)
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

    # Non-road linework first, so roads sit over it and a bridge reads as carrying the road
    # across the water.
    for f in features:
        k = f["kind"]
        if k not in LINE or k == "road" or len(f["pts"]) < 2:
            continue
        s = LINE[k]
        smooth = f.get("smooth", s.get("smooth", False))
        w = f.get("w") or s["w"]
        c.setStrokeColor(HexColor(s["color"]))
        c.setLineWidth(w)
        c.setLineCap(1)
        c.setLineJoin(1)
        c.setDash(*s["dash"]) if s.get("dash") else c.setDash()
        c.drawPath(_path(c, f, False, smooth), stroke=1, fill=0)
        c.setDash()
        if k in ("hedge", "wall", "ditch"):
            _ornament(c, f)

    # Roads in TWO passes: every casing, then every fill. Drawing each road casing-then-fill on
    # its own makes the next road's dark casing slice across the previous one's pale carriageway,
    # so converging roads print as a braid of parallel dark lines instead of merging into one
    # junction. Casing-pass-then-fill-pass is what makes a road network read as a network.
    roads = [f for f in features if f["kind"] == "road" and len(f["pts"]) > 1]
    rs = LINE["road"]
    c.setLineCap(1)
    c.setLineJoin(1)
    c.setDash()
    c.setStrokeColor(HexColor(rs["color"]))
    for f in roads:
        c.setLineWidth((f.get("w") or rs["w"]) + 1.1)
        c.drawPath(_path(c, f, False, f.get("smooth", True)), stroke=1, fill=0)
    c.setStrokeColor(HexColor("#F6EFDC"))
    for f in roads:
        c.setLineWidth(max(0.2, (f.get("w") or rs["w"]) - 0.6))
        c.drawPath(_path(c, f, False, f.get("smooth", True)), stroke=1, fill=0)

    angles = crossing_angles(features)
    for i, f in enumerate(features):                     # point symbols on top of the linework
        if len(f["pts"]) == 1:
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
            s = LINE[kind]
            if kind == "road":
                c.setStrokeColor(HexColor(s["color"]))
                c.setLineWidth(s["w"] + 1.1)
                c.setDash()
                c.line(cx, cy, cx + 18, cy)
                c.setStrokeColor(HexColor("#F6EFDC"))
                c.setLineWidth(s["w"] - 0.6)
                c.line(cx, cy, cx + 18, cy)
            else:
                c.setStrokeColor(HexColor(s["color"]))
                c.setLineWidth(s["w"])
                c.setDash(*s["dash"]) if s.get("dash") else c.setDash()
                c.line(cx, cy, cx + 18, cy)
                c.setDash()
                if kind in ("hedge", "wall", "ditch"):
                    _ornament(c, {"kind": kind, "smooth": False,
                                  "pts": [[cx, cy], [cx + 18, cy]]})
        elif kind in AREA:
            s = AREA[kind]
            c.setFillColor(HexColor(s["fill"]))
            c.setStrokeColor(HexColor(s["color"]))
            c.setLineWidth(0.6)
            c.rect(cx, cy - 4, 18, 8, fill=1, stroke=1)
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
