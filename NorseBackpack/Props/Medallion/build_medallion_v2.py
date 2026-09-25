"""Single solid medallion: millimetres, text down, crest up. No glue.

Build geometry from the saved crest mask and measured font outlines.
Requires numpy, Pillow, opencv-python, matplotlib, shapely >= 2.1.
The mesh is built from exact polygon layer boundaries, not a bitmap height field.
"""
from pathlib import Path
import json, math, struct
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from matplotlib.textpath import TextPath
from matplotlib.font_manager import FontProperties
from shapely import constrained_delaunay_triangles
from shapely.geometry import Polygon, Point, LineString
from shapely.geometry.polygon import orient
from shapely.ops import unary_union
from shapely import affinity

ROOT = Path(__file__).resolve().parent
FONT = FontProperties(fname='C:/Windows/Fonts/arialbd.ttf')
DIAMETER, BODY, HEIGHT, ENGRAVE = 50., 3.8, 4.4, .4

def polys(g):
    if g.is_empty: return []
    return [g] if g.geom_type == 'Polygon' else [p for p in g.geoms if p.geom_type == 'Polygon']

def radius(g):
    return max(math.hypot(x,y) for p in polys(g) for x,y in p.exterior.coords)

def svg(g, name):
    paths=[]
    for p in polys(g):
        p=orient(p,1)
        for ring in [p.exterior,*p.interiors]:
            paths.append('M '+' L '.join(f'{x+25:.5f},{25-y:.5f}' for x,y in list(ring.coords)[:-1])+' Z')
    (ROOT/name).write_text('<svg xmlns="http://www.w3.org/2000/svg" width="50mm" height="50mm" viewBox="0 0 50 50"><path fill="black" fill-rule="nonzero" d="'+' '.join(paths)+'"/></svg>',encoding='utf-8')

def trace_crest():
    raw=Image.open(ROOT/'sources/Crest_Detailed_v2.png').convert('RGBA')
    white=Image.new('RGBA',raw.size,'white'); white.alpha_composite(raw)
    mask=(np.array(white.convert('L'))<128).astype('uint8')*255
    cs,tree=cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE); tree=tree[0]
    def pts(c): return cv2.approxPolyDP(c,.65,True).reshape(-1,2)
    parts=[]
    for i,c in enumerate(cs):
        dep,pa=0,tree[i][3]
        while pa>=0: dep+=1;pa=tree[pa][3]
        if dep%2 or cv2.contourArea(c)<16: continue
        holes=[pts(cc) for j,cc in enumerate(cs) if tree[j][3]==i and cv2.contourArea(cc)>16]
        parts.extend(polys(Polygon(pts(c),holes).buffer(0)))
    g=unary_union(parts)
    a,b,c,d=g.bounds
    g=affinity.translate(g,-(a+c)/2,-(b+d)/2)
    scale=21.8/radius(g)
    g=affinity.scale(g,scale,-scale,origin=(0,0))
    # Widen the feather channels by 0.16 mm; retain the source separately.
    g=g.buffer(-.08,join_style='round').simplify(.008,preserve_topology=True)
    return unary_union([p for p in polys(g) if p.area>.035 and not p.buffer(-.2).is_empty])

def glyph(c, cap):
    # Large source path keeps flattened Bezier curves smooth at printing scale.
    path=TextPath((0,0),c,size=100,prop=FONT)
    rings=path.to_polygons(); g=Polygon()
    for ring in rings:
        if len(ring)>3: g=g.symmetric_difference(Polygon(ring).buffer(0))
    cap100=TextPath((0,0),'H',size=100,prop=FONT).get_extents().height
    g=affinity.scale(g,cap/cap100,cap/cap100,origin=(0,0))
    a,b,c,d=g.bounds
    return affinity.translate(g,-(a+c)/2,-b)

def arc_text(s,cap,r,span,bottom=False,thicken=0):
    gs=[glyph(c,cap).buffer(thicken,join_style='round') if c!=' ' else None for c in s]
    widths=[g.bounds[2]-g.bounds[0] if g is not None else cap*.55 for g in gs]
    arc=math.radians(span)*r
    spacing=(arc-sum(widths))/(len(s)-1)
    if spacing<.4: raise ValueError(f'{s}: character spacing is too small: {spacing}')
    pos=-arc/2; result=[]
    for g,w in zip(gs,widths):
        ang=(pos+w/2)/r; deg=math.degrees(ang)
        if g is not None:
            g=affinity.rotate(g,deg if bottom else -deg,origin=(0,0))
            g=affinity.translate(g,r*math.sin(ang),(-1 if bottom else 1)*r*math.cos(ang))
            result.append(g)
        pos+=w+spacing
    return unary_union(result)

def build_back():
    text={
        'ADVENTURE':arc_text('ADVENTURE',4.1,16.2,139),
        'COMPLETE':arc_text('COMPLETE',4.1,18.1,115,bottom=True),
        'ESCAPE BACKPACK':arc_text('ESCAPE BACKPACK',2.25,22.1,116,bottom=True,thicken=.055)
    }
    # Outline compass keeps every underside bridge narrow.
    vertices=[]
    for i in range(8):
        ang=math.pi/2+i*math.pi/4; rr=9.1 if i%2==0 else 1.7
        vertices.append((rr*math.cos(ang),rr*math.sin(ang)))
    star=LineString(vertices+[vertices[0]]).buffer(.30,join_style='round')
    circle=Point(0,0).buffer(7.3,quad_segs=96).boundary.buffer(.28)
    ticks=[]
    for i in range(4):
        a=math.pi/4+i*math.pi/2
        ticks.append(LineString([(4.5*math.cos(a),4.5*math.sin(a)),(5.9*math.cos(a),5.9*math.sin(a))]).buffer(.3))
    compass=unary_union([star,circle,*ticks])
    rim=Point(0,0).buffer(23.65,quad_segs=128).boundary.buffer(.25)
    return unary_union([*text.values(),compass,rim]), text, compass

def make_mesh(layers):
    triangles=[]
    def flat(g,z,up):
        for p in polys(g):
            for t in constrained_delaunay_triangles(p).geoms:
                xy=np.array(t.exterior.coords)[:3]
                a,b=xy[1]-xy[0],xy[2]-xy[0]
                cross=a[0]*b[1]-a[1]*b[0]
                if (cross>0)!=up: xy=xy[::-1]
                triangles.append(np.column_stack([xy,np.full(3,z)]))
    previous=Polygon()
    for bottom,top,g in layers:
        flat(g.difference(previous),bottom,False)
        flat(previous.difference(g),bottom,True)
        for p in polys(g):
            p=orient(p,1)
            for ring in [p.exterior,*p.interiors]:
                xy=list(ring.coords)
                for a,b in zip(xy,xy[1:]):
                    v0=(*a,bottom); v1=(*b,bottom); v2=(*b,top); v3=(*a,top)
                    triangles.extend([[v0,v1,v2],[v0,v2,v3]])
        previous=g
    flat(previous,layers[-1][1],True)
    return np.asarray(triangles,dtype=np.float64)

def write_stl(tri,path):
    normals=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]); normals/=np.linalg.norm(normals,axis=1)[:,None]
    with path.open('wb') as f:
        f.write(b'Escape Backpack | Norse keepsake v2 | mm | engraved back DOWN'.ljust(80,b' '))
        f.write(struct.pack('<I',len(tri)))
        for n,t in zip(normals,tri): f.write(struct.pack('<12fH',*n,*t.ravel(),0))

def raster(g,size=1600):
    out=Image.new('L',(size,size),0); d=ImageDraw.Draw(out)
    def xy(r): return [((x+27)/54*size,(27-y)/54*size) for x,y in r.coords]
    for p in sorted(polys(g),key=lambda p:(p.bounds[2]-p.bounds[0])*(p.bounds[3]-p.bounds[1]),reverse=True):
        d.polygon(xy(p.exterior),fill=255)
        for h in p.interiors: d.polygon(xy(h),fill=0)
    return np.array(out)>0

def preview(disk,crest,back,groove):
    # Height render of the exact polygons used to create the mesh.
    size=1600; inside=raster(disk,size); cm=raster(crest,size); bm=raster(back,size)
    def render(front):
        h=np.full((size,size),-1.,dtype='float32'); h[inside]=0
        h[cm if front else bm]=.6 if front else -.4
        if front: h[raster(groove,size)]=-.2
        smooth=cv2.GaussianBlur(h,(0,0),1.4)
        gy,gx=np.gradient(smooth,54/size)
        light=np.clip((1-.35*gx-.5*gy)/np.sqrt(1+gx*gx+gy*gy),.22,1.5)
        rgb=np.empty((size,size,3),dtype='float32');rgb[:]=[229,233,232]
        rgb[inside]=[149,157,160]
        if front: rgb[cm]=[201,159,79]
        rgb[inside]*=(.68+.34*light[inside,None])
        if not front: rgb[bm]*=.72
        rgb[~inside]=[245,243,237]
        return Image.fromarray(np.uint8(np.clip(rgb,0,255)))
    out=Image.new('RGB',(2000,1170),'#f5f3ed');d=ImageDraw.Draw(out)
    font=ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',30)
    small=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',25)
    out.paste(render(True).resize((930,930),Image.Resampling.LANCZOS),(35,60))
    out.paste(render(False).resize((930,930),Image.Resampling.LANCZOS),(1035,60))
    d.text((65,1010),'FRONT / PRINTS UP',fill='#25372f',font=font)
    d.text((1065,1010),'BACK / PRINTS DOWN',fill='#25372f',font=font)
    d.text((65,1055),'Detailed raised crest - optional second colour',fill='#53615b',font=small)
    d.text((1065,1055),'Recessed lettering - same filament as the body',fill='#53615b',font=small)
    d.text((65,1120),'50 mm diameter | 4.4 mm thick | One solid print | CAD geometry preview; colours illustrative',fill='#53615b',font=small)
    out.save(ROOT/'Medallion_v2_Preview.png')

def main():
    crest=trace_crest(); back,text,compass=build_back()
    disk=Point(0,0).buffer(DIAMETER/2,quad_segs=128)
    groove=Point(0,0).buffer(23.4,quad_segs=128).boundary.buffer(.3)
    bottom_cut=affinity.scale(back,-1,1,origin=(0,0))
    layers=[(0,.4,disk.difference(bottom_cut)),(.4,3.6,disk),(3.6,3.8,disk.difference(groove)),(3.8,4.4,crest)]
    mesh=make_mesh(layers)
    out=ROOT/'STL/Norse_Medallion_OnePiece_v2.stl';out.parent.mkdir(exist_ok=True)
    write_stl(mesh,out)
    svg(crest,'Crest_Relief_v2.svg');svg(back,'Back_Engraving_v2.svg')
    preview(disk,crest,back,groove)
    report={'dimensions_mm':np.ptp(mesh.reshape(-1,3),axis=0).tolist(),'triangles':len(mesh),'body_top_mm':BODY,'total_height_mm':HEIGHT,'engraving_depth_mm':ENGRAVE,'text_max_radius_mm':{s:round(radius(g),3) for s,g in text.items()},'crest_max_radius_mm':round(radius(crest),3),'text_clearance_to_rim_mm':round(23.4-max(radius(g) for g in text.values()),3),'minimum_distance_between_text_groups_mm':round(min(g.distance(h) for i,g in enumerate(text.values()) for j,h in enumerate(text.values()) if i<j),3),'crest_components':len(polys(crest)),'physical_print_test':False}
    (ROOT/'geometry_report_v2.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2))

if __name__=='__main__': main()
