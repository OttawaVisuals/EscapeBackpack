"""Generate the three Final-riddle visuals as static inline SVG:
   A. timeline of events (22 stops on one dated line, coloured per leg)
   B. timeline of cards (same axis, one lane per trail)
   C. four leg maps, numbered, decoys highlighted
All positions come from the recorded itinerary and from stops.js / the route
plan, so the drawings cannot drift from the data.
"""
import math
import sys
from datetime import date

sys.stdout.reconfigure(encoding='utf-8')

COL = {'leif': '#216580', 'rollo': '#a2562d', 'aud': '#6d528b', 'harald': '#467444'}
NAME = {'leif': 'Leif', 'rollo': 'Rollo', 'aud': 'Aud', 'harald': 'Harald'}
DIGIT = {'leif': '1', 'rollo': '9', 'aud': '7', 'harald': '2'}
INK, RULE, MUTED = '#283B34', '#c9c2ad', '#657065'
DECOY = '#8a2f2f'

# REDATED 20 Sept 2026 for the blocked-leg model. Liv no longer interleaves the
# four trails: she finishes each leg before starting the next, and the journey
# spans two calendar years -- Leif and Rollo in autumn of year one, Aud and
# Harald in May-July of year two, wintering abroad in between.
Y1, Y2 = 2024, 2025
# card, trail, date, nights, place, lat, lng, real?
STOPS = [
    # -- Leif, 24 Aug - 16 Sept Y1 ------------------------------------------
    ('L1', 'leif',   date(Y1, 8, 24), 4, "L'Anse aux Meadows", 51.595, -55.533, True),
    ('L2', 'leif',   date(Y1, 8, 30), 3, 'Battle Harbour',     52.270, -55.580, True),
    ('LD', 'leif',   date(Y1, 9, 5),  3, 'Brattahlíð',         61.160, -45.510, False),
    ('L3', 'leif',   date(Y1, 9, 11), 5, 'Qikiqtarjuaq',       67.560, -64.030, True),
    # -- Rollo, 28 Sept - 6 Nov Y1 ------------------------------------------
    ('RD', 'rollo',  date(Y1, 9, 28), 3, 'Walcheren',          51.530,   3.550, False),
    ('R1', 'rollo',  date(Y1, 10, 4), 3, 'Châlus',             45.655,   0.981, True),
    ('R2', 'rollo',  date(Y1, 10, 11), 4, 'Rouen',             49.443,   1.099, True),
    ('R3', 'rollo',  date(Y1, 10, 18), 3, 'Bayeux',            49.277,  -0.703, True),
    ('R4', 'rollo',  date(Y1, 10, 24), 3, 'Winchester',        51.060,  -1.313, True),
    ('R5', 'rollo',  date(Y1, 10, 29), 2, 'Battle',            50.914,   0.487, True),
    ('R6', 'rollo',  date(Y1, 11, 3),  3, 'Roumare Forest',    49.413,   0.965, True),
    # -- Aud, 9 - 30 May Y2 -------------------------------------------------
    ('A1', 'aud',    date(Y2, 5, 9),  3, 'Dögurðarnes',        65.170, -22.520, True),
    ('A2', 'aud',    date(Y2, 5, 20), 4, 'Hvammur',            65.219, -21.829, True),
    # AD moved after A2, 25 Sept 2026 (was 14 May, 2nd): its message says Liv found the comb
    # with the coins, which happens in the Hvammur treasure hunt. 3rd still satisfies the
    # leg's one rule (the decoy never opens or closes the block).
    ('AD', 'aud',    date(Y2, 5, 24), 3, 'Bjarnarhöfn',        64.998, -22.967, False),
    ('A3', 'aud',    date(Y2, 5, 27), 3, 'Esjuberg',           64.230, -21.800, True),
    # -- Harald, 6 June - 26 July Y2 ----------------------------------------
    ('H1', 'harald', date(Y2, 6, 6),  7, 'Oslo',               59.908,  10.767, True),
    ('H2', 'harald', date(Y2, 6, 17), 4, 'Staraya Ladoga',     59.998,  32.295, True),
    ('H3', 'harald', date(Y2, 6, 23), 4, 'Kyiv',               50.450,  30.523, True),
    ('H4', 'harald', date(Y2, 7, 1),  3, 'Hedeby',             54.491,   9.566, True),
    ('H5', 'harald', date(Y2, 7, 8),  4, 'Aci Castello',       37.5545,  15.1462, True),
    ('HD', 'harald', date(Y2, 7, 15), 3, 'Constantinople',     41.008,  28.978, False),
    ('H6', 'harald', date(Y2, 7, 21), 5, 'Patara',             36.270,  29.290, True),
]

T0, T1 = date(Y1, 8, 12), date(Y2, 8, 8)
SPAN = (T1 - T0).days


def months():
    """Every month boundary the axis crosses, across the two years."""
    out, d = [], date(T0.year, T0.month, 1)
    while d <= T1:
        if d >= T0:
            out.append(d)
        d = date(d.year + 1, 1, 1) if d.month == 12 else date(d.year, d.month + 1, 1)
    return out


def esc(s):
    return (s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))


# ----------------------------------------------------------------- A: events
def timeline_events():
    W, H = 1120, 268
    L, R = 48, 24
    inner = W - L - R
    axis_y = 168

    def x(d):
        return L + inner * (d - T0).days / SPAN

    p = [f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" '
         f'aria-label="Timeline of Liv\'s 22 stops across two years, one leg at a time, '
         f'coloured by trail" xmlns="http://www.w3.org/2000/svg" '
         f'style="display:block;max-width:100%;height:auto">']
    p.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="none"/>')

    # month grid
    for d0 in months():
        mx = x(d0)
        jan = d0.month == 1
        p.append(f'<line x1="{mx:.1f}" y1="{axis_y - 118}" x2="{mx:.1f}" y2="{axis_y + 14}" '
                 f'stroke="{"#a2562d" if jan else RULE}" stroke-width="{1.4 if jan else 1}" '
                 f'stroke-dasharray="{"4 3" if jan else "2 4"}"/>')
        p.append(f'<text x="{mx:.1f}" y="{axis_y + 30}" font-size="12" '
                 f'fill="{"#a2562d" if jan else MUTED}" text-anchor="middle" '
                 f'font-family="Helvetica,Arial,sans-serif">'
                 f'{d0.strftime("%b") + " " + str(d0.year) if jan else d0.strftime("%b")}</text>')

    p.append(f'<line x1="{L}" y1="{axis_y}" x2="{W - R}" y2="{axis_y}" '
             f'stroke="{INK}" stroke-width="1.6"/>')

    # Stagger labels so close dates stay legible. Blocked legs bunch the stops
    # into four tight clusters, which three rows could not hold -- five rows, and
    # always take the row whose last label sits furthest left, so a dense cluster
    # spreads evenly instead of piling onto the first row that happens to clear.
    NROWS, MINGAP = 5, 74
    rows = [-1e9] * NROWS
    for i, (code, trail, d, nights, place, *_rest) in enumerate(STOPS):
        real = _rest[2]
        px = x(d)
        row = min(range(NROWS), key=lambda r: rows[r])
        for r in range(NROWS):
            if px - rows[r] > MINGAP:
                row = r
                break
        rows[row] = px
        ly = axis_y - 22 - row * 21
        c = COL[trail]
        p.append(f'<line x1="{px:.1f}" y1="{axis_y}" x2="{px:.1f}" y2="{ly + 6:.1f}" '
                 f'stroke="{c}" stroke-width="1"/>')
        if real:
            p.append(f'<circle cx="{px:.1f}" cy="{axis_y}" r="6" fill="{c}" '
                     f'stroke="#fffdf7" stroke-width="1.5"/>')
        else:
            p.append(f'<circle cx="{px:.1f}" cy="{axis_y}" r="6.5" fill="#fffdf7" '
                     f'stroke="{c}" stroke-width="2.4" stroke-dasharray="3 2"/>')
        p.append(f'<text x="{px:.1f}" y="{ly:.1f}" font-size="11.5" fill="{INK}" '
                 f'text-anchor="middle" font-family="Helvetica,Arial,sans-serif">'
                 f'<tspan font-weight="700" fill="{c}">{i + 1}</tspan> {esc(place)}</text>')
        p.append(f'<text x="{px:.1f}" y="{axis_y + 16}" font-size="9.5" fill="{MUTED}" '
                 f'text-anchor="middle" font-family="Helvetica,Arial,sans-serif">'
                 f'{d.strftime("%-d" if sys.platform != "win32" else "%d").lstrip("0")}</text>')

    # legend
    lx = L
    p.append(f'<text x="{lx}" y="{H - 14}" font-size="11.5" fill="{MUTED}" '
             f'font-family="Helvetica,Arial,sans-serif">Trail:</text>')
    lx += 42
    for t in ['leif', 'rollo', 'aud', 'harald']:
        p.append(f'<circle cx="{lx + 6}" cy="{H - 18}" r="5.5" fill="{COL[t]}"/>')
        p.append(f'<text x="{lx + 17}" y="{H - 14}" font-size="11.5" fill="{INK}" '
                 f'font-family="Helvetica,Arial,sans-serif">{NAME[t]} '
                 f'<tspan font-weight="700">{DIGIT[t]}</tspan></text>')
        lx += 92
    p.append(f'<circle cx="{lx + 6}" cy="{H - 18}" r="6" fill="#fffdf7" stroke="{MUTED}" '
             f'stroke-width="2.2" stroke-dasharray="3 2"/>')
    p.append(f'<text x="{lx + 17}" y="{H - 14}" font-size="11.5" fill="{INK}" '
             f'font-family="Helvetica,Arial,sans-serif">hollow = decoy</text>')
    p.append('</svg>')
    return '\n'.join(p)


# ------------------------------------------------------------------ B: cards
def timeline_cards():
    W = 1120
    L, R = 78, 24
    inner = W - L - R
    lane_h = 44
    trails = ['leif', 'rollo', 'aud', 'harald']
    H = 34 + lane_h * len(trails) + 34

    def x(d):
        return L + inner * (d - T0).days / SPAN

    p = [f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" '
         f'aria-label="The same timeline split into one lane per trail, showing which '
         f'trail is active when" xmlns="http://www.w3.org/2000/svg" '
         f'style="display:block;max-width:100%;height:auto">']

    for d0 in months():
        mx = x(d0)
        jan = d0.month == 1
        p.append(f'<line x1="{mx:.1f}" y1="22" x2="{mx:.1f}" y2="{H - 30}" '
                 f'stroke="{"#a2562d" if jan else RULE}" stroke-width="{1.4 if jan else 1}" '
                 f'stroke-dasharray="{"4 3" if jan else "2 4"}"/>')
        p.append(f'<text x="{mx:.1f}" y="16" font-size="12" '
                 f'fill="{"#a2562d" if jan else MUTED}" text-anchor="middle" '
                 f'font-family="Helvetica,Arial,sans-serif">'
                 f'{d0.strftime("%b") + " " + str(d0.year) if jan else d0.strftime("%b")}</text>')

    for li, t in enumerate(trails):
        ly = 42 + li * lane_h
        c = COL[t]
        p.append(f'<text x="{L - 12}" y="{ly + 4}" font-size="12.5" fill="{c}" '
                 f'text-anchor="end" font-weight="700" '
                 f'font-family="Helvetica,Arial,sans-serif">{NAME[t]} {DIGIT[t]}</text>')
        pts = [s for s in STOPS if s[1] == t]
        xs = [x(s[2]) for s in pts]
        p.append(f'<line x1="{min(xs):.1f}" y1="{ly:.1f}" x2="{max(xs):.1f}" y2="{ly:.1f}" '
                 f'stroke="{c}" stroke-width="1.2" opacity="0.45"/>')
        for code, _tr, d, _n, place, _la, _lo, real in pts:
            px = x(d)
            if real:
                p.append(f'<rect x="{px - 13:.1f}" y="{ly - 9:.1f}" width="26" height="18" '
                         f'rx="4" fill="{c}"/>')
                p.append(f'<text x="{px:.1f}" y="{ly + 4:.1f}" font-size="11" fill="#fffdf7" '
                         f'text-anchor="middle" font-weight="700" '
                         f'font-family="Helvetica,Arial,sans-serif">{code}</text>')
            else:
                p.append(f'<rect x="{px - 13:.1f}" y="{ly - 9:.1f}" width="26" height="18" '
                         f'rx="4" fill="#fffdf7" stroke="{c}" stroke-width="2" '
                         f'stroke-dasharray="3 2"/>')
                p.append(f'<text x="{px:.1f}" y="{ly + 4:.1f}" font-size="11" fill="{c}" '
                         f'text-anchor="middle" font-weight="700" '
                         f'font-family="Helvetica,Arial,sans-serif">{code}</text>')

    p.append(f'<text x="{L}" y="{H - 10}" font-size="11.5" fill="{MUTED}" '
             f'font-family="Helvetica,Arial,sans-serif">'
             f'Each card sits on the date Liv sent it. Dashed = decoy. '
             f'The lanes no longer overlap, which is the point: the work has moved from unpicking an interleaved calendar to ordering four short legs.'
             f'</text>')
    p.append('</svg>')
    return '\n'.join(p)


# ------------------------------------------------------------------- C: maps
def mercator(lat, lng):
    lat = max(min(lat, 84.0), -84.0)
    return lng, math.degrees(math.log(math.tan(math.radians(45 + lat / 2))))


def leg_map(trail):
    pts = [s for s in STOPS if s[1] == trail]
    real = [s for s in pts if s[7]]
    decoy = next(s for s in pts if not s[7])
    # decoy's slot inside its own trail, by date
    di = sorted(pts, key=lambda s: s[2]).index(decoy)

    W, H = 268, 300
    PAD_T, PAD_B, PAD_X = 42, 34, 30
    proj = {s[0]: mercator(s[5], s[6]) for s in pts}
    xs = [v[0] for v in proj.values()]
    ys = [v[1] for v in proj.values()]
    spanx = max(xs) - min(xs) or 1
    spany = max(ys) - min(ys) or 1
    avail_w, avail_h = W - 2 * PAD_X, H - PAD_T - PAD_B
    k = min(avail_w / spanx, avail_h / spany)       # uniform: shape must not distort
    cx, cy = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2

    def P(code):
        mx, my = proj[code]
        return (W / 2 + (mx - cx) * k, PAD_T + avail_h / 2 - (my - cy) * k)

    c = COL[trail]
    p = [f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" '
         f'aria-label="{NAME[trail]}\'s trail: {len(real)} numbered stops drawing the digit '
         f'{DIGIT[trail]}, with the {esc(decoy[4])} decoy marked" '
         f'xmlns="http://www.w3.org/2000/svg" '
         f'style="display:block;max-width:100%;height:auto">']
    p.append(f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="9" '
             f'fill="#fffcf4" stroke="{RULE}"/>')
    p.append(f'<text x="14" y="22" font-size="13" font-weight="700" fill="{c}" '
             f'font-family="Helvetica,Arial,sans-serif">{NAME[trail]}</text>')
    p.append(f'<text x="{W - 14}" y="24" font-size="21" font-weight="700" fill="{c}" '
             f'text-anchor="end" opacity="0.5" '
             f'font-family="Helvetica,Arial,sans-serif">{DIGIT[trail]}</text>')

    # the wrong path, if the decoy were left in
    order_with = sorted(pts, key=lambda s: s[2])
    wrong = ' '.join(f'{P(s[0])[0]:.1f},{P(s[0])[1]:.1f}' for s in order_with)
    p.append(f'<polyline points="{wrong}" fill="none" stroke="{DECOY}" stroke-width="1.3" '
             f'stroke-dasharray="4 3" opacity="0.75"/>')

    # the real route
    real_pts = ' '.join(f'{P(s[0])[0]:.1f},{P(s[0])[1]:.1f}' for s in real)
    p.append(f'<polyline points="{real_pts}" fill="none" stroke="{c}" stroke-width="2.6" '
             f'stroke-linejoin="round" stroke-linecap="round"/>')

    # Dots sit at their true projected position; only the NUMBER BADGES are pushed
    # apart, with a leader line back to the dot. Rouen/Roumare are 3.6 px apart on
    # this panel and L'Anse/Battle Harbour 7.6 px, so without this the badges are
    # unreadable -- and moving the dots themselves would falsify the shape.
    marks = [(str(i), P(s[0]), c, True) for i, s in enumerate(real, 1)]
    marks.append(('D', P(decoy[0]), DECOY, False))

    lab = [list(m[1]) for m in marks]
    for _ in range(320):
        for i in range(len(lab)):
            for j in range(i + 1, len(lab)):
                ddx = lab[j][0] - lab[i][0]
                ddy = lab[j][1] - lab[i][1]
                dist = math.hypot(ddx, ddy)
                if dist < 21:
                    if dist < 0.01:
                        ddx, ddy, dist = 1.0, 0.6, 1.17
                    push = (21 - dist) / 2
                    ux, uy = ddx / dist, ddy / dist
                    lab[i][0] -= ux * push; lab[i][1] -= uy * push
                    lab[j][0] += ux * push; lab[j][1] += uy * push
        for i, (_t, (ax, ay), _c, _r) in enumerate(marks):   # light pull home
            lab[i][0] += (ax - lab[i][0]) * 0.06
            lab[i][1] += (ay - lab[i][1]) * 0.06
            lab[i][0] = max(13, min(W - 13, lab[i][0]))
            lab[i][1] = max(PAD_T - 8, min(H - PAD_B - 4, lab[i][1]))

    for (txt, (ax, ay), col, is_real), (lx, ly) in zip(marks, lab):
        if math.hypot(lx - ax, ly - ay) > 3:
            p.append(f'<line x1="{ax:.1f}" y1="{ay:.1f}" x2="{lx:.1f}" y2="{ly:.1f}" '
                     f'stroke="{col}" stroke-width="0.9" opacity="0.65"/>')
        if is_real:
            p.append(f'<circle cx="{ax:.1f}" cy="{ay:.1f}" r="3.4" fill="{col}"/>')
            p.append(f'<circle cx="{lx:.1f}" cy="{ly:.1f}" r="8.6" fill="{col}" '
                     f'stroke="#fffdf7" stroke-width="1.5"/>')
            fill = '#fffdf7'
        else:
            p.append(f'<circle cx="{ax:.1f}" cy="{ay:.1f}" r="3.4" fill="{col}"/>')
            p.append(f'<circle cx="{lx:.1f}" cy="{ly:.1f}" r="9" fill="#fffdf7" '
                     f'stroke="{col}" stroke-width="2.4" stroke-dasharray="3.5 2.5"/>')
            fill = col
        p.append(f'<text x="{lx:.1f}" y="{ly + 3.6:.1f}" font-size="10.5" fill="{fill}" '
                 f'text-anchor="middle" font-weight="700" '
                 f'font-family="Helvetica,Arial,sans-serif">{txt}</text>')

    p.append(f'<text x="14" y="{H - 18}" font-size="10.5" fill="{MUTED}" '
             f'font-family="Helvetica,Arial,sans-serif">decoy: {esc(decoy[4])} '
             f'(would sit {di + 1} of {len(pts)})</text>')
    p.append(f'<text x="14" y="{H - 6}" font-size="10" fill="{MUTED}" '
             f'font-family="Helvetica,Arial,sans-serif">'
             f'{" \u2192 ".join(s[0] for s in real)}</text>')
    p.append('</svg>')
    return '\n'.join(p)


if __name__ == '__main__':
    import json
    import pathlib
    out = {
        'events': timeline_events(),
        'cards': timeline_cards(),
        'maps': {t: leg_map(t) for t in ['leif', 'rollo', 'aud', 'harald']},
    }
    # Written next to this script so the run is reproducible on any machine;
    # the previous version pointed at one session's temp directory.
    p = str(pathlib.Path(__file__).resolve().parent / 'final_riddle_visuals.json')
    open(p, 'w', encoding='utf-8').write(json.dumps(out))
    print('generated', {k: len(v) if isinstance(v, str) else len(str(v)) for k, v in out.items()})
