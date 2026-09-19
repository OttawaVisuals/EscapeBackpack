"""Build a visual A/B comparison sheet for every item in Aud's current map legend."""

from pathlib import Path
import math

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

import aud_layer


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = ROOT / "output" / "pdf" / "Aud_Map_Legend_Options.pdf"

INK = HexColor("#283B34")
MUTED = HexColor("#66736D")
RULE = HexColor("#B8AA8D")
PAPER = HexColor("#F7F2E5")
ROW_ALT = HexColor("#F2ECDE")
PURPLE = HexColor("#806F96")
PLUM = HexColor("#523A70")
TEAL = HexColor("#216866")
GREEN = HexColor("#4A6B3A")
BROWN = HexColor("#8A5A32")
GREY = HexColor("#6E6A5E")


ITEMS = [
    ("road", "Paved road", "Outlined carriageway", "Twin wheel tracks"),
    ("path", "Footpath", "Short regular dashes", "Alternating walking ticks"),
    ("river", "River", "Strong line with pale banks", "Double bank and channel"),
    ("stream", "Stream", "Thin continuous line", "Loose repeating wave"),
    ("ditch", "Ditch", "One-sided hachures", "Broken double line"),
    ("hedge", "Hedge", "Even rounded shrubs", "Irregular leaf chain"),
    ("wall", "Stone wall", "Divided stone blocks", "Uneven linked stones"),
    ("bridge", "Bridge", "Deck with heavy end bars", "Three timber planks"),
    ("ford", "Ford", "Large stepping stones", "Broken water and ripples"),
    ("gate", "Gate", "Two posts and rails", "Clearly open gate"),
    ("wood", "Wood", "Sparse tree clusters", "Canopy dots and trunks"),
    ("marsh", "Marsh", "Reeds and water bars", "Edge reed clusters"),
    ("moor", "Moor", "Grass and heather tufts", "Wind-swept curves"),
    ("field", "Field", "Fine parallel furrows", "Rows of crop chevrons"),
    ("lake", "Lake", "Flat wash, strong shore", "Pale wash and waves"),
    ("village", "Village", "Compact solid roofs", "Buildings around a green"),
    ("farm", "Farm", "House with field corner", "Low barn silhouette"),
    ("church", "Chapel", "Gable and clear cross", "Stave-church silhouette"),
    ("mill", "Mill", "House and half-wheel", "Wheel beside millrace"),
    ("well", "Well", "Stone ring and centre", "Posts and crossbar"),
    ("port", "Landing", "T-shaped jetty", "Small beached boat"),
    ("cairn", "Cairn", "Three stacked courses", "Pile of four stones"),
    ("stone", "Standing stone", "Solid asymmetric monolith", "Carved runestone slab"),
    ("ruin", "Ruin", "Broken building outline", "L-shaped wall fragments"),
    ("cave", "Cave", "Dark mouth in rock", "Split rock cleft"),
]


def line(c, x1, y1, x2, y2, colour=INK, width=1.0):
    c.setStrokeColor(colour)
    c.setLineWidth(width)
    c.line(x1, y1, x2, y2)


def poly(c, pts, colour=INK, width=1.0, fill=None, close=True):
    c.setStrokeColor(colour)
    c.setLineWidth(width)
    if fill is not None:
        c.setFillColor(fill)
    p = c.beginPath()
    p.moveTo(*pts[0])
    for pt in pts[1:]:
        p.lineTo(*pt)
    if close:
        p.close()
    c.drawPath(p, stroke=1, fill=1 if fill is not None else 0)


def current_swatch(c, kind, x, y):
    """Draw the current legend mark using the production layer's own definitions."""
    if kind in aud_layer.LINE:
        s = aud_layer.LINE[kind]
        if kind == "road":
            line(c, x - 18, y, x + 18, y, HexColor(s["color"]), s["w"] + 1.1)
            line(c, x - 18, y, x + 18, y, HexColor("#F6EFDC"), s["w"] - 0.6)
        else:
            c.setStrokeColor(HexColor(s["color"]))
            c.setLineWidth(s["w"])
            c.setDash(*s["dash"]) if s.get("dash") else c.setDash()
            c.line(x - 18, y, x + 18, y)
            c.setDash()
            if kind in ("hedge", "wall", "ditch"):
                aud_layer._ornament(c, {"kind": kind, "smooth": False,
                                        "pts": [[x - 18, y], [x + 18, y]]})
        return
    if kind in aud_layer.AREA:
        s = aud_layer.AREA[kind]
        pts = [[x - 18, y - 8], [x + 18, y - 8], [x + 18, y + 8], [x - 18, y + 8]]
        c.setFillColor(HexColor(s["fill"]))
        c.setStrokeColor(HexColor(s["color"]))
        c.setLineWidth(0.7)
        c.rect(x - 18, y - 8, 36, 16, fill=1, stroke=1)
        aud_layer._area_texture(c, {"kind": kind, "pts": pts, "smooth": False})
        return
    aud_layer._point(c, {"kind": kind, "pts": [[x, y]], "label": ""})


def draw_line_option(c, kind, option, x, y):
    left, right = x - 18, x + 18
    if kind == "road":
        if option == "A":
            line(c, left, y, right, y, BROWN, 3.4)
            line(c, left, y, right, y, PAPER, 1.8)
        else:
            line(c, left, y + 2.2, right, y + 2.2, BROWN, 0.9)
            line(c, left, y - 2.2, right, y - 2.2, BROWN, 0.9)
        return
    if kind == "path":
        c.setStrokeColor(HexColor("#8F7E61"))
        c.setLineWidth(1.0)
        if option == "A":
            c.setDash(3.0, 2.4)
            c.line(left, y, right, y)
            c.setDash()
        else:
            for i, xx in enumerate(range(int(left), int(right) + 1, 5)):
                dy = 1.7 if i % 2 else -1.7
                line(c, xx - 1, y + dy - 1.5, xx + 1, y + dy + 1.5,
                     HexColor("#8F7E61"), 0.8)
        return
    if kind == "river":
        if option == "A":
            line(c, left, y, right, y, HexColor("#BFD7D2"), 4.0)
            line(c, left, y, right, y, TEAL, 1.7)
        else:
            line(c, left, y + 2.5, right, y + 2.5, TEAL, 0.8)
            line(c, left, y - 2.5, right, y - 2.5, TEAL, 0.8)
        return
    if kind == "stream":
        if option == "A":
            line(c, left, y, right, y, TEAL, 0.9)
        else:
            c.setStrokeColor(TEAL)
            c.setLineWidth(0.8)
            p = c.beginPath()
            p.moveTo(left, y)
            for i in range(6):
                xx = left + i * 6
                p.curveTo(xx + 1.5, y + 2, xx + 4.5, y - 2, xx + 6, y)
            c.drawPath(p, stroke=1, fill=0)
        return
    if kind == "ditch":
        line(c, left, y, right, y, MUTED, 0.8)
        if option == "A":
            for xx in range(int(left) + 2, int(right), 6):
                line(c, xx, y, xx + 2, y - 4, MUTED, 0.7)
        else:
            c.setStrokeColor(MUTED)
            c.setLineWidth(0.7)
            c.setDash(5, 2)
            c.line(left, y - 3, right, y - 3)
            c.setDash()
        return
    if kind == "hedge":
        if option == "A":
            for xx in range(int(left) + 2, int(right), 5):
                c.setFillColor(GREEN)
                c.circle(xx, y, 2.0, stroke=0, fill=1)
        else:
            for i, xx in enumerate(range(int(left) + 2, int(right), 5)):
                r = 2.4 if i % 3 == 0 else 1.6
                poly(c, [(xx - r, y), (xx, y + r), (xx + r, y), (xx, y - r)],
                     GREEN, 0.5, GREEN)
        return
    if kind == "wall":
        if option == "A":
            line(c, left, y, right, y, GREY, 1.1)
            for xx in range(int(left) + 5, int(right), 7):
                line(c, xx, y - 2.3, xx, y + 2.3, GREY, 0.7)
        else:
            sizes = [5, 7, 4, 6, 5, 7]
            xx = left
            for i, w in enumerate(sizes):
                poly(c, [(xx, y - 2), (xx + w, y - 2.5 + (i % 2)),
                         (xx + w, y + 2), (xx, y + 2.5 - (i % 2))], GREY, 0.7)
                xx += w


def terrain_option(c, kind, option, x, y):
    fills = {"wood": "#CBD9BE", "marsh": "#D5E2DC", "moor": "#E8DFC6",
             "field": "#F0E7CE", "lake": "#DCE7E4"}
    strokes = {"wood": GREEN, "marsh": TEAL, "moor": HexColor("#8A7A5E"),
               "field": HexColor("#B08A5A"), "lake": TEAL}
    c.setFillColor(HexColor(fills[kind]))
    c.setStrokeColor(strokes[kind])
    c.setLineWidth(0.8 if option == "A" else 1.0)
    c.rect(x - 18, y - 8, 36, 16, fill=1, stroke=1)
    col = strokes[kind]
    if kind == "wood":
        if option == "A":
            for xx, yy in ((x - 11, y - 2), (x - 2, y + 2), (x + 9, y - 1)):
                line(c, xx, yy - 3, xx, yy + 2, col, 0.6)
                poly(c, [(xx - 3, yy), (xx, yy + 5), (xx + 3, yy)], col, 0.6)
        else:
            for xx, yy, r in ((x - 12, y + 1, 2.5), (x - 7, y + 3, 2.2),
                              (x + 2, y - 1, 2.7), (x + 9, y + 2, 2.1), (x + 13, y, 2.4)):
                c.setFillColor(col); c.circle(xx, yy, r, stroke=0, fill=1)
                line(c, xx, yy - r, xx, y - 6, col, 0.5)
    elif kind == "marsh":
        xs = (-12, -4, 5, 13) if option == "A" else (-14, -10, 10, 14)
        for dx in xs:
            line(c, x + dx - 3, y - 3, x + dx + 3, y - 3, col, 0.5)
            line(c, x + dx, y - 1, x + dx, y + 4, col, 0.6)
            line(c, x + dx, y + 2, x + dx - 2, y + 4, col, 0.5)
            line(c, x + dx, y + 2, x + dx + 2, y + 4, col, 0.5)
    elif kind == "moor":
        if option == "A":
            for dx in (-12, -4, 5, 13):
                line(c, x + dx, y - 3, x + dx, y + 2, col, 0.5)
                line(c, x + dx, y, x + dx - 2, y + 2, col, 0.5)
                line(c, x + dx, y, x + dx + 2, y + 2, col, 0.5)
        else:
            for dy in (-4, 1, 5):
                c.setStrokeColor(col); c.setLineWidth(0.45)
                p = c.beginPath(); p.moveTo(x - 14, y + dy)
                p.curveTo(x - 6, y + dy + 2, x + 6, y + dy - 2, x + 14, y + dy)
                c.drawPath(p, stroke=1, fill=0)
    elif kind == "field":
        if option == "A":
            for dx in range(-13, 15, 6):
                line(c, x + dx - 3, y - 6, x + dx + 3, y + 6, col, 0.45)
        else:
            for dx in range(-12, 14, 7):
                for dy in (-3, 3):
                    line(c, x + dx, y + dy, x + dx - 2, y + dy + 2, col, 0.45)
                    line(c, x + dx, y + dy, x + dx + 2, y + dy + 2, col, 0.45)
    elif kind == "lake" and option == "B":
        for dx, dy in ((-10, 3), (4, 2), (-3, -3), (11, -3)):
            line(c, x + dx - 4, y + dy, x + dx + 4, y + dy, col, 0.45)


def point_option(c, kind, option, x, y):
    col = PLUM if kind in ("bridge", "gate") else TEAL if kind == "ford" else PURPLE
    if kind == "bridge":
        if option == "A":
            line(c, x - 7, y - 3, x + 7, y - 3, col, 1.4)
            line(c, x - 7, y + 3, x + 7, y + 3, col, 1.4)
            line(c, x - 7, y - 6, x - 7, y + 6, col, 1.6)
            line(c, x + 7, y - 6, x + 7, y + 6, col, 1.6)
        else:
            for dy in (-3, 0, 3): line(c, x - 7, y + dy, x + 7, y + dy, col, 1.0)
            line(c, x - 8, y - 6, x - 8, y + 6, col, 1.2)
            line(c, x + 8, y - 6, x + 8, y + 6, col, 1.2)
        return
    if kind == "ford":
        if option == "A":
            for dx, dy, r in ((-6, 0, 2.1), (0, 1, 2.3), (6, -1, 2.0)):
                c.setFillColor(col); c.circle(x + dx, y + dy, r, stroke=0, fill=1)
        else:
            for dy in (-4, 4):
                line(c, x - 8, y + dy, x - 3, y + dy, col, 0.8)
                line(c, x + 3, y + dy, x + 8, y + dy, col, 0.8)
            for dx in (-4, 0, 4): line(c, x + dx - 2, y, x + dx + 2, y, col, 1.0)
        return
    if kind == "gate":
        line(c, x - 7, y - 6, x - 7, y + 6, col, 1.4)
        line(c, x + 7, y - 6, x + 7, y + 6, col, 1.4)
        if option == "A":
            line(c, x - 7, y - 2.5, x + 7, y - 2.5, col, 0.9)
            line(c, x - 7, y + 2.5, x + 7, y + 2.5, col, 0.9)
        else:
            line(c, x - 7, y - 3, x + 2, y + 5, col, 1.0)
            line(c, x - 7, y + 1, x + 1, y + 5, col, 0.8)
        return
    if kind == "village":
        if option == "A":
            for dx, dy in ((-6, 2), (2, 3), (-1, -4)):
                poly(c, [(x + dx - 3, y + dy - 3), (x + dx - 3, y + dy),
                         (x + dx, y + dy + 3), (x + dx + 3, y + dy),
                         (x + dx + 3, y + dy - 3)], col, 0.7, col)
        else:
            for dx, dy in ((-6, 0), (0, 5), (6, 0), (0, -5)):
                c.setFillColor(col); c.rect(x + dx - 2, y + dy - 2, 4, 4, fill=1, stroke=0)
        return
    if kind == "farm":
        if option == "A":
            poly(c, [(x - 8, y - 4), (x - 8, y + 1), (x - 3, y + 5),
                     (x + 2, y + 1), (x + 2, y - 4)], col, 0.9)
            c.setStrokeColor(col); c.setLineWidth(0.6); c.rect(x + 4, y - 4, 6, 7, fill=0, stroke=1)
            line(c, x + 7, y - 4, x + 7, y + 3, col, 0.4)
        else:
            poly(c, [(x - 8, y - 5), (x - 8, y + 1), (x, y + 6),
                     (x + 8, y + 1), (x + 8, y - 5)], col, 0.9, col)
            line(c, x + 3, y + 4, x + 3, y + 8, col, 1.0)
        return
    if kind == "church":
        if option == "A":
            poly(c, [(x - 6, y - 5), (x - 6, y + 1), (x, y + 6),
                     (x + 6, y + 1), (x + 6, y - 5)], col, 1.0)
            line(c, x, y + 6, x, y + 11, col, 1.0); line(c, x - 2, y + 9, x + 2, y + 9, col, 1.0)
        else:
            poly(c, [(x - 7, y - 5), (x - 6, y + 2), (x - 3, y + 2),
                     (x, y + 10), (x + 3, y + 2), (x + 6, y + 2), (x + 7, y - 5)],
                 col, 0.9, col)
        return
    if kind == "mill":
        if option == "A":
            poly(c, [(x - 8, y - 5), (x - 8, y + 2), (x - 3, y + 6),
                     (x + 2, y + 2), (x + 2, y - 5)], col, 0.8)
            c.setStrokeColor(col); c.setLineWidth(0.9); c.circle(x + 3, y - 1, 5, stroke=1, fill=0)
            for a in (0, math.pi / 2):
                line(c, x + 3 - math.cos(a) * 5, y - 1 - math.sin(a) * 5,
                     x + 3 + math.cos(a) * 5, y - 1 + math.sin(a) * 5, col, 0.6)
        else:
            c.setStrokeColor(col); c.setLineWidth(1.0); c.circle(x - 2, y + 1, 6, stroke=1, fill=0)
            for a in (0, math.pi / 2, math.pi / 4, -math.pi / 4):
                line(c, x - 2 - math.cos(a) * 6, y + 1 - math.sin(a) * 6,
                     x - 2 + math.cos(a) * 6, y + 1 + math.sin(a) * 6, col, 0.5)
            line(c, x + 4, y - 5, x + 10, y - 5, TEAL, 0.8)
        return
    if kind == "well":
        if option == "A":
            c.setStrokeColor(col); c.setLineWidth(1.1); c.circle(x, y, 5, stroke=1, fill=0)
            c.setFillColor(col); c.circle(x, y, 1.5, stroke=0, fill=1)
        else:
            line(c, x - 6, y - 5, x - 6, y + 5, col, 1.0); line(c, x + 6, y - 5, x + 6, y + 5, col, 1.0)
            line(c, x - 7, y + 5, x + 7, y + 5, col, 1.0); line(c, x - 5, y - 3, x + 5, y - 3, col, 1.4)
        return
    if kind == "port":
        if option == "A":
            line(c, x, y - 7, x, y + 6, col, 1.4); line(c, x - 7, y + 6, x + 7, y + 6, col, 1.4)
            for dx in (-5, 0, 5): line(c, x + dx, y + 4, x + dx, y + 8, col, 0.7)
        else:
            c.setStrokeColor(col); c.setLineWidth(1.0)
            p = c.beginPath(); p.moveTo(x - 8, y - 2); p.curveTo(x - 4, y - 7, x + 5, y - 7, x + 8, y - 1)
            p.lineTo(x - 8, y - 2); c.drawPath(p, stroke=1, fill=0)
            line(c, x - 1, y - 2, x - 1, y + 7, col, 0.9); line(c, x - 1, y + 7, x + 5, y + 1, col, 0.8)
        return
    if kind == "cairn":
        if option == "A":
            for i, (w, yy) in enumerate(((14, -5), (10, -1), (6, 3))):
                c.setStrokeColor(col); c.setLineWidth(0.8); c.rect(x - w/2, y + yy, w, 3.5, fill=0, stroke=1)
        else:
            for dx, dy, r in ((-5, -3, 3.2), (1, -3, 3.5), (6, -2, 2.7), (-1, 2, 3.4)):
                c.setFillColor(col); c.circle(x + dx, y + dy, r, stroke=0, fill=1)
        return
    if kind == "stone":
        pts = [(x - 4, y - 6), (x - 3, y + 5), (x, y + 8), (x + 4, y + 4), (x + 5, y - 6)]
        poly(c, pts, col, 1.0, col if option == "A" else None)
        line(c, x - 6, y - 6, x + 7, y - 6, col, 0.8)
        if option == "B": line(c, x - 1, y + 3, x + 2, y - 2, col, 0.9)
        return
    if kind == "ruin":
        if option == "A":
            poly(c, [(x - 7, y - 5), (x - 7, y + 2), (x, y + 7),
                     (x + 7, y + 2), (x + 7, y - 1)], col, 1.0, close=False)
            line(c, x - 7, y - 5, x - 1, y - 5, col, 1.0)
        else:
            line(c, x - 7, y - 5, x - 7, y + 6, col, 2.0); line(c, x - 7, y - 5, x + 7, y - 5, col, 2.0)
            line(c, x + 2, y - 5, x + 2, y, col, 1.2)
        return
    if kind == "cave":
        if option == "A":
            poly(c, [(x - 9, y - 5), (x - 6, y + 2), (x, y + 7),
                     (x + 7, y + 2), (x + 9, y - 5)], col, 0.9)
            c.setFillColor(col)
            p = c.beginPath(); p.moveTo(x - 4, y - 5); p.curveTo(x - 4, y + 3, x + 4, y + 3, x + 4, y - 5); p.close()
            c.drawPath(p, stroke=0, fill=1)
        else:
            poly(c, [(x - 9, y - 5), (x - 5, y + 3), (x - 1, y + 7),
                     (x + 1, y + 1), (x + 5, y + 6), (x + 9, y - 5)], col, 1.0, close=False)
            line(c, x, y + 1, x - 2, y - 5, col, 1.8)


def option_swatch(c, kind, option, x, y):
    if kind in ("road", "path", "river", "stream", "ditch", "hedge", "wall"):
        draw_line_option(c, kind, option, x, y)
    elif kind in ("wood", "marsh", "moor", "field", "lake"):
        terrain_option(c, kind, option, x, y)
    else:
        point_option(c, kind, option, x, y)


def draw_page(c, page_items, page_number, section):
    w, h = letter
    margin = 28
    table_x0, table_x1 = margin, w - margin
    table_top, table_bottom = h - 92, 38
    col_w = (table_x1 - table_x0) / 3
    row_h = (table_top - table_bottom) / len(page_items)

    c.setFillColor(PAPER); c.rect(0, 0, w, h, fill=1, stroke=0)
    c.setFillColor(INK); c.setFont("Times-Bold", 20)
    c.drawString(margin, h - 34, "AUD'S MAP - LEGEND OPTIONS")
    c.setFont("Helvetica", 8.5); c.setFillColor(MUTED)
    c.drawString(margin, h - 51, section)
    c.drawRightString(w - margin, h - 51, f"Page {page_number} of 2")
    c.setFont("Helvetica-Oblique", 7.5)
    c.drawString(margin, h - 66, "Compare the printed marks. Circle A or B, or note 'current' where no change is needed.")

    headers = ("CURRENT", "OPTION A - SURVEY", "OPTION B - SAGA")
    c.setFillColor(HexColor("#6E4E83")); c.rect(table_x0, table_top, table_x1 - table_x0, 22, fill=1, stroke=0)
    c.setFillColor(HexColor("#FFFFFF")); c.setFont("Helvetica-Bold", 8.5)
    for i, header in enumerate(headers):
        c.drawCentredString(table_x0 + col_w * (i + 0.5), table_top + 7, header)

    for r, (kind, name, desc_a, desc_b) in enumerate(page_items):
        y_top = table_top - r * row_h
        y_bottom = y_top - row_h
        if r % 2:
            c.setFillColor(ROW_ALT); c.rect(table_x0, y_bottom, table_x1 - table_x0, row_h, fill=1, stroke=0)
        c.setStrokeColor(RULE); c.setLineWidth(0.35); c.line(table_x0, y_bottom, table_x1, y_bottom)
        for i in (1, 2): c.line(table_x0 + i * col_w, y_bottom, table_x0 + i * col_w, y_top)

        cy = (y_top + y_bottom) / 2 - 5
        for i, desc in enumerate(("Existing map mark", desc_a, desc_b)):
            x0 = table_x0 + i * col_w
            c.setFillColor(INK); c.setFont("Helvetica-Bold", 7.4)
            c.drawString(x0 + 8, y_top - 11, name if i == 0 else ("A" if i == 1 else "B"))
            c.setFillColor(MUTED); c.setFont("Helvetica", 6.5)
            c.drawString(x0 + 51, cy - 2, desc)
            if i == 0:
                current_swatch(c, kind, x0 + 28, cy)
            else:
                option_swatch(c, kind, "A" if i == 1 else "B", x0 + 28, cy)

    c.setStrokeColor(RULE); c.setLineWidth(0.8)
    c.rect(table_x0, table_bottom, table_x1 - table_x0, table_top - table_bottom + 22, fill=0, stroke=1)
    c.setFillColor(MUTED); c.setFont("Helvetica", 6.8)
    c.drawString(margin, 21, "Vector study only. Final symbols will retain Aud's existing palette and puzzle hierarchy.")
    c.drawRightString(w - margin, 21, "Crossings remain the darkest countable marks.")


def build():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUT), pagesize=letter, pageCompression=1)
    c.setTitle("Aud's Map - Legend Options")
    draw_page(c, ITEMS[:15], 1, "Routes, boundaries, crossings and terrain")
    c.showPage()
    draw_page(c, ITEMS[15:], 2, "Settlements, buildings, ancient sites and natural landmarks")
    c.save()
    print(OUT)


if __name__ == "__main__":
    build()
