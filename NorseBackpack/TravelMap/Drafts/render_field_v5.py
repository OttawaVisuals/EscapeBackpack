"""Aud v5: field-only revision; approved v4 hedge/gate and v3 terrain retained."""
import sys,math,json,hashlib,shutil
from pathlib import Path
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
import render_hedge_gate_v4 as H
T,V,S,M=H.T,H.V,H.S,H.M
HERE=Path(__file__).resolve().parent
OUT=HERE/"render_field_v5"
DELIVERY=HERE/"render_baseline"
FARMS=[f["pts"][0] for f in T.FEATURES if f["kind"]=="farm"]

def field(c,f,legend=False):
    pts=f["pts"]; x0,x1=min(x for x,y in pts),max(x for x,y in pts)
    y0,y1=min(y for x,y in pts),max(y for x,y in pts)
    p=S.base._path(c,f,True,f.get("smooth",False))
    c.saveState(); c.clipPath(p,stroke=0,fill=0)
    c.setFillColor(HexColor("#EDDFBC")); c.drawPath(p,fill=1,stroke=0)
    c.saveState()
    if not legend:
        clear=c.beginPath(); clear.rect(-100,-100,900,1100)
        for x,y in FARMS: clear.ellipse(x-13,y-10,x+13,y+10)
        c.clipPath(clear,stroke=0,fill=0,fillMode=0)
    # Curving paired furrows run along the long field, with modest irregularity.
    c.setLineCap(1)
    step=5.7 if not legend else 4.2
    for i in range(int((x1-x0+26)/step)+1):
        start=x0-12+i*step
        q=c.beginPath()
        for j in range(30):
            t=j/29
            y=y0-5+(y1-y0+10)*t
            x=start+7*math.sin(t*2.1+.2)+.17*math.sin(j*2.1+i)
            q.moveTo(x,y) if j==0 else q.lineTo(x,y)
        c.setStrokeColor(HexColor("#A98655")); c.setLineWidth(.47 if not legend else .35)
        c.drawPath(q,stroke=1,fill=0)
        c.saveState(); c.translate(1.1,0)
        c.setStrokeColor(HexColor("#D7BC8A")); c.setLineWidth(.28)
        c.drawPath(q,stroke=1,fill=0); c.restoreState()
    c.restoreState()
    # Sparse edge grass and short soil marks soften the boundary, within its original shape.
    if not legend:
        for j,(x,y,a) in enumerate(S.base._sample(f,True,False,5.7)):
            nx,ny=-math.sin(a),math.cos(a)
            if not V.inside(pts,x+nx*.6,y+ny*.6): nx,ny=-nx,-ny
            if T.near(x,y,FARMS,14): continue
            if j%2==0:
                V.stamp(c,"Field_Grass_v5",x+nx*1.8,y+ny*1.8,3.8,3)
            else:
                c.setStrokeColor(HexColor("#B08A59")); c.setLineWidth(.42)
                c.line(x+nx*.8,y+ny*.8,x+nx*.8+math.cos(a)*1.8,y+ny*.8+math.sin(a)*1.8)
    c.setStrokeColor(HexColor("#AA8452")); c.setLineWidth(.4)
    c.drawPath(p,stroke=1,fill=0)
    c.restoreState()

def texture(c,f):
    field(c,f) if f["kind"]=="field" else T.texture(c,f)

def legend(c,features,box,**kw):
    # Reuse v4 key layout, substituting the actual new field sample.
    original=S.texture_original
    def key_texture(c,f):
        field(c,f,True) if f["kind"]=="field" else original(c,f)
    S.texture_original=key_texture
    try: H.legend(c,features,box,**kw)
    finally: S.texture_original=original

def setup():
    H.setup(); S.texture=texture; S.draw_legend=legend; S.OUT=OUT

def build():
    paths=[S.LAYER,HERE.parent/"aud_layer.py",HERE.parent/"aud_features.json",HERE.parent/"build_trail_maps_pdf.py"]
    hashes={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    setup(); T.grid_under_art(); S.main()
    assert hashes=={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    shutil.copy2(OUT/"Trail_Map_3_Aud_Print.pdf",DELIVERY/"Aud_Field_Draft_v5.pdf")
    (OUT/"validation.json").write_text(json.dumps({"features":20,"source_hashes":hashes,"scope":"field texture and legend only","farm_clearance":"26 x 20pt ellipse","geometry_unchanged":True},indent=2))
    print("PASS: field-only revision; live sources and JSON unchanged.")

def detail():
    setup()
    c=canvas.Canvas(str(DELIVERY/"Aud_Field_Detail_v5.pdf"),pagesize=(792,612))
    c.setFillColor(HexColor("#EFE3C4")); c.rect(0,0,792,612,fill=1,stroke=0)
    c.setFillColor(HexColor("#283B34")); c.setFont("Helvetica-Bold",17)
    c.drawString(24,583,"AUD - FIELD REFINEMENT")
    c.setFont("Helvetica",10)
    c.drawString(24,563,"Natural furrows and grassy edges; field shape, farm, hedge and gate locations retained.")
    focused=[f for f in T.FEATURES if f["kind"] in ("field","hedge","gate","farm")]
    for x,old,label in [(24,True,"PREVIOUS"),(408,False,"REVISED")]:
        c.setFont("Helvetica-Bold",11); c.drawString(x,536,label)
        c.saveState()
        p=c.beginPath(); p.rect(x,187,360,334); c.clipPath(p,stroke=0,fill=0)
        c.translate(x,187); c.scale(3.4,3.4); c.translate(-346,-684)
        S.texture=T.texture if old else texture
        S.draw(c,focused,clip_rect=(346,684,452,783))
        c.restoreState()
    S.texture=texture
    c.setStrokeColor(HexColor("#B09D77")); c.line(24,173,768,173)
    c.setFillColor(HexColor("#283B34")); c.setFont("Helvetica-Bold",11)
    c.drawString(24,145,"FIELD TREATMENT")
    c.setFont("Helvetica",10)
    for i,text in enumerate(["Light wheat tone separates the cultivated ground from the yellow land.",
                              "Curved paired furrows replace the regular horizontal stripes.",
                              "Sparse dry grass softens the edge; clear space remains around the farmhouse."]):
        c.drawString(24,122-i*20,text)
    c.setFont("Helvetica",8); c.drawString(24,29,"Draft style proof. Physical print readability remains untested; live map unchanged.")
    c.showPage(); c.save()

if __name__=="__main__":
    detail() if "--detail" in sys.argv else build()

