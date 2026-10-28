"""Liv's ruler (PP-025): printed card ruler for the rebus distance (PZ-011). Mock-up, 15 Oct 2026.

Resized 20 Oct 2026 (designer, Q-052) from 160 x 40 mm to a 2 x 6 in bookmark (152.4 x 50.8 mm), for stock
bookmark printing. Scales unchanged (same mm per 10 units, same 0 line, same ranges); the rebus pictures are
right-aligned inside the print-shop safe zone; the extra height goes to larger numbers and a larger raven.
Two outputs: the home-print Letter sheet (Liv_Ruler_Print.pdf) and a print-shop file with 0.125 in bleed
(Liv_Ruler_2x6_PrintShop.pdf).

One face for now, two long edges, one scale each. The edge name is a picture rebus, not a ratio:
  top edge    LONGSHIP = long + sheep   (the correct edge)
  bottom edge SPEAR    = pear + S       (decoy)
Scales are free units. On the LONGSHIP edge the Chalus to Saint-Clair-sur-Epte dot-to-dot distance
lands exactly on the numbered 120 mark. On the SPEAR edge the same distance falls half way between
the 70 and 80 marks, so a wrong edge visibly ends off a mark. Only whole ticks are drawn (no minor
ticks) so a reading is always "the nearest numbered mark", about 4 mm of tolerance.

DIST_MM is calculated, not measured on a print: pt() from build_trail_maps_pdf.py, Rollo's sheet,
stops.js coordinates, 235.63 pt. Re-run the check below if the map changes.
"""
from pathlib import Path

import pymupdf
from reportlab.lib.colors import HexColor
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "NorseBackpack" / "Print" / "_pdf_source" / "Liv_Ruler_Print.pdf"
OUT_SHOP = ROOT / "NorseBackpack" / "Print" / "_pdf_source" / "Liv_Ruler_2x6_PrintShop.pdf"
PREVIEW = Path(__file__).with_name("Liv_Ruler_Preview.png")
FONT_DIR = ROOT / "Fonts"

DIST_MM = 83.126  # Chalus to Saint-Clair-sur-Epte, dot to dot, Rollo's sheet
TARGET = 120  # mark the LONGSHIP edge must land on (the lock code); 15 Oct 2026, designer: 120 or 130 rather than 100
DECOY_LAND = 75  # where the same distance falls on the SPEAR edge (between marks)

CARD_W, CARD_H = 152.4, 50.8  # mm: 6 x 2 in bookmark, used landscape (was 160 x 40 mm until 20 Oct 2026)
SAFE = 3.175  # mm (0.125 in): print-shop safe zone; only the measuring edges' ticks run to the trim
BLEED = 3.175  # mm (0.125 in): green background beyond the trim
ZERO_X = 8.0  # mm from the card's left edge
LONG_MM_PER_10 = DIST_MM / (TARGET / 10)  # 6.927 at TARGET 120
SPEAR_MM_PER_10 = DIST_MM / (DECOY_LAND / 10)  # 11.0835
LONG_MAX, SPEAR_MAX = 150, 110  # last numbered mark on each edge
STRIP_H = 15.0  # mm, height of each scale strip (was 13 on the 40 mm card)
TICK, TICK0 = 5.0, 7.0  # mm, tick lengths (numbered marks, the 0 line); were 4.2 and 6.0
NUM_PT = 7.4  # scale numbers (were 6.4 pt)
NUM_CAP = 2.6  # mm, approximate cap height of NUM_PT Cinzel Bold
ICON_Y = 7.0  # mm in from the edge, centre of the rebus pictures

PAPER = HexColor("#EFE3C4")  # postcard paper; the ruler uses it for ticks and numbers
FOREST = HexColor("#1E4A38")  # ruler background (15 Oct 2026, designer)
TEAL = HexColor("#2F7775")
RULE = HexColor("#A99A7B")
DARK = HexColor("#283B34")  # page text and crop marks, outside the card
INK = PAPER  # drawing colour on the card

pdfmetrics.registerFont(TTFont("CinzelExtraBold", str(FONT_DIR / "Cinzel" / "static" / "Cinzel-ExtraBold.ttf")))
pdfmetrics.registerFont(TTFont("CinzelBold", str(FONT_DIR / "Cinzel" / "static" / "Cinzel-Bold.ttf")))
pdfmetrics.registerFont(TTFont("NothingYouCouldDo", str(FONT_DIR / "Nothing_You_Could_Do" / "NothingYouCouldDo-Regular.ttf")))


def pen(c, w=0.9, col=None):
    c.setStrokeColor(col or INK)
    c.setLineWidth(w)
    c.setLineCap(1)
    c.setLineJoin(1)


# --- rebus pictures: drawn in mm around (0, 0), then placed with c.translate -------------------

def icon_long(c):
    """'long': a very long double-headed arrow."""
    pen(c)
    c.line(-6 * mm, 0, 6 * mm, 0)
    for s in (-1, 1):
        x = s * 6 * mm
        c.line(x, 0, x - s * 1.8 * mm, 1.5 * mm)
        c.line(x, 0, x - s * 1.8 * mm, -1.5 * mm)


def icon_sheep(c):
    """'sheep': one woolly outline (inner circle edges hidden), round head, four legs."""
    pen(c)
    for lx in (-2.6, -1.0, 0.6, 2.0):  # legs, behind the body
        c.line(lx * mm, -1.6 * mm, lx * mm, -4.4 * mm)
    wool = ((-2.6, 0.2, 1.9), (-0.9, 1.7, 2.0), (1.2, 1.5, 1.9), (2.1, -0.1, 1.5), (-0.2, -0.5, 2.0), (-2.2, -1.0, 1.4))
    c.setStrokeColor(INK)
    c.setLineWidth(1.8)  # ring twice as wide: the half inside each circle is then covered by the fill
    for cx, cy, r in wool:
        c.circle(cx * mm, cy * mm, r * mm, stroke=1, fill=0)
    c.setFillColor(PAPER)
    for cx, cy, r in wool:
        c.circle(cx * mm, cy * mm, r * mm, stroke=0, fill=1)
    pen(c)
    c.setFillColor(PAPER)
    c.ellipse(3.0 * mm, -1.2 * mm, 5.6 * mm, 1.8 * mm, stroke=1, fill=1)  # head
    c.setFillColor(INK)
    c.circle(4.7 * mm, 0.7 * mm, 0.28 * mm, stroke=0, fill=1)  # eye
    c.line(3.5 * mm, 1.7 * mm, 2.9 * mm, 2.8 * mm)  # ear


def icon_pear(c):
    pen(c)
    p = c.beginPath()
    p.moveTo(-1.0 * mm, 3.0 * mm)
    p.lineTo(1.0 * mm, 3.0 * mm)
    p.curveTo(1.3 * mm, 1.4 * mm, 3.3 * mm, 0.8 * mm, 3.3 * mm, -1.2 * mm)
    p.curveTo(3.3 * mm, -3.2 * mm, 1.6 * mm, -3.6 * mm, 0, -3.6 * mm)
    p.curveTo(-1.6 * mm, -3.6 * mm, -3.3 * mm, -3.2 * mm, -3.3 * mm, -1.2 * mm)
    p.curveTo(-3.3 * mm, 0.8 * mm, -1.3 * mm, 1.4 * mm, -1.0 * mm, 3.0 * mm)
    c.drawPath(p, stroke=1, fill=0)
    c.line(0, 3.0 * mm, 0.5 * mm, 4.6 * mm)  # stem
    lf = c.beginPath()  # leaf
    lf.moveTo(0.4 * mm, 4.2 * mm)
    lf.curveTo(1.4 * mm, 5.0 * mm, 2.8 * mm, 4.8 * mm, 3.2 * mm, 4.2 * mm)
    lf.curveTo(2.6 * mm, 3.4 * mm, 1.2 * mm, 3.4 * mm, 0.4 * mm, 4.2 * mm)
    c.drawPath(lf, stroke=1, fill=0)


def icon_s(c):
    c.setFillColor(INK)
    c.setFont("NothingYouCouldDo", 30)
    c.drawCentredString(0, -3.4 * mm, "S")


ICON_DIR = Path(__file__).with_name("Icons")
ICON_FILES = {icon_long: "long.png", icon_sheep: "sheep.png", icon_pear: "pear.png", icon_s: "s.png"}
ICON_H = 7.5
ICON_MAX_W = 17.0  # mm, caps wide pictures such as the long arrow  # mm, height of a supplied picture; width follows its aspect ratio


def place(c, fn, x_mm, y_mm):
    """Draw a picture centred on (x_mm, y_mm). A PNG in Icons/ replaces the placeholder vector."""
    c.saveState()
    c.translate(x_mm * mm, y_mm * mm)
    png = ICON_DIR / ICON_FILES[fn]
    if png.exists():
        img = ImageReader(str(png))
        iw, ih = img.getSize()
        h = ICON_H * mm
        w = h * iw / ih
        if w > ICON_MAX_W * mm:
            w = ICON_MAX_W * mm
            h = w * ih / iw
        c.drawImage(img, -w / 2, -h / 2, w, h, mask="auto")
    else:
        fn(c)
    c.restoreState()


def icon_width(fn):
    """Width in mm a picture is drawn at by place() (vector placeholders: their nominal 12 mm)."""
    png = ICON_DIR / ICON_FILES[fn]
    if not png.exists():
        return 12.0
    iw, ih = ImageReader(str(png)).getSize()
    return min(ICON_H * iw / ih, ICON_MAX_W)


def right_aligned(fns, gap=1.5):
    """Centres (mm) for pictures laid left to right, the last one ending at the safe zone."""
    x, out = CARD_W - SAFE - 0.3, []
    for fn in reversed(fns):
        w = icon_width(fn)
        out.append((fn, x - w / 2))
        x -= w + gap
    return list(reversed(out))


LONG_ICONS = right_aligned([icon_long, icon_sheep])
SPEAR_ICONS = right_aligned([icon_s, icon_pear])


# --- the card ------------------------------------------------------------------------------------

def draw_scale(c, top, mm_per_10, last, icons):
    """One edge. top=True: ticks hang down from the top edge; False: rise from the bottom edge."""
    sign = -1 if top else 1
    edge_y = CARD_H if top else 0.0
    out = edge_y - sign * 1.5  # ticks start 1.5 mm into the bleed, so a slightly-off cut never detaches them
    pen(c, 0.6)
    c.line(0, edge_y * mm, CARD_W * mm, edge_y * mm)
    c.setFillColor(INK)
    for mark in range(0, last + 1, 10):
        x = ZERO_X + mark / 10 * mm_per_10
        length = TICK0 if mark == 0 else TICK
        pen(c, 1.1 if mark == 0 else 0.6)
        c.line(x * mm, out * mm, x * mm, (edge_y + sign * length) * mm)
        c.setFillColor(INK)
        c.setFont("CinzelBold", NUM_PT)
        ty = edge_y + sign * (TICK + 1.0) - (NUM_CAP if top else 0.0)
        c.drawCentredString(x * mm, ty * mm, str(mark))
    for fn, cx in icons:
        place(c, fn, cx, edge_y + sign * ICON_Y)


def draw_card(c, ox, oy):
    c.saveState()
    c.translate(ox * mm, oy * mm)
    c.setFillColor(FOREST)
    c.rect(-BLEED * mm, -BLEED * mm, (CARD_W + 2 * BLEED) * mm, (CARD_H + 2 * BLEED) * mm, fill=1, stroke=0)
    draw_scale(c, True, LONG_MM_PER_10, LONG_MAX, LONG_ICONS)
    # SPEAR edge: drawn turned 180 degrees about the card centre, so when the player flips the ruler
    # to use it, its numbers and pictures are upright and its 0 is on the left. Reads S + pear = SPEAR.
    c.saveState()
    c.translate(CARD_W / 2 * mm, CARD_H / 2 * mm)
    c.rotate(180)
    c.translate(-CARD_W / 2 * mm, -CARD_H / 2 * mm)
    draw_scale(c, True, SPEAR_MM_PER_10, SPEAR_MAX, SPEAR_ICONS)
    c.restoreState()
    raven = ICON_DIR / "raven.png"
    if raven.exists():
        img = ImageReader(str(raven))
        iw, ih = img.getSize()
        h = (CARD_H - 2 * STRIP_H - 1.5) * mm
        w = h * iw / ih
        c.drawImage(img, (CARD_W / 2) * mm - w / 2, (CARD_H / 2) * mm - h / 2, w, h, mask="auto")
    c.restoreState()


def crop_marks(c, ox, oy):
    pen(c, 0.3, DARK)
    gap, ln = BLEED + 1.0, 4.0  # marks start beyond the bleed
    for x in (ox, ox + CARD_W):
        for y, s in ((oy, -1), (oy + CARD_H, 1)):
            c.line(x * mm, (y + s * gap) * mm, x * mm, (y + s * (gap + ln)) * mm)
    for y in (oy, oy + CARD_H):
        for x, s in ((ox, -1), (ox + CARD_W, 1)):
            c.line((x + s * gap) * mm, y * mm, (x + s * (gap + ln)) * mm, y * mm)


def build():
    page_w, page_h = 215.9, 279.4  # US Letter, mm
    ox, oy = (page_w - CARD_W) / 2, page_h - 35 - CARD_H
    OUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUT), pagesize=(page_w * mm, page_h * mm))
    c.setTitle("Liv's ruler, 2 x 6 in (home print)")
    draw_card(c, ox, oy)
    crop_marks(c, ox, oy)

    # print check, outside the card
    by = oy - 24  # below the crop marks, which now start beyond the 3.2 mm bleed
    c.setFillColor(DARK)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(ox * mm, (oy - 15) * mm, "Print at 100% (Actual size). Do not 'fit to page'. Cut along the corner marks.")
    pen(c, 0.6, DARK)
    c.line(ox * mm, by * mm, (ox + 50) * mm, by * mm)
    for x in (ox, ox + 50):
        c.line(x * mm, (by - 1.5) * mm, x * mm, (by + 1.5) * mm)
    c.setFont("Helvetica", 8)
    c.drawString((ox + 54) * mm, (by - 1) * mm, "This bar must measure exactly 50 mm.")
    c.showPage()
    c.save()

    # print-shop file: one page, trim + 0.125 in bleed on every side, no marks
    shop = canvas.Canvas(str(OUT_SHOP), pagesize=((CARD_W + 2 * BLEED) * mm, (CARD_H + 2 * BLEED) * mm))
    shop.setTitle("Liv's ruler, 2 x 6 in bookmark, 0.125 in bleed")
    draw_card(shop, BLEED, BLEED)
    shop.showPage()
    shop.save()
    print(OUT_SHOP)

    # layout checks: pictures right of the last number, inside the safe zone
    for name, mm_per_10, last, icons in (("LONGSHIP", LONG_MM_PER_10, LONG_MAX, LONG_ICONS),
                                         ("SPEAR", SPEAR_MM_PER_10, SPEAR_MAX, SPEAR_ICONS)):
        last_num_right = ZERO_X + last / 10 * mm_per_10 + 2.6  # half the width of a 3-digit number
        left = min(cx - icon_width(fn) / 2 for fn, cx in icons)
        right = max(cx + icon_width(fn) / 2 for fn, cx in icons)
        assert left > last_num_right + 1.0, (name, left, last_num_right)
        assert right <= CARD_W - SAFE and ICON_Y - ICON_H / 2 >= SAFE, (name, right)
        print(f"{name}: last number ends {last_num_right:.1f} mm, pictures {left:.1f} to {right:.1f} mm")

    # numeric checks of what was drawn
    on_long = (TARGET / 10) * LONG_MM_PER_10
    on_spear = (DECOY_LAND / 10) * SPEAR_MM_PER_10
    print(f"LONGSHIP: 0 to {TARGET} mark = {on_long:.3f} mm (target {DIST_MM})")
    print(f"SPEAR: same distance reads {DIST_MM / SPEAR_MM_PER_10 * 10:.1f} (no mark; nearest are 70 and 80, "
          f"{abs(DIST_MM - 70 / 10 * SPEAR_MM_PER_10):.1f} and {abs(80 / 10 * SPEAR_MM_PER_10 - DIST_MM):.1f} mm away)")
    print(f"last marks: LONGSHIP {LONG_MAX} at {ZERO_X + LONG_MAX / 10 * LONG_MM_PER_10:.1f} mm, "
          f"SPEAR {SPEAR_MAX} at {ZERO_X + SPEAR_MAX / 10 * SPEAR_MM_PER_10:.1f} mm; card {CARD_W} x {CARD_H} mm")

    doc = pymupdf.open(str(OUT))
    clip = pymupdf.Rect(ox * mm - 20, (page_h - oy - CARD_H) * mm - 20, (ox + CARD_W) * mm + 20, (page_h - oy + 28) * mm + 20)
    doc[0].get_pixmap(dpi=300, clip=clip).save(str(PREVIEW))
    print(PREVIEW)


if __name__ == "__main__":
    build()
