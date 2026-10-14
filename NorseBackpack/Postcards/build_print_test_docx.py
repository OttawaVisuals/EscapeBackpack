"""
The postcard print files -- the preferred way to print the deck (decided 25 Sept 2026: the
printer handles these .docx margins better than the PDFs). Writes 11 files to output/docx/,
two cards each, covering all 22 cards in deck order. Rebuild after any card changes, and
after `python NorseBackpack/build_page_images.py` so the back images are current.

Started as a workshop test: alignment seems reliable at the TOP of the page, unreliable near
the bottom. This builds two-page .docx sheets that only ever print in the top
zone, so a sheet can be printed, flipped, and reprinted to use the rest of the
page instead of trusting the bottom.

Each file holds two postcards, rotated 90 deg to portrait (4in wide x 6in
tall since the 6 x 4 in card, 13 Oct 2026; was 3.5 x 5) and placed side by side, so the printed
block is only 6in tall instead of the 8.2in a stacked landscape pair would need -- keeping
everything closer to the top-of-page zone that aligns reliably.

Page 1 = front art of both cards. Page 2 = back text of both cards, same
left/right order. Whether "same order" survives your physical flip is
exactly what this test checks -- if a back ends up on the wrong card, swap
CARD_IDS in the failing group below and regenerate.

Images are placed as floating pictures anchored to absolute page coordinates
(relativeFrom="page"), not inside a table. A table was tried first: even with
autofit=False (fixed layout) and identical declared cell/row sizes, Word still
grew the column to fit a picture wider than its cell, which re-centered the
back page's table 1.5mm off from the front page's -- diagnosed from a printed
test on 2026-09-27. Absolute positioning sidesteps that entirely: front and
back pages compute the same trim-box coordinates from the same constants, so
there is nothing for Word to auto-resize.
"""

from pathlib import Path

from docx import Document
from docx.shared import Inches, Emu, Mm
from docx.enum.section import WD_SECTION
from docx.oxml.ns import qn
from PIL import Image, ImageDraw
import io

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

# Art is 6in x 4in landscape (5 x 3.5 until 13 Oct 2026). Rotated 90 deg it becomes 4in x 6in.
CARD_W_IN = 4.0
CARD_H_IN = 6.0
TOP_MARGIN_IN = 0.3
# Two 4in cards and the gap leave 0.15in each side of a Letter page (was 0.6in). That is just
# inside the Canon MG2900's printable area; the 3 mm back bleed past it is clipped, harmlessly.
SIDE_MARGIN_IN = 0.15
GAP_IN = 0.2  # between the two cards on a page
PAGE_W_IN = 8.5  # python-docx default template: US Letter, 8.5in x 11in
ROTATE_DEGREES = -90  # clockwise, applied to the art page
# The physical flip between art and text pages is top-to-bottom (like a calendar page),
# which inverts orientation. Confirmed on a printed test: rotating both pages the same
# way put the text upside down. The text page needs the extra 180 deg to compensate.
TEXT_ROTATE_DEGREES = ROTATE_DEGREES + 180

# Cards whose art prints upside down relative to their back. A3's message ("my head is
# spinning") is the nudge to turn the treasure tally upside down; the user asked on 2026-09-28
# for the A3 art itself to print inverted as well. Art page only; the back is unchanged.
ART_EXTRA_ROTATE = {"A3": 180}

# Was Mm(1.5), applied as a left-margin shift, to compensate a left-shifted back page.
# Retested 2026-09-27 after switching to a paper-guide slider that holds the sheet snug --
# no offset needed. Now that positions are absolute (not margin-driven), this is a direct
# X/Y nudge added to every back-page card position. Revisit if a duplex run shows drift.
# 2026-10-07: a 1.5 mm shift was tried after an R3/R4 miss and reverted; the Aud ticket printed
# centred with 0 / 0 the same morning, so the miss was a feed problem, not a fixed offset.
TEXT_SHIFT_X_IN = 0
TEXT_SHIFT_Y_IN = 0

# PC-20: 1.5mm bleed on the back (text) side only, matching the production card-back
# generators (build_postcard_L1/L2/L3/LD_pdf.py). The back is a flat colour so it can
# safely print past the trim line; the front is edge-to-edge photo art, so it stays at
# exact trim size -- no bleed applied there. Grown symmetrically so the trim box stays
# at the same absolute position.
BLEED_IN = 3 / 25.4  # was 1.5 mm; doubled 2026-10-07 so a feed slip still leaves paper colour at the edge

# 2026-10-07: page 1 is the text side, page 2 the art. The flat cream back uses less ink than the
# photo art, so printing it first leaves the sheet flatter for the second pass, which is the one
# that skewed on the Canon MG2900. Set False for the old order (art first).
TEXT_FIRST = True

# Ink-saving test mode: draw an empty outline box at each card's exact size/position
# instead of the actual image, so the alignment fix can be checked without printing art.
OUTLINE_ONLY = False
OUTLINE_WEIGHT_PX = 3

# Matches PAPER in every build_postcard_<ID>_pdf.py -- the back's flat background colour.
PAPER_RGB = (0xEF, 0xE3, 0xC4)
SOURCE_DPI = 300
EMU_PER_IN = 914400


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


def outline_box_stream(w_in, h_in):
    w_px = round(w_in * SOURCE_DPI)
    h_px = round(h_in * SOURCE_DPI)
    img = Image.new("RGBA", (w_px, h_px), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, w_px - 1, h_px - 1], outline=(0, 0, 0, 255), width=OUTLINE_WEIGHT_PX)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf


def add_floating_picture(paragraph, image_stream, width_in, height_in, x_in, y_in):
    """Insert a picture anchored to absolute page coordinates (top-left origin),
    independent of margins, table cells, or any other auto-layout."""
    run = paragraph.add_run()
    run.add_picture(image_stream, width=Inches(width_in), height=Inches(height_in))
    drawing = run._element.find(qn("w:drawing"))
    inline = drawing.find(qn("wp:inline"))

    inline.tag = qn("wp:anchor")
    inline.set("behindDoc", "0")
    inline.set("distT", "0")
    inline.set("distB", "0")
    inline.set("distL", "0")
    inline.set("distR", "0")
    inline.set("simplePos", "0")
    inline.set("locked", "0")
    inline.set("layoutInCell", "1")
    inline.set("allowOverlap", "1")
    inline.set("relativeHeight", "1")

    simple_pos = inline.makeelement(qn("wp:simplePos"), {"x": "0", "y": "0"})
    inline.insert(0, simple_pos)

    pos_h = inline.makeelement(qn("wp:positionH"), {"relativeFrom": "page"})
    off_h = pos_h.makeelement(qn("wp:posOffset"), {})
    off_h.text = str(round(x_in * EMU_PER_IN))
    pos_h.append(off_h)
    inline.insert(1, pos_h)

    pos_v = inline.makeelement(qn("wp:positionV"), {"relativeFrom": "page"})
    off_v = pos_v.makeelement(qn("wp:posOffset"), {})
    off_v.text = str(round(y_in * EMU_PER_IN))
    pos_v.append(off_v)
    inline.insert(2, pos_v)

    extent = inline.find(qn("wp:extent"))
    extent_index = list(inline).index(extent)
    wrap_none = inline.makeelement(qn("wp:wrapNone"), {})
    inline.insert(extent_index + 1, wrap_none)


def build_page(doc, card_ids, source_map, bleed_in=0, rotate_degrees=ROTATE_DEGREES,
               shift_x_in=0, shift_y_in=0, mirror=False):
    paragraph = doc.add_paragraph()
    for i, card_id in enumerate(card_ids):
        front_x = SIDE_MARGIN_IN + i * (CARD_W_IN + GAP_IN)
        # Long-edge flip mirrors left-right: a card N in from the left on the front must sit
        # N in from the RIGHT on the back. Reversing card order alone only mirrors correctly
        # when the layout is centred on the page, which it isn't (0.6in left vs 0.7in right)
        # -- that left the back 2.54mm off (printed test, 2026-09-27).
        trim_x = (PAGE_W_IN - front_x - CARD_W_IN if mirror else front_x) + shift_x_in
        trim_y = TOP_MARGIN_IN + shift_y_in
        img_x = trim_x - bleed_in
        img_y = trim_y - bleed_in
        img_w = CARD_W_IN + 2 * bleed_in
        img_h = CARD_H_IN + 2 * bleed_in
        if OUTLINE_ONLY:
            stream = outline_box_stream(img_w, img_h)
        else:
            extra = ART_EXTRA_ROTATE.get(card_id, 0) if source_map is CARD_ART else 0
            stream = rotated_image_stream(source_map[card_id], pad_in=bleed_in,
                                          rotate_degrees=rotate_degrees + extra)
        add_floating_picture(paragraph, stream, img_w, img_h, img_x, img_y)


def build_pair(card_ids, out_name):
    doc = Document()

    def art_page():
        build_page(doc, card_ids, CARD_ART)

    def text_page():
        # Confirmed 2026-09-27 (corner-mark test): the manual flip is long-edge (book-style) --
        # top stays top, left and right swap. mirror=True measures each back card from the right
        # page edge, so it lands on the same physical card as the front. The mirror relation is
        # symmetric, so the order of the two pages does not change any position.
        build_page(doc, card_ids, CARD_TEXT, bleed_in=BLEED_IN, rotate_degrees=TEXT_ROTATE_DEGREES,
                   shift_x_in=TEXT_SHIFT_X_IN, shift_y_in=TEXT_SHIFT_Y_IN, mirror=True)

    first_page, second_page = (text_page, art_page) if TEXT_FIRST else (art_page, text_page)
    first_page()
    doc.add_section(WD_SECTION.NEW_PAGE)
    second_page()

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
