"""Render three native CAD fronts together for comparison; no raster art input."""
from pathlib import Path
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import medallion_cad as cad
from themed_medallion_fronts import FRONTS
from shapely.geometry import Point

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / 'EscapeBackpack/output/medallions/Three_New_Medallions_v1.png'
CONFIG = [('Aurora', 'Space Station Aurora', ROOT/'Space-Station-Aurora/source/Brand/icon.svg'),
          ('Hockey', 'Hockey Road Trip', ROOT/'Hockey-Expedition/assets/identity/icon.svg'),
          ('Canada', 'Canada Exploration', None)]
canvas = Image.new('RGB', (1440, 620), '#F7F4E9')
draw = ImageDraw.Draw(canvas)
font = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', 27)
small = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 22)
disk = Point(0, 0).buffer(25, quad_segs=144)
for i, (stem, name, reference) in enumerate(CONFIG):
    front, trace = FRONTS[stem](reference)
    if stem == 'Aurora': front = front.simplify(.005, preserve_topology=True)
    body, detail = cad.raster(disk, 450), cad.raster(front, 450)
    pixels = np.full((450,450,3), [247,244,233], dtype=np.uint8)
    pixels[body] = [26,55,89]
    pixels[detail] = [255,210,32]
    canvas.paste(Image.fromarray(pixels), (15+i*480, 75))
    draw.text((240+i*480, 33), name, font=font, fill='#1A3759', anchor='mm')
draw.text((720, 554), '50 mm / navy body + yellow relief / shared improved engraved back',
          font=small, fill='#1A3759', anchor='mm')
draw.text((720, 588), 'CAD profiles — physical printing remains untested',
          font=small, fill='#526474', anchor='mm')
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
canvas.save(OUTPUT)
print(OUTPUT)
