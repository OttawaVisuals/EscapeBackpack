"""Re-render every image Norse_Brainstorm.html shows that is a picture of a built PDF.

Run this after rebuilding any postcard, prop or map PDF, so the project page never shows an
older version than the one that prints. Written 25 Sept 2026, after an audit found the prop
renders three to four days behind their PDFs (they had been one-off snapshots with no script).

    python NorseBackpack/build_page_images.py

It writes:
  * Postcards/Postcard_<ID>_Back.png -- page 2 of each NorseBackpack/Print/_pdf_source/Postcard_<ID>_Print.pdf at
    300 dpi (1800 x 1200 since the 6 x 4 in card). Fronts are not rendered: the PDF places the Front.png unchanged.
  * Props/_Renders/<name>.png        -- one page of a prop or map PDF, per RENDERS below.

A missing source PDF or page stops the run rather than leaving a silently stale image.
"""
import re
import sys
from pathlib import Path

import pymupdf

HERE = Path(__file__).resolve().parent
PDF = HERE.parent / "NorseBackpack" / "Print" / "_pdf_source"
POSTCARDS = HERE / "Postcards"
RENDERS = HERE / "Props" / "_Renders"

# render name -> (source PDF in NorseBackpack/Print/_pdf_source, page index, zoom; 1.0 = 72 dpi)
RENDER_MAP = {
    "Aud_Ticket_Front": ("Aud_Ticket_Print", 0, 3.0),
    "Aud_Ticket_Back": ("Aud_Ticket_Print", 1, 3.0),
    "Aud_Ticket_p3": ("Aud_Ticket_Print", 2, 3.0),          # answer copy
    "Hnefatafl_Board_Setup_Insert_Insert": ("Hnefatafl_Board_Setup_Insert", 0, 3.0),
    "Hnefatafl_Ticket_Front": ("Hnefatafl_Ticket_Print", 0, 3.0),
    "Hnefatafl_Ticket_Back": ("Hnefatafl_Ticket_Print", 1, 3.0),
    "Journal_Family_Iconography_Page": ("Journal_Family_Iconography_Print", 0, 2.5),
    "Luggage_Tag_Inserts_Sheet": ("Luggage_Tag_Inserts_Print", 0, 2.5),
    "Lock_Stickers_Sheet": ("Lock_Stickers_Print", 0, 2.5),
    "Museum_Ticket_Front": ("Museum_Ticket_Print", 0, 3.0),
    "Museum_Ticket_Back": ("Museum_Ticket_Print", 1, 3.0),
    "Trail_Map_1_Leif_Print": ("Trail_Map_1_Leif_Print", 0, 2.0),
    "Trail_Map_2_Rollo_Print": ("Trail_Map_2_Rollo_Print", 0, 2.0),
    "Trail_Map_3_Aud_Print": ("Trail_Map_3_Aud_Print", 0, 2.0),
    "Trail_Map_4_Harald_Front": ("Trail_Map_4_Harald_Print", 0, 2.0),
    "Trail_Map_4_Harald_Back": ("Trail_Map_4_Harald_Print", 1, 2.0),
    "Transition_Tickets_Ticket1": ("Transition_Tickets_Print", 0, 3.0),
    "Transition_Tickets_Ticket2": ("Transition_Tickets_Print", 1, 3.0),
    "Transition_Tickets_Ticket3": ("Transition_Tickets_Print", 2, 3.0),
    "Hop_Tickets_Leif": ("Hop_Tickets_Print", 0, 2.5),
    "Hop_Tickets_Rollo": ("Hop_Tickets_Print", 1, 2.5),
    "Hop_Tickets_Aud": ("Hop_Tickets_Print", 2, 2.5),
    "Hop_Tickets_Harald": ("Hop_Tickets_Print", 3, 2.5),
    "Plane_Ticket": ("Plane_Ticket_Print", 0, 3.0),
    "Liv_Final_Letter": ("Liv_Final_Letter_Print", 0, 2.5),
}

# Single-card print PDFs only: not the _Letter_Print sheets, not the Postcard_Sheet_ impositions.
CARD_PDF = re.compile(r"^Postcard_([LRAH][1-6D])_(.+?)(?<!_Letter)_Print\.pdf$")


def render(pdf_path, page_index, zoom, out_path):
    with pymupdf.open(pdf_path) as doc:
        if page_index >= len(doc):
            raise SystemExit("%s has no page %d" % (pdf_path.name, page_index + 1))
        pix = doc[page_index].get_pixmap(matrix=pymupdf.Matrix(zoom, zoom))
    pix.save(out_path)
    return pix.width, pix.height


def render_back(pdf_path, out_path):
    """Back of a postcard. The print PDF has no beige fill (20 Oct 2026, designer), so:
    *_Back_Print.png keeps the page transparent-on-white for the Word print sheets, and
    *_Back.png (website / project page) is the same render laid on the old beige paper."""
    from PIL import Image
    with pymupdf.open(pdf_path) as doc:
        pix = doc[1].get_pixmap(matrix=pymupdf.Matrix(300 / 72, 300 / 72), alpha=True)
    card = Image.frombytes("RGBA", (pix.width, pix.height), pix.samples)
    white = Image.new("RGBA", card.size, (255, 255, 255, 255))
    white.alpha_composite(card)
    white.convert("RGB").save(out_path.with_name(out_path.name.replace("_Back.png", "_Back_Print.png")))
    beige = Image.new("RGBA", card.size, (0xEF, 0xE3, 0xC4, 255))
    beige.alpha_composite(card)
    beige.convert("RGB").save(out_path)


def main():
    problems = []
    cards = 0
    for pdf_path in sorted(PDF.glob("Postcard_*_Print.pdf")):
        match = CARD_PDF.match(pdf_path.name)
        if not match:                               # Letter sheets, imposition sheets
            continue
        out = POSTCARDS / ("Postcard_%s_%s_Back.png" % match.groups())
        render_back(pdf_path, out)
        cards += 1
    if cards != 22:
        problems.append("expected 22 postcard PDFs, found %d" % cards)

    for name, (pdf, page, zoom) in RENDER_MAP.items():
        pdf_path = PDF / (pdf + ".pdf")
        if not pdf_path.exists():
            problems.append("missing %s for %s" % (pdf_path.name, name))
            continue
        w, h = render(pdf_path, page, zoom, RENDERS / (name + ".png"))
        print("%-38s %4d x %d" % (name, w, h))

    print("postcard backs: %d" % cards)
    if problems:
        sys.exit("\n".join(problems))


if __name__ == "__main__":
    main()
