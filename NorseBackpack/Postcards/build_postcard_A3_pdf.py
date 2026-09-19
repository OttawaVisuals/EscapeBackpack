from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "output" / "pdf" / "Postcard_A3_Esjuberg_Print.pdf"
OUT_LETTER = ROOT / "output" / "pdf" / "Postcard_A3_Esjuberg_Letter_Print.pdf"
FRONT = ROOT / "NorseBackpack" / "Postcards" / "Postcard_A3_Esjuberg_Front.png"
STAMP = ROOT / "NorseBackpack" / "Postcards" / "Stamps" / "Stamp_Aud_Pillars_v2_flat.png"
FONT_DIR = ROOT / "Fonts"

PAGE = landscape((3.5 * 72, 5 * 72))
W, H = PAGE
LETTER = (8.5 * 72, 11 * 72)
PAPER = HexColor("#EFE3C4")
NAVY = HexColor("#12343C")
TEAL = HexColor("#6D528B")
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
    if (fw, fh) != (1500, 1050):
        raise ValueError(
            f"Postcard_A3_Esjuberg_Front.png is {fw}x{fh}, expected 1500x1050 (PC-13, "
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

    # Message decided in chat, 18 Sept 2026 (PZ-03/PZ-17). "Last of Aud's places for me" closes
    # her trail (PC-07 table, mirrors R6's "last of Rollo's places"). The "flip it" line is the
    # upside-down scale-display clue (370.56 g -> 370.5 -> SOLE) -- text only so far; the actual
    # crossed-out-digit scale sketch is a separate drawn element, not yet built.
    paragraphs = [
        "Last of Aud’s places for me. Her brother Helgi met her here and offered her a place to "
        "stay — she turned him down and pushed on to build her own. I like her better for it "
        "every time I read it.",
        "One more thing, if you’ve still got that reading from Dogurdarnes: flip it. Whatever "
        "you’re holding right-side up isn’t the answer — upside-down is.",
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

    # Aud's trail stamp (pillars motif) -- one stamp per traveller, not per card. HI-02 flags this
    # motif for redraw to a comb (her documented saga story); swap STAMP once that art exists.
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

    # Postmark: place only. No date drawn -- postmarks never carry one (PC-02/PC-03/PC-04).
    postmark_x, postmark_y = stamp_x - 5, H - 48
    c.setStrokeColor(TEAL)
    c.setLineWidth(0.8)
    c.circle(postmark_x, postmark_y, 23, fill=0, stroke=1)
    c.circle(postmark_x, postmark_y, 19.5, fill=0, stroke=1)
    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", 3.3)
    c.drawCentredString(postmark_x, postmark_y - 1, "ESJUBERG")
    for offset in (-7, -2, 3, 8):
        c.line(postmark_x + 23, postmark_y + offset, right, postmark_y + offset)

    # Address -- same recipient and layout as the rest of the series (PC-13 standard).
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

    # Fun Fact -- typed, real trivia (PC-12). Esjuberg / Kjalarnes is where Laxdæla saga places
    # Aud's meeting with her brother Helgi and her refusal of his offer; see stops.js a-esjuberg.
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
        "Esjuberg, on Kjalarnes, is where Laxdæla saga places Aud's meeting with her brother "
        "Helgi — and her refusal of his offer to settle down."
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
        'Image adaptation: Akrafjall across the bay - Diego Delso, CC BY-SA 4.0.',
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
    c.setTitle("Aunt Liv's Postcard A3 - Esjuberg")
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
    c.setTitle("Two-up Postcard A3 print sheet - Esjuberg")
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
