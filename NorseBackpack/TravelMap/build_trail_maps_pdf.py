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
ART_DIR = HERE / "Art" / "processed"   # alpha-hole-filled derivatives; see fill_art_alpha_holes.py

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
MARGIN = 0.30 * 72
NEAT = (MARGIN, MARGIN, PAGE_W - MARGIN, PAGE_H - MARGIN)
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
        parallels=(64, 66), lon0=-22, frame=(-24.5, -20.0, 63.6, 65.9),
        regions=[("ÍSLAND", "Iceland", 64.72, -20.75)],
        areas=[("Breiðafjörður", 65.36, -22.90), ("Dalir", 65.16, -21.40),
               ("Snæfellsnes", 64.87, -23.20), ("Kjalarnes", 64.28, -21.70)],
        waters=[("DENMARK STRAIT", 65.90, -25.40, -8), ("FAXAFLÓI", 64.45, -22.80, 0)],
        # APPROX -- typed from general knowledge, not source-checked. See PR-10.
        extra_towns=[("Reykjavík", 64.15, -21.94), ("Akranes", 64.32, -22.08),
                     ("Borgarnes", 64.54, -21.92), ("Búðardalur", 65.11, -21.76),
                     ("Stykkishólmur", 65.07, -22.73), ("Grundarfjörður", 64.92, -23.25),
                     ("Ólafsvík", 64.89, -23.71), ("Hellissandur", 64.91, -23.90),
                     ("Reykholt", 64.66, -21.29), ("Mosfellsbær", 64.17, -21.68),
                     ("Hafnarfjörður", 64.07, -21.94)],
    ),
}

BLOCKED = {
    "harald": "stops 5 and 6 are 'Sicily' and 'Asia Minor' -- regions, not points. Same "
              "no-endpoint problem Helluland had; resolve to named settlements first.",
}

# Decorative vignettes approved for Leif's sheet (PR-11), re-placed for the PR-13 frame. The
# three sea pieces sit inside the placement guide's re-run rectangles (build_art_placement_guide.py
# leif). The land pieces were placed by a search, not by eye: maximise clearance from the printed
# coastline, then require the candidate box to miss every OTHER reserved box from a clean build
# (every stop, town, region and water label -- not just a distance-from-point heuristic, which
# first missed a real collision between the wolf and "MARKLAND"). The longship was also shrunk
# from its first pass (2.36 x 1.61 in) to 1.70 x 0.85 in: it was crowding the Labrador Sea.
LEIF_ART = (
    ("Leif_Longship_v1.png",   (417.6, 182.9, 122.4, 61.2), 0.72),  # slot A
    ("Leif_Whale_v1.png",      (267.8, 298.8, 108.0, 72.0), 0.68),  # slot B
    ("Leif_Iceberg_v1.png",    (477.4, 484.9,  93.6, 68.4), 0.64),  # slot D
    ("Leif_Polar_Bear_v1.png", (342.53, 705.48, 48.0, 44.0), 0.62), # F1
    ("Leif_Seal_v1.png",       (221.47, 705.48, 48.0, 44.0), 0.62), # D1
    ("Leif_Hare_v1.png",       ( 39.87, 581.82, 48.0, 44.0), 0.62), # A3
    ("Leif_Deer_v1.png",       (403.07, 643.65, 48.0, 44.0), 0.62), # G2
    ("Leif_Loon_v1.png",       (100.40, 458.15, 48.0, 44.0), 0.62), # B5
    ("Leif_Wolf_v1.png",       ( 39.87, 396.32, 48.0, 44.0), 0.62), # A6
    ("Leif_Orca_v1.png",       (403.07, 334.48, 48.0, 44.0), 0.62), # G7
    ("Leif_Settlement_v1.png", (326.0, 589.8,  58.0, 36.0), 0.62),  # W. Greenland, 4.1deg clear
)


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

    def place(self, name, x, y, font, size, pad=1.4):
        w = pdfmetrics.stringWidth(name, font, size)
        h = size * 0.86
        for dx, dy in ((4.4, -h / 2), (-w - 4.4, -h / 2), (-w / 2, 4.6), (-w / 2, -h - 4.6),
                       (4.0, 3.2), (4.0, -h - 3.2), (-w - 4.0, 3.2), (-w - 4.0, -h - 3.2),
                       (7.5, -h / 2), (-w - 7.5, -h / 2)):
            box = (x + dx - pad, y + dy - pad, x + dx + w + pad, y + dy + h + pad)
            if any(self._hit(box, b) for b in self.boxes):
                continue
            self.boxes.append(box)
            return x + dx, y + dy
        self.skipped.append(name)
        return None


def build(key, cfg, plan, corpus, answer=False, _return_geometry=False):
    stops = sorted(plan["visits"][key], key=lambda s: s["order"])
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

    towns = {}
    for s_ in stops:                      # stops first, so they can never be crowded out
        towns[s_["name"].split(" · ")[0]] = (s_["lat"], s_["lng"])
    for name, lat, lng in corpus + cfg["extra_towns"]:
        if lo0 <= lng <= lo1 and la0 <= lat <= la1:
            towns.setdefault(name, (lat, lng))

    digit = next((d["digit"] for d in plan.get("digitOrder", []) if d["trip"] == key), "?")
    out = OUT_DIR / ("Trail_Map_%d_%s_%s.pdf"
                     % (cfg["n"], key.capitalize(), "ANSWER" if answer else "Print"))
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    # _return_geometry renders to memory: the art-placement guide needs the exact frame, label
    # boxes and projection this map uses, without rewriting (or locking) the real PDF.
    target = BytesIO() if _return_geometry else str(out)
    c = canvas.Canvas(target, pagesize=letter)
    c.setTitle("Trail Map %d - %s%s" % (cfg["n"], key.capitalize(),
                                        " (ANSWER KEY)" if answer else ""))

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

    # Reference grid: over the land, so a settlement can be given a square reference -- but under
    # every label drawn below, so no line printed here can ever sit on top of a clue.
    c.saveState()
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
    if key == "leif":
        for filename, box, alpha in LEIF_ART:
            draw_vignette(c, ART_DIR / filename, box, alpha)
            x, y, w, h = box
            lab.reserve(x, y, x + w, y + h)

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
    lab.reserve(NEAT[2] - 72, MY0 + 16, NEAT[2] - 16, MY0 + 68)

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
    for i in range(GRID_COLS):                 # letters across, repeated top and bottom
        x = MX0 + (i + 0.5) * cw
        c.drawCentredString(x, MY1 + BAND / 2 - 2.3, chr(65 + i))
        c.drawCentredString(x, MY0 - BAND / 2 - 2.3, chr(65 + i))
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
