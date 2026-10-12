"""Postcard marks cut straight from the iconography drawings (PP-041, Q-054).

Playtest 1 (12 Oct 2026): players struggled to match the separate hand-drawn card marks
against the journal's iconography page. The designer chose to make the marks small copies of
the page's own drawings, so matching is instant. Each crest mark is that charge's field,
cropped from the crest, with rounded corners and a rust edge; each symbol mark is that
subject cropped from the circular symbol with an oval fade, so a little knotwork shows.

Run: python NorseBackpack/Art/FinalPuzzle/build_iconography_marks.py
Writes PostcardMarks/<Set>_<Element>_Iconography_v1.png (transparent, longest side 400 px).
The older *_HandDrawn_v1.png marks are kept, unused.
"""
from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
OUT = HERE / "PostcardMarks"
CREST = HERE / "Family_Crest_Six_Field_v2.png"
SYMBOL = HERE / "Family_Symbol_Three_Field_v2.png"
RUST = (0xB5, 0x6A, 0x2A, 255)
SIZE = 400

# Field interiors in the 1254 px crest, measured by eye from a gridded render. The two bottom
# fields follow the shield's curve, so a sliver of its border shows -- left in on purpose.
CREST_FIELDS = {
    "Battle_Axe": (395, 350, 618, 538),
    "Round_Shield": (660, 350, 882, 538),
    "Wolf": (395, 585, 618, 748),
    "Anchor": (660, 585, 882, 748),
    "Drinking_Horn": (430, 797, 618, 965),
    "Valknut": (660, 797, 848, 965),
}
SYMBOL_SUBJECTS = {
    "Raven": (150, 230, 570, 830),
    "Longship": (680, 240, 1100, 760),
    "Sun_Wheel": (395, 705, 860, 1140),
}


def _mask(size, draw):
    w, h = size
    k = 4
    m = Image.new("L", (w * k, h * k), 0)
    draw(ImageDraw.Draw(m), w * k, h * k, k)
    return m.resize((w, h), Image.LANCZOS)


def crest_tile(src, box):
    tile = src.crop(box)
    radius = 28
    tile.putalpha(_mask(tile.size, lambda d, w, h, k: d.rounded_rectangle(
        (0, 0, w - 1, h - 1), radius=radius * k, fill=255)))
    w, h = tile.size
    edge = Image.new("RGBA", (w * 4, h * 4), (0, 0, 0, 0))
    ImageDraw.Draw(edge).rounded_rectangle((4, 4, w * 4 - 5, h * 4 - 5), radius=radius * 4,
                                           outline=RUST, width=28)
    tile.alpha_composite(edge.resize((w, h), Image.LANCZOS))
    return tile


def symbol_subject(src, box):
    part = src.crop(box)
    oval = _mask(part.size, lambda d, w, h, k: d.ellipse((0, 0, w - 1, h - 1), fill=255))
    part.putalpha(Image.composite(part.getchannel("A"), Image.new("L", part.size, 0), oval))
    return part


def main():
    crest = Image.open(CREST).convert("RGBA")
    symbol = Image.open(SYMBOL).convert("RGBA")
    made = {f"Crest_{k}": crest_tile(crest, b) for k, b in CREST_FIELDS.items()}
    made.update({f"Symbol_{k}": symbol_subject(symbol, b) for k, b in SYMBOL_SUBJECTS.items()})
    for name, im in made.items():
        im.thumbnail((SIZE, SIZE), Image.LANCZOS)
        path = OUT / f"{name}_Iconography_v1.png"
        im.save(path, optimize=True)
        print(path.name, im.size)


if __name__ == "__main__":
    main()
