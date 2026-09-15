"""Normalize the Bayeux-style margin symbols to one production format.

The first three ImageGen renders baked a grey transparency grid into RGB; later
symbols arrived with genuine alpha. Preserve source alpha when present,
otherwise use chroma plus the connected dark outline to extract the artwork.
Untouched renders remain in Sources/ for later revisions.
"""

from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage


HERE = Path(__file__).resolve().parent
SOURCES = HERE / "Sources"
CANVAS = 1024
CONTENT = 820

FILES = {
    "Rebus_Roman_I_Bayeux_v1_ImageGen_Source.png": "Rebus_Roman_I_Bayeux_v1.png",
    "Rebus_Arrow_2_Bayeux_v1_ImageGen_Source.png": "Rebus_Arrow_2_Bayeux_v1.png",
    "Rebus_Die_5_Bayeux_v1_ImageGen_Source.png": "Rebus_Die_5_Bayeux_v1.png",
    "Rebus_Arrow_To_Bayeux_v1_ImageGen_Source.png": "Rebus_Arrow_To_Bayeux_v1.png",
    "Rebus_Fish_Scales_Bayeux_v1_ImageGen_Source.png": "Rebus_Fish_Scales_Bayeux_v1.png",
}


def extract(source: Path, destination: Path) -> None:
    source_image = Image.open(source)
    rgb = np.asarray(source_image.convert("RGB"), dtype=np.int16)
    if source_image.mode == "RGBA" and source_image.getchannel("A").getextrema()[0] == 0:
        alpha = np.asarray(source_image.getchannel("A")).copy()
        alpha[alpha <= 4] = 0
    else:
        chroma = rgb.max(axis=2) - rgb.min(axis=2)
        luminance = rgb.mean(axis=2)

        labels, count = ndimage.label(chroma > 8)
        sizes = np.bincount(labels.ravel(), minlength=count + 1)
        # Keep substantial coloured components. This retains the die's five
        # detached pips while rejecting tiny coloured noise in the fake grid.
        seeds = np.isin(labels, np.flatnonzero(sizes >= 180))
        seeds &= labels != 0
        nearby = ndimage.binary_dilation(seeds, iterations=5)

        # The rendered grid has 0-4 points of channel variation. Starting the
        # ramp above that range prevents pale checker pixels becoming a fringe.
        colour_alpha = np.clip((chroma - 5) * 55, 0, 255)
        dark_alpha = np.clip((125 - luminance) * 7, 0, 255)
        alpha = np.maximum(colour_alpha, dark_alpha)
        alpha = np.where(nearby & ((chroma > 5) | (luminance < 115)), alpha, 0).astype(np.uint8)
        alpha = ndimage.median_filter(alpha, size=3)

    components, component_count = ndimage.label(alpha > 0)
    component_sizes = np.bincount(components.ravel(), minlength=component_count + 1)
    component_sizes[0] = 0
    alpha[components != component_sizes.argmax()] = 0

    bbox = Image.fromarray(alpha, "L").getbbox()
    if bbox is None:
        raise RuntimeError(f"No foreground found in {source}")

    art = Image.fromarray(rgb.astype(np.uint8), "RGB").convert("RGBA")
    art.putalpha(Image.fromarray(alpha, "L"))
    art = art.crop(bbox)
    scale = min(CONTENT / art.width, CONTENT / art.height)
    size = (max(1, round(art.width * scale)), max(1, round(art.height * scale)))
    art = art.resize(size, Image.Resampling.LANCZOS)
    resized_alpha = np.asarray(art.getchannel("A")).copy()
    resized_components, resized_count = ndimage.label(resized_alpha > 0)
    resized_sizes = np.bincount(resized_components.ravel(), minlength=resized_count + 1)
    resized_sizes[0] = 0
    resized_alpha[resized_components != resized_sizes.argmax()] = 0
    art.putalpha(Image.fromarray(resized_alpha, "L"))

    output = Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0))
    output.alpha_composite(art, ((CANVAS - size[0]) // 2, (CANVAS - size[1]) // 2))
    output.save(destination, dpi=(300, 300), optimize=True)


def main() -> None:
    for source_name, destination_name in FILES.items():
        destination = HERE / destination_name
        extract(SOURCES / source_name, destination)
        print(destination)


if __name__ == "__main__":
    main()
