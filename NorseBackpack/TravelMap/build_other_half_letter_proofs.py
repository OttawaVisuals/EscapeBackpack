"""Leif, Rollo and Harald proofs matching the approved Aud half-Letter direction.

Non-destructive: outputs under output/other-maps-half-letter only. Current Letter
maps/ruler remain untouched. Includes a matched Rollo ruler and Harald reverse.
"""
from pathlib import Path
from copy import deepcopy
import hashlib
import io
import json
import math
import sys
import zipfile

import pymupdf as fitz
from pyproj import CRS, Transformer
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

HERE=Path(__file__).resolve().parent
PROJECT=HERE.parent
ROOT=PROJECT.parents[1]
OUT=ROOT/'output/other-maps-half-letter'
sys.path.insert(0,str(HERE))
import build_trail_maps_pdf as M
import build_aud_half_letter_proof as A

W,H=A.W,A.H
OLD,TARGET,TRIM,OUTER=A.OLD,A.TARGET,A.TRIM,A.OUTER
xy,rect,text=A.xy,A.rect,A.text
SX,SY=A.SX,A.SY
INK='#283B34'
REPORT={}


def geometry(key):
    cfg=M.TRAILS[key]
    stops=deepcopy(M.load_plan()['visits'][key])
    for s in stops:
        dl,do=M.plot_nudge(s['name']);s['lat']+=dl;s['lng']+=do
    lats=[s['lat'] for s in stops]
    crs=CRS.from_proj4('+proj=lcc +lat_1=%s +lat_2=%s +lat_0=%s +lon_0=%s +datum=WGS84 +units=m +no_defs'%(*cfg['parallels'],(min(lats)+max(lats))/2,cfg['lon0']))
    trans=Transformer.from_crs(CRS.from_epsg(4326),crs,always_xy=True).transform
    lo0,lo1,la0,la1=cfg['frame'];xs=[];ys=[]
    for i in range(31):
        t=i/30
        for lon,lat in ((lo0+t*(lo1-lo0),la0),(lo0+t*(lo1-lo0),la1),(lo0,la0+t*(la1-la0)),(lo1,la0+t*(la1-la0))):
            x,y=trans(lon,lat);xs.append(x);ys.append(y)
    bx0,bx1,by0,by1=min(xs),max(xs),min(ys),max(ys)
    scale=min((M.MX1-M.MX0)/(bx1-bx0),(M.MY1-M.MY0)/(by1-by0))
    def pt(lon,lat):
        x,y=trans(lon,lat)
        return (M.MX0+M.MX1)/2+(x-(bx0+bx1)/2)*scale,792-((M.MY0+M.MY1)/2+(y-(by0+by1)/2)*scale)
    towns={s['name'].split(' · ')[0]:(s['lat'],s['lng']) for s in stops}
    for name,lat,lon in cfg.get('decoy_towns',[]):towns.setdefault(name,(lat,lon))
    for name,lat,lon in M.load_corpus()+cfg['extra_towns']:
        if name in cfg.get('omit_towns',[]):continue
        if lo0<=lon<=lo1 and la0<=lat<=la1:
            dl,do=M.plot_nudge(name);towns.setdefault(name,(lat+dl,lon+do))
    for name,lat,lon in cfg.get('icon_towns',[]):towns.setdefault(name,(lat,lon))
    return {cfg.get('display_names',{}).get(n,n):pt(lon,lat) for n,(lat,lon) in towns.items()}


def font_setup():
    for name,rel in [('Plex','IBM_Plex_Mono/IBMPlexMono-Regular.ttf'),('PlexIt','IBM_Plex_Mono/IBMPlexMono-Italic.ttf'),('Cinzel','Cinzel/static/Cinzel-Regular.ttf'),('CinzelXB','Cinzel/static/Cinzel-ExtraBold.ttf')]:
        pdfmetrics.registerFont(TTFont(name,str(A.FONT/rel)))


def draw_compass(c,center):
    cx,cy=center;r=11.5
    c.setStrokeColor(HexColor('#59635D'));c.setLineWidth(.55);c.circle(cx,H-cy,r,fill=0,stroke=1)
    c.setFillColor(HexColor(INK));p=c.beginPath();p.moveTo(cx,H-cy+r-1);p.lineTo(cx-2.5,H-cy);p.lineTo(cx,H-cy-r+1);p.lineTo(cx+2.5,H-cy);p.close();c.drawPath(p,fill=1,stroke=0)
    c.setFillColor(HexColor('#FFFFFF'));p=c.beginPath();p.moveTo(cx,H-cy+r-1);p.lineTo(cx+2.5,H-cy);p.lineTo(cx,H-cy-r+1);p.close();c.drawPath(p,fill=1,stroke=0)
    text(c,cx,cy-r-4,'N','Cinzel',7,align='center')


def draw_frame(c,key):
    c.setStrokeColor(HexColor(INK));c.setLineWidth(.8);c.rect(18,H-612,378,594,fill=0,stroke=1)
    c.setLineWidth(.6);c.rect(TARGET.x0,H-TARGET.y1,TARGET.width,TARGET.height,fill=0,stroke=1)
    letters=M.TRAILS[key].get('col_letters',list('ABCDEFGHI'))
    for i,ch in enumerate(letters):
        x=TARGET.x0+(i+.5)*TARGET.width/9
        for y in (26,609):text(c,x,y,ch,'Plex',6.8,color='#FFFFFF',align='center')
    for i in range(11):
        y=TARGET.y0+(i+.5)*TARGET.height/11+2.4
        for x in (23.5,390.5):text(c,x,y,str(i+1),'Plex',6.8,color='#FFFFFF',align='center')


def place_image(c,im,png,alpha=1):
    a,b,cc,d,e,f=im['transform'];cx,cy=xy(e+(a+cc)/2,f+(b+d)/2)
    # Original pictogram shape and orientation; corresponding grid position.
    u=SX*1.12;aa,bb,ccc,dd=(v*u for v in (a,b,cc,d));ee=cx-(aa+ccc)/2;ff=cy-(bb+dd)/2
    c.saveState();c.setFillAlpha(alpha);c.transform(aa,-bb,-ccc,dd,ee+ccc,H-ff-dd)
    c.drawImage(ImageReader(io.BytesIO(png)),0,0,1,1,mask='auto');c.restoreState()
    return fitz.Rect(cx-im['bbox_width']*u/2,cy-im['bbox_height']*u/2,cx+im['bbox_width']*u/2,cy+im['bbox_height']*u/2)


def layout_label(name,s,dot,obstacles):
    size=7.2;lines=[name]
    if name=='Happy Valley-Goose Bay':lines=['Happy Valley-','Goose Bay']
    w=max(pdfmetrics.stringWidth(t,'Plex',size) for t in lines);h=7.6+(len(lines)-1)*9
    sx,sy=dot;box=fitz.Rect(s['bbox']);ox,oy=xy(*s['origin'])
    # Prefer the current relationship to the town dot, then try nearby positions.
    oldx,oldy=s['_dot']
    if box.x1<oldx:preferred='left'
    elif box.x0>oldx:preferred='right'
    elif s['origin'][1]<oldy:preferred='above'
    else:preferred='below'
    choices=[]
    for radius in (0,7,14,21,28):
        for side in [preferred]+[t for t in ('right','left','above','below') if t!=preferred]:
            if side=='right':x,y=sx+3.8+radius,sy-4
            elif side=='left':x,y=sx-3.8-radius-w,sy-4
            elif side=='above':x,y=sx-w/2,sy-4-radius-h
            else:x,y=sx-w/2,sy+4+radius
            for shift in (0,-8,8) if side in ('left','right') else (0,):
                r=fitz.Rect(x,y+shift,x+w,y+shift+h)
                if not fitz.Rect(31,31,383,599).contains(r):continue
                hits=[fitz.Rect(r).intersect(o).get_area() for o in obstacles if r.intersects(o)]
                penalty=sum(hits)*100+radius+(0 if side==preferred else 2)+abs(shift)*.2
                choices.append((penalty,r,lines))
    assert choices,name
    score,r,lines=min(choices,key=lambda z:z[0])
    return r,lines,score


def map_proof(key,n):
    source=PROJECT/f'Print/_pdf_source/Trail_Map_{n}_{key.capitalize()}_Print.pdf'
    source_hash=hashlib.sha256(source.read_bytes()).hexdigest()
    doc=fitz.open(source);p=doc[0]
    spans=[dict(s,dir=l['dir']) for b in p.get_text('dict')['blocks'] if 'lines' in b for l in b['lines'] for s in l['spans']]
    images=p.get_image_info(xrefs=True);mapimages=[i for i in images if OLD.contains(fitz.Rect(i['bbox']))]
    compass_bg=p.get_pixmap(matrix=fitz.Matrix(1,1),alpha=False).pixel(563,663)
    for i in mapimages:
        b=fitz.Rect(i['bbox']);i['bbox_width']=b.width;i['bbox_height']=b.height
    pngs={}
    for im in images:
        raw=A.rgba(doc,im['xref']);r=fitz.Rect(im['bbox'])
        raster=Image.open(io.BytesIO(raw))
        # Lossless PNG at up to 600 dpi at final placement; retain alpha.
        raster.thumbnail((max(1,round(r.width*SX*1.12*600/72)),max(1,round(r.height*SX*1.12*600/72))),Image.Resampling.LANCZOS)
        stream=io.BytesIO();raster.save(stream,format='PNG');pngs[im['xref']]=stream.getvalue()
    identifier=max((i for i in images if i['bbox'][1]>695),key=lambda z:z['bbox'][0])
    towncoords=geometry(key)
    towns=[];other=[];seen=set()
    for s in spans:
        if not s['text'].strip():continue
        if not OLD.contains(fitz.Rect(s['bbox'])):continue
        if s['text']=='N' and s['bbox'][1]>600:continue
        if s['font']=='IBMPlexMono-Regular' and abs(s['size']-7.4)<.02:
            if s['text'] in seen:continue
            seen.add(s['text']);assert s['text'] in towncoords,(key,s['text'])
            s['_dot']=towncoords[s['text']];towns.append(s)
        else:other.append(s)
    for xref in {i['xref'] for i in images}:p.delete_image(xref)
    p.add_redact_annot(p.rect,fill=False);p.apply_redactions(images=0,graphics=0)
    outdoc=fitz.open();o=outdoc.new_page(width=W,height=H)
    o.draw_rect(o.rect,color=None,fill=fitz.sRGB_to_pdf(int(M.TRAILS[key]['band'][1:],16)))
    o.show_pdf_page(TARGET,doc,0,clip=OLD,keep_proportion=False)
    compass=xy(546.724409,644.604094)
    o.draw_rect(rect(fitz.Rect(528.724409,626.604094,564.724409,662.604094)),color=None,fill=tuple(v/255 for v in compass_bg))
    buf=io.BytesIO();c=canvas.Canvas(buf,pagesize=(W,H));obstacles=[];art_cells=[]
    for i,im in enumerate(mapimages):
        alpha=.96 if key=='rollo' else .82 if key=='leif' and 3<=i<=9 else .62 if key=='leif' else 1
        b=place_image(c,im,pngs[im['xref']],alpha)
        obstacles.append(b+(-.7,-.7,.7,.7))
        cx=(im['bbox'][0]+im['bbox'][2])/2;cy=(im['bbox'][1]+im['bbox'][3])/2
        nx,ny=xy(cx,cy)
        oldcell=(int((cx-OLD.x0)/OLD.width*9),int((cy-OLD.y0)/OLD.height*11))
        newcell=(int((nx-TARGET.x0)/TARGET.width*9),int((ny-TARGET.y0)/TARGET.height*11))
        assert oldcell==newcell
        art_cells.append(oldcell)
    # Small matching identifier panel, in clear upper-right space on all three.
    badge=fitz.Rect(346,34,379,66)
    c.setFillColor(HexColor('#F4EEDD'));c.setStrokeColor(HexColor('#A99A7B'));c.setLineWidth(.4)
    c.rect(badge.x0,H-badge.y1,badge.width,badge.height,fill=1,stroke=1)
    c.drawImage(ImageReader(io.BytesIO(pngs[identifier['xref']])),badge.x0+3,H-badge.y1+3,badge.width-6,badge.height-6,preserveAspectRatio=True,anchor='c',mask='auto')
    obstacles.append(badge+(-2,-2,2,2))
    if key=='harald':
        for stem in M.HARALD_RUNES_REAL+M.HARALD_RUNES_DECOY:
            x,y=M.cell_center(*stem[:2]);x,y=xy(x,792-y)
            obstacles.append(fitz.Rect(x-7,y-11,x+7,y+11))
    # Larger region captions; subdued water names remain 6.5 pt minimum.
    for s in other:
        x,y=xy(*s['origin']);txt=s['text']
        caption=txt.replace(' ','')
        shift=(-10,7) if key=='leif' and caption in ('MARKLAND','Labrador') else (5,0) if key=='leif' and caption in ('GRŒNLAND','Greenland') else (0,0)
        x+=shift[0];y+=shift[1]
        if s['font']=='Cinzel-ExtraBold':
            x,y=xy((s['bbox'][0]+s['bbox'][2])/2,s['origin'][1]);size=10
            x+=shift[0];y+=shift[1]
            text(c,x,y,txt,'CinzelXB',size,align='center')
            ww=pdfmetrics.stringWidth(txt,'CinzelXB',size);obstacles.append(fitz.Rect(x-ww/2,y-9,x+ww/2,y+2))
        elif s['font']=='IBMPlexMono-Italic':
            size=7;ww=pdfmetrics.stringWidth(txt,'PlexIt',size)
            text(c,x,y,txt,'PlexIt',size,color='#91876E')
            obstacles.append(fitz.Rect(x,y-7,x+ww,y+2))
        elif s['font']=='Cinzel-Regular':
            dx,dy=s['dir'];angle=-math.degrees(math.atan2(SY*dy,SX*dx))
            c.saveState();c.translate(x,H-y);c.rotate(angle);c.setFont('Cinzel',6.5);c.setFillColor(HexColor('#477879'));c.drawString(0,0,txt);c.restoreState()
    dots=[xy(*s['_dot']) for s in towns]
    for x,y in dots:obstacles.append(fitz.Rect(x-2,y-2,x+2,y+2))
    layouts=[]
    for s,dot in zip(towns,dots):
        # Own town dot can touch the label clearance; other dots remain reserved.
        own=fitz.Rect(dot[0]-2,dot[1]-2,dot[0]+2,dot[1]+2)
        obs=[b for b in obstacles if b!=own]
        box,lines,score=layout_label(s['text'],s,dot,obs)
        obstacles.append(box+(-1,-1,1,1));layouts.append((s,box,lines,score,dot))
    for s,box,lines,score,(dx,dy) in layouts:
        qx=min(max(dx,box.x0),box.x1);qy=min(max(dy,box.y0),box.y1)
        if math.hypot(qx-dx,qy-dy)>7:
            c.setStrokeColor(HexColor('#6D786F'));c.setLineWidth(.3);c.line(dx,H-dy,qx,H-qy)
        for j,line in enumerate(lines):text(c,box.x0,box.y0+6.6+j*9,line,'Plex',7.2,halo=True)
    draw_compass(c,compass)
    draw_frame(c,key);c.save()
    overlay=fitz.open(stream=buf.getvalue(),filetype='pdf');o.show_pdf_page(o.rect,overlay,0)
    o.set_trimbox(TRIM);o.set_bleedbox(fitz.Rect(0,0,W,H))
    if key=='harald':
        # The existing board and note fit at 100%; keep physical board/ticket scale.
        original=fitz.open(source);bp=outdoc.new_page(width=W,height=H)
        bp.show_pdf_page(OUTER,original,1,clip=fitz.Rect(117,99,495,693),keep_proportion=True)
        bp.set_trimbox(TRIM);bp.set_bleedbox(fitz.Rect(0,0,W,H))
        oldtext=original[1].get_text().split();newtext=bp.get_text().split();assert oldtext==newtext
    outdoc.set_metadata({'title':f'{key.capitalize()} half Letter map proof','subject':'Design proof; 0.125 inch bleed; current Letter masters unchanged'})
    path=OUT/f'{key.capitalize()}_Map_5.5x8.5_PrintShop_Proof.pdf';outdoc.save(path,garbage=4,deflate=True)
    trimmed=fitz.open();home=fitz.open()
    for i in range(len(outdoc)):
        tp=trimmed.new_page(width=396,height=612);tp.show_pdf_page(tp.rect,outdoc,i,clip=TRIM)
        tp.get_pixmap(matrix=fitz.Matrix(3,3)).save(OUT/(f'{key.capitalize()}_Map_5.5x8.5'+('_Back' if i else '')+'_Preview.png'))
    for i in range(len(trimmed)):
        hp=home.new_page(width=612,height=792);hp.show_pdf_page(fitz.Rect(108,90,504,702),trimmed,i)
        hp.insert_text((108,38),f'{key.upper()} MAP '+('REVERSE' if i else 'FRONT')+' DESIGN PROOF',fontsize=11)
        hp.insert_text((108,56),'Print at 100% / Actual size. Trim is 5.5 x 8.5 inches.',fontsize=8)
        hp.draw_rect(fitz.Rect(108,90,504,702),color=(.65,.65,.65),width=.3)
        hp.draw_line((108,735),(180,735),color=(0,0,0),width=.8);hp.insert_text((108,749),'1 inch check',fontsize=8)
    trimmed.save(OUT/f'{key.capitalize()}_Map_5.5x8.5_Trim_Proof.pdf',garbage=4,deflate=True)
    home.save(OUT/f'{key.capitalize()}_Map_5.5x8.5_Letter_Test.pdf',garbage=4,deflate=True)
    assert source_hash==hashlib.sha256(source.read_bytes()).hexdigest()
    # Typography / safe area and native grid are checked from the final PDF.
    o=outdoc[0]
    data=o.get_text('dict');ss=[s for b in data['blocks'] if 'lines' in b for l in b['lines'] for s in l['spans']]
    bad=[s['text'] for s in ss if not OUTER.contains(fitz.Rect(s['bbox']))]
    issues=[(s['text'],round(score,1)) for s,b,l,score,d in layouts if score>=100]
    REPORT[key]={'source_sha256':source_hash,'source_unchanged':True,'town_count':len(towns),'town_names':[s['text'] for s in towns],'map_art_count':len(mapimages),'art_grid_cells':art_cells,'source_minimum_text_pt':min(s['size'] for s in spans),'new_minimum_text_pt':min(s['size'] for s in ss),'town_pt':7.2,'grid_pt':6.8,'text_outside_safe_box':bad,'crowding_flags':issues,'shop_pages':len(outdoc),'status':'review proof; physical print untested'}
    if key=='harald':REPORT[key]['reverse_scale']=1.0
    if key=='rollo':
        pa,pb=[towncoords[t] for t in ('Châlus','Saint-Clair-sur-Epte')]
        qa,qb=xy(*pa),xy(*pb)
        REPORT[key]['ruler']={'old_distance_mm':math.dist(pa,pb)*25.4/72,'new_distance_mm':math.dist(qa,qb)*25.4/72,'answer':120,'target_points':[qa,qb]}
    print(key,REPORT[key]['town_count'],'towns; outside safe:',bad,'crowding:',issues)
    return outdoc


def ruler_proof():
    sys.path.insert(0,str(PROJECT/'Props/LivRuler'))
    import build_ruler_pdf as R
    oldhash=hashlib.sha256((PROJECT/'Print/_pdf_source/Liv_Ruler_Print.pdf').read_bytes()).hexdigest()
    dist=REPORT['rollo']['ruler']['new_distance_mm']
    R.DIST_MM=dist;R.LONG_MM_PER_10=dist/12;R.SPEAR_MM_PER_10=dist/7.5
    R.OUT=OUT/'Ruler_For_HalfLetter_Maps_Letter_Test.pdf'
    R.OUT_SHOP=OUT/'Ruler_For_HalfLetter_Maps_PrintShop_Proof.pdf'
    R.PREVIEW=OUT/'Ruler_For_HalfLetter_Maps_Preview.png'
    R.build()
    d=fitz.open(R.OUT_SHOP);d[0].set_trimbox(fitz.Rect(9,9,441,153));d[0].set_bleedbox(d[0].rect)
    raw=d.tobytes(garbage=4,deflate=True);d.close();R.OUT_SHOP.write_bytes(raw)
    assert oldhash==hashlib.sha256((PROJECT/'Print/_pdf_source/Liv_Ruler_Print.pdf').read_bytes()).hexdigest()
    assert abs(R.LONG_MM_PER_10*12-dist)<1e-9
    REPORT['rollo']['ruler'].update({'old_ruler_unchanged':True,'longship_zero_to_120_mm':dist,'spear_same_distance':75})


def packages():
    readme=OUT/'README.md'
    readme.write_text('''# Matching half-Letter map proofs

Design proofs only. Current Letter maps, answer copies and prototype ruler are unchanged.

- All map trims: 5.5 × 8.5 inches. Print-shop Media/BleedBox: 5.75 × 8.75 inches, with 0.125 inch bleed on all sides. Important text stays another 0.125 inch inside trim.
- Leif, Rollo and Harald match the Aud direction: bottom title removed, identifier moved to a small upper-right panel, taller schematic frame, pictograms kept in proportion, town names 7.2 pt, grid 6.8 pt. All 18 / 29 / 14 town names retained respectively. No new puzzle geography.
- Leif animal artwork centers keep the same grid squares. Harald uses A,C,E,I,K,N,R,T,V as before; all 12 branch-rune stems keep their original cells and labels clear them.
- Harald's print-shop and trimmed PDFs have two pages. The reverse preserves the original board, note, font sizes and ticket-matching scale at 100%.
- Rollo requires the included half-Letter ruler. The new map's Châlus–Saint-Clair-sur-Epte distance is about 71.329 mm; that matches 0 to 120 on LONGSHIP. SPEAR still reads 75. This ruler is for these proofs, not the Letter prototype.

## Files to use

- `All_Maps_5.5x8.5_Print_Test_Pack.pdf`: six Letter pages — Leif, Rollo, Aud, Harald front, Harald reverse, matched ruler. Print single-sided at 100% / Actual size for review. Check the one-inch bars on maps and 50 mm bar on ruler. Do not use Fit.
- `Harald_Map_5.5x8.5_Letter_Test.pdf`: the separate centered two-page file can be tested duplex, flip on long edge.
- `Maps_And_Matching_Ruler_PrintShop_Proofs.zip`: all four maps (Harald includes reverse), matched 2 × 6 inch ruler and this README. Clean PDFs with bleed, no template guides.
- Individual `*_Trim_Proof.pdf` / `*_Preview.png` files show the trimmed artwork.

PDF dimensions, safe area, labels, source hashes and pictogram grid cells checked. Independent PDF measurements confirm the ruler matches Rollo; Harald reverse fonts/text/placement are unchanged apart from translation. Full pages and enlarged details visually inspected. Physical print quality, readability and player tests remain outstanding.

Builder: `C:/EscapeBackpack/EscapeBackpack/NorseBackpack/TravelMap/build_other_half_letter_proofs.py`. `validation.json` and `verification.json` record the checks.
''',encoding='utf-8')
    combined=fitz.open()
    # Four fronts in journey order, then Harald reverse and the matched ruler.
    for path,indices in [(OUT/'Leif_Map_5.5x8.5_Letter_Test.pdf',[0]),(OUT/'Rollo_Map_5.5x8.5_Letter_Test.pdf',[0]),(ROOT/'output/aud-half-letter/Aud_Map_5.5x8.5_Letter_Test.pdf',[0]),(OUT/'Harald_Map_5.5x8.5_Letter_Test.pdf',[0,1]),(OUT/'Ruler_For_HalfLetter_Maps_Letter_Test.pdf',[0])]:
        d=fitz.open(path)
        for i in indices:combined.insert_pdf(d,from_page=i,to_page=i)
    combined.save(OUT/'All_Maps_5.5x8.5_Print_Test_Pack.pdf',garbage=4,deflate=True)
    c=canvas.Canvas(str(OUT/'Other_Maps_5.5x8.5_Overview.pdf'),pagesize=(792,612))
    c.setFillColor(HexColor(INK));c.setFont('Helvetica-Bold',14);c.drawString(24,580,'HALF-LETTER MAP DESIGN PROOFS')
    c.setFont('Helvetica',9);c.drawString(24,562,'5.5 x 8.5 inch trim | 0.125 inch bleed | names 7.2 pt | prototype Letter masters unchanged')
    for i,key in enumerate(('Leif','Rollo','Harald')):
        x=24+i*254;c.setFont('Helvetica-Bold',11);c.drawString(x,536,key)
        c.drawImage(str(OUT/f'{key}_Map_5.5x8.5_Preview.png'),x,150,236,236*612/396)
    c.setFont('Helvetica',9);c.drawString(24,112,'Use the print-test pack at 100% / Actual size to check labels and puzzle details.')
    c.drawString(24,96,'Rollo requires the included resized ruler. Harald reverse keeps its original board and note scale.')
    c.save();d=fitz.open(OUT/'Other_Maps_5.5x8.5_Overview.pdf');d[0].get_pixmap(matrix=fitz.Matrix(2,2)).save(OUT/'Other_Maps_5.5x8.5_Overview.png')
    files=[OUT/f'{name}_Map_5.5x8.5_PrintShop_Proof.pdf' for name in ('Leif','Rollo','Harald')]+[ROOT/'output/aud-half-letter/Aud_Map_5.5x8.5_PrintShop_Proof.pdf',OUT/'Ruler_For_HalfLetter_Maps_PrintShop_Proof.pdf']
    with zipfile.ZipFile(OUT/'Maps_And_Matching_Ruler_PrintShop_Proofs.zip','w',zipfile.ZIP_DEFLATED) as z:
        for p in files:z.write(p,p.name)
        z.write(readme,readme.name)


if __name__=='__main__':
    OUT.mkdir(parents=True,exist_ok=True);font_setup()
    only=sys.argv[1] if len(sys.argv)>1 else None
    if only and (OUT/'partial_validation.json').exists():
        REPORT.update(json.loads((OUT/'partial_validation.json').read_text(encoding='utf-8')))
    for key,n in [('leif',1),('rollo',2),('harald',4)]:
        if only and key!=only:continue
        map_proof(key,n)
        (OUT/'partial_validation.json').write_text(json.dumps(REPORT,indent=2,ensure_ascii=False),encoding='utf-8')
    ruler_proof();packages()
    (OUT/'validation.json').write_text(json.dumps(REPORT,indent=2,ensure_ascii=False),encoding='utf-8')
