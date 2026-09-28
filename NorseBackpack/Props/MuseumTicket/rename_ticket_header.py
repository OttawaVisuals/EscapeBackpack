"""Redraw the museum ticket's two title lines with a new place name (28 Sept 2026).

Made v5 from v4: the header band behind both title lines is repainted flat, then
"VIKING MUSEUM" / "OF BRATTAHLÍÐ" are drawn in a condensed bold serif and centred.
Usage (as run for v5):
  python rename_ticket_header.py C:/Windows/Fonts/constanb.ttf 0.82 Museum_Ticket_Front_300dpi_v5_transparent.png
Run from the repo root (SRC below is repo-relative).
"""
from PIL import Image, ImageDraw, ImageFont
import numpy as np, sys
SRC='NorseBackpack/Props/MuseumTicket/Museum_Ticket_Front_300dpi_v4_transparent.png'
def line_img(text,fontfile,cap,maxw,color,band,cond):
    size=10
    while True:
        ft=ImageFont.truetype(fontfile,size); bb=ft.getbbox('H')
        if bb[3]-bb[1]>=cap: break
        size+=1
    tb=ft.getbbox(text); w=tb[2]; h=tb[3]
    im=Image.new('RGBA',(w+20,h+40),band); d=ImageDraw.Draw(im)
    d.text((10,20),text,font=ft,fill=color)
    capt=20+ft.getbbox('H')[1]; capb=20+ft.getbbox('H')[3]
    nw=int((w+20)*cond); scale=1
    if nw-20>maxw: cond*=maxw/(nw-20); nw=int((w+20)*cond)
    im=im.resize((nw,im.height),Image.LANCZOS)
    return im,capt,capb
def build(fontfile,cond,out):
    src=Image.open(SRC).convert('RGBA'); a=np.asarray(src.convert('RGB')).astype(int)
    band=tuple(int(v) for v in a[115,20])+(255,)
    color=(247,245,235,255)
    d=ImageDraw.Draw(src); d.rectangle((14,30,586,170),fill=band)
    for text,cap,base in [('VIKING MUSEUM',60,104),('OF BRATTAHLÍÐ',36,163)]:
        im,ct,cb=line_img(text,fontfile,cap,524,color,band,cond)
        # trim horizontal padding to centre on ink
        arr=np.asarray(im.convert('RGB')).astype(int); cols=np.where((arr.sum(-1)>600).any(0))[0]
        x0=(600-(cols.max()-cols.min()))//2-cols.min()
        src.alpha_composite(im,(x0,base-cb))
    src.save(out)
if __name__=='__main__':
    build(sys.argv[1],float(sys.argv[2]),sys.argv[3])
