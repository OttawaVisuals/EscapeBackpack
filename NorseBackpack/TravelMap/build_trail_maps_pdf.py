"""Build the printable trail maps (letter, portrait), one per trail.

Style B from the design discussion: flat screen-print poster, limited palette shared with the
postcards. Stops are deliberately NOT marked (PZ-06) -- players locate the places their postcards
name among the other labels, then draw the legs themselves on the laminated sheet.

Geometry  : Natural Earth 50m land polygons, vendored offline at vendor/land.js (public domain).
Labels    : drawn from stops.js, the 72-entry research corpus, so every settlement label carries a
            coordinate that is already part of the project's sourced dataset rather than typed
            from memory. Curated extras are marked APPROX below and are NOT source-checked.
Projection: Lambert conformal conic, standard parallels fitted per trail.
Grid      : a 9 x 11 lettered/numbered reference grid, A-I across and 1-11 down. It is a property
            of the SHEET, not the frame, so all four maps carry the identical grid and a square
            reference means the same place on the page every time. It divides the map area exactly,
            so there are no runt half-cells. It replaces the old degree graticule.
Framing   : explicit per-trail frames. Auto-fitting the stop box to the sheet aspect was tried
            and rejected -- it zoomed out to show far more empty ocean than the trail needs.

Usage: python build_trail_maps_pdf.py [leif|rollo|aud|...]   (default: every unblocked trail)
"""

import json
import math
from io import BytesIO
import re
import sys
from pathlib import Path

from pyproj import CRS, Transformer

import aud_layer
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FONT_DIR = ROOT / "Fonts"
OUT_DIR = ROOT / "output" / "pdf"
SOURCE_ART_DIR = HERE / "Art"
ART_DIR = SOURCE_ART_DIR / "processed"  # Leif's alpha-hole-filled derivatives

# PZ-09: Harald's map gets a second page, the hnefatafl board-setup panel composited
# onto its back, so the two print as one physical laminated sheet rather than two loose
# pieces of paper. Reuses the insert's own drawing code and palette (shared with the
# tickets, per board_layout.py) rather than duplicating it.
sys.path.insert(0, str(ROOT / "NorseBackpack" / "Props" / "Hnefatafl"))
from build_board_setup_pdf import draw_grid as _draw_hnefatafl_board_setup, W as _BOARD_W, H as _BOARD_H

SEA      = HexColor("#DCE7E4")
LAND_C   = HexColor("#EFE3C4")
COAST    = HexColor("#59635D")
INK      = HexColor("#283B34")
INK_SOFT = HexColor("#59635D")
RUST     = HexColor("#B56A2A")
TEAL     = HexColor("#2F7775")
TAN      = HexColor("#C0B291")
WHITE    = HexColor("#FFFFFF")

for alias, rel in (
    ("Cinzel",   "Cinzel/static/Cinzel-Regular.ttf"),
    ("CinzelBold", "Cinzel/static/Cinzel-Bold.ttf"),
    ("CinzelXB", "Cinzel/static/Cinzel-ExtraBold.ttf"),
    ("Plex",     "IBM_Plex_Mono/IBMPlexMono-Regular.ttf"),
    ("PlexIt",   "IBM_Plex_Mono/IBMPlexMono-Italic.ttf"),
):
    pdfmetrics.registerFont(TTFont(alias, str(FONT_DIR / rel)))

PAGE_W, PAGE_H = letter
# Margin sized to the printer's own non-printable area, each plus a 0.5mm safety pad. First read
# from Hiking_Trip/Support.xlsx's Canon citation (top 3mm, side 3.4mm, bottom 16.7mm), which
# undersized the sides and caused the print driver to visibly rescale/recentre the page. The
# user's corrected, per-edge reading: top 3.0mm, bottom 16.7mm, left 6.4mm, right 6.3mm -- kept
# as two distinct side values rather than averaged, since the user re-supplied them separately a
# second time.
# 20 Sept 2026: first pass used the largest of the four on every side for an even-looking border;
# the user then asked to use the print area right up to each side's own real minimum instead, to
# maximise the map -- accepting that the printed border is no longer even (thin on three sides,
# thick at the bottom, which is the printer's own non-printable zone there, not this file's
# choice).
MARGIN_TOP = 3.5 / 25.4 * 72
MARGIN_LEFT = 6.9 / 25.4 * 72
MARGIN_RIGHT = 6.8 / 25.4 * 72
MARGIN_BOTTOM = 17.2 / 25.4 * 72
NEAT = (MARGIN_LEFT, MARGIN_BOTTOM, PAGE_W - MARGIN_RIGHT, PAGE_H - MARGIN_TOP)
TITLE_H = 0.62 * 72
BAND = 12.0                   # border band carrying the grid letters and numbers
GRID_COLS, GRID_ROWS = 9, 11  # exact division of the map area; cells 0.84 x 0.86 in
MX0, MY0 = NEAT[0] + BAND, NEAT[1] + TITLE_H + BAND
MX1, MY1 = NEAT[2] - BAND, NEAT[3] - BAND
BAND_Y0 = NEAT[1] + TITLE_H   # bottom of the band ring = top of the title band

# ---------------------------------------------------------------- trail config
# "regions" carry a Norse name over a modern one; "areas" are modern-only, in lighter italic,
# so the two-name treatment stays meaningful instead of decorative.
TRAILS = {
    "leif": dict(
        n=1, title="THE WESTERN LANDS", sub="Leif's trail", band="#216580",
        # Frame shifted one grid column east from the original (PR-13): trims the empty
        # Nunavik/Ungava Bay/Quebec mass on the west, brings Greenland's coast fully into view.
        # Same scale as before the shift -- this is a pan, not a zoom. Qikiqtarjuaq (Leif's own
        # Helluland stop, lon -64.03) still lands 1.83 in inside the new west edge: the region
        # label's plain lon/lat bounds check is a conservative proxy and would have flagged this
        # as unsafe, but the conic projection's meridian convergence at 67.6 deg N keeps the
        # actual point well inside. Verified by projecting it, not by relaxing the guard.
        parallels=(52, 66), lon0=-50.3, frame=(-63.56, -37.06, 46.0, 70.5),
        regions=[("HELLULAND", "Baffin Island", 68.5, -70.0),
                 ("MARKLAND", "Labrador", 54.4, -61.0),
                 ("VINLAND", "Newfoundland", 48.0, -56.4),
                 ("GRŒNLAND", "Greenland", 64.0, -46.0)],
        areas=[],
        waters=[("LABRADOR SEA", 57.5, -53.0, -30), ("DAVIS STRAIT", 64.2, -57.0, -38),
                ("GULF OF\nST. LAWRENCE", 48.6, -61.0, 0), ("ATLANTIC\nOCEAN", 48.6, -45.0, 0)],
        # APPROX -- typed from general knowledge, not source-checked. See PR-10.
        extra_towns=[("St. Anthony", 51.37, -55.59), ("Corner Brook", 48.95, -57.95),
                     ("Gander", 48.96, -54.61), ("St. John's", 47.56, -52.71),
                     ("Twillingate", 49.65, -54.77), ("Port aux Basques", 47.57, -59.14),
                     ("Red Bay", 51.73, -56.43), ("Cartwright", 53.71, -57.00),
                     ("Rigolet", 54.18, -58.43), ("Happy Valley-Goose Bay", 53.30, -60.33),
                     ("Makkovik", 55.09, -59.17), ("Hopedale", 55.45, -60.22),
                     ("Nain", 56.54, -61.69), ("Blanc-Sablon", 51.42, -57.13),
                     ("Natashquan", 50.19, -61.82), ("Sept-Îles", 50.22, -66.38),
                     ("Kimmirut", 62.85, -69.87), ("Iqaluit", 63.75, -68.52),
                     ("Pangnirtung", 66.15, -65.71), ("Nuuk", 64.18, -51.72),
                     ("Sisimiut", 66.94, -53.67), ("Paamiut", 61.99, -49.67),
                     ("Narsarsuaq", 61.16, -45.43), ("Qaqortoq", 60.72, -46.03)],
    ),
    "rollo": dict(
        n=2, title="THE GRANTED LANDS", sub="Rollo & descendants", band="#A2562D",
        parallels=(45, 52), lon0=0, frame=(-5.0, 4.0, 43.5, 53.5),
        regions=[("FRAKKLAND", "France", 46.9, 2.1), ("ENGLAND", "", 52.1, -1.6)],
        areas=[("Normandy", 49.0, 0.2), ("Brittany", 48.1, -2.6), ("Wessex", 51.1, -2.4)],
        waters=[("THE CHANNEL", 50.0, -1.4, -14), ("BAY OF\nBISCAY", 45.2, -2.6, 0),
                ("NORTH SEA", 52.6, 2.4, 0)],
        # APPROX -- typed from general knowledge, not source-checked. See PR-10.
        extra_towns=[("Cherbourg", 49.64, -1.62), ("Le Havre", 49.49, 0.11),
                     ("Dieppe", 49.92, 1.08), ("Coutances", 49.05, -1.44),
                     ("Avranches", 48.68, -1.36), ("Évreux", 49.02, 1.15),
                     ("Alençon", 48.43, 0.09), ("Le Mans", 48.00, 0.20),
                     ("Tours", 47.39, 0.69), ("Poitiers", 46.58, 0.34),
                     ("Limoges", 45.83, 1.26), ("Angoulême", 45.65, 0.16),
                     ("Nantes", 47.22, -1.55), ("Rennes", 48.11, -1.68),
                     ("Saint-Malo", 48.65, -2.03), ("Amiens", 49.89, 2.30),
                     ("Calais", 50.95, 1.86), ("Boulogne", 50.73, 1.61),
                     ("Orléans", 47.90, 1.91), ("Canterbury", 51.28, 1.08),
                     ("Dover", 51.13, 1.31), ("Southampton", 50.90, -1.40),
                     ("Portsmouth", 50.80, -1.09), ("Salisbury", 51.07, -1.79),
                     ("Oxford", 51.75, -1.26), ("Chichester", 50.84, -0.78),
                     ("Lewes", 50.87, 0.01), ("Exeter", 50.72, -3.53)],
    ),
    "aud": dict(
        n=3, title="THE ISLAND SETTLEMENT", sub="Aud the Deep-Minded", band="#6D528B",
        parallels=(64, 66), lon0=-22,
        # ZOOM_FRAME. Must stay identical to export_aud_base.py's: aud_features.json stores
        # page points, so the drawn layer only lines up with the coastline at this frame.
        frame=(-22.9751, -20.5451, 64.08, 65.37),
        regions=[("ÍSLAND", "Iceland", 64.72, -20.75)],
        # Repositioned for the zoomed frame. Breiðafjörður ran off the west edge at its old
        # spot and now sits out in the bay; Snæfellsnes and DENMARK STRAIT are dropped because
        # both project well off this sheet -- the peninsula and the strait are simply not on it
        # any more. They are still correct for the old wide frame if it is ever restored.
        areas=[("Breiðafjörður", 65.34, -22.33), ("Dalir", 65.16, -21.40),
               ("Kjalarnes", 64.28, -21.70)],
        # Moved south-east: at 64.45,-22.80 it printed across the legend box.
        waters=[("FAXAFLÓI", 64.242, -22.108, 0)],
        # APPROX -- typed from general knowledge, not source-checked. See PR-10.
        extra_towns=[("Reykjavík", 64.15, -21.94), ("Akranes", 64.32, -22.08),
                     ("Borgarnes", 64.54, -21.92), ("Búðardalur", 65.11, -21.76),
                     ("Stykkishólmur", 65.07, -22.73), ("Grundarfjörður", 64.92, -23.25),
                     ("Ólafsvík", 64.89, -23.71), ("Hellissandur", 64.91, -23.90),
                     ("Reykholt", 64.66, -21.29), ("Mosfellsbær", 64.17, -21.68),
                     ("Hafnarfjörður", 64.07, -21.94)],
    ),
    "harald": dict(
        # Title is a draft pick, not yet confirmed with the user -- "Eastward & back again"
        # is the theme already recorded in stops.js; this titles it after his most famous
        # historical role. Continent-spanning trail (Norway to Ukraine to Sicily to eastern
        # Anatolia), so the frame is necessarily far more zoomed out than the other three
        # sheets -- a much coarser km-per-square is an accepted, not overlooked, consequence.
        n=4, title="THE VARANGIAN ROAD", sub="Harald Hardrada", band="#467444",
        parallels=(40, 58), lon0=22.0, frame=(2.0, 42.0, 34.0, 62.0),
        regions=[],
        areas=[],
        waters=[],
        extra_towns=[],
        # Harald-only grid override (PZ-02 x PZ-09): the branch-rune puzzle's reading order
        # comes from spelling RAVEN against the column letters, so this sheet's columns are
        # relettered A,C,E,I,K,N,R,T,V instead of the shared A-I run. The other three trail
        # sheets keep the plain alphabet -- their own grid references already depend on it.
        col_letters=["A", "C", "E", "I", "K", "N", "R", "T", "V"],
    ),
}

BLOCKED = {}

# Decorative vignettes approved for Leif's sheet (PR-11), re-placed for the PR-13 frame. The
# three sea pieces sit inside the placement guide's re-run rectangles (build_art_placement_guide.py
# leif). The land pieces were placed by a search, not by eye: maximise clearance from the printed
# coastline, then require the candidate box to miss every OTHER reserved box from a clean build
# (every stop, town, region and water label -- not just a distance-from-point heuristic, which
# first missed a real collision between the wolf and "MARKLAND"). The longship was also shrunk
# from its first pass (2.36 x 1.61 in) to 1.70 x 0.85 in: it was crowding the Labrador Sea.
# Rescaled 20 Sept 2026, twice: once for the printer-margin fix (even-padding pass), then again
# when the user chose to maximise the map area with each side at its own true minimum margin
# instead. Both rescales are the same exact transform -- every box is its previous position/size
# scaled about the map's own centre (which now also moved vertically, since the asymmetric
# top/bottom margins no longer share a common page centre with left/right) -- not a re-placement.
# Grid-cell slot comments below refer to the ORIGINAL grid and are kept for provenance only.
LEIF_ART = (
    ("Leif_Longship_v1.png",   (415.06, 207.68, 119.62, 59.81), 0.72),  # slot A
    ("Leif_Whale_v1.png",      (268.67, 320.94, 105.55, 70.36), 0.68),  # slot B
    ("Leif_Iceberg_v1.png",    (473.50, 502.80,  91.47, 66.84), 0.64),  # slot D
    ("Leif_Polar_Bear_v1.png", (341.70, 718.37,  46.91, 43.00), 0.62),  # F1
    ("Leif_Seal_v1.png",       (223.40, 718.37,  46.91, 43.00), 0.62),  # D1
    ("Leif_Hare_v1.png",       ( 45.92, 597.52,  46.91, 43.00), 0.62),  # A3
    ("Leif_Deer_v1.png",       (400.86, 657.94,  46.91, 43.00), 0.62),  # G2
    ("Leif_Loon_v1.png",       (105.08, 476.67,  46.91, 43.00), 0.62),  # B5
    ("Leif_Wolf_v1.png",       ( 45.92, 416.24,  46.91, 43.00), 0.62),  # A6
    ("Leif_Orca_v1.png",       (400.86, 355.81,  46.91, 43.00), 0.62),  # G7
    ("Leif_Settlement_v1.png", (325.55, 605.31,  56.68, 35.19), 0.62),  # W. Greenland, 4.1deg clear
)

# Rollo's seven rust-brown story vignettes. Each 38pt square gives the normalized artwork an
# actual visible width of at most about 0.43in after the closer-placement revision. Positions
# use compact boxes so each vignette can sit beside its associated stop while
# remaining clear of town dots, the answer-route stroke and fixed labels.
# Battle and Hastings share one longship.
# Rescaled 20 Sept 2026, twice (see LEIF_ART above) -- same exact transform.
ROLLO_ART = (
    ("Rollo_Crossbow_Bolt_v1.png", (371.48, 198.98, 37.13, 37.13), 0.62),  # Chalus
    ("Rollo_Treaty_Scroll_v1.png", (370.49, 458.92, 37.13, 37.13), 0.62),  # Saint-Clair-sur-Epte
    ("Rollo_Ducal_Coronet_v1.png", (391.03, 499.00, 37.13, 37.13), 0.62),  # Rouen
    ("Rollo_Needle_Thread_v1.png", (259.09, 446.22, 37.13, 37.13), 0.62),  # Bayeux
    ("Rollo_Crown_v1.png", (281.57, 611.37, 37.13, 37.13), 0.62),          # Winchester
    ("Rollo_Longship_v1.png", (304.04, 545.90, 37.13, 37.13), 0.62),       # Battle / Hastings
    ("Rollo_Boar_v1.png", (323.59, 508.76, 37.13, 37.13), 0.62),           # Roumare forest
)

# Word-lock puzzle vignettes (PZ-15, concept stage): six icons, each somewhere inside its named
# grid cell -- unlike ROLLO_ART above, these ARE the puzzle's answer squares, not scenery placed
# near a real stop. Each box is offset by a different random amount within its cell (never
# centred -- six identically-centred icons read as a deliberate grid overlay, not scenery) while
# staying fully inside the cell bounds.
# Word order fixed by the order the words were chosen in chat: beef, poultry, combat, forest,
# tavern, people -- matched 1:1 against the given grid refs D1, I3, H6, E7, H9, F11.
# Rescaled 20 Sept 2026, twice (see LEIF_ART above) -- same exact transform.
ROLLO_WORDLOCK_ART = (
    ("Rollo_Cow_v1.png",    (220.57, 727.12, 37.13, 37.13), 0.62),  # beef    -> D1
    ("Rollo_Hen_v1.png",    (528.46, 593.46, 37.13, 37.13), 0.62),  # poultry -> I3
    ("Rollo_Combat_v1.png", (461.60, 420.33, 37.13, 37.13), 0.62),  # combat  -> H6
    ("Rollo_Forest_v1.png", (295.13, 356.41, 37.13, 37.13), 0.62),  # forest  -> E7
    ("Rollo_Inn_v1.png",    (456.09, 247.22, 37.13, 37.13), 0.62),  # tavern  -> H9
    ("Rollo_Folk_v1.png",   (348.80, 107.72, 37.13, 37.13), 0.62),  # people  -> F11
)

# Harald's branch-rune reference grid (PZ-02 x PZ-09): five real stems, each a group/position
# pair (left branches = group 1-3, right branches = position within it -- see the Props & specs
# "Branch runes" section), decoding to H R A F N. The cell each sits in is chosen so that reading
# the relettered columns (see col_letters above) in the literal order RAVEN spells -- R, A, V, E,
# N -- visits them in H, R, A, F, N order, the cryptex answer. Seven decoys elsewhere on the
# sheet carry plausible but meaningless group/position pairs so the five real cells cannot be
# spotted by pattern alone; col_idx is 0-based (0=A .. 8=I in the ORIGINAL, unrelettered index),
# row is 1-based from the top, matching the shared GRID_COLS x GRID_ROWS reference grid.
HARALD_RUNES_REAL = (
    (6, 6, 2, 1, "H"),   # G6  -> relettered R6
    (0, 10, 1, 5, "R"),  # A10 -> relettered A10
    (8, 9, 2, 4, "A"),   # I9  -> relettered V9
    (2, 3, 1, 1, "F"),   # C3  -> relettered E3
    (5, 2, 2, 2, "N"),   # F2  -> relettered N2
)
HARALD_RUNES_DECOY = (
    (1, 4, 3, 3),
    (3, 9, 1, 2),
    (4, 2, 2, 5),
    (4, 10, 3, 1),
    (7, 4, 1, 6),
    (7, 8, 2, 3),
    (2, 7, 3, 4),
)



# The cache mark (PZ-03, 24 Sept 2026): the fehu rune beside the treasure cave at I9, the end
# of the ticket's route. It matches the Norse group's icon in the ticket's Coin Room key and so
# selects that pile of the loose hoard. Placed left of the cave: the neat line is 10 pt to its
# right and the road 21 pt above. Same shape as draw_fehu() in Props/AudTicket.
# Decoy marks, same day: the ticket's other two group icons sit at the two caves a wrong route
# would plausibly end at, so a misread route selects a wrong pile (980 or 1320, not a word).
#   G1 camel -- by the H2 ruin and wood, near the lookalike "village at the crossing" (G3).
#   C4 fleur-de-lis -- in the wood by the B5 ruin, the same ruin-and-wood pattern.
# The E7 and I4 caves stay unmarked: no ruin near them, so no plausible route ends there.
AUD_TREASURE_CAVE = (570.178, 248.18)
AUD_CACHE_MARK = (553.0, 247.0, 12.0)      # x, y, height
AUD_DECOY_MARKS = [("camel", 468.0, 724.0, 12.0), ("fleur", 140.0, 582.0, 12.0)]
AUD_ICON_DIR = ROOT / "NorseBackpack" / "Props" / "AudTicket" / "icons"
AUD_PAPER, AUD_PURPLE = "#F4EEDD", "#6D528B"


def _aud_icon(name):
    """Ticket icon recoloured to Aud purple over a paper-coloured halo, like the fehu mark."""
    from PIL import Image, ImageFilter
    src = Image.open(AUD_ICON_DIR / f"{name}.png").getchannel("A")
    pad = 24
    a = Image.new("L", (src.width + 2 * pad, src.height + 2 * pad), 0)
    a.paste(src, (pad, pad))
    halo = a.filter(ImageFilter.MaxFilter(25))
    out = Image.new("RGBA", a.size, (0, 0, 0, 0))
    out.paste(Image.new("RGBA", a.size, AUD_PAPER), mask=halo)
    out.paste(Image.new("RGBA", a.size, AUD_PURPLE), mask=a)
    return ImageReader(out), a.size, pad


def draw_aud_cache_mark(c):
    x, y, h = AUD_CACHE_MARK
    sx = x - 0.2 * h
    strokes = [((sx, y - h / 2), (sx, y + h / 2)),
               ((sx, y + 0.12 * h), (sx + 0.42 * h, y + 0.46 * h)),
               ((sx, y - 0.14 * h), (sx + 0.46 * h, y + 0.16 * h))]
    c.saveState()
    c.setLineCap(1)
    for colour, width in ((AUD_PAPER, 3.2), (AUD_PURPLE, 1.5)):   # paper halo, then Aud purple
        c.setStrokeColor(HexColor(colour))
        c.setLineWidth(width)
        for (x1, y1), (x2, y2) in strokes:
            c.line(x1, y1, x2, y2)
    for name, ix, iy, ih in AUD_DECOY_MARKS:
        img, (w, hgt), pad = _aud_icon(name)
        scale = ih / (hgt - 2 * pad)
        c.drawImage(img, ix - w * scale / 2, iy - hgt * scale / 2, w * scale, hgt * scale,
                    mask="auto")
    c.restoreState()


def cell_center(col_idx, row):
    """Page-space centre of grid cell (col_idx 0-based, row 1-based from the top)."""
    cw, ch = (MX1 - MX0) / GRID_COLS, (MY1 - MY0) / GRID_ROWS
    return MX0 + (col_idx + 0.5) * cw, MY1 - (row - 0.5) * ch


def draw_harald_board_back(c):
    """PZ-09: page 2 of Harald's sheet -- the hnefatafl board-setup insert, centred on
    the same letter page and background tone as the front, so lamination produces one
    physical object with the rune cipher on one face and the game setup on the other."""
    c.setFillColor(LAND_C)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    c.saveState()
    c.translate((PAGE_W - _BOARD_W) / 2, (PAGE_H - _BOARD_H) / 2)
    _draw_hnefatafl_board_setup(c)
    c.restoreState()


def draw_rune_stem(c, x, y, group, position):
    """One branch-rune stem (kvistrunir): a vertical stroke with tally ticks -- left branches
    count the group (1-3), right branches count the position within it (PZ-02)."""
    c.saveState()
    c.setStrokeColor(INK)
    c.setLineWidth(1.1)
    c.setLineCap(1)
    half = 9.0
    c.line(x, y - half, x, y + half)
    step = 2 * half / 6
    top = y + half - step * 0.6
    for i in range(group):
        ty = top - i * step
        c.line(x, ty, x - 6.5, ty - 3.6)
    for i in range(position):
        ty = top - i * step
        c.line(x, ty, x + 6.5, ty - 3.6)
    c.restoreState()


# Superseded 17 Sept 2026, then shelved: Aud briefly had a landscape two-panel sheet with a
# zoomed Dalir/Hvammur survey panel beside the main map (AUD_DETAIL_ART, then AUD_PANEL and a
# plot-number route).  The whole approach is parked under
# NorseBackpack/Drafts/2026-09-17_Aud_split_panel/ -- see its README.  Aud's sheet is a plain
# portrait map again, and its treasure hunt is being redesigned to live on that single map.


def draw_vignette(c, path, box, alpha):
    """Fit one transparent PNG inside a page-space box without stretching it."""
    x, y, w, h = box
    image = ImageReader(str(path))
    iw, ih = image.getSize()
    scale = min(w / iw, h / ih)
    dw, dh = iw * scale, ih * scale
    c.saveState()
    c.setFillAlpha(alpha)
    c.drawImage(image, x + (w - dw) / 2, y + (h - dh) / 2,
                width=dw, height=dh, mask="auto")
    c.restoreState()


def load_corpus():
    """Point-like places from the research corpus. Broad regional anchors are skipped --
    they cannot be labelled as a dot without asserting a position the dataset disclaims."""
    js = (HERE / "stops.js").read_text(encoding="utf-8")
    rows = re.findall(
        r"\['([a-z0-9-]+)','([a-z]+)','([^']*)',(-?[0-9.]+),(-?[0-9.]+),'([^']*)','([^']*)'", js)
    skip = ("Regional anchor", "Island anchor", "District anchor", "Forest anchor")
    out = []
    for _id, _person, name, lat, lng, _ev, prec in rows:
        if prec in skip:
            continue
        out.append((name.split(" · ")[0], float(lat), float(lng)))
    return out


def load_plan():
    p = HERE / "Norse_Aunt_Route_Plan.json"
    return json.loads(p.read_text(encoding="utf-8"))


class Labeller:
    def __init__(self):
        self.boxes, self.skipped = [], []

    @staticmethod
    def _hit(a, b):
        return not (a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1])

    def reserve(self, x0, y0, x1, y1):
        self.boxes.append((x0, y0, x1, y1))

    def reserve_centred(self, x, y, w, h, pad=2.0):
        self.reserve(x - w / 2 - pad, y - h / 2 - pad, x + w / 2 + pad, y + h / 2 + pad)

    def reserve_polyline(self, pts, radius=2.2, step=4.0):
        """Reserve small boxes along linework without blocking its whole bounding rectangle."""
        for a, b in zip(pts, pts[1:]):
            dx, dy = b[0] - a[0], b[1] - a[1]
            length = math.hypot(dx, dy)
            count = max(1, int(math.ceil(length / step)))
            for i in range(count + 1):
                t = i / count
                x, y = a[0] + dx * t, a[1] + dy * t
                self.reserve(x - radius, y - radius, x + radius, y + radius)

    def place(self, name, x, y, font, size, pad=1.4):
        w = pdfmetrics.stringWidth(name, font, size)
        h = size * 0.86
        for dx, dy in ((4.4, -h / 2), (-w - 4.4, -h / 2),
                       (-w / 2, 5.4), (-w / 2, -h - 5.4),
                       (4.0, 3.8), (4.0, -h - 3.8), (-w - 4.0, 3.8), (-w - 4.0, -h - 3.8),
                       (8.0, -h / 2), (-w - 8.0, -h / 2),
                       (-w / 2, 9.0), (-w / 2, -h - 9.0),
                       # Last-resort tier, added for the printer-margin fix: Aud's sheet is
                       # zoomed tight enough (PZ-17) that a long compound name (e.g. "Dögurðarnes
                       # / Dagverðarnes") could run out of the 12 close-in candidates once the
                       # map area shrank. Same centred-above/below shape, just further out.
                       (-w / 2, 19.4), (-w / 2, -h - 19.4)):
            box = (x + dx - pad, y + dy - pad, x + dx + w + pad, y + dy + h + pad)
            if any(self._hit(box, b) for b in self.boxes):
                continue
            self.boxes.append(box)
            return x + dx, y + dy
        self.skipped.append(name)
        return None


# Plotted-position nudges, applied to the drawing only -- stops.js keeps the real coordinate.
#
# The vendored coastline is Natural Earth 50m, generalised to a few kilometres. That is fine on
# the other three sheets; Aud's is zoomed to about 211 m per point, where it is not. Dogurdarnes
# is a headland in Breidafjordur, and at 1:50m the peninsula it sits on does not exist -- its
# real locality anchor (65.17, -22.52, already flagged "uncertain" in stops.js as representing
# the peninsula rather than an exact landing) projects 2.6 km out to sea.
#
# The stop must move at least 2.6 km to reach any land at all, so the shift is necessarily large:
# 3.5 km north-east, landing 900 m inshore, about 16 pt on the zoomed sheet. That shortens the
# digit 7's top bar by 8% and flattens it from +9.3 to +4.8 degrees, which if anything reads more
# like a 7. Re-vendoring ne_10m_land for one dot was considered and declined; see PZ-17.
PLOT_NUDGE = {
    # Stykkisholmur sits on a small peninsula in Breidafjordur that 1:50m does not resolve, so
    # its own correct coordinate plots 16 pt -- about 3.4 km -- offshore. Same cause as
    # Dogurdarnes, same remedy: the drawing moves, stops.js and the config do not.
    "Stykkishólmur": (-0.0324, -0.0480),
    "D\u00f6gur\u00f0arnes / Dagver\u00f0arnes \u00b7 Iceland": (0.02448, 0.04800),  # (dlat, dlon)
}


def plot_nudge(name):
    """The shift for a place, by full stop name or by the short form used for town labels.

    Shared so the printed sheet and export_aud_base.py cannot disagree about where a stop is --
    they did, briefly, and the designer went on showing Dogurdarnes at sea after the sheet was
    fixed."""
    short = name.split(" · ")[0]
    for key, shift in PLOT_NUDGE.items():
        if name == key or short == key.split(" · ")[0]:
            return shift
    return (0.0, 0.0)


def _in_ring(lon, lat, ring):
    inside = False
    n = len(ring)
    for i in range(n):
        x1, y1 = ring[i][0], ring[i][1]
        x2, y2 = ring[(i + 1) % n][0], ring[(i + 1) % n][1]
        if (y1 > lat) != (y2 > lat):
            if lon < x1 + (lat - y1) * (x2 - x1) / (y2 - y1):
                inside = not inside
    return inside


def _coast_km(lon, lat, rings):
    """Distance to the nearest coastline segment. Flat-earth locally, fine for a warning."""
    kx = 111.320 * math.cos(math.radians(lat))
    best = float("inf")
    for ring in rings:
        for i in range(len(ring)):
            a, b = ring[i], ring[(i + 1) % len(ring)]
            px, py = (lon - a[0]) * kx, (lat - a[1]) * 111.320
            bx, by = (b[0] - a[0]) * kx, (b[1] - a[1]) * 111.320
            l2 = bx * bx + by * by
            t = 0.0 if l2 == 0 else max(0.0, min(1.0, (px * bx + py * by) / l2))
            best = min(best, math.hypot(px - t * bx, py - t * by))
    return best


def build(key, cfg, plan, corpus, answer=False, _return_geometry=False):
    # Copied, not aliased: build() runs twice per trail (Print and ANSWER) from the same plan,
    # and nudging in place would apply the shift twice on the second pass.
    stops = [dict(s) for s in sorted(plan["visits"][key], key=lambda s: s["order"])]
    for s_ in stops:
        dlat, dlon = plot_nudge(s_["name"])
        s_["lat"] += dlat
        s_["lng"] += dlon
    lats = [s["lat"] for s in stops]
    lons = [s["lng"] for s in stops]

    crs = CRS.from_proj4(
        "+proj=lcc +lat_1=%s +lat_2=%s +lat_0=%s +lon_0=%s +x_0=0 +y_0=0 +datum=WGS84 "
        "+units=m +no_defs" % (cfg["parallels"][0], cfg["parallels"][1],
                               (min(lats) + max(lats)) / 2, cfg["lon0"]))
    to_map = Transformer.from_crs(CRS.from_epsg(4326), crs, always_xy=True).transform

    lo0, lo1, la0, la1 = cfg["frame"]
    xs, ys = [], []
    for i in range(31):
        t = i / 30
        for lon, lat in ((lo0 + t * (lo1 - lo0), la0), (lo0 + t * (lo1 - lo0), la1),
                         (lo0, la0 + t * (la1 - la0)), (lo1, la0 + t * (la1 - la0))):
            x, y = to_map(lon, lat)
            xs.append(x)
            ys.append(y)
    BX0, BY0, BX1, BY1 = min(xs), min(ys), max(xs), max(ys)
    scale = min((MX1 - MX0) / (BX1 - BX0), (MY1 - MY0) / (BY1 - BY0))
    cx, cy = (BX0 + BX1) / 2, (BY0 + BY1) / 2
    pcx, pcy = (MX0 + MX1) / 2, (MY0 + MY1) / 2

    def pt(lon, lat):
        x, y = to_map(lon, lat)
        return pcx + (x - cx) * scale, pcy + (y - cy) * scale

    # A stop's raw lon/lat can sit outside the nominal frame box and still land safely on the
    # page: this is a conic projection, so meridians converge toward the pole and a point far
    # enough north can be well inside the printed map even though its bare longitude reads as
    # "outside". The real question is always the PROJECTED position, so check that instead of
    # the raw coordinate -- checking the coordinate directly is what let PR-13 initially believe
    # a safe frame was unsafe.
    for s_ in stops:
        px, py = pt(s_["lng"], s_["lat"])
        assert MX0 <= px <= MX1 and MY0 <= py <= MY1, (
            "%s: stop %s projects outside the printed map area" % (key, s_["name"]))

    # land rings overlapping the frame
    txt = (HERE / "vendor" / "land.js").read_text(encoding="utf-8")
    data = json.loads(txt[txt.find("{"): txt.rfind("}") + 1])
    rings = []
    for feat in data["features"]:
        g = feat["geometry"]
        polys = [g["coordinates"]] if g["type"] == "Polygon" else g["coordinates"]
        for poly in polys:
            for ring in poly:
                lo = [c[0] for c in ring]
                la = [c[1] for c in ring]
                if max(lo) < lo0 - 8 or min(lo) > lo1 + 8:
                    continue
                if max(la) < la0 - 8 or min(la) > la1 + 8:
                    continue
                rings.append(ring)

    # The assertion above only asks whether a stop lands on the page, so a stop plotted in
    # the water passes it happily -- which is how Dogurdarnes sat 2.6 km offshore unnoticed.
    # Warn rather than fail: several real stops are genuinely coastal and 50m data is coarse.
    # Reported in points as well as kilometres: 8 km is two points on Leif's 500 km sheet and
    # invisible, but twelve on Aud's zoomed one and glaring. Only the points matter.
    _m_per_pt = (la1 - la0) * 111320.0 / (MY1 - MY0)
    for s_ in stops:
        if not any(_in_ring(s_["lng"], s_["lat"], r) for r in rings):
            _km = _coast_km(s_["lng"], s_["lat"], rings)
            print("        NOTE: %s plots in the sea, %.1f km from the 50m coastline (%.1f pt here)"
                  % (s_["name"].split(" · ")[0], _km, _km * 1000.0 / _m_per_pt))

    towns = {}
    for s_ in stops:                      # stops first, so they can never be crowded out
        towns[s_["name"].split(" · ")[0]] = (s_["lat"], s_["lng"])
    for name, lat, lng in corpus + cfg["extra_towns"]:
        if lo0 <= lng <= lo1 and la0 <= lat <= la1:
            dlat, dlon = plot_nudge(name)
            towns.setdefault(name, (lat + dlat, lng + dlon))

    digit = next((d["digit"] for d in plan.get("digitOrder", []) if d["trip"] == key), "?")
    out = OUT_DIR / ("Trail_Map_%d_%s_%s.pdf"
                     % (cfg["n"], key.capitalize(), "ANSWER" if answer else "Print"))
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    # _return_geometry renders to memory: the art-placement guide needs the exact frame, label
    # boxes and projection this map uses, without rewriting (or locking) the real PDF.
    target = BytesIO() if _return_geometry else str(out)
    c = canvas.Canvas(target, pagesize=letter)

    c.setFillColor(SEA)
    c.rect(NEAT[0], NEAT[1], NEAT[2] - NEAT[0], NEAT[3] - NEAT[1], stroke=0, fill=1)

    c.saveState()
    clip = c.beginPath()
    clip.rect(MX0, MY0, MX1 - MX0, MY1 - MY0)
    c.clipPath(clip, stroke=0, fill=0)

    c.setFillColor(LAND_C)
    c.setStrokeColor(COAST)
    c.setLineWidth(0.55)
    for ring in rings:
        p = c.beginPath()
        for i, (lon, lat) in enumerate(ring):
            x, y = pt(lon, lat)
            p.moveTo(x, y) if i == 0 else p.lineTo(x, y)
        p.close()
        c.drawPath(p, stroke=1, fill=1)

    # The drawn symbol layer (PZ-17). Over the coastline, under the grid, the stop pins and
    # every label: the base map's own labels must win any overlap, the way they do on a real map.
    # Clipped to the map area so a wood running off the edge stops at the neat line.
    if key == "aud" and aud_layer.LAYER.exists():
        _frame, _feats = aud_layer.load()
        aud_layer.assert_frame(_frame, cfg["frame"], key)
        aud_layer.draw(c, _feats, clip_rect=(MX0, MY0, MX1, MY1))
        print("        symbol layer: %d features from aud_features.json" % len(_feats))
        draw_aud_cache_mark(c)

    # Reference grid: over the land, so a settlement can be given a square reference -- but under
    # every label drawn below, so no line printed here can ever sit on top of a clue.
    c.saveState()
    # Aud's sheet carries a drawn symbol layer, so the grid has to step further back than on the
    # other three: at TAN/0.45 it competed with the linework and made the map read as busy.
    if key == "aud":
        c.setStrokeColor(HexColor("#D9CDB2"))
        c.setLineWidth(0.3)
    else:
        c.setStrokeColor(TAN)
        c.setLineWidth(0.45)
    for i in range(1, GRID_COLS):
        x = MX0 + i * (MX1 - MX0) / GRID_COLS
        c.line(x, MY0, x, MY1)
    for j in range(1, GRID_ROWS):
        y = MY0 + j * (MY1 - MY0) / GRID_ROWS
        c.line(MX0, y, MX1, y)
    c.restoreState()

    lab = Labeller()
    # Keep every candidate label wholly inside the map frame; obstacle avoidance can otherwise
    # push a coastal name through the neat line while escaping a nearby road or symbol.
    lab.reserve(-1000, -1000, MX0 + 1, 2000)
    lab.reserve(MX1 - 1, -1000, 2000, 2000)
    lab.reserve(MX0, -1000, MX1, MY0 + 1)
    lab.reserve(MX0, MY1 - 1, MX1, 2000)
    # Legend for Aud's sheet, in the clear water bottom-left. Reserved so the label placer
    # routes town names around it rather than printing them across the key.
    if key == "aud" and aud_layer.LAYER.exists():
        # Rescaled 20 Sept 2026, twice (see LEIF_ART above) -- same exact transform.
        _lx, _ly, _lw, _lh = 39.89, 114.29, 160.06, 200.08
        aud_layer.draw_legend(c, _feats, (_lx, _ly, _lx + _lw, _ly + _lh),
                              ink="#"+INK.hexval()[2:], rule="#"+TAN.hexval()[2:],
                              paper="#F4EEDD")
        lab.reserve(_lx - 2, _ly - 2, _lx + _lw + 2, _ly + _lh + 2)
        # Labels are drawn after the feature layer, so explicitly reserve the visible linework
        # and landmark symbols. This lets the normal right/left/above/below candidate search move
        # names such as Budardalur away from a road instead of printing straight through it.
        for f in _feats:
            if f["kind"] in aud_layer.LINE and len(f["pts"]) > 1:
                radius = 3.0 if f["kind"] in ("road", "river") else 2.2
                lab.reserve_polyline(f["pts"], radius=radius)
            elif len(f["pts"]) == 1 and f["kind"] != "text":
                x, y = f["pts"][0]
                lab.reserve_centred(x, y, 16, 16, pad=1.5)
    if key == "leif":
        for filename, box, alpha in LEIF_ART:
            draw_vignette(c, ART_DIR / filename, box, alpha)
            x, y, w, h = box
            lab.reserve(x, y, x + w, y + h)
    elif key == "rollo":
        for filename, box, alpha in ROLLO_ART:
            draw_vignette(c, SOURCE_ART_DIR / filename, box, alpha)
            x, y, w, h = box
            lab.reserve(x, y, x + w, y + h)
        for filename, box, alpha in ROLLO_WORDLOCK_ART:
            draw_vignette(c, SOURCE_ART_DIR / filename, box, alpha)
            x, y, w, h = box
            lab.reserve(x, y, x + w, y + h)
    elif key == "harald":
        for col_idx, row, group, position, rune_letter in HARALD_RUNES_REAL:
            x, y = cell_center(col_idx, row)
            draw_rune_stem(c, x, y, group, position)
            lab.reserve_centred(x, y - 3, 30, 34, pad=2)
            if answer:
                c.setFillColor(RUST)
                c.setFont("CinzelBold", 7.5)
                c.drawCentredString(x, y - 17, rune_letter)
        for col_idx, row, group, position in HARALD_RUNES_DECOY:
            x, y = cell_center(col_idx, row)
            draw_rune_stem(c, x, y, group, position)
            lab.reserve_centred(x, y, 26, 26, pad=2)

    for nm, _m, la_, lo_ in cfg["regions"]:
        rx, ry = pt(lo_, la_)
        assert MX0 <= rx <= MX1 and MY0 <= ry <= MY1, (
            "%s: region label %s at %.2f,%.2f falls outside the printed map area" % (key, nm, la_, lo_))
    for text, lat, lon, rot in cfg["waters"]:
        x, y = pt(lon, lat)
        lines = text.split("\n")
        widest = max(pdfmetrics.stringWidth(" ".join(l), "Cinzel", 7.4) for l in lines)
        lab.reserve_centred(x, y - (len(lines) - 1) * 5, widest, 10 * len(lines) + 4, pad=3)
        c.saveState()
        c.translate(x, y)
        c.rotate(rot)
        c.setFillColor(TEAL)
        c.setFont("Cinzel", 7.4)
        for i, line in enumerate(lines):
            c.drawCentredString(0, -i * 10, " ".join(line))
        c.restoreState()

    for norse, modern, lat, lon in cfg["regions"]:
        x, y = pt(lon, lat)
        w = max(pdfmetrics.stringWidth(" ".join(norse), "CinzelXB", 12.5),
                pdfmetrics.stringWidth(modern, "PlexIt", 7.2))
        lab.reserve(x - w / 2 - 4, y - 16, x + w / 2 + 4, y + 12)
        c.setFillColor(INK)
        c.setFont("CinzelXB", 12.5)
        c.drawCentredString(x, y, " ".join(norse))
        if modern:                     # blank when the Norse and modern names are the same word
            c.setFillColor(INK_SOFT)
            c.setFont("PlexIt", 7.2)
            c.drawCentredString(x, y - 10.5, modern)

    for name, lat, lon in cfg["areas"]:
        x, y = pt(lon, lat)
        w = pdfmetrics.stringWidth(name, "PlexIt", 8.4)
        lab.reserve(x - w / 2 - 4, y - 6, x + w / 2 + 4, y + 9)
        c.setFillColor(TAN)
        c.setFont("PlexIt", 8.4)
        c.drawCentredString(x, y, name)

    lab.reserve(NEAT[2] - 170, NEAT[1] + 14, NEAT[2] - 8, NEAT[1] + 46)
    # +14pt of headroom: the box stopped at the rose itself, so a village symbol printed
    # straight over the "N" above it.
    lab.reserve(NEAT[2] - 72, MY0 + 16, NEAT[2] - 16, MY0 + 82)

    stop_names = [s_["name"].split(" · ")[0] for s_ in stops]
    ordered = stop_names + sorted(n for n in towns if n not in stop_names)
    for name in ordered:
        lat, lon = towns[name]
        x, y = pt(lon, lat)
        c.setStrokeColor(INK_SOFT)
        c.setFillColor(WHITE)
        c.setLineWidth(0.6)
        c.circle(x, y, 1.7, stroke=1, fill=1)
        lab.reserve_centred(x, y, 5, 5, pad=0.5)
        spot = lab.place(name, x, y, "Plex", 6.6)
        if spot:
            c.setFillColor(INK_SOFT)
            c.setFont("Plex", 6.6)
            c.drawString(spot[0], spot[1], name)

    if answer:
        # The solved route, drawn where a player would draw it with the wet-erase marker.
        route = [pt(s_["lng"], s_["lat"]) for s_ in stops]
        c.setStrokeColor(WHITE)
        c.setLineWidth(7)
        c.setLineCap(1)
        c.setLineJoin(1)
        path = c.beginPath()
        path.moveTo(*route[0])
        for q in route[1:]:
            path.lineTo(*q)
        c.drawPath(path, stroke=1, fill=0)
        c.setStrokeColor(RUST)
        c.setLineWidth(3.4)
        path = c.beginPath()
        path.moveTo(*route[0])
        for q in route[1:]:
            path.lineTo(*q)
        c.drawPath(path, stroke=1, fill=0)
        for i, (qx, qy) in enumerate(route):
            c.setFillColor(RUST)
            c.setStrokeColor(WHITE)
            c.setLineWidth(1.2)
            c.circle(qx, qy, 6.4, stroke=1, fill=1)
            c.setFillColor(WHITE)
            c.setFont("CinzelBold", 7.6)
            c.drawCentredString(qx, qy - 2.7, str(i + 1))
    c.restoreState()

    # neat line, grid band, grid references
    cw, ch = (MX1 - MX0) / GRID_COLS, (MY1 - MY0) / GRID_ROWS

    # Per-trail colour, on the grid band only. Four laminated sheets are hard to tell apart on a
    # crowded table, and the band is the one element visible from any edge that carries no map
    # content. Tinting it leaves the sea/land contrast alone -- that contrast is what identifies
    # the unlabelled animals, so it cannot be spent on route identity. Four strips, not an
    # even-odd ring, so the title band below BAND_Y0 stays clear for the title and scale bar.
    c.setFillColor(HexColor(cfg.get("band", "#59635D")))
    for bx, by, bw, bh in ((NEAT[0], BAND_Y0, MX0 - NEAT[0], NEAT[3] - BAND_Y0),
                           (MX1, BAND_Y0, NEAT[2] - MX1, NEAT[3] - BAND_Y0),
                           (MX0, MY1, MX1 - MX0, NEAT[3] - MY1),
                           (MX0, BAND_Y0, MX1 - MX0, MY0 - BAND_Y0)):
        c.rect(bx, by, bw, bh, stroke=0, fill=1)

    c.setStrokeColor(INK)
    c.setLineWidth(1.6)
    c.rect(NEAT[0], NEAT[1], NEAT[2] - NEAT[0], NEAT[3] - NEAT[1], stroke=1, fill=0)
    c.setLineWidth(0.9)
    c.rect(MX0, MY0, MX1 - MX0, MY1 - MY0, stroke=1, fill=0)
    c.setFillColor(WHITE)                      # grid references now sit on the tinted band
    c.setFont("Plex", 6.4)
    col_letters = cfg.get("col_letters") or [chr(65 + i) for i in range(GRID_COLS)]
    for i in range(GRID_COLS):                 # letters across, repeated top and bottom
        x = MX0 + (i + 0.5) * cw
        c.drawCentredString(x, MY1 + BAND / 2 - 2.3, col_letters[i])
        c.drawCentredString(x, MY0 - BAND / 2 - 2.3, col_letters[i])
    for j in range(GRID_ROWS):                 # numbers down from the top, repeated both sides
        y = MY1 - (j + 0.5) * ch
        c.drawCentredString(MX0 - BAND / 2, y - 2.3, str(j + 1))
        c.drawCentredString(MX1 + BAND / 2, y - 2.3, str(j + 1))
    c.setLineWidth(0.7)
    c.line(NEAT[0], BAND_Y0, NEAT[2], BAND_Y0)

    # Title and map credit only. The trail name, the "Map n of four" numbering and the
    # find-them-by-name instruction were all cut: the first two pre-sorted the deck and handed
    # over the digit order, and the third spoke in the designer's voice rather than Liv's.
    tx = NEAT[0] + 16
    c.setFillColor(INK)
    c.setFont("CinzelXB", 19)
    c.drawString(tx, MY0 - 30, " ".join(cfg["title"]))


    if answer:
        # A banner across the head of the sheet: unmissable, and clear of the scale bar and
        # compass that the title band already carries.
        bh = 21
        c.setFillColor(RUST)
        c.rect(NEAT[0], NEAT[3] - bh, NEAT[2] - NEAT[0], bh, stroke=0, fill=1)
        c.setFillColor(WHITE)
        c.setFont("CinzelXB", 11)
        c.drawString(NEAT[0] + 14, NEAT[3] - 14.5, "A N S W E R   K E Y")
        c.setFont("Plex", 7)
        c.drawString(NEAT[0] + 150, NEAT[3] - 14, "designer copy - not for the bag")
        c.setFont("CinzelXB", 13)
        c.drawRightString(NEAT[2] - 14, NEAT[3] - 15, "reads as  %s" % digit)
        c.saveState()
        c.setFillColor(HexColor("#C9A77B"))
        c.setFillAlpha(0.28)
        c.setFont("PlexIt", 26)
        c.translate(PAGE_W / 2, PAGE_H / 2)
        c.rotate(38)
        c.drawCentredString(0, 0, "A N S W E R   K E Y")
        c.restoreState()

    # scale bar, rounded to something legible at this frame's width
    mid = (la0 + la1) / 2
    x0, _ = to_map(cfg["lon0"], mid)
    x1, _ = to_map(cfg["lon0"] + 1.0, mid)
    km_per_deg = abs(x1 - x0) / 1000.0
    span_km = (lo1 - lo0) * km_per_deg
    nice = min([1, 2, 5, 10, 20, 50, 100, 200, 500, 1000],
               key=lambda v: abs(v - span_km / 4))
    length = (nice / km_per_deg) * abs(x1 - x0) * scale
    bx, by = NEAT[2] - 20 - length, NEAT[1] + 30
    seg = length / 4
    c.setStrokeColor(INK)
    c.setLineWidth(0.8)
    for i in range(4):
        c.setFillColor(INK if i % 2 == 0 else WHITE)
        c.rect(bx + i * seg, by, seg, 3.2, stroke=1, fill=1)
    c.setFillColor(INK_SOFT)
    c.setFont("Plex", 6.2)
    c.drawString(bx, by - 8.5, "0")
    c.drawRightString(bx + length, by - 8.5, "%d km" % nice)

    # compass
    x, y, r = NEAT[2] - 46, MY0 + 42, 17
    c.setStrokeColor(INK_SOFT)
    c.setLineWidth(0.7)
    c.circle(x, y, r, stroke=1, fill=0)
    c.setFillColor(INK)
    p = c.beginPath()
    p.moveTo(x, y + r - 2)
    p.lineTo(x - 4, y)
    p.lineTo(x, y - r + 2)
    p.lineTo(x + 4, y)
    p.close()
    c.drawPath(p, fill=1, stroke=0)
    c.setFillColor(WHITE)
    p = c.beginPath()
    p.moveTo(x, y + r - 2)
    p.lineTo(x + 4, y)
    p.lineTo(x, y - r + 2)
    p.close()
    c.drawPath(p, fill=1, stroke=1)
    c.setFillColor(INK)
    c.setFont("CinzelBold", 7)
    c.drawCentredString(x, y + r + 4, "N")


    c.showPage()
    if key == "harald":
        draw_harald_board_back(c)
        c.showPage()
    c.save()
    if _return_geometry:
        return pt, rings, lab, lo0, lo1, la0, la1

    missing = [s["name"].split(" · ")[0] for s in stops
               if s["name"].split(" · ")[0] not in towns]
    print("%-6s -> %s%s" % (key, out.name, ("  [digit %s]" % digit) if answer else ""))
    print("        frame lon %.2f..%.2f lat %.2f..%.2f | %d labels | scale bar %d km"
          % (lo0, lo1, la0, la1, len(towns), nice))
    if lab.skipped:
        print("        labels dropped for collision: %s" % ", ".join(lab.skipped))
    # A stop can also go unfindable by losing its label to a collision rather than by being absent
    # from the corpus, and the frame is tight enough since the grid band that this is reachable.
    collided = [n for n in lab.skipped if n in stop_names]
    if missing or collided:
        print("        *** STOPS NOT LABELLED ON SHEET: %s"
              % ", ".join(missing + collided))
    return missing + collided


def main():
    plan = load_plan()
    corpus = load_corpus()
    want = sys.argv[1:] or list(TRAILS)
    for key in want:
        if key in BLOCKED:
            print("%-6s -> BLOCKED: %s" % (key, BLOCKED[key]))
            continue
        build(key, TRAILS[key], plan, corpus)
        build(key, TRAILS[key], plan, corpus, answer=True)


if __name__ == "__main__":
    main()
