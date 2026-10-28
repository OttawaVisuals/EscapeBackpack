from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

from postcard_marks import NARROW_MARK_X, NARROW_MARK_Y, draw_mark


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "NorseBackpack" / "Print" / "_pdf_source" / "Postcard_L1_LAnse_Print.pdf"
OUT_LETTER = ROOT / "NorseBackpack" / "Print" / "_pdf_source" / "Postcard_L1_LAnse_Letter_Print.pdf"
FRONT = ROOT / "NorseBackpack" / "Postcards" / "Postcard_L1_LAnse_Front.png"
STAMP = ROOT / "NorseBackpack" / "Postcards" / "Stamps" / "Stamp_Leif_Longship_v2_flat.png"
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
    # PC-11: preserveAspectRatio=False here previously stretched 1536x1024 (3:2) art onto
    # a 10:7 page by 5% vertically. Fail loud instead of silently distorting -- the fix is
    # correctly-sized art (1500x1050, PC-13), not a draw-time hack.
    if (fw, fh) != (1800, 1200):
        raise ValueError(
            f"Postcard_L1_LAnse_Front.png is {fw}x{fh}, expected 1800x1200 (6x4in "
            f"@300dpi). Drawing it here would stretch it to fit the page."
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
    # 14 Oct 2026 (designer, Q-057): narrow right side. Divider x 276 -> 298 (message column
    # 250 -> 272 pt); mark under the postmark; Fun Fact box from mid-card to the bottom.
    divider = 298
    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", 7.5)
    c.drawCentredString(W / 2, H - 22, "POST CARD")
    c.setStrokeColor(RULE)
    c.line(divider, 34, divider, H - 36)

    # 28 Sept 2026 (postcard update, batch 1 -- Leif + Rollo): message rewritten. Text from the user's
    # Postcard update tab export; message 9.5 pt / Fun Fact 9 pt (was 7.7 / 7.4).
    # 14 Oct 2026 (designer, box + envelopes, PR-007): L1 is the loose note on top of the box. It
    # now hands over the first code as a worked example (1021, the tree-ring year) instead of
    # pointing at the luggage tags, which are gone. The wheel's arm prints the three steps
    # (PP-047), so this card only needs the story and the first try. Option 2 chosen in chat.
    paragraphs = [
        # 14 Oct 2026 (designer, Q-058): was 'Hello nephew!'; a greeting that works for any player.
        'Hello, my dear explorer!',
        'I spent months travelling to explore our Norse heritage, and I turned it into an adventure for you, with a surprise at the end! Everything you need is in this box.',
        # 14 Oct 2026 (designer): first names only; each leg's cards introduce their figure (Q-057).
        'You will follow Leif, Rollo, Aud and Harald.',
        # 14 Oct 2026 (designer, Q-057 option A): introduces Leif. "May have": whether this was Leif's own
        # camp is debated.
        'Start right here, where Leif Erikson’s crew may have camped: the Norse were felling trees at this spot in 1021. Set 1 0 2 1 on my rune wheel and open the envelope with the same runes!',
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

    # Souvenir note (playtest 1, 11 Oct 2026): players read the empty address as "why were
    # these never sent?". Wording chosen in chat ("Short"). Since the 6 x 4 card (13 Oct 2026)
    # it sits under the signature in the wider message column; until then it was where the
    # address used to be, and this card's Fun Fact box started lower than the other 21.
    ps_y = y - 13 - leading
    for line in wrap_text("P.S. These postcards were never sent: they're my souvenirs, one from every stop.",
                          font, 10.5, divider - msg_left - 8):
        c.setFont(font, 10.5)
        c.drawString(msg_left, ps_y, line)
        ps_y -= 11.8

    # PZ-18 element mark. Fixed position on every card -- the pocket between the
    # divider and the postmark, above the Fun Fact box. See postcard_marks.py.
    draw_mark(c, "L1", NARROW_MARK_X, NARROW_MARK_Y)

    # The agreed route stamp, shown at approximately 20 x 24 mm.
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

    # The postmark carries the place only — no date (PC-02/PC-03/PC-04, removed).
    postmark_x, postmark_y = stamp_x - 6, H - 58
    c.setStrokeColor(TEAL)
    c.setLineWidth(0.9)
    c.circle(postmark_x, postmark_y, 27.6, fill=0, stroke=1)
    c.circle(postmark_x, postmark_y, 23.4, fill=0, stroke=1)
    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", 5.8)
    c.drawCentredString(postmark_x, postmark_y + 4.8, "L'ANSE AUX")
    c.drawCentredString(postmark_x, postmark_y - 3.6, "MEADOWS")
    for offset in (-8.4, -2.4, 3.6, 9.6):
        c.line(postmark_x + 27.6, postmark_y + offset, right, postmark_y + offset)

    # No address (playtest 1, 11 Oct 2026): the cards were never posted -- they are Liv's
    # souvenirs -- so the TO box and its four ruled lines are gone. The Fun Fact box moves up
    # into the freed space, stopping just below the stamp.
    address_x = divider + 16
    box_right = right + 5

    # Fun Fact — typed, real trivia, under the stamp.
    c.setFillColor(INK)
    fact_font, fact_size, fact_leading = "Helvetica", 10, 11.8
    # 28 Sept 2026 (postcard update, batch 1 -- Leif + Rollo): Fun Fact rewritten. Text from the user's
    # Postcard update tab export; message 9.5 pt / Fun Fact 9 pt (was 7.7 / 7.4).
    fact_text = (
        # 14 Oct 2026 (designer): Fun Facts aim for one sentence under ~70 characters (Q-057). Was "L'Anse aux
        # Meadows was found after a local man pointed out odd bumps in a meadow. It is still the only
        # confirmed Norse site in North America."
        "This is still the only confirmed Viking site in North America."
    )
    # 14 Oct 2026 (Q-057): the box sits on the bottom (y 37) and starts at mid-card; a fact longer
    # than 7 lines raises its top, up to just under the stamp.
    funfact_bottom = 37
    fact_lines = wrap_text(fact_text, fact_font, fact_size, box_right - address_x - 6)
    funfact_top = max(H / 2, funfact_bottom + 35 + fact_leading * (len(fact_lines) - 1))
    if funfact_top > stamp_y - 6:
        raise SystemExit(f"Fun Fact is {len(fact_lines)} lines; too long for the box (Q-057)")
    c.setStrokeColor(FUNFACT)
    c.setLineWidth(0.6)
    c.rect(divider + 10, funfact_bottom, box_right - (divider + 10), funfact_top - funfact_bottom, fill=0, stroke=1)
    c.setFillColor(FUNFACT)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(address_x, funfact_top - 13, "FUN FACT")
    c.setFillColor(INK)
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
    # One line, no file path. A URL on a prop meant to read as a gift-shop postcard was the only
    # anachronism on the card (PC-09); real postcards do print photographer credits. What remains
    # still satisfies CC BY-SA 3.0 on its own — modification notice, title, author, licence — and
    # the fuller record (source URL, adaptation licence) lives in Postcards/Image_Credits.html.
    credit_lines = [
        'Image adaptation: "L\'Anse aux Meadows, The Meeting of Two Worlds" - D. Gordon E. Robertson, CC BY-SA 3.0.',
    ]
    for index, line in enumerate(credit_lines):
        c.drawString(left, credit_top - index * 6, line)

    # Publisher's imprint removed (PZ-18): the camouflage-on-every-card approach is superseded
    # by putting the real grid-reference imprint on the new decoy card 04 alone.
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
    c.setTitle("Aunt Liv's Postcard L1 - L'Anse aux Meadows")
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
    c.setTitle("Two-up Postcard L1 print sheet - L'Anse aux Meadows")
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
