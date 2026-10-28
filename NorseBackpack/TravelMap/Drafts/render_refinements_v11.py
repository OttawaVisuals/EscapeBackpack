"""Aud v11: connected water, forest over roads, stone clearance, larger legend."""
import math,inspect,json,sys
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor,Color
import render_crossings_v10 as C
R,S,V,M=C.R,C.S,C.V,C.M
HERE=C.HERE
OUT=HERE/'render_full_map_v11'
JOINS=[]

def widths(f):
 w=f.get('w') or S.LINE[f['kind']]['w']; outer=w+(3 if f['kind']=='river' else .8)
 return outer,outer-(.8 if f['kind']=='river' else .4)

def water(c,features):
 fs=[f for f in features if f['kind'] in ('river','stream')]
 # All bank outlines precede all water fills: confluences have no internal seams.
 c.saveState(); c.setLineCap(1);c.setLineJoin(1)
 for passno in (0,1):
  c.setStrokeColor(HexColor('#286D70' if passno==0 else '#78AAA7'))
  for f in fs:
   c.setLineWidth(widths(f)[passno]);c.drawPath(S.base._path(c,f,False,f.get('smooth',True)))
 for i,f in enumerate(fs):
  for end in (0,-1):
   p=f['pts'][end]; neighbour=f['pts'][1 if end==0 else -2]
   vx,vy=p[0]-neighbour[0],p[1]-neighbour[1];length=math.hypot(vx,vy);vx/=length;vy/=length
   q=R.nearest_coast(p); kind=None; target=None
   if math.dist(p,q)<2.5:
    kind='sea';target=q;colour=HexColor('#DCE7E4')
   else:
    for g in features:
     if g['kind']=='lake':
      samples=S.base._sample(g,True,g.get('smooth',False),.3)
      distance,x,y=min((math.dist(p,(x,y)),x,y) for x,y,a in samples)
      if distance<2:kind='lake';target=(x,y);colour=HexColor('#A7C8C2');break
   if kind:
    # Open/flared mouth masks the coast/lake rim; a short colour transition joins water surfaces.
    inner=widths(f)[1];nx,ny=-vy,vx
    a=(p[0]-vx*3,p[1]-vy*3);b=(target[0]+vx*3,target[1]+vy*3)
    start=HexColor('#78AAA7')
    for j in range(24):
     t0=j/24;t1=(j+1)/24;t=(t0+t1)/2
     c.setFillColor(Color(start.red+(colour.red-start.red)*t,start.green+(colour.green-start.green)*t,start.blue+(colour.blue-start.blue)*t))
     path=c.beginPath()
     for n,(u,side) in enumerate(((t0,1),(t1,1),(t1,-1),(t0,-1))):
      half=inner/2+u*.9;x=a[0]+(b[0]-a[0])*u+nx*half*side;y=a[1]+(b[1]-a[1])*u+ny*half*side
      path.moveTo(x,y) if n==0 else path.lineTo(x,y)
     path.close();c.drawPath(path,fill=1,stroke=0)
    JOINS.append({'kind':kind,'endpoint':p,'shore':target})
  if f['kind']=='river':
   samples=S.base._sample(f,False,True,1.2);outer=widths(f)[0]
   for j in range(6,len(samples)-6,15):
    x,y,a=samples[j]
    if R.T.near(x,y,R.T.CROSS,13):continue
    c.setStrokeColor(HexColor('#E9EDCF'));c.setLineWidth(.24);path=c.beginPath()
    for n in range(j,min(j+5,len(samples))):
     xx,yy,aa=samples[n];off=.7 if (j//15)%2 else -.7;xx-=math.sin(aa)*off;yy+=math.cos(aa)*off
     path.moveTo(xx,yy) if n==j else path.lineTo(xx,yy)
    c.drawPath(path)
    if j%30==6:
     side=1 if (j//15)%2 else -1
     V.stamp(c,'Marsh_Reeds_v2',x-math.sin(a)*(outer/2+2.6)*side,y+math.cos(a)*(outer/2+2.6)*side,4.8,5)
 c.restoreState()

def point(c,f,angle=0):
 if f['kind']=='stone' and math.dist(f['pts'][0],(430.82,189.82))<.1:
  f=dict(f,pts=[[f['pts'][0][0]-8,f['pts'][0][1]]])
 return C.point(c,f,angle)

def draw(c,features,clip_rect=None):
 c.saveState()
 if clip_rect:
  p=c.beginPath();p.rect(clip_rect[0],clip_rect[1],clip_rect[2]-clip_rect[0],clip_rect[3]-clip_rect[1]);c.clipPath(p,stroke=0,fill=0)
 for f in features:
  if f['kind'] in S.AREA and f['kind']!='wood' and len(f['pts'])>2:
   if f['kind']=='field':
    c.setStrokeColor(HexColor('#9A7545'));c.setLineWidth(.5);c.drawPath(S.base._path(c,f,True,f.get('smooth',False)),fill=0,stroke=1)
   R.texture(c,f)
 water(c,features)
 gaps=[f['pts'][0] for f in features if f['kind']=='gate']
 for f in features:
  if f['kind'] in S.LINE and f['kind'] not in ('road','river','stream') and len(f['pts'])>1:C.line(c,f,gate_gaps=gaps)
 for stage in ('casing','fill'):
  for f in features:
   if f['kind']=='road' and len(f['pts'])>1:C.line(c,f,stage)
 for f in features:
  if f['kind']=='wood':R.texture(c,f)
 angles=S.crossing_angles(features)
 for crossing in (False,True):
  for i,f in enumerate(features):
   if len(f['pts'])==1 and (f['kind'] in ('bridge','ford','gate'))==crossing:point(c,f,angles.get(i,0))
 c.restoreState()

OLD_LEGEND=R.legend

def legend(c,features,box,**kw):
 # Reuse the proven swatches; replace only the live key's layout in its isolated module.
 import importlib.util
 original=importlib.util.module_from_spec
 def module(spec):
  key=original(spec)
  if spec.name=='aud_full_v9_key':
   loader=spec.loader;exec_module=loader.exec_module
   def load(k):
    exec_module(k)
    src=inspect.getsource(k.draw_legend)
    src=src.replace('cy = top - row * row_h - row_h / 2','rh = min(14.4, (top-y0-8)/(len(rows)-per)) if col else row_h\n        cy = top - row * rh - rh / 2')
    src=src.replace('c.scale(0.62, 0.62)','c.scale(1.18 if col else 0.62, 1.0 if col else 0.62)')
    src=src.replace('cx + 22, cy - 1.8','cx + (25 if col else 22), cy - 1.8')
    exec(compile(src,'v11_legend','exec'),k.__dict__)
   loader.exec_module=load
  return key
 importlib.util.module_from_spec=module
 try:OLD_LEGEND(c,features,box,**kw)
 finally:importlib.util.module_from_spec=original

def build():
 R.point=point;R.line=C.line;R.legend=legend;R.OUT=OUT;S.draw=draw
 src=inspect.getsource(R.build).replace('"Aud_Full_Map_v9.pdf"','"Aud_Full_Map_v11.pdf"')
 exec(compile(src,__file__+'::build','exec'),R.__dict__);R.build()
 assert len(JOINS)==9,len(JOINS)
 (OUT/'style_changes.json').write_text(json.dumps({'water_mouths':JOINS,'water_passes':['all banks','all fills','open sea/lake mouths','currents'],'layer_order':['grid','terrain','water','boundaries','roads','trees','landmarks','crossings'],'stone_shift':{'from':[430.82,189.82],'to':[422.82,189.82]},'legend_landmarks_scale_from_v10':[1.18/.62,1/.62]},indent=2))

REGIONS=[('1 - Open water joins',(292,650,35,31)),('2 - Trees above roads',(497,417,76,59)),('3 - Stone moved left',(410,167,47,37)),('4 - Larger legend icons',(122,120,68,151))]
def review():
 c=canvas.Canvas(str(OUT/'Aud_Changes_Review_v11.pdf'),pagesize=(612,792));c.setFillColor(HexColor('#EFE3C4'));c.rect(0,0,612,792,fill=1,stroke=0)
 c.setFillColor(HexColor('#283B34'));c.setFont('Helvetica-Bold',15);c.drawString(24,765,'AUD - MAP REFINEMENTS')
 c.setFont('Helvetica',9);c.drawString(24,746,'Four annotated changes. All crossing symbols and ticket markers retained.')
 c.setFont('Helvetica-Bold',9);c.drawString(24,725,'BEFORE');c.drawString(318,725,'AFTER')
 for row,(label,(x,y,w,h)) in enumerate(REGIONS):
  top=697-row*164;c.setFont('Helvetica-Bold',9);c.drawString(24,top+7,label)
  for px,img in zip((24,318),(HERE/'render_full_map_v10/Aud_Full_Map_v10.png',OUT/'Aud_Full_Map_v11.png')):
   pw,ph=270,142;s=min(pw/(w+12),ph/(h+12));cx,cy=x+w/2,y+h/2
   c.saveState();p=c.beginPath();p.rect(px,top-ph,pw,ph);c.clipPath(p,stroke=0,fill=0);c.drawImage(str(img),px+pw/2-cx*s,top-ph/2-cy*s,612*s,792*s);c.restoreState()
 c.showPage();c.save()
if __name__=='__main__':review() if '--review' in sys.argv else build()


