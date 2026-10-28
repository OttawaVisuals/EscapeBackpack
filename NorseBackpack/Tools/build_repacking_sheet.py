"""Letter-size reset insert, matched to Full_Adventure.html's current contents.

Run from any directory. The adventure page supplies rune labels; the checked
inventory below deliberately excludes puzzle solutions and superseded prose.
"""
from pathlib import Path
from bs4 import BeautifulSoup
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'NorseBackpack/Print/_pdf_source/Raven_Inheritance_Repacking_Letter.pdf'
PAGE = ROOT / 'NorseBackpack/Full_Adventure.html'
FONT = ROOT / 'Fonts/CrypticBureau'
pdfmetrics.registerFont(TTFont('Body', str(FONT / 'SourceSans-400.ttf')))
pdfmetrics.registerFont(TTFont('Bold', str(FONT / 'SourceSans-600.ttf')))
pdfmetrics.registerFontFamily('Body', normal='Body', bold='Bold')
pdfmetrics.registerFont(TTFont('Title', str(ROOT / 'Fonts/Cinzel/static/Cinzel-Regular.ttf')))
pdfmetrics.registerFont(TTFont('Runes', 'C:/Windows/Fonts/seguihis.ttf'))
INK = HexColor('#283B34')
RUST = HexColor('#985626')
RULE = HexColor('#D7D5CA')
LIGHT = HexColor('#F4F4EF')
soup = BeautifulSoup(PAGE.read_text(encoding='utf-8'), 'html.parser')

# Every prop ID must occur exactly once in its listed envelope in the source.
ROWS = [
    (['PP-015', 'PP-028'], '<b>Bjarnarhöfn</b> postcard; Aud\'s comb'),
    (['PP-002', 'PP-003', 'PP-027'], '<b>Battle Harbour</b> and <b>Baffin Island</b> postcards; magnifier'),
    (['PP-017', 'PP-018', 'PP-022'], '<b>Staraya Ladoga</b>, <b>Kyiv</b> and <b>Constantinople</b> postcards'),
    (['PP-013', 'PP-030', 'PP-031'], '<b>Hvammur</b> postcard; <b>The Island Settlement</b> map; Aud\'s Treasure Museum ticket'),
    (['PP-005', 'PP-010', 'PP-011'], '<b>Châlus</b>, <b>Roumare Forest</b> and <b>Walcheren</b> postcards'),
    (['PP-004', 'PP-024', 'PP-029'], '<b>Brattahlíð</b> postcard; <b>The Western Lands</b> map; Brattahlíð museum ticket'),
    (['PP-012', 'PP-014', 'PP-026', 'PP-037'], '<b>Dögurðarnes</b> and <b>Esjuberg</b> postcards; all coins, mixed together; treasure tally set to <b>0000</b>'),
    (['PP-006', 'PP-032', 'PP-033'], '<b>Rouen</b> postcard; <b>The Granted Lands</b> map; Musée Ducal de Rouen ticket'),
    (['PP-007', 'PP-008', 'PP-009', 'PP-025'], '<b>Bayeux</b>, <b>Winchester</b> and <b>Battle</b> postcards; architect\'s scale ruler'),
    (['PP-016', 'PP-034', 'PP-035', 'PP-036'], '<b>Oslo</b> postcard; <b>The Varangian Road</b> map; hnefatafl board and all pieces; Hnefatafl Museum ticket'),
    (['PP-019', 'PP-020', 'PP-038'], '<b>Hedeby</b> and <b>Sicily</b> postcards; raven\'s flights card'),
    (['PP-021', 'PP-039'], '<b>Patara</b> postcard; all four journey sheets of hop tickets'),
    (['PP-043', 'PP-044'], 'Plane ticket; Liv\'s final letter; adventure medallion'),
]

def build():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUT), pagesize=(612, 792))
    c.setTitle('The Raven Inheritance - Repacking checklist')
    c.setAuthor('Escape Backpack')

    def text(x, y, value, size=11, font='Body', color=INK):
        c.setFillColor(color)
        c.setFont(font, size)
        c.drawString(x, y, value)

    def para(x, top, value, width=528, size=11, leading=13):
        p = Paragraph(value, ParagraphStyle('p', fontName='Body', fontSize=size,
                                           leading=leading, textColor=INK))
        w, h = p.wrap(width, 700)
        p.drawOn(c, x, top-h)
        return h

    def check(x, y):
        c.setStrokeColor(INK)
        c.setLineWidth(.65)
        c.rect(x, y-7, 8, 8)

    text(42, 751, 'THE RAVEN INHERITANCE', 19, 'Title')
    text(42, 728, 'REPACKING CHECKLIST', 13, 'Bold', RUST)
    text(42, 710, 'Open after playing. Contains spoilers. Keep this sheet for the next reset.', 10.5)
    c.setStrokeColor(INK)
    c.line(42, 698, 570, 698)

    text(42, 678, '1  PREPARE THE SET', 11, 'Bold')
    para(42, 669, 'Gather every card and prop. Remove player-added notes and route marks; '
         'replace marked paper if needed. Keep all printed clues intact. Reset the treasure tally to <b>0000</b>.', size=10.5)

    text(42, 624, '2  REFILL EACH ENVELOPE', 11, 'Bold')
    text(42, 609, 'Match the four runes on the front. Numbers below are reference only.', 10)
    text(42, 595, 'Find postcard names at the bottom of the art side; map titles along the bottom.', 10)
    text(61, 575, 'NO.', 8.5, 'Bold')
    text(89, 575, 'RUNE LABEL', 8.5, 'Bold')
    text(187, 575, 'RETURN THESE ITEMS', 8.5, 'Bold')
    y = 566
    for n, (ids, contents) in enumerate(ROWS, 1):
        env = soup.select_one(f'#env{n}')
        actual = [p['id'] for p in env.select('.prop')]
        assert actual == ids, (n, actual, ids)
        runes = env.select_one('header .runes').get_text(strip=True)
        assert len(runes) == 4
        style = ParagraphStyle('row', fontName='Body', fontSize=10.6, leading=12.4, textColor=INK)
        p = Paragraph(contents, style)
        w, h = p.wrap(378, 100)
        row_h = max(29, h+10)
        if n % 2:
            c.setFillColor(LIGHT)
            c.rect(42, y-row_h, 528, row_h, fill=1, stroke=0)
        check(47, y-12)
        text(63, y-18, str(n), 10.5, 'Bold')
        text(89, y-20, runes, 17, 'Runes')
        p.drawOn(c, 187, y-5-h)
        c.setStrokeColor(RULE)
        c.setLineWidth(.35)
        c.line(42, y-row_h, 570, y-row_h)
        y -= row_h

    y -= 21
    text(42, y, '3  CLOSE UP FOR THE NEXT TEAM', 11, 'Bold')
    items = [
        'Close every filled envelope. Return both decoy envelopes to the box.',
        'Put the <b>L\'Anse aux Meadows</b> postcard, the assembled rune cypher wheel and '
        '<b>Liv\'s notes card</b> loose on top of the envelopes.',
        'Fold this sheet with the text inside. Return it to the <b>large decoy envelope</b> '
        'and close it. Keep the starting items visible when the box opens.',
    ]
    for item in items:
        y -= 10
        check(44, y-3)
        h = para(60, y+2, item, width=510, size=10.5, leading=12.5)
        y -= h-2
    assert y > 48, y
    c.setStrokeColor(RULE)
    c.line(42, 45, 570, 45)
    text(42, 31, 'Print single-sided on US Letter (8.5 x 11 in) at 100% / Actual size.', 8.5)
    c.setFont('Body', 8)
    c.drawRightString(570, 31, 'Packing list: 18 Oct 2026')
    c.save()
    print(OUT)

if __name__ == '__main__':
    build()
