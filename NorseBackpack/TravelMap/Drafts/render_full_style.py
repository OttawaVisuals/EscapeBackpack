"""Full illustrated draft proof; isolated from live renderer and original style test."""
import sys, math, json, hashlib, shutil
from pathlib import Path
from PIL import Image
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
import render_style_test as S
HERE=Path(__file__).resolve().parent
ASSETS=S.ASSETS
OUT=HERE/"render_full_style"
DELIVERY=HERE/"render_baseline"
CACHE={}
POINTS={"port":("Landing_Boat_v2",12,13),"farm":("Farm_v1",18,13),
        "village":("Village_v1",17,15),"cave":("Cave_v1",18,12),
        "mill":("Mill_v1",18,15),"church":("Chapel_v2",12,16),
        "ruin":("Ruin_v2",14,12)}
# Reference anchors are pixel positions at the two deck ends / two post bases.
# Their midpoint is pinned to the JSON crossing. A vertical shear preserves upright posts.
CROSSINGS={
 "Bridge_Steep_v2":((530,279),(963,668)),
 "Bridge_Shallow_v2":((527,331),(996,601)),
 "Gate_Steep_v2":((461,681),(895,1010)),
}
used=set()
def asset(name):
    if name not in CACHE:
        im=Image.open(ASSETS/("Aud_"+name+".png")).convert("RGBA")
        b=im.getchannel("A").point(lambda a:255 if a>=220 else 0).getbbox()
        assert b is not None
        CACHE[name]=(ImageReader(im),im.size,b)
    return CACHE[name]

def stamp(c,name,x,y,w,h):
    reader,(iw,ih),b=asset(name); used.add(name)
    scale=min(w/(b[2]-b[0]),h/(b[3]-b[1]))
    cx=(b[0]+b[2])/2; cy=ih-(b[1]+b[3])/2
    c.saveState()
    p=c.beginPath(); p.rect(x-w/2-.25,y-h/2-.25,w+.5,h+.5); c.clipPath(p,stroke=0,fill=0)
    c.drawImage(reader,x-cx*scale,y-cy*scale,iw*scale,ih*scale,mask="auto")
    c.restoreState()

def crossing(c,name,x,y,angle,span):
    reader,(iw,ih),b=asset(name); used.add(name)
    (ax,ay),(bx,by)=CROSSINGS[name]
    # Image y is down; PDF y is up.
    dx=bx-ax; dy=ay-by
    a=math.radians(angle)
    scale=span*abs(math.cos(a))/dx
    shear=math.tan(a)-dy/dx
    cx=(ax+bx)/2; cy=ih-(ay+by)/2
    c.saveState(); c.translate(x,y)
    c.transform(scale,shear*scale,0,scale,0,0)
    p=c.beginPath(); p.rect(b[0]-cx-4,ih-b[3]-cy-4,b[2]-b[0]+8,b[3]-b[1]+8)
    c.clipPath(p,stroke=0,fill=0)
    c.drawImage(reader,-cx,-cy,iw,ih,mask="auto")
    c.restoreState()

def point(c,f,angle=0):
    k=f["kind"]; x,y=f["pts"][0]
    if k in POINTS:
        name,w,h=POINTS[k]; stamp(c,name,x,y,w,h)
    elif k=="bridge":
        name="Bridge_Steep_v2" if abs(angle)>45 else "Bridge_Shallow_v2"
        crossing(c,name,x,y,angle,16)
    elif k=="gate": crossing(c,"Gate_Steep_v2",x,y,angle,14)
    else: raise ValueError("No illustrated asset for draft point "+k)

def inside(pts,x,y):
    hit=False
    for i,(ax,ay) in enumerate(pts):
        bx,by=pts[i-1]
        if (ay>y)!=(by>y) and x<(bx-ax)*(y-ay)/(by-ay)+ax: hit=not hit
    return hit

def texture(c,f):
    k=f["kind"]; pts=f["pts"]
    if k not in ("wood","marsh"): return S.texture_original(c,f)
    x0,x1=min(x for x,y in pts),max(x for x,y in pts)
    y0,y1=min(y for x,y in pts),max(y for x,y in pts)
    step=13 if k=="wood" else 14
    c.saveState(); c.clipPath(S.base._path(c,f,True,f.get("smooth",False)),stroke=0,fill=0)
    # Stable jitter keeps the same polygon but avoids rows of identical symbols.
    for row,y in enumerate(range(int(y0)-step,int(y1)+step,step)):
        for col,x in enumerate(range(int(x0)-step,int(x1)+step,step)):
            tx=x+(row%2)*step/2+math.sin(col*7+row*3)*2
            ty=y+math.cos(col*3+row*5)*2
            w,h=(9+(col%3),11+(row%2)) if k=="wood" else (7,8)
            if all(inside(pts,tx+dx,ty+dy) for dx,dy in [(-w/2,-h/2),(w/2,-h/2),(-w/2,h/2),(w/2,h/2)]):
                stamp(c,"Tree_v2" if k=="wood" else "Marsh_Reeds_v2",tx,ty,w,h)
    c.restoreState()

def line(c,f,road_pass=None,gate_gaps=None):
    if f["kind"]!="hedge": return S.line_original(c,f,road_pass,gate_gaps)
    for j,(x,y,a) in enumerate(S.base._sample(f,False,f.get("smooth",False),4)):
        if any(math.hypot(x-gx,y-gy)<8.5 for gx,gy in (gate_gaps or [])): continue
        stamp(c,"Hedge_Bush_v2",x,y,6,3.8)

def legend(c,features,box,**kw):
    import importlib.util
    spec=importlib.util.spec_from_file_location("aud_full_legend",HERE.parent/"aud_layer.py")
    key=importlib.util.module_from_spec(spec); spec.loader.exec_module(key)
    def swatch(c,f):
        x,y=f["pts"][0]
        if f["kind"]=="wood": stamp(c,"Tree_v2",x+6,y+4,5,7); stamp(c,"Tree_v2",x+13,y+4,5,7)
        elif f["kind"]=="marsh": stamp(c,"Marsh_Reeds_v2",x+6,y+4,5,6); stamp(c,"Marsh_Reeds_v2",x+13,y+4,5,6)
        else: S.texture_original(c,f)
    def key_point(c,f,angle=0):
        x,y=f["pts"][0]
        if f["kind"]=="bridge": stamp(c,"Bridge_Shallow_v2",x,y,17,12)
        elif f["kind"]=="gate": stamp(c,"Gate_Steep_v2",x,y,12,13)
        else: point(c,f,angle)
    key._point=key_point; key._draw_line_feature=line; key._area_texture=swatch
    key.draw_legend(c,features,box,**kw)

def build_map():
    paths=[S.LAYER,HERE.parent/"aud_layer.py",HERE.parent/"aud_features.json"]
    before={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    features=S.load()[1]
    assert len(features)==20
    expected=S.base.crossing_angles(features)
    S.texture_original=S.texture; S.line_original=S.line
    S.texture=texture; S.line=line; S.point=point; S.draw_legend=legend; S.OUT=OUT
    S.main()
    assert expected==S.crossing_angles(S.load()[1])
    assert before=={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    DELIVERY.mkdir(exist_ok=True)
    shutil.copy2(OUT/"Trail_Map_3_Aud_Print.pdf",DELIVERY/"Aud_Full_Style_Draft_v2.pdf")
    (OUT/"validation.json").write_text(json.dumps({"features":20,"source_hashes":before,"crossing_angles":expected,"illustrated_assets_used":sorted(used),"geometry_unchanged":True},indent=2))
    print("PASS: all draft landmarks and vegetation use illustrated PNG assets.")

def comparison():
    c=canvas.Canvas(str(DELIVERY/"Aud_Full_Style_Comparison_v2.pdf"),pagesize=(792,612))
    c.setTitle("Aud draft: original and full illustrated style")
    c.setFillColor(HexColor("#EFE3C4")); c.rect(0,0,792,612,fill=1,stroke=0)
    c.setFillColor(HexColor("#283B34")); c.setFont("Helvetica-Bold",16)
    c.drawString(24,585,"AUD MAP - FULL STYLE COMPARISON")
    c.setFont("Helvetica",9); c.drawString(24,570,"Same 20-feature JSON; draft positions retained. Upper map shown below.")
    for x,name,label in [(24,"baseline.png","ORIGINAL SYMBOLS"),(408,"full-style-preview-v2.png","ILLUSTRATED STYLE")]:
        c.setFont("Helvetica-Bold",10); c.drawString(x,550,label)
        c.saveState(); p=c.beginPath(); p.rect(x,204,360,336); c.clipPath(p,stroke=0,fill=0)
        c.drawImage(str(DELIVERY/name),x,540-360*792/612,360,360*792/612)
        c.restoreState()
    c.setStrokeColor(HexColor("#B09D77")); c.line(24,192,768,192)
    c.setFont("Helvetica-Bold",10); c.drawString(24,176,"ARTWORK USED IN THE MAP")
    samples=[("Chapel_v2","Chapel"),("Ruin_v2","Ruin"),("Bridge_Steep_v2","Bridge / steep"),
             ("Bridge_Shallow_v2","Bridge / shallow"),("Gate_Steep_v2","Gate"),
             ("Tree_v2","Wood"),("Hedge_Bush_v2","Hedge"),("Marsh_Reeds_v2","Marsh")]
    for i,(name,label) in enumerate(samples):
        x=69+i*93
        stamp(c,name,x,120,64,64)
        c.setFillColor(HexColor("#283B34")); c.setFont("Helvetica",8); c.drawCentredString(x,73,label)
    c.setFont("Helvetica",8)
    c.drawString(24,44,"Crossings use perspective placement to follow the unchanged road/barrier directions.")
    c.drawString(24,30,"Preview only: original symbol size classes retained; physical print readability not tested.")
    c.showPage(); c.save()

if __name__=="__main__":
    comparison() if "--comparison" in sys.argv else build_map()

