"""Shared fancy carrier layout for exact 3.5 by 2 inch prototype cards."""
from pathlib import Path
from PIL import Image
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor

HERE = Path(__file__).resolve().parent
FONT = HERE.parents[2] / 'Fonts/CrypticBureau/Cormorant-600.ttf'
pdfmetrics.registerFont(TTFont('TravelSerif', str(FONT)))
NAVY = HexColor('#142B36')


def logo(c, path, x, y, width, height):
    with Image.open(path) as im:
        assert im.mode == 'RGBA' and im.getpixel((0, 0))[3] == 0
        # Fit the opaque artwork; clip padding and faint transparent fringes at placement.
        box = im.getchannel('A').point(lambda v: 255 if v > 128 else 0).getbbox()
        assert box
        left, top, right, bottom = box
        iw, ih = im.size
    scale = min(width / (right-left), height / (bottom-top))
    ox = x + (width-(right-left)*scale)/2
    oy = y + (height-(bottom-top)*scale)/2
    c.saveState()
    clip = c.beginPath(); clip.rect(x, y, width, height)
    c.clipPath(clip, stroke=0, fill=0)
    c.drawImage(str(path), ox-left*scale, oy-(ih-bottom)*scale,
                iw*scale, ih*scale, mask='auto')
    c.restoreState()


def label(c, x, y, value, font='Sans', size=8, color=NAVY, max_width=None):
    if max_width is not None:
        assert pdfmetrics.stringWidth(value, font, size) <= max_width + .01, value
    c.setFillColor(color); c.setFont(font, size); c.drawString(x, y, value)


def border(c, width=252, height=144):
    c.setStrokeColor(HexColor('#999999'));c.setLineWidth(.2)
    c.lines([(0,0,width,0),(width,0,width,height),
             (width,height,0,height),(0,height,0,0)])
    c.setStrokeColor(NAVY)
    for inset, radius, weight in [(2.5, 5, .6), (4, 5, .3)]:
        c.setLineWidth(weight); p = c.beginPath()
        p.moveTo(inset+radius, inset); p.lineTo(width-inset-radius, inset)
        p.curveTo(width-inset-radius,inset+radius,width-inset-radius,inset+radius,width-inset,inset+radius)
        p.lineTo(width-inset,height-inset-radius)
        p.curveTo(width-inset-radius,height-inset-radius,width-inset-radius,height-inset-radius,width-inset-radius,height-inset)
        p.lineTo(inset+radius,height-inset)
        p.curveTo(inset+radius,height-inset-radius,inset+radius,height-inset-radius,inset,height-inset-radius)
        p.lineTo(inset,inset+radius)
        p.curveTo(inset+radius,inset+radius,inset+radius,inset+radius,inset+radius,inset)
        p.close(); c.drawPath(p)


def flourish(c, mode, accent):
    # A small ornament in the gap between route lines protects long place names.
    c.setStrokeColor(accent); c.setFillColor(accent); c.setLineWidth(.55)
    if mode == 'TRAIN':
        c.line(143,54,153,61); c.line(184,54,174,61)
        for t in [.1,.35,.6,.85]:
            c.line(143+10*t,54+7*t,184-10*t,54+7*t)
    elif mode == 'BUS':
        for offset in [0, 7]:
            p=c.beginPath();p.moveTo(144+offset,54)
            p.curveTo(186+offset,53,139+offset,62,177+offset,61);c.drawPath(p)
        c.setDash(1.5,1.5)
        p=c.beginPath();p.moveTo(147.5,54)
        p.curveTo(189.5,53,142.5,62,180.5,61);c.drawPath(p);c.setDash([])
    elif mode == 'FLIGHT':
        c.setDash(1.5,1.5)
        p=c.beginPath();p.moveTo(140,55);p.curveTo(154,64,173,64,186,55);c.drawPath(p)
        c.setDash([]);c.circle(140,55,.7,fill=1,stroke=0);c.circle(186,55,.7,fill=1,stroke=0)
        p=c.beginPath();p.moveTo(176,59);p.lineTo(172,63);p.lineTo(179,60);p.lineTo(175,57);p.close();c.drawPath(p,fill=1,stroke=0)
    else:
        for offset in [0, 3]:
            p=c.beginPath();p.moveTo(140,55+offset)
            p.curveTo(155,65+offset,169,48+offset,186,58+offset);c.drawPath(p)


def draw_ticket(c, rec, logo_path, brand, secondary, mode, accent, x=0, y=0):
    c.saveState(); c.translate(x,y); border(c)
    logo(c,logo_path,12,115,32,25)
    label(c,50,125,brand,'Semi',12.5,max_width=137)
    label(c,50,114,' '.join(secondary),'Sans',8,accent,max_width=137)
    logo(c,logo_path,204,116,35,23)
    c.setStrokeColor(accent);c.setLineWidth(.45)
    for xa,ya,xb,yb in [(12,110,187,110),(204,110,240,110),(12,28,187,28),
                         (204,68,240,68),(204,11,240,11)]:
        c.line(xa,ya,xb,yb)
    c.setStrokeColor(NAVY);c.setLineWidth(.4);c.setDash(2,2)
    c.line(196,1,196,143);c.setDash([])
    for field,key,ly,vy in [('FROM','origin',96,79),('TO','destination',57,39)]:
        label(c,13,ly,field)
        value=rec[key].upper()
        size=min(18,174/pdfmetrics.stringWidth(value,'TravelSerif',1))
        assert size >= 14, (value,size)
        label(c,13,vy,value,'TravelSerif',size,max_width=174)
    c.saveState();c.translate(0,8);flourish(c,mode,accent);c.restoreState()
    label(c,13,13,'PASSENGER')
    label(c,68,12,'LIV ERICSON','TravelSerif',11,max_width=119)
    label(c,204,94,mode)
    size=min(13,36/pdfmetrics.stringWidth(rec['service'],'TravelSerif',1))
    assert size>=10
    label(c,204,77,rec['service'],'TravelSerif',size,max_width=36)
    label(c,204,52,'DATE')
    label(c,204,36,rec['date'][:6],'TravelSerif',11.5,max_width=40)
    label(c,204,20,rec['date'][7:],'TravelSerif',11.5,max_width=36)
    c.restoreState()
