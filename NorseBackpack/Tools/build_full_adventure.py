"""Build NorseBackpack/Full_Adventure.html: the whole Norse adventure on one page, envelope by envelope.

For each envelope: what is inside (images), the puzzle that opens it (logic, solution, hints).
Everything is read from the records (via backpack-kit), so a rebuild picks up record changes.
Printed props are shown from the live print PDFs in NorseBackpack/Print/_pdf_source (rendered to Web/adventure/),
postcards from their asset records.

Run from the repository root:  python NorseBackpack/Tools/build_full_adventure.py
"""
import html
import os
import re
import sys

import pypdfium2 as pdfium

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.abspath(os.path.join(HERE, ".."))          # NorseBackpack/
REPO = os.path.abspath(os.path.join(PROJECT, ".."))           # repository root
sys.path.insert(0, os.path.abspath(os.path.join(REPO, "..", "backpack-kit")))
import kit  # noqa: E402

PDF = os.path.join(PROJECT, "Print", "_pdf_source")
OUT_IMG = os.path.join(PROJECT, "Web", "adventure")
OUT_HTML = os.path.join(PROJECT, "Full_Adventure.html")

# Props shown from the live print PDFs: PP id -> [(label, pdf name, page index)]
PDF_IMAGES = {
    "PP-024": [("Front", "Museum_Ticket_Print", 0), ("Back", "Museum_Ticket_Print", 1)],
    "PP-031": [("Front", "Aud_Ticket_Print", 0), ("Back", "Aud_Ticket_Print", 1)],
    "PP-033": [("Front", "Rouen_Ticket_Print", 0), ("Back", "Rouen_Ticket_Print", 1)],
    "PP-036": [("Front", "Hnefatafl_Ticket_Print", 0), ("Back", "Hnefatafl_Ticket_Print", 1)],
    "PP-035": [("Setup insert", "Hnefatafl_Board_Setup_Insert", 0)],
    "PP-048": [("Names and words · front", "Liv_Notes_Card_Print", 0),
               ("Hints and code formats · back", "Liv_Notes_Card_Print", 1)],
    "PP-038": [("Player card", "Raven_Flights_Card_Print", 0)],
    "PP-043": [("Plane ticket", "Plane_Ticket_Print", 0), ("Letter", "Liv_Final_Letter_Print", 0)],
    "PP-039": [("Nordic Air · 4 tickets · sage paper", "Nordic_Air_Letter_Print", 0),
               ("Nordmark Rail · 6 tickets · coral paper", "Nordmark_Rail_Letter_Print", 0),
               ("Northway Buses · 4 tickets · golden-yellow paper", "Northway_Buses_Letter_Print", 0),
               ("Longship Ferries · 4 tickets · dark-green paper", "Longship_Ferries_Letter_Print", 0)],
    # The three itinerary receipts were dropped 20 Oct 2026 (designer): the hop-ticket dates give the journey order.
    "PP-025": [("Ruler", "Liv_Ruler_Print", 0)],
    "PP-029": [("Map", "Trail_Map_1_Leif_Print", 0)],
    "PP-032": [("Map", "Trail_Map_2_Rollo_Print", 0)],
    "PP-030": [("Map", "Trail_Map_3_Aud_Print", 0)],
    "PP-034": [("Map front", "Trail_Map_4_Harald_Print", 0), ("Map back", "Trail_Map_4_Harald_Print", 1)],
    "PP-047": [("Wheel, assembled", "Cypher_Wheel_Assembled_Preview", 0)],
}
# Props with no asset record and no print PDF: an existing preview image in the project folder
FILE_IMAGES = {
    "PP-028": [("Comb on postcard AD", "Props/Comb/Aud_Comb_on_AD.png")],
    "PP-026": [("SOLE ring check", "Props/SoleTally/SOLE_ring_check.png")],
    "PP-037": [("The coin faces", "Props/Coins/Coin_Faces_Overview.png")],
    "PP-044": [("Medallion v3", "Props/Medallion/Medallion_v3_Preview.png")],
}
DPI = 110

# Print costs tab (Q-052, 20 Oct 2026): stock print-shop products, priced per design from the online quote
# system at 100/250/500/1,000. Same 12 rows, same order as the "Print quotes" tab of Production/Norse_Parts_List.xlsx.
PRINT_QTYS = [25, 50, 100, 250, 500, 1000]
PRINT_PRODUCTS = [  # key, label
    ("pc2", "Postcard 4 × 6 · 2 sides"),
    ("pc1", "Postcard 4 × 6 · 1 side"),
    ("bm2", "Bookmark 2 × 6 · 2 sides"),
    ("bm1", "Bookmark 2 × 6 · 1 side"),
    ("bc1", "Business card 3.5 × 2 · 1 side"),
    ("fl1", "Flyer 5.5 × 8.5 · 14 pt card · 1 side"),
    ("fl2", "Flyer 5.5 × 8.5 · 14 pt card · 2 sides"),
]
# Quotes from the online quote system (Newprint / LoudMouth), designer, 20 Oct 2026: total CAD price for ONE design
# at 100 / 250 / 500 / 1,000. Filled in as the page's default prices; the same numbers are in the xlsx Print quotes tab.
PRINT_QUOTES = {
    "pc2": [65.31, 79.10, 111.80, 182.60],
    "pc1": [55.86, 65.75, 82.30, 124.20],
    "bm2": [62.80, 72.35, 83.00, 102.60],
    "bm1": [60.44, 68.75, 77.30, 93.00],
    "bc1": [39.98, 46.78, 60.15, 83.10],
    "fl1": [None, None, None, None],  # production maps, 5.5 x 8.5 (Q-049, 20 Oct 2026): quotes to come
    "fl2": [None, None, None, None],
}
# Notes kept with a price: the exact print-shop spec behind the number, so it is not lost. Key = product / item key
# (PRINT_PRODUCTS, ENVELOPES, BOXES, MADE). Shown as an editable Notes box on the Print costs page (edits stay in the
# browser; to keep one for good, copy it here).
NOTES = {
    "fl1:old": "Cheapest option:\nShape - Rectangle (Portrait)\nFormat - 5.5 x 8.5 Inches Portrait\n"
           "Paper - 80 lb. Lynx® Uncoated Text FSC® ♽\nColours - Colour Front Side Only\n"
           "Coating - No Coating\nPackaging - Pack Loose in Box",
}
# Superseded 20 Oct 2026 when the production maps moved to 5.5 x 8.5 flyers; kept for reference (prototype prints).
OLD_LETTER_QUOTES = {
    "Letter 8.5 × 11 · 1 side": [73.50, 112.65, 188.20, 314.90],
    "Letter 8.5 × 11 · 2 sides": [87.03, 147.75, 254.80, 433.50],
}
# Packaging (designer, 20 Oct 2026). Envelopes are bought in packs: the page works out the price each from the pack
# size and pack price. Boxes are quoted at 250 / 500 / 1,000 (price each); the page counts the ticked box and uses its
# 250 price for the 100 column. Envelopes per box are Claude's assumption from the 15 envelopes (13 + 2 decoys): the
# four map envelopes (4, 6, 8, 10) and one decoy are 6 x 9; the rest are the small size.
PACK_QTYS = [250, 500, 1000]
ENVELOPES = [  # key, item, per box, items per pack, pack price (CAD), link, note
    ("env69", "6 × 9 clasp envelopes", 5, 300, 45.99, "https://www.amazon.ca/dp/B0H274MFZM",
     "Envelopes 4, 6, 8, 10 + 1 decoy (assumed)"),
    ("envsm", "Small string-tie envelopes 4.5 × 6.7", 10, 20, 18.59, "https://www.amazon.ca/dp/B0DFWX19GS",
     "Prototype pack; 9 envelopes + 1 decoy (assumed)"),
    ("mag", "Magnifier, Fresnel card 3.3 × 2.2 in", 1, 200, 54.37, "https://www.amazon.ca/dp/B0GSD9RKKN",
     "Kronabelle, 200 pcs (PP-027)"),
    ("fast", "Brass fastener (cypher wheel centre)", 1, None, None, "", "PP-047"),
    ("clip", "Small paper clips (treasure tally)", 4, None, None, "", "Paper tally holds digits with 4 clips (PP-026)"),
    ("pawn", "Hnefatafl pieces (19 dark, 6 light, 1 king)", 26, None, None, "",
     "Stock wooden pawns; the king must look different (PP-035)"),
]
# Parts made for us, quoted per order: a one-time setup (for example the cutting die) spread over the quantity,
# plus a price each at 250 / 500 / 1,000. The 100 column uses the 250 price.
MADE = [  # key, item, per box, one-time cost, price each at 250 / 500 / 1,000, link, note
    ("diecut", "Die-cut card sheet: cypher wheel + treasure tally + Aud's comb", 1, None, [None, None, None], "",
     "Wheel disks 196/156/116/76 mm + 202 × 34 mm arm; tally 4 × 2 in sleeve, rails, four 6 in strips; comb 100.7 × 87.8 mm"),
    ("board", "Hnefatafl playing board, 11 × 11 (printed card)", 1, None, [None, None, None], "",
     "Or print it on the box or a flyer back"),
    ("coins", "Coin hoard (12 coins)", 12, None, [None, None, None], "", "3D-printed in the prototype (PP-037)"),
    ("medal", "Adventure medallion, 50 mm", 1, None, [None, None, None], "", "3D-printed in the prototype (PP-044)"),
]
BOXES = [  # key, item, per box, price each at 250 / 500 / 1,000, link, note
    ("boxA", "Sales Presentation Box 11.75 × 1 × 10 in, 18 pt SBS", 1, [None, 3.88, None], "",
     "Newprint; inside/outside size and 1 in depth to check"),
    ("boxB", "Box 10 × 8 × 2 in", 1, [None, None, None], "", ""),
]
# The designer's printable list and sizes, 20 Oct 2026 (Q-052).
PRINT_ITEMS = [  # item, product key, designs per box, record anchor, note
    ("Postcards", "pc2", 22, "PP-001", ""),
    ("Liv's note (QR code + helper on the back)", "pc2", 1, "PP-048", ""),
    ("Final Liv note", "pc1", 1, "PP-043", "One side"),
    ("Museum tickets (Brattahlíð, Aud, Rouen, Oslo)", "bm2", 4, "PP-024", "Size open"),
    ("Raven's path card", "bc1", 1, "PP-038", "Built 20 Oct"),
    ("Travel tickets: hops", "bc1", 18, "PP-039", "Built 20 Oct"),
    ("Travel tickets: final plane ticket", "bc1", 1, "PP-043", "Was 7 × 2.9; not rebuilt"),
    ("Ruler", "bm1", 1, "PP-025", "Built 20 Oct"),
    ("Trail maps (Leif, Rollo, Aud)", "fl1", 3, "PP-029", "Production size; prototype stays Letter"),
    ("Harald's map (board note on the back)", "fl2", 1, "PP-034", "Production size; prototype stays Letter"),
]

e = html.escape


def render_pdfs():
    os.makedirs(OUT_IMG, exist_ok=True)
    made = {}
    for pp, items in PDF_IMAGES.items():
        for label, name, page in items:
            src = os.path.join(PDF, name + ".pdf")
            dest = f"{name}_p{page + 1}.png"
            path = os.path.join(OUT_IMG, dest)
            if not os.path.exists(src):
                continue
            if not os.path.exists(path) or os.path.getmtime(path) < os.path.getmtime(src):
                with pdfium.PdfDocument(src) as d:
                    d[page].render(scale=DPI / 72).to_pil().save(path)
            made[(name, page)] = "Web/adventure/" + dest
    return made


# ---------- tiny markdown ----------

def inline(s):
    s = e(s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", s)
    return s


def md(text):
    text = re.sub(r"~~.+?~~", "", text or "", flags=re.S)
    out, lst, para = [], None, []

    def flush_para():
        if para:
            out.append("<p>" + inline(" ".join(para)) + "</p>")
            para.clear()

    def close_list():
        nonlocal lst
        if lst:
            out.append(f"</{lst}>")
            lst = None

    for ln in text.split("\n"):
        m = re.match(r"^\s*(\d+\.|[-*])\s+(.*)$", ln)
        if m:
            flush_para()
            kind = "ol" if m.group(1)[0].isdigit() else "ul"
            if lst != kind:
                close_list()
                out.append(f"<{kind}>")
                lst = kind
            out.append("<li>" + inline(m.group(2)) + "</li>")
        elif not ln.strip():
            flush_para()
            close_list()
        else:
            close_list()
            para.append(ln.strip())
    flush_para()
    close_list()
    return "\n".join(out)


def paragraphs(text):
    return [p.strip() for p in re.split(r"\n\s*\n", text or "") if p.strip()]


def current_paras(text):
    """Paragraphs without superseded notes and without empty leftovers of struck-through text."""
    keep = []
    for p in paragraphs(text):
        if p.lstrip("*").lower().startswith("superseded"):
            continue
        p = re.sub(r"~~.+?~~", "", p, flags=re.S).strip()
        if p:
            keep.append(p)
    return keep


def summary(body):
    ps = current_paras(kit.md_section(body, "How it works"))
    ps = [p for p in ps if not re.match(r"^(Lock \d+ of|\*\*(9|11) Oct)", p)]
    return ps[0] if ps else ""


# ---------- data ----------

def asset_images(rid, assets):
    imgs = []
    for a in assets:
        if a.get("for") != rid or a.get("superseded_by") or a.get("status") in ("parked", "idea"):
            continue
        f = a.get("file") or ""
        if f and os.path.exists(os.path.join(PROJECT, f)) and f.lower().endswith((".png", ".webp", ".jpg", ".jpeg", ".svg")):
            label = re.sub(r"^.*? (front|back)$", lambda m: m.group(1).capitalize(), a["title"], flags=re.I)
            imgs.append((label if label != a["title"] else a["title"], f))
    return imgs


def prop_figures(p, assets, rendered):
    figs = []
    if p["id"] in PDF_IMAGES:
        for label, name, page in PDF_IMAGES[p["id"]]:
            if (name, page) in rendered:
                figs.append((label, rendered[(name, page)]))
    if not figs and p["id"] in FILE_IMAGES:
        figs = [(l, f) for l, f in FILE_IMAGES[p["id"]] if os.path.exists(os.path.join(PROJECT, f))]
    if not figs:
        figs = asset_images(p["id"], assets)
    return figs


FORM = {"printed": "Printed", "physical": "Physical object", "digital": "Digital"}

TRAVEL_PRINTS = [
    ('Nordic Air', 'sage', 'Print_NordicAir_Flights_Sage_Paper', 'Nordic_Air_Letter_Print'),
    ('Nordmark Rail', 'coral', 'Print_NordmarkRail_Trains_Coral_Paper', 'Nordmark_Rail_Letter_Print'),
    ('Northway Buses', 'golden yellow', 'Print_NorthwayBuses_Yellow_Paper', 'Northway_Buses_Letter_Print'),
    ('Longship Ferries', 'dark green', 'Print_LongshipFerries_Green_Paper', 'Longship_Ferries_Letter_Print'),
]


def prop_html(p, assets, rendered):
    figs = prop_figures(p, assets, rendered)
    title = re.sub(r"^Postcard ", "Postcard ", p["title"])
    h = [f'<article class="prop" id="{p["id"]}"><h4>{e(title)} <span class="id">{p["id"]}</span></h4>']
    if p['id'] == 'PP-048':
        h.append('<p>4 × 6 inch card, two sides: names and words on the front, Liv’s hint QR and all 13 code formats on the back. '
                 'Print at Actual size, duplex, flip on long edge. Test QR scanning and alignment before batch printing.</p>'
                 '<p><a href="Print/Print_LivNotesCard.docx">Word print sheet</a> · '
                 '<a href="Print/_pdf_source/Liv_Notes_Card_Print.pdf" target="_blank" rel="noopener">Open PDF</a></p>')
    if p['id'] == 'PP-039':
        h.append('<p>18 hop tickets, each 3½ × 2 inches, in the matching fancy carrier designs. Print one Letter sheet per carrier, '
                 'single-sided at 100% / actual size on the paper colour shown. Check the one-inch ruler before cutting.</p>')
        h.append('<ul class="travel-prints">')
        for carrier, paper, word, pdf in TRAVEL_PRINTS:
            h.append(f'<li><strong>{e(carrier)}</strong> · {e(paper)} paper · '
                     f'<a href="Print/{word}.docx">Word print sheet</a> · '
                     f'<a href="Print/_pdf_source/{pdf}.pdf" target="_blank" rel="noopener">Open PDF</a></li>')
        h.append('</ul><p class="meta">The previews show the unprinted paper as white. '
                 'Routes, dates and service numbers are preserved. Physical print contrast is untested.</p>')
    if figs:
        h.append('<div class="figs">')
        for label, f in figs:
            h.append(f'<figure><a href="{e(f)}" target="_blank" rel="noopener"><img loading="lazy" src="{e(f)}" alt="{e(title)} {e(label)}"></a>'
                     f'<figcaption>{e(label)}</figcaption></figure>')
        h.append("</div>")
    else:
        h.append(f'<div class="noimg">{e(FORM.get(p.get("form"), "Object"))}: no picture yet</div>')
    h.append(f'<p class="meta">{e(FORM.get(p.get("form"), ""))}{" · " if p.get("form") else ""}{e(p.get("status") or "")}</p>')
    h.append("</article>")
    return "\n".join(h)


def envelope_runes(recs):
    """Envelope number -> runes, from the envelope table in PR-007 (row: | n | `code` | runes | contents |)."""
    out = {}
    for ln in (recs.get("PR-007") or {}).get("body", "").splitlines():
        m = re.match(r"^\|\s*(\d+)\s*\|\s*`[^`]+`\s*\|\s*(\S+)\s*\|", ln)
        if m:
            out[int(m.group(1))] = m.group(2)
    return out


def puzzle_html(pz, n, env_of_prop, recs, cipher_syms, runes):
    uses = []
    for pid in kit.as_list(pz.get("props")):
        pr = recs.get(pid)
        if not pr:
            continue
        where = env_of_prop.get(pid)
        uses.append(f'<a class="chip" href="#{pid}">{e(pr["title"])}'
                    f'<small> · {"on the box" if where == 0 else f"envelope {where}"}</small></a>')
    body = pz["body"]
    logic = [summary(body)]
    for sec, label in (("Player notices", "Players have"), ("Player does", "Players do"), ("Player obtains", "They get")):
        ps = current_paras(kit.md_section(body, sec))
        if ps:
            logic.append(f"**{label}:** " + " ".join(ps))
    story = current_paras(kit.md_section(body, "Story reason"))
    if story:
        logic.append("**Why it is there:** " + " ".join(story))
    hints = kit.list_items(kit.md_section(body, "Hints"))
    solution = kit.md_section(body, "Solution")
    shapes = " ".join(cipher_syms.get(c, "") for c in str(pz.get("answer") or "") if c in cipher_syms)
    answer = pz.get("answer") or ""
    h = [f'<div class="puzzle" id="{pz["id"]}">',
         f'<h3>Puzzle that opens envelope {n}: {e(pz["title"])} <span class="id">{pz["id"]}</span>'
         f'<span class="st st-{e(pz.get("status") or "")}">{e(pz.get("status") or "")}</span></h3>']
    if uses:
        h.append('<p class="uses"><strong>Uses:</strong> ' + " ".join(uses) + "</p>")
    h.append('<div class="logic"><h5>The logic</h5>' + "\n".join(md(x) for x in logic if x) + "</div>")
    if hints:
        h.append('<div class="hints"><h5>Hints, easiest first</h5><ol>')
        for i, t in enumerate(hints, 1):
            h.append(f'<li><details class="spoiler"><summary>Hint {i}</summary><div>{inline(t)}</div></details></li>')
        h.append("</ol></div>")
    h.append('<div class="sol"><details class="spoiler"><summary>Solution and code</summary><div>'
             + md(solution)
             + f'<p class="code">Code: <strong>{e(answer)}</strong> &rarr; wheel runes <span class="runes">{e(runes)}</span> &rarr; envelope {n}</p>'
             + "</div></details></div>")
    h.append("</div>")
    return "\n".join(h)


def money_attr(v):
    return "" if v is None else f"{v:.2f}"


def unit_attr(v):
    """Unit prices keep up to 3 decimals (an envelope at $0.153)."""
    return "" if v is None else f"{v:.3f}".rstrip("0").rstrip(".") if v % 1 else f"{v:.2f}"


def note_cell(key, label, default=None):
    v = NOTES.get(key, "") if default is None else default
    return (f'<td class="note"><textarea rows="2" data-k="{key}:note" data-default="{e(v)}" '
            f'aria-label="{e(label)}, notes" placeholder="Notes">{e(v)}</textarea></td>')


def packaging_html():
    """Envelope and box entry tables, and the total per box (printing at each quantity + envelopes + box)."""
    def num(key, field, value, step, label, attr=money_attr):
        v = attr(value) if value is not None else ""
        return (f'<td><input type="number" min="0" step="{step}" data-k="{key}:{field}" value="{v}" data-default="{v}" '
                f'aria-label="{e(label)}"></td>')

    def link(key, value, item):
        return (f'<td><input type="url" data-k="{key}:link" value="{e(value)}" data-default="{e(value)}" '
                f'placeholder="https://" aria-label="{e(item)}, link"></td>')

    def name(item, value):
        return f'<a data-linkname target="_blank" rel="noopener"{f' href="{e(value)}"' if value else ""}>{e(item)}</a>'

    env_rows = "".join(
        f'<tr data-env="{k}" data-name="{e(item)}"><th scope="row">{name(item, url)}'
        f'{f" <small>{e(note)}</small>" if note else ""}</th>'
        + num(k, "qty", n, 1, f"{item}, per box", str)
        + num(k, "pack", pack, 1, f"{item}, items per pack", str)
        + num(k, "packprice", price, 0.01, f"{item}, pack price")
        + link(k, url, item)
        + '<td class="r" data-each></td><td class="r" data-cost></td>' + note_cell(k, item) + '</tr>'
        for k, item, n, pack, price, url, note in ENVELOPES)
    box_rows = "".join(
        f'<tr data-boxrow="{k}" data-name="{e(item)}"><th scope="row"><label><input type="radio" name="cost-box" value="{k}"'
        f'{" checked" if k == "boxA" else ""} aria-label="Count this box"> </label>{name(item, url)}'
        f'{f" <small>{e(note)}</small>" if note else ""}</th>'
        + num(k, "qty", n, 1, f"{item}, per box", str)
        + "".join(num(k, f"p{q}", prices[i], 0.01, f"{item}, price each at {q:,}") for i, q in enumerate(PACK_QTYS))
        + link(k, url, item) + note_cell(k, item) + "</tr>"
        for k, item, n, prices, url, note in BOXES)
    made_rows = "".join(
        f'<tr data-made="{k}" data-name="{e(item)}"><th scope="row">{name(item, url)}'
        f'{f" <small>{e(note)}</small>" if note else ""}</th>'
        + num(k, "qty", n, 1, f"{item}, per box", str)
        + num(k, "setup", setup, 0.01, f"{item}, one-time cost")
        + "".join(num(k, f"p{q}", prices[i], 0.01, f"{item}, price each at {q:,}") for i, q in enumerate(PACK_QTYS))
        + link(k, url, item) + note_cell(k, item) + "</tr>"
        for k, item, n, setup, prices, url, note in MADE)
    pqh = "".join(f'<th class="r">Each @{q:,}</th>' for q in PACK_QTYS)
    qh = "".join(f'<th class="r">@{q:,}</th>' for q in PRINT_QTYS)
    grand = "".join(
        f'<tr{cls}><th scope="row">{label}</th>' + "".join(f'<td class="r" data-{g}="{q}"></td>' for q in PRINT_QTYS) + "</tr>"
        for g, label, cls in (("g1", "Printing per box", ""), ("g2", "Bought in packs", ""),
                              ("g5", "Box <small>(ticked; the 100 column uses its 250 price)</small>", ""),
                              ("g6", "Made parts <small>(one-time costs spread over the quantity)</small>", ""),
                              ("g3", "Total per box", ' class="tot"'), ("g4", "Prices still missing", ' class="miss"')))
    return (
        '<h3 class="inside">4 · Bought in packs (envelopes, magnifier, small parts)</h3>'
        '<div class="tbl"><table class="cost pack"><thead><tr><th>Item</th><th class="r">Per box</th>'
        '<th class="r">Items per pack</th><th class="r">Pack price</th><th>Link</th><th class="r">Price each</th>'
        '<th class="r">Cost per box</th><th>Notes</th></tr></thead><tbody>' + env_rows + '</tbody><tfoot><tr class="tot"><th scope="row">'
        'Bought in packs, per box</th><td></td><td></td><td></td><td></td><td></td><td class="r" id="cost-env"></td><td></td></tr></tfoot></table></div>'
        '<h3 class="inside">5 · Box (quotes, price each; tick the one to count)</h3>'
        f'<div class="tbl"><table class="cost pack"><thead><tr><th>Box</th><th class="r">Per box</th>{pqh}<th>Link</th><th>Notes</th></tr></thead>'
        '<tbody>' + box_rows + '</tbody></table></div>'
        '<h3 class="inside">6 · Made parts (quotes: one-time setup + price each)</h3>'
        f'<div class="tbl"><table class="cost pack"><thead><tr><th>Part</th><th class="r">Per box</th><th class="r">One-time</th>{pqh}<th>Link</th><th>Notes</th></tr></thead>'
        '<tbody>' + made_rows + '</tbody></table></div>'
        '<h3 class="inside">7 · Total per box (printing + bought + box + made parts)</h3>'
        f'<div class="tbl"><table class="cost"><thead><tr><th></th>{qh}</tr></thead><tbody>{grand}</tbody></table></div>'
        '<p class="meta">Not yet here: rune stamps and ink, mailer bag, shipping, fees.</p>')


PLAN_MD = os.path.join(PROJECT, "Production", "Kickstarter_Plan.md")
PARTS_XLSX = os.path.join(PROJECT, "Production", "Norse_Parts_List.xlsx")
# Kickstarter plan sections shown on the Production tab; every other section goes on the Next steps tab.
PLAN_PRODUCTION = ("Phase 2", "How many copies", "Phase 5")


def inline_l(s):
    """inline() plus [text](https://...) links."""
    return re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)",
                  r'<a href="\2" target="_blank" rel="noopener">\1</a>', inline(s))


def md_doc(text):
    """Markdown for the Kickstarter plan: ### headings, tables, lists, paragraphs, links."""
    out, lst, para, table = [], None, [], []

    def flush():
        nonlocal lst
        if para:
            out.append("<p>" + inline_l(" ".join(para)) + "</p>")
            para.clear()
        if lst:
            out.append(f"</{lst}>")
            lst = None
        if table:
            rows = [[c.strip() for c in r.strip().strip("|").split("|")] for r in table
                    if not re.match(r"^\s*\|[\s:|-]+\|\s*$", r)]
            head, body = rows[0], rows[1:]
            out.append('<div class="tbl"><table class="plan"><thead><tr>'
                       + "".join(f"<th>{inline_l(c)}</th>" for c in head) + "</tr></thead><tbody>"
                       + "".join("<tr>" + "".join(f"<td>{inline_l(c)}</td>" for c in r) + "</tr>" for r in body)
                       + "</tbody></table></div>")
            table.clear()

    for ln in text.split("\n"):
        if ln.lstrip().startswith("|"):
            if para or lst:
                flush()
            table.append(ln)
            continue
        m = re.match(r"^\s*(\d+\.|[-*])\s+(.*)$", ln)
        h = re.match(r"^(#{3,4})\s+(.*)$", ln)
        if h:
            flush()
            out.append(f'<h3 class="plan-h">{inline_l(h.group(2))}</h3>')
        elif m:
            kind = "ol" if m.group(1)[0].isdigit() else "ul"
            if table or para or (lst and lst != kind):
                flush()
            if not lst:
                out.append(f"<{kind}>")
                lst = kind
            out.append("<li>" + inline_l(m.group(2)) + "</li>")
        elif not ln.strip() or ln.strip() == "---":
            flush()
        else:
            if table or lst:
                flush()
            para.append(ln.strip())
    flush()
    return "\n".join(out)


def plan_sections():
    """The Kickstarter plan split on '## ': [(title, markdown body)], the preamble first."""
    with open(PLAN_MD, encoding="utf-8") as f:
        parts = re.split(r"^## ", f.read(), flags=re.M)
    return [(p.split("\n", 1)[0].strip(), p.split("\n", 1)[1] if "\n" in p else "") for p in parts[1:]], parts[0]


def plan_details(items, open_first=False):
    return "".join(
        f'<details class="plan"{" open" if open_first and i == 0 else ""}><summary>{inline_l(t)}</summary>'
        f'<div>{md_doc(b)}</div></details>' for i, (t, b) in enumerate(items))


def parts_html():
    """The component list from Production/Norse_Parts_List.xlsx (Parts list tab), read only."""
    import openpyxl
    ws = openpyxl.load_workbook(PARTS_XLSX, data_only=False)["Parts list"]
    rows = [r for r in ws.iter_rows(min_row=2, values_only=True) if r[1]]
    cols = [(0, "Envelope"), (1, "Item"), (2, "Record"), (3, "Qty"), (4, "Prototype now"),
            (5, "Production idea"), (6, "Size / spec"), (7, "Status / open")]

    def cell(i, v):
        v = "" if v is None else str(v)
        if i == 2 and re.match(r"^PP-\d+$", v):
            return f'<a href="#{v}">{v}</a>'
        return e(v)

    body = "".join("<tr>" + "".join(f"<td>{cell(i, r[i])}</td>" for i, _ in cols) + "</tr>" for r in rows)
    return (f'<div class="tbl"><table class="plan parts"><thead><tr>'
            + "".join(f"<th>{h}</th>" for _, h in cols) + f"</tr></thead><tbody>{body}</tbody></table></div>"
            f'<p class="meta">{len(rows)} lines from <code>Production/Norse_Parts_List.xlsx</code> (Parts list tab). '
            'Unit prices at 500 and 1,000 are blank there until quotes arrive.</p>')


def production_html(plan):
    return (
        '<section class="env" id="production"><header><span class="num">$</span><div><h2>Production</h2>'
        '<p>What it costs to make a box and what it is made of. Quotes so far: the print shops (Newprint, LoudMouth) and a few '
        'listed prices; everything else is still to be quoted.</p></div></header>'
        '<h3 class="inside">Components</h3>' + parts_html() + "</section>"
        + costs_html()
        + '<section class="env" id="plan-production"><header><span class="num">…</span><div><h2>Making it</h2>'
        '<p>From the Kickstarter plan (a plan, not a decision; ballpark prices are guesses, not quotes).</p></div></header>'
        + plan_details(plan, open_first=True) + "</section>")


def next_steps_html(plan, preamble, recs):
    open_q = [recs[i] for i in ("Q-064", "Q-063", "Q-053", "Q-054") if i in recs and recs[i]["status"] == "open"]
    qs = "".join(
        f'<article class="prop"><h4>{e(q["title"])} <span class="id">{q["id"]}</span></h4>'
        + md("\n\n".join(current_paras(q["body"])[:2])) + "</article>" for q in open_q)
    intro = preamble.split("\n\n", 1)[1].split("\n\n", 1)[0] if "\n\n" in preamble else ""
    return (
        '<section class="env" id="nextsteps"><header><span class="num">→</span><div><h2>Next steps</h2>'
        f'<p>{inline_l(intro)}</p></div></header>'
        + plan_details(plan[:1], open_first=True) + "</section>"
        + '<section class="env" id="outreach"><header><span class="num">?</span><div><h2>Playtesting and open questions</h2>'
        '<p>Open records that block or shape the next playtests. The full wording is in the records.</p></div></header>'
        f'<div class="props">{qs}</div></section>'
        + '<section class="env" id="plan"><header><span class="num">…</span><div><h2>The full plan</h2>'
        '<p>Phases, playtest rounds, pre-launch, the campaign, awards, wording and risks.</p></div></header>'
        + plan_details(plan[1:]) + "</section>")


SHOPS = [  # key, name, where, link, note (29 Oct 2026; shops other than "old" are leads from a web search, no quotes yet)
    ("old", "Existing quotes (Newprint or LoudMouth)", "Online / Ottawa", "",
     "Quotes entered 20 Oct 2026 from the online quote systems; which shop each row came from was not recorded. "
     "Move them to Newprint or LoudMouth once known."),
    ("newprint", "Newprint", "Ottawa, online", "", "Box quote also from Newprint"),
    ("loudmouth", "LoudMouth", "Ottawa", "", "Starts at 100 copies (designer, 29 Oct 2026); may be cheaper than Newprint at small runs"),
    ("asap", "ASAP PM", "Ottawa, pickup", "", "Advertises small runs and quick turnaround; on the quote list in the plan"),
    ("eprint", "ePrint It", "Ottawa, 580 Booth St", "", "Online printing with flyers; to quote"),
    ("allegra", "Allegra Ottawa Downtown", "Ottawa, pickup", "https://www.allegramarketingprint.com/locations/ottawa-downtown/services/print/flyers",
     "Chain shop; one quote to compare"),
    ("vista", "Vistaprint Canada", "Online, ships", "", "Often cheapest per piece online (a competitor's comparison); check shipping and delivery time"),
    ("pcloud", "Printcloud", "Online, ships in Canada", "", "Not verified; to quote"),
    ("other", "Other shop", "", "", ""),
]
OLD_QTYS = [100, 250, 500, 1000]  # the quantities of the 20 Oct 2026 quotes (PRINT_QUOTES order)


def field(key, value, label, kind="text", extra=""):
    return (f'<td><input type="{kind}" {extra} data-k="{key}" value="{e(value)}" data-default="{e(value)}" '
            f'aria-label="{e(label)}"></td>')


def quote_block(key, label):
    old = dict(zip(OLD_QTYS, PRINT_QUOTES[key]))
    rows = []
    for sk, sname, where, link, snote in SHOPS:
        cells = "".join(
            f'<td><input type="number" min="0" step="0.01" inputmode="decimal" data-p="{key}" data-q="{q}" '
            f'data-k="{key}:{sk}:{q}" value="{money_attr(old.get(q) if sk == "old" else None)}" '
            f'data-default="{money_attr(old.get(q) if sk == "old" else None)}" '
            f'aria-label="{e(label)}, {e(sname)}, total price for {q:,}"></td>' for q in PRINT_QTYS)
        rows.append(
            f'<tr data-qr="{key}" data-shop="{sk}" data-sname="{e(sname)}"><th scope="row">{e(sname)}</th>{cells}'
            + field(f"{key}:{sk}:ship", "", f"{label}, {sname}, shipping", "number",
                    'min="0" step="0.01" inputmode="decimal" data-ship placeholder="0"')
            + field(f"{key}:{sk}:date", "", f"{label}, {sname}, quote date", "text", 'placeholder="date"')
            + field(f"{key}:{sk}:link", "", f"{label}, {sname}, quote link", "url", 'placeholder="https://"')
            + note_cell(f"{key}:{sk}", f"{label}, {sname}") + "</tr>")
    qh = "".join(f'<th class="r">@{q:,}</th>' for q in PRINT_QTYS)
    best = "".join(f'<td class="r" data-best="{key}:{q}"></td>' for q in PRINT_QTYS)
    return (f'<details class="plan prodq" open><summary>{e(label)}</summary><div><div class="tbl"><table class="cost quotes">'
            f'<thead><tr><th>Shop</th>{qh}<th class="r">Shipping</th><th>Quote date</th><th>Link</th>'
            f'<th>Spec (paper, finish, packaging…)</th></tr></thead><tbody>{"".join(rows)}</tbody>'
            f'<tfoot><tr class="bestrow"><th scope="row">Cheapest</th>{best}<td colspan="4"></td></tr></tfoot></table></div></div></details>')


def costs_html():
    """The Print costs tab: shops, a quote per shop and product, cost per box worked out in the page (script below)."""
    qh = "".join(f'<th class="r">@{q:,}</th>' for q in PRINT_QTYS)
    shop_rows = "".join(
        f'<tr><th scope="row"><label><input type="checkbox" data-inc="{k}" checked aria-label="Count {e(name)} in the cheapest"> '
        f'{e(name)}</label></th>'
        + field(f"shop:{k}:where", where, f"{name}, where")
        + field(f"shop:{k}:link", link, f"{name}, website", "url", 'placeholder="https://"')
        + note_cell(f"shop:{k}", name, note) + "</tr>"
        for k, name, where, link, note in SHOPS)
    quotes = "".join(quote_block(key, label) for key, label in PRINT_PRODUCTS)
    label_of = dict(PRINT_PRODUCTS)
    items = "".join(
        f'<tr data-p="{key}" data-n="{n}"><th scope="row">'
        + (f'<a href="#{rid}">{e(item)}</a>' if rid else e(item))
        + (f' <small>{e(note)}</small>' if note else "")
        + f'</th><td>{e(label_of[key])}</td><td class="r">{n}</td>'
        + "".join(f'<td class="r" data-q="{q}"></td>' for q in PRINT_QTYS) + "</tr>"
        for item, key, n, rid, note in PRINT_ITEMS)
    foot = ('<tr class="tot"><th scope="row">Printing per box</th><td></td><td class="r" id="cost-pieces"></td>'
            + "".join(f'<td class="r" data-tot="{q}"></td>' for q in PRINT_QTYS) + "</tr>"
            + '<tr class="tot2"><th scope="row">Whole print order (per box × quantity)</th><td></td><td></td>'
            + "".join(f'<td class="r" data-order="{q}"></td>' for q in PRINT_QTYS) + "</tr>"
            + '<tr class="miss"><th scope="row">Rows without a price</th><td></td><td></td>'
            + "".join(f'<td class="r" data-miss="{q}"></td>' for q in PRINT_QTYS) + "</tr>")
    whole = "".join(
        f'<tr><th scope="row">{e(name)}</th>' + "".join(f'<td class="r" data-shopq="{k}:{q}"></td>' for q in PRINT_QTYS) + "</tr>"
        for k, name, where, link, note in SHOPS)
    mode = '<option value="">Cheapest shop for each item</option>' + "".join(
        f'<option value="{k}">Only {e(name)}</option>' for k, name, *_ in SHOPS)
    return (
        '<section class="env" id="costs"><header><span class="num">$</span>'
        '<div><h2>Print costs</h2><p>Each price is the <b>total for one design</b> from a shop\'s quote system, in CAD. '
        'Enter a quote for any shop and quantity; the page takes the cheapest for each item and works out the cost per box '
        '(designs per box × price ÷ quantity). Shipping is a flat amount per quote; tick HST to add 13%. '
        'Edits stay in this browser only (<i>Reset to quotes</i> brings back the 20 Oct 2026 quotes). '
        'Notes and specs are kept with each quote so the exact product is not lost.</p></div></header>'
        '<h3 class="inside">1 · Shops <small>(untick one to leave it out of the cheapest)</small></h3>'
        '<div class="tbl"><table class="cost shops"><thead><tr><th>Shop</th><th>Where</th><th>Website</th><th>Notes</th></tr></thead>'
        f'<tbody>{shop_rows}</tbody></table></div>'
        '<h3 class="inside">2 · Quotes per product and shop (CAD, total for one design)</h3>'
        + quotes +
        '<h3 class="inside" id="cost-perbox">3 · Cost per box</h3>'
        f'<div class="costbar"><label>Compare using <select id="cost-mode">{mode}</select></label>'
        '<label><input type="checkbox" id="cost-hst"> Add 13% HST (prices above are before tax)</label></div>'
        f'<div class="tbl"><table class="cost"><thead><tr><th>Item</th><th>Product</th><th class="r">Designs per box</th>{qh}</tr></thead>'
        f'<tbody>{items}</tbody><tfoot>{foot}</tfoot></table></div>'
        '<h3 class="inside">Printing per box if everything came from one shop</h3>'
        f'<div class="tbl"><table class="cost"><thead><tr><th>Shop</th>{qh}</tr></thead><tbody>{whole}</tbody></table></div>'
        '<div class="costbar"><button id="cost-copy-notes">Copy all notes</button><span id="cost-msg-notes" class="meta"></span>'
        '<button id="cost-clear">Reset to quotes</button><span id="cost-msg" class="meta"></span></div>'
        + '<p class="meta">Superseded Letter 8.5 × 11 quotes, kept for reference (prototype maps): '
        + "; ".join(f'{e(k)}: ' + " / ".join(f"${v:.2f}" for v in vals) for k, vals in OLD_LETTER_QUOTES.items())
        + ' (at 100 / 250 / 500 / 1,000).</p>'
        + packaging_html() +
        '<p class="meta">Pick the column for the print run: base case about 300 backers ≈ 350 boxes. Compare whole orders: '
        'one order of 500 can cost less than 250 + 100. '
        'Assumes each design is its own order of that quantity; if the shop lets several designs share one order, the cost per box '
        'drops. Museum ticket size is still open (2 × 6 proposed, Q-052). Not here: hnefatafl board, repacking letter, die-cut parts, envelopes, box.</p>'
        "</section>")


def build():
    data = kit.load(PROJECT)
    recs = {r["id"]: r for r in data["records"]}
    assets = [r for r in data["records"] if r["type"] == "asset"]
    rendered = render_pdfs()
    cipher_syms = (data.get("cipher") or {}).get("symbols", {})
    envs = data["envelopes"]["envelopes"]
    start = data["envelopes"]["start"]

    env_of_prop = {pid: 0 for pid in start}
    for i, env in enumerate(envs, 1):
        for pid in env["contents"]:
            env_of_prop[pid] = i

    title = data["config"].get("name", "Norse Backpack")
    rmap = envelope_runes(recs)
    nav = ['<a href="#box" data-tab="design">The box</a>'] + [
        f'<a href="#env{i}" data-tab="design"><b>{i}</b> <span>{e(rmap.get(i, ""))}</span></a>' for i, env in enumerate(envs, 1)]         + ['<a href="#production" data-tab="production"><b>$</b> Components</a>',
           '<a href="#costs" data-tab="production" class="navcost"><b>$</b> Print costs</a>',
           '<a href="#plan-production" data-tab="production"><b>…</b> Making it</a>',
           '<a href="#nextsteps" data-tab="next"><b>→</b> Next steps</a>',
           '<a href="#outreach" data-tab="next"><b>?</b> Open questions</a>',
           '<a href="#plan" data-tab="next"><b>…</b> Full plan</a>']

    sections = []
    # The box, before any envelope
    sections.append('<section class="env" id="box"><header><span class="num">Box</span>'
                    '<div><h2>On top of the box</h2><p>Loose on the lid before any envelope is opened. '
                    'Postcard L1 and the wheel start the first code (a worked example).</p></div></header>'
                    '<h3 class="inside">Inside</h3><div class="props">'
                    + "\n".join(prop_html(recs[pid], assets, rendered) for pid in start)
                    + "</div></section>")
    for i, env in enumerate(envs, 1):
        pz = recs[env["puzzle"]]
        props = "\n".join(prop_html(recs[pid], assets, rendered) for pid in env["contents"])
        sections.append(
            f'<section class="env" id="env{i}"><header><span class="num">{i}</span>'
            f'<div><h2>Envelope {i} <span class="runes">{e(rmap.get(i, ""))}</span></h2>'
            f'<p>Opens when players set the code from <a href="#{pz["id"]}">{e(pz["title"])}</a> on the wheel.</p></div></header>'
            f'<h3 class="inside">Inside</h3><div class="props">{props}</div>'
            + puzzle_html(pz, i, env_of_prop, recs, cipher_syms, rmap.get(i, ""))
            + "</section>")
    plan, preamble = plan_sections()
    plan_prod = [x for x in plan if x[0].startswith(PLAN_PRODUCTION)]
    plan_next = [x for x in plan if not x[0].startswith(PLAN_PRODUCTION)]
    body = ('<div class="tab" id="tab-design" data-tab="design">' + "\n".join(sections) + "</div>"
            '<div class="tab" id="tab-production" data-tab="production" hidden>' + production_html(plan_prod) + "</div>"
            '<div class="tab" id="tab-next" data-tab="next" hidden>' + next_steps_html(plan_next, preamble, recs) + "</div>")

    page = TEMPLATE.replace("{{TITLE}}", e(title)).replace("{{BUILT}}", e(data["builtAt"])) \
        .replace("{{NAV}}", "\n".join(nav)).replace("{{BODY}}", body) \
        .replace("{{COUNT}}", str(len(envs)))
    with open(OUT_HTML, "w", encoding="utf-8") as f:
        f.write(page)
    print(f"Wrote {OUT_HTML} ({len(envs)} envelopes, {len(rendered)} rendered pages)")


TEMPLATE = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>The Raven Inheritance: the full adventure</title>
<style>
:root{--bg:#f4efe3;--card:#fffaf0;--ink:#1f2a26;--mute:#5d6a63;--rule:#d9cfb8;--accent:#2f5d4e;--rust:#a8561f;--spoil:#efe3c4}
@media (prefers-color-scheme:dark){:root{--bg:#161b19;--card:#1f2623;--ink:#ece6d6;--mute:#a4aea8;--rule:#35403b;--accent:#7fc3a9;--rust:#e0955a;--spoil:#2b342f}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.55 system-ui,"Segoe UI",sans-serif}
.wrap{display:grid;grid-template-columns:150px 1fr;max-width:1900px;margin:0 auto}
nav{position:sticky;top:0;align-self:start;height:100vh;overflow:auto;padding:16px 10px;border-right:1px solid var(--rule)}
nav a{display:block;padding:5px 8px;border-radius:6px;color:var(--ink);text-decoration:none;font-size:14px}
nav a:hover{background:var(--spoil)}
nav a b{display:inline-block;min-width:1.6em;color:var(--accent)}
nav a span{color:var(--mute);font-size:12px;letter-spacing:.05em}
main{padding:0 24px 80px;min-width:0}
.top{padding:28px 0 10px}
.top h1{margin:0;font-size:30px}
.top p{color:var(--mute);margin:6px 0}
.bar{position:sticky;top:0;z-index:5;background:var(--bg);padding:10px 0;border-bottom:1px solid var(--rule);display:flex;gap:10px;flex-wrap:wrap;align-items:center}
button{font:inherit;padding:6px 12px;border:1px solid var(--accent);background:transparent;color:var(--accent);border-radius:8px;cursor:pointer}
button:hover{background:var(--accent);color:var(--bg)}
.env{margin-top:36px;padding:20px;background:var(--card);border:1px solid var(--rule);border-radius:14px;scroll-margin-top:60px}
.env>header{display:flex;gap:16px;align-items:center;margin-bottom:6px}
.num{flex:none;min-width:54px;height:54px;padding:0 8px;border-radius:50%;background:var(--accent);color:var(--bg);display:grid;place-items:center;font-weight:700;font-size:22px}
a{color:var(--accent)}
h2{margin:0;font-size:24px}
.env>header p{margin:2px 0 0;color:var(--mute)}
.runes{font-family:"Segoe UI Historic","Noto Sans Runic",serif;letter-spacing:.12em;color:var(--rust)}
h3{margin:22px 0 8px;font-size:18px}
h3.inside{font-size:13px;text-transform:uppercase;letter-spacing:.1em;color:var(--mute)}
h4{margin:0 0 8px;font-size:15px}
h5{margin:0 0 6px;font-size:12px;text-transform:uppercase;letter-spacing:.1em;color:var(--mute)}
.id{font-weight:400;font-size:11px;color:var(--mute);margin-left:6px}
.st{margin-left:8px;font-size:11px;padding:1px 8px;border-radius:99px;border:1px solid var(--rule);color:var(--mute);font-weight:400}
.props{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:14px}
.prop{border:1px solid var(--rule);border-radius:10px;padding:12px;background:var(--bg)}
#PP-039{grid-column:1/-1;scroll-margin-top:100px}
#PP-039 .figs{grid-template-columns:repeat(auto-fit,minmax(230px,1fr))}
.figs{display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:8px}
figure{margin:0}
figure img{width:100%;height:auto;display:block;border-radius:6px;border:1px solid var(--rule);background:#fff}
figcaption{font-size:12px;color:var(--mute);text-align:center;margin-top:3px}
.noimg{padding:22px 10px;text-align:center;color:var(--mute);border:1px dashed var(--rule);border-radius:8px;font-size:13px}
.meta{margin:8px 0 0;font-size:12px;color:var(--mute)}
.puzzle{margin-top:24px;padding-top:6px;border-top:2px solid var(--rule)}
.logic{background:var(--bg);border-radius:10px;padding:12px 16px;margin:10px 0}
.logic p{margin:6px 0}
.uses{margin:6px 0;font-size:14px}
.chip{display:inline-block;margin:2px 4px 2px 0;padding:2px 10px;border:1px solid var(--rule);border-radius:99px;color:var(--ink);text-decoration:none;font-size:13px}
.chip small{color:var(--mute)}
.chip:hover{border-color:var(--accent)}
.hints ol{margin:0;padding-left:22px}
details.spoiler{margin:4px 0;border:1px solid var(--rule);border-radius:8px;background:var(--spoil)}
details.spoiler>summary{cursor:pointer;padding:6px 12px;color:var(--accent);font-weight:600}
details.spoiler>div{padding:4px 14px 10px}
details.spoiler>div p{margin:6px 0}
.sol{margin-top:10px}
.code{padding:8px 12px;border-radius:8px;background:var(--bg)}
code{background:var(--spoil);padding:0 4px;border-radius:4px}
nav a.navcost{margin-top:8px;border-top:1px solid var(--rule);border-radius:0 0 6px 6px}
.tbl{overflow-x:auto}
table.cost{border-collapse:collapse;width:100%;font-size:14px;font-variant-numeric:tabular-nums}
table.cost th,table.cost td{padding:5px 8px;border-bottom:1px solid var(--rule);text-align:left;vertical-align:middle}
table.cost thead th{font-size:12px;text-transform:uppercase;letter-spacing:.06em;color:var(--mute);font-weight:600}
table.cost tbody th{font-weight:500}
table.cost.prices tbody th{white-space:nowrap;width:1%}
table.cost small{color:var(--mute);font-size:11px}
table.cost .r{text-align:right}
table.cost input{width:100%;min-width:76px;font:inherit;text-align:right;padding:4px 6px;border:1px solid var(--rule);border-radius:6px;background:var(--bg);color:var(--ink)}
table.cost textarea{width:100%;min-width:230px;font:inherit;font-size:13px;line-height:1.35;padding:4px 6px;border:1px solid var(--rule);border-radius:6px;background:var(--bg);color:var(--ink);resize:vertical}
table.cost textarea:focus,table.cost input:focus{outline:2px solid var(--accent);outline-offset:0}
table.cost input:focus{outline:2px solid var(--accent);outline-offset:0}
table.cost input[type=checkbox]{width:auto;min-width:0;accent-color:var(--accent);margin:0 4px 0 0}
table.cost.quotes input[type=number]{min-width:64px}
table.cost.quotes input[type=text],table.cost.quotes input[type=url],table.cost.shops input[type=text],table.cost.shops input[type=url]{text-align:left;min-width:110px}
table.cost input.bestc{border-color:var(--accent);background:var(--spoil);font-weight:700}
table.cost tr.bestrow th,table.cost tr.bestrow td{font-weight:700;border-top:2px solid var(--ink);font-size:12px}
details.prodq>div{padding:0 0 6px}
.costbar label{display:flex;gap:6px;align-items:center;font-size:14px}
.costbar select{font:inherit;padding:4px 6px;border:1px solid var(--rule);border-radius:6px;background:var(--bg);color:var(--ink)}
table.cost tr.tot th,table.cost tr.tot td{font-weight:700;border-top:2px solid var(--ink)}
table.cost tr.off th,table.cost tr.off td{opacity:.45}
table.cost.pack input[type=number]{max-width:96px}
table.cost.pack input[type=url]{min-width:150px}
a.nolink{color:var(--ink);text-decoration:none;cursor:default}
table.cost.pack input[type=radio]{accent-color:var(--accent);margin:0 4px 0 0}
table.cost tr.tot2 th,table.cost tr.tot2 td{font-weight:600;color:var(--mute)}
table.cost tr.miss th,table.cost tr.miss td{color:var(--mute);font-size:12px;font-weight:400}
.costbar{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin-top:12px}
.costbar .meta{margin:0}
.tabs{display:flex;gap:8px;margin:10px 0 0}
.tabs button{padding:8px 18px;font-weight:600}
.tabs button[aria-selected=true]{background:var(--accent);color:var(--bg)}
.tab[hidden]{display:none}
table.plan{border-collapse:collapse;width:100%;font-size:14px;margin:8px 0}
table.plan th,table.plan td{border:1px solid var(--rule);padding:5px 8px;text-align:left;vertical-align:top}
table.plan th{background:var(--spoil);font-size:12px;text-transform:uppercase;letter-spacing:.06em}
table.parts{font-size:13px}
details.plan{border:1px solid var(--rule);border-radius:10px;margin:10px 0;background:var(--bg)}
details.plan>summary{cursor:pointer;padding:10px 14px;font-weight:600}
details.plan>div{padding:0 16px 10px}
h3.plan-h{font-size:16px}
@media(max-width:760px){.wrap{display:block}nav{display:none}main{padding:0 14px 60px}}
@media print{nav,.bar{display:none}.wrap{display:block}details.spoiler:not([open])>div{display:block}.env{break-inside:avoid-page}}
</style></head><body>
<div class="wrap"><nav>
{{NAV}}
</nav>
<main>
<div class="top"><h1>{{TITLE}}: the full adventure</h1>
<p>Designer copy with spoilers. <b>Design:</b> envelope by envelope, what is inside, the puzzle that opens it, its logic, hints and solution ({{COUNT}} envelopes). <b>Production:</b> components, print costs, how it gets made. <b>Next steps:</b> playtesting, quotes, launch plan. Built from the records, {{BUILT}}.</p></div>
<div class="tabs" role="tablist"><button data-go="design" role="tab">Design</button><button data-go="production" role="tab">Production</button><button data-go="next" role="tab">Next steps</button></div>
<div class="bar" id="designbar"><button id="open">Open all hints and solutions</button><button id="close">Close all</button>
<span class="mute" style="color:var(--mute);font-size:13px">Hints and solutions are folded until you open them.</span></div>
{{BODY}}
</main></div>
<script>
(function(){
var tabs=document.querySelectorAll('.tab'),btns=document.querySelectorAll('.tabs button'),links=document.querySelectorAll('.wrap>nav a'),bar=document.getElementById('designbar');
function show(name){tabs.forEach(function(t){t.hidden=t.getAttribute('data-tab')!==name});
  btns.forEach(function(b){b.setAttribute('aria-selected',b.getAttribute('data-go')===name)});
  links.forEach(function(a){a.style.display=a.getAttribute('data-tab')===name?'':'none'});
  bar.style.display=name==='design'?'':'none'}
function fromHash(){var id=decodeURIComponent(location.hash.slice(1)),el=id&&document.getElementById(id),t=el&&el.closest('.tab');
  show(t?t.getAttribute('data-tab'):(window.__tab||'design'));if(el)el.scrollIntoView()}
btns.forEach(function(b){b.onclick=function(){window.__tab=b.getAttribute('data-go');history.replaceState(null,'',location.pathname);show(window.__tab);window.scrollTo(0,0)}});
window.addEventListener('hashchange',fromHash);fromHash();
})();
var all=function(){return document.querySelectorAll('details.spoiler')};
document.getElementById('open').onclick=function(){all().forEach(function(d){d.open=true})};
document.getElementById('close').onclick=function(){all().forEach(function(d){d.open=false})};
(function(){
var root=document.getElementById('costs');if(!root)return;
var KEY='norse-print-prices-v2',saved={};
try{saved=JSON.parse(localStorage.getItem(KEY)||'{}')||{}}catch(err){saved={}}
var inputs=root.querySelectorAll('input[data-p],input[data-k],textarea[data-k]'),rows=root.querySelectorAll('tbody tr[data-p]');
var envRows=root.querySelectorAll('tr[data-env]'),boxRows=root.querySelectorAll('tr[data-boxrow]'),madeRows=root.querySelectorAll('tr[data-made]'),radios=root.querySelectorAll('input[name="cost-box"]');
var qtys=[].map.call(root.querySelectorAll('td[data-tot]'),function(td){return +td.getAttribute('data-tot')});
var sel=document.getElementById('cost-mode'),hstBox=document.getElementById('cost-hst'),incs=root.querySelectorAll('input[data-inc]');
function persist(){try{localStorage.setItem(KEY,JSON.stringify(saved))}catch(err){}}
Object.keys(saved).forEach(function(k){var m=/^(\w+)@(\d+)$/.exec(k),n=/^(pc2|pc1|bm2|bm1|bc1|fl1|fl2):note$/.exec(k);
  if(m){saved[m[1]+':old:'+m[2]]=saved[k];delete saved[k]}else if(n){saved[n[1]+':old:note']=saved[k];delete saved[k]}});
function money(x){return '$'+x.toFixed(2)}
function rowTotal(r,q){var i=r.querySelector('input[data-q="'+q+'"]'),v=i?parseFloat(i.value):NaN;if(isNaN(v))return null;
  var sh=parseFloat(r.querySelector('input[data-ship]').value);return (v+(isNaN(sh)?0:sh))*(hstBox.checked?1.13:1)}
function best(p,q,only){var m=only||sel.value,b=null;
  [].forEach.call(root.querySelectorAll('tr[data-qr="'+p+'"]'),function(r){var s=r.getAttribute('data-shop');
    if(m&&s!==m)return;
    if(!m){var c=root.querySelector('input[data-inc="'+s+'"]');if(c&&!c.checked)return}
    var t=rowTotal(r,q);if(t!==null&&(!b||t<b.v))b={v:t,shop:r.getAttribute('data-sname')}});return b}
function marks(){
  root.querySelectorAll('td[data-best]').forEach(function(td){var a=td.getAttribute('data-best').split(':'),b=best(a[0],+a[1]);
    td.textContent=b?money(b.v)+' · '+b.shop:''});
  root.querySelectorAll('tr[data-qr]').forEach(function(r){var p=r.getAttribute('data-qr');
    r.querySelectorAll('input[data-q]').forEach(function(i){var q=+i.getAttribute('data-q'),t=rowTotal(r,q),b=best(p,q);
      i.classList.toggle('bestc',t!==null&&b!==null&&Math.abs(t-b.v)<1e-9)})});
  root.querySelectorAll('td[data-shopq]').forEach(function(td){var a=td.getAttribute('data-shopq').split(':'),q=+a[1],t=0,m=0;
    rows.forEach(function(r){var b=best(r.getAttribute('data-p'),q,a[0]);if(b)t+=(+r.getAttribute('data-n'))*b.v/q;else m++});
    td.textContent=m===rows.length?'':money(t)+(m?' (+'+m+' missing)':'')})}
function calc(){
  var pieces=0,tot={},miss={};qtys.forEach(function(q){tot[q]=0;miss[q]=0});
  rows.forEach(function(r){var p=r.getAttribute('data-p'),n=+r.getAttribute('data-n');pieces+=n;
    qtys.forEach(function(q){var b=best(p,q),v=b?b.v:null,c=r.querySelector('td[data-q="'+q+'"]');
      if(v===null){c.textContent='';c.title='';miss[q]++}else{var x=n*v/q;tot[q]+=x;c.textContent=money(x);c.title=b.shop}})});
  document.getElementById('cost-pieces').textContent=pieces;
  qtys.forEach(function(q){root.querySelector('td[data-tot="'+q+'"]').textContent=miss[q]===rows.length?'':money(tot[q]);
    root.querySelector('td[data-order="'+q+'"]').textContent=miss[q]===rows.length?'':'$'+Math.round(tot[q]*q).toLocaleString('en-CA');
    root.querySelector('td[data-miss="'+q+'"]').textContent=miss[q]});
  var env=0,emiss=0;
  envRows.forEach(function(r){var k=r.getAttribute('data-env'),f=function(n){return parseFloat(r.querySelector('input[data-k="'+k+':'+n+'"]').value)};
    var n=f('qty'),items=f('pack'),pp=f('packprice'),ok=!(isNaN(n)||isNaN(items)||isNaN(pp)||items<=0),each=ok?pp/items:0;
    r.querySelector('td[data-each]').textContent=ok?'$'+each.toFixed(3):'';
    r.querySelector('td[data-cost]').textContent=ok?money(n*each):'';
    if(ok)env+=n*each;else emiss++;
    setLink(r,k)});
  document.getElementById('cost-env').textContent=money(env);
  var box=(root.querySelector('input[name="cost-box"]:checked')||{}).value,tier={};qtys.forEach(function(q){tier[q]=q<=250?250:q});
  boxRows.forEach(function(r){var k=r.getAttribute('data-boxrow');r.classList.toggle('off',k!==box);setLink(r,k)});
  var br=root.querySelector('tr[data-boxrow="'+box+'"]');
  qtys.forEach(function(q){var bn=br?parseFloat(br.querySelector('input[data-k="'+box+':qty"]').value):NaN,
      bp=br?parseFloat(br.querySelector('input[data-k="'+box+':p'+tier[q]+'"]').value):NaN,bc=(isNaN(bn)||isNaN(bp))?null:bn*bp;
    setq('g1',q,money(tot[q]));setq('g2',q,money(env));setq('g5',q,bc===null?'':money(bc));
    var made=0,mmiss=0;
    madeRows.forEach(function(r){var k=r.getAttribute('data-made'),n=parseFloat(r.querySelector('input[data-k="'+k+':qty"]').value),
        su=parseFloat(r.querySelector('input[data-k="'+k+':setup"]').value),pe=parseFloat(r.querySelector('input[data-k="'+k+':p'+tier[q]+'"]').value);
      if(isNaN(pe)||isNaN(n)){mmiss++}else{made+=n*pe+(isNaN(su)?0:su/q)}});
    setq('g6',q,money(made));
    setq('g3',q,money(tot[q]+env+(bc||0)+made));setq('g4',q,miss[q]+emiss+(bc===null?1:0)+mmiss)});
  madeRows.forEach(function(r){setLink(r,r.getAttribute('data-made'))});marks()}
function setq(a,q,t){root.querySelector('td[data-'+a+'="'+q+'"]').textContent=t}
function setLink(r,k){var a=r.querySelector('a[data-linkname]'),v=(r.querySelector('input[data-k="'+k+':link"]').value||'').trim();
  if(/^https?:\/\//i.test(v)){a.href=v;a.classList.remove('nolink')}else{a.removeAttribute('href');a.classList.add('nolink')}}
radios.forEach(function(r){if(saved.box)r.checked=(r.value===saved.box);
  r.addEventListener('change',function(){saved.box=r.value;try{localStorage.setItem(KEY,JSON.stringify(saved))}catch(err){}calc()})});
if(saved.mode)sel.value=saved.mode;if(saved.hst==='1')hstBox.checked=true;
sel.addEventListener('change',function(){if(sel.value)saved.mode=sel.value;else delete saved.mode;persist();calc()});
hstBox.addEventListener('change',function(){if(hstBox.checked)saved.hst='1';else delete saved.hst;persist();calc()});
incs.forEach(function(c){var k='inc:'+c.getAttribute('data-inc');if(saved[k]==='0')c.checked=false;
  c.addEventListener('change',function(){if(c.checked)delete saved[k];else saved[k]='0';persist();calc()})});
inputs.forEach(function(inp){var k=inp.getAttribute('data-k')||(inp.getAttribute('data-p')+'@'+inp.getAttribute('data-q'));
  if(saved[k]!=null)inp.value=saved[k];
  inp.addEventListener('input',function(){if(inp.value===inp.getAttribute('data-default'))delete saved[k];else saved[k]=inp.value;
    try{localStorage.setItem(KEY,JSON.stringify(saved))}catch(err){}calc()})});
var msg=document.getElementById('cost-msg');
document.getElementById('cost-copy-notes').onclick=function(){
  var lines=[].filter.call(root.querySelectorAll('textarea[data-k]'),function(t){return t.value.trim()}).map(function(t){
    return t.getAttribute('aria-label').replace(', notes','')+'\t'+t.value.replace(/\n/g,' / ')});
  var m=document.getElementById('cost-msg-notes');
  function done(){m.textContent='Copied '+lines.length+' notes (item, note).'}
  function fallback(){var t=document.createElement('textarea');t.value=lines.join('\n');document.body.appendChild(t);t.select();
    try{document.execCommand('copy');done()}catch(err){m.textContent='Copy failed.'}t.remove()}
  if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(lines.join('\n')).then(done,fallback)}else{fallback()}};
document.getElementById('cost-clear').onclick=function(){if(!confirm('Put back the quoted prices (20 Oct 2026)?'))return;
  saved={};try{localStorage.removeItem(KEY)}catch(err){}inputs.forEach(function(i){i.value=i.getAttribute('data-default')});
  radios.forEach(function(r){r.checked=(r.value==='boxA')});sel.value='';hstBox.checked=false;incs.forEach(function(c){c.checked=true});calc();msg.textContent='Quoted prices restored.'};
calc();
})();
</script></body></html>
"""

if __name__ == "__main__":
    build()
