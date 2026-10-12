"""v2: existing flag-style maple leaf; Aurora's designer-supplied patch."""
from pathlib import Path
import math
import xml.etree.ElementTree as ET
import cv2
import numpy as np
from PIL import Image
from shapely.geometry import Point, Polygon, box
from shapely import affinity
from shapely.ops import unary_union
from fontTools.pens.basePen import BasePen
from fontTools.svgLib.path import parse_path
import medallion_cad as cad
try:
    from themed_medallion_fronts_v1 import canada as previous_canada, rim
except ModuleNotFoundError:
    from themed_medallion_fronts import canada as previous_canada, rim


class FlattenPen(BasePen):
    def __init__(self):
        super().__init__(None)
        self.rings, self.points = [], []
    def _moveTo(self, point):
        self.points = [point]
    def _lineTo(self, point):
        self.points.append(point)
    def _curveToOne(self, b, c, d):
        a = self.points[-1]
        for t in np.linspace(0, 1, 25)[1:]:
            u = 1-t
            self.points.append(tuple(u**3*a[i]+3*u*u*t*b[i]+3*u*t*t*c[i]+t**3*d[i]
                                     for i in (0,1)))
    def _qCurveToOne(self, b, c):
        a = self.points[-1]
        for t in np.linspace(0,1,25)[1:]:
            self.points.append(tuple((1-t)**2*a[i]+2*(1-t)*t*b[i]+t*t*c[i]
                                     for i in (0,1)))
    def _closePath(self):
        self.rings.append(self.points)
        self.points=[]
    def _endPath(self):
        if self.points: self.rings.append(self.points)
        self.points=[]


def maple_leaf(reference):
    root=ET.parse(reference).getroot()
    pen=FlattenPen()
    parse_path(root.find('{http://www.w3.org/2000/svg}path').attrib['d'],pen)
    leaf=Polygon()
    for ring in pen.rings:
        leaf=leaf.symmetric_difference(Polygon(ring).buffer(0))
    return leaf


def canada(reference):
    old, old_trace=previous_canada()
    old_leaf=next(p for p in cad.polys(old) if p.contains(Point(0,10)))
    unchanged=old.difference(old_leaf)
    leaf=affinity.scale(maple_leaf(reference), .005, -.005, origin=(0,0))
    leaf=affinity.translate(leaf,0,9).simplify(.002,preserve_topology=True)
    front=unary_union([unchanged,leaf])
    diff=old.symmetric_difference(front)
    outside=diff.difference(box(-12,-2.05,12,21)).area
    if outside>1e-7:
        raise ValueError('Train, rails or rim changed outside the leaf region')
    return front, {'method':'existing maple-leaf SVG outline with sampled curves',
                   'reference':str(reference),'source_scale_mm_per_unit':.005,
                   'outline_simplification_mm':.002,
                   'unchanged_train_rails_rim_difference_square_mm':outside}


def aurora(reference):
    rgb=np.array(Image.open(reference).convert('RGB'))
    # The supplied patch is a square, head-on badge. Its grey/white ink has low
    # chroma; crop inside its border so the outer ring can be rebuilt perfectly.
    size=min(rgb.shape[:2])
    cx=cy=size/2
    yy,xx=np.indices(rgb.shape[:2])
    low=rgb.min(axis=2).astype(float)
    high=rgb.max(axis=2).astype(float)
    mask=((low>150)&((high-low)<55)&(((xx-cx)**2+(yy-cy)**2)<(size*.411)**2))
    contours,tree=cv2.findContours(mask.astype(np.uint8)*255,
                                   cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    scale=50/(size*.98)
    tree=tree[0]
    def trace(c):
        p=cv2.approxPolyDP(c,.65,True).reshape(-1,2)
        return [((float(x)-cx)*scale,(cy-float(y))*scale) for x,y in p]
    parts=[]
    for i,c in enumerate(contours):
        depth,parent=0,int(tree[i][3])
        while parent>=0:
            depth+=1;parent=int(tree[parent][3])
        if depth%2 or cv2.contourArea(c)<20:continue
        holes=[trace(contours[j]) for j in range(len(contours))
               if int(tree[j][3])==i and cv2.contourArea(contours[j])>12]
        parts.extend(cad.polys(Polygon(trace(c),holes).buffer(0)))
    ink=unary_union(parts)
    # Slightly widen navy separations while preserving all substantial glyphs.
    ink=ink.buffer(-.035).buffer(.01).simplify(.004,preserve_topology=True)
    ink=unary_union([p for p in cad.polys(ink) if p.area>.08])
    front=unary_union([ink,rim()])
    return front,{'method':'white-ink contour trace from designer supplied patch',
                  'reference':str(reference),'source_pixels':list(rgb.shape[:2][::-1]),
                  'scale_mm_per_pixel':scale,'outer_rim':'exact shared circular CAD rim',
                  'foreground_net_inset_mm':.025,'outline_simplification_mm':.004,
                  'front_text':['STATION','AURORA']}


FRONTS={'Canada':canada,'Aurora':aurora}
