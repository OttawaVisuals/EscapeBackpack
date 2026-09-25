from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from pypdf import PdfReader, PdfWriter
from reportlab.lib.pagesizes import landscape
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[2]
POSTCARDS = ROOT / "NorseBackpack" / "Postcards"
OUT = ROOT / "output" / "pdf"
# PC-13: card is 5 x 3.5 in (10:7), matching build_postcard_L1_pdf.py exactly.
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

# Leif's three real stops (L1, L2, L3) all now have their own dedicated scripts --
# build_postcard_L1_pdf.py, build_postcard_L2_pdf.py, build_postcard_L3_pdf.py -- with real
# messages, Fun Facts and imprints (PZ-05, PZ-10, PZ-13). None of them may be rebuilt here with
# placeholder text. CARDS stays empty until some other future card is ready for its own dedicated
# script; build_back()/build_pdf() are kept for whichever of those gets placeholder content first.
CARDS = []


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
    # All 22 cards, each built by its own build_postcard_<ID>_pdf.py, in deck order: trail by
    # trail (PC-17 numbering), decoy last in each trail. Updated 25 Sept 2026 -- the collection
    # had held only L1-L3 since before the other nineteen cards were built.
    deck = ["L1_LAnse", "L2_Battle_Harbour", "L3_Baffin_Island", "LD_Brattahlid",
            "R1_Chalus", "R2_Rouen", "R3_Bayeux", "R4_Winchester", "R5_Battle",
            "R6_Roumare_Forest", "RD_Walcheren",
            "A1_Dogurdarnes", "A2_Hvammur", "A3_Esjuberg", "AD_Bjarnarhofn",
            "H1_Oslo", "H2_Staraya_Ladoga", "H3_Kyiv", "H4_Hedeby", "H5_Sicily", "H6_Patara",
            "HD_Constantinople"]
    individual = [OUT / f"Postcard_{card}_Print.pdf" for card in deck]
    missing = [path.name for path in individual if not path.exists()]
    if missing:
        raise SystemExit("missing card PDFs: " + ", ".join(missing))
    for card in CARDS:
        back = build_back(card)
        output = OUT / f"Postcard_{card['number']}_{card['slug']}_Print.pdf"
        build_pdf(card["front"], back, output)
        individual.append(output)
        print(output)

    collection = OUT / "Norse_Postcards_Full_Print.pdf"
    combine_pdfs(individual, collection)
    shrink_for_viewing(collection)
    print(collection)


def shrink_for_viewing(path):
    """The 22 lossless cards merge to ~165 MB, over GitHub's 100 MB file limit. This file is the
    page's "View full postcard PDF" preview, not a print master (print from the per-card PDFs),
    so its images are re-encoded as JPEG at quality 88: ~18 MB, no visible change at 300 dpi."""
    import pymupdf
    doc = pymupdf.open(path)
    doc.rewrite_images(dpi_threshold=None, quality=88, lossy=True, lossless=True,
                       bitonal=True, color=True, gray=True, set_to_gray=False)
    tmp = path.with_suffix(".tmp.pdf")
    doc.save(tmp, garbage=4, deflate=True)
    doc.close()
    tmp.replace(path)


if __name__ == "__main__":
    main()
