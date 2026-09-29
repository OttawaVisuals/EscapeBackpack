"""Normalize the transparent ImageGen rebus drawings for postcard printing.

The unmodified renders live under Sources/. Each output is centred on the shared
1024px transparent canvas used by the other production rebus icons.
"""

from pathlib import Path

from PIL import Image


HERE = Path(__file__).resolve().parent
SOURCES = HERE / "Sources"
CANVAS = 1024
CONTENT = 820

FILES = {
    "Rebus_Fish_Scale_Patch_Bayeux_v3_ImageGen_Source.png": "Rebus_Fish_Scale_Patch_Bayeux_v3.png",
    "Rebus_Hand_One_Bayeux_v1_ImageGen_Source.png": "Rebus_Hand_One_Bayeux_v1.png",
    "Rebus_Hand_Two_Bayeux_v1_ImageGen_Source.png": "Rebus_Hand_Two_Bayeux_v1.png",
    "Rebus_Die_1_Bayeux_v1_ImageGen_Source.png": "Rebus_Die_1_Bayeux_v1.png",
    "Rebus_Die_1_Perspective_Bayeux_v2_ImageGen_Source.png": "Rebus_Die_1_Perspective_Bayeux_v2.png",
    "Rebus_Die_1_Perspective_Bayeux_v3_ImageGen_Source.png": "Rebus_Die_1_Perspective_Bayeux_v3.png",
    "Rebus_Die_1_Perspective_Bayeux_v4_ImageGen_Source.png": "Rebus_Die_1_Perspective_Bayeux_v4.png",
    "Rebus_Die_1_Perspective_Bayeux_v6_ImageGen_Source.png": "Rebus_Die_1_Perspective_Bayeux_v6.png",
    "Rebus_Roman_V_Bayeux_v1_ImageGen_Source.png": "Rebus_Roman_V_Bayeux_v1.png",
}


def normalize(source: Path, destination: Path) -> None:
    art = Image.open(source).convert("RGBA")
    alpha = art.getchannel("A")
    bounds = alpha.getbbox()
    if bounds is None:
        raise ValueError(f"No visible artwork in {source}")
    art = art.crop(bounds)
    scale = min(CONTENT / art.width, CONTENT / art.height)
    size = (max(1, round(art.width * scale)), max(1, round(art.height * scale)))
    art = art.resize(size, Image.Resampling.LANCZOS)
    output = Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0))
    output.alpha_composite(art, ((CANVAS - size[0]) // 2, (CANVAS - size[1]) // 2))
    output.save(destination, dpi=(300, 300), optimize=True)


def main() -> None:
    for source_name, output_name in FILES.items():
        output = HERE / output_name
        normalize(SOURCES / source_name, output)
        print(output)


if __name__ == "__main__":
    main()
