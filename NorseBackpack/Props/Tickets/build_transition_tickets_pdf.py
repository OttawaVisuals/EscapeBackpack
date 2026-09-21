"""The three transition tickets (PZ-18) -- the props that chain the four legs.

Each is a printed multi-segment booking confirmation running from the LAST stop
of one leg to the FIRST stop of the next, so one document proves two things:
that card closes its leg, and that card opens the next one. Chain all three and
the leg order falls out, which is why they live in the final bundle and not in
play -- leg order has to stay unknowable until the reveal.

    Leif  -> Rollo    Qikiqtarjuaq      -> Walcheren
    Rollo -> Aud      Roumare Forest    -> Dogurdarnes
    Aud   -> Harald   Esjuberg          -> Oslo

Why multi-segment rather than a boarding pass
---------------------------------------------
There is no direct Qikiqtarjuaq-Netherlands service, and none of the other
endpoints is an airport either -- Roumare is a forest, Dogurdarnes and Esjuberg
are Icelandic farmsteads. A single boarding pass could only name airports, and
"which port serves which town" is exactly the outside knowledge the evidence
rules forbid. A booking confirmation names every waypoint including the real
first and last, so the puzzle-critical endpoints are printed in full.

What matters, and what does not
-------------------------------
LOAD-BEARING: the first origin and the last destination of each ticket. Those
two place names are the entire clue. Everything else -- carriers, service
numbers, times, the booking reference -- is dressing and can be changed freely.

The dates sit in the gaps between legs and are deliberately loose: Liv stays
abroad between legs rather than flying home, so a ticket need not depart the day
a leg's last stay ends. Decided in chat, 20 Sept 2026.

Run:  python NorseBackpack/Props/Tickets/build_transition_tickets_pdf.py
"""
from pathlib import Path

from reportlab.lib.colors import HexColor, Color
from reportlab.lib.pagesizes import LETTER, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[3]
FONT_DIR = ROOT / "Fonts"
OUT = ROOT / "output" / "pdf" / "Transition_Tickets_Print.pdf"
OUT_SHEET = ROOT / "output" / "pdf" / "Transition_Tickets_Letter_Print.pdf"

pdfmetrics.registerFont(TTFont("CinzelBold", str(FONT_DIR / "Cinzel" / "static" / "Cinzel-Bold.ttf")))

PAGE = landscape((5.4 * 72, 2.5 * 72))
W, H = PAGE

PAPER = HexColor("#FAF6EC")
BAND = HexColor("#25372F")
INK = HexColor("#283B34")
RULE = HexColor("#C4BBA2")
MUTED = HexColor("#6B7568")
ACCENT = HexColor("#B56A2A")
ZEBRA = Color(0.83, 0.80, 0.72, alpha=0.30)

AGENCY = "NORDVEG TRAVEL"
# No surname for Liv is recorded anywhere in the project; the nephew the cards
# are addressed to is "John Ericson", so she is given his. Flagged in the page --
# change here if a different family name is ever settled.
PAX = "ERICSON / LIV"

# ref, leg pair, segments as (date, from, to, carrier, service)
# The first `from` and the last `to` are the clue. The rest is dressing.
TICKETS = [
    ("RX7T2Q", "014 2277 418 903", "Leif", "Rollo", [
        ("26 SEP 2024", "Qikiqtarjuaq", "Iqaluit",      "Canadian North", "5T 501"),
        ("26 SEP 2024", "Iqaluit",      "Ottawa",       "Canadian North", "5T 140"),
        ("27 SEP 2024", "Ottawa",       "Amsterdam",    "KLM",            "KL 672"),
        ("28 SEP 2024", "Amsterdam",    "Walcheren",    "NS rail",        "IC 2214"),
    ]),
    ("M4KD8B", "108 5514 260 771", "Rollo", "Aud", [
        ("08 MAY 2025", "Roumare Forest", "Rouen",      "TER Normandie",  "TER 3312"),
        ("08 MAY 2025", "Rouen",          "Paris CDG",  "TER Normandie",  "TER 3350"),
        ("09 MAY 2025", "Paris CDG",      "Reykjavik",  "Icelandair",     "FI 543"),
        ("09 MAY 2025", "Reykjavik",      "Dogurdarnes", "Vestfjardaleid", "CO 58"),
    ]),
    ("QN2V6H", "108 5514 260 984", "Aud", "Harald", [
        ("05 JUN 2025", "Esjuberg",  "Reykjavik", "Vestfjardaleid", "CO 12"),
        ("06 JUN 2025", "Reykjavik", "Oslo",      "Icelandair",     "FI 318"),
    ]),
]


def draw_ticket(c, ref, etkt, leg_from, leg_to, segs, ox=0, oy=0):
    c.saveState()
    c.translate(ox, oy)

    c.setFillColor(PAPER)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # header band
    c.setFillColor(BAND)
    c.rect(0, H - 34, W, 34, fill=1, stroke=0)
    c.setFillColor(HexColor("#EFE3C4"))
    c.setFont("CinzelBold", 12)
    c.drawString(16, H - 22, AGENCY)
    c.setFont("Helvetica", 7)
    c.drawRightString(W - 16, H - 15, "ELECTRONIC TICKET · ITINERARY RECEIPT")
    c.drawRightString(W - 16, H - 25, "RETAIN FOR YOUR RECORDS")

    # passenger / reference strip
    y = H - 50
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 6.4)
    c.drawString(16, y + 9, "PASSENGER")
    c.drawString(168, y + 9, "BOOKING REF")
    c.drawString(236, y + 9, "ISSUED")
    c.drawString(300, y + 9, "E-TICKET")
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(16, y - 1, PAX)
    c.drawString(168, y - 1, ref)
    c.setFont("Helvetica", 8.5)
    c.drawString(236, y - 1, segs[0][0])
    c.setFont("Helvetica", 7.4)
    c.drawString(300, y - 1, etkt)

    c.setStrokeColor(RULE)
    c.setLineWidth(0.7)
    c.line(16, y - 10, W - 16, y - 10)

    # segment table
    cols = (16, 86, 178, 268, 330)
    heads = ("DATE", "FROM", "TO", "CARRIER", "SERVICE")
    ry = y - 22
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 6.4)
    for x, head in zip(cols, heads):
        c.drawString(x, ry, head)
    ry -= 4

    row_h = 15
    for i, (date, frm, to, carrier, svc) in enumerate(segs):
        ry -= row_h
        if i % 2 == 0:
            c.setFillColor(ZEBRA)
            c.rect(13, ry - 3.5, W - 26, row_h - 1, fill=1, stroke=0)
        first, last = i == 0, i == len(segs) - 1
        c.setFillColor(INK)
        c.setFont("Helvetica", 7.6)
        c.drawString(cols[0], ry, date)
        # the two place names the puzzle actually needs are set bolder
        c.setFont("Helvetica-Bold" if first else "Helvetica", 8.4 if first else 7.8)
        c.drawString(cols[1], ry, frm)
        c.setFont("Helvetica-Bold" if last else "Helvetica", 8.4 if last else 7.8)
        c.drawString(cols[2], ry, to)
        c.setFillColor(MUTED)
        c.setFont("Helvetica", 7)
        c.drawString(cols[3], ry, carrier)
        c.drawString(cols[4], ry, svc)

    # footer
    c.setStrokeColor(RULE)
    c.line(16, 26, W - 16, 26)
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 6.6)
    c.drawString(16, 16, "Fares quoted are per passenger and include all taxes and surcharges.")
    c.drawString(16, 8, "Changes permitted up to 24h before the first departure. Non-refundable.")
    c.setFillColor(ACCENT)
    c.setFont("Helvetica-Bold", 6.6)
    c.drawRightString(W - 16, 8, f"{len(segs)} SEGMENTS")

    c.setStrokeColor(RULE)
    c.setLineWidth(0.6)
    c.rect(4, 4, W - 8, H - 8, fill=0, stroke=1)
    c.restoreState()


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)

    c = canvas.Canvas(str(OUT), pagesize=PAGE, pageCompression=1)
    c.setTitle("Transition tickets - Aunt Liv")
    c.setAuthor("Escape Backpack")
    for ref, etkt, a, b, segs in TICKETS:
        draw_ticket(c, ref, etkt, a, b, segs)
        c.showPage()
    c.save()

    # all three on one Letter sheet, stacked, with trim guides
    c = canvas.Canvas(str(OUT_SHEET), pagesize=LETTER, pageCompression=1)
    c.setTitle("Transition tickets - Aunt Liv (Letter)")
    c.setAuthor("Escape Backpack")
    lw, lh = LETTER
    ox = (lw - W) / 2
    gap = 30
    block = len(TICKETS) * H + (len(TICKETS) - 1) * gap
    top = lh - (lh - block) / 2            # centre the block, not hang it from the top
    for i, (ref, etkt, a, b, segs) in enumerate(TICKETS):
        oy = top - (i + 1) * H - i * gap
        draw_ticket(c, ref, etkt, a, b, segs, ox, oy)
        c.setStrokeColor(RULE)
        c.setLineWidth(0.5)
        c.setDash(3, 3)
        c.rect(ox, oy, W, H, fill=0, stroke=1)
        c.setDash()
    c.showPage()
    c.save()

    print(OUT)
    print(OUT_SHEET)


if __name__ == "__main__":
    main()
