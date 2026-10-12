"""Compare revised native CAD profiles without editing raster inputs."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import medallion_cad as cad
from revised_medallion_fronts import FRONTS
from shapely.geometry import Point

ROOT=Path(__file__).resolve().parents[2]
OUTPUT=ROOT/'EscapeBackpack/output/medallions/Revised_Aurora_Canada_v2.png'
items=[('Aurora','Space Station Aurora',ROOT/'Space-Station-Aurora/assets/medallion/sources/Aurora_Patch_Reference_v2.jpg'),
       ('Canada','Canada Exploration',ROOT/'Canada-Exploration/assets/medallion/sources/Maple_Leaf_Reference.svg')]
canvas=Image.new('RGB',(1200,720),'#F7F4E9')
draw=ImageDraw.Draw(canvas)
font=ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',31)
small=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',24)
disk=Point(0,0).buffer(25,quad_segs=144)
for i,(stem,title,reference) in enumerate(items):
    front,trace=FRONTS[stem](reference)
    body,ink=cad.raster(disk,540),cad.raster(front,540)
    pixels=np.full((540,540,3),[247,244,233],dtype=np.uint8)
    pixels[body]=[26,55,89];pixels[ink]=[255,210,32]
    canvas.paste(Image.fromarray(pixels),(30+i*600,75))
    draw.text((300+i*600,35),title,font=font,fill='#1A3759',anchor='mm')
draw.text((600,649),'Revised v2 fronts / unchanged improved back / 50 mm',font=small,fill='#1A3759',anchor='mm')
draw.text((600,688),'CAD previews — physical printing remains untested',font=small,fill='#526474',anchor='mm')
OUTPUT.parent.mkdir(parents=True,exist_ok=True)
canvas.save(OUTPUT)
print(OUTPUT)
