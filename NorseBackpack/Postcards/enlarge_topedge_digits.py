"""Enlarge the four split cloud-fleck digits without changing either card below the sky.

Coordinates are measured on the joined, 1500 px wide pair: L2 rotated 180 degrees
above L3. Each card is edited only in its top 50 source rows. The old flecks are
inpainted, then their light-on-sky residual is enlarged 1.4x around the same x centre.
"""

from pathlib import Path

import cv2
import numpy as np
from PIL import Image


HERE = Path(__file__).resolve().parent
CENTRES = (350, 620, 880, 1150)  # joined orientation, pixels
SOURCE_HALF_WIDTH = 16
SOURCE_HALF_HEIGHT = 36
SCALE = 1.4


def edit(source: Path, output: Path, rotate_for_join: bool) -> None:
    image = Image.open(source).convert("RGB")
    if image.size != (1500, 1050):
        raise ValueError(f"Unexpected illustration size: {image.size}")
    if rotate_for_join:
        image = image.rotate(180)

    original = np.asarray(image).copy()
    # Work with both seam edges at the top of the array.
    if rotate_for_join:
        original = np.flipud(original).copy()

    mask = np.zeros(original.shape[:2], np.uint8)
    for center in CENTRES:
        mask[0:SOURCE_HALF_HEIGHT, center - SOURCE_HALF_WIDTH:center + SOURCE_HALF_WIDTH] = 255
    clean = cv2.inpaint(original, mask, 5, cv2.INPAINT_TELEA)
    result = clean.astype(np.float32)

    for center in CENTRES:
        x0, x1 = center - SOURCE_HALF_WIDTH, center + SOURCE_HALF_WIDTH
        source_delta = original[:SOURCE_HALF_HEIGHT, x0:x1].astype(np.float32) - clean[:SOURCE_HALF_HEIGHT, x0:x1].astype(np.float32)
        # The digit ink is the positive, pale cloud-fleck difference. Retain
        # its original mottling rather than drawing solid type over the sky.
        flecks = np.maximum(source_delta - 3.0, 0.0)
        width = round((x1 - x0) * SCALE)
        height = round(SOURCE_HALF_HEIGHT * SCALE)
        enlarged = cv2.resize(flecks, (width, height), interpolation=cv2.INTER_LINEAR)
        left = round(center - width / 2)
        area = result[:height, left:left + width]
        result[:height, left:left + width] = np.minimum(area + enlarged, 255)

    result = Image.fromarray(result.astype(np.uint8), "RGB")
    if rotate_for_join:
        result = result.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    # Preserve the original alpha and its exact pixels; the original has
    # opaque artwork, but keeping the channel avoids a mode change.
    alpha = Image.open(source).getchannel("A")
    result.putalpha(alpha)
    result.save(output, optimize=True, dpi=(300, 300))


def build_proof() -> None:
    upper = Image.open(HERE / "Postcard_L2_Battle_Harbour_Illustration_v2.png").convert("RGB").rotate(180)
    lower = Image.open(HERE / "Postcard_L3_Baffin_Island_Illustration_v2.png").convert("RGB")
    joined = Image.new("RGB", (1500, 100))
    joined.paste(upper.crop((0, 1000, 1500, 1050)), (0, 0))
    joined.paste(lower.crop((0, 0, 1500, 50)), (0, 50))
    proof = Image.new("RGB", (1280, 400))
    for index, center in enumerate(CENTRES):
        tile = joined.crop((center - 40, 0, center + 40, 100))
        proof.paste(tile.resize((320, 400), Image.Resampling.NEAREST), (index * 320, 0))
    proof.save(HERE / "Postcard_L2_L3_1576_Alignment_Proof.png", optimize=True)


if __name__ == "__main__":
    edit(HERE / "Postcard_L2_Battle_Harbour_Illustration_v1.png", HERE / "Postcard_L2_Battle_Harbour_Illustration_v2.png", True)
    edit(HERE / "Postcard_L3_Baffin_Island_Illustration_v1.png", HERE / "Postcard_L3_Baffin_Island_Illustration_v2.png", False)
    build_proof()
