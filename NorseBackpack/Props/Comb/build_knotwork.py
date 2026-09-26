"""Make the comb's printable black/white band and closed SVG from its ImageGen source."""
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
raw = Image.open(HERE / "knotwork_source.png").convert("RGBA")
white = Image.new("RGBA", raw.size, "white")
white.alpha_composite(raw)
ink = np.asarray(white.convert("L")) < 128
ys, xs = np.where(ink)
if not len(xs):
    raise SystemExit("No black artwork in source")

# The source has transparent padding. Fit only its silhouette in an exact 8:1 canvas.
crop = Image.fromarray((ink[min(ys):max(ys)+1, min(xs):max(xs)+1] * 255).astype("uint8"))
crop = crop.resize((3040, 360), Image.Resampling.LANCZOS)
canvas = Image.new("L", (3200, 400), 0)
canvas.paste(crop, ((3200 - crop.width) // 2, (400 - crop.height) // 2))
mask = (np.asarray(canvas) >= 128).astype("uint8") * 255
Image.fromarray(255 - mask).convert("RGB").save(HERE / "knotwork.png")

contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
if hierarchy is None:
    raise SystemExit("No vector contours")
tree = hierarchy[0]
paths = []
for i, contour in enumerate(contours):
    if cv2.contourArea(contour) < 20:
        continue
    # Even-depth contours are islands; odd-depth contours are holes.
    # The nonzero winding rule gives OpenSCAD reliable solid/void geometry.
    depth, parent = 0, tree[i][3]
    while parent >= 0:
        depth += 1
        parent = tree[parent][3]
    points = cv2.approxPolyDP(contour, 1.0, True).reshape(-1, 2)
    if len(points) < 3:
        continue
    signed = cv2.contourArea(points, oriented=True)
    desired_clockwise = depth % 2 == 0
    if (signed > 0) != desired_clockwise:
        points = points[::-1]
    paths.append("M " + " L ".join(f"{x},{y}" for x, y in points) + " Z")

svg = ('<svg xmlns="http://www.w3.org/2000/svg" width="3200" height="400" '
       'viewBox="0 0 3200 400">\n'
       '<title>Aud comb handle knotwork</title>\n'
       '<path fill="#000000" fill-rule="nonzero" d="' + " ".join(paths) + '"/>\n'
       '</svg>\n')
(HERE / "knotwork.svg").write_text(svg, encoding="utf-8")
print(f"Wrote 3200x400 knotwork.png and knotwork.svg ({len(paths)} closed paths)")
