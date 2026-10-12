"""Printable vector fronts: Aurora station, Hockey Road Trip and Canada.

All coordinates are millimetres. Existing station/badge masters inform Aurora
and Hockey; manufacturing details are widened explicitly rather than rasterized.
"""
import math
import xml.etree.ElementTree as ET
from shapely.geometry import Point, Polygon, LineString, box
from shapely import affinity
from shapely.ops import unary_union, substring


def ellipse(cx, cy, rx, ry):
    return affinity.scale(Point(cx, cy).buffer(1, quad_segs=64), rx, ry)


def rounded_box(x0, y0, x1, y1, radius):
    return box(x0 + radius, y0 + radius, x1 - radius, y1 - radius).buffer(radius)


def rim():
    return Point(0, 0).buffer(23, quad_segs=144).difference(
        Point(0, 0).buffer(22.1, quad_segs=144))


def aurora(reference):
    # The SVG is preserved as the design reference; these are its measured layout
    # coordinates. Transform screen Y down into a physical Cartesian face.
    parts = [LineString([(142, 256), (370, 256)]).buffer(5.5),
             LineString([(256, 150), (256, 362)]).buffer(5.5)]
    for x in (95, 349):
        panel = rounded_box(x, 197, x + 68, 315, 5)
        cuts = [box(x + 20, 202, x + 25, 310),
                box(x + 43, 202, x + 48, 310)]
        cuts += [box(x + 5, y - 2.5, x + 63, y + 2.5) for y in (226, 256, 286)]
        parts.append(panel.difference(unary_union(cuts)))
    parts.extend([rounded_box(169, 221, 243, 291, 18),
                  rounded_box(269, 221, 343, 291, 18),
                  rounded_box(234, 139, 278, 216, 10),
                  rounded_box(234, 296, 278, 373, 10)])
    station = unary_union(parts)
    station = station.difference(Point(256, 256).buffer(42.5, quad_segs=64))
    station = unary_union([station,
        Point(256, 256).buffer(53.5, quad_segs=64).difference(
            Point(256, 256).buffer(42.5, quad_segs=64)),
        Point(256, 256).buffer(17, quad_segs=48)])
    station = affinity.translate(station, -256, -256)
    station = affinity.scale(station, .12, -.12, origin=(0, 0))
    orbit = LineString([(x, -16.5 - 1.5 * math.sin(math.pi * (x + 13) / 26))
                        for x in [i * 26 / 80 - 13 for i in range(81)]]).buffer(.4)
    front = unary_union([station, orbit, Point(13, -16.5).buffer(.8), rim()])
    return front, {"method": "vector CAD adapted from station SVG layout",
                   "reference": str(reference), "solar_grid_gap_mm": .6}


def hockey(reference):
    root = ET.parse(reference).getroot()
    ns = {"s": "http://www.w3.org/2000/svg"}
    # First polygon is the road clip; same vertices as the filled road.
    road = Polygon([tuple(map(float, p.split(',')))
                    for p in root.find('.//s:polygon', ns).attrib['points'].split()])
    centre = root.find('.//s:g/s:path', ns).attrib['d']
    pts = [tuple(map(float, p.split())) for p in centre[1:].split(' L')]
    lane = LineString(pts)
    def fit(g):
        return affinity.scale(affinity.translate(g, -312, -214), .085, -.085,
                              origin=(0, 0))
    road, lane = fit(road), fit(lane)
    # Preserve full walls beside lane slots, omitting dashes in the narrow tip.
    slots = []
    for i in range(int(lane.length / 4.14) + 1):
        a, b = i * 4.14 + .6, min(i * 4.14 + 2.94, lane.length)
        if b <= a: continue
        slot = substring(lane, a, b).buffer(.35)
        if road.contains(slot.buffer(.65)):
            slots.append(slot)
    road = road.difference(unary_union(slots))
    puck = unary_union([ellipse(446, 262, 82, 28), box(364, 262, 528, 312),
                        ellipse(446, 312, 82, 30)])
    puck = fit(puck)
    seam = fit(LineString([(446 + 82 * math.cos(t), 262 + 28 * math.sin(t))
                          for t in [i * math.pi / 80 for i in range(81)]]))
    puck = puck.difference(seam.buffer(.35))
    road = road.difference(puck.buffer(.75))
    front = unary_union([road, puck, rim()])
    return front, {"method": "existing road SVG polygon plus widened puck CAD",
                   "reference": str(reference), "road_lane_gap_mm": .7,
                   "puck_seam_gap_mm": .7, "road_to_puck_gap_mm": .75,
                   "lane_slots": len(slots)}


def canada(reference=None):
    # Maple-leaf vocabulary follows the existing Hockey badge family.
    leaf_points = [(0,-50),(11,-28),(30,-34),(24,-8),(44,-18),(36,8),
                   (22,6),(26,24),(2,18),(2,52),(-2,52),(-2,18),
                   (-26,24),(-22,6),(-36,8),(-44,-18),(-24,-8),
                   (-30,-34),(-11,-28)]
    leaf = Polygon([(x*.21, 9-y*.21) for x,y in leaf_points])
    train = rounded_box(-8, -15, 8, -3, 1.5)
    windows = [rounded_box(-6.1, -7.5, -.8, -4.7, .45),
               rounded_box(.8, -7.5, 6.1, -4.7, .45)]
    cuts = windows + [Point(0, -10).buffer(1.1)]
    cuts += [rounded_box(-4.6, y-.3, 4.6, y+.3, .2) for y in (-12, -13.4)]
    train = train.difference(unary_union(cuts))
    pilot = Polygon([(-6.5,-15.6),(6.5,-15.6),(8.5,-17.6),(-8.5,-17.6)])
    tracks = [LineString([(s*4.5,-18.4),(s*6.5,-20.1)]).buffer(.4)
              for s in (-1,1)]
    tracks.append(LineString([(-7,-19.5),(7,-19.5)]).buffer(.4))
    front = unary_union([leaf, train, pilot, *tracks, rim()])
    return front, {"method": "native vector maple leaf and front-facing train CAD",
                   "minimum_leaf_stem_width_mm": .84,
                   "train_grille_gap_mm": .6,
                   "motif": "maple leaf above train; no operator or team logo"}


FRONTS = {"Aurora": aurora, "Hockey": hockey, "Canada": canada}
