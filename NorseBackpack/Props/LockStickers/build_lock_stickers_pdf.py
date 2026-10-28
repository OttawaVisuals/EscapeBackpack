"""Lock number stickers: approved longship, numbered 1-13 in solve order.

Chosen 8 Oct 2026: longship concept C, replacing the earlier round shield.
Built-in ImageGen removed the sample 6; numbers are typeset on the blank sail.
Two full sets on one
US Letter sheet, so a mis-stuck or torn sticker has a spare. Print on sticker paper at 100%.

Output: NorseBackpack/Print/_pdf_source/Lock_Stickers_Print.pdf
"""
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "NorseBackpack" / "Print" / "_pdf_source" / "Lock_Stickers_Print.pdf"
# Plain bold sans numerals: Cinzel's "11" read as "ll" at sticker size (8 Oct 2026).
# Helvetica-Bold matches the Arial Bold lettering on the medallion back.
NUMBER_FONT = "Helvetica-Bold"

CM = 72 / 2.54
PAGE_W, PAGE_H = 8.5 * 72, 11 * 72
LOCKS = 13
SETS = 2
DIAMETER = 1.3 * CM          # artwork width, excluding its white image margins
GAP = 0.45 * CM
COLS = 9

INK = HexColor("#283B34")
ART = Path(__file__).with_name("Longship_Blank_Sail.png")
# Normalized artwork bounds in the unchanged square source, measured visually.
ART_LEFT, ART_TOP, ART_RIGHT, ART_BOTTOM = 0.069, 0.114, 0.908, 0.904


def longship(c, cx, cy, number):
    """Place the approved artwork and fit an upright number inside its sail."""
    side = DIAMETER / (ART_RIGHT - ART_LEFT)
    height = side * (ART_BOTTOM - ART_TOP)
    left = cx - DIAMETER / 2 - ART_LEFT * side
    bottom = cy - height / 2 - (1 - ART_BOTTOM) * side
    c.saveState()
    c.drawImage(str(ART), left, bottom, side, side)
    text = str(number)
    size = min(side * 0.515,
               side * 0.45 / pdfmetrics.stringWidth(text, NUMBER_FONT, 1))
    cap_height = pdfmetrics.getAscent(NUMBER_FONT) / 1000 * size
    c.setFillColor(INK)
    c.setFont(NUMBER_FONT, size)
    c.drawCentredString(left + side * 0.5,
                       bottom + side * 0.55 - cap_height / 2, text)
    c.restoreState()


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUT), pagesize=(PAGE_W, PAGE_H), pageCompression=1)
    c.setTitle("Lock number stickers")
    c.setAuthor("Escape Backpack")
    c.setFillColor(INK)
    c.setFont("Helvetica", 8)
    top = PAGE_H - 0.75 * 72
    c.drawString(0.75 * 72, top, "Norse backpack · lock stickers 1-13, two sets · print at 100% (each longship 1.3 cm wide)")
    step = DIAMETER + GAP
    grid_w = COLS * DIAMETER + (COLS - 1) * GAP
    x0 = (PAGE_W - grid_w) / 2 + DIAMETER / 2
    y = top - 0.5 * 72 - DIAMETER / 2
    for _ in range(SETS):
        for n in range(1, LOCKS + 1):
            col = (n - 1) % COLS
            if n > 1 and col == 0:
                y -= step
            longship(c, x0 + col * step, y, n)
        y -= step + GAP
    c.showPage()
    c.save()
    print(OUT)


if __name__ == "__main__":
    main()
