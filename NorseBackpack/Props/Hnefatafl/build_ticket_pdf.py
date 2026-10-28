# PRINT LAYOUT SUPERSEDED 20 Oct 2026: use Props/build_museum_bookmarks.py for current 2 x 6 museum tickets.
"""Build the Hnefatafl Museum (Oslo) admission ticket -- PZ-01 / PZ-07.

Front carries the museum branding and a plain-language explanation of the
*real* historical game (light defenders shield the king at the centre, dark
attackers close in from the edges) -- general visitor-centre copy, not the
puzzle's own house rules. Liv's actual task ("get him to a corner in exactly
three moves") lives on the Oslo postcard instead, matching PZ-01's decided
line: "Her task, on a postcard."

Back is only the end panel PZ-07 calls for, with no text beyond the
mirrored column letters: the mirrored three-column offset
(columns I, J, K reversed to read K, J, I) that completes the map-back setup
panel (build_board_setup_pdf.py) when the two are butted together on their
shared grid lines. Geometry comes from board_layout.py so the two panels can
never drift out of registration.

11x11 (PZ-01, board size changed from 7x7) -- the hidden strip grew from 2
columns of 7 to 3 columns of 11, so the panel and the page it sits on both
grew to match.

Output: NorseBackpack/Print/_pdf_source/Hnefatafl_Ticket_Print.pdf, Hnefatafl_Ticket_Letter_Print.pdf
"""

from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import portrait
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from board_layout import (
    ATTACKERS, CELL, CORNERS, DEFENDERS, HIDDEN_COLS, INK, PAPER, RULE,
    RUST, SIZE,
)

from hand_drawn_board import HAND, draw_grid_ink, draw_tokens, draw_column_labels

ROOT = Path(__file__).resolve().parents[3]
# 17 Oct 2026: the hand-drawn hnefatafl shield (Codex), also printed on Harald's map at the last
# black move's square; shown here, without a caption, so players link the two.
SHIELD_ICON = Path(__file__).with_name("Hnefatafl_Shield_Icon_HandDrawn_v1.png")
# 17 Oct 2026: the ticket back uses Codex's wet-ink transfer of the strip (the same drawing as the
# vector strip, same size and place, with the smudge) when this file exists. Delete or rename it to
# fall back to the clean vector strip. Checked: five dark squares at K10, K4, I9, I8, I6, no piece
# on K8, centres within about 0.5 mm of the clean strip.
SMUDGED_BACK = Path(__file__).with_name("Hnefatafl_Ticket_Back_Smudged_2134_v1.png")
OUT = ROOT / "NorseBackpack" / "Print" / "_pdf_source" / "Hnefatafl_Ticket_Print.pdf"
OUT_LETTER = ROOT / "NorseBackpack" / "Print" / "_pdf_source" / "Hnefatafl_Ticket_Letter_Print.pdf"
FONT_DIR = ROOT / "Fonts"

pdfmetrics.registerFont(TTFont("CinzelExtraBold", str(FONT_DIR / "Cinzel" / "static" / "Cinzel-ExtraBold.ttf")))
pdfmetrics.registerFont(TTFont("CinzelBold", str(FONT_DIR / "Cinzel" / "static" / "Cinzel-Bold.ttf")))

# 2.6 x 5.2in portrait -- sized to the back's offset panel (3 columns x 11 rows
# at the shared CELL size, plus its column letters) with even margins; the
# front's rules text fits inside the same height.
PAGE = portrait((2.6 * 72, 5.2 * 72))
W, H = PAGE
LETTER = (8.5 * 72, 11 * 72)

ZEBRA = HexColor("#E7DCC0")

RULES_LINES = [
    "Light pieces defend the king at the",
    "centre of the board.",
    "",
    "Dark pieces start around the edges,",
    "move first and try to trap him.",
    "",
    "Every piece slides any distance in a",
    "straight line, like a rook in chess.",
    "",
    "Trap an enemy piece between two of",
    "your own to capture it.",
    "",
    "The king escapes by reaching a corner.",
    "The attackers win by trapping him first.",
    "",
    "The king is captured only when dark",
    "pieces surround him on all four",
    "sides (the board edge counts).",
]

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

    icon = 36
    c.drawImage(ImageReader(str(SHIELD_ICON)), (W - icon) / 2, H - 80 - icon, icon, icon, mask="auto")

    # Capture diagram (playtest 1, 11 Oct 2026). This was a 5x5 mini-board with the king and
    # four dark pieces, which players read as a starting position to copy. Now a three-square
    # strip -- dark, light, dark -- with the light piece struck out: it shows the capture rule
    # and cannot be mistaken for a setup. Chosen in chat over removing it or a king drawing.
    gy0 = H - 150                       # rules below still hang from here, as before
    cell = 18
    sx0, sy0 = (W - 3 * cell) / 2, gy0 + 28 - 15     # 15 pt lower since the shield icon (17 Oct 2026)
    c.setStrokeColor(HexColor("#59635D"))
    c.setLineWidth(0.6)
    c.rect(sx0, sy0, 3 * cell, cell, fill=0, stroke=1)
    c.line(sx0 + cell, sy0, sx0 + cell, sy0 + cell)
    c.line(sx0 + 2 * cell, sy0, sx0 + 2 * cell, sy0 + cell)
    r = cell * 0.3
    c.setFillColor(INK)
    for i in (0, 2):
        c.circle(sx0 + (i + 0.5) * cell, sy0 + cell / 2, r, fill=1, stroke=0)
    c.setFillColor(PAPER)
    c.setStrokeColor(INK)
    c.setLineWidth(0.8)
    mx, my = sx0 + 1.5 * cell, sy0 + cell / 2
    c.circle(mx, my, r, fill=1, stroke=1)
    c.setStrokeColor(RUST)
    c.setLineWidth(1.2)
    d = r * 0.95
    c.line(mx - d, my - d, mx + d, my + d)
    c.line(mx - d, my + d, mx + d, my - d)
    c.setFillColor(HexColor("#59635D"))
    c.setFont("Helvetica-Oblique", 6.2)
    c.drawCentredString(W / 2, sy0 - 11, "trapped between two: captured")

    # Rules, plain visitor-centre copy.
    ty = gy0 - 22
    c.setFont("Helvetica", 7.4)
    for line in RULES_LINES:
        if line:
            c.setFillColor(INK)
            c.drawCentredString(W / 2, ty, line)
        ty -= 9.4

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

    if SMUDGED_BACK.exists():
        # whole-card image (887 x 1774 px = 2.6 x 5.2 in), already carrying paper tone, border and strip
        c.drawImage(ImageReader(str(SMUDGED_BACK)), 0, 0, W, H)
        c.restoreState()
        return

    c.setFillColor(PAPER)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setStrokeColor(RULE)
    c.setLineWidth(0.7)
    c.rect(6, 6, W - 12, H - 12, fill=0, stroke=1)

    # Reuse the SAME original strokes, then mirror the whole contact face.
    # This reverses tiny line irregularities and handwriting as well as positions.
    panel_w = len(HIDDEN_COLS) * CELL
    panel_h = SIZE * CELL
    ox = (W - panel_w) / 2
    # Centre panel plus its column letters (about 14pt above) vertically.
    oy = (H - panel_h - 14) / 2
    draw_mirrored_panel(c, ox, oy)

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
