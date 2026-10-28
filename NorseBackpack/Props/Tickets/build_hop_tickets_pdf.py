"""The hop tickets (Q-062, 17 Oct 2026): one ticket per move between two stops of a journey.

Each journey's tickets are one prop (Leif's flights and ferry, Rollo's rail pass, Aud's Iceland
buses, Harald's mixed tickets). A ticket only says FROM -> TO; chaining them gives the journey's
stop order, decoy stops included (the raven on a postcard is what tells a real stop from a decoy).
The tickets are printed in a fixed scrambled order so players chain them, and carry no extra clue
(playtest 1 found order clues spread over card text and tickets too complicated). 19 Oct 2026
(designer): every ticket now carries its departure date, from ticket_dates.py.

The stop order is the card numbering already used by the final puzzle (L1-L3, R1-R6, A1-A3,
H1-H6, Tools/final_riddle_clues.py). Where each DECOY sits in its journey was not recorded
before; the positions below are a design choice (flagged in Q-062): the first and last stop of
each journey stay where the old transition tickets put them.

Company names are invented (Nordic Air, Viking Rail, Longship Buses, Longship Ferries).
Reference and service numbers are dressing.

Run:  python NorseBackpack/Props/Tickets/build_hop_tickets_pdf.py
"""
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from ticket_dates import HOP_DATES

ROOT =Path(__file__).resolve().parents[3]
FONT_DIR = ROOT / "Fonts"
OUT = ROOT / "NorseBackpack" / "Print" / "_pdf_source" / "Hop_Tickets_Print.pdf"

pdfmetrics.registerFont(TTFont("CinzelBold", str(FONT_DIR / "Cinzel" / "static" / "Cinzel-Bold.ttf")))

W, H = 5.4 * 72, 1.45 * 72
PAPER = HexColor("#FAF6EC")
INK = HexColor("#283B34")
MUTED = HexColor("#6B7568")
RULE = HexColor("#C4BBA2")
ACCENT = HexColor("#B56A2A")
CREAM = HexColor("#EFE3C4")

PAX = "ERICSON / LIV"

# operator -> (display name, mode word, band colour)
OPS = {
    "air":   ("NORDIC AIR",       "FLIGHT", HexColor("#216580")),
    "rail":  ("VIKING RAIL",      "TRAIN",  HexColor("#7A2E2E")),
    "bus":   ("LONGSHIP BUSES",   "BUS",    HexColor("#6D528B")),
    "ferry": ("LONGSHIP FERRIES", "FERRY",  HexColor("#25372F")),
}

# journey -> (prop title, subtitle, [(from, to, mode, service)] in journey order, print order)
PROPS = [
    ("Leif", "LEIF'S TICKETS", "Flights and a ferry",
     [("L'Anse aux Meadows", "Battle Harbour", "ferry", "LF 11"),
      ("Battle Harbour", "Brattahlid", "air", "NA 722"),
      ("Brattahlid", "Qikiqtarjuaq", "air", "NA 730")],
     [2, 0, 1]),
    ("Rollo", "ROLLO'S TICKETS", "Viking Rail pass, with one ferry",
     [("Walcheren", "Chalus", "rail", "VR 6120"),
      ("Chalus", "Rouen", "rail", "VR 3340"),
      ("Rouen", "Bayeux", "rail", "VR 3412"),
      ("Bayeux", "Winchester", "ferry", "LF 204"),
      ("Winchester", "Battle", "rail", "VR 5530"),
      ("Battle", "Roumare Forest", "rail", "VR 5588")],
     [3, 0, 5, 2, 4, 1]),
    ("Aud", "AUD'S TICKETS", "Iceland bus tickets",
     [("Dogurdarnes", "Hvammur", "bus", "LB 31"),
      ("Hvammur", "Bjarnarhofn", "bus", "LB 47"),
      ("Bjarnarhofn", "Esjuberg", "bus", "LB 52")],
     [1, 2, 0]),
    ("Harald", "HARALD'S TICKETS", "Boats, trains, flights and a bus",
     [("Oslo", "Staraya Ladoga", "ferry", "LF 810"),
      ("Staraya Ladoga", "Kyiv", "rail", "VR 9021"),
      ("Kyiv", "Constantinople", "ferry", "LF 377"),
      ("Constantinople", "Hedeby", "air", "NA 455"),
      ("Hedeby", "Aci Castello", "air", "NA 463"),
      ("Aci Castello", "Patara", "bus", "LB 90")],
     [3, 0, 5, 2, 4, 1]),
]


def draw_ticket(c, frm, to, mode, service, ref, ox, oy):
    name, word, colour = OPS[mode]
    c.saveState()
    c.translate(ox, oy)
    c.setFillColor(PAPER)
    c.roundRect(0, 0, W, H, 6, fill=1, stroke=0)
    # left band
    band = 74
    c.setFillColor(colour)
    c.rect(0, 0, band, H, fill=1, stroke=0)
    c.setFillColor(CREAM)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(band / 2, H / 2 + 4, word)
    c.setFont("Helvetica", 5.6)
    c.drawCentredString(band / 2, H / 2 - 7, name)
    # stub perforation
    stub = W - 78
    c.setStrokeColor(RULE)
    c.setDash(2, 2)
    c.line(stub, 6, stub, H - 6)
    c.setDash()
    # main body
    left = band + 14
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 6)
    c.drawString(left, H - 17, "FROM")
    c.drawString(left, H - 51, "TO")
    c.setFillColor(INK)
    c.setFont("CinzelBold", 13)
    c.drawString(left, H - 31, frm.upper())
    c.drawString(left, H - 65, to.upper())
    c.setStrokeColor(RULE)
    c.line(left, 24, stub - 10, 24)
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 6.4)
    c.drawString(left, 13, "PASSENGER")
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 7.4)
    c.drawString(left + 46, 13, PAX)
    # stub
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 5.6)
    c.drawString(stub + 8, H - 17, "SERVICE")
    c.drawString(stub + 8, H - 43, "TICKET")
    c.drawString(stub + 8, H - 69, "DATE")
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(stub + 8, H - 27, service)
    c.setFont("Helvetica", 7.4)
    c.drawString(stub + 8, H - 53, ref)
    c.setFont("Helvetica", 7.4)
    c.drawString(stub + 8, H - 79, HOP_DATES[service])
    c.setFillColor(ACCENT)
    c.setFont("Helvetica-Bold", 5.6)
    c.drawString(stub + 8, 8, "ONE WAY")
    # outline
    c.setStrokeColor(RULE)
    c.setLineWidth(0.6)
    c.roundRect(0.5, 0.5, W - 1, H - 1, 6, fill=0, stroke=1)
    c.restoreState()


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUT), pagesize=LETTER, pageCompression=1)
    c.setTitle("Hop tickets - Aunt Liv")
    c.setAuthor("Escape Backpack")
    lw, lh = LETTER
    gap = 14
    n_ref = 0
    for key, title, sub, hops, order in PROPS:
        c.setFillColor(MUTED)
        c.setFont("Helvetica", 7)
        c.drawCentredString(lw / 2, lh - 28, f"{title}  ·  {sub}  ·  cut along the dashed lines")
        block = len(hops) * H + (len(hops) - 1) * gap
        top = lh - 44 - (lh - 60 - block) / 2
        ox = (lw - W) / 2
        for slot, idx in enumerate(order):
            frm, to, mode, service = hops[idx]
            n_ref += 1
            ref = f"{"QHXMTKWR"[n_ref % 8]}{(n_ref * 7919) % 9000 + 1000}"
            oy = top - (slot + 1) * H - slot * gap
            draw_ticket(c, frm, to, mode, service, ref, ox, oy)
            c.setStrokeColor(RULE)
            c.setLineWidth(0.4)
            c.setDash(3, 3)
            c.rect(ox - 3, oy - 3, W + 6, H + 6, fill=0, stroke=1)
            c.setDash()
        c.showPage()
    c.save()
    print(OUT)


if __name__ == "__main__":
    main()
