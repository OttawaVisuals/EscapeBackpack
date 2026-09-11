from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "output" / "pdf" / "Luggage_Tag_Inserts_Print.pdf"
FONT_DIR = ROOT / "Fonts"

# Matches the Lewis N. Clark luggage tag's business-card insert slot.
CARD_W, CARD_H = 3.5 * 72, 2 * 72
PAGE = landscape((8.5 * 72, 11 * 72))
PAGE_W, PAGE_H = PAGE

PAPER = HexColor("#EFE3C4")
INK = HexColor("#283B34")
RULE = HexColor("#A99A7B")

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
    c.setFillColor(PAPER)
    c.rect(0, 0, CARD_W, CARD_H, fill=1, stroke=0)
    c.setStrokeColor(RULE)
    c.setLineWidth(0.6)
    c.rect(6, 6, CARD_W - 12, CARD_H - 12, fill=0, stroke=1)

    # Printed manufacturer boilerplate.
    c.setFillColor(INK)
    c.setFont("Helvetica", 8.5)
    c.drawCentredString(CARD_W / 2, CARD_H - 24, "IF FOUND, PLEASE RETURN TO")
    c.setStrokeColor(RULE)
    c.setLineWidth(0.5)
    c.line(CARD_W / 2 - 60, CARD_H - 30, CARD_W / 2 + 60, CARD_H - 30)

    # Handwritten over: she jotted down the hotel she was staying at instead.
    c.setFont("NothingYouCouldDo", 12)
    c.setFillColor(INK)
    c.drawCentredString(CARD_W / 2, CARD_H - 52, tag["hotel"])
    draw_bold_script(c, tag["street"], CARD_W / 2, CARD_H - 74, 14)
    c.setFont("NothingYouCouldDo", 12)
    c.drawCentredString(CARD_W / 2, CARD_H - 94, tag["city"])

    c.restoreState()


def draw_crop_marks(c, x, y):
    c.saveState()
    c.setStrokeColor(HexColor("#777777"))
    c.setLineWidth(0.35)
    gap, length = 3, 8
    for px in (x, x + CARD_W):
        c.line(px, y - gap, px, y - gap - length)
        c.line(px, y + CARD_H + gap, px, y + CARD_H + gap + length)
    for py in (y, y + CARD_H):
        c.line(x - gap, py, x - gap - length, py)
        c.line(x + CARD_W + gap, py, x + CARD_W + gap + length, py)
    c.restoreState()


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUT), pagesize=PAGE, pageCompression=1)
    c.setTitle("Luggage tag inserts - opening puzzle")
    c.setAuthor("Escape Backpack")

    gap = 30
    total_w = len(TAGS) * CARD_W + (len(TAGS) - 1) * gap
    start_x = (PAGE_W - total_w) / 2
    y = (PAGE_H - CARD_H) / 2

    for index, tag in enumerate(TAGS):
        x = start_x + index * (CARD_W + gap)
        draw_insert(c, x, y, tag)
        draw_crop_marks(c, x, y)

    c.showPage()
    c.save()
    print(OUT)


if __name__ == "__main__":
    main()
