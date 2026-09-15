"""Normalize the Rollo map's ImageGen vignettes for print.

The source renders include a low-alpha glow and small colour variations.  The map assets need one
flat ink colour, true transparency, consistent square canvases and enough margin to scale cleanly.

Source: Art/Sources/Rollo_*_ImageGen_Source.png
Output: Art/Rollo_*.png
"""

from pathlib import Path

from PIL import Image


HERE = Path(__file__).resolve().parent
ART = HERE / "Art"
SOURCES = ART / "Sources"
INK = (162, 86, 45)
CANVAS = 1024
CONTENT = 840
ALPHA_FLOOR = 24

ASSETS = {
    "Rollo_Crossbow_Bolt_v1": "Rollo_Crossbow_Bolt_v1_ImageGen_Source.png",
    "Rollo_Treaty_Scroll_v1": "Rollo_Treaty_Scroll_v1_ImageGen_Source.png",
    "Rollo_Ducal_Coronet_v1": "Rollo_Ducal_Coronet_v1_ImageGen_Source.png",
    "Rollo_Needle_Thread_v1": "Rollo_Needle_Thread_v1_ImageGen_Source.png",
    "Rollo_Crown_v1": "Rollo_Crown_v1_ImageGen_Source.png",
    "Rollo_Longship_v1": "Rollo_Longship_v1_ImageGen_Source.png",
    "Rollo_Boar_v1": "Rollo_Boar_v1_ImageGen_Source.png",
    "Rollo_Combat_v1": "Rollo_Combat_v1_ImageGen_Source.png",
    "Rollo_Cow_v1": "Rollo_Cow_v1_ImageGen_Source.png",
    "Rollo_Forest_v1": "Rollo_Forest_v1_ImageGen_Source.png",
    "Rollo_Hen_v1": "Rollo_Hen_v1_ImageGen_Source.png",
    "Rollo_Folk_v1": "Rollo_Folk_v1_ImageGen_Source.png",
    "Rollo_Inn_v1": "Rollo_Inn_v1_ImageGen_Source.png",
}


def normalize(source: Path, destination: Path) -> None:
    image = Image.open(source).convert("RGBA")
    alpha = image.getchannel("A")
    alpha = alpha.point(
        lambda value: 0 if value <= ALPHA_FLOOR
        else round((value - ALPHA_FLOOR) * 255 / (255 - ALPHA_FLOOR))
    )
    bbox = alpha.getbbox()
    if bbox is None:
        raise ValueError(f"No visible artwork in {source}")

    alpha = alpha.crop(bbox)
    scale = min(CONTENT / alpha.width, CONTENT / alpha.height)
    size = (max(1, round(alpha.width * scale)), max(1, round(alpha.height * scale)))
    alpha = alpha.resize(size, Image.Resampling.LANCZOS)

    output = Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0))
    ink = Image.new("RGBA", size, INK + (255,))
    ink.putalpha(alpha)
    output.alpha_composite(ink, ((CANVAS - size[0]) // 2, (CANVAS - size[1]) // 2))
    output.save(destination, dpi=(300, 300), optimize=True)


def main() -> None:
    for stem, source_name in ASSETS.items():
        destination = ART / f"{stem}.png"
        normalize(SOURCES / source_name, destination)
        print(destination.name)


if __name__ == "__main__":
    main()
