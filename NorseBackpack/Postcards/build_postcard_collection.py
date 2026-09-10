from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from pypdf import PdfReader, PdfWriter
from reportlab.lib.pagesizes import landscape
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[2]
POSTCARDS = ROOT / "NorseBackpack" / "Postcards"
OUT = ROOT / "output" / "pdf"
SIZE = (1536, 1024)
PAGE = landscape((4 * 72, 6 * 72))
PAPER = "#EFE3C4"
TEAL = "#2F7775"
INK = "#283B34"
RULE = "#A99A7B"
MUTED = "#59635D"
HAND = ROOT / "Fonts" / "Nothing_You_Could_Do" / "NothingYouCouldDo-Regular.ttf"
SANS = Path(r"C:\Windows\Fonts\arial.ttf")
SANS_BOLD = Path(r"C:\Windows\Fonts\arialbd.ttf")

CARDS = [
    {
        "number": "02",
        "slug": "Baffin_Island",
        "place": "BAFFIN ISLAND",
        "region": "NUNAVUT",
        "front": POSTCARDS / "Postcard_02_Baffin_Island_Front.png",
        "credit": [
            'Adapted from "Grinnell Glacier Bergie Bits, Baffin Island (30587389848)"',
            'by Gregory "Slobirdr" Smith, Wikimedia Commons, CC BY-SA 2.0.',
            "Source: commons.wikimedia.org/wiki/File:Grinnell_Glacier_Bergie_Bits,_Baffin_Island_(30587389848).jpg",
            "Licence: creativecommons.org/licenses/by-sa/2.0/  |  Adapted artwork: CC BY-SA 2.0",
        ],
    },
    {
        "number": "03",
        "slug": "Battle_Harbour",
        "place": "BATTLE HARBOUR",
        "region": "NEWFOUNDLAND AND LABRADOR",
        "front": POSTCARDS / "Postcard_03_Battle_Harbour_Front.png",
        "credit": [
            'Adapted from "Battle Harbour - MacGillivray" by Matt MacGillivray,',
            "Wikimedia Commons, CC BY 2.0.",
            "Source: commons.wikimedia.org/wiki/File:Battle_Harbour_-_MacGillivray.jpg",
            "Licence: creativecommons.org/licenses/by/2.0/  |  Image converted into poster style.",
        ],
    },
]


def font(path, size):
    return ImageFont.truetype(path, size)


def build_back(card):
    image = Image.new("RGB", SIZE, PAPER)
    draw = ImageDraw.Draw(image)
    margin = 34
    draw.rectangle((margin, margin, SIZE[0] - margin, SIZE[1] - margin), outline=RULE, width=2)
    draw.text((96, 78), f"ROUTE POSTCARD {card['number']}  -  {card['place']}", font=font(SANS_BOLD, 28), fill=TEAL)
    draw.line((96, 126, SIZE[0] - 96, 126), fill=RULE, width=2)

    message = "Message and travel date\nto be finalized."
    box = draw.multiline_textbbox((0, 0), message, font=font(HAND, 58), spacing=15, align="center")
    width = box[2] - box[0]
    draw.multiline_text(((SIZE[0] - width) / 2, 340), message, font=font(HAND, 58), fill=INK, spacing=15, align="center")
    region_box = draw.textbbox((0, 0), card["region"], font=font(SANS_BOLD, 20))
    draw.text(((SIZE[0] - (region_box[2] - region_box[0])) / 2, 510), card["region"], font=font(SANS_BOLD, 20), fill=TEAL)

    draw.line((96, 820, SIZE[0] - 96, 820), fill=RULE, width=2)
    y = 842
    for line in card["credit"]:
        draw.text((96, y), line, font=font(SANS, 16), fill=MUTED)
        y += 24

    output = POSTCARDS / f"Postcard_{card['number']}_{card['slug']}_Back.png"
    image.save(output, optimize=True)
    return output


def build_pdf(front, back, output):
    width, height = PAGE
    pdf = canvas.Canvas(str(output), pagesize=PAGE, pageCompression=1)
    for image in (front, back):
        pdf.drawImage(ImageReader(str(image)), 0, 0, width, height, preserveAspectRatio=False, mask="auto")
        pdf.showPage()
    pdf.save()


def combine_pdfs(inputs, output):
    writer = PdfWriter()
    for item in inputs:
        for page in PdfReader(item).pages:
            writer.add_page(page)
    with output.open("wb") as stream:
        writer.write(stream)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    individual = [OUT / "Postcard_01_LAnse_Print.pdf"]
    for card in CARDS:
        back = build_back(card)
        output = OUT / f"Postcard_{card['number']}_{card['slug']}_Print.pdf"
        build_pdf(card["front"], back, output)
        individual.append(output)
        print(output)

    collection = OUT / "Norse_Postcards_Full_Print.pdf"
    combine_pdfs(individual, collection)
    print(collection)


if __name__ == "__main__":
    main()
