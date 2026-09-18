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

Y = 2026
# card, trail, date, nights, place, lat, lng, real?
STOPS = [
    ('L1', 'leif',   date(Y, 2, 2),  4, "L'Anse aux Meadows", 51.595, -55.533, True),
    ('L2', 'leif',   date(Y, 2, 10), 3, 'Battle Harbour',     52.270, -55.580, True),
    ('L3', 'leif',   date(Y, 2, 18), 6, 'Qikiqtarjuaq',       67.560, -64.030, True),
    ('R1', 'rollo',  date(Y, 3, 8),  3, 'Châlus',             45.655,   0.981, True),
    ('R2', 'rollo',  date(Y, 3, 17), 5, 'Rouen',              49.443,   1.099, True),
    ('A1', 'aud',    date(Y, 4, 5),  4, 'Dögurðarnes',        65.170, -22.520, True),
    ('A2', 'aud',    date(Y, 4, 13), 5, 'Hvammur',            65.219, -21.829, True),
    ('H1', 'harald', date(Y, 4, 28), 7, 'Oslo',               59.908,  10.767, True),
    ('AD', 'aud',    date(Y, 5, 13), 3, 'Bjarnarhöfn',        64.998, -22.967, False),
    ('A3', 'aud',    date(Y, 5, 20), 4, 'Esjuberg',           64.230, -21.800, True),
    ('LD', 'leif',   date(Y, 6, 12), 5, 'Brattahlíð',         61.160, -45.510, False),
    ('H2', 'harald', date(Y, 7, 3),  4, 'Staraya Ladoga',     59.998,  32.295, True),
    ('H3', 'harald', date(Y, 7, 10), 4, 'Kyiv',               50.450,  30.523, True),
    ('H4', 'harald', date(Y, 8, 1),  4, 'Hedeby',             54.491,   9.566, True),
    ('H5', 'harald', date(Y, 8, 20), 5, 'Sicily',             37.069,  15.288, True),
    ('HD', 'harald', date(Y, 9, 20), 4, 'Constantinople',     41.008,  28.978, False),
    ('R3', 'rollo',  date(Y, 10, 12), 5, 'Bayeux',            49.277,  -0.703, True),
    ('R4', 'rollo',  date(Y, 10, 21), 3, 'Winchester',        51.060,  -1.313, True),
    ('R5', 'rollo',  date(Y, 10, 28), 2, 'Battle',            50.914,   0.487, True),
    ('RD', 'rollo',  date(Y, 11, 8),  3, 'Walcheren',         51.530,   3.550, False),
    ('R6', 'rollo',  date(Y, 11, 20), 4, 'Roumare Forest',    49.413,   0.965, True),
    ('H6', 'harald', date(Y, 12, 8),  7, 'Patara',            36.270,  29.290, True),
]

T0, T1 = date(Y, 1, 28), date(Y, 12, 22)
SPAN = (T1 - T0).days


def esc(s):
    return (s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))


# ----------------------------------------------------------------- A: events
def timeline_events():
    W, H = 1120, 250
    L, R = 48, 24
    inner = W - L - R
    axis_y = 150

    def x(d):
        return L + inner * (d - T0).days / SPAN

    p = [f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" '
         f'aria-label="Timeline of Liv\'s 22 stops from 2 February to 15 December, '
         f'coloured by trail" xmlns="http://www.w3.org/2000/svg" '
         f'style="display:block;max-width:100%;height:auto">']
    p.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="none"/>')

    # month grid
    for m in range(2, 13):
        mx = x(date(Y, m, 1))
        p.append(f'<line x1="{mx:.1f}" y1="{axis_y - 92}" x2="{mx:.1f}" y2="{axis_y + 14}" '
                 f'stroke="{RULE}" stroke-width="1" stroke-dasharray="2 4"/>')
        p.append(f'<text x="{mx:.1f}" y="{axis_y + 30}" font-size="12" fill="{MUTED}" '
                 f'text-anchor="middle" font-family="Helvetica,Arial,sans-serif">'
                 f'{date(Y, m, 1).strftime("%b")}</text>')

    p.append(f'<line x1="{L}" y1="{axis_y}" x2="{W - R}" y2="{axis_y}" '
             f'stroke="{INK}" stroke-width="1.6"/>')

    # stagger labels over three rows so close dates stay legible
    rows, last_x = [-1e9] * 3, None
    for i, (code, trail, d, nights, place, *_rest) in enumerate(STOPS):
        real = _rest[2]
        px = x(d)
        row = 0
        for r in range(3):
            if px - rows[r] > 78:
                row = r
                break
        else:
            row = 2
        rows[row] = px
        ly = axis_y - 22 - row * 26
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

    for m in range(2, 13):
        mx = x(date(Y, m, 1))
        p.append(f'<line x1="{mx:.1f}" y1="22" x2="{mx:.1f}" y2="{H - 30}" stroke="{RULE}" '
                 f'stroke-width="1" stroke-dasharray="2 4"/>')
        p.append(f'<text x="{mx:.1f}" y="16" font-size="12" fill="{MUTED}" '
                 f'text-anchor="middle" font-family="Helvetica,Arial,sans-serif">'
                 f'{date(Y, m, 1).strftime("%b")}</text>')

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
             f'Overlapping lanes are the interleaving the endgame asks players to unpick.'
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
    out = {
        'events': timeline_events(),
        'cards': timeline_cards(),
        'maps': {t: leg_map(t) for t in ['leif', 'rollo', 'aud', 'harald']},
    }
    p = r'C:\Users\simon\AppData\Local\Temp\claude\C--EscapeBackpack-EscapeBackpack\0bb797c7-5513-4bca-bff8-33877fd3518f\scratchpad\visuals.json'
    open(p, 'w', encoding='utf-8').write(json.dumps(out))
    print('generated', {k: len(v) if isinstance(v, str) else len(str(v)) for k, v in out.items()})
