"""Aud v4 hedge/gate-only refinement, isolated from prior proofs and live files."""
import math,sys,json,hashlib,shutil
from pathlib import Path
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
import render_terrain_v3 as T
V,S,M=T.V,T.S,T.M
HERE=Path(__file__).resolve().parent
OUT=HERE/"render_hedge_gate_v4"
DELIVERY=HERE/"render_baseline"
GATES=[f["pts"][0] for f in T.FEATURES if f["kind"]=="gate"]
OLD_POINT=T.point
OLD_LINE=T.line
def gate(c,x,y,angle):
    name="Gate_Open_v4"
    reader,(iw,ih),b=V.asset(name); V.used.add(name)
    # Two upright post-base anchors measured in the generated asset.
    ax,ay,bx,by=784,551,1106,915
    cx=(ax+bx)/2; cy=ih-(ay+by)/2
    native=math.degrees(math.atan2(ay-by,bx-ax))
    scale=18.2/max(b[2]-b[0],b[3]-b[1])
    # Fit the open leaf below the map frame without moving its passage anchor.
    a=math.radians(angle-native)
    top=max((xx-cx)*math.sin(a)+(ih-yy-cy)*math.cos(a)
            for xx in (b[0],b[2]) for yy in (b[1],b[3]))
    if y<M.MY1 and top>0: scale=min(scale,(M.MY1-y-.7)/top)
    c.saveState(); c.translate(x,y); c.rotate(angle-native); c.scale(scale,scale)
    p=c.beginPath(); p.rect(b[0]-cx-3,ih-b[3]-cy-3,b[2]-b[0]+6,b[3]-b[1]+6)
    c.clipPath(p,stroke=0,fill=0)
    c.drawImage(reader,-cx,-cy,iw,ih,mask="auto")
    c.restoreState()

def point(c,f,angle=0):
    if f["kind"]=="gate": gate(c,*f["pts"][0],angle)
    else: OLD_POINT(c,f,angle)

def line(c,f,road_pass=None,gate_gaps=None):
    if f["kind"]!="hedge": return OLD_LINE(c,f,road_pass,gate_gaps)
    c.saveState()
    # Remove a real passage from the entire hedge layer, including overlapping foliage.
    if gate_gaps:
        cut=c.beginPath(); cut.rect(-100,-100,900,1100)
        for x,y in gate_gaps: cut.circle(x,y,4.8)
        c.clipPath(cut,stroke=0,fill=0,fillMode=0)
    c.setLineCap(1); c.setLineJoin(1)
    c.setStrokeColor(HexColor("#60733F")); c.setLineWidth(3.2)
    c.drawPath(S.base._path(c,f,False,f.get("smooth",False)),stroke=1,fill=0)
    # Overlap textured clumps and orient their long axis along the actual hedge tangent.
    for j,(x,y,a) in enumerate(S.base._sample(f,False,f.get("smooth",False),6.5)):
        normal=.35*math.sin(j*2.3)
        c.saveState(); c.translate(x-math.sin(a)*normal,y+math.cos(a)*normal)
        c.rotate(math.degrees(a))
        V.stamp(c,"Hedge_Clump_v4",0,0,16.5+1.2*math.sin(j*1.7),7.4)
        c.restoreState()
    c.restoreState()

def legend(c,features,box,**kw):
    import importlib.util
    spec=importlib.util.spec_from_file_location("aud_v4_key",HERE.parent/"aud_layer.py")
    key=importlib.util.module_from_spec(spec); spec.loader.exec_module(key)
    def kp(c,f,angle=0):
        x,y=f["pts"][0]; k=f["kind"]
        if k=="gate": V.stamp(c,"Gate_Open_v4",x,y,17,13)
        elif k=="bridge": V.stamp(c,"Bridge_River_v3",x,y,17,12)
        else:
            name,w,h=V.POINTS[k]; V.stamp(c,name,x,y,w,h)
    def swatch(c,f):
        x,y=f["pts"][0]
        if f["kind"]=="wood":
            V.stamp(c,"Conifer_v3",x+5,y+4,5,7); V.stamp(c,"Birch_v3",x+13,y+4,6,7)
        elif f["kind"]=="marsh": V.stamp(c,"Marsh_Reeds_v2",x+9,y+4,8,7)
        else: S.texture_original(c,f)
    def key_line(c,f,road_pass=None,gate_gaps=None):
        if f["kind"]=="hedge":
            x,y=f["pts"][0]; V.stamp(c,"Hedge_Clump_v4",x+9,y,18,6.5)
        else: line(c,f,road_pass,gate_gaps)
    key._point=kp; key._area_texture=swatch; key._draw_line_feature=key_line
    key.draw_legend(c,features,box,**kw)

def setup():
    S.texture_original=S.texture; S.line_original=S.line
    S.texture=T.texture; S.line=line; S.point=point; S.draw_legend=legend; S.OUT=OUT

def build():
    paths=[S.LAYER,HERE.parent/"aud_layer.py",HERE.parent/"aud_features.json",HERE.parent/"build_trail_maps_pdf.py"]
    before={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    setup(); T.grid_under_art(); S.main()
    assert before=={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    shutil.copy2(OUT/"Trail_Map_3_Aud_Print.pdf",DELIVERY/"Aud_Hedge_Gate_Draft_v4.pdf")
    (OUT/"validation.json").write_text(json.dumps({"features":20,"source_hashes":before,"gate_center":GATES,"gate_transform":"rigid rotation + uniform scale, no shear","hedge":"overlapping tangent-aligned clumps; 4.8pt passage radius"},indent=2))
    print("PASS: hedge/gate revision only; all source geometry/live files unchanged.")

def comparison():
    setup()
    c=canvas.Canvas(str(DELIVERY/"Aud_Hedge_Gate_Detail_v4.pdf"),pagesize=(792,612))
    c.setFillColor(HexColor("#EFE3C4")); c.rect(0,0,792,612,fill=1,stroke=0)
    c.setFillColor(HexColor("#283B34")); c.setFont("Helvetica-Bold",17)
    c.drawString(24,583,"AUD - HEDGE AND GATE")
    c.setFont("Helvetica",10); c.drawString(24,563,"Same field, hedge path and gate location. Enlarged detail for style review.")
    focused=[f for f in T.FEATURES if f["kind"] in ("field","hedge","gate","farm")]
    for x,old,title in [(24,True,"PREVIOUS"),(408,False,"REVISED")]:
        c.setFont("Helvetica-Bold",11); c.drawString(x,536,title)
        c.saveState()
        p=c.beginPath(); p.rect(x,187,360,334); c.clipPath(p,stroke=0,fill=0)
        c.translate(x,187); c.scale(3.4,3.4); c.translate(-346,-684)
        S.line=OLD_LINE if old else line
        S.point=OLD_POINT if old else point
        S.draw(c,focused,clip_rect=(346,684,452,783))
        c.restoreState()
    S.line=line; S.point=point
    c.setStrokeColor(HexColor("#B09D77")); c.line(24,173,768,173)
    V.stamp(c,"Hedge_Clump_v4",160,108,200,74)
    V.stamp(c,"Gate_Open_v4",460,109,120,86)
    c.setFillColor(HexColor("#283B34")); c.setFont("Helvetica",9)
    c.drawCentredString(160,57,"Overlapping foliage follows the hedge curve")
    c.drawCentredString(460,57,"Open leaf; no shear")
    c.drawString(612,120,"Draft geometry retained.")
    c.drawString(612,99,"Existing layout retained.")
    c.drawString(612,78,"Physical print untested.")
    c.showPage(); c.save()

if __name__=="__main__":
    comparison() if "--detail" in sys.argv else build()

