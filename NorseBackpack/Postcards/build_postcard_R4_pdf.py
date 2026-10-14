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
OUT = ROOT / "output" / "pdf" / "Postcard_R4_Winchester_Print.pdf"
OUT_LETTER = ROOT / "output" / "pdf" / "Postcard_R4_Winchester_Letter_Print.pdf"
FRONT = ROOT / "NorseBackpack" / "Postcards" / "Postcard_R4_Winchester_Front.png"
STAMP = ROOT / "NorseBackpack" / "Postcards" / "Stamps" / "Stamp_Rollo_Comet_v2_flat.png"
REBUS_DIR = ROOT / "NorseBackpack" / "Postcards" / "RebusIcons"
FONT_DIR = ROOT / "Fonts"

PAGE = (6 * 72, 4 * 72)  # 6 x 4 in since 13 Oct 2026 (was 5 x 3.5)
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
    if (fw, fh) != (1800, 1200):
        raise ValueError(
            f"Postcard_R4_Winchester_Front.png is {fw}x{fh}, expected 1800x1200 (6x4in "
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
    c.setFillColor(PAPER)
    c.rect(-BLEED, -BLEED, W + 2 * BLEED, H + 2 * BLEED, fill=1, stroke=0)
    c.setStrokeColor(RULE)
    c.setLineWidth(0.7)

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
    # cards 01-03 and 06. Names Richard the Lionheart's 1194 recoronation and ties him back to
    # Rollo's line, per the "more history" direction -- and loops toward the treaty rebus below
    # without naming Saint-Clair-sur-Epte outright, so the rebus still does its own job (PZ-14).
    # 20 Sept 2026 (PZ-18) -- rule 2: "Winchester next" was deictic -- it pointed at a card that is
    # not the one in hand, so any change to how the deck is collected or laid out destroyed the
    # referent. The Channel-ferry journal entry places this card now.
    # 28 Sept 2026 (postcard update, batch 1 -- Leif + Rollo): message rewritten. Text from the user's
    # Postcard update tab export; message 9.5 pt / Fun Fact 9 pt (was 7.7 / 7.4).
    paragraphs = [
        'Winchester today — freezing here, but worth every minute. This cathedral is where Richard the Lionheart was crowned a second time.',
        'Another one of Rollo’s own line! Funny to think it’s all because of one deal, centuries earlier.',
        'I got to enjoy the local custom of a scone and hot beverage.',
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
    draw_mark(c, "R4")

    # Rebus icons (PZ-14): tree + teacup spells TREATY, pointing to Saint-Clair-sur-Epte on
    # Rollo's map -- the second piece of the same rebus chain Bayeux started. Anchored below the
    # signature (not a fixed y) so message-length changes can't push icons into overlapping text.
    def draw_rebus_icon(filename, cx, cy, size, angle):
        icon = ImageReader(pencil(REBUS_DIR / filename))  # pencil style, playtest 1
        c.saveState()
        c.translate(cx, cy)
        c.rotate(angle)
        c.drawImage(icon, -size / 2, -size / 2, size, size, mask="auto")
        c.restoreState()

    # 13 Oct 2026 (6 x 4 card): icons 1.2x, spread about x 146, near the wider column's centre (143).
    row_y = (y - 13) - 31
    draw_rebus_icon("Rebus_Tree_Bayeux_v2.png", 96.2, row_y + 2.4, 33.6, -5)
    # 28 Sept 2026: hot-tea cup (three steam lines) so the cup reads as TEA, per the user.
    # v3 is Codex's draft, normalised with RebusIcons/prepare_r5_scale_icons.normalize; drawn
    # 28 pt (was 26) so the cup itself stays about the old size under the added steam.
    draw_rebus_icon("Rebus_Teacup_Hot_Bayeux_v3.png", 159.8, row_y - 3.6, 33.6, 6)

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
    c.setFont("Helvetica-Bold", 4.8)
    c.drawCentredString(postmark_x, postmark_y - 1.2, "WINCHESTER")
    for offset in (-8.4, -2.4, 3.6, 9.6):
        c.line(postmark_x + 27.6, postmark_y + offset, right, postmark_y + offset)

    # No address (playtest 1, 11 Oct 2026): the cards were never posted -- they are Liv's
    # souvenirs -- so the TO box and its four ruled lines are gone. The Fun Fact box moves up
    # into the freed space, stopping just below the stamp.
    address_x = divider + 16
    box_right = right + 5

    # Fun Fact -- typed, real trivia (PC-12). Verified, no date-ordering conflict: separate from
    # the recoronation year already named in the message, so it adds rather than repeats.
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
        'The Round Table hanging in Winchester’s Great Hall is a genuine medieval artifact — just not King Arthur’s.'
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
        'Image adaptation: "Winchester cathedral - geograph.org.uk - 1628919" - Graham Horn, CC BY-SA 2.0.',
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
    c.setTitle("Aunt Liv's Postcard R4 - Winchester")
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
    c.setTitle("Two-up Postcard R4 print sheet - Winchester")
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
