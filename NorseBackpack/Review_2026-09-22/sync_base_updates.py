"""Synchronize approved tally/perch design into the original brainstorm.

The initial migration preserves retired specifications inside closed history
disclosures. Later runs refresh only the shared Approved changes section.
"""
from pathlib import Path
import json
import re
from approved_changes import APPROVED
from review_content import HINTS

BASE = Path(__file__).resolve().parents[1] / 'Norse_Brainstorm.html'

def span(text, ident):
    start = re.search(r'<(div|section)\b[^>]*\bid="'+re.escape(ident)+r'"[^>]*>', text)
    if not start:
        raise ValueError('Missing element: '+ident)
    tag, depth = start.group(1), 0
    for token in re.finditer(r'</?'+tag+r'\b[^>]*>', text[start.start():]):
        depth += -1 if token.group().startswith('</') else 1
        if depth == 0:
            return start.start(), start.start()+token.end()
    raise ValueError('Unclosed element: '+ident)

def replace_element(text, ident, new):
    a,b = span(text,ident)
    return text[:a]+new+text[b:]

def old_inside(text, ident):
    a,b=span(text,ident)
    block=text[a:b]
    return block[block.index('>')+1:block.rfind('</')]

def qrow(ident, status, title, body, history=''):
    past = ('<details><summary>Superseded specification · before 22 September 2026</summary>'+history+'</details>') if history else ''
    return f'<div class="qrow" id="q-{ident}"><div class="qid">{ident} <span class="pill">{status}</span></div><div><div class="qt">{title}</div><div class="qd">{body}{past}</div></div></div>'

def replace_puzzle(text, key, obj):
    a=text.index("{key:'"+key+"'")
    b=text.index('\n\n{key:',a)
    return text[:a]+json.dumps(obj,ensure_ascii=False,indent=1)+','+text[b:]

def sync():
    text=BASE.read_text(encoding='utf-8')
    section='<section id="approved-updates" class="view"><div class="intro"><div><div class="eyebrow">Current decisions</div><h2>Approved changes · 22 September 2026</h2><p>Complete adopted mechanisms, postcard copy drafts and unfinished production work.</p></div></div>'+APPROVED+'<p><a href="Norse_Brainstorm_Review.html#props" target="_blank" rel="noopener">Open the updated review checklist and packing plan</a></p></section>'
    if 'id="approved-updates"' in text:
        text=replace_element(text,'approved-updates',section)
        BASE.write_text(text,encoding='utf-8')
        return
    notice='<div class="good"><strong>Approved update, 22 September 2026:</strong> coin values total 3705 and rotate to SOLE; HRAFN selects four flight digits, 2648, for a lock directly on the board pouch. The scale and cryptex are superseded. <a href="#" data-view="approved-updates">Full specifications, visual and postcard changes</a>. Older options below retain their historical status.</div>'
    text=text.replace('</nav>','<button aria-pressed="false" data-view="approved-updates">Approved changes</button></nav>',1)
    text=text.replace('<section id="story"',section+'\n<section id="story"',1)
    style='''<style>
#approved-updates .grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px;margin:22px 0}#approved-updates .card{min-width:0}#approved-updates h2{font-size:26px}#approved-updates h3{margin:18px 0 8px}#approved-updates p{margin:10px 0}#approved-updates li{margin:9px 0}#approved-updates .callout,#approved-updates .notice{padding:16px 20px;background:#e8ebde;border-left:4px solid #a56c3d;margin:18px 0}#approved-updates .tablewrap{overflow:auto}#approved-updates td,#approved-updates th{padding:12px;vertical-align:top;border-bottom:1px solid #d7d1bf;text-align:left}#approved-updates table{border-collapse:collapse;width:100%;margin:16px 0}#approved-updates figure{margin:24px 0}#approved-updates figure img{width:100%;height:auto}#approved-updates figcaption{font-size:13px;color:#586553}#approved-updates blockquote{border-left:3px solid #a56c3d;margin:15px 0;padding:8px 18px}#approved-updates details{margin:20px 0}@media(max-width:760px){#approved-updates .grid{grid-template-columns:1fr}}
</style>'''
    text=text.replace('</head>',style+'\n</head>',1)
    for ident in ['story','system','puzzles','design','postcards']:
        opening=re.search(r'<section\b[^>]*\bid="'+ident+r'"[^>]*>',text)
        text=text[:opening.end()]+notice+text[opening.end():]
    text=text.replace('the comb reads a message, the balance orders three cards, the board is set up by one.','the tally turns a coin total into a word, the perches turn decoded letters into four digits, and the board is set up by a postcard.')

    history=old_inside(text,'prop-hoard')
    text=replace_element(text,'prop-hoard','''<div class="designsection" id="prop-hoard"><div class="eyebrow">Approved replacement · 22 September 2026</div><h2>The hoard and treasure tally</h2><div class="card"><p>After the 521 treasure-route gate, release A1/A3, a mixed hoard, a merchant’s value key and a labelled treasure tally. The cache mark selects matching coins. Add their fictional game values to <strong>3705</strong>; display the total, then rotate the whole device 180 degrees to read <strong>SOLE</strong>.</p><p>The display can be a calculator or four independently settable 0–9 wheels. Label it <em>“Use this to tally treasure.”</em> A1 must instruct adding values; A3 must refer to the tally. Revised copy is in Approved changes. There is no scale, decimal point, discarded digit or mass target.</p><p><strong>Open:</strong> device choice (PR-24), coin inventory/value key/marks (PR-25), and physical legibility of the upside-down word. SOLE and MEAD require separate word locks.</p><p><a href="#" data-view="approved-updates" data-anchor="approved-coins">Full tally specification and postcard drafts</a></p></div><details><summary>Superseded hoard and balance design</summary>'''+history+'</details></div>')
    a,b=span(text,'prop-runes');block=text[a:b]
    block=block.replace('It fits a five-letter lock or a five-ring cryptex.','It is now an intermediate answer: follow H–R–A–F–N on The raven’s flights card to read 2648 for a four-digit lock directly on the board pouch. The former five-letter lock/cryptex proposal is superseded.')
    block=block.replace('<div class="box lock">HRAFN</div>','<div class="box">HRAFN</div><span class="arr">→</span><div class="box">The raven’s flights<br>H–R–A–F–N</div><span class="arr">→</span><div class="box lock">2648<br>board pouch</div>')
    block=block.replace('<h3>The answer: HRAFN</h3>','<h3>Decoded letters: HRAFN · lock code: 2648</h3>')
    block=block.replace('<div class="eyebrow">Cipher backbone</div>','<div class="eyebrow">Cipher backbone</div>'+notice+'<p><strong>Use the corrected review map:</strong> the old E7 decoy competes with E3. <a href="Review_2026-09-22/Trail_Map_4_Harald_Rune_Review.pdf" target="_blank" rel="noopener">Open corrected map PDF</a>. Pack the player-only perch card with H4/H5, before the board lock. H4/H5 remain unchanged; the new card carries the flight instructions.</p>')
    text=text[:a]+block+text[b:]

    updates=[
      ('PZ-03','Mechanism approved · print changes pending','Aud’s coin-value tally gives SOLE.','Select matching coins, add their fictional values to 3705, record the total and rotate the whole display to read SOLE. A1 requires revised puzzle copy; A3 needs a tally wording update. See Approved changes. Device choice and coin inventory remain open (PR-24/25).'),
      ('PZ-02','Mechanism approved · perch print pending','HRAFN selects five perches and four flight digits.','H4/H5 and the corrected map still decode HRAFN. Follow H–R–A–F–N on the new flight card: 2, 6, 4, 8. One four-digit lock directly secures H1, the board, pieces, ticket and challenge rules. Release the perch card with H4/H5 after SOLE, outside that pouch. No cryptex or key. See PR-26 and Approved changes.'),
      ('PR-02','Revised · values, not weight','Coin puzzle uses a tally; no scale purchase.','The chosen coins must total 3705 in fictional values. Calculator or four-wheel counter replaces the scale. PR-24 tracks the display choice; PR-25 tracks the coin inventory and selection/value marks.'),
      ('PR-20','Revised · to design','Coin faces and inventory need defined values and selection marks.','Make the selection mark distinct from denomination marks. Supply a merchant’s value key and record exact quantities for reset. Test that the selected set totals 3705. No ballast or calibrated mass is required. Track the remaining work under PR-25.'),
      ('PR-21','Superseded','The five-ring cryptex is retired.','HRAFN remains the decoded answer but now selects four flights for 2648. Use a normal four-digit lock directly on the board pouch. No cryptex model, print or extra keyed closure is required; player-card production is PR-26.')]
    for ident,status,title,body in updates:
        history=old_inside(text,'q-'+ident)
        text=replace_element(text,'q-'+ident,qrow(ident,status,title,body,history))
    newrows=qrow('PR-24','Open','Choose calculator or four-wheel treasure tally.','Both must display 3705 so rotating the whole device reveals SOLE. For wheels, use four independently settable 0–9 drums with stable positions and suitable segmented numerals. Calculator is the simplest prototype; device choice is not yet made.')
    newrows+=qrow('PR-25','Open','Define the coin inventory, fictional values and marks.','Selected coins must sum to 3705. Specify counts, a shared selection mark, separate denomination marks and a merchant’s value key. No historical exchange-rate claim. A1/A3 drafts are in Approved changes; PDFs and gallery backs still need regeneration.')
    newrows+=qrow('PR-26','To print and test','Produce The raven’s flights player card.','The eight-perch, twelve-edge network and 2648 code are approved. Print the player view only, with four blank answer boxes, no HRAFN or answer overlay. Proposed half-Letter size needs proof. Release inside G7, before G8. Exact edges and the accepted visual are in Approved changes.')
    a,b=span(text,'q-PR-21');text=text[:b]+newrows+text[b:]
    # Clearly distinguish retained older chain text from the current replacement.
    a,b=span(text,'q-PZ-17');block=text[a:b]
    block=block.replace('class="qd">','class="qd">'+notice,1)
    text=text[:a]+block+text[b:]

    hoard=dict(key='hoard',refs=['PZ-03','PZ-17','PR-24','PR-25'],trail='aud',state='partial',status='Tally approved · coins and display need proof',title='The hoard and treasure tally',verb='Sort, add &amp; flip',code='SOLE',lock='Dedicated four-letter lock; check dial letters',props=[['Mixed coins, value key and treasure tally','design','prop-hoard']],cards=['A1','A3'],releases='Initial Harald packet: H2/H3/H4/H5/HD, corrected Harald map and The raven’s flights card; retain AD for the finale. Comb remains optional in the reviewed flow.',brief='Add the values of selected coins, display the total and turn it upside down to find a word.',input='Mixed hoard, cache selection mark, merchant’s value key, revised A1/A3, calculator or four-wheel tally.',action='Select the matching coins, count and add their values, record 3705, and rotate the entire tally 180 degrees.',clue='A1 instructs value addition; A3 gives the flip. Replacement paragraphs are in Approved changes; existing print PDFs still use the old copy.',solve='3705 in suitable calculator-style digits reads <b>SOLE</b> upside down. No decimal or discarded digit.',why='Preserves physical sorting and the word reveal without a calibrated scale.',hints=list(HINTS[6][1:]),risk='Coin inventory, values, marks and display choice remain open. Check SOLE on the actual rotated display and update A1/A3 before printing. Former weighing/truncation mechanism is superseded.')
    runes=dict(key='runes',refs=['PZ-02','PZ-09','PR-26'],trail='harald',state='partial',status='Five-perch conversion approved · player print pending',title='Branch runes and the raven’s flights',verb='Decode &amp; follow',code='2648',lock='Four-digit lock directly on the board-kit pouch',props=[['Corrected Harald map and H4/H5','design','prop-runes'],['The raven’s flights card','approved-updates','approved-perches']],cards=['H4','H5'],releases='H1, hnefatafl board, 16 dark pieces, 6 light pieces, king, museum ticket and fixed-piece challenge rules.',brief='Decode five letters, then use them as five perches to read four flight digits.',input='H4/H5, corrected Harald map and player-only perch card; all available before the board lock.',action='Use RAVEN to select map columns; H4 decodes HRAFN. Follow the direct connections H→R→A→F→N and read one digit per flight in that order.',clue='Keep H4’s key and H5’s underlined raven. Perch card: “Follow the five letters you uncovered. Read the number on each flight, in order.”',solve='R6→H, A10→R, V9→A, E3→F, N2→N. Then H→R = 2, R→A = 6, A→F = 4, F→N = 8. Code <b>2648</b>. No translation of HRAFN is required.',why='Keeps the existing cipher and replaces the cryptex with one printable card and a normal lock.',hints=list(HINTS[7][1:]),risk='Use the corrected map: the original E7 decoy creates a second answer. H4/H5 remain unchanged. Perch artwork needs player-only print-size proof; comparison image contains the solution and must not be packed. Former cryptex and key are superseded.')
    text=replace_puzzle(text,'hoard',hoard)
    text=replace_puzzle(text,'runes',runes)
    text=text.replace('Code decided · second lock of Harald’s leg, after the rune cryptex','Code decided · follows the 2648 board-pouch lock')
    text=text.replace('which the rune cryptex already uses','which the rune-and-perch branch already uses')
    text=text.replace('same caveat the cryptex prop note already carries','the supplied key defines the convention for this puzzle')
    text=text.replace('Master four-letter combination lock (owned) — reused after PZ-03’s SOLE, reset to a new combination for this job','Optional separate four-letter lock if restored; do not reset or reuse the SOLE lock during play')
    text=text.replace("status:'Candidate word set · exposed-word mechanism still open'","status:'Optional in reviewed flow · extraction unfinished'")
    text=text.replace("{ref:null,title:'The cryptex',answer:'HRAFN',","{ref:null,title:'The cryptex — superseded',answer:'Retired',")
    text=text.replace('A five-ring cryptex, to print. The answer is settled as <code>HRAFN</code> (raven) and the branch-rune backbone that would produce it is fully worked out','Superseded 22 September 2026. HRAFN now selects four flight digits, 2648, for a direct board-pouch lock. The retained branch-rune backbone is fully worked out')
    text=text.replace("open:'No mechanism has been designed and no container is assigned. Nothing currently outputs five letters.'","open:'No cryptex work remains. Produce and proof the perch card under PR-26.'")
    # Replace only the outdated Aud chain, retaining it in a labelled history disclosure.
    marker='<div class="lockflow"><div class="lf-title">Aud &mdash;'
    start=text.index(marker)
    fragment=text[start:];depth=0;end=None
    for t in re.finditer(r'</?div\b[^>]*>',fragment):
        depth += -1 if t.group().startswith('</') else 1
        if depth==0: end=start+t.end();break
    old=text[start:end]
    chain='''<div class="lockflow"><div class="lf-title">Aud → Harald · approved G7/G8 replacements</div><div class="lf-node">Aud route<br>521</div><div class="lf-arrow">→</div><div class="lf-node">A1/A3 + coins + value key + tally<br>3705 → SOLE</div><div class="lf-arrow">→</div><div class="lf-node">H4/H5 + corrected map + perch card<br>HRAFN → 2648</div><div class="lf-arrow">→</div><div class="lf-node lock">Board kit + H1</div><div class="lf-title">MEAD remains the parallel Harald branch in the reviewed packing plan. The comb is optional there; it must not block the approved SOLE-to-Harald release.</div></div>'''
    text=text[:start]+chain+'<details><summary>Superseded Aud chain · earlier map and comb proposal</summary>'+old+'</details>'+text[end:]
    # Current kit must no longer recommend buying retired hardware.
    text=text.replace('A 3D-printed five-ring cryptex, answer <code>HRAFN</code> decided; its place in the container sequence is still open (<code>PZ-02</code>, <code>ST-01</code>).','The raven’s flights card and one four-digit lock set to 2648 directly on the board pouch. HRAFN is the decoded five-perch itinerary. Cryptex and extra keyed closure are superseded (<code>PZ-02</code>, <code>PR-26</code>).')
    text=text.replace('Replica coins and a small balance with weights.','Mixed coins, a merchant’s fictional value key, and a calculator or four-wheel treasure tally. No scale is required (PR-24/25).')
    text=text.replace('A 7 &times; 7 hnefatafl-inspired board with durable pieces (the throne-compartment idea is dropped — the board is a straightforward bought prop now), its task set by the Oslo postcard rather than a separate rule card. Which board to buy is open (<code>PR-08</code>).','An 11 × 11 printed hnefatafl board with 23 pieces: 16 dark, 6 light and a distinctive king. The user can 3D-print pieces. Supply the fixed-piece three-move challenge rules with H1; no captures or jumps.')
    text=text.replace('Diyife mini digital pocket scale (200g/0.01g)</a> &mdash; used by the coin puzzle, where weight is the ordering rule for the three mint cards. Check first that three replica coins of different metals are close enough in mass to actually need weighing (PR-02).','Diyife mini digital pocket scale (200g/0.01g)</a> &mdash; <strong>superseded, do not buy for this puzzle.</strong> Coin values and a treasure tally replace weighing (PR-24/25).')
    # Reorder the three Harald entries so board setup cannot precede its gate.
    start=text.index("{key:'hnefatafl'")
    # Move only hnefatafl after the mead record, preserving every unrelated field.
    board_end=text.index('\n\n{',start)
    board=text[start:board_end]
    text=text[:start]+text[board_end+2:]
    mead_start=text.index("{key:'mead'")
    mead_end=text.index('\n\n{key:',mead_start)
    text=text[:mead_end]+'\n\n'+board+text[mead_end:]
    BASE.write_text(text,encoding='utf-8')

if __name__=='__main__':
    sync()
    print('Synchronized approved tally/perch design into the base brainstorm.')
