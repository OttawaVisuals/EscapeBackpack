from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from pypdf import PdfReader, PdfWriter
from reportlab.lib.pagesizes import landscape
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[2]
POSTCARDS = ROOT / "NorseBackpack" / "Postcards"
OUT = ROOT / "output" / "pdf"
# PC-13: card is 5 x 3.5 in (10:7), matching build_postcard_01_pdf.py exactly.
SIZE = (1500, 1050)
PAGE = landscape((3.5 * 72, 5 * 72))
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
        "slug": "Battle_Harbour",
        "place": "BATTLE HARBOUR",
        "region": "NEWFOUNDLAND AND LABRADOR",
        "front": POSTCARDS / "Postcard_02_Battle_Harbour_Front.png",
        # One human-readable line, matching card 01 (PC-09). The source and licence URLs and the
        # adaptation licence live in Image_Credits.html, which now documents all three cards
        # (PC-14) -- printing URLs on a prop meant to read as a gift-shop postcard was the only
        # anachronism on these backs.
        "credit": [
            'Image adaptation: "Battle Harbour - MacGillivray" - Matt MacGillivray, CC BY 2.0.',
        ],
    },
    {
        "number": "03",
        "slug": "Baffin_Island",
        "place": "BAFFIN ISLAND",
        "region": "NUNAVUT",
        "front": POSTCARDS / "Postcard_03_Baffin_Island_Front.png",
        "credit": [
            'Image adaptation: "Grinnell Glacier Bergie Bits, Baffin Island" '
            '- Gregory "Slobirdr" Smith, CC BY-SA 2.0.',
        ],
    },
]


def font(path, size):
    return ImageFont.truetype(path, size)


def build_back(card):
    # Placeholder layout, positioned as fractions of the card so it holds at any SIZE (PC-13
    # moved this canvas from 1536x1024 to 1500x1050; a fixed-pixel layout would need redoing
    # again on the next size change). Real content will replace this per PZ-05.
    W, H = SIZE
    image = Image.new("RGB", SIZE, PAPER)
    draw = ImageDraw.Draw(image)
    margin = round(W * 0.0221)
    draw.rectangle((margin, margin, W - margin, H - margin), outline=RULE, width=2)
    side = round(W * 0.0625)
    draw.text((side, round(H * 0.0762)), f"ROUTE POSTCARD {card['number']}  -  {card['place']}", font=font(SANS_BOLD, 28), fill=TEAL)
    draw.line((side, round(H * 0.123), W - side, round(H * 0.123)), fill=RULE, width=2)

    message = "Message and travel date\nto be finalized."
    box = draw.multiline_textbbox((0, 0), message, font=font(HAND, 58), spacing=15, align="center")
    width = box[2] - box[0]
    draw.multiline_text(((W - width) / 2, round(H * 0.332)), message, font=font(HAND, 58), fill=INK, spacing=15, align="center")
    region_box = draw.textbbox((0, 0), card["region"], font=font(SANS_BOLD, 20))
    draw.text(((W - (region_box[2] - region_box[0])) / 2, round(H * 0.498)), card["region"], font=font(SANS_BOLD, 20), fill=TEAL)

    draw.line((side, round(H * 0.801), W - side, round(H * 0.801)), fill=RULE, width=2)
    y = round(H * 0.822)
    for line in card["credit"]:
        draw.text((side, y), line, font=font(SANS, 16), fill=MUTED)
        y += 24

    output = POSTCARDS / f"Postcard_{card['number']}_{card['slug']}_Back.png"
    image.save(output, optimize=True)
    return output


def build_pdf(front, back, output):
    width, height = PAGE
    pdf = canvas.Canvas(str(output), pagesize=PAGE, pageCompression=1)
    for image in (front, back):
        img = ImageReader(str(image))
        # PC-11: this previously drew a 1500x1050 front onto a 1536x1024-shaped (6x4in) page
        # with preserveAspectRatio=False, silently stretching it 5%. Fail loud instead.
        if img.getSize() != SIZE:
            raise ValueError(f"{image} is {img.getSize()}, expected {SIZE} (PC-13). "
                              f"Drawing it here would stretch it to fit the page.")
        pdf.drawImage(img, 0, 0, width, height, preserveAspectRatio=False, mask="auto")
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
