"""Aud v14: one water border colour, organic marsh/moor scattering."""
import inspect,random,math,json,sys,hashlib
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from shapely.geometry import Polygon,Point,box
import render_continuous_v13 as Q
R,S,V,M=Q.R,Q.S,Q.V,Q.M
HERE=Q.HERE;OUT=HERE/'render_full_map_v14'
BORDER='#59635D';SCATTER=[]
OLD_TEXTURE=Q.OLD_TEXTURE

def water_colour(value):return HexColor(BORDER if value.upper()=='#286D70' else value)
# These scratch modules handle all water-bank, lake and legend rendering.
Q.HexColor=water_colour;R.HexColor=water_colour;R.T.HexColor=water_colour

def texture(c,f):
 k=f['kind']
 if k not in ('moor','marsh'):return OLD_TEXTURE(c,f)
 poly=Polygon(f['pts']).buffer(0);x0,y0,x1,y1=poly.bounds
 seed=int(hashlib.sha256(json.dumps(f['pts']).encode()).hexdigest()[:12],16)
 rng=random.Random(seed);marsh=k=='marsh';target=max(1,round(poly.area/(230 if marsh else 255)))
 clusters=[(rng.uniform(x0,x1),rng.uniform(y0,y1)) for _ in range(max(2,target//10))]
 drawn=[]
 for attempt in range(target*150):
  if len(drawn)>=target:break
  if rng.random()<.35:
   ax,ay=rng.choice(clusters);x=rng.gauss(ax,(x1-x0)*.15);y=rng.gauss(ay,(y1-y0)*.15)
  else:x=rng.uniform(x0,x1);y=rng.uniform(y0,y1)
  factor=rng.uniform(.7,1.4 if marsh else 1.65)
  w,h=(10.4*factor,10.4*factor) if marsh else (4.4*factor,3.6*factor)
  if not poly.contains(box(x-w/2,y-h/2,x+w/2,y+h/2)):continue
  if R.T.near(x,y,R.T.LANDMARKS,12):continue
  if any(math.dist((x,y),(xx,yy))<(w+ww)*.5+2 for xx,yy,ww,hh in drawn):continue
  drawn.append((x,y,w,h))
 c.saveState();c.clipPath(S.base._path(c,f,True,f.get('smooth',False)),stroke=0,fill=0)
 for x,y,w,h in sorted(drawn,key=lambda p:-p[1]):
  V.stamp(c,'Marsh_Reeds_v2' if marsh else 'Field_Grass_v5',x,y,w,h)
  if marsh:
   c.setStrokeColor(HexColor('#609E9B'));c.setLineWidth(.35)
   c.line(x-w*.7,y-h*.3,x-w*.3,y-h*.3)
   if rng.random()<.65:c.line(x+w*.2,y-h*.42,x+w*.6,y-h*.42)
  elif rng.random()<.5:
   c.setFillColor(HexColor('#806484'));c.circle(x+w*.2,y+h*.2,max(.22,w*.07),stroke=0,fill=1)
 c.restoreState()
 SCATTER.append({'kind':k,'seed':seed,'icons':len(drawn),'width_range':[min(p[2] for p in drawn),max(p[2] for p in drawn)],'positions':[list(p) for p in drawn]})

def build():
 R.point=Q.point;R.line=Q.line;R.texture=texture;R.legend=Q.legend;R.OUT=OUT;S.draw=Q.draw
 R.T.grid_under_art=Q.grid_under_art
 Base=M.Labeller
 class LegendLabeller(Base):
  def __init__(self):
   super().__init__();self.reserve(Q.LEGEND_BOX[0]-2,Q.LEGEND_BOX[1]-2,Q.LEGEND_BOX[2]+2,Q.LEGEND_BOX[3]+2)
 M.Labeller=LegendLabeller
 src=inspect.getsource(R.build).replace('"Aud_Full_Map_v9.pdf"','"Aud_Full_Map_v14.pdf"')
 exec(compile(src,__file__+'::build','exec'),R.__dict__);R.build()
 assert len(Q.MOUTHS)==9 and len(SCATTER)==3
 assert {r['kind'] for r in SCATTER}=={'moor','marsh'}
 (OUT/'style_changes.json').write_text(json.dumps({'water_border':BORDER,'random_terrain':SCATTER,'new_artwork':False},indent=2))
 print('PASS: one water border colour; all three moor/marsh areas use deterministic irregular positions and variable sizes.')

REGIONS=[('1 - One water border colour',(351,246,46,36)),('2 - Irregular moor scatter and varied sizes',(466,117,67,74)),('3 - Irregular marsh scatter and varied sizes',(196,669,80,65))]
def review():
 c=canvas.Canvas(str(OUT/'Aud_Changes_Review_v14.pdf'),pagesize=(612,792));c.setFillColor(HexColor('#EFE3C4'));c.rect(0,0,612,792,fill=1,stroke=0)
 c.setFillColor(HexColor('#283B34'));c.setFont('Helvetica-Bold',15);c.drawString(24,765,'AUD - WATER BORDERS AND TERRAIN')
 c.setFont('Helvetica',9);c.drawString(24,746,'Consistent coast/river/lake borders; existing terrain artwork in a natural scatter.')
 c.setFont('Helvetica-Bold',9);c.drawString(24,725,'BEFORE');c.drawString(318,725,'AFTER')
 for row,(label,(x,y,w,h)) in enumerate(REGIONS):
  top=697-row*214;ph=185;c.setFont('Helvetica-Bold',9);c.drawString(24,top+6,label)
  for px,img in zip((24,318),(HERE/'render_full_map_v13/Aud_Full_Map_v13.png',OUT/'Aud_Full_Map_v14.png')):
   pw=270;s=min(pw/(w+8),ph/(h+8));cx,cy=x+w/2,y+h/2
   c.saveState();p=c.beginPath();p.rect(px,top-ph,pw,ph);c.clipPath(p,stroke=0,fill=0);c.drawImage(str(img),px+pw/2-cx*s,top-ph/2-cy*s,612*s,792*s);c.restoreState()
 c.showPage();c.save()
if __name__=='__main__':review() if '--review' in sys.argv else build()

