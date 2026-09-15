"""Prepare the Château de Robert le Diable line icon for print.

The accepted ImageGen render has genuine alpha but includes low-alpha edge noise and small RGB
variations. This keeps the linework, normalizes every visible pixel to black, and centers it on a
standard transparent landscape canvas.

Source: Art/Sources/Rollo_Chateau_Robert_Le_Diable_Line_v1_ImageGen_Source.png
Output: Art/Rollo_Chateau_Robert_Le_Diable_Line_v1.png
"""

from pathlib import Path

from PIL import Image


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "Art" / "Sources" / "Rollo_Chateau_Robert_Le_Diable_Line_v1_ImageGen_Source.png"
OUTPUT = HERE / "Art" / "Rollo_Chateau_Robert_Le_Diable_Line_v1.png"
CANVAS = (1536, 1024)
CONTENT = (1440, 900)
ALPHA_FLOOR = 16


def main() -> None:
    image = Image.open(SOURCE).convert("RGBA")
    alpha = image.getchannel("A").point(
        lambda value: 0
        if value <= ALPHA_FLOOR
        else round((value - ALPHA_FLOOR) * 255 / (255 - ALPHA_FLOOR))
    )
    bbox = alpha.getbbox()
    if bbox is None:
        raise ValueError(f"No visible linework in {SOURCE}")

    alpha = alpha.crop(bbox)
    scale = min(CONTENT[0] / alpha.width, CONTENT[1] / alpha.height)
    size = (max(1, round(alpha.width * scale)), max(1, round(alpha.height * scale)))
    alpha = alpha.resize(size, Image.Resampling.LANCZOS)

    output = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    linework = Image.new("RGBA", size, (0, 0, 0, 255))
    linework.putalpha(alpha)
    output.alpha_composite(
        linework,
        ((CANVAS[0] - size[0]) // 2, (CANVAS[1] - size[1]) // 2),
    )
    output.save(OUTPUT, dpi=(300, 300), optimize=True)
    print(OUTPUT.name)


if __name__ == "__main__":
    main()
