"""
Word versions of the single-sided printables that had no .docx yet, so every printable
piece can be printed from output/docx/. Each source is rasterised at 300 dpi from its own
Print.pdf (never drifts from the production build) and placed as one floating picture at
its exact PDF size, centred on a Letter page. Rebuild after any of the source PDFs change.

Written: Luggage_Tags, Journal_Family_Iconography, Transition_Tickets, Hnefatafl_Board_Setup_Insert.
(Postcards, double-sided tickets and Raven's Flights card have their own PrintTest_*.docx.)
"""
import importlib.util
import io
from pathlib import Path

import pymupdf
from docx import Document
from docx.shared import Inches

ROOT = Path(__file__).resolve().parents[2]
PDF_DIR = ROOT / "output" / "pdf"
OUT_DIR = ROOT / "output" / "docx"

_spec = importlib.util.spec_from_file_location(
    "postcard_print", ROOT / "NorseBackpack" / "Postcards" / "build_print_test_docx.py")
_postcard = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_postcard)
add_floating_picture = _postcard.add_floating_picture

DPI = 300
# name -> source PDF (page 1 only)
PRINTABLES = {
    "Print_LuggageTags": "Luggage_Tag_Inserts_Print.pdf",                 # Letter portrait
    "Print_JournalFamilyIconography": "Journal_Family_Iconography_Letter_Print.pdf",
    "Print_TransitionTickets": "Transition_Tickets_Letter_Print.pdf",
    "Print_HnefataflBoardSetupInsert": "Hnefatafl_Board_Setup_Insert.pdf",  # small, centred
}


def build(name, pdf_name):
    page = pymupdf.open(PDF_DIR / pdf_name)[0]
    w_in, h_in = page.rect.width / 72, page.rect.height / 72
    pix = page.get_pixmap(matrix=pymupdf.Matrix(DPI / 72, DPI / 72), alpha=False)
    stream = io.BytesIO(pix.tobytes("png"))

    landscape = w_in > h_in and w_in > 8.6
    page_w, page_h = (11.0, 8.5) if landscape else (8.5, 11.0)
    doc = Document()
    section = doc.sections[0]
    section.page_width, section.page_height = Inches(page_w), Inches(page_h)
    for side in ("left_margin", "right_margin", "top_margin", "bottom_margin"):
        setattr(section, side, Inches(0.25))
    add_floating_picture(doc.add_paragraph(), stream, w_in, h_in,
                         (page_w - w_in) / 2, (page_h - h_in) / 2 if w_in < 8 else 0)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / f"{name}.docx"
    doc.save(str(out))
    return out


if __name__ == "__main__":
    for n, p in PRINTABLES.items():
        print(build(n, p))
