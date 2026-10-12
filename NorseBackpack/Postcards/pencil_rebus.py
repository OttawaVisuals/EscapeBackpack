"""Pencil-sketch versions of the rebus icons on postcards R3, R4 and R5.

Playtest 1 (11 Oct 2026): the coloured icons read as printed clip art, not as Liv's own
drawings. Chosen in chat: convert the existing icons at build time, rather than wait for new
art -- Codex can still redraw them as real pencil sketches later, and these builders only
need the filename swapped.

Method: flatten the icon on white, take its luminance, colour-dodge it against a blurred
negative (the usual "pencil sketch" filter, which keeps outlines and drops flat fills), keep
the original tone only as diagonal hatching (darker areas get more hatching), add fixed
paper grain, and use the result as the alpha of a single graphite colour. Nothing is written
to disk -- like the Rouen ticket's castle recolour, the source PNGs stay untouched.
"""
from functools import lru_cache
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

GRAPHITE = (0x46, 0x47, 0x4A)
EDGE_BLUR = 14          # px on the 1024 px source; larger = softer, wider outlines
TONE = 0.08             # share of the original shading kept as a flat wash
HATCH_GAP = 34          # px between hatch lines on the 1024 px source
HATCH_WIDTH = 9         # px
LINE_GROW = 9           # px, odd: min-filter size that thickens the outlines
GRAIN = 0.22            # strength of the paper-grain break-up in the strokes


@lru_cache(maxsize=None)
def pencil(path):
    src = Image.open(Path(path)).convert("RGBA")
    alpha = np.asarray(src.getchannel("A"), dtype=np.float32) / 255
    white = Image.new("RGBA", src.size, (255, 255, 255, 255))
    grey = Image.alpha_composite(white, src).convert("L")

    g = np.asarray(grey, dtype=np.float32)
    blur = np.asarray(Image.fromarray(255 - g.astype(np.uint8)).filter(
        ImageFilter.GaussianBlur(EDGE_BLUR)), dtype=np.float32)
    dodge = np.clip(g * 255 / np.maximum(255 - blur, 1), 0, 255)

    shade = (255 - g) / 255                                    # 0 = white fill, 1 = black
    yy, xx = np.indices(g.shape)
    wobble = 3 * np.sin(yy / 37.0) + 2 * np.sin(xx / 53.0)     # keeps the lines off-straight
    hatch = ((xx + yy + wobble) % HATCH_GAP) < HATCH_WIDTH
    hatch_dark = hatch * np.clip((shade - 0.15) / 0.6, 0, 1) * 170
    # Printed at only 20-30 pt, so the outlines are thickened (min filter on the sketch) and
    # pushed darker; at the source's own size they would otherwise thin to a hairline.
    lines = Image.fromarray(dodge.astype(np.uint8)).filter(ImageFilter.MinFilter(LINE_GROW))
    lines = 255 - np.asarray(lines, dtype=np.float32)
    dark = lines * 2.2 + TONE * (255 - g) + hatch_dark          # 0 = paper, 255 = full lead
    dark = np.clip(dark, 0, 255)
    rng = np.random.default_rng(1066)                          # fixed: same grain every build
    grain = Image.fromarray((rng.random(g.shape) * 255).astype(np.uint8)).filter(
        ImageFilter.GaussianBlur(1.2))
    grain = np.asarray(grain, dtype=np.float32) / 255
    dark *= 1 - GRAIN + GRAIN * 2 * grain
    dark *= alpha

    out = np.zeros((*g.shape, 4), dtype=np.uint8)
    out[..., :3] = GRAPHITE
    out[..., 3] = np.clip(dark, 0, 255).astype(np.uint8)
    return Image.fromarray(out, "RGBA")
