"""Aud v10: reviewer fixes for upright crossings and clear road fords."""
import sys,math,inspect,json
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
import render_full_map_v9 as R
S,V,M=R.S,R.V,R.M
HERE=Path(__file__).resolve().parent
OUT=HERE/"render_full_map_v10"
ORIGINAL_POINT=R.point
ORIGINAL_LINE=R.line
FORDS=[f["pts"][0] for f in R.FEATURES if f["kind"]=="ford"]
LOG={}
# Measured deck endpoints / hinge and latch post bases, pixel coords y down.
ANCHORS={
 "Bridge_Upright_90_v10":((627,1035),(627,315)),
 "Bridge_Upright_75_v10":((525,1060),(716,333)),
 "Bridge_Upright_14_v10":((234,878),(1111,647)),
 "Gate_Upright_10_v10":((439,748),(994,631)),
}
def place_upright(c,name,x,y,span,angle=None):
    reader,(iw,ih),b=V.asset(name)
    (ax,ay),(bx,by)=ANCHORS[name]
    dx,dy=bx-ax,ay-by
    cx,cy=(ax+bx)/2,ih-(ay+by)/2
    scale=span/math.hypot(dx,dy)
    # Native bridge pose, no rotation or shear. Gate uses only a small vertical perspective
    # correction; all screen-vertical posts remain screen-vertical.
    shear=0
    if angle is not None:
        scale=span*abs(math.cos(math.radians(angle)))/dx
        shear=math.tan(math.radians(angle))-dy/dx
    c.saveState(); c.translate(x,y)
    c.transform(scale,shear*scale,0,scale,0,0)
    p=c.beginPath(); p.rect(b[0]-cx-3,ih-b[3]-cy-3,b[2]-b[0]+6,b[3]-b[1]+6)
    c.clipPath(p,stroke=0,fill=0)
    c.drawImage(reader,-cx,-cy,iw,ih,mask="auto")
    c.restoreState()

def point(c,f,angle=0):
    k=f["kind"]; x,y=f["pts"][0]
    if k=="bridge":
        undirected=angle%180
        if 80<=undirected<=100: name="Bridge_Upright_90_v10"
        elif 68<=undirected<=80: name="Bridge_Upright_75_v10"
        elif 5<=undirected<=25: name="Bridge_Upright_14_v10"
        else: return ORIGINAL_POINT(c,f,angle)
        place_upright(c,name,x,y,16)
        LOG[str((x,y))]={"kind":k,"asset":name,"route_angle":angle,"image_rotation":0}
    elif k=="gate" and abs(angle)<=30:
        place_upright(c,"Gate_Upright_10_v10",x,y,10.5,angle)
        LOG[str((x,y))]={"kind":k,"asset":"Gate_Upright_10_v10","barrier_angle":angle,"image_rotation":0}
    elif k=="ford":
        c.saveState(); c.translate(x,y); c.rotate(angle+26)
        V.stamp(c,"Ford_Full_v9",0,0,18,10)
        c.restoreState()
        LOG[str((x,y))]={"kind":k,"stone_width":18,"road_cut_radius":8.5}
    else: ORIGINAL_POINT(c,f,angle)

def line(c,f,road_pass=None,gate_gaps=None):
    if f["kind"] not in ("road","path","track"): return ORIGINAL_LINE(c,f,road_pass,gate_gaps)
    # Exclude road ink while drawing it; do not paint over the already-drawn water.
    c.saveState(); p=c.beginPath(); p.rect(-100,-100,900,1100)
    for x,y in FORDS: p.circle(x,y,8.5)
    c.clipPath(p,stroke=0,fill=0,fillMode=0)
    ORIGINAL_LINE(c,f,road_pass,gate_gaps)
    c.restoreState()

def build():
    R.point=point; R.line=line; R.OUT=OUT
    # Preserve v9 as a review baseline; substitute only the output name in the build function.
    src=inspect.getsource(R.build).replace('"Aud_Full_Map_v9.pdf"','"Aud_Full_Map_v10.pdf"')
    exec(compile(src,str(HERE/"render_crossings_v10.py")+"::build","exec"),R.__dict__)
    R.build()
    ford_logs=[v for v in LOG.values() if v["kind"]=="ford"]
    assert len(ford_logs)==5
    # Every annotated gate/bridge point must have used an upright native view.
    expected=[(437.75,642.95),(463.91,550.32),(523.87,553.45),(521.67,657.7),
              (496.14,648.61),(525.58,501.67),(465.4,513.12),(360.92,416.94),(475.35,314.56)]
    assert all(str(p) in LOG for p in expected)
    (OUT/"crossing_changes.json").write_text(json.dumps(LOG,indent=2))
    print("PASS: all annotated crossing sites use upright views; all five fords have road exclusion.")

REGIONS=[
 ("1 - Gate",(418,630,35,26)),
 ("2 - Bridges",(457,538,83,29)),
 ("3 - Bridges",(487,640,49,38)),
 ("4 - Gates",(455,486,89,37)),
 ("5 - Bridge",(351,404,28,26)),
 ("6 - Bridge",(464,300,30,35)),
 ("7 - Ford",(324,600,16,27)),
]
def review():
    c=canvas.Canvas(str(OUT/"Aud_Crossing_Review_v10.pdf"),pagesize=(612,792))
    c.setFillColor(HexColor("#EFE3C4")); c.rect(0,0,612,792,fill=1,stroke=0)
    c.setFillColor(HexColor("#283B34")); c.setFont("Helvetica-Bold",15)
    c.drawString(24,767,"AUD - CROSSING CORRECTIONS")
    c.setFont("Helvetica",8)
    c.drawString(24,753,"Review of all seven annotated regions. Map geometry and ticket markers retained.")
    c.setFont("Helvetica-Bold",9)
    c.drawString(24,735,"BEFORE"); c.drawString(318,735,"AFTER")
    images=[HERE/"render_full_map_v9/Aud_Full_Map_v9.png",OUT/"Aud_Full_Map_v10.png"]
    for row,(label,(x,y,w,h)) in enumerate(REGIONS):
        top=716-row*94
        c.setFont("Helvetica-Bold",8); c.setFillColor(HexColor("#283B34"))
        c.drawString(24,top+5,label)
        for px,image in zip((24,318),images):
            pw,ph=270,76
            s=min(pw/(w+16),ph/(h+16))
            cx,cy=x+w/2,y+h/2
            c.saveState(); q=c.beginPath(); q.rect(px,top-ph,pw,ph); c.clipPath(q,stroke=0,fill=0)
            c.drawImage(str(image),px+pw/2-cx*s,top-ph/2-cy*s,612*s,792*s)
            c.restoreState()
    c.setFont("Helvetica",8); c.drawString(24,25,"Five fords: larger stones, road ink interrupted underneath, existing water left visible.")
    c.showPage(); c.save()
if __name__=="__main__":
    review() if "--review" in sys.argv else build()

