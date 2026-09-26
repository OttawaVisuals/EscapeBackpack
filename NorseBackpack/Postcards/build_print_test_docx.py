"""
The postcard print files -- the preferred way to print the deck (decided 25 Sept 2026: the
printer handles these .docx margins better than the PDFs). Writes 11 files to output/docx/,
two cards each, covering all 22 cards in deck order. Rebuild after any card changes, and
after `python NorseBackpack/build_page_images.py` so the back images are current.

Started as a workshop test: alignment seems reliable at the TOP of the page, unreliable near
the bottom. This builds two-page .docx sheets that only ever print in the top
zone, so a sheet can be printed, flipped, and reprinted to use the rest of the
page instead of trusting the bottom.

Each file holds two postcards, rotated 90 deg to portrait (3.5in wide x 5in
tall) and placed side by side, so the printed block is only 5in tall instead
of the 7in a stacked landscape pair would need -- keeping everything closer
to the top-of-page zone that aligns reliably.

Page 1 = front art of both cards. Page 2 = back text of both cards, same
left/right order. Whether "same order" survives your physical flip is
exactly what this test checks -- if a back ends up on the wrong card, swap
CARD_IDS in the failing group below and regenerate.
"""

import io
from pathlib import Path

from docx import Document
from docx.shared import Inches, Mm, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ROW_HEIGHT_RULE
from docx.enum.section import WD_SECTION
from docx.oxml.ns import qn
from PIL import Image

ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT.parents[1] / "output" / "docx"      # repo-root output/, with the PDFs

# Deck order (PC-17): trail by trail, decoy last. Paired in this order, so a pair can span two
# trails (RD+A1, AD+H1); that only affects which sheet a card is on, not the card.
DECK = ["L1_LAnse", "L2_Battle_Harbour", "L3_Baffin_Island", "LD_Brattahlid",
        "R1_Chalus", "R2_Rouen", "R3_Bayeux", "R4_Winchester", "R5_Battle",
        "R6_Roumare_Forest", "RD_Walcheren",
        "A1_Dogurdarnes", "A2_Hvammur", "A3_Esjuberg", "AD_Bjarnarhofn",
        "H1_Oslo", "H2_Staraya_Ladoga", "H3_Kyiv", "H4_Hedeby", "H5_Sicily", "H6_Patara",
        "HD_Constantinople"]

CARD_ART = {card.split("_")[0]: ROOT / f"Postcard_{card}_Front.png" for card in DECK}
CARD_TEXT = {card.split("_")[0]: ROOT / f"Postcard_{card}_Back.png" for card in DECK}

# Art is 5in x 3.5in landscape. Rotated 90 deg it becomes 3.5in x 5in portrait.
CARD_W_IN = 3.5
CARD_H_IN = 5.0
TOP_MARGIN_IN = 0.3
SIDE_MARGIN_IN = 0.6
ROTATE_DEGREES = -90  # clockwise, applied to the art page
# The physical flip between art and text pages is top-to-bottom (like a calendar page),
# which inverts orientation. Confirmed on a printed test: rotating both pages the same
# way put the text upside down. The text page needs the extra 180 deg to compensate.
TEXT_ROTATE_DEGREES = ROTATE_DEGREES + 180

# Measured on the printed test: the text (back) page lands 1.5mm left of the art page.
# Shifting its margins right by that much compensates. Art page is untouched.
TEXT_SHIFT = Mm(1.5)

# PC-20: 2mm bleed on the back (text) side only, matching the production card-back
# generators (build_postcard_L1/L2/L3/LD_pdf.py). The back is a flat colour so it can
# safely print past the trim line; the front is edge-to-edge photo art, so it stays at
# exact trim size -- no bleed applied there. Grown symmetrically so the box stays
# centred on the same trim position.
BLEED_IN = 2 / 25.4

# Ink-saving test mode: draw an empty outline box at each card's exact size/position
# instead of the actual image, so the alignment fix can be checked without printing art.
OUTLINE_ONLY = False
OUTLINE_WEIGHT_PT = 0.75  # hairline


# Matches PAPER in every build_postcard_<ID>_pdf.py -- the back's flat background colour.
PAPER_RGB = (0xEF, 0xE3, 0xC4)
SOURCE_DPI = 300


def rotated_image_stream(image_path, pad_in=0, rotate_degrees=ROTATE_DEGREES):
    if not image_path.exists():
        raise FileNotFoundError(image_path)
    img = Image.open(image_path)
    if pad_in:
        pad_px = round(pad_in * SOURCE_DPI)
        padded = Image.new("RGB", (img.width + 2 * pad_px, img.height + 2 * pad_px), PAPER_RGB)
        padded.paste(img, (pad_px, pad_px))
        img = padded
    rotated = img.rotate(rotate_degrees, expand=True)
    buf = io.BytesIO()
    rotated.save(buf, format="PNG")
    buf.seek(0)
    return buf


def remove_table_borders(table):
    tbl_pr = table._tbl.tblPr
    borders = tbl_pr.makeelement(qn("w:tblBorders"), {})
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = borders.makeelement(qn(f"w:{edge}"), {qn("w:val"): "none"})
        borders.append(el)
    tbl_pr.append(borders)


def add_cell_outline(cell):
    tc_pr = cell._tc.get_or_add_tcPr()
    borders = tc_pr.makeelement(qn("w:tcBorders"), {})
    sz = str(int(OUTLINE_WEIGHT_PT * 8))  # eighths of a point
    for edge in ("top", "left", "bottom", "right"):
        el = borders.makeelement(
            qn(f"w:{edge}"), {qn("w:val"): "single", qn("w:sz"): sz, qn("w:color"): "000000"}
        )
        borders.append(el)
    tc_pr.append(borders)


def add_card_cell(cell, card_id, image_path, bleed_in=0, rotate_degrees=ROTATE_DEGREES):
    cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    if OUTLINE_ONLY:
        add_cell_outline(cell)
        return
    run = cell.paragraphs[0].add_run()
    run.add_picture(
        rotated_image_stream(image_path, pad_in=bleed_in, rotate_degrees=rotate_degrees),
        width=Inches(CARD_W_IN + 2 * bleed_in),
        height=Inches(CARD_H_IN + 2 * bleed_in),
    )


def build_page(doc, card_ids, source_map, bleed_in=0, rotate_degrees=ROTATE_DEGREES):
    table = doc.add_table(rows=1, cols=len(card_ids))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    remove_table_borders(table)
    row = table.rows[0]
    row.height_rule = WD_ROW_HEIGHT_RULE.EXACTLY
    row.height = Inches(CARD_H_IN + 2 * bleed_in)
    gap_in = 0 if OUTLINE_ONLY else 0.2
    cell_width = Inches(CARD_W_IN + 2 * bleed_in + gap_in)
    for cell, card_id in zip(row.cells, card_ids):
        cell.width = cell_width
        add_card_cell(cell, card_id, source_map[card_id], bleed_in=bleed_in, rotate_degrees=rotate_degrees)


def set_margins(section, horizontal_shift=0):
    section.top_margin = Inches(TOP_MARGIN_IN)
    section.left_margin = Inches(SIDE_MARGIN_IN) + horizontal_shift
    section.right_margin = Inches(SIDE_MARGIN_IN) - horizontal_shift
    section.bottom_margin = Inches(0.3)


def build_pair(card_ids, out_name):
    doc = Document()
    set_margins(doc.sections[0])
    build_page(doc, card_ids, CARD_ART)

    text_section = doc.add_section(WD_SECTION.NEW_PAGE)
    set_margins(text_section, horizontal_shift=TEXT_SHIFT)
    build_page(doc, card_ids, CARD_TEXT, bleed_in=BLEED_IN, rotate_degrees=TEXT_ROTATE_DEGREES)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUT_DIR / out_name
    doc.save(str(out_path))
    return out_path


def main():
    ids = [card.split("_")[0] for card in DECK]
    for first, second in zip(ids[0::2], ids[1::2]):
        print(build_pair([first, second], f"PrintTest_{first}_{second}.docx"))


if __name__ == "__main__":
    main()
