"""Full Aud layout v9, using user JSON and ticket-derived coin markers."""
import sys,math,json,hashlib,random
from pathlib import Path
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
import render_ditch_v8 as D
A,L,F,H,T,V,S,M=D.A,D.L,D.F,D.H,D.T,D.V,D.S,D.M
HERE=Path(__file__).resolve().parent
SOURCE=HERE/"aud_features_full_2026-10-16.json"
OUT=HERE/"render_full_map_v9"
DATA=json.loads(SOURCE.read_text(encoding="utf-8-sig"))
FEATURES=DATA["features"]
TICKET_DIR=HERE.parents[1]/"Props"/"AudTicket"
sys.path.insert(0,str(TICKET_DIR))
import build_aud_ticket_pdf as ticket
MARKERS={"coin1":"camel","coincorretc":"fehu","coin2":"fleur"}
EXTRA={"stone":"Standing_Stone_v1","cairn":"Cairn_v1","well":"Well_Full_v9"}
SHIFTS=[]; PORTS={}; MARKER_LOG=[]

def fit(x,y,w,h):
    xx=min(max(x,M.MX0+w/2+.6),M.MX1-w/2-.6)
    yy=min(max(y,M.MY0+h/2+.6),M.MY1-h/2-.6)
    if abs(x-xx)+abs(y-yy)>.01 and (x,y,xx,yy) not in SHIFTS: SHIFTS.append((x,y,xx,yy))
    return xx,yy

def landmark(c,name,x,y,width):
    _,_,b=V.asset(name); height=width*(b[3]-b[1])/(b[2]-b[0])
    xx,yy=fit(x,y,width,height)
    V.stamp(c,name,xx,yy,width,height)

def marker(c,f):
    label=f.get("label","").strip().lower()
    assert label in MARKERS,label
    name=MARKERS[label]; x,y=f["pts"][0]; h=12
    c.saveState()
    c.setFillColor(HexColor("#EFE3C4")); c.circle(x,y,7.2,stroke=0,fill=1)
    if name=="fehu":
        c.setStrokeColor(HexColor("#283B34")); ticket.draw_fehu(c,x,y,h,1.3)
    else:
        c.drawImage(str(TICKET_DIR/"icons"/(name+".png")),x-h/2,y-h/2,h,h,
                    preserveAspectRatio=True,anchor="c",mask="auto")
    c.restoreState()
    row={"label":f["label"],"ticket_icon":name,"position":[x,y]}
    if row not in MARKER_LOG: MARKER_LOG.append(row)

def nearest_coast(p):
    best=None
    for ring in L.BASE["land"]:
        for a,b in zip(ring,ring[1:]):
            dx,dy=b[0]-a[0],b[1]-a[1]; ll=dx*dx+dy*dy
            t=max(0,min(1,((p[0]-a[0])*dx+(p[1]-a[1])*dy)/ll)) if ll else 0
            q=(a[0]+t*dx,a[1]+t*dy); row=(math.dist(p,q),q)
            if best is None or row[0]<best[0]: best=row
    return best[1]

def port(c,f):
    p=tuple(f["pts"][0])
    shore=L.SHORE if math.dist(p,(247.8,760.43))<.1 else nearest_coast(p)
    reader,(iw,ih),b=V.asset("Landing_Shore_v6"); ax,ay=L.ART_ANCHOR
    scale=L.WIDTH/(b[2]-b[0])
    scale=min(scale,(M.MY1-shore[1]-.65)/(ay-b[1]))
    assert scale>0
    hull=[(shore[0]+(px-ax)*scale,shore[1]+(ay-py)*scale)
          for px,py in [(245,430),(285,580),(470,760),(690,850),(800,870),(855,805)]]
    assert all(not L.on_land(x,y) for x,y in hull), (p,shore,hull)
    PORTS[str(p)]={"shore_attachment":shore,"hull_samples_on_sea":True}
    c.saveState()
    q=c.beginPath(); q.rect(shore[0]+(b[0]-ax)*scale-.1,shore[1]+(ay-b[3])*scale-.1,
                           (b[2]-b[0])*scale+.2,(b[3]-b[1])*scale+.2)
    c.clipPath(q,stroke=0,fill=0)
    c.drawImage(reader,shore[0]-ax*scale,shore[1]-(ih-ay)*scale,iw*scale,ih*scale,mask="auto")
    c.restoreState()

def ford(c,x,y,angle):
    c.saveState(); c.translate(x,y); c.rotate(angle+26)
    V.stamp(c,"Ford_Full_v9",0,0,13,7)
    c.restoreState()

def point(c,f,angle=0):
    k=f["kind"]; x,y=f["pts"][0]
    if k=="marker": marker(c,f)
    elif k=="port": port(c,f)
    elif k in A.KINDS: landmark(c,A.SIZES[k][0],x,y,A.TARGET)
    elif k in EXTRA:
        width=22 if k!="stone" else 15
        landmark(c,EXTRA[k],x,y,width)
    elif k=="ford": ford(c,x,y,angle)
    elif k in ("bridge","gate"): H.point(c,f,angle)
    else: raise ValueError("Missing point artwork: "+k)

def texture(c,f):
    k=f["kind"]
    if k not in ("lake","moor"): return F.texture(c,f)
    pts=f["pts"]; x0,x1=min(x for x,y in pts),max(x for x,y in pts)
    y0,y1=min(y for x,y in pts),max(y for x,y in pts)
    p=S.base._path(c,f,True,f.get("smooth",False))
    c.saveState(); c.clipPath(p,stroke=0,fill=0)
    if k=="lake":
        c.setFillColor(HexColor("#A7C8C2")); c.setStrokeColor(HexColor("#286D70")); c.setLineWidth(.65)
        c.drawPath(p,fill=1,stroke=1)
        c.setStrokeColor(HexColor("#DAE5CF")); c.setLineWidth(.35)
        for row,y in enumerate(range(int(y0)+5,int(y1),12)):
            for x in range(int(x0)+4,int(x1),18):
                if V.inside(pts,x,y): c.line(x,y,x+5,y)
    else:
        rng=random.Random(int(x0+y0))
        for row,y in enumerate(range(int(y0)+4,int(y1),15)):
            for x in range(int(x0)+4,int(x1),17):
                xx=x+(row%2)*6+rng.uniform(-2,2); yy=y+rng.uniform(-2,2)
                if V.inside(pts,xx,yy):
                    V.stamp(c,"Field_Grass_v5",xx,yy,4.4,3.6)
                    c.setFillColor(HexColor("#806484"))
                    c.circle(xx+1,yy+.5,.4,stroke=0,fill=1)
    c.restoreState()

def line(c,f,road_pass=None,gate_gaps=None):
    k=f["kind"]
    if k=="wall":
        c.saveState()
        if gate_gaps:
            p=c.beginPath(); p.rect(-100,-100,900,1100)
            for x,y in gate_gaps: p.circle(x,y,4.8)
            c.clipPath(p,stroke=0,fill=0,fillMode=0)
        for x,y,a in S.base._sample(f,False,f.get("smooth",False),5.5):
            c.saveState(); c.translate(x,y); c.rotate(math.degrees(a))
            V.stamp(c,"Wall_Clump_v9",0,0,12,4.3); c.restoreState()
        c.restoreState()
    elif k=="path":
        c.setStrokeColor(HexColor("#927044")); c.setLineWidth(.85); c.setDash(2.5,2.3)
        c.drawPath(S.base._path(c,f,False,f.get("smooth",False)),stroke=1,fill=0); c.setDash()
    else: D.line(c,f,road_pass,gate_gaps)

def legend(c,features,box,**kw):
    import importlib.util
    spec=importlib.util.spec_from_file_location("aud_full_v9_key",HERE.parent/"aud_layer.py")
    key=importlib.util.module_from_spec(spec); spec.loader.exec_module(key)
    # The three coin-group symbols are story markers, not a generic marker entry in the key.
    key.LEGEND_ORDER=[(k,n) for k,n in key.LEGEND_ORDER if k!="marker"]
    def kp(c,f,angle=0):
        k=f["kind"]; x,y=f["pts"][0]
        if k in A.KINDS: V.stamp(c,A.SIZES[k][0],x,y,17,13)
        elif k in EXTRA: V.stamp(c,EXTRA[k],x,y,15,13)
        elif k=="port": V.stamp(c,"Landing_Shore_v6",x,y,16,12)
        elif k=="bridge": V.stamp(c,"Bridge_River_v3",x,y,17,12)
        elif k=="gate": V.stamp(c,"Gate_Open_v4",x,y,17,13)
        elif k=="ford": V.stamp(c,"Ford_Full_v9",x,y,17,10)
    def kl(c,f,road_pass=None,gate_gaps=None):
        x,y=f["pts"][0]
        if f["kind"] in ("hedge","wall"):
            name="Hedge_Clump_v4" if f["kind"]=="hedge" else "Wall_Clump_v9"
            V.stamp(c,name,x+9,y,18,6)
        else: line(c,f,road_pass,gate_gaps)
    def ka(c,f):
        x,y=f["pts"][0]; k=f["kind"]
        if k=="wood":
            V.stamp(c,"Conifer_v3",x+5,y+4,5,7); V.stamp(c,"Birch_v3",x+13,y+4,6,7)
        elif k=="marsh": V.stamp(c,"Marsh_Reeds_v2",x+9,y+4,8,7)
        elif k=="moor": V.stamp(c,"Field_Grass_v5",x+9,y+4,8,5)
        elif k=="lake": texture(c,f)
        elif k=="field": F.field(c,f,True)
    key._point=kp; key._draw_line_feature=kl; key._area_texture=ka
    key.draw_legend(c,features,box,**kw)

def build():
    assert len(FEATURES)==102
    assert len([f for f in FEATURES if f["kind"]=="marker"])==3
    paths=[SOURCE,HERE.parent/"aud_layer.py",HERE.parent/"aud_features.json",HERE.parent/"build_trail_maps_pdf.py",L.BASE_PATH]
    hashes={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    S.LAYER=SOURCE
    T.FEATURES=FEATURES
    T.CROSS=[f["pts"][0] for f in FEATURES if f["kind"] in ("bridge","ford","gate")]
    T.LANDMARKS=[f["pts"][0] for f in FEATURES if len(f["pts"])==1]
    H.GATES=[f["pts"][0] for f in FEATURES if f["kind"]=="gate"]
    F.FARMS=[f["pts"][0] for f in FEATURES if f["kind"]=="farm"]
    D.setup()
    cfg=dict(M.TRAILS["aud"])
    cfg["regions"]=[(name,modern,lat,-21.65) for name,modern,lat,lon in cfg["regions"]]
    M.TRAILS["aud"]=cfg
    S.point=point; S.texture=texture; S.line=line; S.draw_legend=legend
    OUT.mkdir(exist_ok=True)
    M.OUT_DIR=OUT; M.aud_layer=S; M.draw_aud_cache_mark=lambda c:None
    T.grid_under_art()
    # Reserve actual new symbol bounds (also protects edge-fitted landmark artwork).
    BaseLabeller=M.Labeller
    class FullLabeller(BaseLabeller):
        def __init__(self):
            super().__init__()
            for f in FEATURES:
                k=f["kind"]
                if k in A.KINDS or k in EXTRA:
                    name=A.SIZES[k][0] if k in A.KINDS else EXTRA[k]
                    width=A.TARGET if k in A.KINDS else (15 if k=="stone" else 22)
                    _,_,b=V.asset(name); height=width*(b[3]-b[1])/(b[2]-b[0])
                    x,y=fit(*f["pts"][0],width,height)
                    self.reserve_centred(x,y,width,height,pad=1)
    M.Labeller=FullLabeller
    result=M.build("aud",M.TRAILS["aud"],M.load_plan(),M.load_corpus())
    assert not result,result
    assert len(MARKER_LOG)==3
    assert sorted(r["ticket_icon"] for r in MARKER_LOG)==["camel","fehu","fleur"]
    assert hashes=={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    target=OUT/"Aud_Full_Map_v9.pdf"
    (OUT/"Trail_Map_3_Aud_Print.pdf").replace(target)
    (OUT/"validation.json").write_text(json.dumps({"features":len(FEATURES),"source_hashes":hashes,
        "markers":MARKER_LOG,"ports":PORTS,"edge_artwork_fit_adjustments":SHIFTS,
        "crossing_counts":{k:sum(f["kind"]==k for f in FEATURES) for k in ("bridge","ford","gate")}},indent=2))
    print("PASS: all 102 features; correct=Fehu, coin1=camel, Coin2=fleur; 4 boats checked on sea.")
if __name__=="__main__": build()

