"""Isolated Aud style proof. Never modifies live renderer or draft geometry."""
import sys, math, json, hashlib
from pathlib import Path
from PIL import Image
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import aud_layer as base
import build_trail_maps_pdf as M

LAYER = HERE / "aud_features_draft_2026-10-16.json"
ASSETS = HERE.parents[1] / "Art" / "MapIcons"
OUT = HERE / "render_style"
LINE, AREA = base.LINE, base.AREA
assert_frame, crossing_angles = base.assert_frame, base.crossing_angles
def load(path=None):
    return base.load(path or LAYER)
INK, PAPER = "#614773", "#F4EEDD"
images = {}

def poly(c, pts, fill, stroke, width=.45):
    p = c.beginPath(); p.moveTo(*pts[0])
    for q in pts[1:]: p.lineTo(*q)
    p.close()
    c.setFillColor(HexColor(fill)); c.setStrokeColor(HexColor(stroke)); c.setLineWidth(width)
    c.drawPath(p, fill=1, stroke=1)

def tree(c,x,y,size=1,conifer=False):
    c.saveState(); c.translate(x,y); c.scale(size,size)
    c.setStrokeColor(HexColor("#56603D")); c.setLineWidth(.45)
    c.line(0,-3,0,3)
    if conifer:
        poly(c,[(-3,0),(-1.8,2),(-2.3,2),(0,7),(2.3,2),(1.8,2),(3,0)],"#859367","#47603C")
        c.line(0,0,0,4)
    else:
        c.setFillColor(HexColor("#899967"))
        for dx,dy,r in [(-1.8,2.1,1.9),(1.6,2.4,2),(0,4.4,2.3),(0,1.9,2)]:
            c.circle(dx,dy,r,stroke=0,fill=1)
        p=c.beginPath(); p.moveTo(-3.5,1)
        p.curveTo(-5,4,-2,5,-1.5,5); p.curveTo(-2,8,2,8,2.1,5)
        p.curveTo(5,5,5,1.5,2,1); p.curveTo(1,-.4,-2,-.2,-3.5,1)
        c.drawPath(p,stroke=1,fill=0)
        c.line(0,-1,0,3); c.line(0,1,-1.5,2); c.line(0,1.5,1.4,3)
    c.restoreState()

def texture(c,f):
    k=f["kind"]; pts=f["pts"]
    x0,x1=min(x for x,y in pts),max(x for x,y in pts)
    y0,y1=min(y for x,y in pts),max(y for x,y in pts)
    c.saveState(); c.clipPath(base._path(c,f,True,f.get("smooth",False)),stroke=0,fill=0)
    c.setLineCap(1); c.setLineWidth(.45)
    def inside(x,y):
        hit=False
        for i,(ax,ay) in enumerate(pts):
            bx,by=pts[i-1]
            if (ay>y)!=(by>y) and x<(bx-ax)*(y-ay)/(by-ay)+ax: hit=not hit
        return hit
    if k=="wood":
        for row,y in enumerate(range(int(y0)-7,int(y1)+10,13)):
            for col,x in enumerate(range(int(x0)-7,int(x1)+10,13)):
                tx=x+(row%2)*6+math.sin(col*7+row*3)*2
                ty=y+math.cos(col*3+row*5)*2
                if all(inside(tx+dx,ty+dy) for dx,dy in [(-4,0),(4,0),(0,7),(0,-3)]):
                    tree(c,tx,ty,.85+(col%3)*.06,conifer=(col+row)%3==0)
    elif k in ("marsh","moor"):
        col="#386D66" if k=="marsh" else "#927044"
        c.setStrokeColor(HexColor(col))
        for row,y in enumerate(range(int(y0)-5,int(y1)+8,12)):
            for x in range(int(x0)-5,int(x1)+8,14):
                xx=x+(row%2)*6
                for dx,dy in [(-2,2),(-1,4),(0,5),(1,3),(2.3,2)]:
                    c.line(xx,y,xx+dx,y+dy)
                if k=="marsh":
                    c.setStrokeColor(HexColor("#5D9694")); c.line(xx-3,y-1.6,xx+3,y-1.6)
                    c.setStrokeColor(HexColor(col))
    elif k=="field":
        c.setStrokeColor(HexColor("#A58150")); c.setLineWidth(.42)
        for x in range(int(x0)-50,int(x1)+50,7):
            c.line(x,y0-5,x+18,y1+5)
    c.restoreState()

def line(c,f,road_pass=None,gate_gaps=None):
    k=f["kind"]; s=LINE[k]; w=f.get("w") or s["w"]
    path=base._path(c,f,False,f.get("smooth",s.get("smooth",False)))
    c.setLineCap(1); c.setLineJoin(1); c.setDash()
    if k=="road":
        if road_pass in (None,"casing"):
            c.setStrokeColor(HexColor("#805A38")); c.setLineWidth(w+1.1); c.drawPath(path)
        if road_pass in (None,"fill"):
            c.setStrokeColor(HexColor("#F6E5BC")); c.setLineWidth(max(.2,w-.6)); c.drawPath(path)
    elif k in ("river","stream"):
        c.setStrokeColor(HexColor("#286D70")); c.setLineWidth(w+(1.2 if k=="river" else .25)); c.drawPath(path)
        c.setStrokeColor(HexColor("#78AAA7")); c.setLineWidth(max(.3,w-.15)); c.drawPath(path)
    elif k in ("hedge","wall"):
        for j,(x,y,a) in enumerate(base._sample(f,False,f.get("smooth",False),3.8)):
            if any(math.hypot(x-gx,y-gy)<8.5 for gx,gy in (gate_gaps or [])): continue
            if k=="hedge":
                c.setStrokeColor(HexColor("#496038")); c.setFillColor(HexColor("#81905C")); c.setLineWidth(.4)
                c.circle(x,y,2.1+(j%3)*.15,stroke=1,fill=1)
                c.circle(x+.7,y+.7,1,stroke=0,fill=1)
            else:
                ca,sa=math.cos(a),math.sin(a)
                pts=[(-1.8,-1),(-1.8,.8),(-.8,2),(1.4,1.5),(1.9,-.7)]
                poly(c,[(x+u*ca-v*sa,y+u*sa+v*ca) for u,v in pts],"#A6A897","#666354")
    else:
        base._draw_line_feature(c,f,road_pass,gate_gaps)

def raster(c,k,x,y):
    files={"port":"Landing_Boat_v2","farm":"Farm_v1","village":"Village_v1","cave":"Cave_v1","mill":"Mill_v1"}
    if k not in files: return False
    name=files[k]
    if name not in images:
        im=Image.open(ASSETS/("Aud_"+name+".png")).convert("RGBA")
        # Measure the solid symbol without changing any image pixels.
        b=im.getchannel("A").point(lambda a:255 if a>=220 else 0).getbbox()
        images[name]=(ImageReader(im),im.size,b)
    reader,(iw,ih),b=images[name]
    # Fit visible content in the original landmark size class.
    maxw,maxh=({"port":(12,13),"farm":(18,13),"village":(17,15),"cave":(18,12),"mill":(18,15)})[k]
    scale=min(maxw/(b[2]-b[0]),maxh/(b[3]-b[1]))
    cx=(b[0]+b[2])/2; cy=ih-(b[1]+b[3])/2
    c.saveState()
    p=c.beginPath(); p.rect(x-maxw/2-1,y-maxh/2-1,maxw+2,maxh+2)
    c.clipPath(p,stroke=0,fill=0)
    c.drawImage(reader,x-cx*scale,y-cy*scale,iw*scale,ih*scale,mask="auto")
    c.restoreState()
    return True

def point(c,f,angle=0):
    k=f["kind"]; x,y=f["pts"][0]
    c.saveState()
    if raster(c,k,x,y): c.restoreState(); return
    c.setStrokeColor(HexColor(INK)); c.setFillColor(HexColor(PAPER)); c.setLineWidth(.6)
    if k=="church":
        poly(c,[(x-5,y-5),(x+3,y-5),(x+3,y+2),(x-1,y+6),(x-5,y+2)],PAPER,INK)
        poly(c,[(x+3,y-5),(x+7,y-2),(x+7,y+4),(x+3,y+2)],"#E4DCC7",INK)
        poly(c,[(x-1,y+6),(x+3,y+2),(x+7,y+4),(x+3,y+8)],PAPER,INK)
        c.setFillColor(HexColor(INK)); c.rect(x-2,y-5,2,4,fill=1,stroke=0)
        c.line(x-1,y+6,x-1,y+11); c.line(x-3,y+9,x+1,y+9)
    elif k=="ruin":
        poly(c,[(x-7,y-5),(x-7,y+3),(x-4,y+3),(x-4,y+6),(x-1,y+6),(x-1,y+1),(x+3,y+2),(x+3,y-5)],PAPER,INK)
        poly(c,[(x+3,y-5),(x+7,y-2),(x+7,y+3),(x+5,y+2),(x+5,y+5),(x+3,y+4)],"#E4DCC7",INK)
        c.setFillColor(HexColor(INK)); c.rect(x-4,y-5,2.5,4,stroke=0,fill=1)
        c.line(x-7,y-1,x-4,y-1)
    elif k in ("bridge","gate"):
        a=math.radians(angle)
        def q(u,v=0,h=0): return (x+u*math.cos(a)-v*math.sin(a),y+u*math.sin(a)+v*math.cos(a)+h)
        if k=="bridge":
            poly(c,[q(-8,-3),q(8,-3),q(8,3),q(-8,3)],PAPER,INK,.7)
            for u in (-4,0,4): c.line(*q(u,-3),*q(u,3))
            for v in (-3,3):
                c.line(*q(-8,v),*q(-8,v,3)); c.line(*q(8,v),*q(8,v,3))
                c.line(*q(-8,v,3),*q(8,v,3))
        else:
            for u in (-7,7):
                c.setLineWidth(1.1); c.line(*q(u,0,-4),*q(u,0,5))
            poly(c,[q(-7,0,-2),q(1,3,-2),q(1,3,3),q(-7,0,3)],PAPER,INK,.7)
            c.line(*q(-7,0,-2),*q(1,3,3))
    else: base._point(c,f,angle)
    c.restoreState()

def draw(c,features,clip_rect=None):
    c.saveState()
    if clip_rect:
        p=c.beginPath(); p.rect(clip_rect[0],clip_rect[1],clip_rect[2]-clip_rect[0],clip_rect[3]-clip_rect[1])
        c.clipPath(p,stroke=0,fill=0)
    for f in features:
        if f["kind"] in AREA and len(f["pts"])>2:
            if f["kind"]=="field":
                c.setStrokeColor(HexColor("#9A7545")); c.setLineWidth(.5)
                c.drawPath(base._path(c,f,True,f.get("smooth",False)),fill=0,stroke=1)
            texture(c,f)
    gaps=[f["pts"][0] for f in features if f["kind"]=="gate"]
    for f in features:
        if f["kind"] in LINE and f["kind"]!="road" and len(f["pts"])>1: line(c,f,gate_gaps=gaps)
    for stage in ("casing","fill"):
        for f in features:
            if f["kind"]=="road" and len(f["pts"])>1: line(c,f,stage)
    angles=crossing_angles(features)
    for crossing in (False,True):
        for i,f in enumerate(features):
            if len(f["pts"])==1 and (f["kind"] in ("bridge","ford","gate"))==crossing:
                point(c,f,angles.get(i,0))
    c.restoreState()

def draw_legend(c,features,box,**kw):
    # Use the existing key layout with this proof's own swatches, in a separate module instance.
    import importlib.util
    spec=importlib.util.spec_from_file_location("aud_proof_legend",HERE.parent/"aud_layer.py")
    key=importlib.util.module_from_spec(spec); spec.loader.exec_module(key)
    def swatch(c,f):
        x0,y0=f["pts"][0]
        if f["kind"]=="wood": tree(c,x0+6,y0+2,.65); tree(c,x0+13,y0+2,.65,True)
        elif f["kind"]=="marsh":
            c.setStrokeColor(HexColor("#386D66")); c.setLineWidth(.45)
            for x in (x0+5,x0+12):
                for dx,dy in [(-2,2),(0,4),(2,3)]: c.line(x,y0+1,x+dx,y0+1+dy)
        else: texture(c,f)
    key._draw_line_feature=line; key._area_texture=swatch; key._point=point
    key.draw_legend(c,features,box,**kw)

def main():
    assert len(load()[1]) == 20, 'Expected the 20-feature draft, not the live layer'
    before=hashlib.sha256(LAYER.read_bytes()).hexdigest()
    live=hashlib.sha256((HERE.parent/"aud_layer.py").read_bytes()).hexdigest()
    OUT.mkdir(exist_ok=True)
    M.OUT_DIR=OUT
    M.aud_layer=sys.modules[__name__]
    # Cache/decoy marks are live-map additions, absent from this draft JSON.
    M.draw_aud_cache_mark=lambda c:None
    result=M.build("aud",M.TRAILS["aud"],M.load_plan(),M.load_corpus())
    assert not result, result
    assert hashlib.sha256(LAYER.read_bytes()).hexdigest()==before
    assert hashlib.sha256((HERE.parent/"aud_layer.py").read_bytes()).hexdigest()==live
    assert crossing_angles(load()[1])==base.crossing_angles(load()[1])
    print("PASS: draft geometry and live renderer unchanged; crossing angles preserved.")
if __name__=="__main__": main()

