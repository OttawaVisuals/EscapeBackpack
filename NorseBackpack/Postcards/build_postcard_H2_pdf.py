from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

from postcard_marks import draw_mark


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "NorseBackpack" / "Print" / "_pdf_source" / "Postcard_H2_Staraya_Ladoga_Print.pdf"
OUT_LETTER = ROOT / "NorseBackpack" / "Print" / "_pdf_source" / "Postcard_H2_Staraya_Ladoga_Letter_Print.pdf"
FRONT = ROOT / "NorseBackpack" / "Postcards" / "Postcard_H2_Staraya_Ladoga_Front.png"
STAMP = ROOT / "NorseBackpack" / "Postcards" / "Stamps" / "Stamp_Harald_Dane_Axe_v1.png"
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
    if (fw, fh) != (1800, 1200):
        raise ValueError(
            f"Postcard_H2_Staraya_Ladoga_Front.png is {fw}x{fh}, expected 1800x1200 (6x4in "
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

    # Message text approved in chat (PZ-20, 17 Sept 2026): an acrostic. The first letter of each
    # of the five sentences below spells DRINK -- one third of the MEAD riddle. Each sentence is
    # its own paragraph so its first letter opens a fresh line, same as a normal handwritten note.
    # 29 Sept 2026 (postcard update, batch 2 -- Aud + Harald): message rewritten. Text from the user's Postcard
    # update tab export (small agreed fixes); message 9.5 pt / Fun Fact 9 pt (was 7.7 / 7.4).
    paragraphs = [
        'Dinners take hours here and nobody rushes, which suits me fine.',
        'Rurik supposedly ruled from right here, if the old chronicles are true.',
        'I climbed the fortress wall and thought of Harald Hardrada, who may have turned up here as a teenage exile before he became king of Norway.',
        # 15 Oct 2026 (designer): N and K rewritten. N = Liv with a hot tea reading the sagas (hint at
        # DRINK, as AD's "I've read everything" hints at BOOK); K introduces Harald and avoids "next"
        # so nobody reads a route order into it. Still D, R, I, N, K.
        'Nestled in a cosy corner with a hot tea, I’ve been reading about the old saga and what our potential ancestors achieved.',
        'Knowing how far Harald still had to go makes my own trip feel short.',
    ]
    c.setFillColor(INK)
    font, size, leading = "NothingYouCouldDo", 11.5, 12.8
    y = H - 44
    # 29 Sept 2026 (user): hanging indent -- only the D, R, I, N, K sentence starts sit on the
    # margin; every wrapped continuation line, and the sign-off, is set in by INDENT.
    # 29 Sept 2026 (user): indent reduced from 10 pt to one space, then to half a space (~2.5 pt).
    # Close to the floor: "y" overhangs its origin by ~1.6 pt, so below ~2 pt the "you is starting"
    # line would sit flush with the margin.
    # 15 Oct 2026 (designer): indent raised from half a space (~2.5 pt) to 1.5 spaces (too much), then set to half a space
    # + 1.5 pt (~4 pt, about 2 px) so the D, R, I, N, K starts stand out a little more.
    INDENT = pdfmetrics.stringWidth(" ", font, size) / 2 + 1.5
    full_w = divider - msg_left - 8
    for paragraph in paragraphs:
        first = wrap_text(paragraph, font, size, full_w)[0]
        rest = paragraph[len(first):].strip()
        lines = [(msg_left, first)] + [(msg_left + INDENT, l) for l in (wrap_text(rest, font, size, full_w - INDENT) if rest else [])]
        for x, line in lines:
            c.setFont(font, size)
            c.drawString(x, y, line)
            y -= leading
        y -= 1.9

    c.setFont("NothingYouCouldDo", 11.8)
    c.drawString(msg_left + INDENT, y, "Love,")
    c.drawString(msg_left + INDENT, y - 13, "Aunt Liv")

    # PZ-18 element mark. Fixed position on every card -- the pocket between the
    # divider and the postmark, above the Fun Fact box. See postcard_marks.py.
    draw_mark(c, "H2")

    # Same trail stamp as the other Harald cards -- one stamp per traveller, not per card.
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

    # Postmark: place only. No date drawn -- PC-03/PC-04 are still open, and PZ-08 needs those
    # dates checked against the trail-order constraint before any are printed.
    postmark_x, postmark_y = stamp_x - 6, H - 58
    c.setStrokeColor(TEAL)
    c.setLineWidth(0.9)
    c.circle(postmark_x, postmark_y, 27.6, fill=0, stroke=1)
    c.circle(postmark_x, postmark_y, 23.4, fill=0, stroke=1)
    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", 5.5)
    c.drawCentredString(postmark_x, postmark_y + 4.8, "STARAYA")
    c.drawCentredString(postmark_x, postmark_y - 2.4, "LADOGA")
    for offset in (-8.4, -2.4, 3.6, 9.6):
        c.line(postmark_x + 27.6, postmark_y + offset, right, postmark_y + offset)

    # No address (playtest 1, 11 Oct 2026): the cards were never posted -- they are Liv's
    # souvenirs -- so the TO box and its four ruled lines are gone. The Fun Fact box moves up
    # into the freed space, stopping just below the stamp.
    address_x = divider + 16
    box_right = right + 5

    # Fun Fact -- typed, real trivia (PC-12), deliberately not about Rurik (already in her
    # handwriting above): a second, unrelated Staraya Ladoga fact, not a restatement.
    funfact_top, funfact_bottom = stamp_y - 6, 37
    c.setStrokeColor(FUNFACT)
    c.setLineWidth(0.6)
    c.rect(divider + 10, funfact_bottom, box_right - (divider + 10), funfact_top - funfact_bottom, fill=0, stroke=1)
    c.setFillColor(FUNFACT)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(address_x, funfact_top - 13, "FUN FACT")
    c.setFillColor(INK)
    fact_font, fact_size, fact_leading = "Helvetica", 10, 11.8
    # 29 Sept 2026 (postcard update, batch 2 -- Aud + Harald): Fun Fact rewritten. Text from the user's Postcard
    # update tab export (small agreed fixes); message 9.5 pt / Fun Fact 9 pt (was 7.7 / 7.4).
    fact_text = (
        "A rune stick found here is one of Russia's oldest runic finds."  # 15 Oct 2026 (designer, Q-057): shortened
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
    # 29 Sept 2026: author name transliterated (Александр Байдуков) -- Helvetica has no Cyrillic
    # glyphs, so the original printed as black boxes.
    credit_lines = [
        'Image adaptation: "The Fortress Of Staraya Ladoga. Fortress wall" - Aleksandr Baydukov, CC BY-SA 4.0.',
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
    c.setTitle("Aunt Liv's Postcard H2 - Staraya Ladoga")
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
    c.setTitle("Two-up Postcard H2 print sheet - Staraya Ladoga")
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
