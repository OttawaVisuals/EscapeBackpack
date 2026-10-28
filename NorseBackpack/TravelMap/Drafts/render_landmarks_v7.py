"""Aud v7: six landmarks match the approved landing's visible width."""
import sys,json,hashlib,shutil
from pathlib import Path
import render_landing_v6 as L
F,H,T,V,S,M=L.F,L.H,L.T,L.V,L.S,L.M
HERE=Path(__file__).resolve().parent
OUT=HERE/"render_landmarks_v7"
DELIVERY=HERE/"render_baseline"
KINDS={"church","ruin","village","cave","mill","farm"}
_,_,LANDING_BBOX,LANDING_SCALE=L.placement()
TARGET=(LANDING_BBOX[2]-LANDING_BBOX[0])*LANDING_SCALE
SIZES={}
for k in KINDS:
    name=V.POINTS[k][0]
    _,_,b=V.asset(name)
    SIZES[k]=(name,TARGET,TARGET*(b[3]-b[1])/(b[2]-b[0]))

def point(c,f,angle=0):
    k=f["kind"]
    if k not in KINDS: return L.point(c,f,angle)
    name,w,h=SIZES[k]; x,y=f["pts"][0]
    V.stamp(c,name,x,y,w,h)

def build():
    paths=[S.LAYER,HERE.parent/"aud_layer.py",HERE.parent/"aud_features.json",HERE.parent/"build_trail_maps_pdf.py",L.BASE_PATH]
    hashes={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    assert len(T.FEATURES)==20
    for f in T.FEATURES:
        if f["kind"] in KINDS:
            _,w,h=SIZES[f["kind"]]; x,y=f["pts"][0]
            assert M.MX0<=x-w/2 and x+w/2<=M.MX1
            assert M.MY0<=y-h/2 and y+h/2<=M.MY1
    L.setup(); S.point=point; S.OUT=OUT
    # Reserve actual enlarged dimensions so labels cannot cover new artwork.
    OriginalLabeller=M.Labeller
    class LandmarkLabeller(OriginalLabeller):
        def __init__(self):
            super().__init__()
            for f in T.FEATURES:
                if f["kind"] in KINDS:
                    _,w,h=SIZES[f["kind"]]; x,y=f["pts"][0]
                    self.reserve_centred(x,y,w,h,pad=2)
    M.Labeller=LandmarkLabeller
    T.grid_under_art(); S.main()
    assert hashes=={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    shutil.copy2(OUT/"Trail_Map_3_Aud_Print.pdf",DELIVERY/"Aud_Landmarks_Draft_v7.pdf")
    (OUT/"validation.json").write_text(json.dumps({"features":20,"source_hashes":hashes,"visible_width_pt":TARGET,
       "landmark_sizes":SIZES,"all_enlarged_icons_inside_map":True,
       "scope":"chapel, ruin, village, cave, mill, farm only"},indent=2))
    print("PASS: all six landmarks match landing width %.3f pt; proportions/positions retained; bounds checked."%TARGET)

if __name__=="__main__": build()

