"""Trim Codex's rebus drawings for the ruler (PP-025). Sources stay untouched in Postcards/RebusIcons.

Adds a little padding, crops to the visible drawing (alpha above a threshold, so the faint glow
around the art does not count) and writes Icons/<name>.png for build_ruler_pdf.py.
"""
from pathlib import Path

from PIL import Image, ImageFilter

SRC = Path(__file__).resolve().parents[2] / "Postcards" / "RebusIcons"
DST = Path(__file__).with_name("Icons")
FILES = {
    "Rebus_Pear_Pencil.png": "pear.png",
    "Rebus_Letter_S_Pencil.png": "s.png",
    "Rebus_Sheep_Pencil.png": "sheep.png",
    "Rebus_Long_Marker_Pencil.png": "long.png",
}
# Line-art-only drawings with no light fill are recoloured cream, so they show on the green card.
TINT_CREAM = set()  # empty since 15 Oct 2026: Codex re-made the long arrow with a light fill
ALPHA_MIN = 40
PAD = 12


def trim(src: Path, dst: Path) -> None:
    im = Image.open(src).convert("RGBA")
    box = im.getchannel("A").point(lambda a: 255 if a >= ALPHA_MIN else 0).getbbox()
    l, t, r, b = box
    box = (max(0, l - PAD), max(0, t - PAD), min(im.width, r + PAD), min(im.height, b + PAD))
    pad = 20 if dst.name in TINT_CREAM else 0
    out = im.crop(box)
    if pad:
        grown = Image.new("RGBA", (out.width + 2 * pad, out.height + 2 * pad), (0, 0, 0, 0))
        grown.paste(out, (pad, pad))
        out = grown
    if dst.name in TINT_CREAM:
        cream = Image.new("RGBA", out.size, (239, 227, 196, 255))
        # the line is hair-thin at 17 mm wide, so thicken it (about 0.4 mm at print size)
        cream.putalpha(out.getchannel("A").filter(ImageFilter.MaxFilter(31)))
        out = cream
    out.save(dst, dpi=(300, 300), optimize=True)
    print(dst.name, out.size)


RAVEN = Path(__file__).with_name("Family_Symbol_Raven_Crest_Light_v1.png")

if __name__ == "__main__":
    DST.mkdir(exist_ok=True)
    for s, d in FILES.items():
        trim(SRC / s, DST / d)
    trim(RAVEN, DST / "raven.png")  # the game's raven crest, middle band of the ruler
