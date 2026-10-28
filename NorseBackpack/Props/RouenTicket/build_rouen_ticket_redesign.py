"""Review draft: roomier Rouen museum ticket, 3.5 x 5.5 inches.

Run from any directory. Reads the live ticket's word/tag data and castle artwork;
does not replace live PDFs, web copies or print-test documents.
"""
from pathlib import Path
import importlib.util

from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("rouen_live", HERE / "build_rouen_ticket_pdf.py")
live = importlib.util.module_from_spec(spec)
spec.loader.exec_module(live)

OUT = live.ROOT / "NorseBackpack/Print/_pdf_source/Rouen_Redesign_Draft"
W, H = 252, 396
INK = live.INK
RUST = HexColor("#985326")
PAPER = HexColor("#F5EFDF")
PALE = HexColor("#E7E6D9")
RULE = HexColor("#B2B5A5")
pdfmetrics.registerFont(TTFont("RouenTag", str(live.FONT_DIR / "IBM_Plex_Mono/IBMPlexMono-SemiBold.ttf")))


def text(c, x, y, value, font="Helvetica", size=12, color=INK, align="left"):
    c.setFillColor(color)
    c.setFont(font, size)
    {"left": c.drawString, "center": c.drawCentredString, "right": c.drawRightString}[align](x, y, value)


def rule(c, x1, x2, y, color=RULE, width=.5):
    c.setStrokeColor(color)
    c.setLineWidth(width)
    c.line(x1, y, x2, y)


def base(c):
    c.setFillColor(PAPER)
    c.rect(0, 0, W, H, stroke=0, fill=1)


def front(c):
    base(c)
    c.setStrokeColor(INK)
    c.setLineWidth(.75)
    c.rect(9, 9, W-18, H-18, fill=0, stroke=1)
    text(c, W/2, 367, "THE DUCAL MUSEUM", "Helvetica-Bold", 9, align="center")
    rule(c, 96, 156, 353, RUST, 2)
    text(c, W/2, 326, "MUSÉE DUCAL", "CinzelExtraBold", 22, align="center")
    text(c, W/2, 298, "DE ROUEN", "CinzelBold", 23, align="center")

    # Architectural niche behind the existing castle engraving. Vector decoration,
    # not a new map clue or a new historical illustration.
    p = c.beginPath()
    p.moveTo(27, 130)
    p.lineTo(27, 208)
    p.curveTo(27, 296, 225, 296, 225, 208)
    p.lineTo(225, 130)
    p.close()
    c.setFillColor(PALE)
    c.drawPath(p, fill=1, stroke=0)
    castle = live.load_castle_ink()
    iw, ih = castle.size
    scale = min(194/iw, 137/ih)
    dw, dh = iw*scale, ih*scale
    c.drawImage(ImageReader(castle), (W-dw)/2, 139+(137-dh)/2, dw, dh, mask="auto")
    text(c, W/2, 111, "ROUEN  /  NORMANDIE", "Helvetica-Bold", 9.5, align="center")

    c.setDash(2, 3)
    rule(c, 18, W-18, 93, RULE, .8)
    c.setDash()
    c.setFillColor(INK)
    c.rect(10, 10, W-20, 71, fill=1, stroke=0)
    text(c, W/2, 59, "ENTRÉE GÉNÉRALE", "CinzelBold", 13, PAPER, "center")
    text(c, W/2, 41, "GENERAL ADMISSION", "Helvetica-Bold", 10, PAPER, "center")
    text(c, W/2, 24, "Galerie des mots  /  Word Gallery", "Helvetica", 9, PAPER, "center")


def badge(c, x, y, value):
    c.setFillColor(INK)
    c.roundRect(x, y-3, 20, 16, 1.5, fill=1, stroke=0)
    text(c, x+10, y+.5, str(value), "RouenTag", 11.5, PAPER, "center")


def back(c):
    base(c)
    # All required reading is 10.5 pt or larger. No decorative dates or serial codes.
    text(c, 22, 371, "MUSÉE DUCAL DE ROUEN", "Helvetica-Bold", 9)
    rule(c, 22, W-22, 360, RUST, 2)
    text(c, 22, 332, "WORD GALLERY", "CinzelExtraBold", 20)
    text(c, 22, 314, "Peasant speech, Norman French", size=10.5)
    text(c, 22, 291, "Match each old word to its new one.", size=11)

    text(c, 22, 267, "SAXON", "Helvetica-Bold", 10, RUST)
    text(c, W-22, 267, "NORMAN", "Helvetica-Bold", 10, RUST, "right")
    rule(c, 22, 113, 259)
    rule(c, 139, W-22, 259)

    for i, ((word, num), (partner, letter)) in enumerate(zip(live.SAXON, live.NORMAN)):
        y = 237 - i*19
        badge(c, 22, y, num)
        text(c, 49, y, word, size=12)
        # Both word columns are left aligned; tags sit on the outer edges.
        text(c, 139, y, partner, size=12)
        badge(c, 210, y, letter)
        assert 49 + pdfmetrics.stringWidth(word, "Helvetica", 12) <= 113
        assert 139 + pdfmetrics.stringWidth(partner, "Helvetica", 12) <= 205

    rule(c, 22, W-22, 32)
    text(c, W/2, 17, "THE DUCAL MUSEUM  /  ROUEN", "Helvetica", 8.5, align="center")


def crop_marks(c, x, y):
    c.setStrokeColor(INK)
    c.setLineWidth(.4)
    for px in (x, x+W):
        c.line(px, y-4, px, y-12)
        c.line(px, y+H+4, px, y+H+12)
    for py in (y, y+H):
        c.line(x-4, py, x-12, py)
        c.line(x+W+4, py, x+W+12, py)


def build(filename, sheet=False):
    page = (612, 792) if sheet else (W, H)
    c = canvas.Canvas(str(OUT / filename), pagesize=page, pageCompression=1)
    c.setTitle("Rouen museum ticket - redesign draft" + (" - Letter print sheet" if sheet else ""))
    c.setAuthor("Escape Backpack")
    x, y = (page[0]-W)/2, (page[1]-H)/2
    for draw, side in ((front, "FRONT"), (back, "BACK")):
        c.saveState()
        c.translate(x, y)
        draw(c)
        c.restoreState()
        if sheet:
            crop_marks(c, x, y)
            text(c, 306, 738, "ROUEN MUSEUM TICKET", "Helvetica-Bold", 12, align="center")
            text(c, 306, 718, "Redesign draft - " + side, size=10, align="center")
            text(c, 306, 114, "Finished size: 3.5 x 5.5 in. Print at 100% / Actual size.", size=10, align="center")
            text(c, 306, 98, "Duplex: flip on the long edge. Check alignment before cutting.", size=10, align="center")
        c.showPage()
    c.save()


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    # Preserve every word, tag and ordering choice from the current live ticket.
    assert len(live.SAXON) == len(live.NORMAN) == 11
    saxon, norman = dict(live.SAXON), dict(live.NORMAN)
    assert [norman[n]+str(saxon[s]) for s,n in
            [("fight", "combat"), ("folk", "people"), ("hen", "poultry"), ("inn", "tavern")]] == ["I6", "F7", "A3", "B9"]
    build("Rouen_Ticket_Redesign.pdf")
    build("Rouen_Ticket_Redesign_Letter.pdf", sheet=True)
    for p in OUT.glob("*.pdf"):
        print(p)


if __name__ == "__main__":
    main()
