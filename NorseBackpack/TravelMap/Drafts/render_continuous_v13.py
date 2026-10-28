"""Aud v13: true water/coast topology, continuous masonry walls, larger clear legend."""
import inspect,math,json,sys,random
from shapely.geometry import Polygon,LineString,Point,box
from shapely.ops import unary_union
from shapely.affinity import translate
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
import render_corrections_v12 as P
R,S,V,M=P.R,P.S,P.V,P.M
HERE=P.HERE;OUT=HERE/'render_full_map_v13'
WATER=P.WATER
OLD_TEXTURE=P.texture
LEGEND_BOX=(36,112,235,360)
MOUTHS=[];WALL_LOG=[]
LAND=unary_union([Polygon(r).buffer(0) for r in R.L.BASE['land'] if len(r)>3])

def path_geom(c,g):
 p=c.beginPath()
 def ring(coords):
  coords=list(coords)
  if not coords:return
  p.moveTo(*coords[0])
  for q in coords[1:]:p.lineTo(*q)
  p.close()
 def add(g):
  if g.is_empty:return
  if g.geom_type=='Polygon':
   ring(g.exterior.coords)
   for r in g.interiors:ring(r.coords)
  elif g.geom_type in ('LineString','LinearRing'):
   pts=list(g.coords);p.moveTo(*pts[0])
   for q in pts[1:]:p.lineTo(*q)
  elif hasattr(g,'geoms'):
   for gg in g.geoms:add(gg)
 add(g);return p

def samples(f):
 a=[(x,y) for x,y,t in S.base._sample(f,False,f.get('smooth',True),.3)]
 if not a or math.dist(a[-1],f['pts'][-1])>.01:a.append(tuple(f['pts'][-1]))
 return a

def water(c,features):
 fs=[f for f in features if f['kind'] in ('river','stream')]
 inners=[];routes=[];local_mouths=[]
 for f in fs:
  pts=samples(f);outer,inner=P.B.widths(f)
  for end in (0,-1):
   source=f['pts'][end];coast=R.nearest_coast(source);target=None;kind=None
   if math.dist(source,coast)<2.5:target=coast;kind='sea'
   else:
    for lake in features:
     if lake['kind']!='lake':continue
     shore=Polygon(lake['pts']).boundary
     if shore.distance(Point(source))<2:
      q=shore.interpolate(shore.project(Point(source)));target=(q.x,q.y);kind='lake';break
   if target:
    # Extend a short distance into receiving water. Topology clips bank strokes to land.
    adjacent=f['pts'][1 if end==0 else -2];dx=source[0]-adjacent[0];dy=source[1]-adjacent[1];d=math.hypot(dx,dy)
    extended=(target[0]+dx/d*3,target[1]+dy/d*3)
    pts.insert(0,extended) if end==0 else pts.append(extended)
    row={'kind':kind,'endpoint':source,'shore':target};MOUTHS.append(row);local_mouths.append(row)
  route=LineString(pts);routes.append((f,route,outer,inner));inners.append(route.buffer(inner/2,quad_segs=12))
 lakes=unary_union([Polygon(f['pts']).buffer(0) for f in features if f['kind']=='lake'])
 channels=unary_union(inners)
 # Bank ink stays on dry ground: no cap or bank can protrude into the receiving water.
 dry=LAND.difference(lakes)
 c.saveState();c.clipPath(path_geom(c,dry),stroke=0,fill=0,fillMode=0)
 c.setFillColor(HexColor('#286D70'))
 for f,route,outer,inner in routes:c.drawPath(path_geom(c,route.buffer(outer/2,quad_segs=12)),fill=1,stroke=0,fillMode=0)
 c.restoreState()
 c.setFillColor(HexColor(WATER));c.drawPath(path_geom(c,channels),fill=1,stroke=0,fillMode=0)
 # This is one shared land/water boundary, rather than separate shoreline patches.
 dry=dry.difference(channels)
 zones=unary_union([Point(row['shore']).buffer(11) for row in local_mouths])
 coastline=dry.boundary.intersection(zones)
 c.saveState();c.setStrokeColor(HexColor('#59635D'));c.setLineWidth(.55);c.setLineJoin(1);c.setLineCap(1)
 c.drawPath(path_geom(c,coastline),fill=0,stroke=1);c.restoreState()
 # Retain river currents and reeds, with clear space around mouths and crossings.
 for f,route,outer,inner in routes:
  if f['kind']!='river':continue
  ss=S.base._sample(f,False,True,1.2)
  for i in range(6,len(ss)-6,15):
   x,y,a=ss[i]
   if R.T.near(x,y,R.T.CROSS,13) or any(math.dist((x,y),q['endpoint'])<9 for q in local_mouths):continue
   c.setStrokeColor(HexColor('#F2F0D9'));c.setLineWidth(.24);p=c.beginPath()
   for j in range(i,min(i+5,len(ss))):
    xx,yy,aa=ss[j];p.moveTo(xx,yy) if j==i else p.lineTo(xx,yy)
   c.drawPath(p)
   if i%30==6:
    side=1 if (i//15)%2 else -1
    V.stamp(c,'Marsh_Reeds_v2',x-math.sin(a)*(outer/2+2.6)*side,y+math.cos(a)*(outer/2+2.6)*side,4.8,5)

def wall_route(f):
 if math.dist(f['pts'][0],(585.46,501.4))<.1:
  pts=[list(p) for p in f['pts']]
  # A broad, level crossing with a smooth approach on both sides.
  pts[8:15]=[[487,506],[479,510.5],[474,513.12],[465.4,513.12],[456,513.12],[451,507],[447,497]]
  f=dict(f,pts=pts,smooth=True)
 return LineString(samples(dict(f,smooth=True)))

def masonry(c,route,gates=(),key=False):
 # A continuous top ribbon and vertically extruded front share the same centerline.
 half=1.5 if key else 1.85;drop=1.8 if key else 2.25
 top=route.buffer(half,cap_style=2,join_style=1,quad_segs=8)
 front=unary_union([top,translate(top,yoff=-drop)])
 c.saveState()
 if gates:
  holes=unary_union([box(x-7,y-8,x+7,y+8) for x,y in gates])
  clip=box(-100,-100,900,1100).difference(holes)
  c.clipPath(path_geom(c,clip),stroke=0,fill=0,fillMode=0)
 c.setLineJoin(1);c.setLineCap(1);c.setLineWidth(.38)
 c.setStrokeColor(HexColor('#4C5045'));c.setFillColor(HexColor('#8D9180'));c.drawPath(path_geom(c,front),fill=1,stroke=1,fillMode=0)
 c.setFillColor(HexColor('#BEC0AD'));c.drawPath(path_geom(c,top),fill=1,stroke=1,fillMode=0)
 # Sparse irregular joints across the wall cap; front joints continue downwards.
 rng=random.Random(391);distance=0
 c.setStrokeColor(HexColor('#626758'));c.setLineWidth(.3)
 while distance<route.length:
  d=min(distance,route.length);p=route.interpolate(d);a=route.interpolate(max(0,d-.2));b=route.interpolate(min(route.length,d+.2))
  dx,dy=b.x-a.x,b.y-a.y;ln=math.hypot(dx,dy)
  if ln:
   nx,ny=-dy/ln,dx/ln
   x1,y1=p.x+nx*half,p.y+ny*half;x2,y2=p.x-nx*half,p.y-ny*half
   q=c.beginPath();q.moveTo(x1,y1);q.lineTo(p.x+.25,p.y+.15);q.lineTo(x2,y2);c.drawPath(q)
   # Screen-lower side is the visible masonry face.
   xx,yy=(x1,y1) if y1<y2 else (x2,y2);c.line(xx,yy,xx,yy-drop)
  distance+=rng.uniform(4.3,6.4) if not key else rng.uniform(4,5)
 c.restoreState()

def line(c,f,road_pass=None,gate_gaps=None):
 if f['kind']=='wall':
  route=wall_route(f);masonry(c,route,gate_gaps or [])
  WALL_LOG.append({'length':route.length,'continuous_surface':True});return
 return P.line(c,f,road_pass,gate_gaps)

def gate(c,x,y):
 # Horizontal wooden gate: posts meet wall ends and rails span the road.
 c.saveState();c.setStrokeColor(HexColor('#70576D'));c.setFillColor(HexColor('#E8DDC5'));c.setLineWidth(.55);c.setLineJoin(1)
 for px in (x-7,x+7):
  p=c.beginPath();p.moveTo(px-1,y-2.4);p.lineTo(px+1,y-2.4);p.lineTo(px+1,y+5);p.lineTo(px,y+6);p.lineTo(px-1,y+5);p.close();c.drawPath(p,fill=1,stroke=1)
 for yy in (y-.1,y+3.1):
  c.rect(x-6,yy,12,1,stroke=1,fill=1)
 c.line(x-5.8,y+.8,x+5.8,y+3.2);c.setLineWidth(.25);c.line(x-6,y-1.7,x+6,y-1.7)
 c.restoreState()

def point(c,f,angle=0):
 if f['kind']=='gate' and math.dist(f['pts'][0],(465.4,513.12))<.1:return gate(c,*f['pts'][0])
 return P.point(c,f,angle)

def legend(c,features,box_unused,**kw):
 x0,y0,x1,y1=LEGEND_BOX;present={f['kind'] for f in features}
 rows=[(k,n) for k,n in S.base.LEGEND_ORDER if k in present and k!='marker'];per=(len(rows)+1)//2;colw=(x1-x0-10)/2
 c.saveState();c.setFillColor(HexColor('#F4EEDD'));c.setStrokeColor(HexColor('#A99A7B'));c.setLineWidth(.7);c.rect(x0,y0,x1-x0,y1-y0,fill=1,stroke=1)
 c.setFillColor(HexColor('#283B34'));c.setFont('Helvetica-Bold',8.5);c.drawCentredString((x0+x1)/2,y1-11,'LEGEND')
 c.setStrokeColor(HexColor('#A99A7B'));c.setLineWidth(.45);c.line(x0+5,y1-15,x1-5,y1-15)
 top=y1-19;rh=(top-y0-5)/per
 for i,(kind,name) in enumerate(rows):
  col,row=divmod(i,per);cx=x0+5+col*colw;cy=top-(row+.5)*rh;sw=cx+12
  if kind in S.LINE:
   if kind=='wall':masonry(c,LineString([(cx,cy),(cx+24,cy)]),key=True)
   elif kind=='hedge':V.stamp(c,'Hedge_Clump_v4',sw,cy,24,8)
   else:line(c,{'kind':kind,'pts':[[cx,cy],[cx+24,cy]],'smooth':False})
  elif kind in S.AREA:
   if kind=='wood':
    V.stamp(c,'Conifer_v3',cx+6,cy,7,12);V.stamp(c,'Birch_v3',cx+17,cy,11,12)
   elif kind=='marsh':V.stamp(c,'Marsh_Reeds_v2',sw,cy,13,12)
   elif kind=='moor':V.stamp(c,'Field_Grass_v5',sw,cy,14,10)
   elif kind=='lake':
    c.setFillColor(HexColor(WATER));c.setStrokeColor(HexColor('#286D70'));c.setLineWidth(.6);c.rect(cx,cy-5,24,10,fill=1,stroke=1)
   elif kind=='field':R.F.field(c,{'kind':kind,'pts':[[cx,cy-5],[cx+24,cy-5],[cx+24,cy+5],[cx,cy+5]],'smooth':False},True)
  else:
   asset=R.A.SIZES[kind][0] if kind in R.A.KINDS else R.EXTRA.get(kind)
   asset=asset or {'port':'Landing_Shore_v6','bridge':'Bridge_River_v3','ford':'Ford_Full_v9','gate':'Gate_Open_v4'}[kind]
   V.stamp(c,asset,sw,cy,25,15)
  c.setFillColor(HexColor('#283B34'));c.setFont('Helvetica',6.5);c.drawString(cx+29,cy-2.2,name)
 c.restoreState()

# Retain v12 terrain order and density; dispatch the new geometry before roads/trees.
env=dict(P.B.__dict__);env.update(water=water,point=point,line=line)
src=inspect.getsource(P.B.draw).replace('C.line(c,','line(c,')
exec(compile(src,'v13_draw','exec'),env);draw=env['draw']

def grid_under_art():
 source=inspect.getsource(M.build)
 a=source.index('    # The drawn symbol layer');b=source.index('    # Reference grid',a);d=source.index('    lab = Labeller()',b)
 source=source[:a]+source[b:d]+source[a:b]+source[d:]
 source=source.replace('for text, lat, lon, rot in cfg["waters"]:\n        x, y = pt(lon, lat)', 'for text, lat, lon, rot in cfg["waters"]:\n        x, y = pt(lon, lat)\n        if key == "aud" and text.startswith("FAXA"):\n            x, y, rot = 249, 176, 90')
 exec(compile(source,'v13_layout','exec'),M.__dict__)

def build():
 R.point=point;R.line=line;R.texture=OLD_TEXTURE;R.legend=legend;R.OUT=OUT;S.draw=draw
 R.T.grid_under_art=grid_under_art
 Base=M.Labeller
 class LegendLabeller(Base):
  def __init__(self):
   super().__init__();self.reserve(LEGEND_BOX[0]-2,LEGEND_BOX[1]-2,LEGEND_BOX[2]+2,LEGEND_BOX[3]+2)
 M.Labeller=LegendLabeller
 src=inspect.getsource(R.build).replace('"Aud_Full_Map_v9.pdf"','"Aud_Full_Map_v13.pdf"')
 exec(compile(src,__file__+'::build','exec'),R.__dict__);R.build()
 assert len(MOUTHS)==9 and len(WALL_LOG)==3
 (OUT/'style_changes.json').write_text(json.dumps({'water_mouths':MOUTHS,'continuous_wall_surfaces':WALL_LOG,'legend_box':LEGEND_BOX,'legend_text_points':6.5,'terrain_key_backgrounds':False},indent=2))

REGIONS=[('1 - Joined coastline and river banks',(290,649,39,37)),('2 - Continuous masonry and aligned gate',(443,488,54,49)),('3 - Larger legend, plain terrain symbols',(34,108,204,256))]
def review():
 c=canvas.Canvas(str(OUT/'Aud_Changes_Review_v13.pdf'),pagesize=(612,792));c.setFillColor(HexColor('#EFE3C4'));c.rect(0,0,612,792,fill=1,stroke=0)
 c.setFillColor(HexColor('#283B34'));c.setFont('Helvetica-Bold',15);c.drawString(24,765,'AUD - COASTLINE, WALL AND LEGEND')
 c.setFont('Helvetica',9);c.drawString(24,747,'Continuous surfaces and boundaries; larger legend with plain wood, marsh and moor symbols.')
 c.setFont('Helvetica-Bold',9);c.drawString(24,725,'BEFORE');c.drawString(318,725,'AFTER')
 for row,(label,(x,y,w,h)) in enumerate(REGIONS):
  top=(697,520,339)[row];ph=(151,151,285)[row];c.setFont('Helvetica-Bold',9);c.drawString(24,top+5,label)
  for px,img in zip((24,318),(HERE/'render_full_map_v12/Aud_Full_Map_v12.png',OUT/'Aud_Full_Map_v13.png')):
   pw=270;s=min(pw/(w+6),ph/(h+6));cx,cy=x+w/2,y+h/2
   c.saveState();p=c.beginPath();p.rect(px,top-ph,pw,ph);c.clipPath(p,stroke=0,fill=0);c.drawImage(str(img),px+pw/2-cx*s,top-ph/2-cy*s,612*s,792*s);c.restoreState()
 c.showPage();c.save()
if __name__=='__main__':review() if '--review' in sys.argv else build()
