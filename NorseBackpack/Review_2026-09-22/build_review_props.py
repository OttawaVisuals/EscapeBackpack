"""Build isolated review proposals. Never writes to the original output directory."""
from pathlib import Path
import sys, importlib.util
import pymupdf
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
GREEN, PAPER, RUST = map(HexColor, ['#283B34', '#EFE3C4', '#B56A2A'])
pdfmetrics.registerFont(TTFont('Liv', str(ROOT/'Fonts/Nothing_You_Could_Do/NothingYouCouldDo-Regular.ttf')))

def wrap(t, font, size, width):
    lines, cur = [], ''
    for word in t.split():
        cand = (cur+' '+word).strip()
        if pdfmetrics.stringWidth(cand,font,size)>width:
            lines.append(cur); cur=word
        else: cur=cand
    return lines+[cur]

def text(c,t,x,y,width,size=11,font='Helvetica',leading=15):
    c.setFont(font,size)
    for line in wrap(t,font,size,width):
        c.drawString(x,y,line); y-=leading
    return y

def build():
    # Aud's canonical PDF includes a designer answer as page 3. Copy player pages only.
    src=pymupdf.open(ROOT/'output/pdf/Aud_Ticket_Print.pdf')
    dst=pymupdf.open(); dst.insert_pdf(src,from_page=0,to_page=1)
    dst.set_metadata({'title':'Aud ticket - PLAYER pages only - review copy'})
    dst.save(HERE/'Aud_Ticket_PLAYER_ONLY.pdf'); dst.close(); src.close()

    # Reuse authoritative geometry and keep all modifications inside this review folder.
    sys.path.insert(0,str(ROOT/'NorseBackpack/TravelMap'))
    import build_trail_maps_pdf as maps
    maps.OUT_DIR=HERE
    # E7 decodes L in a selected RAVEN column, competing with F at E3.
    # Move that decoy one column right to I7. All five selected columns are now unique.
    maps.HARALD_RUNES_DECOY=tuple((3,7,g,p) if (col,row)==(2,7) else (col,row,g,p)
                                 for col,row,g,p in maps.HARALD_RUNES_DECOY)
    assert len([r for r in maps.HARALD_RUNES_REAL+maps.HARALD_RUNES_DECOY if r[0]==2])==1
    maps.build('harald',maps.TRAILS['harald'],maps.load_plan(),maps.load_corpus())
    generated=HERE/'Trail_Map_4_Harald_Print.pdf'
    generated.replace(HERE/'Trail_Map_4_Harald_Rune_Review.pdf')

    # A Letter-sized journal gives the small reference drawings and instructions room.
    c=canvas.Canvas(str(HERE/'Journal_Family_Iconography_Review.pdf'),pagesize=(612,792))
    c.setTitle('Family iconography - proposed review edition')
    c.setFillColor(PAPER);c.rect(24,24,564,744,fill=1,stroke=0)
    c.setFillColor(GREEN);text(c,'Family iconography',44,736,520,25,'Liv',30)
    text(c,'Each stop I chose for the four traced routes carries one of these nine marks.',44,704,520,12,'Liv',17)
    text(c,'The other postcards are still memories of my travels. Keep them with the tickets.',44,669,520,11,'Liv',16)
    art=ROOT/'NorseBackpack/Art/FinalPuzzle'
    for x,file,caption,names in [
        (51,'Family_Symbol_Three_Field_v2.png','The symbol - three','raven / longship / sun-wheel'),
        (325,'Family_Crest_Six_Field_v2.png','The crest - six','bearded axe / round shield / wolf / anchor / drinking horn / valknut')]:
        c.drawImage(ImageReader(str(art/file)),x,430,230,215,preserveAspectRatio=True,anchor='c',mask='auto')
        c.setFillColor(GREEN);text(c,caption,x,416,230,13,'Liv',17)
        text(c,names,x,396,230,10,'Helvetica',13)
    c.setStrokeColor(RUST);c.line(44,354,568,354)
    c.setFillColor(GREEN);text(c,'Travel highlights',44,331,524,22,'Liv',27)
    y=301
    entries=[
        ('By train','Staraya Ladoga to Kyiv. My next postcard stop after Ladoga was Kyiv. Two days by the window, and I still slept through the best of it.'),
        ('By train','Walcheren to Chalus. Chalus was my next postcard stop. Three changes and one missed connection; a stranger shared his sandwiches.'),
        ('By train','Rouen to Bayeux. My next postcard stop after Rouen was Bayeux. I had been looking forward to that tapestry for months.'),
        ('By sea and road','After Bayeux, I crossed the Channel and continued to Winchester. Battle and its battlefield were still ahead of me.'),
        ('Turning south','I had already visited Kyiv when I reached Hedeby. Aci Castello and Patara were still ahead of me.')]
    for heading,body in entries:
        c.setFillColor(RUST);text(c,heading,44,y,524,10,'Helvetica-Bold',14);y-=15
        c.setFillColor(GREEN);y=text(c,body,44,y,524,11,'Liv',15)-7
    assert y>32,y
    c.showPage();c.save()

    slips=[
        ('Start here','Keep every postcard and ticket, even after it has helped you open something. Read both sides. You may separate papers and use the tools provided; nothing needs force. The first postcard starts your journey. Ask for a hint whenever the trail goes cold.'),
        ('Two skies','Those two northern skies belong together. Put the picture sides face to face, turn one card half a turn, and line up their top edges against a bright light. Look closely along the join.'),
        ('Walking through words','The four word-pairs mentioned in my Rouen message give four journeys on the map, in the order I mention them. Either word in a pair counts. Match each pair on the ticket: letter first, number second. Start at its picture and count grid steps to its square. Count the moves, not the starting square.'),
        ('Reading the balance','Sort the coins by their marks. Weigh the pile whose mark matches the cache. Use grams, with the scale empty and zeroed first. Ignore the last digit after the decimal point, then ignore the dot. Turn the remaining four digits upside down. What word do they become?'),
        ('Our three-move challenge','This is our own little puzzle: only the king moves. All other pieces stay fixed, and none are captured or jumped over. Slide in a straight line along a row or column. Reach any corner in exactly three moves. Count the squares travelled on each move, excluding the starting square.'),
        ('The whole journey','Group the postcards by their stamps. Use my family drawings to choose the stops to trace; set the other cards aside for drawing, but keep them for reading the tickets. The first origin and final destination of each travel ticket join my journeys. Use the journal and postcards to order the stops within each journey. On each map, join the chosen place dots with straight lines in that order. Keep north at the top and read each route as a digit. Follow the ticket chain to put the four digits in order.'),
    ]
    c=canvas.Canvas(str(HERE/'Playtest_Clue_Inserts_Review.pdf'),pagesize=(612,792))
    c.setTitle('Proposed clue inserts - review edition - three Letter sheets')
    for i in range(0,len(slips),2):
        c.setFillColor(GREEN);text(c,'PROPOSED PLAYTEST INSERTS - print at 100%; cut on outlines',36,763,540,10,'Helvetica-Bold',13)
        text(c,'Review notes: fit these cues into Liv\'s props after testing. Balance slip requires a cache mark and a calibrated coin pile.',36,742,540,9,'Helvetica',12)
        for j,(title,body) in enumerate(slips[i:i+2]):
            x,y,w,h=54,414-j*336,504,288
            c.setFillColor(PAPER);c.setStrokeColor(RUST);c.rect(x,y,w,h,fill=1,stroke=1)
            c.setFillColor(GREEN);text(c,title,x+24,y+h-37,w-48,20,'Liv',24)
            bottom=text(c,body,x+24,y+h-71,w-48,13,'Helvetica',19)
            assert bottom>y+15,(title,bottom,y)
        c.showPage()
    c.save()
    for p in HERE.glob('*.pdf'):
        d=pymupdf.open(p)
        for i,page in enumerate(d):
            page.get_pixmap(matrix=pymupdf.Matrix(1.5,1.5)).save(HERE/'Previews'/f'{p.stem}_{i+1}.png')
    print('Built four review PDFs; originals untouched.')

if __name__=='__main__':build()
