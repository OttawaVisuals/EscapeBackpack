"""Digital art for Harald's leg: the Oslo Hnefatafl ticket held up to the light.

The ticket's back carries columns I-K of the board layout in mirror image ("hold to the
light, align on the grid lines", PZ-01/PZ-07). Online there is no light to hold it to, so
the ticket gets a third face: the front, with the back showing through the paper the
right way round, as it looks against a window.

Run: python NorseBackpack/Digital/build_harald_digital_assets.py
Writes NorseBackpack/Digital/assets/Hnefatafl_Ticket_Light.webp
"""
from pathlib import Path

from PIL import Image, ImageChops, ImageEnhance, ImageOps

HERE = Path(__file__).resolve().parent
RENDERS = HERE.parent / "Props" / "_Renders"
OUT = HERE / "assets" / "Hnefatafl_Ticket_Light.webp"


def main():
    front = Image.open(RENDERS / "Hnefatafl_Ticket_Front.png").convert("RGB")
    back = ImageOps.mirror(Image.open(RENDERS / "Hnefatafl_Ticket_Back.png").convert("RGB")).resize(front.size)
    # Light through paper: everything paler, both sides' ink darkening it (multiply), the far side fainter.
    lit_front = ImageEnhance.Brightness(front).enhance(1.12)
    far_side = Image.blend(Image.new("RGB", back.size, (255, 255, 255)), back, 0.62)
    seen = ImageChops.multiply(lit_front, far_side)
    warm = Image.new("RGB", seen.size, (255, 247, 228))
    seen = ImageChops.multiply(ImageEnhance.Brightness(seen).enhance(1.08), warm)
    seen.save(OUT, "WEBP", quality=90)
    print(OUT, seen.size)


if __name__ == "__main__":
    main()
