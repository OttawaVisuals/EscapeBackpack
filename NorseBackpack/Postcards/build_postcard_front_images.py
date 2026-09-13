from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
POSTCARDS = ROOT / "NorseBackpack" / "Postcards"
TITLE_FONT = ROOT / "Fonts" / "Cinzel" / "static" / "Cinzel-ExtraBold.ttf"
SUBTITLE_FONT = Path(r"C:\Windows\Fonts\arialbd.ttf")
PAPER = "#EFE3C4"
SHADOW = "#071B1E"

CARDS = [
    (
        POSTCARDS / "Postcard_01_LAnse_Illustration_v3.png",
        POSTCARDS / "Postcard_01_LAnse_Front.png",
        "L'ANSE AUX MEADOWS",
        "NEWFOUNDLAND AND LABRADOR",
    ),
    (
        POSTCARDS / "Postcard_02_Battle_Harbour_Illustration_v1.png",
        POSTCARDS / "Postcard_02_Battle_Harbour_Front.png",
        "BATTLE HARBOUR",
        "NEWFOUNDLAND AND LABRADOR",
    ),
    (
        POSTCARDS / "Postcard_03_Baffin_Island_Illustration_v1.png",
        POSTCARDS / "Postcard_03_Baffin_Island_Front.png",
        "BAFFIN ISLAND",
        "NUNAVUT",
    ),
]


def spaced_width(draw, text, font, spacing):
    return sum(draw.textlength(char, font=font) for char in text) + spacing * (len(text) - 1)


def draw_spaced_text(draw, center_x, y, text, font, spacing, fill):
    width = spaced_width(draw, text, font, spacing)
    x = center_x - width / 2
    for char in text:
        draw.text((x, y), char, font=font, fill=fill, anchor="lt")
        x += draw.textlength(char, font=font) + spacing


def fit_title(draw, text, max_width):
    size = 92
    while size > 52:
        font = ImageFont.truetype(TITLE_FONT, size)
        spacing = round(size * 0.045)
        if spaced_width(draw, text, font, spacing) <= max_width:
            return font, spacing
        size -= 2
    return ImageFont.truetype(TITLE_FONT, size), round(size * 0.045)


# PC-13: card is 5 x 3.5 in (10:7). At 300 dpi that is 1500 x 1050 px -- matches
# build_postcard_01_pdf.py's PAGE exactly, so no aspect distortion at draw time.
EXPECTED_SIZE = (1500, 1050)


def build_card(source, output, title, subtitle):
    image = Image.open(source).convert("RGB")
    if image.size != EXPECTED_SIZE:
        raise ValueError(
            f"Expected {EXPECTED_SIZE[0]} x {EXPECTED_SIZE[1]} artwork (PC-13, 5x3.5in "
            f"@300dpi), got {image.size}: {source}. Illustration art must be regenerated "
            f"or reframed to this size -- do not stretch or force-resize it here."
        )

    draw = ImageDraw.Draw(image)
    center_x = image.width / 2
    title_font, title_spacing = fit_title(draw, title, image.width * 0.88)
    subtitle_font = ImageFont.truetype(SUBTITLE_FONT, 23)
    subtitle_spacing = 4

    # Text positions as a fraction of card height, carried over from the 1536x1024 layout
    # (838/1024, 841/1024, 948/1024) so the title hierarchy looks the same at the new size.
    h = image.height
    draw_spaced_text(draw, center_x + 2, round(h * 0.8213), title, title_font, title_spacing, SHADOW)
    draw_spaced_text(draw, center_x, round(h * 0.8184), title, title_font, title_spacing, PAPER)
    draw_spaced_text(draw, center_x, round(h * 0.9258), subtitle, subtitle_font, subtitle_spacing, PAPER)
    image.save(output, optimize=True)
    print(output)


def main():
    for card in CARDS:
        build_card(*card)


if __name__ == "__main__":
    main()
