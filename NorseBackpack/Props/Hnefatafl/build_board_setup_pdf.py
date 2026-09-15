"""Build the hnefatafl board-setup insert: the panel meant for the back of
Harald's Oslo trail map (PZ-07), plus Liv's margin note beside the stain.

Harald has no trail map sheet yet (build_trail_maps_pdf.py has no TRAILS entry
for him), so this is a standalone insert sized to drop onto that map's back
once it exists -- not yet composited onto a real sheet. Geometry (cell size,
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
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from board_layout import (
    ATTACKERS, CELL, CORNERS, DEFENDERS, HIDDEN_COLS, INK, PAPER, RULE,
    RUST, SIZE, STAIN, THRONE, VISIBLE_COLS,
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

# Irregular stain outline over the hidden columns, hand-picked offsets so the
# blot's edge is uneven rather than a clean rectangle (PZ-07's own
# requirement). Coordinates are fractions of the hidden strip's own bounding
# box, in drawing order around the perimeter.
STAIN_OUTLINE = [
    (-0.14, 0.03), (0.18, -0.06), (0.42, -0.02), (0.64, 0.07),
    (0.86, 0.04), (1.08, 0.10), (1.14, 0.30), (1.06, 0.50),
    (1.12, 0.68), (1.02, 0.86), (1.10, 1.02), (0.80, 0.98),
    (0.58, 1.08), (0.34, 0.97), (0.12, 1.06), (-0.10, 0.90),
    (0.00, 0.70), (-0.16, 0.52), (-0.02, 0.34), (-0.18, 0.18),
]


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
    c.setFont("CinzelBold", 12.5)
    c.drawCentredString(W / 2, H - 22, "HNEFATAFL — BOARD LAYOUT")
    c.setFillColor(RUST)
    c.setFont("Helvetica-Oblique", 7.5)
    c.drawCentredString(W / 2, H - 34, "(so I don't forget!)")

    # Grid lines.
    c.setStrokeColor(HexColor("#59635D"))
    c.setLineWidth(0.7)
    for i in range(SIZE + 1):
        c.line(ox + i * CELL, oy, ox + i * CELL, oy + GRID_H)
        c.line(ox, oy + i * CELL, ox + GRID_W, oy + i * CELL)

    # Column letters (top) and row numbers (left) -- columns under the stain
    # are added too, then painted over, so they visibly run into it rather
    # than stopping short of it.
    c.setFont("Helvetica-Bold", 7.5)
    c.setFillColor(INK)
    for x in range(SIZE):
        cx = ox + x * CELL + CELL / 2
        c.drawCentredString(cx, oy + GRID_H + 4, chr(65 + x))
    for y in range(SIZE):
        cy = oy + y * CELL + CELL / 2 - 3
        c.drawRightString(ox - 4, cy, str(y + 1))

    # Corner markers (open diamond). Only the two on the visible side are
    # drawn here -- the two under the stain never got drawn in the first
    # place, so the stain has nothing to hide but paper.
    for (x, y) in CORNERS:
        if x not in VISIBLE_COLS:
            continue
        px, py = cell_rect(x, y)
        cx, cy = px + CELL / 2, py + CELL / 2
        r = CELL * 0.26
        c.setStrokeColor(RUST)
        c.setLineWidth(1.1)
        c.setFillColor(PAPER)
        p = c.beginPath()
        p.moveTo(cx, cy + r)
        p.lineTo(cx + r, cy)
        p.lineTo(cx, cy - r)
        p.lineTo(cx - r, cy)
        p.close()
        c.drawPath(p, fill=0, stroke=1)

    # Throne (filled circle, distinct from either piece token).
    tx, ty = cell_rect(*THRONE)
    c.setFillColor(RUST)
    c.circle(tx + CELL / 2, ty + CELL / 2, CELL * 0.24, fill=1, stroke=0)

    # Attackers (solid dark square) and defenders (light square, dark
    # outline) -- distinct tokens now that this layout has both. Same rule as
    # before: pieces on the hidden side are never drawn, so the stain covers
    # nothing but paper.
    pad = CELL * 0.2
    for (x, y) in ATTACKERS:
        if x not in VISIBLE_COLS:
            continue
        px, py = cell_rect(x, y)
        c.setFillColor(INK)
        c.rect(px + pad, py + pad, CELL - 2 * pad, CELL - 2 * pad, fill=1, stroke=0)
    for (x, y) in DEFENDERS:
        if x not in VISIBLE_COLS:
            continue
        px, py = cell_rect(x, y)
        c.setFillColor(PAPER)
        c.setStrokeColor(INK)
        c.setLineWidth(1.1)
        c.rect(px + pad, py + pad, CELL - 2 * pad, CELL - 2 * pad, fill=1, stroke=1)

    # The stain, over the hidden columns.
    hx0 = ox + min(HIDDEN_COLS) * CELL
    hy0 = oy
    hw = len(list(HIDDEN_COLS)) * CELL
    hh = GRID_H
    c.saveState()
    c.setFillColor(STAIN)
    c.setFillAlpha(0.82)
    path = c.beginPath()
    for i, (fx, fy) in enumerate(STAIN_OUTLINE):
        px = hx0 + fx * hw
        py = hy0 + fy * hh
        if i == 0:
            path.moveTo(px, py)
        else:
            path.lineTo(px, py)
    path.close()
    c.drawPath(path, fill=1, stroke=0)
    c.restoreState()

    # Caption -- counts rather than a full coordinate list, since 19 visible
    # pieces don't fit on one line legibly.
    visible_attackers = sum(1 for p in ATTACKERS if p[0] in VISIBLE_COLS)
    visible_defenders = sum(1 for p in DEFENDERS if p[0] in VISIBLE_COLS)
    c.setFillColor(INK)
    c.setFont("Helvetica", 7.2)
    c.drawString(
        ox, oy - 14,
        f"This side: {visible_attackers} dark, {visible_defenders} light. King starts on the throne."
    )
    c.setFont("Helvetica", 7.0)
    c.drawString(ox, oy - 25, "Escape = any corner.")

    # Liv's own margin apology, small and handwritten in tone, tucked under
    # the caption rather than explaining the puzzle.
    c.setFillColor(HexColor("#59635D"))
    c.setFont("Helvetica-Oblique", 6.8)
    c.drawString(ox, oy - 42, "Oops — ticket was still wet with glue when I set it down here.")
    c.drawString(ox, oy - 52, "Sorry, past me. — L")


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
