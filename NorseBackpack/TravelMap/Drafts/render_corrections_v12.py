"""Aud v12: solid connected water, larger wall/legend crossings and fuller wood."""
import inspect,math,json,sys,random
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
import render_refinements_v11 as B
R,S,V,M=B.R,B.S,B.V,B.M
HERE=B.HERE;OUT=HERE/'render_full_map_v12'
OLD_TEXTURE=R.texture
OLD_POINT=B.point
OLD_LINE=B.C.line
WATER='#DCE7E4'
EXTRA_TREES=[]


def point(c,f,angle=0):
 if f['kind']=='gate' and math.dist(f['pts'][0],(465.4,513.12))<.1:
  return V.stamp(c,'Gate_Open_v4',*f['pts'][0],18,12)
 return OLD_POINT(c,f,angle)

def wall_feature(f):
 if math.dist(f['pts'][0],(585.46,501.4))<.1:
  f=dict(f,pts=[list(p) for p in f['pts']])
  # Horizontal seat at the road; connect to the original wall on either side.
  f['pts'][9:13]=[[479,513.12],[474.29,513.12],[465.4,513.12],[456,513.12]]
 return f

def line(c,f,road_pass=None,gate_gaps=None):
 if f['kind'] in ('river','stream'):
  original=R.T.HexColor
  R.T.HexColor=lambda value:original(WATER if value=='#78AAA7' else value)
  try:return OLD_LINE(c,f,road_pass,gate_gaps)
  finally:R.T.HexColor=original
 if f['kind']!='wall':return OLD_LINE(c,f,road_pass,gate_gaps)
 f=wall_feature(f)
 c.saveState()
 if gate_gaps:
  p=c.beginPath();p.rect(-100,-100,900,1100)
  for x,y in gate_gaps:p.circle(x,y,5.8)
  c.clipPath(p,stroke=0,fill=0,fillMode=0)
 # Larger overlapping clusters on a smooth tangent make a continuous stone wall.
 for x,y,a in S.base._sample(f,False,True,8):
  c.saveState();c.translate(x,y);c.rotate(math.degrees(a));V.stamp(c,'Wall_Clump_v9',0,0,17,7);c.restoreState()
 c.restoreState()

def texture(c,f):
 if f['kind']=='lake':
  # Keep the existing ripple treatment, using the same solid water fill as sea/rivers.
  original=R.HexColor
  R.HexColor=lambda value:original(WATER if value=='#A7C8C2' else value)
  try:return OLD_TEXTURE(c,f)
  finally:R.HexColor=original
 if f['kind']=='wood' and min(p[1] for p in f['pts'])<350 and max(p[1] for p in f['pts'])>480:
  # Densify only the marked woodland. Retain its polygon, mixed species and landmark clearance.
  src=inspect.getsource(R.T.wood).replace('def wood(', 'def dense_wood(').replace(',15)',',12)').replace('(row%2)*7','(row%2)*6')
  env=dict(R.T.__dict__);exec(compile(src,'v12_wood','exec'),env)
  c.saveState();c.clipPath(S.base._path(c,f,True,False),stroke=0,fill=0)
  env['dense_wood'](c,f);c.restoreState();return
 return OLD_TEXTURE(c,f)

# Keep v11 water path and current details; replace the fade with one solid opening.
src=inspect.getsource(B.water)
src=src.replace("'#78AAA7'","'#DCE7E4'")
start=src.index('    start=HexColor(');end=src.index('    JOINS.append',start)
src=src[:start]+'''    c.setFillColor(HexColor('#DCE7E4'))
    path=c.beginPath()
    for n,(u,side) in enumerate(((0,1),(1,1),(1,-1),(0,-1))):
     half=inner/2+u*.5;x=a[0]+(b[0]-a[0])*u+nx*half*side;y=a[1]+(b[1]-a[1])*u+ny*half*side
     path.moveTo(x,y) if n==0 else path.lineTo(x,y)
    path.close();c.drawPath(path,fill=1,stroke=0)
'''+src[end:]
exec(compile(src,'v12_water','exec'),B.__dict__)

# Same enlarged scale for all point symbols in the legend, including bridge/ford/gate.
src=inspect.getsource(B.legend).replace('1.18 if col else 0.62, 1.0 if col else 0.62','1.18, 1.0').replace('cx + (25 if col else 22)','cx + 25')
exec(compile(src,'v12_legend','exec'),B.__dict__)

# v11 layering, with the updated wall and point dispatchers.
src=inspect.getsource(B.draw).replace('C.line(c,','line(c,')
env=dict(B.__dict__);env.update(line=line,point=point)
exec(compile(src,'v12_draw','exec'),env);draw=env['draw']

def build():
 R.point=point;R.line=line;R.texture=texture;R.legend=B.legend;R.OUT=OUT;S.draw=draw
 # draw has a snapshot of B globals, while R remains shared.
 src=inspect.getsource(R.build).replace('"Aud_Full_Map_v9.pdf"','"Aud_Full_Map_v12.pdf"')
 exec(compile(src,__file__+'::build','exec'),R.__dict__);R.build()
 assert len(B.JOINS)==9
 (OUT/'style_changes.json').write_text(json.dumps({'water_fill':WATER,'fade':False,'open_mouths':B.JOINS,'gate':{'position':[465.4,513.12],'barrier_angle':0},'wall':{'stamp_width':17,'stamp_height':7,'spacing':8,'smooth':True},'wood_grid_spacing':{'marked_polygon':12,'other_woods':15},'legend_point_scale':[1.18,1]},indent=2))

REGIONS=[('1 - Larger crossing symbols',(47,163,48,50)),('2 - Solid water connection',(357,247,30,29)),('3 - Horizontal gate and wall',(448,495,39,30)),('4 - Larger connected wall stones',(425,449,26,37)),('5 - More trees',(467,346,49,136))]
def review():
 c=canvas.Canvas(str(OUT/'Aud_Changes_Review_v12.pdf'),pagesize=(612,792));c.setFillColor(HexColor('#EFE3C4'));c.rect(0,0,612,792,fill=1,stroke=0)
 c.setFillColor(HexColor('#283B34'));c.setFont('Helvetica-Bold',15);c.drawString(24,765,'AUD - FIVE MAP CORRECTIONS')
 c.setFont('Helvetica',9);c.drawString(24,747,'Solid water connections, consistent legend symbols, wall/gate details and fuller wood.')
 c.setFont('Helvetica-Bold',9);c.drawString(24,726,'BEFORE');c.drawString(318,726,'AFTER')
 for row,(label,(x,y,w,h)) in enumerate(REGIONS):
  top=698-row*132;c.setFont('Helvetica-Bold',9);c.drawString(24,top+5,label)
  for px,img in zip((24,318),(HERE/'render_full_map_v11/Aud_Full_Map_v11.png',OUT/'Aud_Full_Map_v12.png')):
   pw,ph=270,112;s=min(pw/(w+8),ph/(h+8));cx,cy=x+w/2,y+h/2
   c.saveState();p=c.beginPath();p.rect(px,top-ph,pw,ph);c.clipPath(p,stroke=0,fill=0);c.drawImage(str(img),px+pw/2-cx*s,top-ph/2-cy*s,612*s,792*s);c.restoreState()
 c.showPage();c.save()
if __name__=='__main__':review() if '--review' in sys.argv else build()
