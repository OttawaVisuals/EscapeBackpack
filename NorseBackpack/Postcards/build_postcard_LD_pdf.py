from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

from postcard_marks import draw_mark


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "output" / "pdf" / "Postcard_LD_Brattahlid_Print.pdf"
OUT_LETTER = ROOT / "output" / "pdf" / "Postcard_LD_Brattahlid_Letter_Print.pdf"
FRONT = ROOT / "NorseBackpack" / "Postcards" / "Postcard_LD_Brattahlid_Front.png"
STAMP = ROOT / "NorseBackpack" / "Postcards" / "Stamps" / "Stamp_Leif_Longship_v2_flat.png"
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
            f"Postcard_LD_Brattahlid_Front.png is {fw}x{fh}, expected 1500x1050 (PC-13, "
            f"5x3.5in @300dpi). Drawing it here would stretch it to fit the page."
        )
    c.drawImage(front, 0, 0, W, H, preserveAspectRatio=False, mask="auto")
    c.restoreState()


def draw_back_card(c, x=0, y=0):
    c.saveState()
    c.translate(x, y)
    # PC-20: bleed. Kept as a safety margin even after the manual-duplex offset was
    # fixed (paper-guide slider) -- without extra background past the trim line, a
    # slightly-off cut still reveals a white band. 1.5mm bleed extends the PAPER fill
    # past the card edge; only the sheet crop marks define trim, so this prints
    # harmlessly into the surrounding paper.
    BLEED = 1.5 / 25.4 * 72
    c.setFillColor(PAPER)
    c.rect(-BLEED, -BLEED, W + 2 * BLEED, H + 2 * BLEED, fill=1, stroke=0)
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

    # Message decided in chat (15 Sept 2026, PZ-05/PZ-18): this is Leif's decoy card, a real
    # place Liv visited that isn't one of his three trail stops. Carries the "You know me --
    # every little detail counts" rule line (PZ-10) for the first time -- it belongs wherever
    # the real F1 imprint lives, which is now this card, not card 02.
    # "Brattahlid" is spelled without the eth here on purpose: the handwriting font
    # (NothingYouCouldDo) renders "ð" as a broken glyph -- confirmed by comparing against the
    # Fun Fact box below, set in Helvetica, which renders "Brattahlíð" and "Þjóðhildar's"
    # correctly. Liv's casual handwriting dropping the diacritic (vs. the typed Fun Fact
    # keeping it) is a plausible, deliberate difference, not a workaround pretending to be one.
    # 28 Sept 2026 (postcard update, batch 1 -- Leif + Rollo): message rewritten. Text from the user's
    # Postcard update tab export; message 9.5 pt / Fun Fact 9 pt (was 7.7 / 7.4).
    paragraphs = [
        'Amazing place today! Brattahlid, Greenland where Leif actually grew up.',
        "It's stunning here! Erik apparently picked the name “Greenland” on purpose, to lure settlers! Funny how a name can cast a _spell_ like that. I really enjoy those small details!",
        'I hope you enjoy this puzzle, there might be a few steps to get the final code.',
    ]
    c.setFillColor(INK)
    font, size, leading = "NothingYouCouldDo", 9.5, 10.6
    y = H - 36
    for paragraph in paragraphs:
        for line in wrap_text(paragraph, font, size, divider - left - 12):
            # _word_ marks an underlined word (28 Sept 2026: "spell", the user's choice, same
            # hand-drawn underline style as H5's "raven"). Drawn word by word so it can fall mid-line.
            c.setFont(font, size)
            x = left
            space_w = pdfmetrics.stringWidth(" ", font, size)
            for word in line.split(" "):
                marked = word.startswith("_") and "_" in word[1:]
                text = word.replace("_", "") if marked else word
                c.drawString(x, y, text)
                word_w = pdfmetrics.stringWidth(text, font, size)
                if marked:
                    core_w = pdfmetrics.stringWidth(word[1:word.index("_", 1)], font, size)
                    c.setStrokeColor(INK)
                    c.setLineWidth(0.6)
                    c.line(x, y - 1.8, x + core_w, y - 1.8)
                x += word_w + space_w
            y -= leading
        y -= 1.8

    c.setFont("NothingYouCouldDo", 9.8)
    c.drawString(left, y, "With Love,")
    c.drawString(left, y - 11, "Aunt Liv")

    # PZ-18 element mark. Fixed position on every card -- the pocket between the
    # divider and the postmark, above the address box. See postcard_marks.py.
    draw_mark(c, "LD")

    # Leif's trail stamp -- one stamp per traveller, not per card.
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

    # Postmark: place only. No date drawn -- PC-03/PC-04 (the eighteen postmark dates) are
    # still open. Whether this decoy takes a calendar slot at all is also open (PZ-18).
    postmark_x, postmark_y = stamp_x - 5, H - 48
    c.setStrokeColor(TEAL)
    c.setLineWidth(0.8)
    c.circle(postmark_x, postmark_y, 23, fill=0, stroke=1)
    c.circle(postmark_x, postmark_y, 19.5, fill=0, stroke=1)
    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", 4.0)
    c.drawCentredString(postmark_x, postmark_y - 1, "BRATTAHLÍÐ")
    for offset in (-7, -2, 3, 8):
        c.line(postmark_x + 23, postmark_y + offset, right, postmark_y + offset)

    # Address -- same recipient and layout as cards 01-03, 06-09 (PC-13 standard).
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

    # Fun Fact -- typed, real trivia (PC-12).
    # 26 Sept 2026: rewritten -- the old text restated the message's "little church his wife
    # built" line almost exactly. New fact keeps the homestead/Eastern Settlement angle but
    # states different content (the settlement's scale) instead of the church.
    funfact_top, funfact_bottom = 120, 31
    c.setStrokeColor(FUNFACT)
    c.setLineWidth(0.6)
    c.rect(divider + 11, funfact_bottom, box_right - (divider + 11), funfact_top - funfact_bottom, fill=0, stroke=1)
    c.setFillColor(FUNFACT)
    c.setFont("Helvetica-Bold", 7.5)
    c.drawString(address_x, funfact_top - 11, "FUN FACT")
    c.setFillColor(INK)
    fact_font, fact_size, fact_leading = "Helvetica", 9, 10.7
    # 28 Sept 2026 (postcard update, batch 1 -- Leif + Rollo): Fun Fact rewritten. Text from the user's
    # Postcard update tab export; message 9.5 pt / Fun Fact 9 pt (was 7.7 / 7.4).
    fact_text = (
        "Leif's mother built Greenland's first church here. It was tiny and turf-walled, and the saga says she put it well away from pagan Erik's farmhouse."
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
        'Image adaptation: "Reproduction of Brattahlíð Viking church" - Claire Rowland, CC BY 2.0.',
    ]
    for index, line in enumerate(credit_lines):
        c.drawString(left, credit_top - index * 5, line)

    # Publisher's imprint -- the REAL grid reference (PZ-10, PZ-18). Moved here from card 02:
    # this decoy card must be in hand by the time the beasts chain runs, since it's now the
    # only card carrying the pointer to square F1 on Leif's map (polar bear).
    c.setFont("Helvetica", 5)
    c.drawRightString(right, credit_top, "Vinland Editions  ·  Series F, No. 1")
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
    c.setTitle("Aunt Liv's Postcard LD - Brattahlíð (decoy)")
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
    c.setTitle("Two-up Postcard LD print sheet - Brattahlíð (decoy)")
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
