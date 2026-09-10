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
        POSTCARDS / "Postcard_02_Baffin_Island_Illustration_v1.png",
        POSTCARDS / "Postcard_02_Baffin_Island_Front.png",
        "BAFFIN ISLAND",
        "NUNAVUT",
    ),
    (
        POSTCARDS / "Postcard_03_Battle_Harbour_Illustration_v1.png",
        POSTCARDS / "Postcard_03_Battle_Harbour_Front.png",
        "BATTLE HARBOUR",
        "NEWFOUNDLAND AND LABRADOR",
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


def build_card(source, output, title, subtitle):
    image = Image.open(source).convert("RGB")
    if image.size != (1536, 1024):
        raise ValueError(f"Expected 1536 x 1024 artwork, got {image.size}: {source}")

    draw = ImageDraw.Draw(image)
    center_x = image.width / 2
    title_font, title_spacing = fit_title(draw, title, image.width * 0.88)
    subtitle_font = ImageFont.truetype(SUBTITLE_FONT, 23)
    subtitle_spacing = 4

    # Text positions match the established L'Anse aux Meadows title hierarchy.
    draw_spaced_text(draw, center_x + 2, 841, title, title_font, title_spacing, SHADOW)
    draw_spaced_text(draw, center_x, 838, title, title_font, title_spacing, PAPER)
    draw_spaced_text(draw, center_x, 948, subtitle, subtitle_font, subtitle_spacing, PAPER)
    image.save(output, optimize=True)
    print(output)


def main():
    for card in CARDS:
        build_card(*card)


if __name__ == "__main__":
    main()
