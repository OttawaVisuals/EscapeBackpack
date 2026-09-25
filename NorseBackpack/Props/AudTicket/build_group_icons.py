"""Coin-group icons for the ticket's Coin Room key (PZ-03, 24 Sept 2026).

Camel = dirhams (eastern trade), fleur-de-lis = deniers (Frankish). The third group, Norse
coins, uses the fehu rune, which is drawn as vector in build_aud_ticket_pdf.py and on Aud's
map (the cache mark), so it is not built here.

Rendered once from Windows' Segoe UI Symbol into transparent PNGs, so the ticket build does
not depend on system fonts. Re-run only to change an icon.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
FONT = Path(r"C:\Windows\Fonts\seguisym.ttf")
ICONS = {"camel": "\U0001F42B", "fleur": "\u269C"}
SIZE = 400


def main():
    font = ImageFont.truetype(str(FONT), 300)
    for name, ch in ICONS.items():
        im = Image.new("L", (SIZE, SIZE), 0)
        d = ImageDraw.Draw(im)
        l, t, r, b = d.textbbox((0, 0), ch, font=font)
        d.text(((SIZE - (r - l)) / 2 - l, (SIZE - (b - t)) / 2 - t), ch, font=font, fill=255)
        im = im.crop(im.getbbox())
        out = Image.new("RGBA", im.size, (0x28, 0x3B, 0x34, 0))
        out.putalpha(im)
        out.save(HERE / "icons" / f"{name}.png")
        print(HERE / "icons" / f"{name}.png", im.size)


if __name__ == "__main__":
    main()
