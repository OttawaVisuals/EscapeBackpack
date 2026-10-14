"""Render the Bureau overview from the shared Bible. Run from any directory."""
from pathlib import Path
import urllib.parse
import urllib.request
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from fontTools.ttLib import TTFont as FontToolsFont
from fontTools.varLib.instancer import instantiateVariableFont

ROOT = Path(__file__).resolve().parents[2]
BIBLE = ROOT.parent / 'Cryptic-Bureau' / 'Bureau_Bible.md'
OUT = ROOT / 'output/pdf/Cryptic_Bureau_One_Pager.pdf'
FONTS = ROOT / 'Fonts/CrypticBureau'
FONTS.mkdir(parents=True, exist_ok=True)
families = {
    'Cormorant': ('cormorantgaramond', 'CormorantGaramond[wght].ttf'),
    'SourceSans': ('sourcesans3', 'SourceSans3[wght].ttf'),
}
for family, (folder, filename) in families.items():
    variable = FONTS / filename
    for remote, local in [(filename, variable), ('OFL.txt', FONTS / f'{family}-OFL.txt')]:
        if not local.exists():
            url = 'https://raw.githubusercontent.com/google/fonts/main/ofl/' + folder + '/' + urllib.parse.quote(remote)
            urllib.request.urlretrieve(url, local)
    for weight in ([600] if family == 'Cormorant' else [400, 600]):
        static = FONTS / f'{family}-{weight}.ttf'
        if not static.exists():
            font = instantiateVariableFont(FontToolsFont(variable), {'wght': weight}, inplace=False)
            font.save(static)
        pdfmetrics.registerFont(TTFont(f'{family}{weight}', str(static)))

text = BIBLE.read_text(encoding='utf-8')
story = text.split('### Origin story\n\n', 1)[1].split('\n\n### Members and roles', 1)[0].split('\n\n')
members_text = text.split('### Members and roles\n\n', 1)[1].split('\n\n', 1)[0]
members = [tuple(s.strip() for s in line.strip('|').split('|')) for line in members_text.splitlines()[2:]]
OUT.parent.mkdir(parents=True, exist_ok=True)
c = canvas.Canvas(str(OUT), pagesize=(612, 792))
c.setTitle('The Cryptic Bureau | Story, members and design')
c.setAuthor('The Cryptic Bureau')
BURGUNDY = HexColor('#542C3B')
IVORY = HexColor('#F4EBDD')
COPPER = HexColor('#B87650')
INK = HexColor('#382B30')
c.setFillColor(IVORY)
c.rect(0, 0, 612, 792, fill=1, stroke=0)

def para(content, x, y, width, size=10.8, leading=14.4, font='SourceSans400', color=INK):
    style = ParagraphStyle('body', fontName=font, fontSize=size, leading=leading, textColor=color)
    p = Paragraph(content, style)
    _, h = p.wrap(width, 1000)
    p.drawOn(c, x, y-h)
    return y-h

def label(content, x, y):
    c.setFillColor(BURGUNDY)
    c.setFont('SourceSans600', 9)
    c.drawString(x, y, content)

def rule(y):
    c.setStrokeColor(COPPER)
    c.setLineWidth(.7)
    c.line(38, y, 574, y)

# Place the approved image through a PDF clipping viewport; source PNG is unchanged.
logo = ROOT / 'Brand/CrypticBureau/LogoConcepts/CB_Logo_B_Archive_Hidden_Flaps_v1.png'
x, y, w, h = 38, 669, 135, 87
scale = w/700
c.saveState()
p = c.beginPath(); p.rect(x, y, w, h); c.clipPath(p, stroke=0)
c.drawImage(str(logo), x-280*scale, y-(1254-780)*scale, width=1254*scale, height=1254*scale)
c.restoreState()
label('STORY / MEMBERS / DESIGN', 193, 750)
para('The Cryptic Bureau', 191, 738, 385, 34, 36, 'Cormorant600', BURGUNDY)
para('A family tradition, delivered in puzzles.', 193, 695, 375, 13, 17, 'SourceSans400', BURGUNDY)
rule(651)
para('Cooperative puzzle adventures sent as mysterious family packages. Each box stands alone; every dispatch belongs to a larger family story.', 38, 637, 536, 12, 16)

label('HOW IT BEGAN', 38, 584)
yy = 569
for paragraph in story:
    yy = para(paragraph, 38, yy, 322, 11, 14.7) - 12
label('THE FAMILY RITUAL', 38, yy-5)
yy = para('Receive a package. Explore its puzzles.<br/>Become part of the Bureau. Pass the tradition on.', 38, yy-17, 322, 13, 17, 'Cormorant600', BURGUNDY)
assert yy > 247, f'Story overflow: {yy}'

c.setStrokeColor(COPPER); c.setLineWidth(.5); c.line(380, 578, 380, 251)
label('THE MEMBERS', 398, 584)
my = 569
for name, role in members:
    my = para(name, 398, my, 176, 11.5, 13, 'Cormorant600', BURGUNDY)
    my = para(role, 398, my-2, 176, 9.7, 12) - 10
assert my > 247, f'Member overflow: {my}'

rule(237)
label('THE ARCHIVE IDENTITY', 38, 220)
para('An envelope and keyhole, with CRYPTIC and BUREAU tucked into the light flap seams. A mark for letters, packages and the family\'s shared seal.', 38, 208, 304, 10.6, 13.5)
para('Cormorant Garamond Semibold', 38, 151, 310, 17, 19, 'Cormorant600', BURGUNDY)
para('Display and wordmark / Source Sans 3 for supporting text', 38, 128, 310, 9.3, 12)
for xx, name, hx in [(370,'Burgundy','#542C3B'),(442,'Ivory','#F4EBDD'),(514,'Copper','#B87650')]:
    c.setFillColor(HexColor(hx)); c.setStrokeColor(COPPER); c.setLineWidth(.5)
    c.rect(xx, 166, 60, 39, fill=1, stroke=1)
    para(name, xx, 159, 67, 10, 12, 'SourceSans600', BURGUNDY)
    para(hx, xx, 144, 67, 9.2, 11)
para('Mysterious, playful and personal. Reusable games; no locks or app required. Optional hints are available online.', 38, 99, 536, 10.2, 13)
rule(57)
para('FICTIONAL SERIES OVERVIEW  /  13 OCTOBER 2026', 38, 45, 536, 8, 10, 'SourceSans600', BURGUNDY)
para('Member names and family links remain open. Logo shown is the approved raster concept.', 38, 32, 536, 8, 10)
c.showPage(); c.save()
print(OUT)
print(f'Story bottom: {yy:.1f}; members bottom: {my:.1f}')
