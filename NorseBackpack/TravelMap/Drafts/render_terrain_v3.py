"""Aud v3: mixed woodland, decorated water, grid below art, enlarged landmarks."""
import sys, math, json, hashlib, inspect, shutil, random
from pathlib import Path
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
import render_full_style as V
S=V.S; M=S.M
HERE=Path(__file__).resolve().parent
OUT=HERE/"render_style_v3"
DELIVERY=HERE/"render_baseline"
FEATURES=S.load()[1]
CROSS=[f["pts"][0] for f in FEATURES if f["kind"] in ("bridge","gate","ford")]
LANDMARKS=[f["pts"][0] for f in FEATURES if len(f["pts"])==1]
SCALE=1.3
LOG=[]
def near(x,y,points,r):
    return any(math.hypot(x-px,y-py)<r for px,py in points)

def bridge(c,name,x,y,angle,span=16):
    # Rigid placement: NO shear or nonuniform stretch of the bridge artwork.
    reader,(iw,ih),b=V.asset(name); V.used.add(name)
    endpoints={"Bridge_River_v3":((516,274),(1006,724)),
               "Bridge_Shallow_v2":V.CROSSINGS["Bridge_Shallow_v2"]}
    (ax,ay),(bx,by)=endpoints[name]
    native=math.degrees(math.atan2(ay-by,bx-ax))
    scale=span/math.hypot(bx-ax,by-ay)
    cx=(ax+bx)/2; cy=ih-(ay+by)/2
    c.saveState(); c.translate(x,y); c.rotate(angle-native)
    c.scale(scale,scale)
    p=c.beginPath(); p.rect(b[0]-cx-3,ih-b[3]-cy-3,b[2]-b[0]+6,b[3]-b[1]+6)
    c.clipPath(p,stroke=0,fill=0)
    c.drawImage(reader,-cx,-cy,iw,ih,mask="auto")
    c.restoreState()

def point(c,f,angle=0):
    k=f["kind"]; x,y=f["pts"][0]
    if k in V.POINTS:
        name,w,h=V.POINTS[k]; V.stamp(c,name,x,y,w*SCALE,h*SCALE)
    elif k=="bridge":
        bridge(c,"Bridge_River_v3" if abs(angle)>45 else "Bridge_Shallow_v2",x,y,angle)
    elif k=="gate":
        V.crossing(c,"Gate_Steep_v2",x,y,angle,14*SCALE)
    else: raise ValueError(k)

def wood(c,f):
    pts=f["pts"]; x0,x1=min(x for x,y in pts),max(x for x,y in pts)
    y0,y1=min(y for x,y in pts),max(y for x,y in pts)
    rng=random.Random(round(x0*71+y0*37))
    trees=[]
    for row,y in enumerate(range(int(y0)-10,int(y1)+12,15)):
        for col,x in enumerate(range(int(x0)-10,int(x1)+12,15)):
            tx=x+(row%2)*7+rng.uniform(-4.2,4.2); ty=y+rng.uniform(-4,4)
            choice=(col+2*row)%6
            name="Conifer_v3" if choice in (0,3) else ("Birch_v3" if choice==2 else "Tree_v2")
            w,h=(8.5,15.5) if name=="Conifer_v3" else (10.5,12)
            factor=SCALE*rng.uniform(.82,1.12); w*=factor; h*=factor
            if near(tx,ty,LANDMARKS,12): continue
            if all(V.inside(pts,tx+dx,ty+dy) for dx,dy in [(-w/2,-h/2),(w/2,-h/2),(-w/2,h/2),(w/2,h/2)]):
                trees.append((tx,ty,name,w,h))
    for x,y,name,w,h in sorted(trees,key=lambda q:-q[1]): V.stamp(c,name,x,y,w,h)

def texture(c,f):
    k=f["kind"]; pts=f["pts"]
    c.saveState(); c.clipPath(S.base._path(c,f,True,f.get("smooth",False)),stroke=0,fill=0)
    if k=="wood": wood(c,f)
    elif k=="marsh":
        rng=random.Random(771)
        x0,x1=min(x for x,y in pts),max(x for x,y in pts)
        y0,y1=min(y for x,y in pts),max(y for x,y in pts)
        for row,y in enumerate(range(int(y0),int(y1),14)):
            for x in range(int(x0),int(x1),14):
                tx=x+(row%2)*6+rng.uniform(-2,2); ty=y+rng.uniform(-2,2)
                if not V.inside(pts,tx,ty): continue
                if all(V.inside(pts,tx+dx,ty+dy) for dx,dy in [(-4,-5),(4,5)]):
                    V.stamp(c,"Marsh_Reeds_v2",tx,ty,8*SCALE,8*SCALE)
                    c.setStrokeColor(HexColor("#609E9B")); c.setLineWidth(.45)
                    c.line(tx-5,ty-4.2,tx-1,ty-4.2); c.line(tx+1,ty-3,tx+5,ty-3)
    elif k=="field":
        x0,x1=min(x for x,y in pts),max(x for x,y in pts)
        y0,y1=min(y for x,y in pts),max(y for x,y in pts)
        c.setStrokeColor(HexColor("#9C7949")); c.setLineWidth(.5)
        for y in range(int(y0)-6,int(y1)+6,7):
            p=c.beginPath(); p.moveTo(x0-5,y)
            p.curveTo(x0+(x1-x0)*.3,y+3,x0+(x1-x0)*.7,y-3,x1+5,y+1)
            c.drawPath(p,stroke=1,fill=0)
    else: S.texture_original(c,f)
    c.restoreState()

def line(c,f,road_pass=None,gate_gaps=None):
    k=f["kind"]
    if k in ("river","stream"):
        w=f.get("w") or S.LINE[k]["w"]
        smooth=f.get("smooth",True)
        p=S.base._path(c,f,False,smooth)
        outer=w+3.0 if k=="river" else w+.8
        inner=outer-.8 if k=="river" else outer-.4
        c.setLineCap(1); c.setLineJoin(1)
        c.setStrokeColor(HexColor("#286D70")); c.setLineWidth(outer); c.drawPath(p)
        c.setStrokeColor(HexColor("#78AAA7")); c.setLineWidth(inner); c.drawPath(p)
        samples=S.base._sample(f,False,smooth,1.2)
        if k=="river":
            for i in range(6,len(samples)-6,15):
                x,y,a=samples[i]
                if near(x,y,CROSS,13): continue
                nx,ny=-math.sin(a),math.cos(a)
                # Short pale current strokes follow the centerline and stay inside banks.
                c.setStrokeColor(HexColor("#E9EDCF")); c.setLineWidth(.24)
                q=c.beginPath()
                for j in range(i,min(i+5,len(samples))):
                    xx,yy,aa=samples[j]; off=.7 if (i//15)%2 else -.7
                    xx-=math.sin(aa)*off; yy+=math.cos(aa)*off
                    q.moveTo(xx,yy) if j==i else q.lineTo(xx,yy)
                c.drawPath(q)
                if i%30==6:
                    side=1 if (i//15)%2 else -1
                    V.stamp(c,"Marsh_Reeds_v2",x+nx*(outer/2+2.6)*side,y+ny*(outer/2+2.6)*side,4.8,5.0)
        return
    if k=="hedge":
        for j,(x,y,a) in enumerate(S.base._sample(f,False,f.get("smooth",False),3.8)):
            if near(x,y,gate_gaps or [],9.5): continue
            V.stamp(c,"Hedge_Bush_v2",x,y,6*SCALE,3.8*SCALE)
        return
    S.line_original(c,f,road_pass,gate_gaps)
    if k=="road" and road_pass=="fill":
        c.setStrokeColor(HexColor("#AD8959")); c.setLineWidth(.22)
        samples=S.base._sample(f,False,f.get("smooth",True),1)
        for i in range(6,len(samples)-4,20):
            x,y,a=samples[i]
            if near(x,y,CROSS,13): continue
            c.line(x,y,x+math.cos(a)*2.2,y+math.sin(a)*2.2)

def legend(c,features,box,**kw):
    # Same assets and readable row-sized swatches; map-only 30% scaling does not overflow key.
    import importlib.util
    spec=importlib.util.spec_from_file_location("aud_v3_key",HERE.parent/"aud_layer.py")
    key=importlib.util.module_from_spec(spec); spec.loader.exec_module(key)
    def key_point(c,f,angle=0):
        x,y=f["pts"][0]; k=f["kind"]
        if k=="bridge": V.stamp(c,"Bridge_River_v3",x,y,17,12)
        elif k=="gate": V.stamp(c,"Gate_Steep_v2",x,y,12,13)
        elif k in V.POINTS:
            name,w,h=V.POINTS[k]; V.stamp(c,name,x,y,w,h)
    def swatch(c,f):
        x,y=f["pts"][0]
        if f["kind"]=="wood":
            V.stamp(c,"Conifer_v3",x+5,y+4,5,7); V.stamp(c,"Birch_v3",x+13,y+4,6,7)
        elif f["kind"]=="marsh": V.stamp(c,"Marsh_Reeds_v2",x+9,y+4,8,7)
        else: S.texture_original(c,f)
    key._point=key_point; key._area_texture=swatch; key._draw_line_feature=line
    key.draw_legend(c,features,box,**kw)

def grid_under_art():
    # Reorder two intact blocks in build() IN MEMORY, only for this scratch renderer.
    # No live source file is edited.
    source=inspect.getsource(M.build)
    a=source.index("    # The drawn symbol layer")
    b=source.index("    # Reference grid",a)
    d=source.index("    lab = Labeller()",b)
    new=source[:a]+source[b:d]+source[a:b]+source[d:]
    assert new.index("# Reference grid")<new.index("# The drawn symbol layer")
    exec(compile(new,str(HERE/"render_terrain_v3.py")+"::scratch_build","exec"),M.__dict__)

def build():
    paths=[S.LAYER,HERE.parent/"aud_layer.py",HERE.parent/"aud_features.json",HERE.parent/"build_trail_maps_pdf.py"]
    before={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    assert len(FEATURES)==20
    S.texture_original=S.texture; S.line_original=S.line
    S.texture=texture; S.line=line; S.point=point; S.draw_legend=legend; S.OUT=OUT
    grid_under_art()
    S.main()
    assert before=={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    shutil.copy2(OUT/"Trail_Map_3_Aud_Print.pdf",DELIVERY/"Aud_Style_Draft_v3.pdf")
    (OUT/"validation.json").write_text(json.dumps({"features":20,"source_hashes":before,"grid_below_art":True,"non_bridge_scale":SCALE,"bridge_deck_span":16,"bridge_transform":"rigid rotation + uniform scale; no shear","assets":sorted(V.used)},indent=2))
    print("PASS: grid below art, non-bridge icons 1.3x, bridge span 16pt, live files unchanged.")

def comparison():
    c=canvas.Canvas(str(DELIVERY/"Aud_Style_Comparison_v3.pdf"),pagesize=(792,612))
    c.setFillColor(HexColor("#EFE3C4")); c.rect(0,0,792,612,fill=1,stroke=0)
    c.setFillColor(HexColor("#283B34")); c.setFont("Helvetica-Bold",16)
    c.drawString(24,586,"AUD MAP - TERRAIN AND ICON REVISION")
    c.setFont("Helvetica",9); c.drawString(24,571,"Mixed woodland, detailed water and paths, grid beneath art; non-bridge map icons +30%.")
    for x,name,label in [(24,"full-style-preview-v2.png","PREVIOUS PREVIEW"),(408,"style-preview-v3.png","REVISED PREVIEW")]:
        c.setFont("Helvetica-Bold",10); c.drawString(x,550,label)
        c.saveState(); p=c.beginPath(); p.rect(x,216,360,324); c.clipPath(p,stroke=0,fill=0)
        c.drawImage(str(DELIVERY/name),x,540-360*792/612,360,360*792/612)
        c.restoreState()
    c.setStrokeColor(HexColor("#B09D77")); c.line(24,204,768,204)
    c.setFont("Helvetica-Bold",10); c.drawString(24,186,"MIXED TREE SILHOUETTES AND UNDISTORTED BRIDGE")
    for x,name,label in [(95,"Tree_v2","Broadleaf"),(240,"Birch_v3","Birch"),(385,"Conifer_v3","Conifer"),(550,"Bridge_River_v3","River bridge")]:
        V.stamp(c,name,x,117,82,90)
        c.setFont("Helvetica",9); c.setFillColor(HexColor("#283B34")); c.drawCentredString(x,57,label)
    c.setFont("Helvetica",8)
    c.drawString(640,127,"JSON positions")
    c.drawString(640,115,"unchanged.")
    c.drawString(640,91,"Print-size check")
    c.drawString(640,79,"still required.")
    c.drawString(24,25,"Terrain remains clipped to original shapes; live renderer and map are unchanged.")
    c.showPage(); c.save()

if __name__=="__main__":
    comparison() if "--comparison" in sys.argv else build()

