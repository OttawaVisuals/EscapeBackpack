"""Build the Hnefatafl Museum (Oslo) admission ticket -- PZ-01 / PZ-07.

Front carries the museum branding and a plain-language explanation of the
*real* historical game (light defenders shield the king at the centre, dark
attackers close in from the edges) -- general visitor-centre copy, not the
puzzle's own house rules. Liv's actual task ("get him to a corner in exactly
three moves") lives on the Oslo postcard instead, matching PZ-01's decided
line: "Her task, on a postcard."

Back is almost entirely the blank end panel PZ-07 calls for: a short
reconstruction-caveat line up top, then the mirrored three-column offset
(columns I, J, K reversed to read K, J, I) that completes the map-back setup
panel (build_board_setup_pdf.py) when the two are butted together on their
shared grid lines. Geometry comes from board_layout.py so the two panels can
never drift out of registration.

11x11 (PZ-01, board size changed from 7x7) -- the hidden strip grew from 2
columns of 7 to 3 columns of 11, so the panel and the page it sits on both
grew to match.

Output: output/pdf/Hnefatafl_Ticket_Print.pdf, Hnefatafl_Ticket_Letter_Print.pdf
"""

from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import portrait
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from board_layout import (
    ATTACKERS, CELL, CORNERS, DEFENDERS, HIDDEN_COLS, INK, PAPER, RULE,
    RUST, SIZE,
)

from hand_drawn_board import HAND, draw_grid_ink, draw_tokens, draw_column_labels

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "output" / "pdf" / "Hnefatafl_Ticket_Print.pdf"
OUT_LETTER = ROOT / "output" / "pdf" / "Hnefatafl_Ticket_Letter_Print.pdf"
FONT_DIR = ROOT / "Fonts"

pdfmetrics.registerFont(TTFont("CinzelExtraBold", str(FONT_DIR / "Cinzel" / "static" / "Cinzel-ExtraBold.ttf")))
pdfmetrics.registerFont(TTFont("CinzelBold", str(FONT_DIR / "Cinzel" / "static" / "Cinzel-Bold.ttf")))

# 2.6 x 6.6in portrait -- tall enough for the front's full rules text and the
# back's offset panel (3 columns x 11 rows at the shared CELL size) with real
# margins. Grew from the 7x7 layout's 2.4 x 5.6in now that the hidden strip
# is 3 columns of 11 rows instead of 2 columns of 7.
PAGE = portrait((2.6 * 72, 6.6 * 72))
W, H = PAGE
LETTER = (8.5 * 72, 11 * 72)

ZEBRA = HexColor("#E7DCC0")

RULES_LINES = [
    "Light pieces defend the king at the",
    "centre of the board.",
    "",
    "Dark pieces start around the edges",
    "and try to trap him.",
    "",
    "Every piece slides any distance in a",
    "straight line, like a rook in chess.",
    "",
    "Trap an enemy piece between two of",
    "your own to capture it.",
    "",
    "The king escapes by reaching a corner.",
    "The attackers win by trapping him first.",
]

CAVEAT = (
    "No complete Viking-Age tafl ruleset survives to us today. "
    "What you see here is one modern reconstruction, pieced "
    "together from fragments, later sagas, and a fair amount "
    "of educated guessing."
)


def wrap_lines(c, text, font, size, max_width):
    c.setFont(font, size)
    words = text.split(" ")
    lines, current = [], ""
    for word in words:
        trial = (current + " " + word).strip()
        if c.stringWidth(trial, font, size) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_front(c, x=0, y=0):
    c.saveState()
    c.translate(x, y)

    c.setFillColor(PAPER)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setStrokeColor(RULE)
    c.setLineWidth(0.7)
    c.rect(6, 6, W - 12, H - 12, fill=0, stroke=1)

    c.setFillColor(INK)
    c.setFont("CinzelExtraBold", 13)
    c.drawCentredString(W / 2, H - 28, "HNEFATAFL")
    c.drawCentredString(W / 2, H - 43, "MUSEUM")
    c.setFillColor(RUST)
    c.setFont("Helvetica-Bold", 6.6)
    c.drawCentredString(W / 2, H - 55, "OSLO")
    c.setStrokeColor(INK)
    c.setLineWidth(1.0)
    c.line(16, H - 62, W - 16, H - 62)

    c.setFillColor(HexColor("#59635D"))
    c.setFont("Helvetica-Oblique", 6.6)
    c.drawCentredString(W / 2, H - 74, "the Viking game of kings and corners")

    # Simple vector board icon: 5x5 mini-grid, king at centre, a few dark
    # attacker tokens around the rim -- decorative, not the puzzle's own
    # 11x11 asymmetric layout.
    mini = 12
    gx0 = (W - 5 * mini) / 2
    gy0 = H - 200
    c.setStrokeColor(HexColor("#59635D"))
    c.setLineWidth(0.6)
    for i in range(6):
        c.line(gx0 + i * mini, gy0, gx0 + i * mini, gy0 + 5 * mini)
        c.line(gx0, gy0 + i * mini, gx0 + 5 * mini, gy0 + i * mini)
    c.setFillColor(RUST)
    c.circle(gx0 + 2.5 * mini, gy0 + 2.5 * mini, mini * 0.32, fill=1, stroke=0)
    for (dx, dy) in [(2, 0), (0, 2), (4, 2), (2, 4)]:
        c.setFillColor(INK)
        c.rect(gx0 + dx * mini + 2, gy0 + dy * mini + 2, mini - 4, mini - 4, fill=1, stroke=0)

    # Rules, plain visitor-centre copy.
    ty = gy0 - 22
    c.setFont("Helvetica", 7.6)
    for line in RULES_LINES:
        if line:
            c.setFillColor(INK)
            c.drawCentredString(W / 2, ty, line)
        ty -= 10.5

    c.setStrokeColor(RULE)
    c.setLineWidth(0.6)
    c.line(16, 22, W - 16, 22)
    c.setFillColor(HexColor("#59635D"))
    c.setFont("Helvetica", 5.6)
    c.drawCentredString(W / 2, 12, "GENERAL ADMISSION")

    c.restoreState()


def draw_mirrored_panel(c, ox, oy):
    """Reflect the original I-K pen strokes, tokens and letters as contact ink."""
    c.saveState()
    c.translate(ox + len(HIDDEN_COLS) * CELL, oy)
    c.scale(-1, 1)
    c.translate(-min(HIDDEN_COLS) * CELL, 0)
    draw_grid_ink(c, HIDDEN_COLS)
    draw_tokens(c, HIDDEN_COLS)
    draw_column_labels(c, HIDDEN_COLS)
    c.restoreState()


def draw_back(c, x=0, y=0):
    c.saveState()
    c.translate(x, y)

    c.setFillColor(PAPER)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setStrokeColor(RULE)
    c.setLineWidth(0.7)
    c.rect(6, 6, W - 12, H - 12, fill=0, stroke=1)

    c.setFillColor(INK)
    c.setFont("Helvetica-Oblique", 6.6)
    caveat_lines = wrap_lines(c, CAVEAT, "Helvetica-Oblique", 6.6, W - 36)
    ty = H - 22
    for line in caveat_lines:
        c.drawCentredString(W / 2, ty, line)
        ty -= 8.4

    # Reuse the SAME original strokes, then mirror the whole contact face.
    # This reverses tiny line irregularities and handwriting as well as positions.
    panel_w = len(HIDDEN_COLS) * CELL
    panel_h = SIZE * CELL
    ox = (W - panel_w) / 2
    oy = ty - 14 - panel_h
    draw_mirrored_panel(c, ox, oy)

    c.setFillColor(HexColor("#59635D"))
    c.setFont(HAND, 6.4)
    c.drawCentredString(W / 2, oy - 14, "hold to the light, align on the grid lines")

    c.restoreState()


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
    c.setTitle("Hnefatafl Museum Oslo - admission ticket")
    c.setAuthor("Escape Backpack")
    draw_front(c)
    c.showPage()
    draw_back(c)
    c.showPage()
    c.save()


def build_letter():
    letter_w, letter_h = LETTER
    x = (letter_w - W) / 2
    y = (letter_h - H) / 2
    c = canvas.Canvas(str(OUT_LETTER), pagesize=LETTER, pageCompression=1)
    c.setTitle("Two-up Hnefatafl ticket print sheet - front and back")
    c.setAuthor("Escape Backpack")
    draw_front(c, x, y)
    draw_crop_marks(c, x, y)
    c.showPage()
    draw_back(c, x, y)
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
