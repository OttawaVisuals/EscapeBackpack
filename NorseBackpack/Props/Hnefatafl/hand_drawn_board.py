"""One repeatable pen drawing for the map and its genuinely mirrored ticket strip.

Grid intersections retain board_layout.CELL exactly. Cubic strokes wander only
between intersections. Seeds depend on canonical board coordinates, never on
which panel is being drawn, so the reverse transfer is the same original ink.
"""
import math
import random
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from board_layout import ATTACKERS, CELL, CORNERS, DEFENDERS, INK, RUST, SIZE, THRONE

HAND = "LivBoardHand"
pdfmetrics.registerFont(TTFont(HAND, str(Path(__file__).resolve().parents[3] /
    "Fonts/Nothing_You_Could_Do/NothingYouCouldDo-Regular.ttf")))
GRID_INK = HexColor("#59635D")


def pen_line(c, a, b, seed, wobble=0.65, width=0.72):
    rng = random.Random(seed)
    dx, dy = b[0] - a[0], b[1] - a[1]
    length = math.hypot(dx, dy)
    nx, ny = -dy / length, dx / length
    bends = [rng.uniform(-wobble, wobble) for _ in range(2)]
    p = c.beginPath()
    p.moveTo(*a)
    p.curveTo(a[0] + dx / 3 + nx * bends[0], a[1] + dy / 3 + ny * bends[0],
              a[0] + dx * 2 / 3 + nx * bends[1], a[1] + dy * 2 / 3 + ny * bends[1], *b)
    c.setLineWidth(width * rng.uniform(0.88, 1.12))
    c.drawPath(p, stroke=1, fill=0)


def draw_grid_ink(c, columns=range(SIZE)):
    """Clip canonical strokes to a column interval; endpoints remain exact."""
    x0, x1 = min(columns) * CELL, (max(columns) + 1) * CELL
    c.saveState()
    clip = c.beginPath()
    clip.rect(x0 - 0.6, -0.6, x1 - x0 + 1.2, SIZE * CELL + 1.2)
    c.clipPath(clip, stroke=0, fill=0)
    c.setLineCap(1)
    c.setStrokeColor(GRID_INK)
    for line in range(SIZE + 1):
        for segment in range(SIZE):
            pen_line(c, (line * CELL, segment * CELL),
                     (line * CELL, (segment + 1) * CELL), 1000 + line * 31 + segment)
            pen_line(c, (segment * CELL, line * CELL),
                     ((segment + 1) * CELL, line * CELL), 3000 + line * 31 + segment)
    c.restoreState()


def rough_outline(c, vertices, seed):
    rng = random.Random(seed)
    points = [(x + rng.uniform(-0.55, 0.55), y + rng.uniform(-0.55, 0.55))
              for x, y in vertices]
    p = c.beginPath()
    p.moveTo(*points[0])
    for a, b in zip(points, points[1:] + points[:1]):
        dx, dy = b[0] - a[0], b[1] - a[1]
        p.curveTo(a[0] + dx / 3 + rng.uniform(-0.5, 0.5),
                  a[1] + dy / 3 + rng.uniform(-0.5, 0.5),
                  a[0] + 2 * dx / 3 + rng.uniform(-0.5, 0.5),
                  a[1] + 2 * dy / 3 + rng.uniform(-0.5, 0.5), *b)
    p.close()
    return p


def shade(c, outline, cx, cy, seed):
    c.saveState()
    c.clipPath(outline, stroke=0, fill=0)
    # Close-spaced diagonal pen strokes retain small paper gaps.
    for k in range(-24, 25):
        offset = k * 1.25
        pen_line(c, (cx - CELL, cy - CELL + offset),
                 (cx + CELL, cy + CELL + offset), seed + k + 30, 0.8, 0.82)
    c.restoreState()


def draw_tokens(c, columns=range(SIZE)):
    c.saveState()
    c.setLineCap(1)
    c.setLineJoin(1)
    for x, y in sorted(ATTACKERS | DEFENDERS | CORNERS | {THRONE}):
        if x not in columns:
            continue
        cx, cy = (x + 0.5) * CELL, (y + 0.5) * CELL
        seed = 5000 + x * 47 + y * 103
        if (x, y) in CORNERS:
            r = CELL * 0.26
            vertices = [(cx, cy + r), (cx + r, cy), (cx, cy - r), (cx - r, cy)]
        elif (x, y) == THRONE:
            r = CELL * 0.24
            vertices = [(cx + r * math.cos(i * math.tau / 18),
                         cy + r * math.sin(i * math.tau / 18)) for i in range(18)]
        else:
            r = CELL * 0.30
            vertices = [(cx - r, cy - r), (cx + r, cy - r),
                        (cx + r, cy + r), (cx - r, cy + r)]
        p = rough_outline(c, vertices, seed)
        c.setStrokeColor(RUST if (x, y) in CORNERS or (x, y) == THRONE else INK)
        if (x, y) in ATTACKERS or (x, y) == THRONE:
            shade(c, p, cx, cy, seed)
        c.setLineWidth(1.0)
        c.drawPath(p, stroke=1, fill=0)
    c.restoreState()


def draw_column_labels(c, columns=range(SIZE)):
    c.setFillColor(INK)
    c.setFont(HAND, 9)
    for x in columns:
        rng = random.Random(8000 + x)
        c.saveState()
        c.translate((x + 0.5) * CELL, SIZE * CELL + 4 + rng.uniform(-0.4, 0.4))
        c.rotate(rng.uniform(-1.2, 1.2))
        c.drawCentredString(0, 0, chr(65 + x))
        c.restoreState()


def draw_row_labels(c):
    c.setFillColor(INK)
    c.setFont(HAND, 8.5)
    for y in range(SIZE):
        c.drawRightString(-4, (y + 0.5) * CELL - 3, str(y + 1))


def hand_text(c, text, x, y, size, max_width=None):
    if max_width:
        size = min(size, size * max_width / pdfmetrics.stringWidth(text, HAND, size))
    c.setFont(HAND, size)
    c.drawString(x, y, text)
