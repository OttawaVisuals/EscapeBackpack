"""4-up postcard print sheets for Staples duplex printing + Cricut cutting.

Combines 4 different postcards per Letter sheet (2x2 grid, landscape) instead of
printing each postcard on its own page. Each card keeps its real front/back
artwork (drawn via the existing draw_front_card/draw_back_card in each card's
own build_postcard_<CODE>_pdf.py script) with crop-mark guides added at the
5x3.5in card boundaries for cutting.

Duplex alignment depends on which edge the printer flips on, and Staples's
online order interface only offers "double sided" with no flip-edge detail. So
this builds BOTH variants per sheet -- test-print page 1 of each, see which one
lines up front-to-back, keep that one and discard the other:

  Postcard_Sheet_01_LongEdge_Print.pdf   (assumes flip on long edge)
  Postcard_Sheet_01_ShortEdge_Print.pdf  (assumes flip on short edge)

"Long edge" mirrors the two columns for the back page (left/right swap).
"Short edge" mirrors the two rows for the back page (top/bottom swap). This
matches the assumption already baked into each card's own single-column
build_letter() (no mirroring needed there since a single column is unaffected
by a left/right swap) -- i.e. the existing 2-up sheets are already implicitly
long-edge sheets.
"""

import importlib.util
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[2]
POSTCARDS_DIR = Path(__file__).resolve().parent
OUT_DIR = ROOT / "output" / "pdf"

LETTER_LANDSCAPE = (11 * 72, 8.5 * 72)
COL_GAP = 0.3 * 72
ROW_GAP = 0.3 * 72

# Every postcard with its own build_postcard_<CODE>_pdf.py script, in the order
# they should fill sheets. Update this list as new postcard scripts are added.
CARD_CODES = [
    "L1", "L2", "L3", "LD",
    "R1", "R2", "R3", "R4",
    "R5", "R6", "RD",
    "H1", "H4", "H5",
]


def load_card_module(code):
    module_name = f"build_postcard_{code}_pdf"
    path = POSTCARDS_DIR / f"{module_name}.py"
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def chunk(items, size):
    return [items[i:i + size] for i in range(0, len(items), size)]


def grid_positions(card_w, card_h, page_w, page_h):
    group_w = 2 * card_w + COL_GAP
    group_h = 2 * card_h + ROW_GAP
    x0 = (page_w - group_w) / 2
    y0 = (page_h - group_h) / 2
    # (row, col) -> (x, y) of the card's lower-left corner. Row 0 is the top row.
    return {
        (0, 0): (x0, y0 + card_h + ROW_GAP),
        (0, 1): (x0 + card_w + COL_GAP, y0 + card_h + ROW_GAP),
        (1, 0): (x0, y0),
        (1, 1): (x0 + card_w + COL_GAP, y0),
    }


def draw_crop_marks(c, x, y, w, h):
    c.saveState()
    c.setStrokeColor(HexColor("#777777"))
    c.setLineWidth(0.35)
    gap, length = 3, 10
    for px in (x, x + w):
        c.line(px, y - gap, px, y - gap - length)
        c.line(px, y + h + gap, px, y + h + gap + length)
    for py in (y, y + h):
        c.line(x - gap, py, x - gap - length, py)
        c.line(x + w + gap, py, x + w + gap + length, py)
    c.restoreState()


def build_sheet(codes, index, flip):
    modules = [load_card_module(code) for code in codes]
    card_w, card_h = modules[0].W, modules[0].H
    for code, module in zip(codes, modules):
        if (module.W, module.H) != (card_w, card_h):
            raise ValueError(
                f"Card {code} is {module.W}x{module.H}pt, expected {card_w}x{card_h}pt "
                f"(PC-13, 5x3.5in). All cards on one sheet must share the same card size."
            )

    page_w, page_h = LETTER_LANDSCAPE
    positions = grid_positions(card_w, card_h, page_w, page_h)
    slots = [(0, 0), (0, 1), (1, 0), (1, 1)][:len(modules)]
    if flip == "long":
        back_slots = [(r, 1 - c) for r, c in slots]
    else:
        back_slots = [(1 - r, c) for r, c in slots]

    label = "-".join(codes)
    out_path = OUT_DIR / f"Postcard_Sheet_{index:02d}_{flip.capitalize()}Edge_Print.pdf"
    c = canvas.Canvas(str(out_path), pagesize=LETTER_LANDSCAPE, pageCompression=1)
    c.setTitle(f"Postcard sheet {index} ({flip}-edge duplex) - {label}")
    c.setAuthor("Escape Backpack")

    for module, slot in zip(modules, slots):
        x, y = positions[slot]
        module.draw_front_card(c, x, y)
        draw_crop_marks(c, x, y, card_w, card_h)
    c.showPage()

    for module, slot in zip(modules, back_slots):
        x, y = positions[slot]
        module.draw_back_card(c, x, y)
        draw_crop_marks(c, x, y, card_w, card_h)
    c.showPage()

    c.save()
    return out_path


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for index, codes in enumerate(chunk(CARD_CODES, 4), start=1):
        for flip in ("long", "short"):
            out_path = build_sheet(codes, index, flip)
            print(out_path)


if __name__ == "__main__":
    main()
