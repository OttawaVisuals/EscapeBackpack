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
STAMP = ROOT / "NorseBackpack" / "Postcards" / "Stamps" / "Stamp_Leif_Longship_v1.png"
FONT_DIR = ROOT / "Fonts"

PAGE = landscape((3.5 * 72, 5 * 72))
W, H = PAGE
LETTER = (8.5 * 72, 11 * 72)
PAPER = HexColor("#EFE3C4")
NAVY = HexColor("#12343C")
TEAL = HexColor("#2F7775")
RULE = HexColor("#A99A7B")
INK = HexColor("#283B34")
FUNFACT = HexColor("#B56A2A")

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

    left, right = 20, W - 20
    divider = 184
    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", 6.5)
    c.drawCentredString(W / 2, H - 20, "POST CARD")
    c.setStrokeColor(RULE)
    c.line(divider, 24, divider, H - 30)

    paragraphs = [
        "Hello, nephew!",
        "As you know, I've spent the last two years travelling and exploring our family history. I've discovered so many fascinating things - and perhaps even a small treasure!",
        "Along with this postcard, you should have received the travel bag I carried everywhere during my journey.",
        "I know how much you love mysteries and puzzles, so I've prepared an adventure for you. There's a surprise locked inside the bag. To open it, you'll need to follow my travels and solve the puzzles I've left behind.",
        "This postcard comes from the first stop on my journey: L'Anse aux Meadows. It should help you get started.",
    ]
    c.setFillColor(INK)
    font, size, leading = "NothingYouCouldDo", 7.7, 8.6
    y = H - 36
    for paragraph in paragraphs:
        for line in wrap_text(paragraph, font, size, divider - left - 12):
            c.setFont(font, size)
            c.drawString(left, y, line)
            y -= leading
        y -= 1.8

    c.setFont("NothingYouCouldDo", 8)
    c.drawString(left, y, "With love,")
    c.drawString(left, y - 9, "Aunt Liv")

    # The agreed route stamp, shown at approximately 20 x 24 mm.
    stamp_w, stamp_h = 20 / 25.4 * 72, 24 / 25.4 * 72
    stamp_x, stamp_y = right - stamp_w, H - 35 - stamp_h
    c.drawImage(
        ImageReader(str(STAMP)),
        stamp_x,
        stamp_y,
        stamp_w,
        stamp_h,
        preserveAspectRatio=True,
        anchor="c",
        mask="auto",
    )

    # Place and date form the universal postmark. The day-of-month is
    # underlined: it is the first two digits of the opening puzzle's code.
    postmark_x, postmark_y = stamp_x - 5, H - 64
    c.setStrokeColor(TEAL)
    c.setLineWidth(0.8)
    c.circle(postmark_x, postmark_y, 23, fill=0, stroke=1)
    c.circle(postmark_x, postmark_y, 19.5, fill=0, stroke=1)
    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", 4.8)
    c.drawCentredString(postmark_x, postmark_y + 7, "L'ANSE AUX")
    c.drawCentredString(postmark_x, postmark_y + 1, "MEADOWS")
    date_font, date_size = "Helvetica-Bold", 4.2
    day_text, date_text = "07", "07 JUL"
    c.setFont(date_font, date_size)
    c.drawCentredString(postmark_x, postmark_y - 7, date_text)
    full_width = pdfmetrics.stringWidth(date_text, date_font, date_size)
    day_width = pdfmetrics.stringWidth(day_text, date_font, date_size)
    underline_x = postmark_x - full_width / 2
    c.setLineWidth(0.5)
    c.line(underline_x, postmark_y - 9, underline_x + day_width, postmark_y - 9)
    for offset in (-7, -2, 3, 8):
        c.line(postmark_x + 23, postmark_y + offset, right, postmark_y + offset)

    # Address — shrunk to make room for the Fun Fact block below it.
    address_x = divider + 17
    box_right = right + 5
    c.setStrokeColor(RULE)
    c.setLineWidth(0.6)
    c.rect(divider + 11, 81, box_right - (divider + 11), 66, fill=0, stroke=1)

    address_y = H - 124
    c.setFillColor(HexColor("#59635D"))
    c.setFont("Helvetica-Bold", 5.2)
    c.drawString(address_x, address_y + 12, "TO")
    c.setFillColor(INK)
    c.setFont("NothingYouCouldDo", 8)
    address_lines = [
        "John Ericson",
        "24 Longship Way",
        "Ottawa ON  K1L 1S1",
        "Canada",
    ]
    for index, line in enumerate(address_lines):
        line_y = address_y - index * 13
        c.drawString(address_x, line_y, line)
        c.setStrokeColor(HexColor("#C0B291"))
        c.setLineWidth(0.4)
        c.line(address_x, line_y - 3, right, line_y - 3)

    # Fun Fact — typed, real trivia, stacked under the address.
    funfact_top, funfact_bottom = 76, 28
    c.setStrokeColor(FUNFACT)
    c.setLineWidth(0.6)
    c.rect(divider + 11, funfact_bottom, box_right - (divider + 11), funfact_top - funfact_bottom, fill=0, stroke=1)
    c.setFillColor(FUNFACT)
    c.setFont("Helvetica-Bold", 6)
    c.drawString(address_x, funfact_top - 9, "FUN FACT")
    c.setFillColor(INK)
    fact_font, fact_size, fact_leading = "Helvetica", 5, 5.8
    fact_text = (
        "L'Anse aux Meadows turned up butternuts and worked butternut wood, though "
        "the nearest wild butternut trees grow hundreds of kilometres south, near "
        "the St. Lawrence. Read as evidence its people ranged well beyond it, into "
        "the wider “Vinland” the sagas describe."
    )
    fact_y = funfact_top - 20
    for line in wrap_text(fact_text, fact_font, fact_size, box_right - address_x - 6):
        c.setFont(fact_font, fact_size)
        c.drawString(address_x, fact_y, line)
        fact_y -= fact_leading

    credit_top = 16
    c.setStrokeColor(RULE)
    c.line(left, credit_top + 7, right, credit_top + 7)
    c.setFillColor(HexColor("#59635D"))
    c.setFont("Helvetica", 3.2)
    credit_lines = [
        'Image adaptation: "L\'Anse aux Meadows, The Meeting of Two Worlds" - D. Gordon E. Robertson, CC BY-SA 3.0.',
        "Source and full attribution: Postcards/Image_Credits.html",
    ]
    for index, line in enumerate(credit_lines):
        c.drawString(left, credit_top - index * 4, line)
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
