"""Swap only the title-band stamp on the current approved Aud PDFs; save drafts."""
from pathlib import Path
import sys
import pymupdf

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import build_trail_maps_pdf as m

# 17 Oct 2026 (designer): the pillars draft is rejected (Aud's postcards, stamp and ticket use the comb); the title band
# now carries the same transparent comb ink as the live stamp. Pillars draft kept in NorseBackpack/Print/_pdf_source/Aud_Stamp_Cleanup_Draft.
ASSET = HERE / 'Aud_Comb_Titleband_v1.png'  # Aud_Comb_Ink_v15_final.png cropped to its solid area
OUT = m.ROOT / 'NorseBackpack/Print/_pdf_source/Aud_Comb_Titleband_Draft'

def build():
    OUT.mkdir(parents=True, exist_ok=True)
    image = pymupdf.Pixmap(ASSET)
    height = m.TITLE_H - 4
    width = height * image.width / image.height
    x1 = m.NEAT[2] - 6
    y1 = m.PAGE_H - m.NEAT[1] - 2
    box = pymupdf.Rect(x1 - width, y1 - height, x1, y1)
    for kind in ('Print', 'ANSWER'):
        name = 'Trail_Map_3_Aud_' + kind + '.pdf'
        source = m.ROOT / 'NorseBackpack/Print/_pdf_source' / name
        doc = pymupdf.open(source)
        page = doc[0]
        text = page.get_text()
        map_clip = pymupdf.Rect(0, 0, m.PAGE_W, m.PAGE_H - m.NEAT[1] - m.TITLE_H)
        before = page.get_pixmap(matrix=pymupdf.Matrix(2, 2), clip=map_clip).samples
        stamps = [info for info in page.get_image_info(xrefs=True)
                  if info['bbox'][0] > 530 and info['bbox'][1] > 695]
        assert len(stamps) == 1, 'Expected exactly one title-band stamp'
        stamp = stamps[0]
        assert len(page.get_image_rects(stamp['xref'])) == 1, 'Stamp image is shared'
        page.delete_image(stamp['xref'])
        page.insert_image(box, filename=str(ASSET), keep_proportion=True)
        target = OUT / name
        doc.save(target, garbage=4, deflate=True)
        doc.close()
        check = pymupdf.open(target)
        assert check[0].get_text() == text, 'Map text changed'
        after = check[0].get_pixmap(matrix=pymupdf.Matrix(2, 2), clip=map_clip).samples
        assert after == before, 'Map artwork outside the title band changed'
        check[0].get_pixmap(matrix=pymupdf.Matrix(2, 2)).save(OUT / (target.stem + '_Preview.png'))
        if kind == 'Print':
            clip = pymupdf.Rect(m.NEAT[0], m.PAGE_H - m.NEAT[1] - m.TITLE_H - 3,
                                m.NEAT[2], m.PAGE_H - m.NEAT[1] + 2)
            check[0].get_pixmap(matrix=pymupdf.Matrix(3, 3), clip=clip).save(OUT / 'Aud_Title_Band_Preview.png')
        print(name + ': text preserved; map above title band pixel-identical')

if __name__ == '__main__':
    build()
