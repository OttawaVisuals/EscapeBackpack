"""Five readability proposals, kept separate from live Norse production files.

Builds a mixed-size review PDF and a 10-page Letter duplex proof pack. Imports
current puzzle data and uses current artwork; no live builder is run or rewritten.
"""
from pathlib import Path
import importlib.util
import math
import sys
from xml.sax.saxutils import escape

from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.pdfgen.canvas import FILL_EVEN_ODD
from reportlab.platypus import Paragraph

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "NorseBackpack/Print/_pdf_source/Readability_Redesign_Drafts"
sys.path.insert(0, str(ROOT / "NorseBackpack/Postcards"))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


museum = load("museum_live", "NorseBackpack/Props/MuseumTicket/build_museum_ticket_pdf.py")
aud = load("aud_live", "NorseBackpack/Props/AudTicket/build_aud_ticket_pdf.py")
notes = load("notes_live", "NorseBackpack/Props/LivNotes/build_liv_notes_pdf.py")
ld = load("ld_live", "NorseBackpack/Postcards/build_postcard_LD_pdf.py")
wheel = load("wheel_live", "NorseBackpack/Props/CypherWheel/build_cypher_wheel_pdf.py")
pdfmetrics.registerFont(TTFont("ClearTag", str(ROOT / "Fonts/IBM_Plex_Mono/IBMPlexMono-SemiBold.ttf")))

PAPER = HexColor("#F5EFDF")
INK = HexColor("#283B34")
RUST = HexColor("#985326")
TEAL = HexColor("#2F7775")
RULE = HexColor("#B2B5A5")
PALE = HexColor("#E9E6D9")
MM = wheel.MM
HAND = "NothingYouCouldDo"


def text(c, x, y, value, size=11, font="Helvetica", color=INK, align="left"):
    c.setFillColor(color)
    c.setFont(font, size)
    {"left": c.drawString, "center": c.drawCentredString, "right": c.drawRightString}[align](x, y, value)


def rule(c, x1, x2, y, color=RULE, width=.5):
    c.setStrokeColor(color)
    c.setLineWidth(width)
    c.line(x1, y, x2, y)


def base(c, w, h, border=False):
    c.setFillColor(PAPER)
    c.rect(0, 0, w, h, stroke=0, fill=1)
    if border:
        c.setStrokeColor(RULE)
        c.setLineWidth(.7)
        c.rect(12, 12, w-24, h-24, stroke=1, fill=0)


def para(c, value, x, top, width, size=11.5, leading=14.5, font="Helvetica", color=INK):
    p = Paragraph(value, ParagraphStyle("body", fontName=font, fontSize=size,
                                       leading=leading, textColor=color))
    _, h = p.wrap(width, 1000)
    p.drawOn(c, x, top-h)
    return top-h


def museum_front(c):
    w, h = 252, 432
    base(c, w, h)
    # Recomposition preserves the nine numbered sites while filling the ticket.
    # The generated source is exactly 3:4, so no crop or distortion is needed.
    art=ImageReader(str(Path(__file__).with_name("Brattahlid_Map_Wide_v1.png")))
    iw,ih=art.getSize()
    assert abs(iw/ih-.75)<.001
    c.drawImage(art,0,0,w,336)
    c.setFillColor(INK)
    c.rect(0,336,w,96,stroke=0,fill=1)
    text(c,w/2,402,"VIKING MUSEUM",18,"CinzelExtraBold",PAPER,"center")
    text(c,w/2,379,"OF BRATTAHLÍÐ",17,"CinzelBold",PAPER,"center")
    rule(c,24,w-24,368,RUST,1.5)
    text(c,w/2,351,"GENERAL ADMISSION",10,"Helvetica-Bold",PAPER,"center")


def museum_back(c):
    w, h = 252, 432
    base(c, w, h)
    text(c, 20, 409, "VIKING MUSEUM OF BRATTAHLÍÐ", 9, "Helvetica-Bold")
    rule(c, 20, w-20, 399, RUST, 2)
    text(c, 20, 376, "VISITOR INDEX", 19, "CinzelExtraBold")
    text(c, 46, 359, "GALLERY", 9, "Helvetica-Bold", RUST)
    text(c, w-21, 359, "ROOM", 9, "Helvetica-Bold", RUST, "right")
    rule(c, 20, w-20, 354)
    for i, (letter, name, number) in enumerate(museum.INDEX):
        y = 339 - i*12.5
        if i % 2:
            c.setFillColor(PALE)
            c.rect(17, y-2.7, w-34, 12.5, stroke=0, fill=1)
        text(c, 23, y, letter, 11, "ClearTag", RUST)
        text(c, 46, y, name, 11)
        text(c, w-23, y, str(number), 11.5, "ClearTag", align="right")
        assert 46 + pdfmetrics.stringWidth(name, "Helvetica", 11) < w-43


def aud_front(c):
    w, h = 252, 432
    base(c, w, h)
    text(c, w/2, 404, "AUÐAR SAFN", 22, "CinzelExtraBold", align="center")
    text(c, w/2, 385, "TREASURE MUSEUM / HVAMMUR, DALIR", 9, "Helvetica-Bold", RUST, "center")
    rule(c, 20, w-20, 373, RUST, 1.5)
    text(c, 20, 350, "THE COIN ROOM", 16, "CinzelBold")
    text(c, 20, 334, "What each coin is worth today", 10.5)
    y = 316
    for group, coins in aud.COIN_KEY:
        rule(c, 20, 110, y)
        rule(c, 142, w-20, y)
        if group == "fehu":
            c.setStrokeColor(INK)
            aud.draw_fehu(c, 126, y, 15, 1.5)
        else:
            c.drawImage(str(aud.ICONS / (group + ".png")), 118, y-8, 16, 16,
                        mask="auto", preserveAspectRatio=True, anchor="c")
        y -= 34
        for name, label, value, rare in coins:
            c.drawImage(aud.coin_icon(name, rare), 22, y-4, 27, 27, mask="auto")
            text(c, 58, y+5, label, 10.5)
            text(c, w-20, y+5, f"${value:,}", 11.5, "Helvetica-Bold", RUST, "right")
            assert 58+pdfmetrics.stringWidth(label,"Helvetica",10.5)+8 < w-20-pdfmetrics.stringWidth(f"${value:,}","Helvetica-Bold",11.5)
            y -= 31
        y += 16
    assert y > 10


def aud_back(c):
    w, h = 252, 432
    base(c, w, h)
    text(c, 20, 409, "AUÐAR SAFN", 9, "Helvetica-Bold")
    rule(c, 20, w-20, 398, RUST, 2)
    text(c, 20, 373, "TREASURE HUNT", 19, "CinzelExtraBold")
    text(c, 20, 353, "Trace the route on your map.", 11)
    top = 334
    for i, leg in enumerate(aud.LEGS):
        text(c, 21, top-12, str(i+1), 12, "ClearTag", RUST)
        bottom = para(c, escape(leg), 45, top, w-65, size=11.5, leading=14.5)
        rule(c, 45, w-20, bottom-10)
        top = bottom-22
    assert top >= 10, top


def notes_front(c):
    w,h=288,432
    base(c,w,h,True)
    text(c,w/2,402,"LIV'S NOTES",19,"CinzelExtraBold",TEAL,"center")
    intro_bottom=para(c,escape(notes.INTRO),18,393,252,10.5,11.5,HAND)
    assert intro_bottom>=358.5,intro_bottom
    text(c,18,350,"WHO'S WHO",9,"Helvetica-Bold",RUST)
    rule(c,18,270,346)
    def entry(name,meaning,y):
        s=f'<font name="Helvetica-Bold" color="#2F7775">{escape(name)}</font>  {escape(meaning)}'
        return para(c,s,18,y,252,10.5,11.5,HAND)-.5
    y=343
    for name, meaning in notes.WHO:
        y=entry(name,meaning,y)
    text(c,18,252,"WORDS",9,"Helvetica-Bold",RUST)
    assert y>259,y
    rule(c,18,270,248)
    y=245
    for name,meaning in notes.WORDS:y=entry(name,meaning,y)
    assert y>18,y


IMPRINT = "Vinland Editions  ·  Series A, No. 6"
CREDIT = 'Image adaptation: "Reproduction of Brattahlíð Viking church" - Claire Rowland, CC BY 2.0.'


def ld_front(c): ld.draw_front_card(c)


def ld_back(c):
    # Designer correction: this is deliberately a tiny discovered mark, not
    # routine instructions. Keep the live footer and its 6 pt imprint exactly.
    ld.draw_back_card(c)


def arm_holes(cx,cy):
    holes=[]
    for r in wheel.RADII:
        for offset, x0, x1 in [
            (wheel.SYM_R,cx-(r-1)*MM,cx-(r-wheel.SPLIT+.5)*MM),
            (wheel.RUNE_R,cx+(r-wheel.BAND+.5)*MM,cx+(r-wheel.SPLIT-.5)*MM)]:
            height=min(.8*2*math.pi*(r-offset)/len(wheel.SYMBOLS),11)*MM
            holes.append((x0,cy-height/2,x1-x0,height))
    return holes


def wheel_arm(c,cx,cy):
    half=(wheel.RADII[0]+3)*MM
    height=34*MM  # 18 mm live arm; all eight apertures and the pin are identical.
    holes=arm_holes(cx,cy)
    path=c.beginPath()
    path.roundRect(cx-half,cy-height/2,half*2,height,8*MM)
    for hole in holes:path.rect(*hole)
    c.setFillColor(wheel.HUB)
    c.drawPath(path,fill=1,stroke=0,fillMode=FILL_EVEN_ODD)
    c.setStrokeColor(INK);c.setLineWidth(.8)
    c.roundRect(cx-half,cy-height/2,half*2,height,8*MM,fill=0,stroke=1)
    c.setStrokeColor(wheel.RED);c.setLineWidth(.6);c.setDash(2,1.5)
    for hole in holes:c.rect(*hole,fill=0,stroke=1)
    c.setDash()
    left,right=cx-54*MM,cx+54*MM
    text(c,left,cy+28,"1  SET THE CODE",12,"Helvetica-Bold",align="center")
    text(c,right,cy+28,"2  READ THE RUNES",12,"Helvetica-Bold",align="center")
    text(c,left,cy-29,"Three digits? First window:",10.5,align="center")
    text(c,left,cy-41,"leave it blank, not zero.",10.5,align="center")
    text(c,right,cy-29,"3  Open the envelope",10.5,"Helvetica-Bold",align="center")
    text(c,right,cy-41,"with these runes.",10.5,align="center")
    wheel.pin(c,cx,cy)


def wheel_sheet(c):
    text(c,36,746,"RUNE CYPHER WHEEL",20,"CinzelBold")
    text(c,36,724,"Replacement instruction arm - readability draft",12)
    para(c,"Print at 100% / Actual size on cardstock. Cut around the outer edge, then cut out all eight red-dashed windows. Replace the existing top arm; keep the existing wheels and centre fastener.",36,690,540,12,17)
    wheel_arm(c,306,500)
    text(c,36,397,"Same centre and window positions. Wider arm: 34 mm.",11)
    rule(c,36,36+50*MM,360,INK,.8)
    for x in (36,36+50*MM):
        c.line(x,355,x,365)
    text(c,36,337,"This line must measure 50 mm after printing.",11)
    text(c,36,290,"Check that all four disks still turn freely after fitting the arm.",11)


BOUNDS = wheel.register_fonts()
MAPS = wheel.rune_maps()


def wheel_preview(code):
    def draw(c):
        for i in range(4):wheel.wheel(c,BOUNDS,MAPS,i,306,306,turn=wheel.SYMBOLS.index(code[i]))
        wheel_arm(c,306,306)
        text(c,24,17,"Assembly preview - code " + code.replace(" ","_") + " - not a player print sheet",9)
    return draw


PROPS=[
    ("Brattahlid museum ticket",(252,432),museum_front,museum_back),
    ("Aud museum ticket",(252,432),aud_front,aud_back),
    ("Liv's glossary",(288,432),notes_front,None),
    ("LD postcard",(432,288),ld_front,ld_back),
]


def crop_marks(c,x,y,w,h):
    c.setStrokeColor(INK);c.setLineWidth(.4)
    for px in (x,x+w):
        c.line(px,y-4,px,y-12);c.line(px,y+h+4,px,y+h+12)
    for py in (y,y+h):
        c.line(x-4,py,x-12,py);c.line(x+w+4,py,x+w+12,py)


def build():
    OUT.mkdir(parents=True,exist_ok=True)
    proof=canvas.Canvas(str(OUT/'Readability_Drafts_Review.pdf'),pageCompression=1)
    sheets=canvas.Canvas(str(OUT/'Readability_Drafts_Letter_Print.pdf'),pagesize=(612,792),pageCompression=1)
    for c in (proof,sheets):
        c.setAuthor("Escape Backpack")
        c.setTitle("Norse props - readability redesign drafts")
    for title,(w,h),front,back in PROPS:
        for side,draw in (("FRONT",front),("BACK",back)):
            if draw is not None:
                proof.setPageSize((w,h));draw(proof);proof.showPage()
            x,y=(612-w)/2,(792-h)/2
            text(sheets,306,742,title.upper(),13,"Helvetica-Bold",align="center")
            text(sheets,306,722,"Review draft - "+(side if draw is not None else "BLANK REVERSE"),11,align="center")
            if draw is not None:
                sheets.saveState();sheets.translate(x,y);draw(sheets);sheets.restoreState()
            crop_marks(sheets,x,y,w,h)
            text(sheets,306,104,f"Finished size: {w/72:g} x {h/72:g} in. Print at 100% / Actual size.",10,align="center")
            text(sheets,306,88,"Duplex: flip on the long edge. Check registration before cutting.",10,align="center")
            sheets.showPage()
    for code in ("1021"," 532"):
        proof.setPageSize((612,612));wheel_preview(code)(proof);proof.showPage()
    wheel_sheet(sheets);sheets.showPage()
    text(sheets,306,396,"Blank reverse for the wheel arm.",11,align="center")
    sheets.showPage()
    proof.save();sheets.save()
    index={letter:number for letter,_,number in museum.INDEX}
    assert ''.join(str(index[s]) for s in 'WOLF')=='4865'
    assert tuple(sum(p[i] for p in aud.PER_LEG) for i in range(3))==aud.ANSWER==(5,3,2)
    assert sum(v for _,_,v,_ in aud.COIN_KEY[2][1])==3705
    assert wheel.label(" 532",MAPS)=="ᛈᚹᛟᛇ"
    assert wheel.label("0532",MAPS)!=wheel.label(" 532",MAPS)
    print("Built both PDFs; WOLF, Aud route/coins and blank-first wheel checks pass.")


if __name__=='__main__':build()
