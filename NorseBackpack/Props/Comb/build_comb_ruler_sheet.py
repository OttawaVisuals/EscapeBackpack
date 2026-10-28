"""One Letter page with Aud's comb (PZ-003) and Liv's ruler (PP-025), for home printing on heavy paper.

Added 21 Oct 2026 (designer's request). The comb is drawn from the same geometry as the 3D-printed comb
(build_comb.py reads the live AD print PDF, so it fits the 6 x 4 in postcard); the ruler is the existing
2 x 6 in bookmark from Props/LivRuler/build_ruler_pdf.py, matched to the current Rollo map (120 mark).

Output: NorseBackpack/Print/_pdf_source/Comb_And_Ruler_Print.pdf (Letter, print at 100 %).
"""
import sys
from pathlib import Path

from PIL import Image
from reportlab.lib.colors import Color, HexColor
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.pdfgen.pathobject import PDFPathObject
from shapely.ops import unary_union

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "LivRuler"))
import build_comb as B  # noqa: E402
import build_ruler_pdf as R  # noqa: E402

OUT = B.ROOT / "NorseBackpack" / "Print" / "_pdf_source" / "Comb_And_Ruler_Print.pdf"
PT = B.PT
PAGE_W, PAGE_H = 215.9, 279.4  # mm, US Letter

BONE = Color(226 / 255, 214 / 255, 188 / 255)
CUT = HexColor("#5E4A2E")      # cut line
CARVE = Color(150 / 255, 128 / 255, 95 / 255)
INK = (110, 90, 60)


def fill_path(c, geom, to_xy, **kw):
    """Draw a shapely (Multi)Polygon with holes via even-odd fill."""
    p = c.beginPath()
    for poly in getattr(geom, "geoms", [geom]):
        if poly.is_empty:
            continue
        for ring in [poly.exterior, *poly.interiors]:
            pts = [to_xy(x, y) for x, y in ring.coords]
            p.moveTo(*pts[0])
            for pt in pts[1:]:
                p.lineTo(*pt)
            p.close()
    c.drawPath(p, fillMode=0, **kw)  # 0 = even-odd


def knot_image():
    """knotwork.png (black on white) as brown ink with transparency, turned to run along the handle."""
    g = Image.open(B.KNOTWORK_SVG.with_suffix(".png")).convert("L")
    alpha = g.point(lambda v: 255 - v)
    ink = Image.new("RGBA", g.size, INK + (255,))
    ink.putalpha(alpha)
    return ink.rotate(90, expand=True)


def draw_comb(c, ox, top):
    """ox, top: mm position of the comb's left and top edges on the page (top measured from the page bottom)."""
    line_ys, tips, handle, teeth, holes, gaps, lobe_gap = B.build_geometry()
    cuts, knot = B.carvings(handle, holes)
    outline = unary_union([handle] + teeth).difference(unary_union(holes))
    minx, miny, maxx, maxy = outline.bounds

    def to_xy(x, y):
        return (ox + (x - minx) * PT) * mm, (top - (y - miny) * PT) * mm

    c.setFillColor(BONE)
    c.setStrokeColor(CUT)
    c.setLineWidth(0.4)
    fill_path(c, outline, to_xy, fill=1, stroke=1)
    c.setFillColor(CARVE)
    fill_path(c, cuts, to_xy, fill=1, stroke=0)
    bx0, by0, bx1, by1 = knot[1]
    img = knot_image()
    px0, py1 = to_xy(bx0, by0)
    px1, py0 = to_xy(bx1, by1)
    c.drawImage(ImageReader(img), px0, py0, px1 - px0, py1 - py0, mask="auto")
    w_mm, h_mm = (maxx - minx) * PT, (maxy - miny) * PT
    return w_mm, h_mm, [to_xy(x, y) for x, y in B.AD.COMB_MARKS]


def main():
    c = canvas.Canvas(str(OUT), pagesize=(PAGE_W * mm, PAGE_H * mm))
    c.setTitle("Aud's comb and Liv's ruler (home print, heavy paper)")

    comb_w, comb_h = 100.7, 87.8
    comb_x = (PAGE_W - comb_w) / 2
    comb_top = PAGE_H - 22
    w, h, _ = draw_comb(c, comb_x, comb_top)

    c.setFillColor(R.DARK)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(20 * mm, (PAGE_H - 11) * mm, "Aud's comb and Liv's ruler. Print at 100% (Actual size) on heavy paper. Do not 'fit to page'.")
    c.setFont("Helvetica", 8)
    c.drawString(20 * mm, (PAGE_H - 15.5) * mm,
                 "Comb: cut on the brown outline, cut out the slots between the teeth and punch the two 2 mm holes.")

    ox = (PAGE_W - R.CARD_W) / 2
    oy = comb_top - h - 40 - R.CARD_H
    R.draw_card(c, ox, oy)
    R.crop_marks(c, ox, oy)

    by = oy - 14
    R.pen(c, 0.6, R.DARK)
    c.line(ox * mm, by * mm, (ox + 50) * mm, by * mm)
    for x in (ox, ox + 50):
        c.line(x * mm, (by - 1.5) * mm, x * mm, (by + 1.5) * mm)
    c.setFillColor(R.DARK)
    c.setFont("Helvetica", 8)
    c.drawString((ox + 54) * mm, (by - 1) * mm, "This bar must measure exactly 50 mm. Ruler: cut along the corner marks.")
    c.showPage()
    c.save()
    print(OUT, f"comb {w:.1f} x {h:.1f} mm, ruler bottom at {oy - 14:.0f} mm from page bottom")


if __name__ == "__main__":
    main()
