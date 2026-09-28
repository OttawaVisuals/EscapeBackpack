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
GRAPH_W = 2.7 * inch
GRAPH_TOP = 0.8 * inch  # from the card top, to the top perch centre
NODE_R = 0.125 * inch


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
    pos = node_positions()
    c.setFillColor(INK)
    c.setFont("CinzelBold", 12.5)
    c.drawCentredString(CARD_W / 2, CARD_H - 0.3 * inch, "THE RAVEN’S FLIGHTS")
    c.setFont("Helvetica", 7)
    c.drawCentredString(CARD_W / 2, CARD_H - 0.44 * inch, "Follow the five letters you uncovered.")
    c.drawCentredString(CARD_W / 2, CARD_H - 0.555 * inch, "Read the number on each flight, in order.")

    # Flights: all drawn alike, digit on a white knockout at the midpoint.
    c.setStrokeColor(LINE)
    c.setLineWidth(0.6)
    for a, b, _ in PERCH_FLIGHTS:
        (x1, y1), (x2, y2) = pos[a], pos[b]
        c.line(x1, y1, x2, y2)
    c.setFont("CinzelRegular", 8.5)
    for a, b, n in PERCH_FLIGHTS:
        (x1, y1), (x2, y2) = pos[a], pos[b]
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        c.setFillColor(white)
        c.rect(mx - 4.2, my - 4.6, 8.4, 9.2, stroke=0, fill=1)
        c.setFillColor(INK)
        c.drawCentredString(mx, my - 3, str(n))

    # Perches.
    c.setLineWidth(0.8)
    c.setStrokeColor(INK)
    c.setFont("CinzelBold", 9.5)
    for k, (x, y) in pos.items():
        c.setFillColor(white)
        c.circle(x, y, NODE_R, stroke=1, fill=1)
        c.setFillColor(INK)
        c.drawCentredString(x, y - 3.4, k)

    # Four blank answer boxes.
    box, gap = 0.26 * inch, 0.07 * inch
    total = 4 * box + 3 * gap
    bx, by = (CARD_W - total) / 2, 0.16 * inch
    c.setLineWidth(0.6)
    c.setStrokeColor(LINE)
    for i in range(4):
        c.rect(bx + i * (box + gap), by, box, box, stroke=1, fill=0)

    # Small raven emblem, matching the one on the pouch lock (PZ-02 release note).
    icon = 0.32 * inch
    c.drawImage(str(RAVEN_ICON), CARD_W - icon - 0.14 * inch, 0.12 * inch, icon, icon, mask="auto")


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
    print(build_docx())


if __name__ == "__main__":
    main()
