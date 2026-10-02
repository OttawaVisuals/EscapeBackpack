"""Draw the digital architect's scale ruler: three faces of a triangular 30 cm metric ruler,
two scales per face (one along each long edge), as SVG in millimetres.

Scales assume the standard metric set 1:20, 1:25, 1:50, 1:75, 1:100, 1:125. The game's
rebus names 1:125 (PZ-14); if the physical ruler differs, change FACES and re-run.

Run: python NorseBackpack/Digital/build_ruler_svg.py
Writes NorseBackpack/Digital/assets/Ruler_Face_{1,2,3}.svg
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "assets"
LENGTH, WIDTH = 300.0, 15.0      # mm, one face
ZERO = 6.0                       # mm from the left end to the 0 mark
FACES = [(20, 25), (50, 75), (100, 125)]   # (top edge, bottom edge) scales per face
INK, BODY, EDGE = "#1f2a2a", "#f4f1e6", "#b9b4a2"


def ticks(denominator, top):
    """Tick marks and metre labels for one scale along the top or bottom edge."""
    mm_per_m = 1000.0 / denominator
    step = 0.1 if mm_per_m * 0.1 >= 1.0 else 0.2   # never closer than 1 mm apart
    usable = LENGTH - ZERO - 14.0   # keep the right end clear for the scale names
    out = []
    n = 0
    while True:
        metres = round(n * step, 4)
        x = ZERO + metres * mm_per_m
        if x - ZERO > usable:
            break
        whole = abs(metres - round(metres)) < 1e-6
        half = abs(metres * 2 - round(metres * 2)) < 1e-6
        length = 3.4 if whole else 2.4 if half else 1.4
        y1, y2 = (0, length) if top else (WIDTH, WIDTH - length)
        out.append(f'<line x1="{x:.3f}" y1="{y1}" x2="{x:.3f}" y2="{y2:.2f}" stroke="{INK}" stroke-width="{0.16 if whole else 0.11}"/>')
        if whole:
            label_y = 5.6 if top else WIDTH - 4.1
            out.append(f'<text x="{x:.3f}" y="{label_y}" font-size="2" text-anchor="middle">{int(round(metres))}</text>')
        n += 1
    return "".join(out)


def face_svg(top, bottom):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {LENGTH:g} {WIDTH:g}" width="{LENGTH:g}mm" height="{WIDTH:g}mm">
<rect x="0" y="0" width="{LENGTH:g}" height="{WIDTH:g}" rx="0.6" fill="{BODY}" stroke="{EDGE}" stroke-width="0.3"/>
<line x1="0" y1="{WIDTH / 2:g}" x2="{LENGTH:g}" y2="{WIDTH / 2:g}" stroke="{EDGE}" stroke-width="0.12"/>
<g font-family="Helvetica, Arial, sans-serif" fill="{INK}">
{ticks(top, True)}
{ticks(bottom, False)}
<text x="{LENGTH - 2.2:g}" y="5.3" font-size="2.4" font-weight="700" text-anchor="end">1:{top}</text>
<text x="{LENGTH - 2.2:g}" y="{WIDTH - 3.2:g}" font-size="2.4" font-weight="700" text-anchor="end">1:{bottom}</text>
<text x="{LENGTH - 2.2:g}" y="{WIDTH / 2 + 0.7:g}" font-size="1.5" text-anchor="end" fill="#6d7368">m</text>
</g>
</svg>
'''


def main():
    OUT.mkdir(exist_ok=True)
    for i, (top, bottom) in enumerate(FACES, 1):
        (OUT / f"Ruler_Face_{i}.svg").write_text(face_svg(top, bottom), encoding="utf-8")
        print(f"Ruler_Face_{i}.svg  1:{top} / 1:{bottom}")


if __name__ == "__main__":
    main()
