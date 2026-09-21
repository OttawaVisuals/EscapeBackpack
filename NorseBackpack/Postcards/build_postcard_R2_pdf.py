from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

from postcard_marks import draw_mark


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "output" / "pdf" / "Postcard_R2_Rouen_Print.pdf"
OUT_LETTER = ROOT / "output" / "pdf" / "Postcard_R2_Rouen_Letter_Print.pdf"
FRONT = ROOT / "NorseBackpack" / "Postcards" / "Postcard_R2_Rouen_Front.png"
STAMP = ROOT / "NorseBackpack" / "Postcards" / "Stamps" / "Stamp_Rollo_Comet_v2_flat.png"
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
            f"Postcard_R2_Rouen_Front.png is {fw}x{fh}, expected 1500x1050 (PC-13, "
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

    # Message decided in chat (PZ-05), revised 19 Sept 2026: Liv's own text, kept verbatim
    # including "fighting" rather than the ticket's exact "fight" -- accepted as deliberate
    # extra friction (PZ-15), not a typo to fix. The forest/cow sentence is cut, dropping
    # those two word-pairs from the chain; it's replaced by a rule-line planting counting as
    # Liv's habit (same device as LD's "every little detail counts", PZ-10). Carries the
    # word-lock order clue: fight, people, poultry, inn, in that order (PZ-15) -- resolves to
    # the numeric-lock combination 1486. No rebus on this card.
    # 20 Sept 2026 (PZ-18) -- rule 3: deleted "The tapestry towns are still ahead of me -- saving
    # those for later." Added 17 Sept, rejected 20 Sept: a solver has to work out that "tapestry
    # towns" means Bayeux, and whether Battle counts. The Rouen journal entry places R2 now.
    paragraphs = [
        "Today I got to visit Rouen, and it might be my favourite so far!",
        "This was Rollo’s own capital! The King gave Rollo all of Normandy so the fighting would stop.",
        "Can’t walk anywhere without counting my steps — always have. This afternoon was the city proper, the cathedral and the famous half-timbered houses. The city was vibrant today with lots of people milling about.",
        "All that walking around made me crave fast-food: the battered poultry from Kentucky. Tonight’s dinner was a bit fancier, the Inn I’m staying at is famous for their snails!",
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

    # PZ-18 element mark. Fixed position on every card -- the pocket between the
    # divider and the postmark, above the address box. See postcard_marks.py.
    draw_mark(c, "R2")

    # Rollo's trail stamp (comet) -- one stamp per traveller, not per card.
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
    # still open; do not invent one here.
    postmark_x, postmark_y = stamp_x - 5, H - 48
    c.setStrokeColor(TEAL)
    c.setLineWidth(0.8)
    c.circle(postmark_x, postmark_y, 23, fill=0, stroke=1)
    c.circle(postmark_x, postmark_y, 19.5, fill=0, stroke=1)
    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", 4.8)
    c.drawCentredString(postmark_x, postmark_y - 1, "ROUEN")
    for offset in (-7, -2, 3, 8):
        c.line(postmark_x + 23, postmark_y + offset, right, postmark_y + offset)

    # Address -- same recipient and layout as cards 01-03, 06-08 (PC-13 standard).
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

    # Fun Fact -- typed, real trivia (PC-12). Both supplied facts combined into one callout
    # (decided in chat): the Lionheart's heart entombed at Rouen Cathedral, plus its spire's
    # height record.
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
        "Rouen Cathedral holds the actual heart of Richard the Lionheart, King of England and "
        "Duke of Normandy. Its spire also once held a record of its own: at 151 metres "
        "(495 feet) it’s the tallest church spire in France, and was briefly the tallest "
        "structure in the world in the late 19th century."
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
        'Image adaptation: "Rouen Place du Vieux-Marché 05" - Zairon, CC BY-SA 4.0.',
    ]
    for index, line in enumerate(credit_lines):
        c.drawString(left, credit_top - index * 5, line)

    # Publisher's imprint removed (PZ-18): only the new decoy card 04 carries this line now.
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
    c.setTitle("Aunt Liv's Postcard R2 - Rouen")
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
    c.setTitle("Two-up Postcard R2 print sheet - Rouen")
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
