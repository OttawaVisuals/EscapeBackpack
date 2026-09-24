"""Trace ImageGen coin masks into closed SVG profiles and matching PNG previews.

Run with Python + Pillow, numpy, opencv-python-headless, shapely.
Sources are copied once from generation_manifest.json; later rebuilds use local copies.
No coin diameter, thickness, relief height or printer tolerance is assumed.
"""
from pathlib import Path
import html
import json
import shutil
import zipfile
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from shapely.geometry import Polygon
from shapely.geometry.polygon import orient
from shapely import affinity

ROOT = Path(__file__).resolve().parent
manifest = json.loads((ROOT / 'generation_manifest.json').read_text(encoding='utf-8'))
(ROOT / 'sources').mkdir(exist_ok=True)
checks = []
previews = []
for entry in manifest:
    name = entry['id']
    source = ROOT / 'sources' / (name + '.png')
    if not source.exists():
        shutil.copy2(entry['sourcePath'], source)
    raw = Image.open(source).convert('RGBA')
    white = Image.new('RGBA', raw.size, 'white')
    white.alpha_composite(raw)
    mask = (np.array(white.convert('L')) < 128).astype('uint8') * 255
    contours, tree = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    tree = tree[0]
    polys = []
    def points(c):
        return cv2.approxPolyDP(c, 0.7, True).reshape(-1, 2)
    for i, contour in enumerate(contours):
        depth, parent = 0, tree[i][3]
        while parent >= 0:
            depth += 1
            parent = tree[parent][3]
        if depth % 2 or cv2.contourArea(contour) < 24:
            continue
        shell = points(contour)
        holes = [points(c) for j, c in enumerate(contours)
                 if tree[j][3] == i and cv2.contourArea(c) >= 160]
        p = Polygon(shell, holes)
        if not p.is_valid:
            p = p.buffer(0)
        polys.extend(list(p.geoms) if p.geom_type == 'MultiPolygon' else [p])
    assert polys and all(p.is_valid and p.area > 0 for p in polys)
    minx = min(p.bounds[0] for p in polys)
    miny = min(p.bounds[1] for p in polys)
    maxx = max(p.bounds[2] for p in polys)
    maxy = max(p.bounds[3] for p in polys)
    cx, cy = (minx+maxx)/2, (miny+maxy)/2
    radius = max(((x-cx)**2+(y-cy)**2)**0.5
                 for p in polys for x, y in p.exterior.coords)
    scale = 460/radius
    polys = [orient(affinity.translate(affinity.scale(p, scale, scale, origin=(cx,cy)),
                    500-cx, 500-cy), sign=1.0) for p in polys]
    paths = []
    for p in polys:
        for ring in [p.exterior, *p.interiors]:
            xy = list(ring.coords)[:-1]
            paths.append('M ' + ' L '.join(f'{x:.3f},{y:.3f}' for x,y in xy) + ' Z')
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="1000" '
           'viewBox="0 0 1000 1000">\n'
           f'<title>{html.escape(entry["name"])} relief profile</title>\n'
           '<desc>Closed black relief shapes, no coin blank. Normalized 1000-unit canvas; '
           'art fits a radius of 460 around 500,500. Scale to chosen coin size.</desc>\n'
           '<path fill="#000000" fill-rule="nonzero" d="' + ' '.join(paths) + '"/>\n</svg>\n')
    (ROOT / (name+'.svg')).write_text(svg, encoding='utf-8')
    out = Image.new('1', (2000,2000), 1)
    draw = ImageDraw.Draw(out)
    for p in polys:
        draw.polygon([(round(x*2),round(y*2)) for x,y in p.exterior.coords], fill=0)
        for ring in p.interiors:
            draw.polygon([(round(x*2),round(y*2)) for x,y in ring.coords], fill=1)
    out.save(ROOT / (name+'.png'))
    previews.append(out.convert('RGB'))
    checks.append({'id':name, 'closed_valid_components':len(polys),
                   'holes':sum(len(p.interiors) for p in polys),
                   'png_size':[2000,2000], 'art_radius_canvas_units':460})

sheet = Image.new('RGB',(1600,910),'#f1f1ed')
d = ImageDraw.Draw(sheet)
font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf',24)
small = ImageFont.truetype('C:/Windows/Fonts/arial.ttf',20)
for i,(entry,preview) in enumerate(zip(manifest,previews)):
    x,y = 20+(i%4)*395, 20+(i//4)*440
    sheet.paste(preview.resize((360,360),Image.Resampling.LANCZOS),(x,y))
    d.text((x,y+372),entry['name'],fill='black',font=font)
d.text((1205,475),'COIN FACE ARTWORK',fill='black',font=font)
d.text((1205,520),'Black = raised detail\nSVG + PNG per design\nScale in modelling software\nCoin blank not included\nPhysical print test pending',fill='black',font=small,spacing=12)
sheet.save(ROOT / 'Coin_Faces_Overview.png')
(ROOT / 'validation.json').write_text(json.dumps(checks,indent=2)+'\n',encoding='utf-8')
with zipfile.ZipFile(ROOT / 'Coin_Face_Artwork.zip','w',zipfile.ZIP_DEFLATED) as z:
    for entry in manifest:
        for ext in ('.svg','.png'):
            z.write(ROOT/(entry['id']+ext),entry['id']+ext)
    z.write(ROOT/'Coin_Faces_Overview.png','Coin_Faces_Overview.png')
    if (ROOT/'README.md').exists():
        z.write(ROOT/'README.md','README.md')
print(json.dumps(checks,indent=2))
