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


def draw_sugar_cubes(c, cx, cy, s):
    # Three small squares, stacked/offset like sugar cubes tipped from a bowl.
    c.setStrokeColor(INK)
    c.setLineWidth(0.7)
    c.setFillColor(PAPER)
    offsets = [(-s * 0.55, -s * 0.35), (s * 0.15, -s * 0.5), (-s * 0.15, s * 0.15)]
    for ox, oy in offsets:
        c.rect(cx + ox, cy + oy, s * 0.55, s * 0.55, fill=1, stroke=1)


def draw_bubbling_jar(c, cx, cy, w, h):
    # An open jar (narrow neck, rounded body), a liquid line partway up, and bubbles rising
    # above it -- read as "something fermenting", not a lidded box.
    c.setStrokeColor(INK)
    c.setLineWidth(0.8)
    c.setFillColor(PAPER)
    body_bottom, body_top = cy - h / 2, cy + h * 0.28
    neck_top = cy + h / 2
    neck_w = w * 0.5
    body_w = w
    p = c.beginPath()
    p.moveTo(cx - neck_w / 2, neck_top)
    p.lineTo(cx - neck_w / 2, body_top)
    p.curveTo(cx - body_w / 2, body_top, cx - body_w / 2, body_top, cx - body_w / 2, cy)
    p.curveTo(cx - body_w / 2, body_bottom, cx + body_w / 2, body_bottom, cx + body_w / 2, cy)
    p.curveTo(cx + body_w / 2, body_top, cx + body_w / 2, body_top, cx + neck_w / 2, body_top)
    p.lineTo(cx + neck_w / 2, neck_top)
    c.drawPath(p, fill=1, stroke=1)
    # liquid line partway up the body
    c.setLineWidth(0.6)
    c.line(cx - body_w / 2 + 1, cy - h * 0.05, cx + body_w / 2 - 1, cy - h * 0.05)
    # bubbles rising inside and just above the neck
    c.setFillColor(INK)
    bubble_spots = [(-2.2, cy - h * 0.2), (1.8, cy - h * 0.02), (-1.0, cy + h * 0.18),
                     (0.6, neck_top + 1.5), (-1.4, neck_top + 4.5)]
    for bx, by in bubble_spots:
        c.circle(cx + bx, by, 0.9, fill=1, stroke=0)


def draw_hourglass(c, cx, cy, w, h):
    # Two triangles meeting at the waist, classic hourglass silhouette, with a little sand.
    c.setStrokeColor(INK)
    c.setLineWidth(0.8)
    c.setFillColor(PAPER)
    top = cy + h / 2
    mid = cy
    bottom = cy - h / 2
    left, right = cx - w / 2, cx + w / 2
    # frame bars
    c.line(left, top, right, top)
    c.line(left, bottom, right, bottom)
    # upper triangle
    p = c.beginPath()
    p.moveTo(left, top)
    p.lineTo(right, top)
    p.lineTo(cx, mid)
    p.close()
    c.drawPath(p, fill=1, stroke=1)
    # lower triangle
    p2 = c.beginPath()
    p2.moveTo(left, bottom)
    p2.lineTo(right, bottom)
    p2.lineTo(cx, mid)
    p2.close()
    c.drawPath(p2, fill=1, stroke=1)
    # a little settled sand at the bottom
    c.setFillColor(INK)
    p3 = c.beginPath()
    p3.moveTo(cx - w * 0.18, bottom + 1.5)
    p3.lineTo(cx + w * 0.18, bottom + 1.5)
    p3.lineTo(cx, mid - h * 0.12)
    p3.close()
    c.drawPath(p3, fill=1, stroke=0)


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

    # Message text approved in chat (PZ-20, 17 Sept 2026). No longer a pure decoy card -- HD
    # carries the rebus third of the MEAD riddle, drawn rather than written, below.
    paragraphs = [
        "Constantinople — well, Istanbul now, but I like the old name for this trip.",
        "Impossible not to think about Harald everywhere here; this is where he made his "
        "fortune, long before Norway ever heard of him.",
        "Found this in a little shop near the Hippodrome, couldn't resist:",
    ]
    c.setFillColor(INK)
    font, size, leading = "NothingYouCouldDo", 7.7, 8.6
    y = H - 36
    for paragraph in paragraphs:
        for line in wrap_text(paragraph, font, size, divider - left - 12):
            c.setFont(font, size)
            c.drawString(left, y, line)
            y -= leading
        y -= 1.6

    # The rebus itself (PZ-20): sugar cubes + a bubbling jar + an hourglass, read together as
    # FERMENTED -- sugar (raw sweetness), visible fermentation, and time acting on it.
    rebus_top = y - 4
    rebus_bottom = max(34, rebus_top - 46)
    c.setStrokeColor(RULE)
    c.setLineWidth(0.6)
    c.rect(left, rebus_bottom, divider - left - 8, rebus_top - rebus_bottom, fill=0, stroke=1)
    row_y = (rebus_top + rebus_bottom) / 2 + 3
    box_w = divider - left - 8
    icon_xs = [left + box_w * 0.18, left + box_w * 0.5, left + box_w * 0.82]
    draw_sugar_cubes(c, icon_xs[0], row_y, 12)
    draw_bubbling_jar(c, icon_xs[1], row_y, 16, 22)
    draw_hourglass(c, icon_xs[2], row_y, 13, 20)
    c.setFillColor(INK)
    c.setFont("NothingYouCouldDo", 9)
    plus_y = row_y - 2.5
    c.drawCentredString((icon_xs[0] + icon_xs[1]) / 2, plus_y, "+")
    c.drawCentredString((icon_xs[1] + icon_xs[2]) / 2, plus_y, "+")

    c.setFillColor(INK)
    c.setFont("NothingYouCouldDo", 8)
    c.drawString(left, rebus_bottom - 11, "Love,")
    c.drawString(left, rebus_bottom - 20, "Aunt Liv")

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

    # Fun Fact -- typed, real trivia (PC-12), deliberately more specific than the message's own
    # "made his fortune" tease, so neither repeats the other.
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
        "Harald really did serve here — in the Byzantine emperor's own Varangian Guard, from "
        "1034 to 1043, under three different emperors. The wealth he brought home from "
        "Constantinople is what funded his eventual claim to the throne of Norway."
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
