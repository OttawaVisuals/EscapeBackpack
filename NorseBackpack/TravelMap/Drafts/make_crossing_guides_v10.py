"""Pose guides only: lock deck axes and upright posts for generated crossing art."""
from pathlib import Path
import math
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
HERE=Path(__file__).resolve().parent
OUT=HERE/"crossing_guides_v10"; OUT.mkdir(exist_ok=True)
def poly(c,pts,fill="#F4EEDD"):
    p=c.beginPath(); p.moveTo(*pts[0])
    for q in pts[1:]: p.lineTo(*q)
    p.close(); c.setFillColor(HexColor(fill)); c.drawPath(p,fill=1,stroke=1)
for name,angle in [("Bridge_90",90),("Bridge_75",75),("Bridge_14",14),("Gate_10",10)]:
    c=canvas.Canvas(str(OUT/(name+".pdf")),pagesize=(800,800))
    c.setFillColor(HexColor("#EFE3C4")); c.rect(0,0,800,800,fill=1,stroke=0)
    c.setStrokeColor(HexColor("#614773")); c.setLineWidth(9); c.setLineJoin(1); c.setLineCap(1)
    a=math.radians(angle)
    def q(u,v=0,h=0): return (400+u*math.cos(a)-v*math.sin(a),355+u*math.sin(a)+v*math.cos(a)+h)
    if name.startswith("Bridge"):
        # Upright posts share the same screen vertical, independently of deck travel direction.
        poly(c,[q(-220,-90,-30),q(220,-90,-30),q(220,-90),q(-220,-90)],"#DACEB6")
        poly(c,[q(-220,-90),q(220,-90),q(220,90),q(-220,90)])
        for u in [-145,-73,0,73,145]: c.line(*q(u,-90),*q(u,90))
        for v in [90,-90]:
            for u in [-220,220]:
                x,y=q(u,v)
                poly(c,[(x-13,y),(x+13,y),(x+13,y+110),(x-13,y+110)])
            p1=q(-220,v,85); p2=q(220,v,85)
            c.setLineWidth(15); c.line(*p1,*p2); c.setLineWidth(9)
    else:
        # Two latch/hinge post bases follow the wall direction; leaf is fully open toward viewer.
        for u in [-220,220]:
            x,y=q(u)
            poly(c,[(x-18,y),(x+18,y),(x+18,y+150),(x-18,y+150)])
        # Swung leaf goes down-left on the map, no connection across the passage.
        hinge=q(-220)
        far=(hinge[0]-90,hinge[1]-165)
        poly(c,[(hinge[0],hinge[1]+30),(far[0],far[1]+30),(far[0],far[1]+130),(hinge[0],hinge[1]+130)])
        c.line(hinge[0],hinge[1]+30,far[0],far[1]+130)
    c.showPage(); c.save()

