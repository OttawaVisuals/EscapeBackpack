"""Build the V2 paper prototype. Run with Python + reportlab from any directory."""
import json
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, black, white
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
D = json.loads((HERE / 'aurora-qr-layoutV2.json').read_text())
OUT = ROOT / 'output/pdf/Aurora_V2_Paper_Prototype.pdf'
OUT.parent.mkdir(parents=True, exist_ok=True)
C = canvas.Canvas(str(OUT), pagesize=letter)
C.setTitle('Aurora - V2 QR repair paper prototype')
W, H = letter
M = D['moduleSizeMm'] * mm
INK = HexColor('#163441')
STYLE = ParagraphStyle('body', fontName='Helvetica', fontSize=12, leading=18, textColor=INK)
def text(x, y, s, size=11, color=INK, font='Helvetica'):
    C.setFillColor(color); C.setFont(font, size); C.drawString(x, y, s)
def para(s, y, width=500):
    p = Paragraph(s, STYLE); _, h = p.wrap(width, 600); p.drawOn(C, 54, y-h); return y-h-16
def start(title, sub, page):
    text(54, H-52, 'AURORA / COMMUNICATIONS', 10)
    text(54, H-86, title, 23, font='Helvetica-Bold')
    text(54, H-110, sub, 10)
    C.setStrokeColor(INK); C.setLineWidth(.7); C.line(54, H-125, W-54, H-125)
    text(54, 30, f'V2 PAPER PROTOTYPE  |  {page}/5', 8)
def end(): C.showPage()
def qr(matrix, x, top):
    C.setFillColor(white); C.rect(x-4*M, top-29*M, 33*M, 33*M, fill=1, stroke=0)
    C.setFillColor(black)
    for r in range(25):
        for col in range(25):
            if matrix[r*25+col]: C.rect(x+col*M, top-(r+1)*M, M, M, fill=1, stroke=0)
def outline(cells, x, top, color=INK, width=.5):
    cells = set(map(tuple, cells)); C.setStrokeColor(color); C.setLineWidth(width)
    for r,c in cells:
        l=x+c*M; t=top-r*M
        for dr,dc,edge in [(-1,0,(l,t,l+M,t)),(1,0,(l,t-M,l+M,t-M)),(0,-1,(l,t,l,t-M)),(0,1,(l+M,t,l+M,t-M))]:
            if (r+dr,c+dc) not in cells: C.line(*edge)
def axes(x, top):
    # All labels and orientation marks stay beyond the four-module quiet zone.
    for i in range(25):
        C.setFont('Helvetica',5); C.setFillColor(INK)
        C.drawCentredString(x+(i+.5)*M, top+5*M, str(i+1))
        C.drawRightString(x-5*M, top-(i+.7)*M, str(i+1))
    text(x, top+9*M, 'TOP / ALIGN THIS EDGE', 9, font='Helvetica-Bold')
def scale(y):
    C.setStrokeColor(black); C.setLineWidth(.7)
    C.line(54,y,54+50*mm,y)
    for x in [54,54+50*mm]: C.line(x,y-4,x,y+4)
    text(54,y-18,'This line must measure exactly 50 mm.',9)

BRIEF = [
 '12 MARCH 2032 / URGENT<br/>FROM: HAROLD &nbsp;&nbsp; TO: DR. SARAH LANCASTER',
 'Dr. Lancaster, a micrometeorite strike has damaged Aurora. You appear to have struck your head during the impact. Preliminary scans suggest you may be experiencing memory loss.',
 'Commander Helena Chen and Engineer Alistair Johnson are sealed inside the crew quarters. You are the only crew member currently able to reach the damaged sections.',
 "You have located Engineer Johnson's emergency backpack. Some repair tools are locked inside its compartments. I have begun compiling the information you will need to open them.",
 'My communications system is failing. Before we can proceed, you must restore the optical interface in the open pocket of the backpack.',
 '<b>Find the six repair patches and the optical maintenance diagram. Match every patch to its outline, keep the same orientation, and transfer it to the corresponding position on the interface. Install all six patches, then scan.</b>',
 'I will guide you through the remaining repairs once the connection is res...'
]
# Player-facing Aurora letterhead; essential text remains clear despite the failed transmission.
NAVY = HexColor('#16253c')
ORANGE = HexColor('#a84420')
C.drawImage(str(ROOT/'Images/SpaceStationAurora.jpg'), 48, 668, 78, 78, mask='auto')
text(142, 730, 'STATION AURORA', 24, NAVY, 'Helvetica-Bold')
text(143, 709, 'HAROLD / EMERGENCY COMMUNICATIONS', 9, NAVY)
text(143, 689, 'LOCAL HARDCOPY  /  12 MARCH 2032', 9, ORANGE, 'Courier-Bold')
C.setStrokeColor(NAVY); C.setLineWidth(1.5); C.line(54, 654, 558, 654)
C.setFillColor(ORANGE); C.rect(54, 615, 65, 24, fill=1, stroke=0)
text(66, 623, 'URGENT', 10, white, 'Helvetica-Bold')
text(131, 622, 'MICROMETEORITE STRIKE', 16, NAVY, 'Helvetica-Bold')
text(54, 594, 'FROM  HAROLD', 10, NAVY, 'Courier')
text(275, 594, 'TO  DR. SARAH LANCASTER', 10, NAVY, 'Courier')
C.setStrokeColor(HexColor('#d8dee4')); C.setLineWidth(.6); C.line(54, 580, 558, 580)
y=562
for s in BRIEF[1:5]: y=para(s,y)
# Distinct first action block, readable in grayscale as well as colour.
p = Paragraph(BRIEF[5], STYLE); _, box_h = p.wrap(472, 500)
C.setFillColor(HexColor('#f3f1ed')); C.rect(54, y-box_h-46, 504, box_h+46, fill=1, stroke=0)
C.setFillColor(ORANGE); C.rect(54, y-box_h-46, 3, box_h+46, fill=1, stroke=0)
text(70,y-19,'FIRST ACTION / RESTORE THE INTERFACE',9,ORANGE,'Helvetica-Bold')
p.drawOn(C,70,y-32-box_h)
y=y-box_h-66
y=para(BRIEF[6],y)
text(54,y,'[LINK LOST]  [PRINT BUFFER INCOMPLETE]',9,ORANGE,'Courier')
# Restrained interrupted-printer marks below the message, never over instructions.
for i,length in enumerate([169,117,58]):
    C.setStrokeColor(HexColor('#bac0c5')); C.setLineWidth(.4); C.line(54,y-14-i*3,54+length,y-14-i*3)
C.setStrokeColor(NAVY); C.setLineWidth(.6); C.line(54,55,558,55)
text(54,40,'AURORA / CREW EMERGENCY NOTICE',8,NAVY,'Courier')
text(421,40,'LOCAL COPY  /  01',8,NAVY,'Courier')
assert y-23 > 65, 'Briefing overlaps footer'
end()

start('Optical interface', 'PLAYER PANEL - KEEP FLAT AND UPRIGHT', 2)
para('Communications link damaged.<br/><b>Install all six repair patches before scanning.</b>',H-151)
x=(W-25*M)/2; top=485
qr(D['baseMatrix'],x,top); axes(x,top)
para('Use the maintenance diagram to locate the repairs. Row and column numbers refer to the small squares inside the code.',210)
scale(105); end()

start('Repair patches / cut sheet', 'PREPARATION SHEET - CUT BEFORE GIVING TO PLAYERS', 3)
para('Print single-sided at <b>100% / Actual size</b>. Use opaque white paper. Cut around each irregular outer outline, retaining every white square. The letters identify loose pieces during preparation; they are not part of the patches.',H-151)
positions=[(70,535),(335,535),(70,410),(335,410),(70,270),(335,270)]
for p,(px,pt) in zip(D['patches'],positions):
    cells=p['cells']; r0=min(a for a,b in cells); c0=min(b for a,b in cells)
    text(px,pt+19,'PATCH '+p['id'],10,font='Helvetica-Bold')
    for r,col in cells:
        C.setFillColor(black if D['targetMatrix'][r*25+col] else white)
        C.rect(px+(col-c0)*M,pt-(r-r0+1)*M,M,M,fill=1,stroke=0)
    outline([(r-r0,c-c0) for r,c in cells],px,pt,HexColor('#aaaaaa'),.25)
scale(85); end()

start('Optical maintenance diagram', 'AURORA ENGINEERING / EMERGENCY REPAIR PROCEDURE',4)
para('<b>1. Match</b> each repair patch to its shape below, printed face up.<br/><b>2. Transfer</b> it to the same rows and columns on the optical interface.<br/><b>3. Reconnect</b> after installing all six. Keep TOP pointing up.',H-151)
x=(W-25*M)/2; top=455
C.setStrokeColor(HexColor('#d7dee0')); C.setLineWidth(.25)
for i in range(26):
    C.line(x+i*M,top,x+i*M,top-25*M); C.line(x,top-i*M,x+25*M,top-i*M)
for r,c in [(0,0),(0,18),(18,0)]:
    C.setFillColor(INK); C.rect(x+c*M,top-(r+7)*M,7*M,7*M,fill=1,stroke=0)
    C.setFillColor(white); C.rect(x+(c+1)*M,top-(r+6)*M,5*M,5*M,fill=1,stroke=0)
    C.setFillColor(INK); C.rect(x+(c+2)*M,top-(r+5)*M,3*M,3*M,fill=1,stroke=0)
for p in D['patches']: outline(p['cells'],x,top,width=1)
axes(x,top)
para('The three large corner markers establish orientation.<br/>The small grid squares on this diagram and the interface are the same size. Do not rotate or turn over a patch during transfer.',185)
end()

start('Test setup / facilitator only', 'KEEP THIS PAGE AND THE CUT-SHEET OFFCUTS AWAY FROM PLAYERS',5)
y=para('<b>Print:</b> US Letter, single-sided, Actual size / 100%. Do not use Fit or Shrink. The 50 mm rulers on pages 2 and 3 must match. Each QR square is 3 mm; the code is 75 mm wide, or 99 mm including its white quiet zone.',H-151)
y=para('<b>Prepare:</b> give players page 1 (briefing), page 2 (base panel), page 4 (maintenance diagram) and the six cut patches from page 3. Secure patches flat with small amounts of removable adhesive underneath. Leave the white border clear.',y)
y=para('<b>Check first:</b> the bare panel should decode to https://escapepack.ca/coms. All six patches should decode to https://escapepack.ca/Harold (capital H). These pages have not been verified as deployed; reading the URL is enough for a paper test.',y)
y=para('<b>Accepted behavior:</b> earlier ideal-image tests found four five-patch subsets also decode to HAROLD. This prototype asks for all six, but does not enforce that physically. Test with actual phones, lighting and paper before production.',y)
text(54,y-3,'PLACEMENT REFERENCE / 1-BASED ROWS AND COLUMNS',10,font='Helvetica-Bold'); y-=27
for p in D['patches']:
    rows=[r for r,c in p['cells']]; cols=[c for r,c in p['cells']]
    text(54,y,f"{p['id']}   Rows {min(rows)+1}-{max(rows)+1}    Columns {min(cols)+1}-{max(cols)+1}    ({len(rows)} squares)",11); y-=21
y-=10
para('<b>Observe:</b> can players identify all six outlines, preserve orientation, align the 3 mm cells and scan the result? A few strips are only one square wide. If cutting or alignment dominates the experience, enlarge the entire pack together for another test.',y)
end(); C.save()
from pypdf import PdfReader, PdfWriter
brief_out = ROOT / 'output/pdf/Aurora_Emergency_Briefing.pdf'
writer = PdfWriter(); writer.add_page(PdfReader(str(OUT)).pages[0])
writer.add_metadata({'/Title': 'Station Aurora - Emergency briefing'})
with brief_out.open('wb') as stream: writer.write(stream)
(HERE/'Briefing_Refined_Draft.txt').write_text('STATION AURORA - METEORITE STRIKE - URGENT\n\n'+ '\n\n'.join(s.replace('<br/>','\n').replace('<b>','').replace('</b>','').replace('&nbsp;',' ') for s in BRIEF)+'\n\n[LINK LOST] [PRINT BUFFER INCOMPLETE]\n',encoding='utf-8')
print(OUT)
