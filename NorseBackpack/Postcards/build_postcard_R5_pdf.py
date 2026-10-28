from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

from pencil_rebus import pencil
from postcard_marks import draw_mark


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "NorseBackpack" / "Print" / "_pdf_source" / "Postcard_R5_Battle_Print.pdf"
OUT_LETTER = ROOT / "NorseBackpack" / "Print" / "_pdf_source" / "Postcard_R5_Battle_Letter_Print.pdf"
FRONT = ROOT / "NorseBackpack" / "Postcards" / "Postcard_R5_Battle_Front.png"
STAMP = ROOT / "NorseBackpack" / "Postcards" / "Stamps" / "Stamp_Rollo_Comet_v2_flat.png"
REBUS_DIR = ROOT / "NorseBackpack" / "Postcards" / "RebusIcons"
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
            f"Postcard_R5_Battle_Front.png is {fw}x{fh}, expected 1800x1200 (6x4in "
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

    # Message text decided in chat (PZ-05): enthusiastic/warm/fun/friendly voice, matching
    # cards 01-03, 06 and 07. Names William the Conqueror's 1066 victory and loops back to the
    # Bayeux Tapestry from card 06, per the "more history" direction. This card carries no rebus
    # -- its earlier TREATY-rebus candidacy moved to Winchester (PZ-14).
    # 28 Sept 2026 (postcard update, batch 1 -- R5): message rewritten. Text from the user's Postcard update
    # tab export, with option B chosen in chat for the measuring line; 9.5 pt / 9 pt (was 7.7 / 7.4).
    paragraphs = [
        "Today I visited Battle, the village where the Battle of Hastings happened. It’s so cool to be able to see it in person, especially after seeing it on the tapestry! But it doesn't really measure up to what the tapestry depicts.",
        # 1 Oct 2026 (PZ-14): "they" became "my maps", so the hint points at the map, where dotted
        # leader lines run from each drawing to its town dot, rather than at the drawings.
        "I hope you're enjoying my drawings! Good thing I packed my old ruler: my maps only make sense when I pick the right side.",
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
    c.drawString(msg_left, y, "Love,")
    c.drawString(msg_left, y - 13, "Aunt Liv")

    # PZ-18 element mark. Fixed position on every card -- the pocket between the
    # divider and the postmark, above the Fun Fact box. See postcard_marks.py.
    draw_mark(c, "R5")

    # Rebus (PZ-14, replaced 16 Oct 2026): was fish scales, finger, colon, die, fingers, Roman V
    # (SCALE 1:125); now a longship drawing. The pencil() icon helper below is kept, unused.
    def draw_rebus_icon(filename, cx, cy, size, angle):
        icon = ImageReader(pencil(REBUS_DIR / filename))  # pencil style, playtest 1
        c.saveState()
        c.translate(cx, cy)
        c.rotate(angle)
        c.drawImage(icon, -size / 2, -size / 2, size, size, mask="auto")
        c.restoreState()

    # 16 Oct 2026 (designer, PZ-011 redesign): the SCALE 1:125 rebus is replaced by one drawing
    # of a longship (Codex, already pencil style, so it skips the pencil filter). It matches the
    # LONGSHIP edge of the ruler (PP-025), the right one for the distance.
    row_y = (y - 13) - 31
    ship = ImageReader(str(REBUS_DIR / "Rebus_Longship_Pencil_Codex_v1.png"))
    ship_w = 92.0
    ship_h = ship_w * ship.getSize()[1] / ship.getSize()[0]
    c.drawImage(ship, 143 - ship_w / 2, row_y - ship_h / 2, ship_w, ship_h, mask="auto")

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

    # Postmark: place only. No date drawn -- PC-03/PC-04 (the eighteen postmark dates) are
    # still open; do not invent one here.
    postmark_x, postmark_y = stamp_x - 6, H - 58
    c.setStrokeColor(TEAL)
    c.setLineWidth(0.9)
    c.circle(postmark_x, postmark_y, 27.6, fill=0, stroke=1)
    c.circle(postmark_x, postmark_y, 23.4, fill=0, stroke=1)
    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", 5.8)
    c.drawCentredString(postmark_x, postmark_y - 1.2, "BATTLE")
    for offset in (-8.4, -2.4, 3.6, 9.6):
        c.line(postmark_x + 27.6, postmark_y + offset, right, postmark_y + offset)

    # No address (playtest 1, 11 Oct 2026): the cards were never posted -- they are Liv's
    # souvenirs -- so the TO box and its four ruled lines are gone. The Fun Fact box moves up
    # into the freed space, stopping just below the stamp.
    address_x = divider + 16
    box_right = right + 5

    # Fun Fact -- typed, real trivia (PC-12). Loops back to the Bayeux Tapestry from card 06.
    funfact_top, funfact_bottom = stamp_y - 6, 37
    c.setStrokeColor(FUNFACT)
    c.setLineWidth(0.6)
    c.rect(divider + 10, funfact_bottom, box_right - (divider + 10), funfact_top - funfact_bottom, fill=0, stroke=1)
    c.setFillColor(FUNFACT)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(address_x, funfact_top - 13, "FUN FACT")
    c.setFillColor(INK)
    fact_font, fact_size, fact_leading = "Helvetica", 10, 11.8
    # 28 Sept 2026 (postcard update, batch 1 -- R5): Fun Fact shortened. Text from the user's Postcard update
    # tab export, with option B chosen in chat for the measuring line; 9.5 pt / 9 pt (was 7.7 / 7.4).
    fact_text = (
        'The arrow in Harold’s eye on the Bayeux Tapestry may have been reworked by Victorian restorers.'
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
        'Image adaptation: "Sculpture at the Site of the Battle of Hastings - geograph.org.uk - 5801680" - Richard Cooke, CC BY-SA 2.0.',
    ]
    for index, line in enumerate(credit_lines):
        c.drawString(left, credit_top - index * 6, line)

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
    c.setTitle("Aunt Liv's Postcard R5 - Battle")
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
    c.setTitle("Two-up Postcard R5 print sheet - Battle")
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
