"""
Word versions of the single-sided printables that had no .docx yet, so every printable
piece can be printed from NorseBackpack/Print/. Each source is rasterised at 300 dpi from its own
Print.pdf (never drifts from the production build) and placed as one floating picture at
its exact PDF size, centred on a Letter page. Multi-page PDFs give one Letter page each. Rebuild after any of the source PDFs change.

Written: Luggage_Tags, Journal_Family_Iconography, Transition_Tickets, Hnefatafl_Board_Setup_Insert, Lock_Stickers.
(Postcards, double-sided tickets and Raven's Flights card have their own PrintTest_*.docx.)
"""
import importlib.util
import io
from pathlib import Path

import pymupdf
from docx import Document
from docx.oxml import OxmlElement
from docx.enum.section import WD_SECTION
from docx.shared import Inches

ROOT = Path(__file__).resolve().parents[2]
PDF_DIR = ROOT / "NorseBackpack" / "Print" / "_pdf_source"
OUT_DIR = ROOT / "NorseBackpack" / "Print"

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
    # "Print_TransitionTickets" retired 20 Oct 2026: itinerary receipts dropped (PP-039).
    "Print_HnefataflBoardSetupInsert": "Hnefatafl_Board_Setup_Insert.pdf",  # small, centred
    "Print_LockStickers": "Lock_Stickers_Print.pdf",                       # Letter portrait
    "Print_PlaneTicket": "Plane_Ticket_Print.pdf",                         # small, centred
    "Print_LivFinalLetter": "Liv_Final_Letter_Print.pdf",                  # small, centred
    "Print_LivNotesCard": "Liv_Notes_Card_Print.pdf",                      # two-sided 4 x 6; duplex long edge
    "Print_LivRuler": "Liv_Ruler_Print.pdf",                               # Letter portrait
    "Print_CombAndRuler": "Comb_And_Ruler_Print.pdf",                     # Letter portrait, heavy paper (21 Oct 2026)
    "Print_RepackingLetter": "Raven_Inheritance_Repacking_Letter.pdf",    # Letter portrait
    "Print_HopTickets": "Hop_Tickets_Print.pdf",                           # 4 Letter pages, one per journey
}


def build(name, pdf_name):
    """One Letter page per PDF page (every printable here is single-sided or a set of single pages)."""
    pdf = pymupdf.open(PDF_DIR / pdf_name)
    doc = Document()
    for i, page in enumerate(pdf):
        w_in, h_in = page.rect.width / 72, page.rect.height / 72
        pix = page.get_pixmap(matrix=pymupdf.Matrix(DPI / 72, DPI / 72), alpha=False)
        stream = io.BytesIO(pix.tobytes("png"))
        landscape = w_in > h_in and w_in > 8.6
        page_w, page_h = (11.0, 8.5) if landscape else (8.5, 11.0)
        if i:
            doc.add_section(WD_SECTION.NEW_PAGE)
        section = doc.sections[-1]
        section.page_width, section.page_height = Inches(page_w), Inches(page_h)
        for side in ("left_margin", "right_margin", "top_margin", "bottom_margin"):
            setattr(section, side, Inches(0.25))
        top = .5 if name == "Print_LivNotesCard" else ((page_h - h_in) / 2 if w_in < 8 else 0)
        paragraph = doc.add_paragraph()
        add_floating_picture(paragraph, stream, w_in, h_in,
                             (page_w - w_in) / 2, top)
        if name == "Print_LivNotesCard" and i == 0:
            props = paragraph._p.xpath('.//pic:spPr')[0]
            line = OxmlElement('a:ln'); line.set('w', '6350')
            fill = OxmlElement('a:solidFill')
            colour = OxmlElement('a:srgbClr'); colour.set('val', '777777')
            fill.append(colour); line.append(fill)
            dash = OxmlElement('a:prstDash'); dash.set('val', 'dash')
            line.append(dash); props.append(line)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / f"{name}.docx"
    doc.save(str(out))
    return out


if __name__ == "__main__":
    for n, p in PRINTABLES.items():
        print(build(n, p))
