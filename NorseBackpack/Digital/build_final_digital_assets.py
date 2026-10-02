"""Digital art for the end of the Norse game: the two faces of the adventure medallion.

Crops the front (raven crest) and back ("Adventure complete") from the v2 CAD preview in
Props/Medallion, each to a circle on a transparent background.

Run: python NorseBackpack/Digital/build_final_digital_assets.py
Writes NorseBackpack/Digital/assets/Medallion_Front.webp and Medallion_Back.webp
"""
from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
SRC = HERE.parent / "Props" / "Medallion" / "Medallion_v2_Preview.png"
OUT = HERE / "assets"
# Centres and radius of the two discs in the 2000 x 1170 preview, measured from the image.
FACES = {"Front": (500, 525), "Back": (1500, 525)}
RADIUS = 432
SIZE = 600


def main():
    src = Image.open(SRC).convert("RGBA")
    for name, (cx, cy) in FACES.items():
        disc = src.crop((cx - RADIUS, cy - RADIUS, cx + RADIUS, cy + RADIUS)).resize((SIZE, SIZE), Image.LANCZOS)
        mask = Image.new("L", (SIZE * 4, SIZE * 4), 0)
        ImageDraw.Draw(mask).ellipse((0, 0, SIZE * 4 - 1, SIZE * 4 - 1), fill=255)
        disc.putalpha(mask.resize((SIZE, SIZE), Image.LANCZOS))
        disc.save(OUT / f"Medallion_{name}.webp", "WEBP", quality=90)
        print(OUT / f"Medallion_{name}.webp")


if __name__ == "__main__":
    main()
