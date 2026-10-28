"""Aud v8: dry illustrated ditch; v7 map otherwise retained."""
import sys,math,json,hashlib,shutil
from pathlib import Path
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
import render_landmarks_v7 as A
L,F,H,T,V,S,M=A.L,A.F,A.H,A.T,A.V,A.S,A.M
HERE=Path(__file__).resolve().parent
OUT=HERE/"render_ditch_v8"
DELIVERY=HERE/"render_baseline"
BASE_LINE=None

def polygon(c,points,color):
    p=c.beginPath(); p.moveTo(*points[0])
    for q in points[1:]: p.lineTo(*q)
    p.close(); c.setFillColor(HexColor(color)); c.drawPath(p,stroke=0,fill=1)

def ditch(c,f):
    samples=S.base._sample(f,False,f.get("smooth",False),.9)
    if len(samples)<2: return
    c.saveState(); c.setLineCap(1); c.setLineJoin(1)
    def bank(side,width):
        result=[]
        for i,(x,y,a) in enumerate(samples):
            uneven=.20*math.sin(i*1.39)+.13*math.sin(i*.47)
            d=side*(width+uneven)
            result.append((x-math.sin(a)*d,y+math.cos(a)*d))
        return result
    left,right=bank(1,1.75),bank(-1,1.55)
    polygon(c,left+right[::-1],"#BDA174")
    # Narrow recessed bottom and one shaded earthen bank, not road casings.
    bottom_l,bottom_r=bank(1,.55),bank(-1,.42)
    polygon(c,left+bottom_l[::-1],"#9A7B53")
    polygon(c,bottom_l+bottom_r[::-1],"#7D6348")
    # Broken highlights keep the bank rough rather than a rigid pair of rails.
    c.setStrokeColor(HexColor("#DCC18F")); c.setLineWidth(.40)
    for i in range(2,len(samples)-4,7):
        x,y,a=samples[i]
        if T.near(x,y,T.CROSS,10): continue
        q=c.beginPath()
        for j in range(i,min(i+4,len(samples))):
            xx,yy,aa=samples[j]; d=-1.25
            xx-=math.sin(aa)*d; yy+=math.cos(aa)*d
            q.moveTo(xx,yy) if j==i else q.lineTo(xx,yy)
        c.drawPath(q,stroke=1,fill=0)
    # Sparse dry grass and soil flecks; leave the bridge approaches uncluttered.
    for i in range(6,len(samples)-5,14):
        x,y,a=samples[i]
        if T.near(x,y,T.CROSS,12): continue
        side=1 if (i//14)%2 else -1
        gx=x-math.sin(a)*3.4*side; gy=y+math.cos(a)*3.4*side
        V.stamp(c,"Field_Grass_v5",gx,gy,3.8,3.2)
        c.setFillColor(HexColor("#AA8C61"))
        c.circle(x+math.sin(a)*2.4,y-math.cos(a)*2.4,.27,fill=1,stroke=0)
    c.restoreState()

def base_dispatch(c,f,road_pass=None,gate_gaps=None):
    if f["kind"]=="ditch": ditch(c,f)
    else: BASE_LINE(c,f,road_pass,gate_gaps)

def line(c,f,road_pass=None,gate_gaps=None):
    if f["kind"]=="ditch": ditch(c,f)
    else: H.line(c,f,road_pass,gate_gaps)

def setup():
    global BASE_LINE
    L.setup(); BASE_LINE=S.line_original
    S.line_original=base_dispatch; S.line=line; S.point=A.point; S.OUT=OUT
    OriginalLabeller=M.Labeller
    class LandmarkLabeller(OriginalLabeller):
        def __init__(self):
            super().__init__()
            for f in T.FEATURES:
                if f["kind"] in A.KINDS:
                    _,w,h=A.SIZES[f["kind"]]; x,y=f["pts"][0]
                    self.reserve_centred(x,y,w,h,pad=2)
    M.Labeller=LandmarkLabeller

def build():
    paths=[S.LAYER,HERE.parent/"aud_layer.py",HERE.parent/"aud_features.json",HERE.parent/"build_trail_maps_pdf.py",L.BASE_PATH]
    before={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    assert len(T.FEATURES)==20
    setup(); T.grid_under_art(); S.main()
    assert before=={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    shutil.copy2(OUT/"Trail_Map_3_Aud_Print.pdf",DELIVERY/"Aud_Ditch_Draft_v8.pdf")
    (OUT/"validation.json").write_text(json.dumps({"features":20,"source_hashes":before,
        "scope":"ditch artwork and matching legend only","ditch_source_paths":[f["pts"] for f in T.FEATURES if f["kind"]=="ditch"],
        "crossing_angles":S.crossing_angles(T.FEATURES)},indent=2))
    print("PASS: ditch-only revision; geometry, crossing directions and live files unchanged.")

def detail():
    setup()
    c=canvas.Canvas(str(DELIVERY/"Aud_Ditch_Detail_v8.pdf"),pagesize=(792,612))
    c.setFillColor(HexColor("#EFE3C4")); c.rect(0,0,792,612,fill=1,stroke=0)
    c.setFillColor(HexColor("#283B34")); c.setFont("Helvetica-Bold",17)
    c.drawString(24,583,"AUD - DRY DITCH")
    c.setFont("Helvetica",10); c.drawString(24,563,"A shallow earth channel replaces the technical line and ticks.")
    for x,old,label in [(24,True,"PREVIOUS"),(408,False,"REVISED")]:
        c.setFont("Helvetica-Bold",11); c.drawString(x,536,label)
        c.saveState(); p=c.beginPath(); p.rect(x,194,360,326); c.clipPath(p,stroke=0,fill=0)
        c.translate(x,194); c.scale(3.5,3.5); c.translate(-155,-445)
        L.coast(c)
        S.line_original=BASE_LINE if old else base_dispatch
        S.line=H.line if old else line
        S.draw(c,T.FEATURES,clip_rect=(155,445,258,538))
        c.restoreState()
    S.line_original=base_dispatch; S.line=line
    c.setStrokeColor(HexColor("#B09D77")); c.line(24,179,768,179)
    c.setFillColor(HexColor("#283B34")); c.setFont("Helvetica",11)
    for i,text in enumerate(["Dry brown banks distinguish the ditch from the teal streams.",
                              "A darker centre gives depth; sparse grass softens the edges.",
                              "Detail reduces near the bridge so the crossing remains easy to count."]):
        c.drawString(24,148-i*24,text)
    c.setFont("Helvetica",8); c.drawString(24,29,"Source path, bridge and other map artwork retained. Physical print proof not performed.")
    c.showPage(); c.save()

if __name__=="__main__":
    detail() if "--detail" in sys.argv else build()

