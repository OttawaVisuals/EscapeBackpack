"""
The raven's flights player card (PZ-02 / PR-26). 3.5 x 2 in business card, landscape, single-sided.
Resized 20 Oct 2026 from 4 x 3 in (designer, Q-052: stock business-card printing). The graph is
stretched to fill the safe area (separate x and y scales, so no flight crosses another and the
layout keeps its shape); digits and perch letters keep their 11 / 12 pt sizes.
Earlier: 4 x 3 in chosen by the user, 28 Sept 2026 (the review's working size was half-Letter).

Graph, clue and title are the approved 22 Sept 2026 spec (Review_2026-09-22/approved_changes.py,
RV-21): eight perches, twelve two-way flights, one digit each, no crossings, no route marked.
HRAFN -> 2, 6, 4, 8. Node positions follow the accepted sketch,
output/visualizations/norse-five-perches-comparison.png.

Writes:
  NorseBackpack/Print/_pdf_source/Raven_Flights_Card_Print.pdf      -- the card at exact trim size (player view only)
  Props/RavenFlights/Raven_Flights_Card_preview.png -- 300dpi render for the Norse page
  NorseBackpack/Print/Print_RavenFlights_Card.docx  -- home-print Letter sheet: the card at 100 % with
                                                  corner crop marks outside the trim
"""

import importlib.util
import io
import math
import sys
from pathlib import Path

import pymupdf as fitz
from docx import Document
from PIL import Image, ImageDraw
from reportlab.lib.colors import HexColor, white
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[3]
FONT_DIR = ROOT / "Fonts"
OUT_PDF = ROOT / "NorseBackpack" / "Print" / "_pdf_source" / "Raven_Flights_Card_Print.pdf"
PREVIEW = Path(__file__).resolve().parent / "Raven_Flights_Card_preview.png"
OUT_DOCX = ROOT / "NorseBackpack" / "Print" / "Print_RavenFlights_Card.docx"
RAVEN_ICON = ROOT / "NorseBackpack" / "Art" / "Raven" / "Raven_Profile_Icon_v1.png"

sys.path.insert(0, str(ROOT / "NorseBackpack" / "Review_2026-09-22"))
from review_content import PERCH_FLIGHTS, PERCH_ROUTE, PERCH_CODE  # noqa: E402

_spec = importlib.util.spec_from_file_location(
    "postcard_print", ROOT / "NorseBackpack" / "Postcards" / "build_print_test_docx.py")
_postcard = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_postcard)
add_floating_picture = _postcard.add_floating_picture

CARD_W = 3.5 * inch
CARD_H = 2.0 * inch
SAFE = 0.125 * inch  # print-shop safe zone: nothing closer than this to the trim
INK = HexColor("#222222")
LINE = HexColor("#555555")

pdfmetrics.registerFont(TTFont("CinzelBold", str(FONT_DIR / "Cinzel" / "static" / "Cinzel-Bold.ttf")))
pdfmetrics.registerFont(TTFont("CinzelRegular", str(FONT_DIR / "Cinzel" / "static" / "Cinzel-Regular.ttf")))

# Perch centres in the accepted sketch's pixel space (y down).
SKETCH = {"H": (128, 329), "R": (385, 293), "T": (675, 329), "A": (385, 444),
          "O": (128, 465), "N": (675, 465), "F": (253, 604), "S": (550, 604)}
NODE_R = 0.14 * inch  # was 0.16 on the 4 x 3 card; the 12 pt letter still clears the ring
DIGIT_PT, NODE_PT = 11, 12


def check_route():
    """HRAFN must read PERCH_CODE along direct flights, or the card is wrong."""
    edges = {frozenset((a, b)): n for a, b, n in PERCH_FLIGHTS}
    digits = "".join(str(edges[frozenset(p)]) for p in zip(PERCH_ROUTE, PERCH_ROUTE[1:]))
    assert digits == PERCH_CODE, (digits, PERCH_CODE)
    assert len(edges) == 12 and set(SKETCH) == {x for e in edges for x in e}


def node_positions():
    """Perch centres filling the safe area: perch rings touch the safe zone on all four sides."""
    xs = [p[0] for p in SKETCH.values()]
    ys = [p[1] for p in SKETCH.values()]
    inset = SAFE + NODE_R
    sx = (CARD_W - 2 * inset) / (max(xs) - min(xs))
    sy = (CARD_H - 2 * inset) / (max(ys) - min(ys))
    return {k: (inset + (x - min(xs)) * sx, CARD_H - inset - (y - min(ys)) * sy)
            for k, (x, y) in SKETCH.items()}


def draw_card(c):
    """Path only: perches, flights and their digits. No title, text, answer boxes or emblem.
    Nothing is filled white, so the card can be printed on coloured paper: each flight stops
    at the perch outline and breaks around its digit instead of using a white knockout."""
    pos = node_positions()

    c.setStrokeColor(LINE)
    c.setLineWidth(0.8)
    digit_gap = 6.5
    c.setFont("CinzelRegular", DIGIT_PT)
    for a, b, n in PERCH_FLIGHTS:
        (x1, y1), (x2, y2) = pos[a], pos[b]
        length = math.hypot(x2 - x1, y2 - y1)
        ux, uy = (x2 - x1) / length, (y2 - y1) / length
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        # Gap half-width along the line: enough to clear the digit's box in this direction.
        # (Steep flights used abs(uy) * 0.75 on the 4 x 3 card; at 3.5 x 2 the short vertical
        # flights need their full length, and a digit is about as tall as it is wide.)
        half = digit_gap / max(abs(ux), abs(uy)) * 0.9 + 0.5
        sx, sy = x1 + ux * NODE_R, y1 + uy * NODE_R
        ex, ey = x2 - ux * NODE_R, y2 - uy * NODE_R
        c.line(sx, sy, mx - ux * half, my - uy * half)
        c.line(mx + ux * half, my + uy * half, ex, ey)
        c.setFillColor(INK)
        c.drawCentredString(mx, my - DIGIT_PT * 0.34, str(n))

    c.setLineWidth(1.0)
    c.setStrokeColor(INK)
    c.setFont("CinzelBold", NODE_PT)
    for k, (x, y) in pos.items():
        c.circle(x, y, NODE_R, stroke=1, fill=0)
        c.setFillColor(INK)
        c.drawCentredString(x, y - NODE_PT * 0.36, k)


def build_pdf():
    OUT_PDF.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUT_PDF), pagesize=(CARD_W, CARD_H))
    c.setTitle("The raven's flights - player card")
    draw_card(c)
    c.showPage()
    c.save()
    return OUT_PDF


# Crop marks sit in a margin around the trim box; the docx picture carries that margin.
MARK_MARGIN_IN = 0.25
MARK_LEN_IN = 0.18
MARK_GAP_IN = 0.04
DPI = 300
TOP_MARGIN_IN = _postcard.TOP_MARGIN_IN
SIDE_MARGIN_IN = _postcard.SIDE_MARGIN_IN


def build_docx():
    pix = fitz.open(OUT_PDF)[0].get_pixmap(matrix=fitz.Matrix(DPI / 72, DPI / 72), alpha=False)
    card = Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB")
    card.save(PREVIEW)
    m = round(MARK_MARGIN_IN * DPI)
    img = Image.new("RGB", (card.width + 2 * m, card.height + 2 * m), "white")
    img.paste(card, (m, m))
    d = ImageDraw.Draw(img)
    L, g, w = round(MARK_LEN_IN * DPI), round(MARK_GAP_IN * DPI), 2
    x0, y0, x1, y1 = m, m, m + card.width, m + card.height
    for x in (x0, x1):
        for y, sign in ((y0, -1), (y1, 1)):
            d.line([(x, y + sign * g), (x, y + sign * (g + L))], fill="black", width=w)
    for y in (y0, y1):
        for x, sign in ((x0, -1), (x1, 1)):
            d.line([(x + sign * g, y), (x + sign * (g + L), y)], fill="black", width=w)
    buf = io.BytesIO()
    img.save(buf, format="PNG", dpi=(DPI, DPI))
    buf.seek(0)

    doc = Document()
    add_floating_picture(doc.add_paragraph(), buf, CARD_W / inch + 2 * MARK_MARGIN_IN, CARD_H / inch + 2 * MARK_MARGIN_IN,
                         SIDE_MARGIN_IN - MARK_MARGIN_IN, TOP_MARGIN_IN)
    OUT_DOCX.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(OUT_DOCX))
    return OUT_DOCX


def main():
    check_route()
    print(build_pdf())
    # Its own print sheet again since 20 Oct 2026: the luggage tags it shared a sheet with are parked
    # (PP-023), so Props/build_luggage_tag_inserts_pdf.py is no longer the card's print master.
    print(build_docx())


if __name__ == "__main__":
    main()
