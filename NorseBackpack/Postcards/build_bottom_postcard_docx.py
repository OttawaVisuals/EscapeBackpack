"""(Revised 21 Oct 2026: the designer feeds the sheet turned 180 degrees, so the free strip is printed first, at the
top of the page; both images are rotated 180 degrees so they come out upright on the sheet.)

One landscape postcard for the free strip at the bottom of an already-printed pair sheet (21 Oct 2026).

The pair sheets (build_print_test_docx.py) use only the top 6.3 in of the Letter page (two 4 x 6 in cards,
portrait). The strip below is 4.7 in tall, so one more card fits LANDSCAPE (6 x 4 in), centred. Written for
the five cards the designer has no paper left for: H2 to H6. One file per card, two pages: page 1 = back
(text) side, page 2 = front (art) side, the same order as the pair sheets, so feed the sheet the same way as
before for each pass. Landscape art and text both use rotation 0: the long-edge flip keeps the top at the top
and the card is centred, so the back lands on the same card.
"""
import io
from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION
from PIL import Image

import build_print_test_docx as P

CARDS = ["L2_Battle_Harbour", "HD_Constantinople", "H2_Staraya_Ladoga", "H3_Kyiv", "H4_Hedeby", "H5_Sicily", "H6_Patara"]
W_IN, H_IN = 6.0, 4.0
TOP_IN = P.TOP_MARGIN_IN   # 0.3 in: the card prints at the TOP of the page (alignment is reliable there)


def stream(path):
    buf = io.BytesIO()
    Image.open(path).rotate(180).save(buf, format="PNG")
    buf.seek(0)
    return buf


def build(card):
    cid = card.split("_")[0]
    doc = Document()
    for i, src in enumerate((P.CARD_TEXT[cid], P.CARD_ART[cid])):   # text first, like the pair sheets
        if i:
            doc.add_section(WD_SECTION.NEW_PAGE)
        P.add_floating_picture(doc.add_paragraph(), stream(src), W_IN, H_IN, (P.PAGE_W_IN - W_IN) / 2, TOP_IN)
    out = P.OUT_DIR / f"PrintBottom_{cid}.docx"
    doc.save(str(out))
    return out


if __name__ == "__main__":
    for c in CARDS:
        print(build(c))
