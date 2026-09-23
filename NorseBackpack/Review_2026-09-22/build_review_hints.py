"""Build the review hint companion; puzzle text stays in review_content.py."""
from pathlib import Path
from html import escape
from review_content import HINTS

HERE = Path(__file__).resolve().parent
GROUPS = [('Before the journey', [0]), ('Leif · Across the sea', [1, 2]),
          ('Rollo · Through Normandy', [3, 4]), ('Aud · Into Iceland', [5, 6]),
          ('Harald · Further east', [7, 8, 9]), ('The final journey', [10])]
CUES = ['Postcard & luggage tags', 'Sea chart & museum ticket', 'Two northern postcards',
        'Rouen postcard, ticket & map', 'Chalus, Roumare & Walcheren', 'Museum ticket & Iceland map',
        'Coins, value key & treasure tally', 'Sicily, Hedeby, rune map & perch card', 'Kyiv, Ladoga & Constantinople',
        'Board, map back & museum ticket', 'All four maps, journal & travel tickets']
OPTIONAL = [
    ('Rollo’s rebus cards', 'Bayeux: CROSS + BOW + BOLT. Winchester: TREE + TEA → TREATY. Battle: SCALE + I + TO + FIVE. These identify two map icons and a scale. The review version assigns no distance code; this is an optional discovery.'),
    ('The comb', 'The intended idea is an overlay on the Bjarnarhofn card. Its extraction is not finished in this prototype. It is not required to enter Harald’s stage.')]

def build():
    nav, options, panels = [], [], []
    for group, indices in GROUPS:
        nav.append(f'<div class="nav-group"><p class="group-label">{escape(group)}</p>')
        options.append(f'<optgroup label="{escape(group)}">')
        for i in indices:
            title, *steps = HINTS[i]
            name = title.split(' · ', 1)[1]
            ident = f'g{i+1}'
            nav.append(f'<a href="#{ident}"><span class="nav-number">{i+1:02}</span><span>{escape(name)}</span><span class="nav-arrow" aria-hidden="true">↗</span></a>')
            options.append(f'<option value="{ident}">{i+1:02} · {escape(name)}</option>')
            clues = ''.join(f'<details class="hint"><summary><span class="step">0{j+1}</span><span>Hint {j+1}<small>{["A gentle nudge", "A little more direction", "One last clue"][j]}</small></span><span class="plus" aria-hidden="true"></span></summary><div class="hint-copy"><p>{escape(t)}</p></div></details>' for j, t in enumerate(steps[:3]))
            panels.append(f'''<article id="{ident}" class="puzzle" aria-labelledby="{ident}-title">
<div class="panel-top"><span class="eyebrow">{escape(group)}</span><span class="folio">{i+1:02} / 11</span></div>
<h2 id="{ident}-title" tabindex="-1">{escape(name)}</h2><p class="materials">{escape(CUES[i])}</p>
<div class="hint-stack">{clues}</div>
<details class="solution"><summary><span aria-hidden="true">◇</span> Need the answer?<span class="plus" aria-hidden="true"></span></summary>
<div class="solution-body"><p>This reveals the solution to <strong>{escape(name)}</strong>.</p><button class="reveal" aria-controls="{ident}-answer" aria-expanded="false">Reveal solution <span aria-hidden="true">→</span></button>
<div id="{ident}-answer" class="answer" hidden><p>{escape(steps[3])}</p></div></div></details>
<div class="panel-foot"><span>No rush. Try your idea before opening another hint.</span><button class="close-hints" type="button">Close these hints</button></div></article>''')
        nav.append('</div>')
        options.append('</optgroup>')
    extras = ''.join(f'<details class="hint"><summary><span>{escape(title)}</span><span class="plus" aria-hidden="true"></span></summary><div class="hint-copy"><p>{escape(text)}</p></div></details>' for title, text in OPTIONAL)
    nav.append('<div class="nav-group"><p class="group-label">Off the trail</p><a href="#discoveries"><span class="nav-number">＋</span><span>Optional discoveries</span><span class="nav-arrow" aria-hidden="true">↗</span></a></div>')
    options.append('<option value="discoveries">Optional discoveries</option>')
    panels.append(f'<article id="discoveries" class="puzzle" aria-labelledby="discoveries-title"><div class="panel-top"><span class="eyebrow">Off the trail</span><span class="folio">EXTRA</span></div><h2 id="discoveries-title" tabindex="-1">Optional discoveries</h2><p class="materials">Not needed to complete the review version.</p><div class="hint-stack">{extras}</div><div class="panel-foot"><span>A few loose threads from Liv’s travels.</span><button class="close-hints" type="button">Close these hints</button></div></article>')
    template = (HERE/'hint_companion.template.html').read_text(encoding='utf-8')
    for token, value in [('NAVIGATION', ''.join(nav)), ('OPTIONS', ''.join(options)), ('PANELS', '\n'.join(panels))]:
        template = template.replace('{{'+token+'}}', value)
    (HERE/'Norse_Hints_Review.html').write_text(template, encoding='utf-8')

if __name__ == '__main__':
    build()
    print('Built the 11-puzzle review hint companion.')
