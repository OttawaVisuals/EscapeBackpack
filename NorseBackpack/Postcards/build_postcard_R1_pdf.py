from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

from postcard_marks import draw_mark


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "NorseBackpack" / "Print" / "_pdf_source" / "Postcard_R1_Chalus_Print.pdf"
OUT_LETTER = ROOT / "NorseBackpack" / "Print" / "_pdf_source" / "Postcard_R1_Chalus_Letter_Print.pdf"
FRONT = ROOT / "NorseBackpack" / "Postcards" / "Postcard_R1_Chalus_Front.png"
STAMP = ROOT / "NorseBackpack" / "Postcards" / "Stamps" / "Stamp_Rollo_Comet_v2_flat.png"
FONT_DIR = ROOT / "Fonts"

PAGE = (6 * 72, 4 * 72)  # 6 x 4 in since 13 Oct 2026 (was 5 x 3.5)
W, H = PAGE
LETTER = (8.5 * 72, 11 * 72)
PAPER = HexColor("#EFE3C4")
# 20 Oct 2026 (designer): no beige fill behind the back; it prints on the paper itself. True restores it.
PAPER_BACKGROUND = False
NAVY = HexColor("#12343C")
TEAL = HexColor("#2F7775")
RULE = HexColor("#A99A7B")
INK = HexColor("#283B34")
FUNFACT = HexColor("#B56A2A")

pdfmetrics.registerFont(TTFont("CinzelExtraBold", str(FONT_DIR / "Cinzel" / "static" / "Cinzel-ExtraBold.ttf")))
pdfmetrics.registerFont(TTFont("NothingYouCouldDo", str(FONT_DIR / "Nothing_You_Could_Do" / "NothingYouCouldDo-Regular.ttf")))


def wrap_text(text, font, size, width):
    words = text.split(" ")
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
    if (fw, fh) != (1800, 1200):
        raise ValueError(
            f"Postcard_R1_Chalus_Front.png is {fw}x{fh}, expected 1800x1200 (6x4in "
            f"@300dpi). Drawing it here would stretch it to fit the page."
        )
    c.drawImage(front, 0, 0, W, H, preserveAspectRatio=False, mask="auto")
    c.restoreState()


def draw_back_card(c, x=0, y=0):
    c.saveState()
    c.translate(x, y)
    # PC-20: 1.5mm bleed, same as build_postcard_L1_pdf.py. Extends the PAPER fill past the
    # card edge so a slightly-off cut or duplex registration never shows a white band; only
    # the sheet crop marks define trim. Confirmed on the L1/L2 print test, 2026-09-27.
    BLEED = 1.5 / 25.4 * 72
    if PAPER_BACKGROUND:
        c.setFillColor(PAPER)
        c.rect(-BLEED, -BLEED, W + 2 * BLEED, H + 2 * BLEED, fill=1, stroke=0)
    c.setStrokeColor(RULE)
    c.setLineWidth(0.7)
    # 14 Oct 2026 (designer): thin border back "for now" (removed 7 Oct 2026 because off-centre
    # duplex prints made it look uneven). 12 pt in: the old 10 pt, 1.2x for the 6 x 4 card.
    c.rect(12, 12, W - 24, H - 24, fill=0, stroke=1)

    # 13 Oct 2026 (designer, after playtest 1): the card is now 6 x 4 in, layout B. The divider
    # moves right (x 184 of 360 -> 276 of 432) for a wider message column; message 11.5 pt
    # (was 9.5), Fun Fact 10 pt (was 9); stamp, postmark and mark 1.2x.
    left, right = 24, W - 24
    # 29 Sept 2026: message column widened -- starts 5 pt from the border (was 10) and wraps
    # 6 pt before the divider (was 12), at the user's request, on all 22 cards.
    msg_left = 18
    divider = 276
    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", 7.5)
    c.drawCentredString(W / 2, H - 22, "POST CARD")
    c.setStrokeColor(RULE)
    c.line(divider, 34, divider, H - 36)

    # Message decided in chat (PZ-19): last of the counting-lock's three cards in read order
    # (Walcheren -> Roumare -> Chalus, decided history, not trip chronology). Evidence category
    # is "supported" so it states the history plainly, unlike Walcheren/Roumare's "story goes"
    # hedge. Mentions a crossbow bolt in passing (flavour) without stating the hidden count of
    # two -- that stays in the front art for players to find themselves.
    # 20 Sept 2026 (PZ-18) -- rule 1: deleted "but this is where I began". The Walcheren-Chalus journal entry places
    # this card now. 26 Sept 2026: also deleted "Odd place to start his family's story, at the very
    # end of it" -- not a position claim, but the user found it confusing alongside the ticket, so it goes too.
    # 28 Sept 2026 (postcard update, batch 1 -- Leif + Rollo): message rewritten. Text from the user's
    # Postcard update tab export; message 9.5 pt / Fun Fact 9 pt (was 7.7 / 7.4).
    paragraphs = [
        'Châlus, where Richard the Lionheart’s story ends.',
        'He was besieging a tiny castle here over a rumoured treasure hoard, of all things, when a crossbow bolt caught him in the shoulder.',
        'Found an old carving near the gate of a bolt just like the one that got him.',
    ]
    c.setFillColor(INK)
    font, size, leading = "NothingYouCouldDo", 11.5, 12.8
    y = H - 44
    for paragraph in paragraphs:
        for line in wrap_text(paragraph, font, size, divider - msg_left - 8):
            c.setFont(font, size)
            c.drawString(msg_left, y, line)
            y -= leading
        y -= 2.2

    c.setFont("NothingYouCouldDo", 11.8)
    c.drawString(msg_left, y, "With love,")
    c.drawString(msg_left, y - 13, "Aunt Liv")

    # PZ-18 element mark. Fixed position on every card -- the pocket between the
    # divider and the postmark, above the Fun Fact box. See postcard_marks.py.
    draw_mark(c, "R1")

    # Rollo's trail stamp (comet) -- one stamp per traveller, not per card.
    stamp_w, stamp_h = 24 / 25.4 * 72, 28.8 / 25.4 * 72
    stamp_x, stamp_y = right - stamp_w, H - 36 - stamp_h
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
    postmark_x, postmark_y = stamp_x - 6, H - 58
    c.setStrokeColor(TEAL)
    c.setLineWidth(0.9)
    c.circle(postmark_x, postmark_y, 27.6, fill=0, stroke=1)
    c.circle(postmark_x, postmark_y, 23.4, fill=0, stroke=1)
    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", 5.8)
    c.drawCentredString(postmark_x, postmark_y - 1.2, "CHÂLUS")
    for offset in (-8.4, -2.4, 3.6, 9.6):
        c.line(postmark_x + 27.6, postmark_y + offset, right, postmark_y + offset)

    # No address (playtest 1, 11 Oct 2026): the cards were never posted -- they are Liv's
    # souvenirs -- so the TO box and its four ruled lines are gone. The Fun Fact box moves up
    # into the freed space, stopping just below the stamp.
    address_x = divider + 16
    box_right = right + 5

    # Fun Fact -- typed, real trivia (PC-12). Carries the counting-lock's sorting clue: the
    # exact date 1199, latest of the three (PZ-19) -- sorts after Walcheren's "before 911" and
    # Roumare's "911".
    # 26 Sept 2026: rewritten to stop retelling the message's bolt/shoulder/gangrene story --
    # now a different fact (the lineage span) that still keeps the 1199 date the lock needs.
    funfact_top, funfact_bottom = stamp_y - 6, 37
    c.setStrokeColor(FUNFACT)
    c.setLineWidth(0.6)
    c.rect(divider + 10, funfact_bottom, box_right - (divider + 10), funfact_top - funfact_bottom, fill=0, stroke=1)
    c.setFillColor(FUNFACT)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(address_x, funfact_top - 13, "FUN FACT")
    c.setFillColor(INK)
    fact_font, fact_size, fact_leading = "Helvetica", 10, 11.8
    # 28 Sept 2026 (postcard update, batch 1 -- Leif + Rollo): Fun Fact rewritten. Text from the user's
    # Postcard update tab export; message 9.5 pt / Fun Fact 9 pt (was 7.7 / 7.4).
    fact_text = (
        'Richard the Lionheart, a descendant of Rollo, was shot here in April 1199 CE.'
    )
    fact_y = funfact_top - 26
    for line in wrap_text(fact_text, fact_font, fact_size, box_right - address_x - 6):
        c.setFont(fact_font, fact_size)
        c.drawString(address_x, fact_y, line)
        fact_y -= fact_leading

    credit_top = 22
    c.setStrokeColor(RULE)
    c.line(left, credit_top + 8, right, credit_top + 8)
    c.setFillColor(HexColor("#59635D"))
    c.setFont("Helvetica", 4.8)
    credit_lines = [
        'Image adaptation: "Chateau Chalus Chabrol" - Fonquebure, CC BY-SA 3.0.',
    ]
    for index, line in enumerate(credit_lines):
        c.drawString(left, credit_top - index * 6, line)

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
    c.setTitle("Aunt Liv's Postcard R1 - Chalus")
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
    c.setTitle("Two-up Postcard R1 print sheet - Chalus")
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
