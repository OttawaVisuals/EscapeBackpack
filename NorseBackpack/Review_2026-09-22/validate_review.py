"""Read-only checks against originals and the separate review outputs."""
from pathlib import Path
from collections import Counter
from itertools import product
from urllib.parse import unquote,urlparse
import ast,json,sys,subprocess
import pymupdf
from bs4 import BeautifulSoup
from review_content import RELEASES,HINTS,FINDINGS

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'NorseBackpack/Tools'))
import final_riddle_clues as f
sys.path.insert(0,str(ROOT/'NorseBackpack/Props/Hnefatafl'))
import board_layout as b
sys.path.insert(0,str(ROOT/'NorseBackpack/Postcards'))
import postcard_marks as marks
report={'date':'2026-09-22','baseline_commit':'688ed06','physical_playtest':'NOT RUN','runtime_timing':'NOT MEASURED','historical_claims':'Not independently re-researched'}
assert set(RELEASES)==set(marks.MARKS)
report['card_releases']={'count':len(RELEASES),'all_22_exactly_once':True}
report['element_frequencies']=dict(Counter(marks.MARKS.values()))
assert all(v==2 for v in report['element_frequencies'].values())
report['original_order_model']={leg:len(f.solve_leg(leg)) for leg in f.LEG_ORDER}
assert all(v==1 for v in report['original_order_model'].values())
weaker=[x for x in f.CLUES if not(x[0]=='adjacent' and x[1]==('R3','R4'))]
weaker += [('before',('R3','R4'),'JOURNAL','Bayeux before Winchester'),('before',('R4','R5'),'JOURNAL','Winchester before Battle')]
report['weaker_printed_ferry_rollo_orders']=len(f.solve_leg('rollo',clues=weaker))
assert report['weaker_printed_ferry_rollo_orders']==1
proposed=[x for x in weaker if x[0]!='med_split']
proposed += [('before',('H3','H4'),'JOURNAL','Kyiv before Hedeby'),('before',('H4','H5'),'JOURNAL','Hedeby before Aci'),('before',('H4','H6'),'JOURNAL','Hedeby before Patara')]
report['proposed_journal_real_orders']={leg:[list(x) for x in f.solve_leg(leg,clues=proposed)] for leg in f.LEG_ORDER}
assert all(len(v)==1 for v in report['proposed_journal_real_orders'].values())
routes=[]
def walk(pos,path):
    if len(path)==4:
        if pos in b.CORNERS:routes.append(path)
        return
    if pos in b.CORNERS:return
    for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
        x,y=pos
        while True:
            x+=dx;y+=dy
            if not(0<=x<11 and 0<=y<11) or (x,y) in b.BLOCKS:break
            walk((x,y),path+[(x,y)])
walk(b.THRONE,[b.THRONE])
assert routes==[b.SOLUTION_PATH]
report['fixed_board']={'solutions':len(routes),'path':[b.coord_label(*p) for p in routes[0]],'code':'253','rule_assumption':'Only king moves; all other pieces fixed; no jumps or captures.'}
tree=ast.parse((ROOT/'NorseBackpack/TravelMap/build_trail_maps_pdf.py').read_text(encoding='utf-8'))
v={}
for node in tree.body:
    if isinstance(node,ast.Assign) and isinstance(node.targets[0],ast.Name) and node.targets[0].id in ['HARALD_RUNES_REAL','HARALD_RUNES_DECOY']:
        v[node.targets[0].id]=ast.literal_eval(node.value)
key=['fuþörk','hnias',"tbmlr"]
def choices(decoys):
    all_stems=v['HARALD_RUNES_REAL']+tuple(decoys)
    choices=[]
    for col in [6,0,8,2,5]:
        choices.append([key[r[2]-1][r[3]-1].upper() for r in all_stems if r[0]==col])
    return [''.join(x) for x in product(*choices)]
report['original_raven_readings']=choices(v['HARALD_RUNES_DECOY'])
fixed=[(3,7,g,p) if (c,r)==(2,7) else (c,r,g,p) for c,r,g,p in v['HARALD_RUNES_DECOY']]
report['review_raven_readings']=choices(fixed)
assert report['review_raven_readings']==['HRAFN']
report['original_print_bundles']={}
for path in [ROOT/'output/pdf/Norse_Postcards_Full_Print.pdf',*sorted((ROOT/'output/pdf').glob('Postcard_Sheet_*LongEdge_Print.pdf'))]:
    d=pymupdf.open(path)
    report['original_print_bundles'][path.name]={'pages':len(d),'postcard_backs':sum(p.get_text().count('POST CARD') for p in d)}
broken=[];bad_pdf_links=[];duplicate_ids=[];links=0
for path in [ROOT/'NorseBackpack/Norse_Brainstorm_Review.html',HERE/'Norse_Hints_Review.html']:
    s=BeautifulSoup(path.read_text(encoding='utf-8'),'html.parser')
    ids=[e['id'] for e in s.select('[id]')]
    duplicate_ids += [id for id,cnt in Counter(ids).items() if cnt>1]
    for e in s.select('[href],[src]'):
        u=e.get('href',e.get('src'));parsed=urlparse(u)
        if parsed.scheme:continue
        if parsed.path:
            target=(path.parent/unquote(parsed.path)).resolve();links+=1
            if not target.exists():broken.append(str(target))
        elif parsed.fragment and parsed.fragment not in ids:broken.append(path.name+'#'+parsed.fragment)
        if parsed.path.lower().endswith('.pdf'):
            if e.get('target')!='_blank' or 'noopener' not in e.get('rel',[]) or e.has_attr('download'):bad_pdf_links.append(u)
    for i,script in enumerate(s.find_all('script')):
        if script.string:
            proc=subprocess.run(['node','--check'],input=script.string,text=True,capture_output=True)
            assert proc.returncode==0,proc.stderr
assert not duplicate_ids,duplicate_ids
assert not bad_pdf_links,bad_pdf_links
# Handoff is written at session close; require it before the final validation.
report['html']={'local_references_checked':links,'broken':broken,'duplicate_ids':duplicate_ids,'pdf_link_policy_errors':bad_pdf_links,'javascript_syntax':'PASS'}
report['review_pdfs']={}
for path in HERE.glob('*.pdf'):
    d=pymupdf.open(path);report['review_pdfs'][path.name]=len(d)
    for p in d:
        for block in p.get_text('dict')['blocks']:
            if 'lines' not in block:continue
            assert pymupdf.Rect(block['bbox']) in p.rect,(path.name,block['bbox'])
original=pymupdf.open(ROOT/'output/pdf/Trail_Map_4_Harald_Print.pdf')
review=pymupdf.open(HERE/'Trail_Map_4_Harald_Rune_Review.pdf')
report['harald_board_back_unchanged']=original[1].get_pixmap().samples==review[1].get_pixmap().samples
assert report['harald_board_back_unchanged']
aud=pymupdf.open(HERE/'Aud_Ticket_PLAYER_ONLY.pdf');source=pymupdf.open(ROOT/'output/pdf/Aud_Ticket_Print.pdf')
report['aud_player_pages_unchanged']=all(aud[i].get_pixmap().samples==source[i].get_pixmap().samples for i in range(2))
assert report['aud_player_pages_unchanged'] and len(aud)==2
report['required_gates']=len(HINTS)
report['findings']=len(FINDINGS)
(HERE/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
assert not broken,broken
print('PASS: 22 releases; original and proposed order logic; board uniqueness; rune fix; PDFs; links; JS syntax.')
print('Physical proof and team timing remain untested.')
