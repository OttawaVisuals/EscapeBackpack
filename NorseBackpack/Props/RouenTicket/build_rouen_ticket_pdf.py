"""Build the Musee Ducal de Rouen admission ticket (PZ-15, concept stage).

Unlike the L'Anse ticket (Props/MuseumTicket), there is no single baked full-bleed front
image here -- Codex supplied a standalone castle line icon (TravelMap/Art/
Rollo_Chateau_Robert_Le_Diable_Line_v1.png, black ink, true alpha), so both faces are drawn
with ReportLab and the castle icon is recoloured to the shared ink green at draw time.

Back carries the steward's word list: two independently-shuffled columns (Saxon words
numbered, Norman words lettered) that a solver matches word-to-word. The tag on each of the
six real answer words is fixed by the map mechanism (PZ-15 / build_trail_maps_pdf.py
ROLLO_WORDLOCK_ART) -- letter is the target grid column (A-I only), number is the target
grid row (1-11 only) -- while the other nine words carry arbitrary tags, some of which
deliberately spill outside those ranges as camouflage, the same trick PZ-12's A-Z index uses.

Source: TravelMap/Art/Rollo_Chateau_Robert_Le_Diable_Line_v1.png
Output: output/pdf/Rouen_Ticket_Print.pdf, Rouen_Ticket_Letter_Print.pdf
"""

from pathlib import Path

from PIL import Image
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import portrait
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
FONT_DIR = ROOT / "Fonts"
OUT = ROOT / "output" / "pdf" / "Rouen_Ticket_Print.pdf"
OUT_LETTER = ROOT / "output" / "pdf" / "Rouen_Ticket_Letter_Print.pdf"
CASTLE_SOURCE = ROOT / "NorseBackpack" / "TravelMap" / "Art" / "Rollo_Chateau_Robert_Le_Diable_Line_v1.png"

# 2 x 3 in portrait -- smaller than L'Anse's 2 x 5.5 in (PZ-12 found that ticket's own dead
# space once the real front art pinned its size; this one starts from the shorter proportion).
PAGE = portrait((2 * 72, 3 * 72))
W, H = PAGE
LETTER = (8.5 * 72, 11 * 72)

PAPER = HexColor("#EFE3C4")
ZEBRA = HexColor("#E7DCC0")
INK = HexColor("#283B34")
INK_RGB = (0x28, 0x3B, 0x34)
RUST = HexColor("#B56A2A")
RULE = HexColor("#A99A7B")
CREAM = HexColor("#F4EEDD")

pdfmetrics.registerFont(TTFont("CinzelExtraBold", str(FONT_DIR / "Cinzel" / "static" / "Cinzel-ExtraBold.ttf")))
pdfmetrics.registerFont(TTFont("CinzelBold", str(FONT_DIR / "Cinzel" / "static" / "Cinzel-Bold.ttf")))

# Saxon word, its printed order on the back, and its number tag (1-15). Six of these numbers
# are load-bearing (2, 3, 6, 7, 9, 10 -- the target grid ROWS for cow, hen, fight, folk, inn
# and woodland); the rest are camouflage, four of them (12-15) deliberately past row 11, the
# map's last row, so they can never resolve to a real square.
SAXON = [
    ("sheep", 1),
    ("fight", 6),
    ("deer", 4),
    ("cow", 2),
    ("inn", 9),
    ("fire", 5),
    ("hen", 3),
    ("board", 8),
    ("woodland", 10),
    ("sight", 11),
    ("folk", 7),
    ("freedom", 12),
    ("snake", 13),
    ("flee", 14),
    ("gather", 15),
]
assert len(SAXON) == 15

# Norman word, its printed order, and its letter tag (A-O). Six are load-bearing (A, B, D, E,
# F, I -- the target grid COLUMNS for poultry, tavern, beef, forest, people and combat); the
# rest are camouflage, six of them (J-O) past column I, the map's last column.
NORMAN = [
    ("mutton", "C"),
    ("combat", "I"),
    ("venison", "G"),
    ("beef", "D"),
    ("flame", "H"),
    ("poultry", "A"),
    ("table", "J"),
    ("tavern", "B"),
    ("vision", "K"),
    ("forest", "E"),
    ("liberty", "L"),
    ("people", "F"),
    ("serpent", "M"),
    ("escape", "N"),
    ("assemble", "O"),
]
assert len(NORMAN) == 15


def load_castle_ink() -> Image.Image:
    """Recolour the black castle line icon to the shared ink green, in memory."""
    source = Image.open(CASTLE_SOURCE).convert("RGBA")
    alpha = source.getchannel("A")
    tinted = Image.new("RGBA", source.size, INK_RGB + (255,))
    tinted.putalpha(alpha)
    return tinted


def draw_front_card(c, castle, x=0, y=0):
    c.saveState()
    c.translate(x, y)

    c.setFillColor(PAPER)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setStrokeColor(RULE)
    c.setLineWidth(0.7)
    c.rect(6, 6, W - 12, H - 12, fill=0, stroke=1)

    # Header: bilingual, matching a real regional French museum's tourist ticket.
    c.setFillColor(INK)
    c.setFont("CinzelExtraBold", 14.5)
    c.drawCentredString(W / 2, H - 26, "MUSEE DUCAL")
    c.drawCentredString(W / 2, H - 41, "DE ROUEN")
    c.setStrokeColor(INK)
    c.setLineWidth(1.0)
    c.line(16, H - 48, W - 16, H - 48)
    c.setFillColor(RUST)
    c.setFont("Helvetica-Bold", 6.6)
    c.drawCentredString(W / 2, H - 58, "THE DUCAL MUSEUM")

    # Castle icon, centred in the remaining body.
    iw, ih = castle.size
    box_w, box_h = W - 28, H - 100
    scale = min(box_w / iw, box_h / ih)
    dw, dh = iw * scale, ih * scale
    reader = ImageReader(castle)
    c.drawImage(
        reader,
        (W - dw) / 2,
        44 + (box_h - dh) / 2,
        dw,
        dh,
        mask="auto",
    )

    # Footer: admission line + stub, matching the L'Anse ticket's front convention.
    c.setStrokeColor(RULE)
    c.setLineWidth(0.6)
    c.line(16, 34, W - 16, 34)
    c.setFillColor(INK)
    c.setFont("CinzelBold", 8.2)
    c.drawCentredString(W / 2, 21, "GENERAL ADMISSION")
    c.setFillColor(HexColor("#59635D"))
    c.setFont("Helvetica", 5.6)
    c.drawCentredString(W / 2, 10, "No. 0163")

    c.restoreState()


def draw_back_card(c, x=0, y=0):
    c.saveState()
    c.translate(x, y)

    c.setFillColor(PAPER)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    header_h = 46
    c.setFillColor(INK)
    c.rect(0, H - header_h, W, header_h, fill=1, stroke=0)
    c.setFillColor(CREAM)
    c.setFont("CinzelExtraBold", 10.5)
    c.drawCentredString(W / 2, H - 18, "WORD GALLERY")
    c.setStrokeColor(RUST)
    c.setLineWidth(1.0)
    c.line(14, H - 25, W - 14, H - 25)
    c.setFillColor(RUST)
    c.setFont("Helvetica-Bold", 4.6)
    c.drawCentredString(W / 2, H - 34, "PEASANT SPEECH, NORMAN FRENCH")
    c.setFillColor(CREAM)
    c.setFont("Helvetica", 4.6)
    c.drawCentredString(W / 2, H - 42, "MATCH EACH OLD WORD TO ITS NEW ONE")

    c.setStrokeColor(RULE)
    c.setLineWidth(0.7)
    c.rect(6, 6, W - 12, H - 12, fill=0, stroke=1)

    col_top = H - header_h - 6
    footer_h = 14
    col_bottom = footer_h + 6
    row_h = (col_top - col_bottom) / len(SAXON)

    mid = W / 2
    left_x = 10
    left_tag_x = left_x
    left_word_x = left_x + 11
    right_x = W - 10
    right_tag_x = right_x
    right_word_x = right_x - 11

    for i, (word, num) in enumerate(SAXON):
        row_top = col_top - i * row_h
        row_bottom = row_top - row_h
        if i % 2 == 1:
            c.setFillColor(ZEBRA)
            c.rect(6, row_bottom, mid - 6, row_h, fill=1, stroke=0)
        baseline = row_bottom + row_h * 0.3
        c.setFillColor(RUST)
        c.setFont("Helvetica-Bold", 5.6)
        c.drawString(left_tag_x, baseline, str(num))
        c.setFillColor(INK)
        c.setFont("Helvetica", 5.8)
        c.drawString(left_word_x, baseline, word)

    for i, (word, letter) in enumerate(NORMAN):
        row_top = col_top - i * row_h
        row_bottom = row_top - row_h
        if i % 2 == 1:
            c.setFillColor(ZEBRA)
            c.rect(mid, row_bottom, W - 6 - mid, row_h, fill=1, stroke=0)
        baseline = row_bottom + row_h * 0.3
        c.setFillColor(RUST)
        c.setFont("Helvetica-Bold", 5.6)
        c.drawRightString(right_tag_x, baseline, letter)
        c.setFillColor(INK)
        c.setFont("Helvetica", 5.8)
        c.drawRightString(right_word_x, baseline, word)

    c.setStrokeColor(RULE)
    c.setLineWidth(0.8)
    c.line(mid, col_bottom - 2, mid, col_top + 2)

    c.setStrokeColor(RULE)
    c.setLineWidth(0.5)
    c.line(left_x, footer_h, right_x, footer_h)
    c.setFillColor(HexColor("#59635D"))
    c.setFont("Helvetica", 4.6)
    c.drawCentredString(W / 2, 7, "MUSEE DUCAL DE ROUEN")

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


def build_single(castle):
    c = canvas.Canvas(str(OUT), pagesize=PAGE, pageCompression=1)
    c.setTitle("Musee Ducal de Rouen - admission ticket")
    c.setAuthor("Escape Backpack")
    draw_front_card(c, castle)
    c.showPage()
    draw_back_card(c)
    c.showPage()
    c.save()


def build_letter(castle):
    letter_w, letter_h = LETTER
    x = (letter_w - W) / 2
    y = (letter_h - H) / 2
    c = canvas.Canvas(str(OUT_LETTER), pagesize=LETTER, pageCompression=1)
    c.setTitle("Two-up Rouen ticket print sheet - front and back")
    c.setAuthor("Escape Backpack")
    draw_front_card(c, castle, x, y)
    draw_crop_marks(c, x, y)
    c.showPage()
    draw_back_card(c, x, y)
    draw_crop_marks(c, x, y)
    c.showPage()
    c.save()


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    castle = load_castle_ink()
    build_single(castle)
    build_letter(castle)
    print(OUT)
    print(OUT_LETTER)


if __name__ == "__main__":
    main()
