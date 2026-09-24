"""Turn the coin relief SVGs into printable STLs for a Prusa i3 MK3S+ (0.4mm nozzle, FDM).

Two problems an FDM nozzle has that a vector trace does not:
1. Any stroke thinner than roughly one nozzle-width will blob together or vanish.
   `01_dirham_common.svg`/`02_dirham_rare.svg` (Kufic-style pseudo-script) and
   `04_denier_rare.svg` (crown) measured below MIN_FEATURE_MM at DIAMETER_MM below.
2. OpenSCAD, not Pillow/opencv, does the actual solid-modelling (blank + relief union).

This script:
  1. Re-measures each design's thinnest stroke from its source PNG.
  2. Where a design falls under MIN_FEATURE_MM at the chosen coin size, dilates the
     mask just enough to clear that minimum, then re-traces it (same method as
     build_coin_art.py) into a new "*_print.svg" — the flat-art SVGs are untouched.
  3. Writes one parametric .scad per coin (cylinder blank + extruded relief union).
  4. Shells out to the `openscad` CLI to export each .scad to STL, if installed.

Run with Python + Pillow, numpy, opencv-python-headless, shapely (same deps as
build_coin_art.py). Requires OpenSCAD (https://openscad.org/downloads.html) on PATH
for step 4; steps 1-3 run without it and the .scad files can be opened by hand.

    python build_coin_stl.py
"""
from pathlib import Path
import html
import json
import shutil
import subprocess
import cv2
import numpy as np
from PIL import Image
from shapely.geometry import Polygon
from shapely.geometry.polygon import orient
from shapely import affinity

# ---- Printer / coin parameters -------------------------------------------------
PRINTER = "Prusa i3 MK3S+, stock 0.4mm nozzle, FDM"
DIAMETER_MM = 28.0     # coin diameter
THICKNESS_MM = 2.0     # blank thickness below the relief
RELIEF_MM = 0.6        # relief height above the blank (3 layers at 0.2mm)
MIN_FEATURE_MM = 0.5   # thinnest allowed stroke (~1 nozzle-width) before dilating
FN = 128               # cylinder smoothness

ROOT = Path(__file__).resolve().parent
OUT_STL = ROOT / "STL"
OUT_STL.mkdir(exist_ok=True)
manifest = json.loads((ROOT / "generation_manifest.json").read_text(encoding="utf-8"))

report = []

def measure_p5_width_px(mask):
    """5th-percentile stroke width (px) along the mask's skeleton, out of a 2000px canvas."""
    dist = cv2.distanceTransform(mask, cv2.DIST_L2, 5)
    # cheap skeleton proxy: thin the mask with repeated erosion peaks (ridge = local maxima)
    # avoids adding scikit-image as a hard dependency of the coin pipeline.
    max_filt = cv2.dilate(dist, np.ones((3, 3), np.uint8))
    ridge = (dist == max_filt) & (mask > 0) & (dist > 0)
    widths = 2 * dist[ridge]
    return float(np.percentile(widths, 5)) if widths.size else None


def trace_mask_to_svg_and_png(mask2000, name, title):
    """Same normalize/trace/export as build_coin_art.py, applied to an already-2000px mask."""
    contours, tree = cv2.findContours(mask2000, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    tree = tree[0]
    polys = []

    def points(c):
        return cv2.approxPolyDP(c, 1.4, True).reshape(-1, 2)  # 2x source res -> 2x tolerance

    for i, contour in enumerate(contours):
        depth, parent = 0, tree[i][3]
        while parent >= 0:
            depth += 1
            parent = tree[parent][3]
        if depth % 2 or cv2.contourArea(contour) < 96:  # 4x area threshold at 2x linear res
            continue
        shell = points(contour)
        holes = [points(c) for j, c in enumerate(contours)
                 if tree[j][3] == i and cv2.contourArea(c) >= 640]
        p = Polygon(shell, holes)
        if not p.is_valid:
            p = p.buffer(0)
        polys.extend(list(p.geoms) if p.geom_type == "MultiPolygon" else [p])
    if not polys:
        return None
    minx = min(p.bounds[0] for p in polys)
    miny = min(p.bounds[1] for p in polys)
    maxx = max(p.bounds[2] for p in polys)
    maxy = max(p.bounds[3] for p in polys)
    cx, cy = (minx + maxx) / 2, (miny + maxy) / 2
    radius = max(((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
                 for p in polys for x, y in p.exterior.coords)
    scale = 460 / radius
    polys = [orient(affinity.translate(affinity.scale(p, scale, scale, origin=(cx, cy)),
                     500 - cx, 500 - cy), sign=1.0) for p in polys]
    paths = []
    for p in polys:
        for ring in [p.exterior, *p.interiors]:
            xy = list(ring.coords)[:-1]
            paths.append("M " + " L ".join(f"{x:.3f},{y:.3f}" for x, y in xy) + " Z")
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="1000" '
           'viewBox="0 0 1000 1000">\n'
           f"<title>{html.escape(title)} print-safe relief profile</title>\n"
           "<desc>Same design as the flat-art SVG, with strokes dilated just enough to "
           f"clear {MIN_FEATURE_MM}mm at a {DIAMETER_MM}mm coin on a 0.4mm nozzle.</desc>\n"
           '<path fill="#000000" fill-rule="nonzero" d="' + " ".join(paths) + '"/>\n</svg>\n')
    (ROOT / f"{name}_print.svg").write_text(svg, encoding="utf-8")
    return polys


SCAD_TEMPLATE = """// Auto-generated by build_coin_stl.py — do not hand-edit, edit the script instead.
DIAMETER = {diameter};
THICKNESS = {thickness};
RELIEF = {relief};
$fn = {fn};

union() {{
    cylinder(h=THICKNESS, d=DIAMETER, $fn=$fn);
    translate([0, 0, THICKNESS])
        linear_extrude(height=RELIEF)
            translate([-DIAMETER/2, -DIAMETER/2, 0])
                scale([DIAMETER/1000, DIAMETER/1000])
                    import("{svg_name}", dpi=25.4);  // 1 SVG unit = 1mm; default 96dpi shrinks it
}}
"""

openscad_available = shutil.which("openscad") is not None

for entry in manifest:
    name = entry["id"]
    source = ROOT / "sources" / (name + ".png")
    raw = Image.open(source).convert("RGBA")
    white = Image.new("RGBA", raw.size, "white")
    white.alpha_composite(raw)
    mask_src = (np.array(white.convert("L")) < 128).astype(np.uint8)
    mask2000 = cv2.resize(mask_src, (2000, 2000), interpolation=cv2.INTER_NEAREST)

    p5_before = measure_p5_width_px(mask2000)
    mm_before = (p5_before / 2000 * DIAMETER_MM) if p5_before else None
    dilate_radius_px = 0
    svg_name = name + ".svg"  # default: reuse the existing flat-art SVG as-is

    if mm_before is not None and mm_before < MIN_FEATURE_MM:
        shortfall_mm = MIN_FEATURE_MM - mm_before
        dilate_radius_px = int(np.ceil(shortfall_mm / DIAMETER_MM * 2000 / 2))
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,
                                            (2 * dilate_radius_px + 1, 2 * dilate_radius_px + 1))
        mask2000 = (cv2.dilate(mask2000 * 255, kernel) > 0).astype(np.uint8)
        trace_mask_to_svg_and_png(mask2000, name, entry["name"])
        svg_name = name + "_print.svg"

    p5_after = measure_p5_width_px(mask2000)
    mm_after = (p5_after / 2000 * DIAMETER_MM) if p5_after else None

    scad_path = OUT_STL / f"{name}.scad"
    scad_path.write_text(SCAD_TEMPLATE.format(
        diameter=DIAMETER_MM, thickness=THICKNESS_MM, relief=RELIEF_MM, fn=FN,
        svg_name=f"../{svg_name}"), encoding="utf-8")

    stl_path = OUT_STL / f"{name}.stl"
    stl_ok = False
    if openscad_available:
        result = subprocess.run(["openscad", "-o", str(stl_path), str(scad_path)],
                                 capture_output=True, text=True)
        stl_ok = result.returncode == 0 and stl_path.exists()

    report.append({
        "id": name,
        "min_stroke_mm_before_fix": round(mm_before, 3) if mm_before else None,
        "dilate_radius_canvas_px": dilate_radius_px,
        "min_stroke_mm_after_fix": round(mm_after, 3) if mm_after else None,
        "svg_used": svg_name,
        "scad": str(scad_path.relative_to(ROOT)),
        "stl_exported": stl_ok,
    })

(ROOT / "stl_report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print(json.dumps({
    "printer": PRINTER,
    "diameter_mm": DIAMETER_MM, "thickness_mm": THICKNESS_MM,
    "relief_mm": RELIEF_MM, "min_feature_mm": MIN_FEATURE_MM,
    "openscad_on_path": openscad_available,
}, indent=2))
print(json.dumps(report, indent=2))
if not openscad_available:
    print("\nOpenSCAD not found on PATH — .scad files were written to STL/ but not "
          "exported. Install OpenSCAD (https://openscad.org/downloads.html), then either "
          "open each .scad and export STL by hand, or re-run this script.")
