"""The final plane ticket (PP-043, envelope 13): Ottawa -> Stockholm, summer 2027.

Designer brief (17 Oct 2026): passenger shown by LAST NAME only, Ottawa to Stockholm, summer 2027.
No exact date was given, so it is an open ticket marked SUMMER 2027. Carrier Nordic Air and the
flight number are invented dressing, like the other tickets (build_hop_tickets_pdf.py).
The surname is the one already used on the other tickets (Q-058 notes it points at Leif).

Run:  python NorseBackpack/Props/Tickets/build_plane_ticket_pdf.py
"""
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[3]
FONT_DIR = ROOT / "Fonts"
OUT = ROOT / "NorseBackpack" / "Print" / "_pdf_source" / "Plane_Ticket_Print.pdf"
pdfmetrics.registerFont(TTFont("CinzelBold", str(FONT_DIR / "Cinzel" / "static" / "Cinzel-Bold.ttf")))

W, H = 7.0 * 72, 2.9 * 72
PAPER, BAND = HexColor("#FAF6EC"), HexColor("#216580")
INK, MUTED, RULE = HexColor("#283B34"), HexColor("#6B7568"), HexColor("#C4BBA2")
CREAM, ACCENT = HexColor("#EFE3C4"), HexColor("#B56A2A")

SURNAME = "ERICSON"


def label(c, x, y, text):
    c.setFillColor(MUTED); c.setFont("Helvetica", 6.4); c.drawString(x, y, text)


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUT), pagesize=(W, H), pageCompression=1)
    c.setTitle("Plane ticket - Ottawa to Stockholm"); c.setAuthor("Escape Backpack")
    c.setFillColor(PAPER); c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(BAND); c.rect(0, H - 38, W, 38, fill=1, stroke=0)
    c.setFillColor(CREAM); c.setFont("CinzelBold", 15); c.drawString(18, H - 25, "NORDIC AIR")
    c.setFont("Helvetica-Bold", 8); c.drawRightString(W - 18, H - 24, "BOARDING PASS  ·  ECONOMY")

    stub = W - 112
    c.setStrokeColor(RULE); c.setDash(2, 2); c.line(stub, 8, stub, H - 46); c.setDash()

    label(c, 18, H - 56, "PASSENGER")
    c.setFillColor(INK); c.setFont("Helvetica-Bold", 13); c.drawString(18, H - 72, SURNAME)

    label(c, 18, H - 96, "FROM")
    c.setFillColor(INK); c.setFont("CinzelBold", 24); c.drawString(18, H - 120, "OTTAWA")
    c.setFont("Helvetica-Bold", 9); c.setFillColor(ACCENT); c.drawString(20, H - 133, "YOW")
    c.setFillColor(ACCENT); c.setFont("Helvetica-Bold", 16); c.drawString(158, H - 118, "→")
    label(c, 190, H - 96, "TO")
    c.setFillColor(INK); c.setFont("CinzelBold", 24); c.drawString(190, H - 120, "STOCKHOLM")
    c.setFont("Helvetica-Bold", 9); c.setFillColor(ACCENT); c.drawString(192, H - 133, "ARN")

    label(c, 18, 22, "FLIGHT"); c.setFillColor(INK); c.setFont("Helvetica-Bold", 9.5); c.drawString(18, 10, "NA 901")
    label(c, 100, 22, "DATE"); c.setFillColor(INK); c.setFont("Helvetica-Bold", 9.5); c.drawString(100, 10, "SUMMER 2027")
    label(c, 210, 22, "TICKET"); c.setFillColor(INK); c.setFont("Helvetica", 9.5); c.drawString(210, 10, "OPEN · ONE WAY")

    sx = stub + 12
    label(c, sx, H - 56, "PASSENGER"); c.setFillColor(INK); c.setFont("Helvetica-Bold", 9); c.drawString(sx, H - 68, SURNAME)
    label(c, sx, H - 88, "FROM"); c.setFillColor(INK); c.setFont("Helvetica-Bold", 11); c.drawString(sx, H - 101, "YOW")
    label(c, sx, H - 118, "TO"); c.setFillColor(INK); c.setFont("Helvetica-Bold", 11); c.drawString(sx, H - 131, "ARN")
    label(c, sx, 22, "DATE"); c.setFillColor(INK); c.setFont("Helvetica-Bold", 8.5); c.drawString(sx, 10, "SUMMER 2027")

    c.setStrokeColor(RULE); c.setLineWidth(0.6); c.roundRect(3, 3, W - 6, H - 6, 6, fill=0, stroke=1)
    c.showPage(); c.save(); print(OUT)


if __name__ == "__main__":
    main()
