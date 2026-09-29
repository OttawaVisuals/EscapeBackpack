import importlib.util
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "output" / "pdf" / "Luggage_Tag_Inserts_Print.pdf"
FONT_DIR = ROOT / "Fonts"

# Measured paper area inside the Lewis N. Clark luggage tag's insert slot: 9 cm x 5.4 cm.
CM = 72 / 2.54
CARD_W, CARD_H = 9 * CM, 5.4 * CM
PAGE = (8.5 * 72, 11 * 72)  # US Letter portrait
PAGE_W, PAGE_H = PAGE

INK = HexColor("#283B34")
RULE = HexColor("#A99A7B")

# The raven's flights card (path only) shares this sheet; it is drawn by its own build script.
_spec = importlib.util.spec_from_file_location(
    "raven_flights", Path(__file__).resolve().parent / "RavenFlights" / "build_raven_flights_pdf.py")
_raven = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_raven)
RAVEN_W, RAVEN_H = _raven.CARD_W, _raven.CARD_H

pdfmetrics.registerFont(TTFont("NothingYouCouldDo", str(FONT_DIR / "Nothing_You_Could_Do" / "NothingYouCouldDo-Regular.ttf")))

# PC-01: the opening code reads 10 (L'Anse aux Meadows tag) then 21 (the
# second tag), from the Norse crew reaching L'Anse aux Meadows in 1021 CE.
# Liv never filled in the tag's printed "if found" line properly - she
# scrawled the address of wherever she was staying instead, on both tags.
# The street number is the only number on each tag, so it is the code digit.
TAGS = [
    {"hotel": "Vinland Trail Lodge", "street": "10 Skipper's Wharf", "city": "L'Anse aux Meadows, NL"},
    {"hotel": "Hôtel Rollon", "street": "21 avenue Rollo", "city": "Rouen, France"},
]


def draw_bold_script(c, text, x, y, size, color=INK):
    """NothingYouCouldDo has one weight; fake a heavier stroke for emphasis."""
    c.setFont("NothingYouCouldDo", size)
    c.setFillColor(color)
    for dx, dy in ((0, 0), (0.35, 0), (0, 0.35), (0.35, 0.35)):
        c.drawCentredString(x + dx, y + dy, text)


def draw_insert(c, x, y, tag):
    c.saveState()
    c.translate(x, y)
    # No background fill (27 Sept 2026): printed on coloured paper, which supplies the tint
    # and means a slightly-off cut can never show a white edge.
    c.setStrokeColor(RULE)
    c.setLineWidth(0.6)
    c.rect(6, 6, CARD_W - 12, CARD_H - 12, fill=0, stroke=1)

    # Printed manufacturer boilerplate.
    c.setFillColor(INK)
    c.setFont("Helvetica", 10.5)
    c.drawCentredString(CARD_W / 2, CARD_H - 28, "IF FOUND, PLEASE RETURN TO")
    c.setStrokeColor(RULE)
    c.setLineWidth(0.5)
    c.line(CARD_W / 2 - 75, CARD_H - 35, CARD_W / 2 + 75, CARD_H - 35)

    # Handwritten over: she jotted down the hotel she was staying at instead.
    c.setFont("NothingYouCouldDo", 16)
    c.setFillColor(INK)
    c.drawCentredString(CARD_W / 2, CARD_H - 62, tag["hotel"])
    draw_bold_script(c, tag["street"], CARD_W / 2, CARD_H - 90, 19)
    c.setFont("NothingYouCouldDo", 16)
    c.drawCentredString(CARD_W / 2, CARD_H - 117, tag["city"])

    c.restoreState()


def draw_crop_marks(c, x, y, w=CARD_W, h=CARD_H):
    c.saveState()
    c.setStrokeColor(HexColor("#777777"))
    c.setLineWidth(0.35)
    gap, length = 3, 8
    for px in (x, x + w):
        c.line(px, y - gap, px, y - gap - length)
        c.line(px, y + h + gap, px, y + h + gap + length)
    for py in (y, y + h):
        c.line(x - gap, py, x - gap - length, py)
        c.line(x + w + gap, py, x + w + gap + length, py)
    c.restoreState()


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUT), pagesize=PAGE, pageCompression=1)
    c.setTitle("Luggage tag inserts and raven's flights card")
    c.setAuthor("Escape Backpack")

    # One centred column: tag, tag, then the raven card, all on US Letter portrait.
    gap = 36
    block_h = 2 * CARD_H + RAVEN_H + 2 * gap
    top = (PAGE_H + block_h) / 2
    x = (PAGE_W - CARD_W) / 2
    ys = [top - CARD_H, top - 2 * CARD_H - gap]
    for tag, y in zip(TAGS, ys):
        draw_insert(c, x, y, tag)
        draw_crop_marks(c, x, y)
    y = ys[1]

    rx, ry = (PAGE_W - RAVEN_W) / 2, y - gap - RAVEN_H
    c.saveState()
    c.translate(rx, ry)
    _raven.draw_card(c)
    c.restoreState()
    draw_crop_marks(c, rx, ry, RAVEN_W, RAVEN_H)

    c.showPage()
    c.save()
    print(OUT)


if __name__ == "__main__":
    main()
