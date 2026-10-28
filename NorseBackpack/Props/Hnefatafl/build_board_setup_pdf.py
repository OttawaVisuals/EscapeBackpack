"""Build the hnefatafl board-setup insert: the panel meant for the back of
Harald's Oslo trail map (PZ-07), plus Liv's margin note beside the stain.

Also drawn on Harald's map back by build_trail_maps_pdf.py. Geometry (cell size,
piece squares) is imported from board_layout.py so it can never drift out of
registration with the ticket's mirrored offset panel (build_ticket_pdf.py).

11x11 (PZ-01, board size changed from 7x7). Attackers and defenders are drawn
as distinct tokens (dark filled vs. light outlined squares) since this layout,
unlike the old 7x7 one, includes both.

Output: NorseBackpack/Print/_pdf_source/Hnefatafl_Board_Setup_Insert.pdf
"""

import math
import random
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import portrait
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from board_layout import ATTACKERS, BLACK_MOVES, CELL, DEFENDERS, HIDDEN_COLS, INK, PAPER, RUST, SIZE, VISIBLE_COLS
from hand_drawn_board import (
    HAND, draw_grid_ink, draw_tokens, draw_column_labels, draw_row_labels, hand_text, pen_line,
)

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "NorseBackpack" / "Print" / "_pdf_source" / "Hnefatafl_Board_Setup_Insert.pdf"
FONT_DIR = ROOT / "Fonts"

pdfmetrics.registerFont(TTFont("CinzelExtraBold", str(FONT_DIR / "Cinzel" / "static" / "Cinzel-ExtraBold.ttf")))
pdfmetrics.registerFont(TTFont("CinzelBold", str(FONT_DIR / "Cinzel" / "static" / "Cinzel-Bold.ttf")))

MARGIN_TOP = 46      # title
MARGIN_LABEL = 16    # column-letter row above the grid
MARGIN_SIDE = 16      # row-number column left of the grid
MARGIN_BOTTOM = 130    # caption + margin note

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
# Under the stain the grid lines read as untouched while the pieces are gone (user,
# 7 Oct 2026). A wash in the page colour, shaped by the smear's own alpha, erases the
# straight pen lines there; smudged copies (wavy, dragged, blurred, broken) are drawn
# in their place, so the grid is still faintly traceable for registration.
LINE_FADE = 1.0
SMUDGE_SEED = 1171
SMUDGE_INK = (0x59, 0x63, 0x5D)   # hand_drawn_board.GRID_INK


def _png(img):
    buf = BytesIO()
    img.save(buf, "PNG")
    buf.seek(0)
    return ImageReader(buf)


def _smear_alpha():
    """Where the stain lies, as a mask. The artwork's own alpha is low in its pale
    middle, so it is boosted: inside the stain counts fully, only the edge ramps."""
    alpha = Image.open(SMEAR_ART).convert("RGBA").getchannel("A")
    return alpha.point(lambda v: min(255, v * 5)).filter(ImageFilter.GaussianBlur(2))


def _smear_wash(color):
    """The smear's alpha channel filled with one flat colour."""
    alpha = _smear_alpha()
    rgb = tuple(round(v * 255) for v in (color.red, color.green, color.blue))
    wash = Image.new("RGBA", alpha.size, rgb + (255,))
    wash.putalpha(alpha)
    return _png(wash)


def _smudged_lines(box, ox, oy):
    """The hidden columns' grid lines as if dragged through wet glue: each line wanders,
    thickens and thins, drops out in places and trails downward, then is blurred and
    kept only where the smear lies (its alpha), so it meets the clean pen line at the
    stain's edge."""
    alpha = _smear_alpha()
    iw, ih = alpha.size
    bx, by, bw, bh = box
    sx, sy = iw / bw, ih / bh

    def px(x, y):
        return (x - bx) * sx, (by + bh - y) * sy

    rng = random.Random(SMUDGE_SEED)

    def wave(n, amp, cycles=1.0):
        phases = [(rng.uniform(0, 6.28), rng.uniform(0.6, 1.4) * k * cycles)
                  for k in (1.0, 2.3, 4.7)]
        return [amp * sum(math.sin(p + f * 6.28 * t) / (1 + j)
                          for j, (p, f) in enumerate(phases))
                for t in (i / n for i in range(n + 1))]

    lines = [((ox + k * CELL, oy), (ox + k * CELL, oy + GRID_H)) for k in range(8, SIZE + 1)]
    lines += [((ox + 7.6 * CELL, oy + r * CELL), (ox + SIZE * CELL + 0.2 * CELL, oy + r * CELL))
              for r in range(SIZE + 1)]

    ink = Image.new("L", alpha.size, 0)
    draw = ImageDraw.Draw(ink)
    for (x0, y0), (x1, y1) in lines:
        a, b = px(x0, y0), px(x1, y1)
        length = math.hypot(b[0] - a[0], b[1] - a[1])
        n = max(8, int(length / 6))
        nx, ny = -(b[1] - a[1]) / length, (b[0] - a[0]) / length      # unit normal
        cycles = length / (3 * CELL * sy)                              # long lines wander more often
        off = wave(n, 1.4 * sx, max(1.0, cycles))                      # up to ~2.5 pt sideways
        drag = wave(n, 1.6 * sy)                                       # downward pull
        fade = wave(n, 0.9, max(1.0, cycles))
        width = wave(n, 2.2)
        pts = []
        for i in range(n + 1):
            t = i / n
            x = a[0] + (b[0] - a[0]) * t + nx * off[i]
            y = a[1] + (b[1] - a[1]) * t + ny * off[i] + abs(drag[i])
            pts.append((x, y))
        for i in range(n):
            level = max(0.0, min(1.0, 0.55 + 0.45 * fade[i]))         # breaks where < 0
            if level < 0.08:
                continue
            w = max(2, int(4.5 + width[i]))
            draw.line([pts[i], pts[i + 1]], fill=int(200 * level), width=w)
    # Dragged tail: stacked, fading copies pulled down the stain.
    tail = ink.copy()
    for step in range(1, 6):
        shifted = Image.new("L", ink.size, 0)
        shifted.paste(ink.point(lambda v, s=step: int(v * (0.5 ** s))), (0, step * 5))
        tail = ImageChops.lighter(tail, shifted)
    tail = tail.filter(ImageFilter.GaussianBlur(3.2))
    mask = ImageChops.multiply(tail, alpha)
    out = Image.new("RGBA", alpha.size, SMUDGE_INK + (255,))
    out.putalpha(mask)
    return _png(out)


PENCIL = HexColor("#4A4A4A")

# Liv's note under the board (17 Oct 2026, PZ-008). The first two dark moves are the numbered
# arrows; the third is the riddle; the last is on Harald's map and the ticket, so the note stays vague.
LIV_NOTE = ("Silly sausage me, I smudged part of the board with my wet museum ticket. "
            "Not to worry, for the 3rd attacker move solve this riddle: "
            "The attacker on the second-highest row steps up to the top row. "
            "For the last attacker move, you might have to look somewhere else for it.")


def draw_move_arrows(c):
    """Numbered pencil arrows for the first two dark moves (BLACK_MOVES[0] and [1]). Drawn in the
    board's own coordinates (called inside the translate to the grid origin). Visible columns only."""
    c.saveState()
    c.setLineCap(1)
    c.setStrokeColor(PENCIL)
    c.setFillColor(PENCIL)
    for n, ((fx, fy), (tx, ty)) in enumerate(BLACK_MOVES[:2], start=1):
        assert fx in VISIBLE_COLS and tx in VISIBLE_COLS, "arrows must sit on the visible columns"
        x0, y0 = (fx + 0.5) * CELL, (fy + 0.5) * CELL
        x1, y1 = (tx + 0.5) * CELL, (ty + 0.5) * CELL
        dx, dy = x1 - x0, y1 - y0
        length = math.hypot(dx, dy)
        ux, uy = dx / length, dy / length
        a = (x0 + ux * CELL * 0.38, y0 + uy * CELL * 0.38)       # leave the piece
        b = (x1 - ux * CELL * 0.30, y1 - uy * CELL * 0.30)       # stop short of the centre
        pen_line(c, a, b, 7100 + n, wobble=0.9, width=1.5)
        nx, ny = -uy, ux
        for side in (1, -1):
            h = (b[0] - ux * 6.5 + nx * 3.6 * side, b[1] - uy * 6.5 + ny * 3.6 * side)
            pen_line(c, b, h, 7200 + n * 2 + (side > 0), wobble=0.3, width=1.5)
        mx, my = (a[0] + b[0]) / 2 - 11, (a[1] + b[1]) / 2          # number to the left of the shaft
        c.setFont(HAND, 11)
        c.drawCentredString(mx, my - 3.5, str(n))
        c.setLineWidth(0.9)
        c.circle(mx, my, 6.2, stroke=1, fill=0)
    c.restoreState()


def grid_origin():
    return MARGIN_SIDE, MARGIN_BOTTOM


def cell_rect(x, y):
    ox, oy = grid_origin()
    return ox + x * CELL, oy + y * CELL


def draw_grid(c, background=True):
    """background=False leaves the panel unfilled: the standalone insert prints on a
    white Letter page, where a paper-tone block looked pasted on (7 Oct 2026)."""
    ox, oy = grid_origin()

    if background:
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
    draw_move_arrows(c)
    c.restoreState()

    # The stain, over the hidden columns.
    hx0 = ox + min(HIDDEN_COLS) * CELL
    hy0 = oy
    hw = len(list(HIDDEN_COLS)) * CELL
    hh = GRID_H
    box = (hx0 - 0.28 * CELL, hy0 - 0.18 * CELL, hw + 0.75 * CELL, hh + 0.52 * CELL)
    c.saveState()
    c.setFillAlpha(LINE_FADE)
    c.drawImage(_smear_wash(PAPER if background else HexColor("#FFFFFF")),
                box[0], box[1], width=box[2], height=box[3], mask="auto")
    c.setFillAlpha(1)
    c.drawImage(_smudged_lines(box, ox, oy), box[0], box[1],
                width=box[2], height=box[3], mask="auto")
    c.setFillAlpha(SMEAR_OPACITY)
    c.drawImage(ImageReader(str(SMEAR_ART)), box[0], box[1],
                width=box[2], height=box[3], mask="auto")
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
    line, ly = "", oy - 43
    for word in LIV_NOTE.split(" "):
        trial = (line + " " + word).strip()
        if pdfmetrics.stringWidth(trial, HAND, 8.4) > GRID_W:
            hand_text(c, line, ox, ly, 8.4)
            ly -= 11.5
            line = word
        else:
            line = trial
    hand_text(c, line, ox, ly, 8.4)
    hand_text(c, "- L", ox, ly - 12, 8.4)


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUT), pagesize=PAGE, pageCompression=1)
    c.setTitle("Hnefatafl board-setup insert (map-back panel)")
    c.setAuthor("Escape Backpack")
    draw_grid(c, background=False)
    c.showPage()
    c.save()
    print(OUT)


if __name__ == "__main__":
    main()
