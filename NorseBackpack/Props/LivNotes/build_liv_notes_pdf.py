# SUPERSEDED FOR PRINT 17 Oct 2026 (designer): the live notes card PDF now comes from the readability redesign
# (Props/ReadabilityDrafts/adopt_to_live.py). Running this builder overwrites it with the old layout. Kept for its text and history.
"""Liv's notes card (PP-048): a 4 x 6 in portrait card that comes with postcard L1.

Mock-up, 15 Oct 2026. Text is the approved draft in records/props/PP-048. Same paper, border and
fonts as the postcards (build_postcard_R1_pdf.py). Writes the print PDF and a PNG preview.
"""
from pathlib import Path

import fitz  # PyMuPDF, preview only
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "NorseBackpack" / "Print" / "_pdf_source" / "Liv_Notes_Card_Print.pdf"
PREVIEW = Path(__file__).with_name("Liv_Notes_Card_Preview.png")
FONT_DIR = ROOT / "Fonts"

W, H = 4 * 72, 6 * 72
BLEED = 1.5 / 25.4 * 72
PAPER = HexColor("#EFE3C4")
TEAL = HexColor("#2F7775")
RULE = HexColor("#A99A7B")
INK = HexColor("#283B34")
FUNFACT = HexColor("#B56A2A")

pdfmetrics.registerFont(TTFont("CinzelExtraBold", str(FONT_DIR / "Cinzel" / "static" / "Cinzel-ExtraBold.ttf")))
pdfmetrics.registerFont(TTFont("NothingYouCouldDo", str(FONT_DIR / "Nothing_You_Could_Do" / "NothingYouCouldDo-Regular.ttf")))
HAND = "NothingYouCouldDo"

INTRO = "I've discovered a lot of words I never knew before. They might be useful to you too, so keep this card handy all the way through!"
WHO = [
    ("Leif Erikson", "Norse explorer who sailed to North America"),
    ("Aud the Deep-Minded", "Viking settler who sailed to Iceland"),
    ("Rollo", "Viking leader, first ruler of Normandy"),
    ("Harald Hardrada", "Norse king who served the emperor in Constantinople"),
]
WORDS = [
    ("Chainmail", "flexible armour made from interlocking iron rings"),
    ("Crossbow bolt", "short arrow fired from a crossbow"),
    ("Ford", "a shallow place where you can wade across a river"),
    ("Hoard", "a hidden stash of treasure"),
    ("Longship", "a long, narrow Viking ship with oars and a sail"),
    ("Mead", "a drink of the feasting hall, made with honey"),
    ("Rune", "a letter of the old Norse alphabet, made of straight lines for carving"),
    ("Runestone", "a carved stone with a message"),
    # 15 Oct 2026 (designer): saga added; Liv's postcards quote "the sagas" from L2 on.
    ("Saga", "an old Icelandic story about heroes and families, written down in the Middle Ages"),
    ("Spear", "a long pole with a pointed head, for thrusting or throwing"),
    ("Tapestry", "a large woven cloth that tells a story in pictures"),
]


def wrap(text, font, size, width):
    lines, cur = [], ""
    for word in text.split():
        cand = f"{cur} {word}".strip()
        if pdfmetrics.stringWidth(cand, font, size) <= width:
            cur = cand
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def entry(c, y, term, text, left, width, size=9.2, leading=10.4):
    """Teal term, then the definition in Liv's hand on the same line; wraps under the term."""
    term_font, term_size = "CinzelExtraBold", 6.8
    tw = pdfmetrics.stringWidth(term.upper(), term_font, term_size) + 5
    c.setFillColor(TEAL)
    c.setFont(term_font, term_size)
    c.drawString(left, y, term.upper())
    first = wrap(text, HAND, size, width - tw)
    # words that did not fit beside the term flow onto full-width lines
    placed = first[0] if first else ""
    rest = text[len(placed):].strip()
    c.setFillColor(INK)
    c.setFont(HAND, size)
    c.drawString(left + tw, y, placed)
    for line in (wrap(rest, HAND, size, width - 6) if rest else []):
        y -= leading
        c.drawString(left + 6, y, line)
    return y - leading - 1.6


def heading(c, y, text, left, right):
    c.setFillColor(FUNFACT)
    c.setFont("Helvetica-Bold", 7)
    c.drawString(left, y, text.upper())
    c.setStrokeColor(RULE)
    c.setLineWidth(0.5)
    c.line(left + pdfmetrics.stringWidth(text.upper(), "Helvetica-Bold", 7) + 5, y + 2.4, right, y + 2.4)
    return y - 12


def build():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUT), pagesize=(W, H))
    c.setTitle("Liv's notes card (mock-up)")
    c.setFillColor(PAPER)
    c.rect(-BLEED, -BLEED, W + 2 * BLEED, H + 2 * BLEED, fill=1, stroke=0)
    c.setStrokeColor(RULE)
    c.setLineWidth(0.7)
    c.rect(12, 12, W - 24, H - 24, fill=0, stroke=1)

    left, right = 22, W - 22
    width = right - left - 8

    c.setFillColor(TEAL)
    c.setFont("CinzelExtraBold", 13)
    c.drawCentredString(W / 2, H - 34, "LIV'S NOTES")
    c.setFillColor(INK)
    c.setFont(HAND, 9.6)
    y = H - 50
    for line in wrap(INTRO, HAND, 9.6, right - left):
        c.drawCentredString(W / 2, y, line)
        y -= 11

    y -= 5
    y = heading(c, y, "Who's who", left, right)
    for term, text in WHO:
        y = entry(c, y, term, text, left, width)

    y -= 2
    y = heading(c, y, "Words", left, right)
    for term, text in WORDS:
        y = entry(c, y, term, text, left, width)

    c.showPage()
    c.save()
    print(f"bottom of text at y={y:.1f} pt (border at 12 pt)")
    return y


def preview():
    doc = fitz.open(str(OUT))
    doc[0].get_pixmap(dpi=200).save(str(PREVIEW))
    print(PREVIEW)


if __name__ == "__main__":
    build()
    preview()
