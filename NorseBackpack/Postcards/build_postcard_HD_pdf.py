from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

from postcard_marks import draw_mark


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "output" / "pdf" / "Postcard_HD_Constantinople_Print.pdf"
OUT_LETTER = ROOT / "output" / "pdf" / "Postcard_HD_Constantinople_Letter_Print.pdf"
FRONT = ROOT / "NorseBackpack" / "Postcards" / "Postcard_HD_Constantinople_Front.png"
STAMP = ROOT / "NorseBackpack" / "Postcards" / "Stamps" / "Stamp_Harald_Dane_Axe_v1.png"
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
            f"Postcard_HD_Constantinople_Front.png is {fw}x{fh}, expected 1500x1050 (PC-13, "
            f"5x3.5in @300dpi). Drawing it here would stretch it to fit the page."
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
    c.setFillColor(PAPER)
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
    c.setFillColor(PAPER)
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
    c.setFillColor(PAPER)
    c.rect(-BLEED, -BLEED, W + 2 * BLEED, H + 2 * BLEED, fill=1, stroke=0)
    c.setStrokeColor(RULE)
    c.setLineWidth(0.7)
    c.rect(10, 10, W - 20, H - 20, fill=0, stroke=1)

    left, right = 20, W - 20
    # 29 Sept 2026: message column widened -- starts 5 pt from the border (was 10) and wraps
    # 6 pt before the divider (was 12), at the user's request, on all 22 cards.
    msg_left = 15
    divider = 184
    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", 6.5)
    c.drawCentredString(W / 2, H - 20, "POST CARD")
    c.setStrokeColor(RULE)
    c.line(divider, 24, divider, H - 30)

    # Message text approved in chat (PZ-20, 17 Sept 2026). No longer a pure decoy card -- HD
    # carries the rebus third of the MEAD riddle, drawn rather than written, below.
    paragraphs = [
        "Constantinople — well, Istanbul now, but I like the old name for this trip.",
        "Impossible not to think about Harald everywhere here; this is where he made his "
        "fortune, long before Norway ever heard of him.",
        "Found this in a little shop near the Hippodrome, couldn't resist:",
    ]
    c.setFillColor(INK)
    font, size, leading = "NothingYouCouldDo", 9.5, 10.6
    y = H - 36
    for paragraph in paragraphs:
        for line in wrap_text(paragraph, font, size, divider - msg_left - 6):
            c.setFont(font, size)
            c.drawString(msg_left, y, line)
            y -= leading
        y -= 1.6

    # PZ-20, revised 29 Sept 2026: dotted sugar cubes on a spoon + yeast + reaction flask.
    # The hourglass and bubbling jar are superseded. The three icons point to fermentation.
    rebus_top = y - 4
    rebus_bottom = max(34, rebus_top - 46)
    c.setStrokeColor(RULE)
    c.setLineWidth(0.6)
    c.rect(msg_left, rebus_bottom, divider - msg_left - 6, rebus_top - rebus_bottom, fill=0, stroke=1)
    # 29 Sept 2026 review: icons lowered 3 pt to sit centred in the box, spaced evenly
    # (12 pt margins, equal gaps), and the signs drawn as 0.9 pt strokes (plus, then arrow).
    row_y = (rebus_top + rebus_bottom) / 2
    icon_xs = [msg_left + 29.75, msg_left + 87.75, msg_left + 139.5]
    draw_sugar_spoon(c, icon_xs[0], row_y)
    draw_yeast_packet(c, icon_xs[1], row_y)
    draw_reaction_flask(c, icon_xs[2], row_y)
    c.setFillColor(INK)
    # Plus drawn with the same line weight as the arrow below, so the two signs match.
    px = msg_left + 62.6
    c.setStrokeColor(INK)
    c.setLineWidth(0.9)
    c.setLineCap(1)
    c.line(px - 4, row_y, px + 4, row_y)
    c.line(px, row_y - 4, px, row_y + 4)
    # 29 Sept 2026 (user): second sign is an arrow, so the flask reads as the result of
    # sugar + yeast. Drawn, because NothingYouCouldDo has no arrow glyph.
    ax, ay = msg_left + 112.9, row_y
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

    c.setFillColor(INK)
    c.setFont("NothingYouCouldDo", 9.8)
    c.drawString(msg_left, rebus_bottom - 12, "Love,")
    c.drawString(msg_left, rebus_bottom - 23, "Aunt Liv")

    # PZ-18 element mark. Fixed position on every card -- the pocket between the
    # divider and the postmark, above the address box. See postcard_marks.py.
    draw_mark(c, "HD")

    # Same trail stamp as the other Harald cards -- one stamp per traveller, not per card.
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

    # Postmark: place only. No date drawn -- PC-03/PC-04 are still open, and PZ-08 needs those
    # dates checked against the trail-order constraint before any are printed.
    postmark_x, postmark_y = stamp_x - 5, H - 48
    c.setStrokeColor(TEAL)
    c.setLineWidth(0.8)
    c.circle(postmark_x, postmark_y, 23, fill=0, stroke=1)
    c.circle(postmark_x, postmark_y, 19.5, fill=0, stroke=1)
    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", 4.6)
    c.drawCentredString(postmark_x, postmark_y + 4, "CONSTANTI-")
    c.drawCentredString(postmark_x, postmark_y - 2, "NOPLE")
    for offset in (-7, -2, 3, 8):
        c.line(postmark_x + 23, postmark_y + offset, right, postmark_y + offset)

    # Address -- same recipient and layout as the other cards (PC-13 standard).
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
    # 26 Sept 2026: rewritten -- the old text ("wealth... funded his eventual claim to the
    # throne") was judged too close to the message's "made his fortune" line despite the
    # different wording. New fact is unrelated Constantinople trivia instead. This supersedes
    # PZ-20's design note in Norse_Brainstorm.html, which argued the old pairing didn't repeat --
    # see that note for the superseded reasoning.
    funfact_top, funfact_bottom = 120, 31
    c.setStrokeColor(FUNFACT)
    c.setLineWidth(0.6)
    c.rect(divider + 11, funfact_bottom, box_right - (divider + 11), funfact_top - funfact_bottom, fill=0, stroke=1)
    c.setFillColor(FUNFACT)
    c.setFont("Helvetica-Bold", 7.5)
    c.drawString(address_x, funfact_top - 11, "FUN FACT")
    c.setFillColor(INK)
    fact_font, fact_size, fact_leading = "Helvetica", 9, 10.7
    # 29 Sept 2026 (postcard update, batch 2 -- Aud + Harald): Fun Fact rewritten. Text from the user's Postcard
    # update tab export (small agreed fixes); message 9.5 pt / Fun Fact 9 pt (was 7.7 / 7.4).
    fact_text = (
        "A Viking carved “Halfdan was here” in runes on a marble balustrade in Hagia Sophia. It's still there."
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
        'Image adaptation: "Historical peninsula and modern skyline of Istanbul" - Hunanuk, CC0.',
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
