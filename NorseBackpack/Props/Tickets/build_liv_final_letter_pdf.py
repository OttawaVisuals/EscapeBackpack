"""Liv's final letter (PP-043, envelope 13): handwritten on lined paper, with the family raven and the
Cryptic Bureau logo.

Text: the designer's (17 Oct 2026): the first two paragraphs verbatim, the third (the decoy-card
puzzle for AUD, Q-062) approved in chat, the closing line from PR-001. No accents (handwriting font).
The Bureau logo is the approved raster concept, background keyed out so it sits on the paper.

Run:  python NorseBackpack/Props/Tickets/build_liv_final_letter_pdf.py
"""
from pathlib import Path

from PIL import Image
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "NorseBackpack" / "Print" / "_pdf_source" / "Liv_Final_Letter_Print.pdf"
LOGO = ROOT / "Brand/CrypticBureau/LogoConcepts/CB_Logo_B_Archive_Hidden_Flaps_v1.png"
RAVEN = ROOT / "NorseBackpack/Art/Raven/Raven_Profile_Knotwork_Pencil_v2.png"
LOGO_KEYED = Path(__file__).with_name("_cb_logo_keyed.png")
pdfmetrics.registerFont(TTFont("NothingYouCouldDo", str(ROOT / "Fonts/Nothing_You_Could_Do/NothingYouCouldDo-Regular.ttf")))

W, H = 5.5 * 72, 8.5 * 72
# office-stock look (designer, 17 Oct 2026): white paper, light blue rules, pink margin line
PAPER, LINE, MARGIN, INK = HexColor("#FFFFFF"), HexColor("#A9C6E3"), HexColor("#E7A4A4"), HexColor("#283B34")

PARAS = [
    "My dear explorer,",
    "Congratulations! I'm so excited to see you this summer and continue our adventures!",
    "During my research, I think I found who could be one of our ancestors. I'll leave you that final puzzle to figure it out.",
    "Remember the cards you set aside, the places without our raven? I didn't forget about them. On one of those cards I wondered whether someone was actually our family. Whose name is it?",
    "I could use someone who notices what everyone else walks past.",
]


def key_logo():
    im = Image.open(LOGO).convert("RGB")
    bg = im.getpixel((20, 20))
    out = Image.new("RGBA", im.size)
    px, src = out.load(), im.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b = src[x, y]
            d = max(abs(r - bg[0]), abs(g - bg[1]), abs(b - bg[2]))
            a = max(0, min(255, int((d - 8) * 255 / 70)))
            px[x, y] = (101, 40, 62, a)          # the logo's burgundy, alpha from distance to paper
    out.crop((110, 320, 1150, 990)).save(LOGO_KEYED)


def wrap(text, size, width):
    lines, cur = [], ""
    for w in text.split():
        cand = f"{cur} {w}".strip()
        if pdfmetrics.stringWidth(cand, "NothingYouCouldDo", size) <= width:
            cur = cand
        else:
            lines.append(cur); cur = w
    return lines + [cur]


def main():
    key_logo()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUT), pagesize=(W, H), pageCompression=1)
    c.setTitle("Liv's final letter"); c.setAuthor("Escape Backpack")
    c.setFillColor(PAPER); c.rect(0, 0, W, H, fill=1, stroke=0)
    gap = 24
    y = H - 126
    c.setStrokeColor(LINE); c.setLineWidth(0.6)
    while y > 30:
        c.line(20, y, W - 20, y); y -= gap
    c.setStrokeColor(MARGIN); c.setLineWidth(0.8); c.line(48, 24, 48, H - 20)

    # family raven, top right; Bureau logo, bottom right
    c.drawImage(ImageReader(str(RAVEN)), W - 20 - 100, H - 16 - 100, 100, 100, mask="auto", preserveAspectRatio=True)
    c.drawImage(ImageReader(str(LOGO_KEYED)), W - 20 - 110, 24, 110, 71, mask="auto", preserveAspectRatio=True)

    size, left, width = 15, 58, W - 58 - 24
    baseline = H - 126 - gap + 5
    c.setFillColor(INK); c.setFont("NothingYouCouldDo", size)
    for p in PARAS:
        for line in wrap(p, size, width):
            c.drawString(left, baseline, line); baseline -= gap
        if p != PARAS[0]:
            pass
        baseline -= 0 if p == PARAS[0] else gap
    baseline -= 0
    c.setFont("NothingYouCouldDo", size + 1)
    c.drawString(left, baseline, "With love,"); baseline -= gap
    c.drawString(left, baseline, "Aunt Liv")
    c.showPage(); c.save(); print(OUT, "last baseline", baseline)


if __name__ == "__main__":
    main()
