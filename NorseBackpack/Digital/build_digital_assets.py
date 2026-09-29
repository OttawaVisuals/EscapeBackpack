"""Export props for the browser prototype (Prototype_Comb_Tally.html).

Aud's comb is taken from Props/Comb/build_comb.py, so the on-screen comb is the printed comb:
same teeth, same broken tips, same alignment holes. Output is in card points (the AD card is
360 x 252 pt), so the page can lay it straight over the AD back PNG.

Writes, next to this script:
  assets/comb.svg   -- comb body (holes cut through), carvings and knotwork
  assets/comb.json  -- the SVG's origin and the two hole centres, in card points
  assets/comb.js    -- the same two, as a script, so the page also opens from file://
"""
import json
import re
import sys
from pathlib import Path

from shapely.ops import unary_union

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "Props" / "Comb"))
import build_comb as C  # noqa: E402

OUT = HERE / "assets"


def path_d(geom):
    parts = []
    for p in getattr(geom, "geoms", [geom]):
        if p.is_empty:
            continue
        for ring in [p.exterior, *p.interiors]:
            pts = list(ring.coords)
            parts.append("M" + " L".join("%.2f,%.2f" % xy for xy in pts) + "Z")
    return " ".join(parts)


def main():
    OUT.mkdir(exist_ok=True)
    line_ys, tips, handle, teeth, holes, gaps, lobe_gap = C.build_geometry()
    cuts, knot = C.carvings(handle, holes)
    body = unary_union([handle] + teeth).difference(unary_union(holes))
    x0, y0, x1, y1 = body.bounds
    pad = 1.0
    x0, y0, x1, y1 = x0 - pad, y0 - pad, x1 + pad, y1 + pad
    knot_svg = ""
    if knot[0] == "band_svg":
        bx0, by0, bx1, by1 = knot[1]
        src = C.KNOTWORK_SVG.read_text(encoding="utf-8")
        paths = "".join(re.findall(r"<path[^>]*/>", src)).replace('fill="#000000"', "")
        # the band is drawn 3200 x 400, horizontally; stand it up along the handle
        knot_svg = ('<g class="knot" transform="translate(%.2f,%.2f) rotate(90) scale(%.5f,%.5f) '
                    'translate(-1600,-200)">%s</g>'
                    % ((bx0 + bx1) / 2, (by0 + by1) / 2, (by1 - by0) / 3200, (bx1 - bx0) / 400, paths))
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="%.2f %.2f %.2f %.2f" width="%.2f" height="%.2f">\n'
           '<path class="body" fill-rule="evenodd" d="%s"/>\n'
           '<path class="cut" fill-rule="evenodd" d="%s"/>\n%s\n</svg>\n'
           % (x0, y0, x1 - x0, y1 - y0, x1 - x0, y1 - y0, path_d(body), path_d(cuts), knot_svg))
    (OUT / "comb.svg").write_text(svg, encoding="utf-8")
    info = {"origin_pt": [round(x0, 2), round(y0, 2)], "size_pt": [round(x1 - x0, 2), round(y1 - y0, 2)],
            "holes_pt": [[round(h.centroid.x, 2), round(h.centroid.y, 2)] for h in holes],
            "card_marks_pt": C.AD.COMB_MARKS}
    (OUT / "comb.json").write_text(json.dumps(info, indent=2), encoding="utf-8")
    (OUT / "comb.js").write_text("window.COMB_ASSET = %s;\n" % json.dumps(dict(info, svg=svg)), encoding="utf-8")
    print(json.dumps(info, indent=2))


if __name__ == "__main__":
    main()
