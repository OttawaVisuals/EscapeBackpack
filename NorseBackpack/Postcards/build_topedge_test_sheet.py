"""Print-at-true-size test sheet for the Card 02 / Card 03 top-edge digit registration.

Crops just the top strip of each front illustration (where the hidden 1576 halves live)
and lays them out on a PDF sized so printing at 100% / Actual Size reproduces the same
physical scale as the final card (1500x1050 px over a 5 x 3.5 in card = 300 dpi).
Not the whole card -- just enough to test cutting and aligning the top edge.
"""

from pathlib import Path

from reportlab.lib.colors import HexColor, black
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

ROOT = Path(__file__).resolve().parents[2]
POSTCARDS = ROOT / "NorseBackpack" / "Postcards"
OUT = ROOT / "output" / "pdf" / "Postcard_02_03_TopEdge_Test.pdf"

DPI = 300.0  # PC-13: 1500x1050 art over a 5 x 3.5 in card
STRIP_PX = 300  # crop height in source pixels; digits sit in roughly the first 30-40 px
STRIP_W_IN = 1500 / DPI
STRIP_H_IN = STRIP_PX / DPI

MARGIN = 0.5 * inch
LABEL_H = 0.35 * inch
GAP = 0.4 * inch
RULER_H = 0.3 * inch
RULER_NOTE_H = 0.3 * inch
RIGHT_LABEL_W = 1.4 * inch

PAGE_W = STRIP_W_IN * inch + MARGIN + RIGHT_LABEL_W
PAGE_H = 2 * (LABEL_H + STRIP_H_IN * inch) + GAP + RULER_H + RULER_NOTE_H + 2 * MARGIN

CARDS = [
    ("Postcard_02_Battle_Harbour_Front.png", "CARD 02 · Battle Harbour — as printed, right side up"),
    ("Postcard_03_Baffin_Island_Front.png", "CARD 03 · Baffin Island — as printed, right side up"),
]


def crop_top_strip(src, dest, height_px):
    from PIL import Image

    im = Image.open(src)
    if im.size != (1500, 1050):
        raise ValueError(f"Expected 1500x1050 front for PC-13, got {im.size}: {src}")
    im.crop((0, 0, im.width, height_px)).save(dest)


def build():
    tmp_dir = POSTCARDS / "_topedge_test_tmp"
    tmp_dir.mkdir(exist_ok=True)
    crops = []
    for filename, _ in CARDS:
        src = POSTCARDS / filename
        dest = tmp_dir / f"strip_{filename}"
        crop_top_strip(src, dest, STRIP_PX)
        crops.append(dest)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUT), pagesize=(PAGE_W, PAGE_H))
    c.setTitle("Card 02/03 top-edge registration test -- print at 100%")

    c.setFillColor(black)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(MARGIN, PAGE_H - MARGIN + 2, "PRINT AT 100% / ACTUAL SIZE -- do not use “fit to page”")

    y = PAGE_H - MARGIN - 12
    for (filename, label), crop in zip(CARDS, crops):
        y -= LABEL_H
        c.setFont("Helvetica-Bold", 8)
        c.drawString(MARGIN, y + 6, label)
        strip_h = STRIP_H_IN * inch
        y -= strip_h
        c.drawImage(ImageReader(str(crop)), MARGIN, y, STRIP_W_IN * inch, strip_h)
        # The true top edge of the finished card is the top pixel row of this crop.
        c.setStrokeColor(HexColor("#c0392b"))
        c.setLineWidth(1)
        c.setDash(4, 2)
        c.line(MARGIN, y + strip_h, MARGIN + STRIP_W_IN * inch, y + strip_h)
        c.setFont("Helvetica", 6.5)
        c.setFillColor(HexColor("#c0392b"))
        c.drawString(MARGIN + STRIP_W_IN * inch + 4, y + strip_h - 3, "cut here = true top edge")
        c.setFillColor(black)
        y -= GAP

    # A measured reference line so a wrongly-scaled print is caught immediately.
    y -= RULER_H
    ruler_len_in = 6.0
    c.setStrokeColor(black)
    c.setLineWidth(1)
    c.line(MARGIN, y + RULER_H / 2, MARGIN + ruler_len_in * inch, y + RULER_H / 2)
    for i in range(int(ruler_len_in) + 1):
        x = MARGIN + i * inch
        c.line(x, y + RULER_H / 2 - 4, x, y + RULER_H / 2 + 4)
        c.setFont("Helvetica", 6)
        c.drawCentredString(x, y + RULER_H / 2 + 6, str(i))
    c.setFont("Helvetica-Bold", 7)
    c.drawString(MARGIN, y - 14, f"This line must measure exactly {ruler_len_in:.2f} in ({ruler_len_in*25.4:.1f} mm) after printing. If it doesn't, your printer rescaled the page.")

    c.showPage()
    c.save()

    for f in tmp_dir.glob("*"):
        f.unlink()
    tmp_dir.rmdir()

    print(OUT)


if __name__ == "__main__":
    build()
