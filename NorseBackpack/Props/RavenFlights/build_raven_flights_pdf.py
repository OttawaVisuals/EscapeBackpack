"""
The raven's flights player card (PZ-02 / PR-26). 4 x 3 in, landscape, single-sided, plain white.
Size and paper chosen by the user, 28 Sept 2026 (the review's working size was half-Letter).

Graph, clue and title are the approved 22 Sept 2026 spec (Review_2026-09-22/approved_changes.py,
RV-21): eight perches, twelve two-way flights, one digit each, no crossings, no route marked.
HRAFN -> 2, 6, 4, 8. Node positions follow the accepted sketch,
output/visualizations/norse-five-perches-comparison.png.

Writes:
  output/pdf/Raven_Flights_Card_Print.pdf      -- the card at exact trim size (player view only)
  Props/RavenFlights/Raven_Flights_Card_preview.png -- 300dpi render for the Norse page
  output/docx/PrintTest_RavenFlights.docx      -- print file, same top-left zone and floating
                                                  picture as the postcard/ticket print files,
                                                  with corner crop marks outside the trim
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
OUT_PDF = ROOT / "output" / "pdf" / "Raven_Flights_Card_Print.pdf"
PREVIEW = Path(__file__).resolve().parent / "Raven_Flights_Card_preview.png"
OUT_DOCX = ROOT / "output" / "docx" / "PrintTest_RavenFlights.docx"
RAVEN_ICON = ROOT / "NorseBackpack" / "Art" / "Raven" / "Raven_Profile_Icon_v1.png"

sys.path.insert(0, str(ROOT / "NorseBackpack" / "Review_2026-09-22"))
from review_content import PERCH_FLIGHTS, PERCH_ROUTE, PERCH_CODE  # noqa: E402

_spec = importlib.util.spec_from_file_location(
    "postcard_print", ROOT / "NorseBackpack" / "Postcards" / "build_print_test_docx.py")
_postcard = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_postcard)
add_floating_picture = _postcard.add_floating_picture

CARD_W = 4.0 * inch
CARD_H = 3.0 * inch
INK = HexColor("#222222")
LINE = HexColor("#555555")

pdfmetrics.registerFont(TTFont("CinzelBold", str(FONT_DIR / "Cinzel" / "static" / "Cinzel-Bold.ttf")))
pdfmetrics.registerFont(TTFont("CinzelRegular", str(FONT_DIR / "Cinzel" / "static" / "Cinzel-Regular.ttf")))

# Perch centres in the accepted sketch's pixel space (y down).
SKETCH = {"H": (128, 329), "R": (385, 293), "T": (675, 329), "A": (385, 444),
          "O": (128, 465), "N": (675, 465), "F": (253, 604), "S": (550, 604)}
GRAPH_W = 3.4 * inch
GRAPH_TOP = 0.0  # unused: the graph is centred vertically in draw_card
NODE_R = 0.16 * inch
DIGIT_PT, NODE_PT = 11, 12


def check_route():
    """HRAFN must read PERCH_CODE along direct flights, or the card is wrong."""
    edges = {frozenset((a, b)): n for a, b, n in PERCH_FLIGHTS}
    digits = "".join(str(edges[frozenset(p)]) for p in zip(PERCH_ROUTE, PERCH_ROUTE[1:]))
    assert digits == PERCH_CODE, (digits, PERCH_CODE)
    assert len(edges) == 12 and set(SKETCH) == {x for e in edges for x in e}


def node_positions():
    xs = [p[0] for p in SKETCH.values()]
    ys = [p[1] for p in SKETCH.values()]
    scale = GRAPH_W / (max(xs) - min(xs))
    x0 = (CARD_W - GRAPH_W) / 2
    return {k: (x0 + (x - min(xs)) * scale, CARD_H - GRAPH_TOP - (y - min(ys)) * scale)
            for k, (x, y) in SKETCH.items()}


def draw_card(c):
    """Path only: perches, flights and their digits. No title, text, answer boxes or emblem.
    Nothing is filled white, so the card can be printed on coloured paper: each flight stops
    at the perch outline and breaks around its digit instead of using a white knockout."""
    pos = node_positions()
    ys = [y for _, y in pos.values()]
    dy = CARD_H / 2 - (max(ys) + min(ys)) / 2   # centre the graph vertically on the card
    pos = {k: (x, y + dy) for k, (x, y) in pos.items()}

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
        half = digit_gap / max(abs(ux), abs(uy) * 0.75) * 0.9 + 0.5
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
    add_floating_picture(doc.add_paragraph(), buf, 4.0 + 2 * MARK_MARGIN_IN, 3.0 + 2 * MARK_MARGIN_IN,
                         SIDE_MARGIN_IN - MARK_MARGIN_IN, TOP_MARGIN_IN)
    OUT_DOCX.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(OUT_DOCX))
    return OUT_DOCX


def main():
    check_route()
    print(build_pdf())
    # The card is now printed on the luggage-tag sheet (Props/build_luggage_tag_inserts_pdf.py);
    # build_docx() made the old stand-alone print file and is no longer called.


if __name__ == "__main__":
    main()
