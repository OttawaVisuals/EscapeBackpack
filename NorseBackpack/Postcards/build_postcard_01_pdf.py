from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "output" / "pdf" / "Postcard_01_LAnse_Print.pdf"
OUT_LETTER = ROOT / "output" / "pdf" / "Postcard_01_LAnse_Letter_Print.pdf"
ART = ROOT / "NorseBackpack" / "Postcards" / "Postcard_01_LAnse_Illustration_v2.png"
FONT_DIR = ROOT / "Fonts"

PAGE = landscape((4 * 72, 6 * 72))
W, H = PAGE
LETTER = (8.5 * 72, 11 * 72)
PAPER = HexColor("#EFE3C4")
NAVY = HexColor("#12343C")
TEAL = HexColor("#2F7775")
RULE = HexColor("#A99A7B")
INK = HexColor("#283B34")

pdfmetrics.registerFont(TTFont("CinzelExtraBold", str(FONT_DIR / "Cinzel" / "static" / "Cinzel-ExtraBold.ttf")))
pdfmetrics.registerFont(TTFont("NothingYouCouldDo", str(FONT_DIR / "Nothing_You_Could_Do" / "NothingYouCouldDo-Regular.ttf")))


def wrap_text(text, font, size, width):
    words = text.split()
    lines, current = [], ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if pdfmetrics.stringWidth(candidate, font, size) <= width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_front_card(c, x=0, y=0):
    c.saveState()
    c.translate(x, y)
    c.drawImage(ImageReader(str(ART)), 0, 0, W, H, preserveAspectRatio=False, mask="auto")
    c.setFillColor(PAPER)
    c.setFont("CinzelExtraBold", 25)
    c.drawCentredString(W / 2, 45, "L'ANSE AUX MEADOWS")
    c.setFont("Helvetica-Bold", 7.2)
    c.drawCentredString(W / 2, 27, "NEWFOUNDLAND AND LABRADOR")
    c.restoreState()


def draw_back_card(c, x=0, y=0):
    c.saveState()
    c.translate(x, y)
    c.setFillColor(PAPER)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setStrokeColor(RULE)
    c.setLineWidth(0.7)
    c.rect(10, 10, W - 20, H - 20, fill=0, stroke=1)

    left, right = 27, W - 27
    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", 7.8)
    c.drawString(left, H - 28, "FIRST STOP  -  L'ANSE AUX MEADOWS")
    c.setStrokeColor(RULE)
    c.line(left, H - 35, right, H - 35)

    paragraphs = [
        "Hello, nephew!",
        "As you know, I've spent the last two years travelling and exploring our family history. I've discovered so many fascinating things - and perhaps even a small treasure!",
        "Along with this postcard, you should have received the travel bag I carried everywhere during my journey.",
        "I know how much you love mysteries and puzzles, so I've prepared an adventure for you. There's a surprise locked inside the bag. To open it, you'll need to follow my travels and solve the puzzles I've left behind.",
        "This postcard comes from the first stop on my journey: L'Anse aux Meadows. It should help you get started.",
    ]
    c.setFillColor(INK)
    font, size, leading = "NothingYouCouldDo", 11.2, 13
    y = H - 53
    for paragraph in paragraphs:
        for line in wrap_text(paragraph, font, size, right - left):
            c.setFont(font, size)
            c.drawString(left, y, line)
            y -= leading
        y -= 3

    c.setFont("NothingYouCouldDo", 11.2)
    c.drawString(left, y, "With love,")
    c.drawString(left, y - 13, "Aunt Liv")

    credit_top = 45
    c.setStrokeColor(RULE)
    c.line(left, credit_top + 9, right, credit_top + 9)
    c.setFillColor(HexColor("#59635D"))
    c.setFont("Helvetica", 5)
    credit_lines = [
        'Adapted from "L\'Anse aux Meadows, The Meeting of Two Worlds" by D. Gordon E. Robertson, Wikimedia Commons, CC BY-SA 3.0.',
        "Converted into poster style. Source: commons.wikimedia.org/wiki/File:L%27Anse_aux_Meadows,_The_Meeting_of_Two_Worlds.jpg",
        "Licence: creativecommons.org/licenses/by-sa/3.0/  |  Adapted artwork: CC BY-SA 3.0",
    ]
    for index, line in enumerate(credit_lines):
        c.drawString(left, credit_top - index * 7, line)
    c.restoreState()


def draw_crop_marks(c, x, y):
    c.saveState()
    c.setStrokeColor(HexColor("#777777"))
    c.setLineWidth(0.35)
    gap, length = 3, 10
    for px in (x, x + W):
        c.line(px, y - gap, px, y - gap - length)
        c.line(px, y + H + gap, px, y + H + gap + length)
    for py in (y, y + H):
        c.line(x - gap, py, x - gap - length, py)
        c.line(x + W + gap, py, x + W + gap + length, py)
    c.restoreState()


def build_single():
    c = canvas.Canvas(str(OUT), pagesize=PAGE, pageCompression=1)
    c.setTitle("Aunt Liv's Postcard 01 - L'Anse aux Meadows")
    c.setAuthor("Escape Backpack")
    draw_front_card(c)
    c.showPage()
    draw_back_card(c)
    c.showPage()
    c.save()


def build_letter():
    letter_w, letter_h = LETTER
    x = (letter_w - W) / 2
    gap = 18
    group_h = 2 * H + gap
    lower_y = (letter_h - group_h) / 2
    positions = [(x, lower_y + H + gap), (x, lower_y)]
    c = canvas.Canvas(str(OUT_LETTER), pagesize=LETTER, pageCompression=1)
    c.setTitle("Two-up Postcard 01 print sheet - L'Anse aux Meadows")
    c.setAuthor("Escape Backpack")
    for card_x, card_y in positions:
        draw_front_card(c, card_x, card_y)
        draw_crop_marks(c, card_x, card_y)
    c.showPage()
    for card_x, card_y in positions:
        draw_back_card(c, card_x, card_y)
        draw_crop_marks(c, card_x, card_y)
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
