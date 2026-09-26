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
        POSTCARDS / "Postcard_L1_LAnse_Illustration_v3.png",
        POSTCARDS / "Postcard_L1_LAnse_Front.png",
        "L'ANSE AUX MEADOWS",
        "NEWFOUNDLAND AND LABRADOR",
    ),
    (
        POSTCARDS / "Postcard_L2_Battle_Harbour_Illustration_v1.png",
        POSTCARDS / "Postcard_L2_Battle_Harbour_Front.png",
        "BATTLE HARBOUR",
        "NEWFOUNDLAND AND LABRADOR",
    ),
    (
        POSTCARDS / "Postcard_L3_Baffin_Island_Illustration_v1.png",
        POSTCARDS / "Postcard_L3_Baffin_Island_Front.png",
        "BAFFIN ISLAND",
        "NUNAVUT",
    ),
    (
        POSTCARDS / "Postcard_LD_Brattahlid_Illustration_v1.png",
        POSTCARDS / "Postcard_LD_Brattahlid_Front.png",
        "BRATTAHLÍÐ",
        "GREENLAND",
    ),
    (
        POSTCARDS / "Postcard_R1_Chalus_Illustration_v2.png",
        POSTCARDS / "Postcard_R1_Chalus_Front.png",
        "CHÂLUS",
        "HAUTE-VIENNE",
    ),
    (
        POSTCARDS / "Postcard_R2_Rouen_Illustration_v1.png",
        POSTCARDS / "Postcard_R2_Rouen_Front.png",
        "ROUEN",
        "NORMANDY",
    ),
    (
        POSTCARDS / "Postcard_R3_Bayeux_Illustration_v1.png",
        POSTCARDS / "Postcard_R3_Bayeux_Front.png",
        "BAYEUX",
        "NORMANDY",
    ),
    (
        POSTCARDS / "Postcard_R4_Winchester_Illustration_v1.png",
        POSTCARDS / "Postcard_R4_Winchester_Front.png",
        "WINCHESTER",
        "ENGLAND",
    ),
    (
        POSTCARDS / "Postcard_R5_Battle_Illustration_v1.png",
        POSTCARDS / "Postcard_R5_Battle_Front.png",
        "BATTLE",
        "EAST SUSSEX",
    ),
    (
        POSTCARDS / "Postcard_R6_Roumare_Forest_Illustration_v2.png",
        POSTCARDS / "Postcard_R6_Roumare_Forest_Front.png",
        "ROUMARE FOREST",
        "NORMANDY",
    ),
    (
        POSTCARDS / "Postcard_RD_Walcheren_Illustration_v1.png",
        POSTCARDS / "Postcard_RD_Walcheren_Front.png",
        "WALCHEREN",
        "NETHERLANDS",
    ),
    (
        POSTCARDS / "Postcard_A1_Dogurdarnes_Illustration_v1.png",
        POSTCARDS / "Postcard_A1_Dogurdarnes_Front.png",
        "DÖGURÐARNES",
        "ICELAND",
    ),
    (
        POSTCARDS / "Postcard_A2_Hvammur_Illustration_v1.png",
        POSTCARDS / "Postcard_A2_Hvammur_Front.png",
        "HVAMMUR",
        "ICELAND",
    ),
    (
        POSTCARDS / "Postcard_A3_Esjuberg_Illustration_v1.png",
        POSTCARDS / "Postcard_A3_Esjuberg_Front.png",
        "ESJUBERG",
        "ICELAND",
    ),
    (
        POSTCARDS / "Postcard_AD_Bjarnarhofn_Illustration_v1.png",
        POSTCARDS / "Postcard_AD_Bjarnarhofn_Front.png",
        "BJARNARHÖFN",
        "ICELAND",
    ),
    (
        POSTCARDS / "Postcard_H1_Oslo_Illustration_v1.png",
        POSTCARDS / "Postcard_H1_Oslo_Front.png",
        "OSLO",
        "NORWAY",
    ),
    (
        POSTCARDS / "Postcard_H2_Staraya_Ladoga_Illustration_v1.png",
        POSTCARDS / "Postcard_H2_Staraya_Ladoga_Front.png",
        "STARAYA LADOGA",
        "RUSSIA",
    ),
    (
        POSTCARDS / "Postcard_H3_Kyiv_Illustration_v1.png",
        POSTCARDS / "Postcard_H3_Kyiv_Front.png",
        "KYIV",
        "UKRAINE",
    ),
    (
        POSTCARDS / "Postcard_H4_Hedeby_Illustration_v1.png",
        POSTCARDS / "Postcard_H4_Hedeby_Front.png",
        "HEDEBY",
        "GERMANY",
    ),
    (
        POSTCARDS / "Postcard_H5_Sicily_Illustration_v1.png",
        POSTCARDS / "Postcard_H5_Sicily_Front.png",
        "SICILY",
        "ITALY",
    ),
    (
        POSTCARDS / "Postcard_H6_Patara_Illustration_v1.png",
        POSTCARDS / "Postcard_H6_Patara_Front.png",
        "PATARA",
        "TURKEY",
    ),
    (
        POSTCARDS / "Postcard_HD_Constantinople_Illustration_v1.png",
        POSTCARDS / "Postcard_HD_Constantinople_Front.png",
        "CONSTANTINOPLE",
        "TURKEY",
    ),
]

# PC-19: these six illustration sources were generated full-bleed, with no blank title band
# reserved the way every other card's source has one -- their own ImageGen prompts even said
# "the title band will be added separately," but that compositing step never ran. Painting the
# band here, once, for exactly these six, rather than changing build_card() unconditionally for
# every card and risking a slightly different navy shade on the sixteen that are already correct.
NEEDS_BAND = {
    "Postcard_H2_Staraya_Ladoga_Front.png",
    "Postcard_H3_Kyiv_Front.png",
    "Postcard_H4_Hedeby_Front.png",
    "Postcard_H5_Sicily_Front.png",
    "Postcard_H6_Patara_Front.png",
    "Postcard_HD_Constantinople_Front.png",
}
# Sampled from the existing correctly-built cards' own bands (e.g. L1, H1) rather than invented.
BAND_NAVY = (18, 52, 60)
BAND_DIVIDER = (235, 226, 185)


def spaced_width(draw, text, font, spacing):
    return sum(draw.textlength(char, font=font) for char in text) + spacing * (len(text) - 1)


def draw_spaced_text(draw, center_x, y, text, font, spacing, fill):
    # Centre the actual ink bounds; put every glyph on one baseline. The old
    # per-character top anchor lowered accented letters and raised the J tail.
    cursor = 0
    bounds = []
    for char in text:
        left, top, right, bottom = font.getbbox(char, anchor="ls")
        bounds.append((cursor + left, cursor + right))
        cursor += draw.textlength(char, font=font) + spacing
    x = center_x - (min(b[0] for b in bounds) + max(b[1] for b in bounds)) / 2
    for char in text:
        draw.text((x, y), char, font=font, fill=fill, anchor="ls")
        x += draw.textlength(char, font=font) + spacing


def fit_title(draw, text, max_width):
    size = 84
    while size > 52:
        font = ImageFont.truetype(TITLE_FONT, size)
        spacing = round(size * 0.045)
        if spaced_width(draw, text, font, spacing) <= max_width:
            return font, spacing
        size -= 2
    return ImageFont.truetype(TITLE_FONT, size), round(size * 0.045)


# PC-13: card is 5 x 3.5 in (10:7). At 300 dpi that is 1500 x 1050 px -- matches
# build_postcard_L1_pdf.py's PAGE exactly, so no aspect distortion at draw time.
EXPECTED_SIZE = (1500, 1050)


def build_card(source, output, title, subtitle):
    image = Image.open(source).convert("RGB")
    if image.size != EXPECTED_SIZE:
        raise ValueError(
            f"Expected {EXPECTED_SIZE[0]} x {EXPECTED_SIZE[1]} artwork (PC-13, 5x3.5in "
            f"@300dpi), got {image.size}: {source}. Illustration art must be regenerated "
            f"or reframed to this size -- do not stretch or force-resize it here."
        )

    if output.name in NEEDS_BAND:
        w, h = image.size
        band_top = round(h * 0.80)
        draw = ImageDraw.Draw(image)
        draw.rectangle((0, band_top, w, h), fill=BAND_NAVY)
        draw.rectangle((0, band_top - 3, w, band_top), fill=BAND_DIVIDER)

    draw = ImageDraw.Draw(image)
    center_x = image.width / 2
    title_font, title_spacing = fit_title(draw, title, image.width * 0.88)
    subtitle_font = ImageFont.truetype(SUBTITLE_FONT, 23)
    subtitle_spacing = 4

    # Shared baselines at 300 dpi: clear the lowest existing divider (AD/RD),
    # retain accent headroom and leave space below Cinzel's descending J.
    # Keep the original illustrated bands and all scenery unchanged.
    draw_spaced_text(draw, center_x + 2, 965, title, title_font, title_spacing, SHADOW)
    draw_spaced_text(draw, center_x, 962, title, title_font, title_spacing, PAPER)
    draw_spaced_text(draw, center_x, 1012, subtitle, subtitle_font, subtitle_spacing, PAPER)
    image.save(output, optimize=True, dpi=(300, 300))
    print(output)


def main():
    for card in CARDS:
        build_card(*card)


if __name__ == "__main__":
    main()
