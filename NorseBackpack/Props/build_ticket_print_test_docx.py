"""
Ticket print files -- the postcard PrintTest technique (Postcards/build_print_test_docx.py)
applied to the double-sided tickets: the L'Anse museum ticket (PZ-12), the Rouen ticket
(PZ-15), the Hnefatafl museum ticket (PZ-01/PZ-07) and Aud's treasure-museum ticket (PZ-17). Writes one .docx per ticket to
output/docx/.

Same settings the postcards were confirmed with on the L1/L2 print test, 2026-09-27:
  * Each ticket is rotated 90 deg so its short side is the printed height, keeping it in
    the top zone of the page where this printer aligns reliably.
  * Pictures are floating, anchored to absolute page coordinates (no table -- Word grew a
    table column 1.5mm on the postcards).
  * The manual flip is long-edge: top stays top, left and right swap. So the back sits as far
    from the RIGHT page edge as the front sits from the LEFT, at the same height.
  * No back-page shift (the old 1.5mm shift was dropped for the postcards too).
  * 1.5mm bleed on the back only; the front stays at exact trim size. Ticket backs are not one
    flat colour (the museum back is a dark band over bare paper), so the bleed repeats each
    edge's own pixels outward instead of padding with a single colour.

Source: rasterized straight from each ticket's own Print.pdf (exact trim size) at 300dpi via
PyMuPDF, so this never drifts from the production build. Rebuild after any of
build_museum_ticket_pdf.py, build_rouen_ticket_pdf.py, Hnefatafl/build_ticket_pdf.py or
AudTicket/build_aud_ticket_pdf.py changes.
"""

import importlib.util
import io
from pathlib import Path

import pymupdf as fitz
import numpy as np
from docx import Document
from docx.enum.section import WD_SECTION
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "output" / "docx"
PDF_DIR = ROOT / "output" / "pdf"

# Reuse the postcard script's absolute-position picture helper so both stay identical.
_spec = importlib.util.spec_from_file_location(
    "postcard_print", ROOT / "NorseBackpack" / "Postcards" / "build_print_test_docx.py")
_postcard = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_postcard)
add_floating_picture = _postcard.add_floating_picture

RENDER_DPI = 300
PAGE_W_IN = 8.5  # python-docx default template: US Letter
TOP_MARGIN_IN = 0.3
SIDE_MARGIN_IN = 0.6
ROTATE_DEGREES = _postcard.ROTATE_DEGREES
TEXT_ROTATE_DEGREES = _postcard.TEXT_ROTATE_DEGREES
TEXT_SHIFT_X_IN = 0
TEXT_SHIFT_Y_IN = 0
BLEED_IN = _postcard.BLEED_IN

# w_in x h_in = the ticket as designed (portrait); page indices = front, back in its Print.pdf.
TICKETS = {
    "MuseumTicket": {"pdf": PDF_DIR / "Museum_Ticket_Print.pdf", "w_in": 2.0, "h_in": 5.5},
    "RouenTicket": {"pdf": PDF_DIR / "Rouen_Ticket_Print.pdf", "w_in": 2.0, "h_in": 3.0},
    "HnefataflTicket": {"pdf": PDF_DIR / "Hnefatafl_Ticket_Print.pdf", "w_in": 2.6, "h_in": 6.6},
    # Page 3 of Aud_Ticket_Print.pdf is the filled-in answer copy -- never printed for players.
    "AudTicket": {"pdf": PDF_DIR / "Aud_Ticket_Print.pdf", "w_in": 3.0, "h_in": 4.0},
}


def page_to_image_stream(pdf_path, page_index, rotate_degrees, bleed_in=0):
    doc = fitz.open(pdf_path)
    page = doc[page_index]
    zoom = RENDER_DPI / 72
    pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)
    img = Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB")
    if bleed_in:
        pad = round(bleed_in * RENDER_DPI)
        img = Image.fromarray(np.pad(np.asarray(img), ((pad, pad), (pad, pad), (0, 0)), mode="edge"))
    rotated = img.rotate(rotate_degrees, expand=True)
    buf = io.BytesIO()
    rotated.save(buf, format="PNG")
    buf.seek(0)
    return buf


def build_ticket(name, spec):
    # Rotated 90 deg: printed width/height swap.
    printed_w, printed_h = spec["h_in"], spec["w_in"]
    front_x, front_y = SIDE_MARGIN_IN, TOP_MARGIN_IN

    doc = Document()
    paragraph = doc.add_paragraph()
    add_floating_picture(paragraph, page_to_image_stream(spec["pdf"], 0, ROTATE_DEGREES),
                         printed_w, printed_h, front_x, front_y)

    doc.add_section(WD_SECTION.NEW_PAGE)
    paragraph = doc.add_paragraph()
    back_x = PAGE_W_IN - front_x - printed_w + TEXT_SHIFT_X_IN
    back_y = front_y + TEXT_SHIFT_Y_IN
    add_floating_picture(paragraph,
                         page_to_image_stream(spec["pdf"], 1, TEXT_ROTATE_DEGREES, bleed_in=BLEED_IN),
                         printed_w + 2 * BLEED_IN, printed_h + 2 * BLEED_IN,
                         back_x - BLEED_IN, back_y - BLEED_IN)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUT_DIR / f"PrintTest_{name}.docx"
    doc.save(str(out_path))
    return out_path


def main():
    for name, spec in TICKETS.items():
        print(build_ticket(name, spec))


if __name__ == "__main__":
    main()
