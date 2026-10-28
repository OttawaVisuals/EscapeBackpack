"""Aud v6: larger landing attached to coast, boat on sea side; other v5 art retained."""
import sys,math,json,hashlib,shutil
from pathlib import Path
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
import render_field_v5 as F
H,T,V,S,M=F.H,F.T,F.V,F.S,F.M
HERE=Path(__file__).resolve().parent
OUT=HERE/"render_landing_v6"
DELIVERY=HERE/"render_baseline"
BASE_PATH=HERE.parent/"aud_base.js"
BASE=json.loads(BASE_PATH.read_text(encoding="utf-8").split("=",1)[1].strip().rstrip(";"))
SHORE=(220.38,752.98)
ART_ANCHOR=(1120,770)
WIDTH=26.0

def placement():
    reader,size,b=V.asset("Landing_Shore_v6")
    scale=WIDTH/(b[2]-b[0])
    # Keep post tops and boat entirely within the original map frame.
    scale=min(scale,(M.MY1-SHORE[1]-.65)/(ART_ANCHOR[1]-b[1]))
    return reader,size,b,scale

def map_point(px,py):
    _,_,_,scale=placement()
    return SHORE[0]+(px-ART_ANCHOR[0])*scale,SHORE[1]+(ART_ANCHOR[1]-py)*scale

def on_land(x,y):
    return any(V.inside(r,x,y) for r in BASE["land"])

def landing(c):
    name="Landing_Shore_v6"; reader,(iw,ih),b,scale=placement(); V.used.add(name)
    x,y=SHORE; ax,ay=ART_ANCHOR
    c.saveState()
    p=c.beginPath()
    p.rect(x+(b[0]-ax)*scale-.1,y+(ay-b[3])*scale-.1,(b[2]-b[0])*scale+.2,(b[3]-b[1])*scale+.2)
    c.clipPath(p,stroke=0,fill=0)
    c.drawImage(reader,x-ax*scale,y-(ih-ay)*scale,iw*scale,ih*scale,mask="auto")
    c.restoreState()

def point(c,f,angle=0):
    landing(c) if f["kind"]=="port" else H.point(c,f,angle)

def legend(c,features,box,**kw):
    old=V.POINTS["port"]
    V.POINTS["port"]=("Landing_Shore_v6",12,13)
    try: F.legend(c,features,box,**kw)
    finally: V.POINTS["port"]=old

def setup():
    F.setup(); S.point=point; S.draw_legend=legend; S.OUT=OUT
    # Move the decorative bay caption into clear water, away from the enlarged landing.
    cfg=dict(M.TRAILS["aud"])
    cfg["areas"]=[(name,lat,-22.63 if name.startswith("Bre") else lon)
                  for name,lat,lon in cfg["areas"]]
    M.TRAILS["aud"]=cfg

def build():
    paths=[S.LAYER,HERE.parent/"aud_layer.py",HERE.parent/"aud_features.json",HERE.parent/"build_trail_maps_pdf.py",BASE_PATH]
    hashes={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    assert BASE["frame"]==S.load()[0]
    # Hull perimeter landmarks on the new artwork, inspected visually against the silhouette.
    boat=[(245,430),(285,580),(470,760),(690,850),(800,870),(855,805)]
    hull=[map_point(*p) for p in boat]
    assert all(not on_land(x,y) for x,y in hull),hull
    setup(); T.grid_under_art(); S.main()
    assert hashes=={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    shutil.copy2(OUT/"Trail_Map_3_Aud_Print.pdf",DELIVERY/"Aud_Landing_Draft_v6.pdf")
    (OUT/"validation.json").write_text(json.dumps({"source_hashes":hashes,"features":20,"source_port":[247.8,760.43],"draft_shore_attachment":SHORE,"art_width_target_pt":WIDTH,"boat_hull_samples":hull,"all_hull_samples_on_sea":True},indent=2))
    print("PASS: six hull samples in sea; source geometry/live files unchanged.")

def coast(c):
    c.setFillColor(HexColor("#DCE7E4")); c.rect(M.MX0,M.MY0,M.MX1-M.MX0,M.MY1-M.MY0,fill=1,stroke=0)
    c.saveState(); p=c.beginPath(); p.rect(M.MX0,M.MY0,M.MX1-M.MX0,M.MY1-M.MY0); c.clipPath(p,stroke=0,fill=0)
    c.setFillColor(HexColor("#EFE3C4")); c.setStrokeColor(HexColor("#59635D")); c.setLineWidth(.55)
    for ring in BASE["land"]:
        p=c.beginPath(); p.moveTo(*ring[0])
        for q in ring[1:]: p.lineTo(*q)
        p.close(); c.drawPath(p,stroke=1,fill=1)
    c.restoreState()

def detail():
    setup()
    c=canvas.Canvas(str(DELIVERY/"Aud_Landing_Detail_v6.pdf"),pagesize=(792,612))
    c.setFillColor(HexColor("#EFE3C4")); c.rect(0,0,792,612,fill=1,stroke=0)
    c.setFillColor(HexColor("#283B34")); c.setFont("Helvetica-Bold",17)
    c.drawString(24,583,"AUD - LANDING ON THE SHORE")
    c.setFont("Helvetica",10); c.drawString(24,563,"Larger jetty and boat, positioned against the actual coastline.")
    for x,old,label in [(24,True,"PREVIOUS"),(408,False,"REVISED")]:
        c.setFont("Helvetica-Bold",11); c.drawString(x,536,label)
        c.saveState(); p=c.beginPath(); p.rect(x,205,360,315); c.clipPath(p,stroke=0,fill=0)
        c.translate(x,205); c.scale(4.5,4.5); c.translate(-187,-715)
        coast(c)
        c.saveState(); p=c.beginPath(); p.rect(M.MX0,M.MY0,M.MX1-M.MX0,M.MY1-M.MY0); c.clipPath(p,stroke=0,fill=0)
        if old: H.point(c,{"kind":"port","pts":[[247.8,760.43]]})
        else: landing(c)
        c.restoreState(); c.restoreState()
    c.setStrokeColor(HexColor("#B09D77")); c.line(24,188,768,188)
    c.setFillColor(HexColor("#283B34")); c.setFont("Helvetica",11)
    for i,text in enumerate(["The landward end touches the shore; the boat sits fully on the sea side.",
                              "Landing artwork is larger; upper posts fit below the map frame.",
                              "Placement override is in this draft renderer only; source JSON is unchanged."]):
        c.drawString(24,155-i*24,text)
    c.setFont("Helvetica",8); c.drawString(24,29,"Physical print proof remains outstanding. Other map styling and the live map are unchanged.")
    c.showPage(); c.save()

if __name__=="__main__":
    detail() if "--detail" in sys.argv else build()

