"""Reusable medallion geometry with the approved Space back-lettering layout.

Requires numpy, Pillow, OpenCV, matplotlib, Shapely >= 2.1.
The PNG supplies only a traced front profile; all Z coordinates are exact CAD.
"""
from pathlib import Path
import json
import math
import struct
import zipfile
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from matplotlib.textpath import TextPath
from matplotlib.font_manager import FontProperties
from shapely import affinity, constrained_delaunay_triangles, maximum_inscribed_circle
from shapely.geometry import Polygon, Point, LineString
from shapely.geometry.polygon import orient
from shapely.ops import unary_union

OUT = None
SOURCE = None
DIAMETER, BODY_TOP, TOTAL_HEIGHT, ENGRAVE = 50.0, 3.8, 4.4, 0.4
BRAND_CAP, MAIN_CAP = 4.0, 4.6
FONT_BOLD = FontProperties(fname="C:/Windows/Fonts/arialbd.ttf")
FONT_OPEN = FontProperties(fname="C:/Windows/Fonts/arial.ttf")


def polys(g):
    if g.is_empty:
        return []
    if g.geom_type == "Polygon":
        return [g]
    return [p for p in g.geoms if p.geom_type == "Polygon"]


def radial_extent(g):
    return max(math.hypot(x, y) for p in polys(g) for x, y in p.exterior.coords)


def save_svg(g, name):
    paths = []
    for p in polys(g):
        p = orient(p, 1)
        for ring in [p.exterior, *p.interiors]:
            paths.append("M " + " L ".join(
                f"{x + 25:.5f},{25 - y:.5f}" for x, y in list(ring.coords)[:-1]) + " Z")
    (OUT / name).write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" width="50mm" height="50mm" '
        'viewBox="0 0 50 50"><path fill="black" fill-rule="nonzero" d="' +
        " ".join(paths) + '"/></svg>', encoding="utf-8")


def front_profile():
    rgb = np.array(Image.open(SOURCE).convert("RGB"))
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
    mask = cv2.inRange(hsv, np.array([12, 100, 100]), np.array([45, 255, 255]))
    contours, tree = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    tree = tree[0]
    outer = max(range(len(contours)), key=lambda i: cv2.contourArea(contours[i]))
    (cx, cy), (a, b), angle = cv2.fitEllipse(contours[outer])
    # Normalize the illustration's slight oval projection to a true circular face.
    def trace_points(c):
        points = cv2.approxPolyDP(c, .85, True).reshape(-1, 2)
        return [(float(x - cx), float(cy - y)) for x, y in points]
    parts = []
    for i, c in enumerate(contours):
        depth, parent = 0, int(tree[i][3])
        while parent >= 0:
            depth += 1
            parent = int(tree[parent][3])
        if depth % 2 or cv2.contourArea(c) < 20:
            continue
        holes = [trace_points(contours[j]) for j in range(len(contours))
                 if int(tree[j][3]) == i and cv2.contourArea(contours[j]) > 12]
        parts.extend(polys(Polygon(trace_points(c), holes).buffer(0)))
    inside = unary_union(parts)
    # fitEllipse's two axes are rotated, not necessarily aligned with X/Y.
    inside = affinity.rotate(inside, angle, origin=(0, 0))
    inside = affinity.scale(inside, 46.6 / a, 46.6 / b, origin=(0, 0))
    inside = affinity.rotate(inside, -angle, origin=(0, 0))
    # A foreground motif can connect to a source rim.
    # Clip away only the outer rim band, never its entire connected component.
    inside = inside.intersection(Point(0, 0).buffer(21.85, quad_segs=144))
    # Open cramped decorative seams slightly and round extremely sharp tips.
    inside = inside.buffer(-.07, join_style="round").buffer(.025, join_style="round")
    inside = inside.simplify(.015, preserve_topology=True)
    before_filter_count = len(polys(inside))
    retained = [p for p in polys(inside) if p.area > .08 and not p.buffer(-.22).is_empty]
    inside = unary_union(retained)
    border = Point(0, 0).buffer(23.0, quad_segs=144).difference(
        Point(0, 0).buffer(22.1, quad_segs=144))
    front = unary_union([inside, border])
    if not front.is_valid or radial_extent(front) > 23.5:
        raise ValueError("Front relief exceeds the safe circular face.")
    Image.fromarray(mask).save(OUT / "front_trace_mask_v1.png")
    return front, {"source_pixels": [rgb.shape[1], rgb.shape[0]],
                   "fitted_outer_yellow_ellipse": [cx, cy, a, b, angle],
                   "removed_tiny_components": before_filter_count - len(retained)}


def glyph(c, cap, font):
    path = TextPath((0, 0), c, size=100, prop=font)
    g = Polygon()
    for ring in path.to_polygons():
        if len(ring) > 3:
            g = g.symmetric_difference(Polygon(ring).buffer(0))
    h = TextPath((0, 0), "H", size=100, prop=font).get_extents().height
    g = affinity.scale(g, cap / h, cap / h, origin=(0, 0))
    x0, y0, x1, y1 = g.bounds
    return affinity.translate(g, -(x0 + x1) / 2, -y0)


def arc_text(s, cap, radius, span, bottom=False, font=FONT_BOLD):
    glyphs = [glyph(c, cap, font) if c != " " else None for c in s]
    widths = [g.bounds[2] - g.bounds[0] if g is not None else cap * .60 for g in glyphs]
    arc = math.radians(span) * radius
    spacing = (arc - sum(widths)) / (len(s) - 1)
    if spacing < .65:
        raise ValueError(f"Insufficient character spacing: {s}: {spacing:.3f} mm")
    position = -arc / 2
    placed = []
    for c, g, width in zip(s, glyphs, widths):
        angle = (position + width / 2) / radius
        if g is not None:
            g = affinity.rotate(g, math.degrees(angle) * (1 if bottom else -1),
                                origin=(0, 0))
            g = affinity.translate(g, radius * math.sin(angle),
                                   (-1 if bottom else 1) * radius * math.cos(angle))
            placed.append((c, g))
        position += width + spacing
    gaps = [g.distance(h) for (_, g), (_, h) in zip(placed, placed[1:])]
    return unary_union([g for _, g in placed]), placed, spacing, min(gaps)


def back_profile():
    groups, measurements, placed_all = {}, {}, []
    specs = [
        ("ADVENTURE", MAIN_CAP, 17.0, 144, False, FONT_BOLD),
        ("COMPLETE", MAIN_CAP, 16.5, 174, True, FONT_BOLD),
        ("ESCAPE BACKPACK", BRAND_CAP, 22.1, 186, True, FONT_OPEN),
    ]
    for text, cap, radius, span, bottom, font in specs:
        group, placed, spacing, gap = arc_text(text, cap, radius, span, bottom, font)
        if gap < .7:
            raise ValueError(f"Adjacent glyphs too close: {text}: {gap:.3f} mm")
        groups[text] = group
        placed_all.extend((text, c, g) for c, g in placed)
        measurements[text] = {"cap_height_mm": cap, "font": Path(font.get_file()).name,
                              "nominal_advance_gap_mm": spacing,
                              "minimum_adjacent_glyph_distance_mm": gap,
                              "maximum_radius_mm": radial_extent(group)}
    vertices = []
    for i in range(8):
        ang = math.pi / 2 + i * math.pi / 4
        r = 6.8 if i % 2 == 0 else 1.45
        vertices.append((r * math.cos(ang), r * math.sin(ang)))
    star = LineString(vertices + [vertices[0]]).buffer(.35, join_style="round")
    circle = Point(0, 0).buffer(5.7, quad_segs=100).boundary.buffer(.35)
    compass = unary_union([star, circle])
    border = Point(0, 0).buffer(23.75, quad_segs=144).boundary.buffer(.25)
    text_geom = unary_union(list(groups.values()))
    if not text_geom.is_valid or text_geom.distance(border) < .7:
        raise ValueError("Back text too close to the engraving border.")
    pair_gaps = [g.distance(h) for i, g in enumerate(groups.values())
                 for j, h in enumerate(groups.values()) if i < j]
    if min(pair_gaps) < .8 or text_geom.distance(compass) < .8:
        raise ValueError("Back text groups overlap or approach the compass.")
    counters = []
    for text, c, g in placed_all:
        for p in polys(g):
            for ring in p.interiors:
                island = Polygon(ring)
                diameter = 2 * maximum_inscribed_circle(island, tolerance=.001).length
                counters.append({"text": text, "letter": c,
                                 "largest_inscribed_diameter_mm": diameter,
                                 "survives_0_2mm_inset": not island.buffer(-.2).is_empty})
    back = unary_union([text_geom, compass, border])
    return back, {
        "text": measurements,
        "minimum_distance_between_text_groups_mm": min(pair_gaps),
        "minimum_text_to_compass_distance_mm": text_geom.distance(compass),
        "minimum_text_to_border_distance_mm": text_geom.distance(border),
        "letter_counter_islands": counters,
        "smallest_counter_inscribed_diameter_mm": min(c["largest_inscribed_diameter_mm"]
                                                     for c in counters),
    }


def make_mesh(layers):
    triangles = []
    def flat(g, z, up):
        for p in polys(g):
            for tri in constrained_delaunay_triangles(p).geoms:
                xy = np.array(tri.exterior.coords)[:3]
                a, b = xy[1] - xy[0], xy[2] - xy[0]
                if ((a[0] * b[1] - a[1] * b[0]) > 0) != up:
                    xy = xy[::-1]
                triangles.append(np.column_stack([xy, np.full(3, z)]))
    previous = Polygon()
    for bottom, top, g in layers:
        flat(g.difference(previous), bottom, False)
        flat(previous.difference(g), bottom, True)
        for p in polys(g):
            p = orient(p, 1)
            for ring in [p.exterior, *p.interiors]:
                xy = list(ring.coords)
                for a, b in zip(xy, xy[1:]):
                    v0, v1, v2, v3 = (*a, bottom), (*b, bottom), (*b, top), (*a, top)
                    triangles.extend([[v0, v1, v2], [v0, v2, v3]])
        previous = g
    flat(previous, layers[-1][1], True)
    return np.asarray(triangles, dtype=np.float64)


def write_stl(triangles, path):
    cross = np.cross(triangles[:, 1] - triangles[:, 0], triangles[:, 2] - triangles[:, 0])
    normals = cross / np.linalg.norm(cross, axis=1)[:, None]
    with path.open("wb") as stream:
        header = (path.stem[:55] + " | mm | back DOWN").encode("ascii")
        stream.write(header.ljust(80, b" "))
        stream.write(struct.pack("<I", len(triangles)))
        for n, triangle in zip(normals, triangles):
            stream.write(struct.pack("<12fH", *n, *triangle.ravel(), 0))


def check_mesh(path, report_name="mesh_check_v1.json"):
    data = path.read_bytes()
    count = struct.unpack("<I", data[80:84])[0]
    if len(data) != 84 + 50 * count:
        raise ValueError("Invalid binary STL length")
    dtype = np.dtype([("normal", "<f4", 3), ("vertices", "<f4", (3, 3)), ("attribute", "<u2")])
    triangles = np.frombuffer(data, dtype=dtype, offset=84, count=count)["vertices"].astype(float)
    # Validate the exported float32 geometry, not just the source polygons.
    vertices, indices = np.unique(triangles.reshape(-1, 3), axis=0, return_inverse=True)
    faces = indices.reshape(-1, 3)
    edges = np.concatenate([faces[:, [0, 1]], faces[:, [1, 2]], faces[:, [2, 0]]])
    sorted_edges = np.sort(edges, axis=1)
    unique_edges, inverse, counts = np.unique(sorted_edges, axis=0, return_inverse=True,
                                             return_counts=True)
    direction = np.where(edges[:, 0] < edges[:, 1], 1, -1)
    balances = np.bincount(inverse, weights=direction)
    parent = list(range(len(vertices)))
    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a
    for a, b in unique_edges:
        ra, rb = find(int(a)), find(int(b))
        if ra != rb:
            parent[ra] = rb
    components = len({find(i) for i in range(len(vertices))})
    cross = np.cross(triangles[:, 1] - triangles[:, 0], triangles[:, 2] - triangles[:, 0])
    degenerate = int(np.sum(np.linalg.norm(cross, axis=1) < 1e-10))
    volume = float(np.einsum("ij,ij->i", triangles[:, 0],
                            np.cross(triangles[:, 1], triangles[:, 2])).sum() / 6)
    report = {
        "triangles": count, "closed_edges_all_used_twice": bool(np.all(counts == 2)),
        "consistent_orientation": bool(np.all(balances == 0)),
        "connected_components": components, "degenerate_facets": degenerate,
        "bounds_mm": [vertices.min(axis=0).tolist(), vertices.max(axis=0).tolist()],
        "signed_volume_mm3": volume, "physical_print_test": False,
        "printer_profile_slice": False,
    }
    if not report["closed_edges_all_used_twice"] or not report["consistent_orientation"]:
        raise ValueError(f"STL is not a closed consistently-oriented surface: {report}")
    if components != 1 or degenerate or volume <= 0:
        raise ValueError(f"Invalid STL solid: {report}")
    (OUT / report_name).write_text(json.dumps(report, indent=2) + "\n")
    return report


def raster(g, size=1500):
    result = np.zeros((size, size), dtype=bool)
    def xy(r):
        return [((x + 27) / 54 * size, (27 - y) / 54 * size) for x, y in r.coords]
    for p in polys(g):
        image = Image.new("L", (size, size), 0)
        draw = ImageDraw.Draw(image)
        draw.polygon(xy(p.exterior), fill=255)
        for h in p.interiors:
            draw.polygon(xy(h), fill=0)
        result |= np.array(image) > 0
    return result


def preview(disk, front, back, filename, front_caption):
    size = 1500
    body = raster(disk, size)
    def render(profile, is_front):
        detail = raster(profile, size)
        height = np.full((size, size), -1.0, dtype="float32")
        height[body] = 0
        height[detail] = .6 if is_front else -.4
        smoothed = cv2.GaussianBlur(height, (0, 0), 1.3)
        gy, gx = np.gradient(smoothed, 54 / size)
        light = np.clip((1 - .32 * gx - .48 * gy) / np.sqrt(1 + gx * gx + gy * gy), .3, 1.4)
        rgb = np.empty((size, size, 3), dtype="float32")
        rgb[:] = [247, 244, 234]
        rgb[body] = [25, 54, 91]
        if is_front:
            rgb[detail] = [250, 200, 35]
        else:
            rgb[detail] = [11, 29, 52]
        rgb[body] *= (.74 + .30 * light[body, None])
        return Image.fromarray(np.uint8(np.clip(rgb, 0, 255)))
    image = Image.new("RGB", (2000, 1160), "#f7f4ea")
    image.paste(render(front, True).resize((920, 920), Image.Resampling.LANCZOS), (40, 45))
    image.paste(render(back, False).resize((920, 920), Image.Resampling.LANCZOS), (1040, 45))
    draw = ImageDraw.Draw(image)
    bold = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 29)
    small = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 24)
    draw.text((75, 987), "FRONT / PRINTS UP", font=bold, fill="#19365b")
    draw.text((1075, 987), "BACK / PRINTS DOWN", font=bold, fill="#19365b")
    draw.text((75, 1032), front_caption, font=small, fill="#56636e")
    draw.text((1075, 1032), "4.0 mm brand lettering / 0.4 mm engraving", font=small, fill="#56636e")
    draw.text((75, 1100), "50 mm diameter / 4.4 mm thick / one solid piece / exact profile preview / physically untested",
              font=small, fill="#56636e")
    image.save(OUT / filename)


def build_model(output_dir, stem, version, front, trace, preview_filename,
                front_caption, top_groove=None):
    global OUT
    OUT = Path(output_dir)
    OUT.mkdir(parents=True, exist_ok=True)
    back, back_report = back_profile()
    disk = Point(0, 0).buffer(DIAMETER / 2, quad_segs=144)
    mirrored_back = affinity.scale(back, -1, 1, origin=(0, 0))
    layers = [(0, ENGRAVE, disk.difference(mirrored_back))]
    if top_groove is not None:
        layers.extend([(ENGRAVE, 3.6, disk),
                       (3.6, BODY_TOP, disk.difference(top_groove))])
    else:
        layers.append((ENGRAVE, BODY_TOP, disk))
    layers.append((BODY_TOP, TOTAL_HEIGHT, front))
    for _, _, geometry in layers:
        if not geometry.is_valid:
            raise ValueError("Invalid layer geometry")
    mesh = make_mesh(layers)
    (OUT / "STL").mkdir(exist_ok=True)
    path = OUT / "STL" / f"{stem}_Medallion_OnePiece_{version}.stl"
    write_stl(mesh, path)
    checks = check_mesh(path, f"mesh_check_{version}.json")
    save_svg(front, f"Front_Relief_{version}.svg")
    save_svg(back, f"Back_Engraving_{version}.svg")
    preview(disk, front, back, preview_filename, front_caption)
    analytic_volume = sum((top - bottom) * geometry.area for bottom, top, geometry in layers)
    if abs(checks["signed_volume_mm3"] - analytic_volume) > .02:
        raise ValueError("Mesh volume disagrees with the exact polygon layers")
    coupon_layers = [(0, ENGRAVE, disk.difference(mirrored_back)),
                     (ENGRAVE, 1.2, disk)]
    coupon_path = OUT / "STL" / f"{stem}_Back_Lettering_Test_1.2mm_{version}.stl"
    write_stl(make_mesh(coupon_layers), coupon_path)
    coupon_checks = check_mesh(coupon_path, f"lettering_test_mesh_check_{version}.json")
    coupon_volume = sum((top - bottom) * g.area for bottom, top, g in coupon_layers)
    if abs(coupon_checks["signed_volume_mm3"] - coupon_volume) > .02:
        raise ValueError("Test coupon volume mismatch")
    report = {
        "diameter_mm": DIAMETER, "body_top_mm": BODY_TOP, "total_height_mm": TOTAL_HEIGHT,
        "engraving_depth_mm": ENGRAVE, "front_relief_height_mm": TOTAL_HEIGHT - BODY_TOP,
        "front_maximum_radius_mm": radial_extent(front),
        "front_components": len(polys(front)), "front_trace": trace,
        "back": back_report, "analytic_volume_mm3": analytic_volume,
        "physical_print_test": False, "printer_profile_slice": False,
        "print_orientation": "Back engraving DOWN; yellow front relief UP",
        "assumed_nozzle_mm": .4,
    }
    (OUT / f"geometry_report_{version}.json").write_text(json.dumps(report, indent=2) + "\n")
    return report, checks


def package_files(root, archive, files):
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as package:
        for path in files:
            path = Path(path)
            package.write(path, path.relative_to(root).as_posix())
    with zipfile.ZipFile(archive) as package:
        if package.testzip() is not None:
            raise ValueError("Print archive integrity failed")
