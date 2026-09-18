"""SHELVED 17 Sept 2026 -- the split-panel detail drawing lifted out of
build_trail_maps_pdf.py verbatim, so it is recoverable without git archaeology.

It depends on AUD_PANEL / AUD_PAGE / AUD_MAIN_* (also removed) and on
aud_detail_panel.py, shelved beside this file. See README.md.
"""

def _aud_offset(col, row):
    """A small, stable per-cell nudge so icons are never all cell-centred.

    Six identically-centred icons read as a deliberate grid overlay rather than scenery -- the
    same reason ROLLO_WORDLOCK_ART jitters its boxes.  Derived from the cell, so it is stable
    across builds without a second table to keep in step with aud_detail_panel.py.

    The range is bounded so a glyph can never cross a cell line -- a landmark straddling a
    boundary would let players read the wrong plot number, which is unrecoverable.  Budget:
    max offset 9.0 x 8.0; largest glyph half-extent 12.5 x 10.0 (farm's home-field, chapel's
    cross); cell half-size 22.9 x 24.6.  9.0 + 12.5 = 21.5 < 22.9 and 8.0 + 10.0 = 18.0 < 24.6.
    Widen a glyph or the offsets and this has to be rechecked.
    """
    h = (col * 73 + row * 149) % 97
    return ((h % 19) - 9.0, ((h // 19) % 17) - 8.0)


def _aud_placeholder_glyph(c, kind, x, y):
    """PLACEHOLDER vector landmark, pending Codex vignettes (PZ-17).

    Stand-ins, so the sheet can be built and checked end to end.  When the real purple
    vignettes exist they replace this function, not the placements: cells, route and plot
    numbers all live in aud_detail_panel.py and do not move.

    For the art brief: cairn and standing stone are stops 6 and 7, so they have to read as
    clearly different objects at roughly 34 pt.
    """
    purple = HexColor("#6D528B")
    c.saveState()
    c.setStrokeColor(purple)
    c.setFillColor(purple)
    c.setLineWidth(0.75)
    if kind == "farm":                                   # longhouse inside its home-field
        c.setStrokeColor(TAN)
        c.setLineWidth(0.4)
        c.rect(x - 12, y - 8, 24, 16, stroke=1, fill=0)
        c.setStrokeColor(purple)
        c.setLineWidth(0.75)
        p = c.beginPath()
        p.moveTo(x - 6, y - 3); p.lineTo(x - 6, y + 2); p.lineTo(x, y + 6)
        p.lineTo(x + 6, y + 2); p.lineTo(x + 6, y - 3); p.close()
        c.drawPath(p, stroke=1, fill=0)
    elif kind == "mill":                                 # wheel-house plus overshot wheel
        p = c.beginPath()
        p.moveTo(x - 8, y - 5); p.lineTo(x - 8, y + 2); p.lineTo(x - 2, y + 7)
        p.lineTo(x + 1, y + 3); p.lineTo(x + 1, y - 5); p.close()
        c.drawPath(p, stroke=1, fill=0)
        c.circle(x + 5.5, y - 2, 5.0, stroke=1, fill=0)
        c.circle(x + 5.5, y - 2, 1.7, stroke=1, fill=0)
        for k in range(6):
            a = k * math.pi / 3
            c.line(x + 5.5 + 1.7 * math.cos(a), y - 2 + 1.7 * math.sin(a),
                   x + 5.5 + 5.0 * math.cos(a), y - 2 + 5.0 * math.sin(a))
    elif kind == "fold":                                 # drystone stock pen, one gate gap
        c.ellipse(x - 9, y - 6, x + 9, y + 6, stroke=1, fill=0)
        c.ellipse(x - 6.5, y - 4, x + 6.5, y + 4, stroke=1, fill=0)
        c.setStrokeColor(LAND_C)
        c.setLineWidth(2.0)
        c.line(x + 5, y - 5, x + 9.5, y - 2.5)
    elif kind == "chapel":                               # roofless: the east wall is broken
        p = c.beginPath()
        p.moveTo(x - 8, y - 5); p.lineTo(x - 8, y + 2); p.lineTo(x - 3, y + 7)
        p.lineTo(x + 2, y + 2)
        c.drawPath(p, stroke=1, fill=0)
        c.line(x + 2, y + 2, x + 2, y - 0.5)
        c.line(x + 2, y - 2.5, x + 2, y - 5)
        c.line(x - 8, y - 5, x + 2, y - 5)
        c.line(x - 3, y + 7, x - 3, y + 10)
        c.line(x - 5, y + 9, x - 1, y + 9)
    elif kind == "naust":                                # boat shed, open to the water
        p = c.beginPath()
        p.moveTo(x - 7, y - 3); p.lineTo(x - 5, y + 4); p.lineTo(x + 5, y + 4)
        p.lineTo(x + 7, y - 3); p.close()
        c.drawPath(p, stroke=1, fill=0)
        c.line(x - 5, y + 4, x + 5, y + 4)
    elif kind == "stone":                                # upright slab on a ground line
        p = c.beginPath()
        p.moveTo(x - 4, y - 7); p.lineTo(x - 3, y + 4); p.lineTo(x, y + 8)
        p.lineTo(x + 3, y + 3); p.lineTo(x + 4, y - 7); p.close()
        c.drawPath(p, stroke=1, fill=0)
        c.setStrokeColor(TAN)
        c.setLineWidth(0.5)
        c.line(x - 5.5, y - 7, x + 5.5, y - 7)
    elif kind == "cairn":                                # coursed heap, deliberately not a slab
        p = c.beginPath()
        p.moveTo(x - 6, y - 5); p.lineTo(x, y + 7); p.lineTo(x + 6, y - 5); p.close()
        c.drawPath(p, stroke=1, fill=0)
        c.line(x - 3.6, y - 0.6, x + 3.6, y - 0.6)
        c.line(x - 5, y - 3, x + 5, y - 3)
    elif kind == "falls":
        c.setStrokeColor(TEAL)
        c.setLineWidth(0.9)
        c.line(x - 8, y + 5, x + 8, y + 5)
        for k in range(5):
            c.line(x - 7 + k * 3.5, y + 5, x - 7 + k * 3.5, y - 5)
    elif kind == "birch":
        c.setFillColor(HexColor("#B3C2A6"))
        for bx, by in ((-8, -3), (-1, 2), (6, -2), (-3, -7), (4, 5), (9, 3)):
            c.circle(x + bx, y + by, 3.5, stroke=0, fill=1)
    elif kind == "marsh":
        c.setStrokeColor(TEAL)
        c.setLineWidth(0.5)
        for k in range(3):
            for j in range(3):
                c.line(x - 9 + j * 7.5, y - 5 + k * 4.5, x - 4.5 + j * 7.5, y - 5 + k * 4.5)
    elif kind == "ford":                                 # stepping stones across the river
        c.setStrokeColor(TAN)
        c.setLineWidth(1.0)
        for k in range(4):
            c.line(x - 7 + k * 4.6, y - 6, x - 7 + k * 4.6, y + 6)
    c.restoreState()


def _aud_hachures(c, pts, n, ln):
    """Hill shading in two offset passes, so a ridge reads as mass rather than loose ticks."""
    c.setStrokeColor(HexColor("#9E957E"))
    for depth, width in ((1.0, 0.55), (0.55, 0.4)):
        c.setLineWidth(width)
        for i in range(len(pts) - 1):
            (ax, ay), (bx, by) = pts[i], pts[i + 1]
            L = math.hypot(bx - ax, by - ay) or 1
            ux, uy = -(by - ay) / L, (bx - ax) / L
            for k in range(n):
                t = (k + 0.5 * depth) / n
                px = ax + (bx - ax) * t + ux * ln * (1 - depth) * 1.1
                py = ay + (by - ay) * t + uy * ln * (1 - depth) * 1.1
                c.line(px, py, px + ux * ln * depth, py + uy * ln * depth)


def _aud_glyph(c, kind, x, y):
    """Place the approved PZ-17 vignette inside its fixed 34 pt clearance box."""
    if kind == "marsh":
        # PZ-17 deliberately keeps marsh as diffuse vector terrain, not an isolated icon.
        _aud_placeholder_glyph(c, kind, x, y)
        return
    draw_vignette(c, SOURCE_ART_DIR / ("Aud_%s_v2.png" % kind),
                  (x - 17, y - 17, 34, 34), 0.72)


def draw_aud_detail_panel(c, answer=False):
    """Draw the Dalir/Hvammur close-up beside Aud's main map (PZ-17).

    This panel is a NON-GEOREFERENCED local survey, not a zoom of the real projection: its
    coastline, river, tracks and hills are designed terrain and its grid is its own reference
    system.  It carries no place names, so it asserts nothing about real geography.

    Its entire puzzle content -- the survey plot number in every cell, where each landmark
    sits, and which seven cells the route visits -- comes from aud_detail_panel.py.  Run that
    module after changing anything there; it checks that the route stays solvable.
    """
    purple = HexColor("#6D528B")
    x0, y0, x1, y1 = AUD_PANEL
    gx0, gx1 = x0 + 16, x1 - 16
    gy0, gy1 = y0 + 28, y1 - 48
    cols, rows = AUD.COLS, AUD.ROWS
    cw, ch = (gx1 - gx0) / cols, (gy1 - gy0) / rows

    def cx(col, f=0.5):
        return gx0 + (col + f) * cw

    def cy(row, f=0.5):                       # row 0 is the TOP row, printed as "1"
        return gy1 - (row + f) * ch

    c.setFillColor(SEA)
    c.rect(x0, y0, x1 - x0, y1 - y0, stroke=0, fill=1)
    c.setFillColor(HexColor("#E8DEED"))
    c.rect(x0, y1 - 34, x1 - x0, 34, stroke=0, fill=1)
    c.setStrokeColor(INK)
    c.setLineWidth(1.2)
    c.rect(x0, y0, x1 - x0, y1 - y0, stroke=1, fill=0)
    c.setStrokeColor(purple)
    c.setLineWidth(1.1)
    c.line(x1 + 5, y0, x1 + 5, y1)            # physical divider between the two panels

    c.setFillColor(INK)
    c.setFont("CinzelXB", 9.5)
    c.drawCentredString((x0 + x1) / 2, y1 - 16, "DALIR  /  HVAMMUR")
    c.setFillColor(INK_SOFT)
    c.setFont("PlexIt", 5.6)
    c.drawCentredString((x0 + x1) / 2, y1 - 27, "land survey  -  plot numbers shown")

    c.saveState()
    clip = c.beginPath()
    clip.rect(gx0, gy0, gx1 - gx0, gy1 - gy0)
    c.clipPath(clip, stroke=0, fill=0)

    c.setFillColor(LAND_C)
    c.rect(gx0, gy0, gx1 - gx0, gy1 - gy0, stroke=0, fill=1)

    # The fjord: an inlet from the top-left tapering to a head, where the river empties.
    inlet = c.beginPath()
    inlet.moveTo(gx0 - 4, gy1 + 4)
    inlet.lineTo(gx0 - 4, cy(3, 0.2))
    inlet.curveTo(cx(0, 0.22), cy(4, 0.15), cx(0, 0.44), cy(4, 0.7), cx(0, 0.66), cy(5, 0.05))
    inlet.curveTo(cx(1, 0.20), cy(4, 0.10), cx(1, 0.50), cy(2, 0.20), cx(1, 0.86), gy1 + 4)
    inlet.close()
    c.setFillColor(SEA)
    c.drawPath(inlet, stroke=0, fill=1)
    c.setFillColor(HexColor("#E2D6B6"))
    c.circle(cx(0, 0.62), cy(4, 0.92), 8, stroke=0, fill=1)     # beach at the fjord head
    c.setStrokeColor(COAST)
    c.setLineWidth(0.85)
    sh = c.beginPath()
    sh.moveTo(gx0 - 4, cy(3, 0.2))
    sh.curveTo(cx(0, 0.22), cy(4, 0.15), cx(0, 0.44), cy(4, 0.7), cx(0, 0.66), cy(5, 0.05))
    sh.curveTo(cx(1, 0.20), cy(4, 0.10), cx(1, 0.50), cy(2, 0.20), cx(1, 0.86), gy1 + 4)
    c.drawPath(sh, stroke=1, fill=0)

    # River: fjord head -> the ford -> a confluence -> north branch (falls) and south branch.
    # The confluence is load-bearing: it is what tells the two mills apart.
    c.setStrokeColor(TEAL)
    c.setLineWidth(1.35)
    r = c.beginPath()
    r.moveTo(cx(0, 0.66), cy(5, 0.05))
    r.curveTo(cx(1, 0.1), cy(5, 0.55), cx(1, 0.7), cy(6, 0.25), cx(2, 0.5), cy(6, 0.5))
    r.curveTo(cx(2, 0.85), cy(6, 0.62), cx(3, 0.15), cy(6, 0.55), cx(3, 0.58), cy(6, 0.48))
    c.drawPath(r, stroke=1, fill=0)
    c.setLineWidth(0.9)                       # branches read as tributaries, not a second coast
    b1 = c.beginPath()
    b1.moveTo(cx(3, 0.58), cy(6, 0.48))
    b1.curveTo(cx(3, 0.85), cy(5, 0.65), cx(4, 0.15), cy(4, 0.75), cx(4, 0.46), cy(3, 0.50))
    b1.curveTo(cx(4, 0.60), cy(2, 0.55), cx(4, 0.80), cy(1, 0.60), cx(5, 0.15), cy(0, 0.30))
    c.drawPath(b1, stroke=1, fill=0)
    b2 = c.beginPath()
    b2.moveTo(cx(3, 0.58), cy(6, 0.48))
    b2.curveTo(cx(3, 0.80), cy(7, 0.40), cx(3, 0.55), cy(8, 0.35), cx(4, 0.25), cy(9, 0.45))
    c.drawPath(b2, stroke=1, fill=0)

    # Two tracks meeting at the ford -- the route's given starting point.
    c.setStrokeColor(TAN)
    c.setLineWidth(1.05)
    c.setDash(3.2, 2.2)
    t1 = c.beginPath()
    t1.moveTo(gx0 - 8, cy(3, 0.85))
    t1.curveTo(cx(1, 0.55), cy(4, 0.45), cx(1, 0.85), cy(6, 0.15), cx(2, 0.5), cy(6, 0.5))
    t1.curveTo(cx(3, 0.25), cy(6, 0.95), cx(4, 0.15), cy(7, 0.25), gx1 + 8, cy(7, 0.35))
    c.drawPath(t1, stroke=1, fill=0)
    t2 = c.beginPath()
    t2.moveTo(cx(2, 0.28), gy1 + 8)
    t2.curveTo(cx(2, 0.80), cy(3), cx(2, 0.20), cy(5), cx(2, 0.5), cy(6, 0.5))
    t2.curveTo(cx(2, 0.80), cy(8), cx(2, 0.30), cy(9), cx(2, 0.60), gy0 - 8)
    c.drawPath(t2, stroke=1, fill=0)
    c.setDash()

    _aud_hachures(c, [(cx(3, 0.8), cy(1, 0.95)), (cx(4, 0.5), cy(1, 0.45)),
                      (cx(5, 0.3), cy(1, 0.75)), (gx1 + 6, cy(2, 0.1))], 11, -8)
    _aud_hachures(c, [(cx(4, 0.9), cy(3, 0.15)), (cx(5, 0.45), cy(3, 0.85)),
                      (gx1 + 6, cy(4, 0.4))], 8, -7)
    _aud_hachures(c, [(cx(3, 0.5), cy(9, 0.25)), (cx(4, 0.45), cy(8, 0.85)),
                      (cx(5, 0.3), cy(9, 0.1)), (gx1 + 6, cy(9, 0.6))], 12, -8)
    c.restoreState()

    c.setStrokeColor(TAN)
    c.setLineWidth(0.4)
    for i in range(1, cols):
        c.line(gx0 + i * cw, gy0, gx0 + i * cw, gy1)
    for j in range(1, rows):
        c.line(gx0, gy0 + j * ch, gx1, gy0 + j * ch)
    c.setStrokeColor(INK)
    c.setLineWidth(0.8)
    c.rect(gx0, gy0, gx1 - gx0, gy1 - gy0, stroke=1, fill=0)

    # The survey plot numbers: quiet, same corner every cell, repeats allowed on purpose.
    c.setFillColor(HexColor("#9C8F6E"))
    c.setFont("Plex", 4.8)
    for j in range(rows):
        for i in range(cols):
            c.drawString(gx0 + i * cw + 2.6, gy1 - (j + 1) * ch + 2.8,
                         "%02d" % AUD.plot(i, j))

    c.setFillColor(purple)
    c.setFont("Plex", 5.6)
    for i in range(cols):
        c.drawCentredString(cx(i), gy1 + 4.5, "abcdef"[i])
        c.drawCentredString(cx(i), gy0 - 8.5, "abcdef"[i])
    for j in range(rows):
        c.drawRightString(gx0 - 4, cy(j) - 2, str(j + 1))
        c.drawString(gx1 + 4, cy(j) - 2, str(j + 1))

    for kind, col, row in AUD.FEATURES:
        dx, dy = _aud_offset(col, row)
        if kind == "farm":
            # The field is terrain notation, not part of the reusable farm asset.
            c.saveState()
            c.setStrokeColor(TAN)
            c.setLineWidth(0.4)
            c.rect(cx(col) + dx - 12, cy(row) + dy - 8, 24, 16, stroke=1, fill=0)
            c.restoreState()
        _aud_glyph(c, kind, cx(col) + dx, cy(row) + dy)

    if answer:
        pts = []
        for _, col, row in AUD.ROUTE:
            dx, dy = _aud_offset(col, row)
            pts.append((cx(col) + dx, cy(row) + dy))
        c.setStrokeColor(RUST)
        c.setLineWidth(1.5)
        c.setDash(4, 2.5)
        path = c.beginPath()
        path.moveTo(*pts[0])
        for q in pts[1:]:
            path.lineTo(*q)
        c.drawPath(path, stroke=1, fill=0)
        c.setDash()
        badge = ((-13, 11), (13, -11), (14, 9), (-13, 10), (-14, -9), (-13, -10), (12, 11))
        for k, (px, py) in enumerate(pts):
            ox, oy = badge[k]                 # sit clear of the glyph the badge marks
            c.setStrokeColor(RUST)
            c.setLineWidth(0.6)
            c.line(px, py, px + ox * 0.75, py + oy * 0.75)
            c.setFillColor(RUST)
            c.circle(px + ox, py + oy, 6.4, stroke=0, fill=1)
            c.setFillColor(WHITE)
            c.setFont("CinzelBold", 6.8)
            c.drawCentredString(px + ox, py + oy - 2.4, str(k + 1))
        c.setFillColor(RUST)
        c.setFont("CinzelBold", 7.2)
        c.drawCentredString((x0 + x1) / 2, y0 + 9, "%s      SUM %d"
                            % ("  >  ".join(AUD.ref(col, row) for _, col, row in AUD.ROUTE),
                               AUD.route_sum()))


