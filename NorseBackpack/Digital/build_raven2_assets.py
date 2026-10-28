"""Digital art for The Raven Inheritance, V2 (box, envelopes and cypher wheel).

Renders the live print PDFs in NorseBackpack/Print/_pdf_source to cropped, real-size images in
Digital/assets/v2/ and writes their sizes in inches to Digital/raven2-sizes.js, so the digital
table draws every printed prop at the size it prints.

Run: python NorseBackpack/Digital/build_raven2_assets.py
"""
import json
from pathlib import Path

import pymupdf
from PIL import Image, ImageChops, ImageEnhance, ImageOps

HERE = Path(__file__).resolve().parent
PDF = HERE.parent / "Print" / "_pdf_source"
OUT = HERE / "assets" / "v2"
DPI = 150

# image name -> (pdf, page, crop). crop: None = whole page, "ink" = trim to the printed tickets,
# "green" = trim to the green ruler card.
JOBS = {
    "Notes_Card": ("Liv_Notes_Card_Print", 0, None),
    "Aud_Ticket_Front": ("Aud_Ticket_Print", 0, None),
    "Aud_Ticket_Back": ("Aud_Ticket_Print", 1, None),
    "Museum_Ticket_Front": ("Museum_Ticket_Print", 0, None),
    "Museum_Ticket_Back": ("Museum_Ticket_Print", 1, None),
    "Rouen_Ticket_Front": ("Rouen_Ticket_Print", 0, None),
    "Rouen_Ticket_Back": ("Rouen_Ticket_Print", 1, None),
    "Hnefatafl_Ticket_Front": ("Hnefatafl_Ticket_Print", 0, None),
    "Hnefatafl_Ticket_Back": ("Hnefatafl_Ticket_Print", 1, None),
    "Map_Leif": ("Trail_Map_1_Leif_Print", 0, None),
    "Map_Rollo": ("Trail_Map_2_Rollo_Print", 0, None),
    "Map_Aud": ("Trail_Map_3_Aud_Print", 0, None),
    "Map_Harald_Front": ("Trail_Map_4_Harald_Print", 0, None),
    "Map_Harald_Back": ("Trail_Map_4_Harald_Print", 1, None),
    "Raven_Flights_Card": ("Raven_Flights_Card_Print", 0, None),
    "Flight_Booking_1": ("Transition_Tickets_Print", 0, None),
    "Flight_Booking_2": ("Transition_Tickets_Print", 1, None),
    "Flight_Booking_3": ("Transition_Tickets_Print", 2, None),
    "Hop_Tickets_Leif": ("Hop_Tickets_Print", 0, "ink"),
    "Hop_Tickets_Rollo": ("Hop_Tickets_Print", 1, "ink"),
    "Hop_Tickets_Aud": ("Hop_Tickets_Print", 2, "ink"),
    "Hop_Tickets_Harald": ("Hop_Tickets_Print", 3, "ink"),
    "Plane_Ticket": ("Plane_Ticket_Print", 0, None),
    "Final_Letter": ("Liv_Final_Letter_Print", 0, None),
    "Ruler": ("Liv_Ruler_Print", 0, "green"),
}


def crop_box(img, mode):
    rgb = img.convert("RGB")
    if mode == "green":
        # the card is the only large forest-green area (#1E4A38)
        r, g, b = rgb.split()
        mask = ImageChops.multiply(ImageChops.multiply(r.point(lambda v: 255 if v < 70 else 0), g.point(lambda v: 255 if 55 < v < 100 else 0)), b.point(lambda v: 255 if 35 < v < 90 else 0))
        # keep rows and columns that are mostly green, so thin text and corner marks do not count
        cols = [x for x in range(mask.width) if sum(1 for y in range(0, mask.height, 4) if mask.getpixel((x, y))) > 20]
        rows = [y for y in range(mask.height) if sum(1 for x in range(0, mask.width, 4) if mask.getpixel((x, y))) > mask.width / 8]
        return (cols[0], rows[0], cols[-1] + 1, rows[-1] + 1)
    # ink: anything not near white, below the page header (top 8%)
    diff = ImageChops.difference(rgb, Image.new("RGB", rgb.size, (255, 255, 255))).convert("L").point(lambda v: 255 if v > 14 else 0)
    top = int(rgb.height * 0.08)
    diff.paste(0, (0, 0, rgb.width, top))
    return diff.getbbox()


def main():
    sizes = {}
    for name, (pdf, page, mode) in JOBS.items():
        src = PDF / f"{pdf}.pdf"
        with pymupdf.open(src) as d:
            pm = d[page].get_pixmap(dpi=DPI)
            img = Image.frombytes("RGB", (pm.width, pm.height), pm.samples)
        if mode:
            box = crop_box(img, mode)
            img = img.crop(box)
        img.save(OUT / f"{name}.webp", "WEBP", quality=88)
        sizes[name] = [round(img.width / DPI, 3), round(img.height / DPI, 3)]
        print(f"{name:24s} {sizes[name][0]:6.2f} x {sizes[name][1]:5.2f} in")
    # The ruler turned half way round: its SPEAR edge on top, 0 at the left (second face).
    Image.open(OUT / "Ruler.webp").rotate(180).save(OUT / "Ruler_Spear.webp", "WEBP", quality=88)
    sizes["Ruler_Spear"] = sizes["Ruler"]
    # The Oslo ticket held up to the light: the back shows through, mirrored (PZ-008).
    front = Image.open(OUT / "Hnefatafl_Ticket_Front.webp").convert("RGB")
    back = ImageOps.mirror(Image.open(OUT / "Hnefatafl_Ticket_Back.webp").convert("RGB")).resize(front.size)
    far = Image.blend(Image.new("RGB", back.size, (255, 255, 255)), back, 0.62)
    seen = ImageChops.multiply(ImageEnhance.Brightness(front).enhance(1.12), far)
    seen = ImageChops.multiply(ImageEnhance.Brightness(seen).enhance(1.08), Image.new("RGB", seen.size, (255, 247, 228)))
    seen.save(OUT / "Hnefatafl_Ticket_Light.webp", "WEBP", quality=88)
    sizes["Hnefatafl_Ticket_Light"] = sizes["Hnefatafl_Ticket_Front"]
    js = ("/* Written by build_raven2_assets.py: printed prop sizes in inches. Do not edit. */\n"
          "(function (root) { const sizes = " + json.dumps(sizes, indent=1) + ";\n"
          "  if (typeof module !== 'undefined' && module.exports) module.exports = sizes; else root.RavenSizes = sizes;\n"
          "})(typeof window === 'undefined' ? globalThis : window);\n")
    (HERE / "raven2-sizes.js").write_text(js, encoding="utf-8")


if __name__ == "__main__":
    main()
