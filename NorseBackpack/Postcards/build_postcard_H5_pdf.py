from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "output" / "pdf" / "Postcard_H5_Sicily_Print.pdf"
OUT_LETTER = ROOT / "output" / "pdf" / "Postcard_H5_Sicily_Letter_Print.pdf"
FRONT = ROOT / "NorseBackpack" / "Postcards" / "Postcard_H5_Sicily_Front.png"
STAMP = ROOT / "NorseBackpack" / "Postcards" / "Stamps" / "Stamp_Harald_Labrys_v2_flat.png"
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
    front = ImageReader(str(FRONT))
    fw, fh = front.getSize()
    # PC-13: same guard as build_postcard_01_pdf.py -- fail loud rather than stretch.
    if (fw, fh) != (1500, 1050):
        raise ValueError(
            f"Postcard_H5_Sicily_Front.png is {fw}x{fh}, expected 1500x1050 (PC-13, "
            f"5x3.5in @300dpi). Drawing it here would stretch it to fit the page."
        )
    c.drawImage(front, 0, 0, W, H, preserveAspectRatio=False, mask="auto")
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

    # Message text approved in chat (PZ-02/PZ-09, 17 Sept 2026). "raven" is drawn underlined
    # below -- that is the whole reading-order clue (PZ-02): spell RAVEN against the relettered
    # columns on Harald's map. No other emphasis or explanation is added on the card itself.
    font, size, leading = "NothingYouCouldDo", 7.7, 8.6
    max_w = divider - left - 12
    y = H - 36

    def draw_paragraph(segments):
        nonlocal y
        # segments: list of (text, underline) pieces that must stay in reading order. Wrapping
        # is done word-by-word across the whole paragraph so an underlined word can fall mid-line.
        words = []
        for text, underline in segments:
            for word in text.split():
                words.append((word, underline))
        line, line_w = [], 0.0
        space_w = pdfmetrics.stringWidth(" ", font, size)
        for word, underline in words:
            word_w = pdfmetrics.stringWidth(word, font, size)
            extra = (space_w if line else 0) + word_w
            if line and line_w + extra > max_w:
                draw_line(line)
                line, line_w = [], 0.0
                extra = word_w
            line.append((word, underline))
            line_w += extra
        if line:
            draw_line(line)
        y -= 1.8

    def draw_line(line):
        nonlocal y
        c.setFont(font, size)
        x = left
        for i, (word, underline) in enumerate(line):
            if i:
                x += pdfmetrics.stringWidth(" ", font, size)
            c.setFillColor(INK)
            c.drawString(x, y, word)
            if underline:
                w = pdfmetrics.stringWidth(word, font, size)
                c.setStrokeColor(INK)
                c.setLineWidth(0.6)
                c.line(x, y - 1.4, x + w, y - 1.4)
            x += pdfmetrics.stringWidth(word, font, size)
        y -= leading

    draw_paragraph([("Aci Castello today.", False)])
    draw_paragraph([("A Norman Castle in Sicily! It's crazy to think how far they travelled!", False)])
    draw_paragraph([
        ("Being a good tourist, I enjoyed a gelato while walking around the ruins. Little "
         "did I know, that is a great way to attract wildlife. A", False),
        ("raven", True),
        ("followed me the whole time!", False),
    ])
    draw_paragraph([("Half convinced it was you, checking up on me.", False)])

    c.setFillColor(INK)
    c.setFont("NothingYouCouldDo", 8)
    c.drawString(left, y, "Love,")
    c.drawString(left, y - 9, "Aunt Liv")

    # Same trail stamp as the other Harald cards -- one stamp per traveller, not per card.
    stamp_w, stamp_h = 20 / 25.4 * 72, 24 / 25.4 * 72
    stamp_x, stamp_y = right - stamp_w, H - 30 - stamp_h
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

    # Postmark: place only. No date drawn -- PC-03/PC-04 are still open, and PZ-08 needs those
    # dates checked against the trail-order constraint before any are printed.
    postmark_x, postmark_y = stamp_x - 5, H - 48
    c.setStrokeColor(TEAL)
    c.setLineWidth(0.8)
    c.circle(postmark_x, postmark_y, 23, fill=0, stroke=1)
    c.circle(postmark_x, postmark_y, 19.5, fill=0, stroke=1)
    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", 4.6)
    c.drawCentredString(postmark_x, postmark_y + 4, "ACI")
    c.drawCentredString(postmark_x, postmark_y - 2, "CASTELLO")
    for offset in (-7, -2, 3, 8):
        c.line(postmark_x + 23, postmark_y + offset, right, postmark_y + offset)

    # Address -- same recipient and layout as the other cards (PC-13 standard).
    address_x = divider + 17
    box_right = right + 5
    rule_right = 278
    c.setStrokeColor(RULE)
    c.setLineWidth(0.6)
    c.rect(divider + 11, 126, box_right - (divider + 11), 62, fill=0, stroke=1)

    address_y = 166
    c.setFillColor(HexColor("#59635D"))
    c.setFont("Helvetica-Bold", 5.8)
    c.drawString(address_x, address_y + 12, "TO")
    c.setFillColor(INK)
    c.setFont("NothingYouCouldDo", 8.6)
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
        c.line(address_x, line_y - 3, rule_right, line_y - 3)

    # Fun Fact -- typed, real trivia (PC-12), deliberately not the Norman-castle mention already
    # in her handwriting above: the typed box and her voice never carry the same fact twice.
    funfact_top, funfact_bottom = 120, 31
    c.setStrokeColor(FUNFACT)
    c.setLineWidth(0.6)
    c.rect(divider + 11, funfact_bottom, box_right - (divider + 11), funfact_top - funfact_bottom, fill=0, stroke=1)
    c.setFillColor(FUNFACT)
    c.setFont("Helvetica-Bold", 7.5)
    c.drawString(address_x, funfact_top - 11, "FUN FACT")
    c.setFillColor(INK)
    fact_font, fact_size, fact_leading = "Helvetica", 7.4, 8.8
    fact_text = (
        "Aci Castello's rock is over 500,000 years old — lava that cooled underwater into "
        "a mass of glassy basalt pillars. The castle itself later spent three centuries as a "
        "prison, until an 1818 earthquake made it too unsafe to hold anyone."
    )
    fact_y = funfact_top - 24
    for line in wrap_text(fact_text, fact_font, fact_size, box_right - address_x - 6):
        c.setFont(fact_font, fact_size)
        c.drawString(address_x, fact_y, line)
        fact_y -= fact_leading

    credit_top = 19
    c.setStrokeColor(RULE)
    c.line(left, credit_top + 7, right, credit_top + 7)
    c.setFillColor(HexColor("#59635D"))
    c.setFont("Helvetica", 4)
    credit_lines = [
        'Image adaptation: "Acicastello - Castello Normanno" - Pannuccis, CC BY-SA 4.0.',
    ]
    for index, line in enumerate(credit_lines):
        c.drawString(left, credit_top - index * 5, line)

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
    c.setTitle("Aunt Liv's Postcard H5 - Aci Castello (Sicily)")
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
    c.setTitle("Two-up Postcard H5 print sheet - Aci Castello (Sicily)")
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
