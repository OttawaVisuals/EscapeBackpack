from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

from postcard_marks import draw_mark


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "NorseBackpack" / "Print" / "_pdf_source" / "Postcard_HD_Constantinople_Print.pdf"
OUT_LETTER = ROOT / "NorseBackpack" / "Print" / "_pdf_source" / "Postcard_HD_Constantinople_Letter_Print.pdf"
FRONT = ROOT / "NorseBackpack" / "Postcards" / "Postcard_HD_Constantinople_Front.png"
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
            f"Postcard_HD_Constantinople_Front.png is {fw}x{fh}, expected 1800x1200 (6x4in "
            f"@300dpi). Drawing it here would stretch it to fit the page."
        )
    c.drawImage(front, 0, 0, W, H, preserveAspectRatio=False, mask="auto")
    c.restoreState()


def draw_sugar_spoon(c, cx, cy):
    # Three dotted cubes on a spoon. Coordinates follow the approved vector sketch.
    # 29 Sept 2026 review: handle shortened to about half (x past 204 scaled by 0.45) so the
    # spoon is closer in width to the yeast and flask; the icon is now centred on cx.
    c.saveState()
    c.translate(cx - 22.25, cy + 16.3)
    c.scale(0.125, -0.125)
    c.setStrokeColor(INK)
    c.setLineWidth(8)
    c.setLineCap(1)
    c.setLineJoin(1)

    def line(points):
        p = c.beginPath()
        p.moveTo(*points[0])
        for point in points[1:]:
            p.lineTo(*point)
        c.drawPath(p, stroke=1, fill=0)

    for left, top in ((43, 121), (108, 121), (76, 67)):
        center = left + 33
        right = left + 66
        line([(left, top + 24), (center, top), (right, top + 24), (center, top + 47), (left, top + 24)])
        lower = 183 if top == 121 else 145
        line([(left, top + 24), (left, lower)])
        line([(center, top + 47), (center, lower)])
        line([(right, top + 24), (right, lower)])

    bowl = c.beginPath()
    bowl.moveTo(36, 182)
    bowl.curveTo(39, 222, 76, 232, 179, 210)
    bowl.curveTo(190, 199, 194, 196, 204, 190)
    bowl.curveTo(236, 158, 278, 147, 310, 157)
    bowl.curveTo(319, 160, 320, 174, 313, 182)
    bowl.curveTo(278, 168, 239, 180, 211, 206)
    bowl.curveTo(202, 214, 202, 214, 190, 229)
    bowl.curveTo(148, 258, 83, 250, 42, 243)
    bowl.curveTo(36, 226, 36, 217, 36, 207)
    bowl.close()
    c.drawPath(bowl, stroke=1, fill=0)
    line([(38, 183), (184, 183)])
    c.setFillColor(INK)
    for x, y in ((101, 87), (120, 88), (90, 117), (127, 123),
                 (64, 145), (58, 169), (93, 174), (129, 145),
                 (122, 172), (156, 173)):
        c.circle(x, y, 5, stroke=0, fill=1)  # 29 Sept 2026: radius 3.2 -> 5 (0.4 -> 0.63 pt) so dots print
    c.restoreState()


def draw_yeast_packet(c, cx, cy):
    c.saveState()
    c.setStrokeColor(INK)
    c.setLineWidth(0.9)
    c.setFillColor(HexColor("#FFFFFF"))  # was PAPER; the back has no beige now
    x, bottom, width, top = cx - 10, cy - 13, 20, cy + 13
    p = c.beginPath()
    p.moveTo(x, bottom)
    p.lineTo(x, top - 3)
    for dx, dy in ((3, 0), (6, -3), (9, 0), (12, -3), (15, 0), (18, -3), (20, 0)):
        p.lineTo(x + dx, top + dy)
    p.lineTo(x + width, bottom)
    p.close()
    c.drawPath(p, fill=1, stroke=1)
    c.setLineWidth(0.5)
    c.line(x + 2, cy + 6, x + width - 2, cy + 6)
    c.line(x + 2, cy - 6, x + width - 2, cy - 6)
    c.setFillColor(INK)
    # 29 Sept 2026 review: lettered in Aunt Liv's hand, not a typeset product label.
    c.setFont("NothingYouCouldDo", 6.3)
    c.drawCentredString(cx, cy - 1.8, "Yeast")
    c.restoreState()


def draw_reaction_flask(c, cx, cy):
    c.saveState()
    c.setStrokeColor(INK)
    c.setLineWidth(1)
    c.setLineCap(1)
    c.setLineJoin(1)
    c.setFillColor(HexColor("#FFFFFF"))  # was PAPER; the back has no beige now
    p = c.beginPath()
    p.moveTo(cx - 3, cy + 13)
    p.lineTo(cx - 3, cy + 4)
    p.lineTo(cx - 11, cy - 11)
    p.curveTo(cx - 12, cy - 13, cx - 10, cy - 14, cx - 8, cy - 14)
    p.lineTo(cx + 8, cy - 14)
    p.curveTo(cx + 10, cy - 14, cx + 12, cy - 13, cx + 11, cy - 11)
    p.lineTo(cx + 3, cy + 4)
    p.lineTo(cx + 3, cy + 13)
    c.drawPath(p, fill=1, stroke=1)
    c.line(cx - 4.5, cy + 13, cx + 4.5, cy + 13)
    wave = c.beginPath()
    wave.moveTo(cx - 8, cy - 8)
    wave.curveTo(cx - 3, cy - 5, cx + 2, cy - 10, cx + 8, cy - 8)
    c.drawPath(wave, stroke=1, fill=0)
    c.setFillColor(INK)
    for dx, dy, radius in ((-3, -3, 1), (4, -2, 1), (0, 3, 1.1), (-2, 8, 0.7)):
        c.circle(cx + dx, cy + dy, radius, stroke=0, fill=1)
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

    # Message text approved in chat (PZ-20, 17 Sept 2026). No longer a pure decoy card -- HD
    # carries the rebus third of the MEAD riddle, drawn rather than written, below.
    paragraphs = [
        "Constantinople — well, Istanbul now, but I like the old name for this trip.",
        "Impossible not to think about Harald everywhere here; this is where he made his "
        "fortune, long before Norway ever heard of him.",
        # 15 Oct 2026 (designer): lead-in now says it is a picture riddle; Hippodrome dropped.
        "Here’s another riddle in pictures, sketched for me in a little shop here:",
    ]
    c.setFillColor(INK)
    font, size, leading = "NothingYouCouldDo", 11.5, 12.8
    y = H - 44
    for paragraph in paragraphs:
        for line in wrap_text(paragraph, font, size, divider - msg_left - 8):
            c.setFont(font, size)
            c.drawString(msg_left, y, line)
            y -= leading
        y -= 1.9

    # PZ-20, revised 29 Sept 2026: dotted sugar cubes on a spoon + yeast + reaction flask.
    # The hourglass and bubbling jar are superseded. The three icons point to fermentation.
    rebus_top = y - 4
    rebus_bottom = max(37, rebus_top - 58)
    box_w = divider - msg_left - 8
    c.setStrokeColor(RULE)
    c.setLineWidth(0.6)
    c.rect(msg_left, rebus_bottom, box_w, rebus_top - rebus_bottom, fill=0, stroke=1)
    # 29 Sept 2026 review: icons lowered 3 pt to sit centred in the box, spaced evenly
    # (12 pt margins, equal gaps), and the signs drawn as 0.9 pt strokes (plus, then arrow).
    # 13 Oct 2026 (6 x 4 card): the whole row is drawn 1.25x about the box's centre; the
    # x positions below are offsets from that centre in the old 163 pt box's units.
    row_y = (rebus_top + rebus_bottom) / 2
    c.saveState()
    c.translate(msg_left + box_w / 2, row_y)
    c.scale(1.25, 1.25)
    row_y = 0
    icon_xs = [29.75 - 81.5, 87.75 - 81.5, 139.5 - 81.5]
    draw_sugar_spoon(c, icon_xs[0], row_y)
    draw_yeast_packet(c, icon_xs[1], row_y)
    draw_reaction_flask(c, icon_xs[2], row_y)
    c.setFillColor(INK)
    # Plus drawn with the same line weight as the arrow below, so the two signs match.
    px = 62.6 - 81.5
    c.setStrokeColor(INK)
    c.setLineWidth(0.9)
    c.setLineCap(1)
    c.line(px - 4, row_y, px + 4, row_y)
    c.line(px, row_y - 4, px, row_y + 4)
    # 29 Sept 2026 (user): second sign is an arrow, so the flask reads as the result of
    # sugar + yeast. Drawn, because NothingYouCouldDo has no arrow glyph.
    ax, ay = 112.9 - 81.5, row_y
    c.setStrokeColor(INK)
    c.setLineWidth(0.9)
    c.setLineCap(1)
    c.setLineJoin(1)
    c.line(ax - 6, ay, ax + 5.5, ay)
    head = c.beginPath()
    head.moveTo(ax + 2.5, ay + 3)
    head.lineTo(ax + 6, ay)
    head.lineTo(ax + 2.5, ay - 3)
    c.drawPath(head, stroke=1, fill=0)
    c.restoreState()

    c.setFillColor(INK)
    c.setFont("NothingYouCouldDo", 11.8)
    c.drawString(msg_left, rebus_bottom - 14, "Love,")
    c.drawString(msg_left, rebus_bottom - 27, "Aunt Liv")

    # PZ-18 element mark. Fixed position on every card -- the pocket between the
    # divider and the postmark, above the Fun Fact box. See postcard_marks.py.
    draw_mark(c, "HD")

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
    c.drawCentredString(postmark_x, postmark_y + 4.8, "CONSTANTI-")
    c.drawCentredString(postmark_x, postmark_y - 2.4, "NOPLE")
    for offset in (-8.4, -2.4, 3.6, 9.6):
        c.line(postmark_x + 27.6, postmark_y + offset, right, postmark_y + offset)

    # No address (playtest 1, 11 Oct 2026): the cards were never posted -- they are Liv's
    # souvenirs -- so the TO box and its four ruled lines are gone. The Fun Fact box moves up
    # into the freed space, stopping just below the stamp.
    address_x = divider + 16
    box_right = right + 5

    # Fun Fact -- typed, real trivia (PC-12).
    # 26 Sept 2026: rewritten -- the old text ("wealth... funded his eventual claim to the
    # throne") was judged too close to the message's "made his fortune" line despite the
    # different wording. New fact is unrelated Constantinople trivia instead. This supersedes
    # PZ-20's design note in Norse_Brainstorm.html, which argued the old pairing didn't repeat --
    # see that note for the superseded reasoning.
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
        "A Viking carved “Halfdan was here” in Hagia Sophia. It's still there."  # 15 Oct 2026 (designer, Q-057): shortened
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
        'Image adaptation: "Historical peninsula and modern skyline of Istanbul" - Hunanuk, CC0.',
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
    c.setTitle("Aunt Liv's Postcard HD - Constantinople")
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
    c.setTitle("Two-up Postcard HD print sheet - Constantinople")
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
