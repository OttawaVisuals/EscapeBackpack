"""Combine the per-coin STLs into two print plates for the Prusa i3 MK3S+.

Plate_Common_9.stl: 4 common dirham, 3 common denier, 1 Hedeby, 1 York (black relief).
Plate_Rare_3.stl:   1 rare dirham, 1 rare denier, 1 raven penny (yellow relief).
Both plates use a gray base; add one colour change at the first relief layer (z = 2.2mm
at 0.2mm layers) in the slicer. Run build_coin_stl.py first.

    python build_coin_plates.py
"""
from pathlib import Path
import re

STL = Path(__file__).resolve().parent / "STL"
BED_CENTRE = (125.0, 105.0)  # MK3S+ bed is 250 x 210 mm
PITCH = 34.0                 # 28mm coins + 6mm gap

PLATES = {
    "Plate_Common_9": ["01_dirham_common"] * 4 + ["03_denier_common"] * 3
                      + ["05_hedeby_ship", "06_york_cross"],
    "Plate_Rare_3": ["02_dirham_rare", "04_denier_rare", "07_raven"],
}
VERTEX = re.compile(r"vertex\s+(\S+)\s+(\S+)\s+(\S+)")


def facets(name):
    text = (STL / f"{name}.stl").read_text(encoding="utf-8")
    return re.findall(r"facet.*?endfacet", text, re.S)


def grid(n):
    cols = 3 if n > 3 else n
    rows = -(-n // cols)
    for i in range(n):
        r, c = divmod(i, cols)
        yield (BED_CENTRE[0] + (c - (cols - 1) / 2) * PITCH,
               BED_CENTRE[1] + ((rows - 1) / 2 - r) * PITCH)


for plate, coins in PLATES.items():
    out = [f"solid {plate}"]
    for name, (dx, dy) in zip(coins, grid(len(coins))):
        for f in facets(name):
            out.append(VERTEX.sub(lambda m: "vertex %.6f %.6f %s" % (
                float(m.group(1)) + dx, float(m.group(2)) + dy, m.group(3)), f))
    out.append(f"endsolid {plate}")
    (STL / f"{plate}.stl").write_text("\n".join(out) + "\n", encoding="utf-8")
    print(plate, len(coins), "coins")
