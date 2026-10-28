"""Leif review draft: stronger animals, coastal labels and transparent title symbol."""
from copy import deepcopy
from pathlib import Path
import json
import sys
import pymupdf

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import build_trail_maps_pdf as m

OUT = m.ROOT / 'NorseBackpack/Print/_pdf_source/Leif_Cleanup_Draft'
cfg = deepcopy(m.TRAILS['leif'])
cfg['stamp_path'] = HERE / 'Leif_Longship_Transparent_v1.png'
cfg['stamp_height'] = m.TITLE_H - 4
cfg['stamp_right_inset'] = 6
cfg['fixed_labels'] = {
    'Makkovik': (5, -2.8),
    'Rigolet': (5, -3),
    'Cartwright': (5, -3),
    'Corner Brook': (5, 7),
    'Gander': (5, 7),
}
animals = ('Polar_Bear', 'Seal', 'Hare', 'Deer', 'Loon', 'Wolf', 'Orca')
original_art = m.LEIF_ART
m.LEIF_ART = tuple((name, box, .82 if any('_'+a+'_' in name for a in animals) else alpha)
                   for name, box, alpha in original_art)

def build():
    OUT.mkdir(parents=True, exist_ok=True)
    m.OUT_DIR = OUT
    plan, corpus = m.load_plan(), m.load_corpus()
    for answer in (False, True):
        assert not m.build('leif', cfg, plan, corpus, answer=answer), 'Missing route label'
    assert [box for name, box, alpha in m.LEIF_ART] == [box for name, box, alpha in original_art]
    for field in ('frame', 'parallels', 'lon0', 'extra_towns', 'omit_towns', 'display_names'):
        assert cfg[field] == m.TRAILS['leif'][field], field
    for kind in ('Print', 'ANSWER'):
        name = 'Trail_Map_1_Leif_'+kind+'.pdf'
        doc = pymupdf.open(OUT / name)
        page = doc[0]
        # Halos repeat names in extracted text; compare sets of complete text lines.
        source = pymupdf.open(m.ROOT / 'NorseBackpack/Print/_pdf_source' / name)
        assert set(source[0].get_text().splitlines()) == set(page.get_text().splitlines()), 'Label content changed'
        page.get_pixmap(matrix=pymupdf.Matrix(2, 2)).save(OUT / (Path(name).stem+'_Preview.png'))
        if kind == 'Print':
            page.get_pixmap(matrix=pymupdf.Matrix(3, 3), clip=pymupdf.Rect(
                m.NEAT[0], m.PAGE_H-m.NEAT[1]-m.TITLE_H-3,
                m.NEAT[2], m.PAGE_H-m.NEAT[1]+2)).save(OUT/'Leif_Title_Band_Preview.png')
    (OUT/'draft_notes.json').write_text(json.dumps({
        'status': 'review draft; live PDFs unchanged',
        'changes': ['Seven animal vignettes: opacity 0.62 to 0.82',
                    'Makkovik label east of dot', 'Rigolet label east of dot',
                    'Cartwright label east of dot', 'Corner Brook and Gander labels raised',
                    'Larger transparent longship symbol on blue title band'],
        'preserved': ['All art boxes and animal puzzle squares', 'All town coordinates',
                      'All text content', 'Page size, projection, grid and route geometry'],
        'physical_print_test': False,
    }, indent=2), encoding='utf-8')

if __name__ == '__main__':
    build()
