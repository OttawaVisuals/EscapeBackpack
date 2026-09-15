from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import portrait
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "output" / "pdf" / "Museum_Ticket_Print.pdf"
OUT_LETTER = ROOT / "output" / "pdf" / "Museum_Ticket_Letter_Print.pdf"
FRONT = Path(__file__).resolve().parent / "Museum_Ticket_Front_300dpi_v3_transparent.png"
FONT_DIR = ROOT / "Fonts"

# Matches the front artwork: a 2 x 5.5 in portrait admission ticket (PZ-12).
PAGE = portrait((2 * 72, 5.5 * 72))
W, H = PAGE
LETTER = (8.5 * 72, 11 * 72)

PAPER = HexColor("#EFE3C4")
ZEBRA = HexColor("#E7DCC0")
INK = HexColor("#283B34")
RUST = HexColor("#B56A2A")
RULE = HexColor("#A99A7B")
CREAM = HexColor("#F4EEDD")

pdfmetrics.registerFont(TTFont("CinzelExtraBold", str(FONT_DIR / "Cinzel" / "static" / "Cinzel-ExtraBold.ttf")))
pdfmetrics.registerFont(TTFont("CinzelBold", str(FONT_DIR / "Cinzel" / "static" / "Cinzel-Bold.ttf")))

# PZ-12: the decided A-Z visitor index. Only 13 letters (A B C D E F H L N O R S W)
# are load-bearing for the current beast set (BEAR WOLF SEAL ORCA LOON HARE DEER);
# the rest exist purely as camouflage so the list doesn't read as suspiciously short.
INDEX = [
    ("A", "Arrival Hall", 1),
    ("B", "Boat Shed", 3),
    ("C", "Compass Room", 3),
    ("D", "Dye Vats", 4),
    ("E", "Excavation Pit", 2),
    ("F", "Forge", 5),
    ("G", "Great Hall", 8),
    ("H", "Hearth House", 5),
    ("I", "Iron Bog", 2),
    ("J", "Jarl's Quarters", 7),
    ("K", "Keel Yard", 3),
    ("L", "Longhouse", 6),
    ("M", "Midden", 4),
    ("N", "Navigation Room", 3),
    ("O", "Ocean Gallery", 8),
    ("P", "Palisade", 9),
    ("Q", "Quay", 3),
    ("R", "Rune Stone", 2),
    ("S", "Sod House", 4),
    ("T", "Tool Shed", 5),
    ("U", "Upper Meadow", 9),
    ("V", "Visitor Centre", 1),
    ("W", "Weaving Hut", 4),
    ("X", "X Marks the Site", 2),
    ("Y", "Yarn Room", 4),
    ("Z", "Zooarchaeology Lab", 9),
]
assert len(INDEX) == 26

MARGIN = 9
HEADER_H = 78


def draw_front_card(c, x=0, y=0):
    c.saveState()
    c.translate(x, y)
    front = ImageReader(str(FRONT))
    fw, fh = front.getSize()
    # PZ-12: the front is a fixed 600x1650px (2x5.5in @300dpi) ImageGen asset.
    # Fail loud rather than silently stretching a differently-sized file onto the page.
    if (fw, fh) != (600, 1650):
        raise ValueError(
            f"Museum_Ticket_Front_300dpi_v2.png is {fw}x{fh}, expected 600x1650 "
            f"(PZ-12, 2x5.5in @300dpi). Drawing it here would stretch it to fit the page."
        )
    c.drawImage(front, 0, 0, W, H, preserveAspectRatio=False, mask="auto")
    c.restoreState()


def draw_back_card(c, x=0, y=0):
    c.saveState()
    c.translate(x, y)

    # No background fill below the header: printed on 176 g/m2 cream stock
    # that already matches PAPER, so the card stock itself supplies the tint.

    # Header band, styled to match the front's dark band + rust rule + caption line.
    c.setFillColor(INK)
    c.rect(0, H - HEADER_H, W, HEADER_H, fill=1, stroke=0)
    c.setFillColor(CREAM)
    c.setFont("CinzelExtraBold", 14)
    c.drawCentredString(W / 2, H - 24, "VISITOR")
    c.drawCentredString(W / 2, H - 38, "INDEX")
    c.setStrokeColor(RUST)
    c.setLineWidth(1.1)
    c.line(20, H - 47, W - 20, H - 47)
    c.setFillColor(RUST)
    c.setFont("Helvetica-Bold", 6.5)
    c.drawCentredString(W / 2, H - 58, "GALLERY GUIDE")
    c.setFillColor(CREAM)
    c.setFont("Helvetica", 5.4)
    c.drawCentredString(W / 2, H - 70, "PLEASE RETAIN THIS TICKET")

    # Outer rule, matching the other paper props (luggage tags, postcard backs).
    c.setStrokeColor(RULE)
    c.setLineWidth(0.7)
    c.rect(6, 6, W - 12, H - 12, fill=0, stroke=1)

    # Body: one alphabetical column, room number right-aligned. A single column
    # (not the two originally sketched) is what actually fits a 2in-wide ticket
    # at a legible size once the real front art pinned the physical dimensions.
    footer_h = 16
    list_top = H - HEADER_H - 8
    list_bottom = footer_h + 6
    row_h = (list_top - list_bottom) / len(INDEX)
    left = MARGIN + 6
    right = W - MARGIN - 6
    name_x = left + 13

    for i, (letter, name, number) in enumerate(INDEX):
        row_top = list_top - i * row_h
        row_bottom = row_top - row_h
        if i % 2 == 1:
            c.setFillColor(ZEBRA)
            c.rect(6, row_bottom, W - 12, row_h, fill=1, stroke=0)
        baseline = row_bottom + row_h * 0.32
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 6.6)
        c.drawString(left, baseline, letter)
        c.setFont("Helvetica", 6.2)
        c.drawString(name_x, baseline, name)
        c.setFont("Helvetica-Bold", 6.2)
        c.drawRightString(right, baseline, str(number))

    # Footer, matching the front's small ticket-stub number.
    c.setStrokeColor(RULE)
    c.setLineWidth(0.5)
    c.line(left, footer_h, right, footer_h)
    c.setFillColor(HexColor("#59635D"))
    c.setFont("Helvetica", 5.2)
    c.drawCentredString(W / 2, 7, "No. 084726")

    c.restoreState()


def draw_crop_marks(c, x, y):
    c.saveState()
    c.setStrokeColor(HexColor("#777777"))
    c.setLineWidth(0.35)
    gap, length = 3, 8
    for px in (x, x + W):
        c.line(px, y - gap, px, y - gap - length)
        c.line(px, y + H + gap, px, y + H + gap + length)
    for py in (y, y + H):
        c.line(x - gap, py, x - gap - length, py)
        c.line(x + W + gap, py, x + W + gap + length, py)
    c.restoreState()


def build_single():
    c = canvas.Canvas(str(OUT), pagesize=PAGE, pageCompression=1)
    c.setTitle("Viking Museum of L'Anse aux Meadows - admission ticket")
    c.setAuthor("Escape Backpack")
    draw_front_card(c)
    c.showPage()
    draw_back_card(c)
    c.showPage()
    c.save()


def build_letter():
    letter_w, letter_h = LETTER
    x = (letter_w - W) / 2
    y = (letter_h - H) / 2
    c = canvas.Canvas(str(OUT_LETTER), pagesize=LETTER, pageCompression=1)
    c.setTitle("Two-up Museum ticket print sheet - front and back")
    c.setAuthor("Escape Backpack")
    draw_front_card(c, x, y)
    draw_crop_marks(c, x, y)
    c.showPage()
    draw_back_card(c, x, y)
    draw_crop_marks(c, x, y)
    c.showPage()
    c.save()


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    build_single()
    build_letter()
    print(OUT)
    print(OUT_LETTER)


if __name__ == "__main__":
    main()
