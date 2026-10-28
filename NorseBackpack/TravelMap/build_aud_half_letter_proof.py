"""Non-adopted Aud half-Letter professional-print concept, 20 Oct 2026.

Keeps the live Letter map untouched. Reflows its schematic geography to a taller
frame, preserves pictogram proportions, and resets labels at physical print size.
No new illustration or puzzle geometry is invented. Run with project Python
(PyMuPDF/reportlab required). Outputs live only under output/aud-half-letter.
"""
from pathlib import Path
from collections import Counter
import hashlib
import io
import json
import math
import re
import sys

import pymupdf as fitz
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, Color
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
ROOT = PROJECT.parents[1]
OUT = ROOT / 'output/aud-half-letter'
SOURCE = PROJECT / 'Print/_pdf_source/Trail_Map_3_Aud_Print.pdf'
TEMPLATE = Path('C:/Users/simon/Downloads/flyers_portrait_5-5x8-5_single_pdf.pdf')
FONT = PROJECT.parent / 'Fonts'
W,H = 414,630
TRIM = fitz.Rect(9,9,405,621)
OUTER = fitz.Rect(18,18,396,612)
TARGET = fitz.Rect(29,29,385,601)
OLD = fitz.Rect(31.559055,21.92126,580.72441,686.60315)
OLD_LEGEND = fitz.Rect(36,432,235,680)
LEGEND = fitz.Rect(32,378,162,596)
PURPLE = '#6D528B'
SEA = '#DCE7E4'
INK = '#283B34'
SX,SY = TARGET.width/OLD.width,TARGET.height/OLD.height


def xy(x,y):
    return TARGET.x0+(x-OLD.x0)*SX, TARGET.y0+(y-OLD.y0)*SY


def rect(r):
    return fitz.Rect(*xy(r.x0,r.y0),*xy(r.x1,r.y1))


def rgba(doc,xref):
    pix=fitz.Pixmap(doc,xref)
    entry=next(x for x in doc[0].get_images(full=True) if x[0]==xref)
    if entry[1]:
        pix=fitz.Pixmap(pix,fitz.Pixmap(doc,entry[1]))
    return pix.tobytes('png')


def text(c,x,y,txt,font,size,color=INK,halo=False,align='left'):
    c.saveState()
    width=pdfmetrics.stringWidth(txt,font,size)
    x-=width/2 if align=='center' else width if align=='right' else 0
    c.setFillColor(HexColor(color))
    if halo:
        c.setStrokeColor(HexColor('#FFFFFF'));c.setLineWidth(1.5)
        t=c.beginText(x,H-y);t.setFont(font,size);t.setTextRenderMode(1);t.textOut(txt)
        t.setTextOrigin(x,H-y);t.setTextRenderMode(0);t.textOut(txt);c.drawText(t)
    else:
        c.setFont(font,size);c.drawString(x,H-y,txt)
    c.restoreState()


def build():
    OUT.mkdir(parents=True,exist_ok=True)
    before=hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    tpl=fitz.open(TEMPLATE)
    assert tpl[0].rect==fitz.Rect(0,0,W,H) and tpl[0].trimbox==TRIM
    for name,rel in [('Plex','IBM_Plex_Mono/IBMPlexMono-Regular.ttf'),('PlexIt','IBM_Plex_Mono/IBMPlexMono-Italic.ttf'),('Cinzel','Cinzel/static/Cinzel-Regular.ttf'),('CinzelXB','Cinzel/static/Cinzel-ExtraBold.ttf')]:
        pdfmetrics.registerFont(TTFont(name,str(FONT/rel)))
    doc=fitz.open(SOURCE);page=doc[0]
    spans=[s for b in page.get_text('dict')['blocks'] if 'lines' in b for l in b['lines'] for s in l['spans']]
    base_js=(HERE/'aud_base.js').read_text(encoding='utf-8')
    geo=json.loads(base_js.split('=',1)[1].strip().rstrip(';'))
    town_positions={t['name']:xy(t['x'],792-t['y']) for t in geo['towns']}
    images=page.get_image_info(xrefs=True)
    chosen=[i for i in images if fitz.Rect(i['bbox']).intersects(OLD) and not OLD_LEGEND.contains(fitz.Rect(i['bbox']))]
    pic={i['xref']:rgba(doc,i['xref']) for i in chosen}
    # Legend samples are crops of the approved legend, never newly drawn substitutes.
    labels=[s for s in spans if abs(s['size']-6.5)<.01 and OLD_LEGEND.contains(fitz.Rect(s['bbox']))]
    samples=[]
    for s in labels:
        left=39 if s['origin'][0]<110 else 133.5
        cy=s['origin'][1]-2.2
        clip=fitz.Rect(left,cy-8,left+29,cy+8)
        samples.append((s['text'],page.get_pixmap(matrix=fitz.Matrix(5,5),clip=clip,alpha=False).tobytes('png')))
    assert len(samples)==25

    # Remove source lettering and bitmaps in a temporary in-memory copy only.
    for xref in set(i['xref'] for i in images):page.delete_image(xref)
    page.add_redact_annot(page.rect,fill=False)
    page.apply_redactions(images=0,graphics=0)
    base=fitz.open();out=base.new_page(width=W,height=H)
    out.draw_rect(out.rect,color=None,fill=fitz.sRGB_to_pdf(int(PURPLE[1:],16)))
    out.show_pdf_page(TARGET,doc,0,clip=OLD,keep_proportion=False)
    # Remove the old legend field; its former footprint remains the same sea area.
    out.draw_rect(rect(OLD_LEGEND)+(-.3,-.3,.3,.3),color=None,fill=fitz.sRGB_to_pdf(int(SEA[1:],16)))
    compass=xy(546.724409,644.604094)
    out.draw_rect(rect(fitz.Rect(528.724409,626.604094,564.724409,662.604094)),color=None,fill=fitz.sRGB_to_pdf(0xEFE3C4))

    buf=io.BytesIO();c=canvas.Canvas(buf,pagesize=(W,H))
    c.saveState();clip=c.beginPath();clip.rect(TARGET.x0,H-TARGET.y1,TARGET.width,TARGET.height);c.clipPath(clip,stroke=0,fill=0)
    # Reinsert every original map pictogram at the reflowed position, without
    # squashing its aspect ratio. Rotate crossings to the new local road angle.
    for im in chosen:
        a,b,cc,d,e,f=im['transform'];cx,cy=xy(e+(a+cc)/2,f+(b+d)/2)
        theta=math.atan2(b,a);delta=math.atan2(SY*math.sin(theta),SX*math.cos(theta))-theta
        cs,sn=math.cos(delta),math.sin(delta);u=SX*1.12
        aa=u*(cs*a-sn*b);bb=u*(sn*a+cs*b);ccc=u*(cs*cc-sn*d);dd=u*(sn*cc+cs*d)
        ee=cx-(aa+ccc)/2;ff=cy-(bb+dd)/2
        c.saveState();c.transform(aa,-bb,-ccc,dd,ee+ccc,H-ff-dd)
        c.drawImage(ImageReader(io.BytesIO(pic[im['xref']])),0,0,1,1,mask='auto');c.restoreState()
    c.restoreState()

    # Reset all surviving map captions at their final physical size.
    seen=set();towns=[]
    for s in spans:
        box=fitz.Rect(s['bbox']);key=(s['text'],tuple(round(v,2) for v in s['origin']))
        if key in seen or not OLD.contains(box) or OLD_LEGEND.intersects(box) or s['text']=='N':continue
        seen.add(key)
        if len(s['text'])==1 and s['text'] in 'ABCDEFGHI123456789':continue
        x,y=xy(*s['origin'])
        if s['font']=='IBMPlexMono-Regular' and abs(s['size']-7.4)<.02:
            # Labels that were left of their dot retain their right anchor.
            align='right' if s['text'] in ('Dögurðarnes','Búðardalur') else 'left'
            if align=='right':x=xy(box.x1,s['origin'][1])[0]
            if s['text']=='Eiríksstaðir':
                x,y=town_positions[s['text']];y+=11;align='center'
            text(c,x,y,s['text'],'Plex',7.2,halo=True,align=align);towns.append(s['text'])
        elif s['text'].startswith('F A X A'):
            # Sea name stays between the legend and the Borgarnes/Akranes shore.
            c.saveState();c.translate(171,H-560);c.rotate(90);c.setFillColor(HexColor('#477879'));c.setFont('Cinzel',7);c.drawString(0,0,s['text']);c.restoreState()
        elif s['font']=='Cinzel-ExtraBold':text(c,x,y,s['text'],'CinzelXB',10)
        elif s['text']=='Iceland':text(c,x,y,s['text'],'PlexIt',7)
        else:text(c,x,y,s['text'],'PlexIt',7.2,color='#807D65')

    # Two columns of readable 6.5 pt type; the matching comb now identifies the map.
    c.setFillColor(HexColor('#F4EEDD'));c.setStrokeColor(HexColor('#A99A7B'));c.setLineWidth(.55)
    c.rect(LEGEND.x0,H-LEGEND.y1,LEGEND.width,LEGEND.height,fill=1,stroke=1)
    text(c,38,392,'LEGEND','Helvetica-Bold',8)
    c.drawImage(str(HERE/'Drafts/Aud_Comb_Titleband_v1.png'),119,H-399,35,20,preserveAspectRatio=True,anchor='c',mask='auto')
    c.setStrokeColor(HexColor('#A99A7B'));c.setLineWidth(.4);c.line(36,H-402,158,H-402)
    for i,(name,png) in enumerate(samples):
        col,row=divmod(i,13);x=36+64*col;cy=412+14*row
        c.drawImage(ImageReader(io.BytesIO(png)),x,H-cy-5.5,16,11,mask='auto')
        text(c,x+16.5,cy+2.3,name,'Helvetica',6.5)

    # Rebuilt grid edge and references at 6.8 pt, inside the template safe area.
    c.setStrokeColor(HexColor(INK));c.setLineWidth(.8)
    c.rect(OUTER.x0,H-OUTER.y1,OUTER.width,OUTER.height,fill=0,stroke=1)
    c.setLineWidth(.6);c.rect(TARGET.x0,H-TARGET.y1,TARGET.width,TARGET.height,fill=0,stroke=1)
    for i,ch in enumerate('ABCDEFGHI'):
        x=TARGET.x0+(i+.5)*TARGET.width/9
        for y in (26,609):text(c,x,y,ch,'Plex',6.8,color='#FFFFFF',align='center')
    for i in range(11):
        y=TARGET.y0+(i+.5)*TARGET.height/11+2.4
        for x in (23.5,390.5):text(c,x,y,str(i+1),'Plex',6.8,color='#FFFFFF',align='center')
    # Keep the compass circular after the schematic geography is reflowed.
    cx,cy=compass;rr=11.5
    c.setStrokeColor(HexColor('#59635D'));c.setLineWidth(.55);c.circle(cx,H-cy,rr,fill=0,stroke=1)
    c.setFillColor(HexColor(INK));p=c.beginPath()
    p.moveTo(cx,H-cy+rr-1);p.lineTo(cx-2.5,H-cy);p.lineTo(cx,H-cy-rr+1);p.lineTo(cx+2.5,H-cy);p.close();c.drawPath(p,fill=1,stroke=0)
    c.setFillColor(HexColor('#FFFFFF'));p=c.beginPath()
    p.moveTo(cx,H-cy+rr-1);p.lineTo(cx+2.5,H-cy);p.lineTo(cx,H-cy-rr+1);p.close();c.drawPath(p,fill=1,stroke=0)
    text(c,cx,cy-rr-4,'N','Cinzel',7,align='center')
    c.save()
    overlay=fitz.open(stream=buf.getvalue(),filetype='pdf');out.show_pdf_page(out.rect,overlay,0)
    out.set_trimbox(TRIM);out.set_bleedbox(fitz.Rect(0,0,W,H))
    base.set_metadata({'title':'Aud half Letter print shop design proof','subject':'Draft only; 5.5 x 8.5 inch trim; 0.125 inch bleed. Geometry reflowed; physical legibility untested.'})
    shop=OUT/'Aud_Map_5.5x8.5_PrintShop_Proof.pdf';base.save(shop,garbage=4,deflate=True)
    trim=fitz.open();tp=trim.new_page(width=396,height=612);tp.show_pdf_page(tp.rect,base,0,clip=TRIM)
    trim.save(OUT/'Aud_Map_5.5x8.5_Trim_Proof.pdf',garbage=4,deflate=True)
    tp.get_pixmap(matrix=fitz.Matrix(3,3)).save(OUT/'Aud_Map_5.5x8.5_Preview.png')
    home=fitz.open();hp=home.new_page(width=612,height=792)
    frame=fitz.Rect(108,90,504,702);hp.show_pdf_page(frame,trim,0)
    hp.insert_text((108,38),'AUD MAP DESIGN PROOF',fontsize=11)
    hp.insert_text((108,55),'Print at 100% / Actual size. Card boundary: 5.5 x 8.5 inches.',fontsize=8)
    hp.insert_text((108,73),'Draft only. Check names, legend and crossings on paper.',fontsize=8)
    hp.draw_rect(frame,color=(.65,.65,.65),width=.3)
    hp.draw_line((108,735),(180,735),color=(0,0,0),width=.8)
    hp.insert_text((108,749),'1 inch check',fontsize=8)
    home.save(OUT/'Aud_Map_5.5x8.5_Letter_Test.pdf',garbage=4,deflate=True)
    # Magnified detail proof is solely for visual QA, never a claim of print legibility.
    for name,clip in [('Legend',fitz.Rect(20,360,160,594)),('North',fitz.Rect(65,35,305,180)),('Crossings',fitz.Rect(260,170,378,330))]:
        tp.get_pixmap(matrix=fitz.Matrix(4,4),clip=clip).save(OUT/f'Detail_{name}.png')
    template_text=out.get_text()
    sizes=[s['size'] for b in out.get_text('dict')['blocks'] if 'lines' in b for l in b['lines'] for s in l['spans']]
    assert len(towns)==11,(len(towns),towns)
    assert all(name in template_text for name,_ in samples)
    assert before==hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    features=json.loads((HERE/'aud_features.json').read_text(encoding='utf-8'))
    counts=Counter(f['kind'] for f in features['features'])
    assert (counts['bridge'],counts['ford'],counts['gate'])==(12,5,7)
    report={'source_sha256':before,'source_unchanged':True,'trim_inches':[5.5,8.5],'media_inches':[5.75,8.75],'bleed_inches':.125,'safe_inset_inches':.125,'town_names':towns,'town_font_pt':7.2,'legend_font_pt':6.5,'grid_font_pt':6.8,'smallest_pdf_text_pt':round(min(sizes),2),'map_art_placements':len(chosen),'legend_entries':len(samples),'source_features':len(features['features']),'source_counting_features':{'bridges':counts['bridge'],'fords':counts['ford'],'gates':counts['gate']},'geography_scale_xy':[SX,SY],'pictograms':'original assets; aspect ratio retained; 12% larger than width-based shrink','status':'design proof only; live Letter map and geometry JSON untouched; physical legibility untested'}
    (OUT/'validation.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
    print(json.dumps(report,indent=2,ensure_ascii=False))


if __name__=='__main__':build()
