"""Reproducible Rollo cleanup draft. Live maps and their builder are unchanged."""
from copy import deepcopy
from pathlib import Path
import json
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import build_trail_maps_pdf as m

OUT = m.ROOT / "NorseBackpack" / "Print" / "_pdf_source" / 'Rollo_Cleanup_Draft'
cfg = deepcopy(m.TRAILS['rollo'])
cfg['stamp_path'] = HERE / 'Rollo_Comet_Transparent_v1.png'
cfg['stamp_height'] = m.TITLE_H - 4
cfg['stamp_right_inset'] = 6
cfg['fixed_labels'].update({'Rouen': (8, -3), 'Roumare forest': (-66, -24)})
# This is a region caption, not a settlement: move it below the crowded names.
cfg['areas'] = [(name, 48.67, -0.20) if name == 'Normandy' else (name, lat, lon)
                for name, lat, lon in cfg['areas']]

original_story = m.ROLLO_ART
original_word = m.ROLLO_WORDLOCK_ART
# Preserve original asset silhouettes, boxes, and therefore every puzzle square.
m.ROLLO_ART = tuple((name, box, .96) for name, box, alpha in original_story)
m.ROLLO_WORDLOCK_ART = tuple((name, box, .96) for name, box, alpha in original_word)

original_leader = m.draw_leader
def draw_leader(c, lab, path, box, dot):
    original_leader(c, lab, path, box, dot)
    if path.name == 'Rollo_Boar_v1.png':
        x, y = dot
        points = [(x - 2, y - 3), (x - 10, y - 16), (x - 16, y - 16)]
        c.saveState()
        c.setStrokeColor(m.LEADER_INK)
        c.setLineWidth(.55)
        c.setDash([])
        p = c.beginPath()
        p.moveTo(*points[0])
        for q in points[1:]:
            p.lineTo(*q)
        c.drawPath(p)
        c.restoreState()
        lab.reserve_polyline(points, radius=.7)
m.draw_leader = draw_leader

if __name__ == '__main__':
    OUT.mkdir(parents=True, exist_ok=True)
    m.OUT_DIR = OUT
    plan, corpus = m.load_plan(), m.load_corpus()
    for answer in (False, True):
        assert not m.build('rollo', cfg, plan, corpus, answer=answer), 'Missing route label'
    assert all(a[1] == b[1] for a, b in zip(original_story, m.ROLLO_ART))
    assert all(a[1] == b[1] for a, b in zip(original_word, m.ROLLO_WORDLOCK_ART))
    # Same projection, frame, page, town data and art boxes as the live map.
    for field in ('frame', 'parallels', 'lon0', 'extra_towns', 'icon_towns', 'decoy_towns'):
        assert cfg[field] == m.TRAILS['rollo'][field], field
    (OUT / 'draft_notes.json').write_text(json.dumps({
        'status': 'review draft; live PDFs unchanged',
        'changes': ['Icon opacity 0.62 to 0.96', 'Rouen label east of dot',
                    'Roumare forest label southwest with fine leader',
                    'Normandy region caption moved below settlement names',
                    'Larger transparent comet artwork on the blue title-band background'],
        'preserved': ['Page size', 'Projection and ruler scale', 'All town dots',
                      'All icon boxes and puzzle grid squares', 'Final route geometry'],
        'physical_print_test': False,
    }, indent=2), encoding='utf-8')
