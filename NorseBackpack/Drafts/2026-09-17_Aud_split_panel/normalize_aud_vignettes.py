"""Normalize Aud's treasure-map vignettes for print.

ImageGen source renders are converted to one flat #6D528B ink, with transparent holes retained,
then fitted to equal square canvases.  The map can therefore place them at print scale without
each source render carrying a different glow, colour or margin.
"""

from pathlib import Path

from PIL import Image


HERE = Path(__file__).resolve().parent
ART = HERE / "Art"
SOURCES = ART / "Sources"
INK = (109, 82, 139)  # #6D528B
CANVAS = 1024
CONTENT = 840
ALPHA_FLOOR = 24

ASSETS = {
    "Aud_ford_v2": "Aud_ford_v2_ImageGen_Source.png",
    "Aud_mill_v2": "Aud_mill_v2_ImageGen_Source.png",
    "Aud_falls_v2": "Aud_falls_v2_ImageGen_Source.png",
    "Aud_fold_v2": "Aud_fold_v2_ImageGen_Source.png",
    "Aud_chapel_v2": "Aud_chapel_v2_ImageGen_Source.png",
    "Aud_cairn_v2": "Aud_cairn_v2_ImageGen_Source.png",
    "Aud_stone_v2": "Aud_stone_v2_ImageGen_Source.png",
    "Aud_naust_v2": "Aud_naust_v2_ImageGen_Source.png",
    "Aud_farm_v2": "Aud_farm_v2_ImageGen_Source.png",
    "Aud_birch_v2": "Aud_birch_v2_ImageGen_Source.png",
}


def normalize(source: Path, destination: Path) -> None:
    image = Image.open(source).convert("RGBA")
    alpha = image.getchannel("A").point(
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
