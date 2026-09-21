"""The "Family iconography" journal page -- the keystone prop of the endgame (PZ-18).

One sheet, two halves, and they must not refer to each other:

  TOP     the symbol (3 elements) and the crest (6 elements), unannotated.
          This is the decoy filter: a card carrying none of the nine is not one
          of Liv's trail stops.

  BOTTOM  "Travel highlights" -- journey entries with a memorable detail and NO
          reference to the elements at all. An earlier draft tied the two
          together ("thought of the horn on the train from Rouen to Bayeux"),
          which implies the horn belongs to one of those stops and corrupts the
          filter.

Decoupling them buys something better: the highlights are unusable until the
filter above them has been applied, because one entry names a decoy stop. A team
reading the list cold reconstructs a route through a place that is not hers. The
page teaches its own use, top to bottom.

Two rules for anyone editing the entries
----------------------------------------
1. A journey entry means the two stops are CONSECUTIVE, not merely in that
   order. Naming two stops constrains them whether or not that was the intent,
   so vet any new or "texture" entry against Tools/final_riddle_clues.py first.
2. Entries are grouped by transport and deliberately NOT in date order -- the
   list must not give away the chronology through its own sequence.

Run:  python NorseBackpack/Props/Journal/build_journal_page_pdf.py
"""
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import LETTER, portrait
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[3]
ART = ROOT / "NorseBackpack" / "Art" / "FinalPuzzle"
SYMBOL = ART / "Family_Symbol_Three_Field_v2.png"
CREST = ART / "Family_Crest_Six_Field_v2.png"
FONT_DIR = ROOT / "Fonts"
OUT = ROOT / "output" / "pdf" / "Journal_Family_Iconography_Print.pdf"
OUT_LETTER = ROOT / "output" / "pdf" / "Journal_Family_Iconography_Letter_Print.pdf"

PAGE = portrait((148 / 25.4 * 72, 210 / 25.4 * 72))          # A5, prints 2-up on Letter
W, H = PAGE

PAPER = HexColor("#EFE3C4")
INK = HexColor("#283B34")
RULE = HexColor("#A99A7B")
ACCENT = HexColor("#B56A2A")
MUTED = HexColor("#5E6B60")

pdfmetrics.registerFont(TTFont("Hand", str(FONT_DIR / "Nothing_You_Could_Do" / "NothingYouCouldDo-Regular.ttf")))

MARGIN = 22

# "bearded axe", not "axe": Rollo's and Harald's decoy mark is a DOUBLE-bladed
# axe and the crest carries a single-bladed one. The drawings show that plainly,
# but a name list reading just "axe" would let a team match the decoy by name and
# never look -- unfair rather than difficult. Same for "round shield", "drinking
# horn".
# Element names, so a team can tell a close call apart -- the round shield and
# the sun-wheel were confusable enough that the shield was redrawn (PR-22).
# Naming the elements is safe; naming which CARD carries which would not be.
SYMBOL_NAMES = "raven  ~  longship  ~  sun-wheel"
CREST_NAMES = "bearded axe  ~  round shield  ~  wolf\nanchor  ~  drinking horn  ~  valknut"

# Grouped by transport, deliberately NOT in date order.
HIGHLIGHTS = [
    ("By train", [
        ("Staraya Ladoga – Kyiv",
         "Two days on a train, most of it running alongside the rivers they "
         "would have rowed. Felt like cheating. Slept through the best of it, "
         "naturally."),
        ("Walcheren – Châlus",
         "The long one. Three changes, one missed connection, and a man in the "
         "second carriage who shared his sandwiches after I gave up waiting for "
         "the buffet car."),
        ("from Rouen",
         "Heading west, a short hop, for a museum I’d been looking forward "
         "to for months."),
    ]),
    ("By sea", [
        ("English Channel ferry",
         "Landed in Winchester after a rocky night, but excited to finally see "
         "the battlefield itself, after all those hours in front of the "
         "tapestry."),
    ]),
]


def wrap(text, font, size, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        cand = f"{cur} {w}".strip()
        if pdfmetrics.stringWidth(cand, font, size) <= width:
            cur = cand
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_page(c, ox=0, oy=0):
    c.saveState()
    c.translate(ox, oy)

    c.setFillColor(PAPER)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    left, right = MARGIN, W - MARGIN
    inner = right - left

    # ---- title ------------------------------------------------------------
    c.setFillColor(INK)
    c.setFont("Hand", 23)
    c.drawString(left, H - 48, "Family iconography")
    c.setStrokeColor(RULE)
    c.setLineWidth(0.9)
    c.line(left, H - 58, right, H - 58)

    c.setFont("Hand", 9.5)
    c.setFillColor(MUTED)
    for i, line in enumerate([
            "Everything I could find of ours, finally drawn out properly.",
            "Every place I actually stopped carries one of these nine."]):
        c.drawString(left, H - 74 - i * 12, line)

    # ---- the two drawings -------------------------------------------------
    gap = 10
    box = (inner - gap) / 2
    art_y = H - 100 - box
    for img, x, caption, names in (
            (SYMBOL, left, "the symbol — three", SYMBOL_NAMES),
            (CREST, left + box + gap, "the crest — six", CREST_NAMES)):
        if not img.exists():
            raise FileNotFoundError(f"missing reference drawing: {img}")
        c.drawImage(ImageReader(str(img)), x, art_y, box, box,
                    preserveAspectRatio=True, anchor="c", mask="auto")
        c.setFillColor(INK)
        c.setFont("Hand", 11)
        c.drawCentredString(x + box / 2, art_y - 12, caption)
        c.setFillColor(MUTED)
        c.setFont("Hand", 8.6)
        for j, line in enumerate(names.split("\n")):
            c.drawCentredString(x + box / 2, art_y - 24 - j * 10, line)

    # ---- divider ----------------------------------------------------------
    div_y = art_y - 54
    c.setStrokeColor(RULE)
    c.line(left, div_y, right, div_y)

    # ---- travel highlights ------------------------------------------------
    y = div_y - 26
    c.setFillColor(INK)
    c.setFont("Hand", 17)
    c.drawString(left, y, "Travel highlights")
    y -= 19

    for group, entries in HIGHLIGHTS:
        c.setFillColor(ACCENT)
        c.setFont("Hand", 11)
        c.drawString(left, y, group)
        y -= 15
        for where, what in entries:
            c.setFillColor(INK)
            c.setFont("Hand", 10)
            c.drawString(left + 8, y, where + ".")
            used = pdfmetrics.stringWidth(where + ". ", "Hand", 10)
            c.setFillColor(MUTED)
            c.setFont("Hand", 9.4)
            # first line runs on after the place, the rest hang under it
            first = wrap(what, "Hand", 9.4, inner - 8 - used)
            if first:
                c.drawString(left + 8 + used, y, first[0])
                rest = what[len(first[0]):].strip()
            else:
                rest = what
            y -= 11
            for line in wrap(rest, "Hand", 9.4, inner - 16):
                c.drawString(left + 16, y, line)
                y -= 11
            y -= 7
        y -= 6

    c.restoreState()


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)

    c = canvas.Canvas(str(OUT), pagesize=PAGE, pageCompression=1)
    c.setTitle("Aunt Liv's journal - Family iconography")
    c.setAuthor("Escape Backpack")
    draw_page(c)
    c.showPage()
    c.save()

    c = canvas.Canvas(str(OUT_LETTER), pagesize=LETTER, pageCompression=1)
    c.setTitle("Aunt Liv's journal - Family iconography (Letter)")
    c.setAuthor("Escape Backpack")
    lw, lh = LETTER
    ox, oy = (lw - W) / 2, (lh - H) / 2
    draw_page(c, ox, oy)
    c.setStrokeColor(RULE)
    c.setLineWidth(0.5)
    c.setDash(3, 3)
    c.rect(ox, oy, W, H, fill=0, stroke=1)     # trim guide
    c.showPage()
    c.save()

    print(OUT)
    print(OUT_LETTER)


if __name__ == "__main__":
    main()
