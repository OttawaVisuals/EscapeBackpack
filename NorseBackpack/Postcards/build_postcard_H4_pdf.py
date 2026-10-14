from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

from postcard_marks import draw_mark


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "output" / "pdf" / "Postcard_H4_Hedeby_Print.pdf"
OUT_LETTER = ROOT / "output" / "pdf" / "Postcard_H4_Hedeby_Letter_Print.pdf"
FRONT = ROOT / "NorseBackpack" / "Postcards" / "Postcard_H4_Hedeby_Front.png"
STAMP = ROOT / "NorseBackpack" / "Postcards" / "Stamps" / "Stamp_Harald_Dane_Axe_v1.png"
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
            f"Postcard_H4_Hedeby_Front.png is {fw}x{fh}, expected 1800x1200 (6x4in "
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

    # Message text approved in chat (PZ-02/PZ-09, 17 Sept 2026): sets up the branch-rune key
    # she copied at Hedeby. The hand-drawn table below carries the actual group letters -- the
    # message only needs to establish that it exists and what the two branch counts mean.
    # 20 Sept 2026 (PZ-18): the opener was "New stop: Hedeby -- saltwater again, after all that
    # river country." That clue was dropped: "river country" only reliably points at Staraya
    # Ladoga, whose card mentions a river bend, so placing Kyiv before Hedeby needed outside
    # knowledge of the Dnieper. The replacement names the Mediterranean instead, which the map
    # resolves: it puts Sicily, Constantinople and Patara after Hedeby and leaves Kyiv before it,
    # taking the leg from 60 possible orders to 4 and saving a journal entry.
    # 29 Sept 2026 (postcard update, batch 2 -- Aud + Harald): message rewritten. Text from the user's Postcard
    # update tab export (small agreed fixes); message 9.5 pt / Fun Fact 9 pt (was 7.7 / 7.4).
    paragraphs = [
        'Today: Hedeby — barely a Hedeby left. From here I’m turning south: nothing but Mediterranean weather for the rest of this trip.',
        'A woodcarver showed me how the old branch-runes worked — count the branches one way for the family, the other way for the letter.',
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
    draw_mark(c, "H4")
    y -= 13  # 29 Sept 2026: matches the sign-off spacing (was 9); 13 since the 6 x 4 card

    # Her copied rune key (PZ-02): a hand-drawn table, not typed -- this is Liv's own copy, not
    # museum reference material, so it lives in her handwriting font like the message above it.
    # ą and ʀ have no glyph in NothingYouCouldDo (checked against the font's cmap), so her copy
    # substitutes ö and r' -- a legible stand-in, not a change to the actual cipher, since HRAFN
    # only ever needs h, r, a, f, n, none of which are affected.
    # 11 Oct 2026 (playtest 1): the key was three lines ("1 — f u þ ö r k"), which players did
    # not read as a lookup table. It is now a ruled grid -- rows 1-3 down the side, places 1-6
    # across the top -- drawn with slightly uneven pen lines so it still reads as her copy.
    # 13 Oct 2026 (6 x 4 card): the key is about 1.15x and the box is shorter: the caption and
    # the footnote sit beside the grid instead of above and below it, since the larger message
    # leaves less height under the signature.
    table_top = y - 9
    table_bottom = max(37, table_top - 67)
    c.setStrokeColor(RULE)
    c.setLineWidth(0.6)
    c.rect(msg_left, table_bottom, divider - msg_left - 8, table_top - table_bottom, fill=0, stroke=1)
    c.setFillColor(INK)
    # 12 Oct 2026 (designer): lighter table. Only two rules -- one under the header row, one
    # right of the label column -- and the headers are half-runes instead of digits: down the
    # side, a stave with 1-3 branches on the left only (the row); across the top, a stave with
    # 1-6 branches on the right only (the place). A rune is read by matching its left branches
    # to a row and its right branches to a column. Stems are drawn like Harald's map
    # (draw_rune_stem in TravelMap/build_trail_maps_pdf.py), smaller.
    rows = [["f", "u", "þ", "ö", "r", "k"], ["h", "n", "i", "a", "s"], ["t", "b", "m", "l", "r'"]]
    label_w, cell_w, head_h, cell_h = 19, 21, 18, 12.5
    grid_x, grid_top = msg_left + 8, table_top - 5
    grid_w, grid_h = label_w + 6 * cell_w, head_h + 3 * cell_h
    # Fixed small wobbles (pt) so each pen line is a touch off-straight, the same on every build.
    wobble = [0.6, -0.5, 0.4, -0.75]
    c.setStrokeColor(INK)
    c.setLineWidth(0.6)
    c.line(grid_x - 1, grid_top - head_h + wobble[0], grid_x + grid_w + 1, grid_top - head_h + wobble[1])
    c.line(grid_x + label_w + wobble[2], grid_top - 1.9, grid_x + label_w + wobble[3], grid_top - grid_h - 1.2)

    def half_rune(x, y, half, left, right_):
        """A branch-rune stave with ticks on one side only; step and tick shape fixed so the
        side and top headers match."""
        c.setLineWidth(0.75)
        c.setLineCap(1)
        c.line(x, y - half, x, y + half)
        step, top = 2.6, y + half - 1.5
        for i in range(left):
            c.line(x, top - i * step, x - 4.2, top - i * step - 2.2)
        for i in range(right_):
            c.line(x, top - i * step, x + 4.2, top - i * step - 2.2)

    for col in range(6):                                 # header: right branches = place
        half_rune(grid_x + label_w + (col + 0.5) * cell_w - 1.9, grid_top - head_h / 2, 7.9, 0, col + 1)
    c.setFont("NothingYouCouldDo", 10.2)
    for r, letters in enumerate(rows):
        mid = grid_top - head_h - (r + 0.5) * cell_h
        half_rune(grid_x + label_w / 2 + 1.9, mid, 5.2, r + 1, 0)   # side: left branches = row
        for col, letter in enumerate(letters):
            c.drawCentredString(grid_x + label_w + (col + 0.5) * cell_w, mid - 3.1, letter)
    note_x, note_w = grid_x + grid_w + 12, divider - 8 - (grid_x + grid_w + 12) - 4
    c.setFont("NothingYouCouldDo", 9.5)
    note_y = grid_top - 10
    for line in wrap_text("his key, copied out:", "NothingYouCouldDo", 9.5, note_w):
        c.drawString(note_x, note_y, line)
        note_y -= 11
    note_y -= 4
    c.setFont("NothingYouCouldDo", 8)
    for line in wrap_text("(left branches = which row. right = where in it.)", "NothingYouCouldDo", 8, note_w):
        c.drawString(note_x, note_y, line)
        note_y -= 9.5

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
    c.setFont("Helvetica-Bold", 6.7)
    c.drawCentredString(postmark_x, postmark_y - 1.8, "HEDEBY")
    for offset in (-8.4, -2.4, 3.6, 9.6):
        c.line(postmark_x + 27.6, postmark_y + offset, right, postmark_y + offset)

    # No address (playtest 1, 11 Oct 2026): the cards were never posted -- they are Liv's
    # souvenirs -- so the TO box and its four ruled lines are gone. The Fun Fact box moves up
    # into the freed space, stopping just below the stamp.
    address_x = divider + 16
    box_right = right + 5

    # Fun Fact -- typed, real trivia (PC-12), deliberately not about the rune key: her handwriting
    # and the typed box each carry different content, never the same fact twice.
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
        'During his war with Denmark, Harald burned Hedeby to the ground — sailing burning ships straight into the harbour.'
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
        'Image adaptation: "Hedeby, Busdorf (P1100664)" - Matti Blume, CC BY-SA 4.0.',
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
    c.setTitle("Aunt Liv's Postcard H4 - Hedeby")
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
    c.setTitle("Two-up Postcard H4 print sheet - Hedeby")
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
