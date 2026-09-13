"""Fill enclosed transparent holes in Codex's map vignettes (PR-11 / PR-12).

The reference grid is drawn under every label but the vignettes were composited with fully
transparent interiors (a sail, a hull, an iceberg face), so the grid printed straight through
them -- a ship made of glass. This is not a style problem, it is a missing opaque fill, and it
can be fixed on the pixels Codex already produced without asking for a re-render.

Method: take each asset's alpha channel, close 1-2px gaps in the linework (binary_closing) so a
nearly-closed outline reads as closed, then fill every fully-enclosed hole (binary_fill_holes)
with a pale paper tone. A genuinely open motif -- the whale and the settlement, both effectively
line art with no enclosed body to begin with -- comes back untouched; this is data-driven per
asset, not a style decision applied uniformly.

Source: Art/*.png (Codex's originals, left alone). Output: Art/processed/*.png (what the build
script actually draws). Re-run this after any new or replaced asset lands in Art/.
"""

import sys
from pathlib import Path

import numpy as np
from PIL import Image
from scipy.ndimage import binary_closing, binary_fill_holes

HERE = Path(__file__).resolve().parent
SRC = HERE / "Art"
OUT = SRC / "processed"
FILL = (250, 248, 240, 255)   # pale paper tone -- reads as sail/hull/rock, not added shading


def process(path: Path) -> int:
    im = Image.open(path).convert("RGBA")
    arr = np.array(im)
    mask = arr[:, :, 3] > 10
    closed = binary_closing(mask, structure=np.ones((5, 5)))
    filled = binary_fill_holes(closed)
    newly = filled & ~mask
    if newly.any():
        arr[newly] = FILL
    OUT.mkdir(exist_ok=True)
    Image.fromarray(arr, "RGBA").save(OUT / path.name)
    return int(newly.sum())


def main():
    for p in sorted(SRC.glob("*.png")):
        n = process(p)
        print("%-26s filled %7d px" % (p.name, n))


if __name__ == "__main__":
    main()
