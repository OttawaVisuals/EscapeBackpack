"""Where can decorative art go on a trail map without breaking it?

The trail maps have two hard constraints that decoration must respect:

  1. Players draw the trail legs on the sheet with a wet-erase marker. Anything printed under
     that line competes with it, and the drawn line is the answer.
  2. Players locate stops by reading place names. Anything printed over a label hides a clue.

This script renders a placement guide for Codex: sea areas that are clear of the route corridor,
clear of every label box, and clear of the title band, compass and scale bar. It then finds clear
rectangles and prints their size in inches so vignettes can be drawn to fit.

Slots are chosen LANDSCAPE, not largest-area. Maximising area produced tall narrow columns (one
was 1.62 x 4.25 in), which is the worst possible frame for a ship under sail -- the main subject.
Aspect is constrained to roughly 1.4:1 - 2.0:1 instead, which costs some area and buys usable art.

Output: output/pdf/Trail_Map_<n>_<Trail>_ART_GUIDE.pdf  (designer aid, never printed for play)

Usage: python build_art_placement_guide.py [leif|rollo|aud]
"""

import sys
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from shapely.geometry import Point, Polygon
from shapely.ops import unary_union
from shapely.prepared import prep

import build_trail_maps_pdf as M

CELL = 9.0          # sampling grid, PDF points
ROUTE_CLEAR = 26.0  # keep-clear halo around the drawn route, points
LABEL_CLEAR = 3.0

SAFE = HexColor("#5B8C5A")
DANGER = HexColor("#A4472F")


ASPECTS = (1.4, 1.7, 2.0)   # landscape only: a ship under sail does not fit a portrait column
MIN_W_IN = 1.10


def landscape_rects(grid, cols, rows, n=5):
    """Clear rectangles constrained to a landscape aspect, biggest first, non-overlapping.

    A prefix sum makes the "is this whole rectangle safe?" test O(1), so every candidate size can
    be slid across the whole grid cheaply."""
    ps = [[0] * (cols + 1) for _ in range(rows + 1)]
    for r in range(rows):
        for ccol in range(cols):
            ps[r + 1][ccol + 1] = (ps[r][ccol + 1] + ps[r + 1][ccol] - ps[r][ccol]
                                   + (1 if grid[r][ccol] else 0))

    def clear(x0, y0, w, h):
        return (ps[y0 + h][x0 + w] - ps[y0][x0 + w]
                - ps[y0 + h][x0] + ps[y0][x0]) == w * h

    sizes = set()
    for w in range(int(MIN_W_IN * 72 / CELL), cols + 1):
        for a in ASPECTS:
            h = max(1, round(w / a))
            if h <= rows:
                sizes.add((w, h))
    cands = []
    for w, h in sizes:
        for y0 in range(rows - h + 1):
            for x0 in range(cols - w + 1):
                if clear(x0, y0, w, h):
                    cands.append((w * h, x0, y0, w, h))
    cands.sort(reverse=True)
    out = []
    for _, x0, y0, w, h in cands:
        if any(not (x0 + w <= ox or ox + ow <= x0 or y0 + h <= oy or oy + oh <= y0)
               for ox, oy, ow, oh in out):
            continue
        out.append((x0, y0, w, h))
        if len(out) >= n:
            break
    return out


def run(key):
    cfg = M.TRAILS[key]
    plan = M.load_plan()
    corpus = M.load_corpus()
    stops = sorted(plan["visits"][key], key=lambda s: s["order"])

    # Rebuild the exact geometry the real map uses, by calling the builder's own internals.
    geom = M.build(key, cfg, plan, corpus, answer=False, _return_geometry=True)
    pt, rings, lab, lo0, lo1, la0, la1 = geom

    land = unary_union([Polygon(r) for r in rings if len(r) >= 4]).buffer(0)
    land_p = prep(land)

    route = [pt(s["lng"], s["lat"]) for s in stops]

    def near_route(x, y):
        for i in range(len(route) - 1):
            ax, ay = route[i]
            bx, by = route[i + 1]
            dx, dy = bx - ax, by - ay
            L2 = dx * dx + dy * dy or 1.0
            t = max(0.0, min(1.0, ((x - ax) * dx + (y - ay) * dy) / L2))
            px, py = ax + t * dx, ay + t * dy
            if (x - px) ** 2 + (y - py) ** 2 < ROUTE_CLEAR ** 2:
                return True
        return False

    boxes = [(b[0] - LABEL_CLEAR, b[1] - LABEL_CLEAR, b[2] + LABEL_CLEAR, b[3] + LABEL_CLEAR)
             for b in lab.boxes]

    cols = int((M.MX1 - M.MX0) // CELL)
    rows = int((M.MY1 - M.MY0) // CELL)
    grid = [[False] * cols for _ in range(rows)]
    # invert the page->lonlat mapping by bisection on each axis (the projection is monotonic
    # in each direction across a frame this size)
    def page_to_lonlat(x, y):
        lo, hi = lo0 - 5, lo1 + 5
        for _ in range(40):
            mid = (lo + hi) / 2
            if pt(mid, (la0 + la1) / 2)[0] < x:
                lo = mid
            else:
                hi = mid
        lon = (lo + hi) / 2
        lo, hi = la0 - 5, la1 + 5
        for _ in range(40):
            mid = (lo + hi) / 2
            if pt(lon, mid)[1] < y:
                lo = mid
            else:
                hi = mid
        return lon, (lo + hi) / 2

    for r in range(rows):
        for ccol in range(cols):
            x = M.MX0 + ccol * CELL + CELL / 2
            y = M.MY0 + r * CELL + CELL / 2
            if near_route(x, y):
                continue
            if any(bx0 <= x <= bx1 and by0 <= y <= by1 for bx0, by0, bx1, by1 in boxes):
                continue
            lon, lat = page_to_lonlat(x, y)
            if land_p.contains(Point(lon, lat)):
                continue          # sea only: ships belong on water, and land carries the labels
            grid[r][ccol] = True

    rects = landscape_rects(grid, cols, rows)

    out = M.OUT_DIR / ("Trail_Map_%d_%s_ART_GUIDE.pdf" % (cfg["n"], key.capitalize()))
    c = canvas.Canvas(str(out), pagesize=letter)
    c.setTitle("Art placement guide - %s" % key.capitalize())
    c.setFillColor(HexColor("#FBF7EE"))
    c.rect(0, 0, M.PAGE_W, M.PAGE_H, stroke=0, fill=1)

    c.saveState()
    c.setFillAlpha(0.30)
    c.setFillColor(SAFE)
    for r in range(rows):
        for ccol in range(cols):
            if grid[r][ccol]:
                c.rect(M.MX0 + ccol * CELL, M.MY0 + r * CELL, CELL, CELL, stroke=0, fill=1)
    c.restoreState()

    c.setStrokeColor(DANGER)
    c.setLineWidth(ROUTE_CLEAR * 2)
    c.setLineCap(1)
    c.setLineJoin(1)
    c.saveState()
    c.setStrokeAlpha(0.13)
    p = c.beginPath()
    p.moveTo(*route[0])
    for q in route[1:]:
        p.lineTo(*q)
    c.drawPath(p, stroke=1, fill=0)
    c.restoreState()
    c.setLineWidth(1.6)
    p = c.beginPath()
    p.moveTo(*route[0])
    for q in route[1:]:
        p.lineTo(*q)
    c.drawPath(p, stroke=1, fill=0)

    c.setStrokeColor(HexColor("#283B34"))
    c.setLineWidth(1.4)
    c.setFont("CinzelBold", 9)
    print("%s: %d clear slots" % (key, len(rects)))
    for i, (x0, y0, w, h) in enumerate(rects):
        px, py = M.MX0 + x0 * CELL, M.MY0 + y0 * CELL
        pw, ph = w * CELL, h * CELL
        c.rect(px, py, pw, ph, stroke=1, fill=0)
        c.setFillColor(HexColor("#283B34"))
        c.drawString(px + 4, py + ph - 11, chr(65 + i))
        c.setFont("Helvetica", 7)
        c.drawString(px + 4, py + 4, "%.2f x %.2f in" % (pw / 72, ph / 72))
        c.setFont("CinzelBold", 9)
        print("   slot %s: %.2f x %.2f in at (%.2f, %.2f) from sheet bottom-left"
              % (chr(65 + i), pw / 72, ph / 72, px / 72, py / 72))

    c.setFillColor(HexColor("#283B34"))
    c.setFont("Helvetica-Bold", 11)
    c.drawString(M.NEAT[0] + 14, M.NEAT[1] + 34, "ART PLACEMENT GUIDE - %s" % cfg["title"])
    c.setFont("Helvetica", 7.6)
    c.drawString(M.NEAT[0] + 14, M.NEAT[1] + 22,
                 "Green = sea clear of the drawn route, every label, and the title band. "
                 "Red = keep clear (route corridor).")
    c.drawString(M.NEAT[0] + 14, M.NEAT[1] + 12,
                 "Lettered boxes are the largest clear LANDSCAPE rectangles. Designer aid - not printed for play.")
    c.showPage()
    c.save()
    print("   -> %s" % out.name)


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    for k in (sys.argv[1:] or ["leif"]):
        run(k)
