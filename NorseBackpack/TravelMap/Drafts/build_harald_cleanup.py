"""Harald draft: title symbol and board-note styling; all puzzle geometry preserved."""
from pathlib import Path
from io import BytesIO
import math
import random
import sys
import pymupdf
from reportlab.lib.colors import HexColor

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import build_trail_maps_pdf as m
import build_board_setup_pdf as board
from reportlab.pdfgen import canvas

OUT = m.ROOT / 'NorseBackpack/Print/_pdf_source/Harald_Cleanup_Draft'
ASSET = HERE / 'Harald_Axe_Transparent_v1.png'

def arrows(c):
    c.saveState()
    c.setStrokeColor(board.PENCIL)
    c.setFillColor(board.PENCIL)
    c.setLineCap(1)
    for n, ((fx, fy), (tx, ty)) in enumerate(board.BLACK_MOVES[:2], 1):
        x0, y0 = (fx+.5)*board.CELL, (fy+.5)*board.CELL
        x1, y1 = (tx+.5)*board.CELL, (ty+.5)*board.CELL
        length = math.hypot(x1-x0, y1-y0)
        ux, uy = (x1-x0)/length, (y1-y0)/length
        nx, ny = -uy, ux
        a = (x0+ux*board.CELL*.38, y0+uy*board.CELL*.38)
        b = (x1-ux*board.CELL*.30, y1-uy*board.CELL*.30)
        # Subtle second pencil pass with the same precise endpoints.
        c.setStrokeAlpha(.32)
        board.pen_line(c, a, b, 9170+n, wobble=1.6, width=.65)
        c.setStrokeAlpha(1)
        board.pen_line(c, a, b, 7100+n, wobble=1.3, width=1.05)
        for side in (-1, 1):
            q = (b[0]-ux*6.5+nx*3.6*side, b[1]-uy*6.5+ny*3.6*side)
            board.pen_line(c, b, q, 7200+n*2+(side>0), wobble=.45, width=1.05)
        mx, my = (a[0]+b[0])/2-11, (a[1]+b[1])/2
        c.setFont(board.HAND, 12)
        c.drawCentredString(mx, my-3.5, str(n))
        pts = [(mx+6.8*math.cos(i*math.tau/16), my+7.0*math.sin(i*math.tau/16)) for i in range(16)]
        for i in range(16):
            board.pen_line(c, pts[i], pts[(i+1)%16], 9400+n*20+i, wobble=.18, width=.7)
    c.restoreState()

def board_core(c):
    """White paper; transferred columns, headings and both K corners stay smudged."""
    ox, oy = board.grid_origin()
    c.setFillColor(board.INK)
    c.setFont(board.HAND, 16)
    c.drawCentredString(board.W/2, board.H-22, 'Hnefatafl - board layout')
    c.setFillColor(board.RUST)
    c.setFont(board.HAND, 8.2)
    c.drawCentredString(board.W/2, board.H-34, "(so I don't forget!)")
    c.saveState()
    c.translate(ox, oy)
    board.draw_grid_ink(c)
    board.draw_column_labels(c, board.VISIBLE_COLS)
    board.draw_row_labels(c)
    board.draw_tokens(c, board.VISIBLE_COLS)
    arrows(c)
    c.restoreState()
    # Extend beyond the grid to cover the column headings and lower corner.
    box = (ox+min(board.HIDDEN_COLS)*board.CELL-.28*board.CELL,
           oy-.35*board.CELL,
           len(board.HIDDEN_COLS)*board.CELL+.75*board.CELL,
           board.GRID_H+1.15*board.CELL)
    c.saveState()
    c.drawImage(board._smear_wash(HexColor('#FFFFFF')), *box[:2],
                width=box[2], height=box[3], mask='auto')
    c.drawImage(board._smudged_lines(box, ox, oy), *box[:2],
                width=box[2], height=box[3], mask='auto')
    # Pale dragged traces remain where the ticket lifted the headings and corners.
    for dx, dy, alpha in ((0, 0, .075), (1.3, -.8, .035), (2.4, -1.7, .02)):
        c.saveState()
        c.translate(ox+dx, oy+dy)
        c.setFillColor(board.INK)
        c.setFillAlpha(alpha)
        c.setFont(board.HAND, 9)
        for col in board.HIDDEN_COLS:
            rng = random.Random(8000+col)
            c.saveState()
            c.translate((col+.5)*board.CELL, board.GRID_H+4+rng.uniform(-.4,.4))
            c.rotate(rng.uniform(-1.2,1.2))
            c.drawCentredString(0, 0, chr(65+col))
            c.restoreState()
        c.setStrokeColor(board.RUST)
        c.setStrokeAlpha(alpha)
        for row in (0, board.SIZE-1):
            cx, cy = (board.SIZE-.5)*board.CELL, (row+.5)*board.CELL
            r = board.CELL*.26
            pts = [(cx, cy+r), (cx+r, cy), (cx, cy-r), (cx-r, cy)]
            for i in range(4):
                board.pen_line(c, pts[i], pts[(i+1)%4], 9800+row*4+i,
                               wobble=.8, width=.85)
        c.restoreState()
    c.setFillAlpha(board.SMEAR_OPACITY)
    c.drawImage(board.ImageReader(str(board.SMEAR_ART)), *box[:2],
                width=box[2], height=box[3], mask='auto')
    c.restoreState()

def back_pdf():
    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=(m.PAGE_W, m.PAGE_H))
    c.setFillColor(HexColor('#FFFFFF'))
    c.rect(0, 0, m.PAGE_W, m.PAGE_H, fill=1, stroke=0)
    c.translate((m.PAGE_W-board.W)/2, (m.PAGE_H-board.H)/2)
    board_core(c)
    ox, oy = board.grid_origin()
    c.setFillColor(board.INK)
    visible_dark = sum(x in board.VISIBLE_COLS for x, y in board.ATTACKERS)
    visible_light = sum(x in board.VISIBLE_COLS for x, y in board.DEFENDERS)
    board.hand_text(c, f'This side: {visible_dark} dark, {visible_light} light.', ox, oy-17, 10.5)
    board.hand_text(c, 'King starts on the throne. Escape = any corner.', ox, oy-32, 10.5)
    line, y = '', oy-55
    for word in board.LIV_NOTE.split():
        trial = (line+' '+word).strip()
        if board.pdfmetrics.stringWidth(trial, board.HAND, 11) > board.GRID_W:
            board.hand_text(c, line, ox, y, 11)
            line, y = word, y-15
        else:
            line = trial
    board.hand_text(c, line, ox, y, 11)
    board.hand_text(c, '- L', ox, y-16, 11)
    assert (m.PAGE_H-board.H)/2+y-16 > 50, 'Note too close to page edge'
    c.showPage()
    c.save()
    return pymupdf.open(stream=buf.getvalue(), filetype='pdf')

def build():
    OUT.mkdir(parents=True, exist_ok=True)
    back = back_pdf()
    pix = pymupdf.Pixmap(ASSET)
    h = m.TITLE_H-4
    w = h*pix.width/pix.height
    right = m.NEAT[2]-6
    bottom = m.PAGE_H-m.NEAT[1]-2
    stamp_box = pymupdf.Rect(right-w, bottom-h, right, bottom)
    for kind in ('Print', 'ANSWER'):
        name = 'Trail_Map_4_Harald_'+kind+'.pdf'
        doc = pymupdf.open(m.ROOT/'NorseBackpack/Print/_pdf_source'/name)
        page = doc[0]
        old_text = page.get_text()
        clip = pymupdf.Rect(0, 0, m.PAGE_W, m.PAGE_H-m.NEAT[1]-m.TITLE_H)
        before = page.get_pixmap(matrix=pymupdf.Matrix(2, 2), clip=clip).samples
        stamps = [i for i in page.get_image_info(xrefs=True) if i['bbox'][0]>530 and i['bbox'][1]>695]
        assert len(stamps)==1
        assert len(page.get_image_rects(stamps[0]['xref']))==1
        page.delete_image(stamps[0]['xref'])
        page.insert_image(stamp_box, filename=str(ASSET))
        assert page.get_text()==old_text
        assert page.get_pixmap(matrix=pymupdf.Matrix(2, 2), clip=clip).samples==before
        doc.delete_page(1)
        doc.insert_pdf(back)
        target = OUT/name
        doc.save(target, garbage=4, deflate=True)
        check = pymupdf.open(target)
        note_text = ' '.join(check[1].get_text().split())
        assert board.LIV_NOTE in note_text, 'Note wording changed'
        for i, p in enumerate(check):
            p.get_pixmap(matrix=pymupdf.Matrix(2, 2)).save(OUT/(target.stem+f'_Page_{i+1}.png'))
        print(name+': front above title pixel-identical; note wording preserved')
    check[0].get_pixmap(matrix=pymupdf.Matrix(3, 3), clip=pymupdf.Rect(
        m.NEAT[0], m.PAGE_H-m.NEAT[1]-m.TITLE_H-3,
        m.NEAT[2], m.PAGE_H-m.NEAT[1]+2)).save(OUT/'Harald_Title_Band_Preview.png')

if __name__=='__main__':
    build()
