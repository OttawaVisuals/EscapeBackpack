"""Aud's Treasure Museum ticket -- the sheet the treasure hunt is written on (PZ-17).

Unlike the L'Anse ticket this one has no ImageGen front art, so both faces are drawn as vector.
Same 2 x 5.5 in stock and the same palette, header band and outer rule, so the two read as
tickets from the same world.

The back carries the hunt: six legs, one per row, with three tally columns -- bridges, fords
and gates. It gives DIRECTIONS ONLY. Listing the crossings would leave nothing to solve; counting
them as you trace is the puzzle. Row 1 is pre-filled as the worked example.

Legs 5 and 6 were merged, 19 Sept 2026 -- the standing stone at H7 is no longer a named stop.
Leg 5 now runs all the way to "the village at the crossing" (H9), crossing both the H5 gate and
the H7-H9 bridge in one row. A second, identical-looking village-at-a-crossing sits near H3/G3,
well off the real route (back near the start) -- that lookalike, not a fork in the road, is the
trap now. Card A2 carries the detail that resolves it; the sheet alone cannot.
"""
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import portrait
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "output" / "pdf" / "Aud_Ticket_Print.pdf"
OUT_LETTER = ROOT / "output" / "pdf" / "Aud_Ticket_Letter_Print.pdf"
FONT_DIR = ROOT / "Fonts"

PAGE = portrait((2 * 72, 5.5 * 72))
W, H = PAGE
LETTER = (8.5 * 72, 11 * 72)

PAPER = HexColor("#EFE3C4")
ZEBRA = HexColor("#E7DCC0")
INK = HexColor("#283B34")
RUST = HexColor("#B56A2A")
RULE = HexColor("#A99A7B")
CREAM = HexColor("#F4EEDD")
SOFT = HexColor("#59635D")
PURPLE = HexColor("#6D528B")

pdfmetrics.registerFont(TTFont("CinzelExtraBold", str(FONT_DIR / "Cinzel" / "static" / "Cinzel-ExtraBold.ttf")))
pdfmetrics.registerFont(TTFont("CinzelBold", str(FONT_DIR / "Cinzel" / "static" / "Cinzel-Bold.ttf")))

MARGIN = 9
HEADER_H = 78

# Directions only -- never what they cross. Leg 1's answer is printed as the worked example.
LEGS = [
    "From the chapel, follow the road east to the next chapel.",
    "Take the road south-west and keep to it as far as the well at the fork.",
    "From the well the road runs south to the landing.",
    "Follow the long road east to the standing stone by the church.",
    "Follow the road to the village at the crossing.",
    "Where the road ends at the ruin, search the wood beyond.",
]
WORKED = (1, 0, 0)          # leg 1: one bridge, no ford, no gate
ANSWER = (5, 2, 1)          # the full tally, for the answer copy only


def wrap(c, text, font, size, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if pdfmetrics.stringWidth(trial, font, size) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_front_card(c, x=0, y=0):
    c.saveState()
    c.translate(x, y)
    c.setFillColor(PAPER)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    c.setFillColor(INK)
    c.rect(0, H - HEADER_H, W, HEADER_H, fill=1, stroke=0)
    c.setFillColor(CREAM)
    c.setFont("CinzelExtraBold", 11)
    c.drawCentredString(W / 2, H - 22, "AUÐAR")
    c.drawCentredString(W / 2, H - 35, "SAFN")
    c.setStrokeColor(RUST)
    c.setLineWidth(1.1)
    c.line(20, H - 44, W - 20, H - 44)
    c.setFillColor(RUST)
    c.setFont("Helvetica-Bold", 6.0)
    c.drawCentredString(W / 2, H - 55, "TREASURE MUSEUM")
    c.setFillColor(CREAM)
    c.setFont("Helvetica", 5.2)
    c.drawCentredString(W / 2, H - 67, "HVAMMUR · DALIR")

    c.setStrokeColor(RULE)
    c.setLineWidth(0.7)
    c.rect(6, 6, W - 12, H - 12, fill=0, stroke=1)

    cx = W / 2
    ty = H - HEADER_H - 30
    c.setFillColor(INK)
    c.setFont("CinzelBold", 9)
    c.drawCentredString(cx, ty, "ADMIT ONE")
    c.setStrokeColor(RULE)
    c.setLineWidth(0.5)
    c.line(MARGIN + 8, ty - 10, W - MARGIN - 8, ty - 10)

    c.setFillColor(SOFT)
    c.setFont("Helvetica", 5.6)
    for i, (label, value) in enumerate([("VALID", "DAY OF ISSUE"),
                                        ("ADMISSION", "INCL. TREASURE HUNT"),
                                        ("GUIDE", "SELF-LED")]):
        yy = ty - 26 - i * 16
        c.setFillColor(SOFT)
        c.setFont("Helvetica-Bold", 5.0)
        c.drawString(MARGIN + 8, yy, label)
        c.setFillColor(INK)
        c.setFont("Helvetica", 6.0)
        c.drawRightString(W - MARGIN - 8, yy, value)
        c.setStrokeColor(HexColor("#DCD2B8"))
        c.setLineWidth(0.4)
        c.line(MARGIN + 8, yy - 5, W - MARGIN - 8, yy - 5)

    c.setFillColor(SOFT)
    c.setFont("Helvetica-Oblique", 5.4)
    for i, ln in enumerate(["The valley she claimed, the ships she",
                            "freed, and what the ground still keeps."]):
        c.drawCentredString(cx, ty - 84 - i * 8, ln)

    # A plain rust lozenge stands in for a crest: the museum has no logo asset yet.
    c.setStrokeColor(RUST)
    c.setLineWidth(0.9)
    c.setFillColor(PAPER)
    c.circle(cx, ty - 126, 17, fill=1, stroke=1)
    c.setFillColor(RUST)
    c.setFont("CinzelBold", 12)
    c.drawCentredString(cx, ty - 130, "A")

    c.setStrokeColor(HexColor("#DCD2B8"))
    c.setLineWidth(0.4)
    c.line(MARGIN + 20, ty - 156, W - MARGIN - 20, ty - 156)
    c.setFillColor(SOFT)
    c.setFont("Helvetica-Bold", 4.6)
    c.drawCentredString(cx, ty - 168, "OPEN DAILY · 10 – 17")

    c.setFillColor(SOFT)
    c.setFont("Helvetica", 5.0)
    c.drawCentredString(cx, 44, "TURN OVER FOR THE")
    c.drawCentredString(cx, 36, "TREASURE HUNT")
    c.setStrokeColor(RULE)
    c.setLineWidth(0.5)
    c.line(MARGIN + 6, 22, W - MARGIN - 6, 22)
    c.setFont("Helvetica", 5.2)
    # Deliberately unrelated to the code: an earlier draft read "No. 531-A", which
    # printed the answer on the front of the ticket.
    c.drawCentredString(cx, 12, "No. 209418")
    c.restoreState()


def draw_back_card(c, x=0, y=0, answer=False):
    c.saveState()
    c.translate(x, y)
    c.setFillColor(PAPER)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    band = 56
    c.setFillColor(INK)
    c.rect(0, H - band, W, band, fill=1, stroke=0)
    c.setFillColor(CREAM)
    c.setFont("CinzelExtraBold", 10)
    c.drawCentredString(W / 2, H - 20, "TREASURE HUNT")
    c.setStrokeColor(RUST)
    c.setLineWidth(1.0)
    c.line(20, H - 28, W - 20, H - 28)
    c.setFillColor(RUST)
    c.setFont("Helvetica-Bold", 5.2)
    c.drawCentredString(W / 2, H - 38, "TRACE THE ROUTE ON YOUR MAP")
    c.setFillColor(CREAM)
    c.setFont("Helvetica", 4.8)
    c.drawCentredString(W / 2, H - 48, "COUNT WHAT YOU CROSS")

    c.setStrokeColor(RULE)
    c.setLineWidth(0.7)
    c.rect(6, 6, W - 12, H - 12, fill=0, stroke=1)

    left = MARGIN + 3
    right = W - MARGIN - 3
    box_w = 12.0
    gap = 2.0
    tally_w = box_w * 3 + gap * 2
    tally_x = right - tally_w
    text_w = tally_x - left - 14 - 4          # 14pt for the leg number column

    # column heads
    head_y = H - band - 12
    c.setFillColor(SOFT)
    c.setFont("Helvetica-Bold", 4.4)
    for i, lab in enumerate(("BRG", "FRD", "GTE")):
        c.drawCentredString(tally_x + box_w * i + box_w / 2 + gap * i, head_y, lab)
    c.setStrokeColor(RULE)
    c.setLineWidth(0.5)
    c.line(left, head_y - 4, right, head_y - 4)

    top = head_y - 8
    bottom = 30
    # measure first so a too-long leg fails loudly instead of overflowing the card
    line_h = 6.0
    blocks = [wrap(c, t, "Helvetica", 5.3, text_w) for t in LEGS]
    needed = sum(max(len(b) * line_h + 7.0, box_w + 7.0) for b in blocks)
    if needed > top - bottom:
        raise ValueError("leg text needs %.1fpt but only %.1fpt is available on the card"
                         % (needed, top - bottom))
    pad = (top - bottom - needed) / len(LEGS)

    yy = top
    for i, (leg, lines) in enumerate(zip(LEGS, blocks), start=1):
        rows_h = max(len(lines) * line_h + 7.0, box_w + 7.0) + pad
        if i % 2 == 0:
            c.setFillColor(ZEBRA)
            c.rect(6, yy - rows_h, W - 12, rows_h, fill=1, stroke=0)
        c.setFillColor(RUST)
        c.setFont("Helvetica-Bold", 6.4)
        c.drawString(left, yy - 9, str(i))
        c.setFillColor(INK)
        c.setFont("Helvetica", 5.3)
        for k, ln in enumerate(lines):
            c.drawString(left + 14, yy - 8 - k * line_h, ln)
        # three tally boxes
        for b in range(3):
            bx = tally_x + b * (box_w + gap)
            by = yy - 4 - box_w
            c.setStrokeColor(RULE)
            c.setLineWidth(0.5)
            c.setFillColor(CREAM)
            c.rect(bx, by, box_w, box_w, fill=1, stroke=1)
            val = None
            if i == 1:
                val = WORKED[b]
            elif answer:
                per = PER_LEG[i - 1]
                val = per[b]
            if val is not None:
                c.setFillColor(PURPLE if i == 1 else RUST)
                c.setFont("Helvetica-Bold", 6.2)
                c.drawCentredString(bx + box_w / 2, by + 3.4, str(val))
        yy -= rows_h

    c.setStrokeColor(RULE)
    c.setLineWidth(0.5)
    c.line(left, 24, right, 24)
    c.setFillColor(SOFT)
    c.setFont("Helvetica", 4.4)
    c.drawCentredString(W / 2, 16, "BRG BRIDGES · FRD FORDS · GTE GATES")
    if answer:
        c.setFillColor(RUST)
        c.setFont("Helvetica-Bold", 6.0)
        c.drawCentredString(W / 2, 8, "ANSWER  %d %d %d" % ANSWER)
    else:
        c.setFillColor(SOFT)
        c.setFont("Helvetica", 4.4)
        c.drawCentredString(W / 2, 8, "LEG 1 FILLED IN · TOTAL EACH COLUMN")
    c.restoreState()


# per-leg answers, used only on the designer copy
PER_LEG = [(1, 0, 0), (1, 2, 0), (1, 0, 0), (1, 0, 0), (1, 0, 1), (0, 0, 0)]
assert tuple(sum(p[i] for p in PER_LEG) for i in range(3)) == ANSWER


def draw_crop_marks(c, x, y):
    c.saveState()
    c.setStrokeColor(HexColor("#777777"))
    c.setLineWidth(0.35)
    gap, length = 3, 8
    for px in (x, x + W):
        c.line(px, y - gap, px, y - gap - length)
        c.line(px, y + H + gap, px, y + H + gap + length)
    for py in (y, y + H):
        c.line(x - gap, py, x - gap - length, py)
        c.line(x + W + gap, py, x + W + gap + length, py)
    c.restoreState()


def build_single():
    c = canvas.Canvas(str(OUT), pagesize=PAGE, pageCompression=1)
    c.setTitle("Audar Safn - treasure museum ticket")
    c.setAuthor("Escape Backpack")
    draw_front_card(c)
    c.showPage()
    draw_back_card(c)
    c.showPage()
    draw_back_card(c, answer=True)
    c.showPage()
    c.save()


def build_letter():
    lw, lh = LETTER
    x, y = (lw - W) / 2, (lh - H) / 2
    c = canvas.Canvas(str(OUT_LETTER), pagesize=LETTER, pageCompression=1)
    c.setTitle("Aud ticket print sheet - front and back")
    c.setAuthor("Escape Backpack")
    draw_front_card(c, x, y)
    draw_crop_marks(c, x, y)
    c.showPage()
    draw_back_card(c, x, y)
    draw_crop_marks(c, x, y)
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
