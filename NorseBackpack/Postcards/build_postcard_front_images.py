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
        POSTCARDS / "Postcard_L2_Battle_Harbour_Illustration_v2.png",
        POSTCARDS / "Postcard_L2_Battle_Harbour_Front.png",
        "BATTLE HARBOUR",
        "NEWFOUNDLAND AND LABRADOR",
    ),
    (
        POSTCARDS / "Postcard_L3_Baffin_Island_Illustration_v2.png",
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
        POSTCARDS / "Postcard_R6_Roumare_Forest_Illustration_v3.png",
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


def fit_title(draw, text, max_width, k=1.0):
    # k scales the source-pixel sizes to the output (1.2 since the 6 x 4 in card).
    size = round(84 * k)
    while size > 52 * k:
        font = ImageFont.truetype(TITLE_FONT, size)
        spacing = round(size * 0.045)
        if spaced_width(draw, text, font, spacing) <= max_width:
            return font, spacing
        size -= 2
    return ImageFont.truetype(TITLE_FONT, size), round(size * 0.045)


# PC-13: the illustration sources are 5 x 3.5 in (10:7), 1500 x 1050 px at 300 dpi.
SOURCE_SIZE = (1500, 1050)
# 13 Oct 2026 (designer, after playtest 1): the card is now 6 x 4 in (3:2), so the front is
# 1800 x 1200 px. Each source loses 50 rows to become 3:2 (1500 x 1000), then is scaled 1.2x.
# The rows come off the top (plain sky on most cards) and, where the top holds something that
# matters, from inside the navy title band instead, just under its top edge, where a cut can't
# be seen. TOP_TRIM is how many of the 50 come off the top; the rest come out of the band.
OUTPUT_SIZE = (1800, 1200)
TRIM = 50
TOP_TRIM = {
    "Postcard_L1_LAnse_Front.png": 10,             # tip of the sculpture
    "Postcard_L2_Battle_Harbour_Front.png": 0,     # top edge carries the 1576 digits (PZ-002)
    "Postcard_L3_Baffin_Island_Front.png": 0,      # same
    "Postcard_R2_Rouen_Front.png": 36,             # band starts low: needs at least 36 off the top
    "Postcard_R3_Bayeux_Front.png": 19,            # tapestry border along the top
    "Postcard_A2_Hvammur_Front.png": 11,           # cliff reaches the top
    "Postcard_A3_Esjuberg_Front.png": 2,           # painted frame edge along the top
    "Postcard_AD_Bjarnarhofn_Front.png": 8,        # cross on the church (see SCENE_CUT)
}
# AD's band starts too low to give up the rows its cross needs, so a strip of the grass
# foreground just above the band goes instead: (first source row, rows).
SCENE_CUT = {"Postcard_AD_Bjarnarhofn_Front.png": (834, 26)}
# Title and subtitle baselines, measured up from the card's bottom edge in source pixels.
# Unchanged from the 5 x 3.5 card (965 and 1012 on a 1050 px source).
TITLE_FROM_BOTTOM, SUBTITLE_FROM_BOTTOM = 1050 - 965, 1050 - 1012


def find_band_top(image):
    """First row of the plain navy title band: 12 rows in a row that are flat and band-coloured."""
    import numpy as np
    a = np.asarray(image).astype(int)
    ref = a[-8].mean(0)
    flat = [(np.abs(a[r].mean(0) - ref).max() < 25 and a[r].std(0).max() < 30) for r in range(len(a))]
    for r in range(600, len(a) - 12):
        if all(flat[r:r + 12]):
            return r
    raise ValueError("no title band found")


def to_three_two(image, top, scene=None):
    """Drop TRIM rows: `top` off the top edge, any SCENE_CUT strip, the rest from the band."""
    w, h = image.size
    band = TRIM - top
    if scene:
        start, rows = scene
        kept = Image.new("RGB", (w, h - rows))
        kept.paste(image.crop((0, 0, w, start)), (0, 0))
        kept.paste(image.crop((0, start + rows, w, h)), (0, start))
        image, h, band = kept, h - rows, band - rows
    if band:
        cut = find_band_top(image) + 6
        # The title must still fit in the band: its top sits about 60 px above its baseline.
        if cut + band > h - TITLE_FROM_BOTTOM - 70:
            raise ValueError(f"band too short to lose {band} rows")
        kept = Image.new("RGB", (w, h - band))
        kept.paste(image.crop((0, 0, w, cut)), (0, 0))
        kept.paste(image.crop((0, cut + band, w, h)), (0, cut))
        image = kept
    return image.crop((0, top, w, image.height))


def build_card(source, output, title, subtitle):
    image = Image.open(source).convert("RGB")
    if image.size != SOURCE_SIZE:
        raise ValueError(
            f"Expected {SOURCE_SIZE[0]} x {SOURCE_SIZE[1]} artwork (PC-13, 10:7 "
            f"source), got {image.size}: {source}. Illustration art must be regenerated "
            f"or reframed to this size -- do not stretch or force-resize it here."
        )

    if output.name in NEEDS_BAND:
        w, h = image.size
        band_top = round(h * 0.80)
        draw = ImageDraw.Draw(image)
        draw.rectangle((0, band_top, w, h), fill=BAND_NAVY)
        draw.rectangle((0, band_top - 3, w, band_top), fill=BAND_DIVIDER)

    image = to_three_two(image, TOP_TRIM.get(output.name, TRIM), SCENE_CUT.get(output.name))
    image = image.resize(OUTPUT_SIZE, Image.LANCZOS)
    k = OUTPUT_SIZE[0] / SOURCE_SIZE[0]

    draw = ImageDraw.Draw(image)
    center_x = image.width / 2
    title_font, title_spacing = fit_title(draw, title, image.width * 0.88, k)
    subtitle_font = ImageFont.truetype(SUBTITLE_FONT, round(23 * k))
    subtitle_spacing = round(4 * k)

    # Shared baselines: clear the lowest existing divider (AD/RD), retain accent headroom and
    # leave space below Cinzel's descending J. Keep the original illustrated bands unchanged.
    title_y = image.height - TITLE_FROM_BOTTOM * k
    subtitle_y = image.height - SUBTITLE_FROM_BOTTOM * k
    draw_spaced_text(draw, center_x + 2 * k, title_y + 3 * k, title, title_font, title_spacing, SHADOW)
    draw_spaced_text(draw, center_x, title_y, title, title_font, title_spacing, PAPER)
    draw_spaced_text(draw, center_x, subtitle_y, subtitle, subtitle_font, subtitle_spacing, PAPER)
    image.save(output, optimize=True, dpi=(300, 300))
    print(output)


def main():
    for card in CARDS:
        build_card(*card)


if __name__ == "__main__":
    main()
