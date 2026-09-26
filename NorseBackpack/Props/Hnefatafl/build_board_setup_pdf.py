"""Build the hnefatafl board-setup insert: the panel meant for the back of
Harald's Oslo trail map (PZ-07), plus Liv's margin note beside the stain.

Also drawn on Harald's map back by build_trail_maps_pdf.py. Geometry (cell size,
piece squares) is imported from board_layout.py so it can never drift out of
registration with the ticket's mirrored offset panel (build_ticket_pdf.py).

11x11 (PZ-01, board size changed from 7x7). Attackers and defenders are drawn
as distinct tokens (dark filled vs. light outlined squares) since this layout,
unlike the old 7x7 one, includes both.

Output: output/pdf/Hnefatafl_Board_Setup_Insert.pdf
"""

from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import portrait
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from board_layout import ATTACKERS, CELL, DEFENDERS, HIDDEN_COLS, INK, PAPER, RUST, SIZE, VISIBLE_COLS
from hand_drawn_board import (
    HAND, draw_grid_ink, draw_tokens, draw_column_labels, draw_row_labels, hand_text,
)

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "output" / "pdf" / "Hnefatafl_Board_Setup_Insert.pdf"
FONT_DIR = ROOT / "Fonts"

pdfmetrics.registerFont(TTFont("CinzelExtraBold", str(FONT_DIR / "Cinzel" / "static" / "Cinzel-ExtraBold.ttf")))
pdfmetrics.registerFont(TTFont("CinzelBold", str(FONT_DIR / "Cinzel" / "static" / "Cinzel-Bold.ttf")))

MARGIN_TOP = 46      # title
MARGIN_LABEL = 16    # column-letter row above the grid
MARGIN_SIDE = 16      # row-number column left of the grid
MARGIN_BOTTOM = 62    # caption + margin note

GRID_W = SIZE * CELL
GRID_H = SIZE * CELL
W = MARGIN_SIDE + GRID_W + 14
H = MARGIN_TOP + GRID_H + MARGIN_LABEL + MARGIN_BOTTOM
PAGE = portrait((W, H))

# Organic wet-ticket smear; original asset filename retained for existing references.
# Preserve the source alpha; PDF opacity lets the registration grid show through.
# Hidden tokens are never drawn, so pale patches cannot leak their positions.
SMEAR_ART = Path(__file__).with_name("Hnefatafl_Glue_Smear_v1.png")
SMEAR_OPACITY = 0.72


def grid_origin():
    return MARGIN_SIDE, MARGIN_BOTTOM


def cell_rect(x, y):
    ox, oy = grid_origin()
    return ox + x * CELL, oy + y * CELL


def draw_grid(c):
    ox, oy = grid_origin()

    c.setFillColor(PAPER)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # Title, in Liv's practical "note to self" voice, not a puzzle-clue voice.
    c.setFillColor(INK)
    c.setFont(HAND, 16)
    c.drawCentredString(W / 2, H - 22, "Hnefatafl - board layout")
    c.setFillColor(RUST)
    c.setFont(HAND, 8.2)
    c.drawCentredString(W / 2, H - 34, "(so I don't forget!)")

    # One canonical pen drawing, reused and truly reflected on the ticket.
    c.saveState()
    c.translate(ox, oy)
    draw_grid_ink(c)
    draw_column_labels(c)
    draw_row_labels(c)
    draw_tokens(c, VISIBLE_COLS)
    c.restoreState()

    # The stain, over the hidden columns.
    hx0 = ox + min(HIDDEN_COLS) * CELL
    hy0 = oy
    hw = len(list(HIDDEN_COLS)) * CELL
    hh = GRID_H
    c.saveState()
    c.setFillAlpha(SMEAR_OPACITY)
    c.drawImage(
        ImageReader(str(SMEAR_ART)),
        hx0 - 0.28 * CELL, hy0 - 0.18 * CELL,
        width=hw + 0.75 * CELL, height=hh + 0.52 * CELL,
        mask="auto",
    )
    c.restoreState()

    # Caption -- counts rather than a full coordinate list, since 19 visible
    # pieces don't fit on one line legibly.
    visible_attackers = sum(1 for p in ATTACKERS if p[0] in VISIBLE_COLS)
    visible_defenders = sum(1 for p in DEFENDERS if p[0] in VISIBLE_COLS)
    c.setFillColor(INK)
    hand_text(c,
        f"This side: {visible_attackers} dark, {visible_defenders} light. King starts on the throne.",
        ox, oy - 14, 7.5, GRID_W)
    hand_text(c, "Escape = any corner.", ox, oy - 26, 8)

    c.setFillColor(HexColor("#59635D"))
    hand_text(c, "Oops - ticket was still wet when I set it down here.",
              ox, oy - 43, 8, GRID_W)
    hand_text(c, "Sorry, past me. - L", ox, oy - 55, 8)


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUT), pagesize=PAGE, pageCompression=1)
    c.setTitle("Hnefatafl board-setup insert (map-back panel)")
    c.setAuthor("Escape Backpack")
    draw_grid(c)
    c.showPage()
    c.save()
    print(OUT)


if __name__ == "__main__":
    main()
