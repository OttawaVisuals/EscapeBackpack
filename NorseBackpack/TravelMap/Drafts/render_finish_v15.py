"""Aud v15: uniform water outline weight, blue-backed comb, remove tiny land sliver."""
import inspect,json,sys,math
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from shapely.geometry import box,LineString
import render_terrain_v14 as A
Q,R,S,V,M=A.Q,A.R,A.S,A.V,A.M
HERE=A.HERE;OUT=HERE/'render_full_map_v15'
STAMP=HERE/'Aud_Comb_Ink_v15_final.png'
BORDER='#59635D';WEIGHT=.55
REMOVE=box(90,100,114,113)
LAND=Q.LAND.difference(REMOVE)
OLD_TEXTURE=A.texture

def texture(c,f):
 if f['kind']!='lake':return OLD_TEXTURE(c,f)
 # Fill only; all actual coast/river/lake outlines are drawn together below.
 p=S.base._path(c,f,True,f.get('smooth',False))
 c.saveState();c.clipPath(p,stroke=0,fill=0);c.setFillColor(HexColor(A.Q.WATER));c.drawPath(p,fill=1,stroke=0)
 xs=[x for x,y in f['pts']];ys=[y for x,y in f['pts']]
 c.setStrokeColor(HexColor('#DAE5CF'));c.setLineWidth(.35)
 for y in range(int(min(ys))+5,int(max(ys)),12):
  for x in range(int(min(xs))+4,int(max(xs)),18):
   if V.inside(f['pts'],x,y):c.line(x,y,x+5,y)
 c.restoreState()

src=inspect.getsource(Q.water)
a=src.index(' # Bank ink stays');b=src.index(' # Retain river currents',a)
src=src[:a]+''' # Remove the small land remnant below the legend, inside the clipped map frame.
 c.setFillColor(HexColor(WATER));c.drawPath(path_geom(c,REMOVE),fill=1,stroke=0)
 c.setFillColor(HexColor(WATER));c.drawPath(path_geom(c,channels),fill=1,stroke=0,fillMode=0)
 # One vector stroke pass gives every shore and bank the exact same colour AND weight.
 dry=LAND.difference(lakes.union(channels))
 c.saveState();c.setStrokeColor(HexColor('#59635D'));c.setLineWidth(.55);c.setLineJoin(1);c.setLineCap(1)
 c.drawPath(path_geom(c,dry.boundary),fill=0,stroke=1);c.restoreState()
'''+src[b:]
env=dict(Q.__dict__);env.update(LAND=LAND,REMOVE=REMOVE)
exec(compile(src,'v15_water','exec'),env);water=env['water']

def line(c,f,road_pass=None,gate_gaps=None):
 if f['kind'] in ('river','stream'):
  _,inner=Q.P.B.widths(f)
  shape=LineString(Q.samples(f)).buffer(inner/2,quad_segs=12)
  c.saveState();c.setFillColor(HexColor(Q.WATER));c.setStrokeColor(HexColor(BORDER));c.setLineWidth(WEIGHT);c.drawPath(Q.path_geom(c,shape),fill=1,stroke=1);c.restoreState();return
 return Q.line(c,f,road_pass,gate_gaps)

src=inspect.getsource(Q.legend).replace('c.setLineWidth(.6);c.rect(cx,cy-5','c.setLineWidth(.55);c.rect(cx,cy-5')
le=dict(Q.__dict__);le['line']=line
exec(compile(src,'v15_legend','exec'),le);legend=le['legend']

env=dict(Q.P.B.__dict__);env.update(water=water,point=Q.point,line=line)
src=inspect.getsource(Q.P.B.draw).replace('C.line(c,','line(c,')
exec(compile(src,'v15_draw','exec'),env);draw=env['draw']

def grid_under_art():
 source=inspect.getsource(M.build)
 a=source.index('    # The drawn symbol layer');b=source.index('    # Reference grid',a);d=source.index('    lab = Labeller()',b)
 source=source[:a]+source[b:d]+source[a:b]+source[d:]
 needle='p.close()\n        c.drawPath(p, stroke=1, fill=1)'
 assert needle in source
 source=source.replace(needle,'p.close()\n        c.drawPath(p, stroke=0, fill=1)',1)
 source=source.replace('for text, lat, lon, rot in cfg["waters"]:\n        x, y = pt(lon, lat)', 'for text, lat, lon, rot in cfg["waters"]:\n        x, y = pt(lon, lat)\n        if key == "aud" and text.startswith("FAXA"):\n            x, y, rot = 249, 176, 90')
 exec(compile(source,'v15_layout','exec'),M.__dict__)

def build():
 assert STAMP.exists(),STAMP
 R.point=Q.point;R.line=line;R.texture=texture;R.legend=legend;R.OUT=OUT;S.draw=draw
 R.T.grid_under_art=grid_under_art;M.TRAIL_STAMPS=dict(M.TRAIL_STAMPS,aud=STAMP)
 Base=M.Labeller
 class LegendLabeller(Base):
  def __init__(self):
   super().__init__();self.reserve(Q.LEGEND_BOX[0]-2,Q.LEGEND_BOX[1]-2,Q.LEGEND_BOX[2]+2,Q.LEGEND_BOX[3]+2)
 M.Labeller=LegendLabeller
 src=inspect.getsource(R.build).replace('"Aud_Full_Map_v9.pdf"','"Aud_Full_Map_v15.pdf"')
 exec(compile(src,__file__+'::build','exec'),R.__dict__);R.build()
 assert len(Q.MOUTHS)==9 and len(A.SCATTER)==3
 (OUT/'style_changes.json').write_text(json.dumps({'water_border':BORDER,'water_border_weight_pt':WEIGHT,'border_method':'one shared coast/river/lake boundary stroke; no filled casings','removed_land_box':[90,100,114,113],'stamp_ink_asset':str(STAMP),'stamp_background':'transparent, existing blue band shows through'},indent=2))

REGIONS=[('1 - Identical water outline colour and weight',(488,286,46,45)),('2 - Blue band behind comb',(543,48,45,50)),('3 - Land fragment removed',(87,98,32,22))]
def review():
 c=canvas.Canvas(str(OUT/'Aud_Changes_Review_v15.pdf'),pagesize=(612,792));c.setFillColor(HexColor('#EFE3C4'));c.rect(0,0,612,792,fill=1,stroke=0)
 c.setFillColor(HexColor('#283B34'));c.setFont('Helvetica-Bold',15);c.drawString(24,765,'AUD - WATER OUTLINES AND FINISHING')
 c.setFont('Helvetica',9);c.drawString(24,746,'One outline stroke throughout; blue band behind the comb; small land fragment removed.')
 c.setFont('Helvetica-Bold',9);c.drawString(24,725,'BEFORE');c.drawString(318,725,'AFTER')
 for row,(label,(x,y,w,h)) in enumerate(REGIONS):
  top=697-row*214;ph=185;c.setFont('Helvetica-Bold',9);c.drawString(24,top+6,label)
  for px,img in zip((24,318),(HERE/'render_full_map_v14/Aud_Full_Map_v14.png',OUT/'Aud_Full_Map_v15.png')):
   pw=270;s=min(pw/(w+8),ph/(h+8));cx,cy=x+w/2,y+h/2
   c.saveState();p=c.beginPath();p.rect(px,top-ph,pw,ph);c.clipPath(p,stroke=0,fill=0);c.drawImage(str(img),px+pw/2-cx*s,top-ph/2-cy*s,612*s,792*s);c.restoreState()
 c.showPage();c.save()
if __name__=='__main__':review() if '--review' in sys.argv else build()
