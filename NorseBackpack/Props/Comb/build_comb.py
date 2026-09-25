"""Aud's comb -- the grille that reads BOOK off decoy card AD (PR-19, PZ-17, 25 Sept 2026).

How it plays. The comb lies upright on the back of AD, handle in the left margin, teeth pointing
right. Its two end ring-and-dots are drilled through; players sit the two printed ring-and-dots
(build_postcard_AD_pdf.COMB_MARKS) in those holes. There is one tooth per line of Liv's message,
at the message's own line spacing. Intact teeth cover their whole line. Four teeth are broken
short, each ending just before a chosen letter, so the only text left showing is

    line 1  [At her ]brother's harbor -- the one Aud
    line 3  [I've read everything I c]ould find about
    line 8  [al]ongside the coins, and the museum let
    line 9  [me ]keep it!

and the first visible letters, top to bottom, read B O O K.

Nothing here is typed in by hand: line positions and the target letters' left edges are read
from the built AD print PDF, so re-run this after any change to AD's back.

Handle carving follows AD's own stamp (Stamp_Aud_Comb_v1.png): flared ends with a ring-and-dot
each, a knotwork band along the middle, a small dot either side of it and a border line. If
knotwork.svg (black shapes on white, the band laid out horizontally) sits next to this script it
is cut into the handle; otherwise a two-strand twist is used as a placeholder. The Codex prompt
for knotwork.svg is recorded in Norse_Brainstorm.html under the comb prop.

Outputs, next to this script:
  Aud_Comb.scad / Aud_Comb.stl   -- flat bottom, printed face up, no supports
  Aud_Comb_on_AD.png             -- the comb outline drawn over the real AD back at 300 dpi
  comb_geometry.json             -- every number used, for the page and for print checks

Requires pymupdf, shapely, Pillow; OpenSCAD for the STL (on PATH or the default install dir).
"""
import json
import math
import shutil
import subprocess
import sys
from pathlib import Path

import pymupdf
from PIL import Image, ImageDraw
from shapely import affinity
from shapely.geometry import LineString, Point, Polygon, box
from shapely.ops import unary_union

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "NorseBackpack" / "Postcards"))
import build_postcard_AD_pdf as AD  # noqa: E402

AD_PDF = ROOT / "output" / "pdf" / "Postcard_AD_Bjarnarhofn_Print.pdf"
KNOTWORK_SVG = HERE / "knotwork.svg"
PT = 25.4 / 72                    # mm per point

# (line number, word, index of the target letter in that word)
TARGETS = [(1, "brother", 0), (3, "could", 1), (8, "alongside", 2), (9, "keep", 0)]
ANSWER = "BOOK"

# Geometry, in card points (x right, y down from the card's top-left) unless marked mm.
TOOTH_ROOT_X = 18.5               # message text starts at x = 20
HANDLE_OUTER_X = -15.5            # handle overhangs the card's left edge by ~5.5 mm
INTACT_TIP_X = 168.0              # longest line ends at ~165.7; divider at 184
TOOTH_HALF = 3.1                  # 2.19 mm teeth; ~0.85 mm gaps at 8.6 pt leading
INK_SHIFT = -0.6                  # handwriting ink sits a little above the glyph-box centre
TIP_CLEAR = 0.4                   # broken tip stops this far short of the letter
LOBE_R = 8.0                      # flared end around each alignment hole
ROUND_OUT_MM = 2.5                # radius on the handle's outer corners (25 Sept 2026)
ROUND_IN_MM = 0.3                 # fillet where the flared ends meet the handle bar; larger reaches tooth 1
HOLE_R_MM = 1.0                   # 2 mm through-hole; the printed dot is 1 mm
TEETH_MM, HANDLE_MM, CARVE_MM = 1.6, 3.0, 0.6
GROOVE_MM = 0.6                   # minimum carved line width for a 0.4 mm nozzle
BONE = (226, 214, 188, 255)       # preview colour only


def read_layout():
    page = pymupdf.open(AD_PDF)[1]
    lines = []
    for block in page.get_text("rawdict")["blocks"]:
        for line in block.get("lines", []):
            x0, y0, x1, y1 = line["bbox"]
            if x0 < 30 and 25 < y0 < 125:
                chars = [ch for span in line["spans"] for ch in span["chars"]]
                lines.append(((y0 + y1) / 2, chars))
    lines.sort(key=lambda item: item[0])
    if len(lines) != 11:
        raise SystemExit("expected 11 message lines on AD, found %d" % len(lines))
    tips = {}
    for number, word, index in TARGETS:
        chars = lines[number - 1][1]
        text = "".join(ch["c"] for ch in chars)
        at = text.find(word)
        if at < 0:
            raise SystemExit("line %d no longer contains %r: %r" % (number, word, text))
        ch = chars[at + index]
        if ch["c"].upper() != ANSWER[len(tips)]:
            raise SystemExit("line %d letter is %r, expected %r" % (number, ch["c"], ANSWER[len(tips)]))
        tips[number] = ch["bbox"][0] - TIP_CLEAR
    return [y for y, _ in lines], tips


def jagged_end(x, y0, y1):
    """A snapped-off tooth end: three small teeth of break instead of a clean cut."""
    h = y1 - y0
    return [(x, y1), (x - 1.0, y1 - h * 0.3), (x - 0.2, y1 - h * 0.55),
            (x - 1.1, y1 - h * 0.8), (x - 0.3, y0)]


def tooth(yc, tip, broken):
    y0, y1 = yc - TOOTH_HALF, yc + TOOTH_HALF
    if broken:
        return Polygon([(TOOTH_ROOT_X, y0), (TOOTH_ROOT_X, y1)] + jagged_end(tip, y0, y1))
    return Polygon([(TOOTH_ROOT_X, y0), (TOOTH_ROOT_X, y1), (tip - 4, y1), (tip, yc + 0.8),
                    (tip, yc - 0.8), (tip - 4, y0)])


def build_geometry():
    line_ys, tips = read_layout()
    (mx0, my0), (mx1, my1) = AD.COMB_MARKS
    handle = unary_union([
        box(HANDLE_OUTER_X, my0 - LOBE_R + 0.5, TOOTH_ROOT_X, my1 + LOBE_R - 0.5),
        Point(mx0, my0).buffer(LOBE_R, 64),
        Point(mx1, my1).buffer(LOBE_R, 64),
    ])
    r_out, r_in = ROUND_OUT_MM / PT, ROUND_IN_MM / PT
    handle = handle.buffer(-r_out, 64).buffer(r_out, 64)   # round every outer corner
    handle = handle.buffer(r_in, 64).buffer(-r_in, 64)     # fillet the inside corners
    teeth = []
    for number, y in enumerate(line_ys, 1):
        yc = y + INK_SHIFT
        broken = number in tips
        teeth.append(tooth(yc, tips.get(number, INTACT_TIP_X), broken))
    holes = [Point(mx0, my0).buffer(HOLE_R_MM / PT, 48), Point(mx1, my1).buffer(HOLE_R_MM / PT, 48)]
    gaps = [line_ys[i + 1] - line_ys[i] - 2 * TOOTH_HALF for i in range(len(line_ys) - 1)]
    # clearance from each tooth to the parts of the handle that reach past the tooth root line
    # (the flared ends and their fillets), measured on the real shapes
    reach = handle.intersection(box(TOOTH_ROOT_X + 0.01, -999, 999, 999))
    lobe_gap = min(t.distance(reach) for t in teeth)
    if min(gaps) * PT < 0.75 or lobe_gap * PT < 0.75:
        raise SystemExit("a gap between teeth is under 0.75 mm -- too tight to print cleanly")
    return line_ys, tips, handle, teeth, holes, gaps, lobe_gap


def carvings(handle, holes):
    """Grooves cut 0.6 mm into the handle's top face, after the stamp's handle."""
    g = GROOVE_MM / PT
    (mx0, my0), (mx1, my1) = AD.COMB_MARKS
    cuts = []
    for mx, my in AD.COMB_MARKS:                           # ring of each ring-and-dot
        r = HOLE_R_MM / PT + 2.2
        cuts.append(Point(mx, my).buffer(r + g, 48).difference(Point(mx, my).buffer(r, 48)))
    # Border line inside the straight part of the handle, stopping short of the two end rings.
    bar = box(HANDLE_OUTER_X, my0, TOOTH_ROOT_X, my1).buffer(-1.4 / PT, join_style=2)
    corner = (ROUND_OUT_MM - 1.4) / PT                       # follow the rounded outline
    bar = bar.buffer(-corner, 64).buffer(corner, 64)
    frame = bar.difference(bar.buffer(-g, 64))
    keep_clear = unary_union([Point(mx, my).buffer(HOLE_R_MM / PT + 2.2 + g + 2.5, 48)
                              for mx, my in AD.COMB_MARKS])
    cuts.append(frame.difference(keep_clear))
    band_x0, band_x1 = HANDLE_OUTER_X + 3.6 / PT, TOOTH_ROOT_X - 3.6 / PT
    band_y0, band_y1 = my0 + LOBE_R + 8, my1 - LOBE_R - 8
    if KNOTWORK_SVG.exists():
        knot = ("band_svg", (band_x0, band_y0, band_x1, band_y1))
    else:
        cx, amp = (band_x0 + band_x1) / 2, (band_x1 - band_x0) / 2 - g
        period = 34.0
        for phase in (0, math.pi):
            pts = [(cx + amp * math.sin(2 * math.pi * (y - band_y0) / period + phase), y)
                   for y in [band_y0 + i * 0.5 for i in range(int((band_y1 - band_y0) / 0.5) + 1)]]
            cuts.append(LineString(pts).buffer(g / 2, 16))
        knot = ("placeholder_twist", (band_x0, band_y0, band_x1, band_y1))
    for y in (band_y0 - 4.5, band_y1 + 4.5):              # the stamp's two small dots
        cuts.append(Point((band_x0 + band_x1) / 2, y).buffer(1.6, 24))
    return unary_union(cuts).intersection(handle.buffer(-0.8 / PT)), knot


def to_mm(geom):
    """Card points (y down) -> mm with y up, the way OpenSCAD and the slicer see it."""
    return affinity.scale(geom, PT, -PT, origin=(0, 0))


def scad_polys(geom):
    geom = to_mm(geom)
    parts = getattr(geom, "geoms", [geom])
    out = []
    for p in parts:
        if p.is_empty or p.area < 1e-4:
            continue
        rings = [list(p.exterior.coords)[:-1]] + [list(r.coords)[:-1] for r in p.interiors]
        pts, paths, n = [], [], 0
        for ring in rings:
            pts += ring
            paths.append(list(range(n, n + len(ring))))
            n += len(ring)
        out.append("polygon(points=%s, paths=%s);" % (
            json.dumps([[round(x, 4), round(y, 4)] for x, y in pts]), json.dumps(paths)))
    return "\n    ".join(out)


def write_scad(handle, teeth, holes, cuts, knot):
    outline = unary_union([handle] + teeth).difference(unary_union(holes))
    handle_solid = handle.difference(unary_union(holes))
    knot_block = ""
    if knot[0] == "band_svg":
        bx0, by0, bx1, by1 = (v * PT for v in knot[1])
        knot_block = (
            "    // knotwork.svg: band drawn horizontally, rotated to run along the handle\n"
            "    translate([%.3f, %.3f, %.3f]) linear_extrude(%.3f)\n"
            "        resize([%.3f, %.3f]) rotate(90) import(\"knotwork.svg\", center=true);\n"
            % ((bx0 + bx1) / 2, -(by0 + by1) / 2, HANDLE_MM - CARVE_MM, CARVE_MM + 1,
               bx1 - bx0, by1 - by0))
    scad = """// Aud's comb (PR-19). Generated by build_comb.py -- edit that, not this.
$fn = 48;
difference() {
  union() {
    linear_extrude(%(teeth).3f) {
    %(outline)s
    }
    linear_extrude(%(handle).3f) {
    %(handle_poly)s
    }
  }
  translate([0, 0, %(carve_z).3f]) linear_extrude(%(carve_h).3f) {
    %(cuts)s
  }
%(knot)s}
""" % dict(teeth=TEETH_MM, handle=HANDLE_MM, outline=scad_polys(outline),
           handle_poly=scad_polys(handle_solid), carve_z=HANDLE_MM - CARVE_MM,
           carve_h=CARVE_MM + 1, cuts=scad_polys(cuts), knot=knot_block)
    (HERE / "Aud_Comb.scad").write_text(scad, encoding="utf-8")
    return outline


def export_stl():
    exe = shutil.which("openscad") or r"C:\Program Files\OpenSCAD\openscad.com"
    if not Path(exe).exists() and not shutil.which("openscad"):
        print("OpenSCAD not found -- wrote Aud_Comb.scad only")
        return False
    subprocess.run([exe, "-o", str(HERE / "Aud_Comb.stl"), str(HERE / "Aud_Comb.scad")],
                   check=True, capture_output=True)
    return True


def overlay_png(handle, teeth, holes, cuts):
    k = 300 / 72
    page = pymupdf.open(AD_PDF)[1]
    img = page.get_pixmap(dpi=300).pil_image().convert("RGBA")
    pad = int(20 * k)                                     # room for the off-card overhang
    canvas = Image.new("RGBA", (img.width + pad, img.height), (255, 255, 255, 255))
    canvas.paste(img, (pad, 0))
    over = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    g = ImageDraw.Draw(over)

    def draw(geom, fill, outline):
        # largest first, so a shape sitting inside another's hole is painted on top of it
        for p in sorted(getattr(geom, "geoms", [geom]), key=lambda q: -q.area):
            pts = [(x * k + pad, y * k) for x, y in p.exterior.coords]
            g.polygon(pts, fill=fill, outline=outline)
            for r in p.interiors:                         # a ring's middle is handle surface
                g.polygon([(x * k + pad, y * k) for x, y in r.coords], fill=BONE, outline=outline)
    body = unary_union([handle] + teeth).difference(unary_union(holes))
    draw(body, BONE, (110, 90, 60, 255))
    draw(cuts, (150, 128, 95, 255), None)
    out = Image.alpha_composite(canvas, over)
    # punch the holes back through so the printed dots show, as they would on the table
    base = canvas.copy()
    mask = Image.new("L", canvas.size, 0)
    mg = ImageDraw.Draw(mask)
    for h in holes:
        mg.polygon([(x * k + pad, y * k) for x, y in h.exterior.coords], fill=255)
    out.paste(base, (0, 0), mask)
    out.convert("RGB").crop((0, 0, pad + int(200 * k), int(175 * k))).save(HERE / "Aud_Comb_on_AD.png")


def main():
    line_ys, tips, handle, teeth, holes, gaps, lobe_gap = build_geometry()
    cuts, knot = carvings(handle, holes)
    outline = write_scad(handle, teeth, holes, cuts, knot)
    stl = export_stl()
    overlay_png(handle, teeth, holes, cuts)
    minx, miny, maxx, maxy = to_mm(outline).bounds
    info = {
        "answer": ANSWER,
        "targets": [{"line": n, "word": w, "tip_x_mm": round(tips[n] * PT, 2),
                     "broken_length_mm": round((tips[n] - TOOTH_ROOT_X) * PT, 2)} for n, w, _ in TARGETS],
        "intact_length_mm": round((INTACT_TIP_X - TOOTH_ROOT_X) * PT, 2),
        "tooth_width_mm": round(2 * TOOTH_HALF * PT, 2),
        "min_tooth_gap_mm": round(min(gaps) * PT, 2),
        "lobe_to_tooth_gap_mm": round(lobe_gap * PT, 2),
        "alignment_holes_mm_apart": round((AD.COMB_MARKS[1][1] - AD.COMB_MARKS[0][1]) * PT, 1),
        "overall_mm": [round(maxx - minx, 1), round(maxy - miny, 1)],
        "thickness_mm": {"teeth": TEETH_MM, "handle": HANDLE_MM, "carving_depth": CARVE_MM},
        "handle_carving": knot[0],
        "stl_written": stl,
    }
    (HERE / "comb_geometry.json").write_text(json.dumps(info, indent=2), encoding="utf-8")
    print(json.dumps(info, indent=2))


if __name__ == "__main__":
    main()
