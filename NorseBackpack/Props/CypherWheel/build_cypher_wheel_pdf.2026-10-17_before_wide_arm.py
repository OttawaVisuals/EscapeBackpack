"""Rune cypher wheel: a cardstock volvelle that points each code to its envelope.

Decided 11 Oct 2026 (PR-007): the game is a box of rune-marked envelopes, no locks.
Players set a code on four wheels and read four runes in the opposite window;
the envelope carrying those runes is the one the code opens.

- Same 20 symbols on every wheel: 0-9, a blank (3-digit codes start with it)
  and the nine letters the word codes use. Letters print in red so O and 0
  can't be confused.
- Each wheel gives every symbol its own rune, so each code reads as its own
  rune string and a wrong code never shows an envelope's runes.
- Codes and envelope numbers come from the puzzle records (answer, container
  "Envelope N"); the key lists each envelope's props (found_in).

Output: NorseBackpack/Print/_pdf_source/Cypher_Wheel_Print.pdf (5 Letter pages: wheels I-IV, arm,
envelope labels, designer key). Print at 100% on cardstock.
"""
import random
import re
from pathlib import Path

from fontTools.ttLib import TTFont
from reportlab.lib.colors import HexColor, white
from reportlab.lib.utils import simpleSplit
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont as RLFont
from reportlab.pdfgen import canvas
from reportlab.pdfgen.canvas import FILL_EVEN_ODD

ROOT = Path(__file__).resolve().parents[3]
RECORDS = ROOT / "NorseBackpack" / "records"
OUT = ROOT / "NorseBackpack" / "Print" / "_pdf_source" / "Cypher_Wheel_Print.pdf"
PREVIEW = ROOT / "NorseBackpack" / "Print" / "_pdf_source" / "Cypher_Wheel_Assembled_Preview.pdf"
FONTS = {
    "Digit": Path(r"C:\Windows\Fonts\arialbd.ttf"),
    "Rune": Path(r"C:\Windows\Fonts\seguihis.ttf"),
    "Cinzel": ROOT / "Fonts" / "Cinzel" / "static" / "Cinzel-Bold.ttf",
}

MM = 72 / 25.4
PAGE_W, PAGE_H = 8.5 * 72, 11 * 72
INK = HexColor("#283B34")
RED = HexColor("#9B2D20")
PARCHMENT = HexColor("#F3EBD8")
RUNE_BAND = HexColor("#E2D3B1")
HUB = HexColor("#C9B48A")

BLANK = " "
SYMBOLS = list("0123456789") + [BLANK] + list("ABDEKLMOS")
# Elder Futhark minus four look-alikes (ansuz~fehu, mannaz~ehwaz, jera, ingwaz).
RUNES = list("ᚠᚢᚦᚱᚲᚷᚹᚺᚾᛁᛇᛈᛉᛊᛏᛒᛖᛚᛟᛞ")
SEED = 1021
STEP = 360 / len(SYMBOLS)

# Wheel I is the bottom (largest) disk; IV sits on top. Radii in mm.
RADII = [98, 78, 58, 38]
NAMES = ["I", "II", "III", "IV"]
BAND = 20
SYM_R = 5.5      # symbol centre, mm in from the wheel edge
RUNE_R = 15.25   # rune centre, mm in from the wheel edge
SPLIT = 10.5     # line between the symbol and rune rings


def register_fonts():
    bounds = {}
    for name, path in FONTS.items():
        pdfmetrics.registerFont(RLFont(name, str(path)))
        tt = TTFont(str(path))
        cmap, glyf = tt.getBestCmap(), tt["glyf"]
        upm = tt["head"].unitsPerEm
        b = {}
        for ch in SYMBOLS + RUNES:
            g = cmap.get(ord(ch))
            if g and hasattr(glyf[g], "yMax"):
                gl = glyf[g]
                b[ch] = ((gl.xMin + gl.xMax) / 2 / upm, (gl.yMin + gl.yMax) / 2 / upm,
                         (gl.yMax - gl.yMin) / upm)
        bounds[name] = b
    return bounds


def field(text, key):
    m = re.search(rf"^{key}:[ \t]*(.*)$", text, re.M)
    return m.group(1).strip() if m else ""


def short(title):
    """'Postcard L2 · Battle Harbour (Markland)' -> 'L2'; drop bracketed asides."""
    m = re.match(r"Postcard (\w+) ·", title)
    return m.group(1) if m else re.sub(r"\s*\(.*?\)", "", title)


def read_codes():
    """(envelope number, code, what's inside) for every puzzle, in play order."""
    inside = {}
    for f in sorted((RECORDS / "props").glob("PP-*.md")):
        text = f.read_text(encoding="utf-8")
        if field(text, "status") != "parked" and field(text, "found_in"):
            inside.setdefault(field(text, "found_in"), []).append(short(field(text, "title")))
    locks = []
    for f in (RECORDS / "puzzles").glob("PZ-*.md"):
        text = f.read_text(encoding="utf-8")
        answer = field(text, "answer")
        number = re.match(r"Envelope (\d+)$", field(text, "container"))
        if answer and number:
            code = answer.upper().rjust(4, BLANK)
            assert len(code) == 4 and all(s in SYMBOLS for s in code), (f.name, code)
            locks.append((int(number.group(1)), code, ", ".join(inside.get(field(text, "id"), []))))
    return sorted(locks)


def check_hint_titles(labels):
    """Hint steps are named after the envelope just opened (Q-048): step N says
    "Just opened <runes of envelope N-1>". Warn when a code change has left one stale."""
    stale = []
    for f in (RECORDS / "puzzles").glob("PZ-*.md"):
        text = f.read_text(encoding="utf-8")
        number = re.match(r"Envelope (\d+)$", field(text, "container"))
        if number and int(number.group(1)) > 1:
            want = f"Just opened {labels[int(number.group(1)) - 2]}"
            if field(text, "hint_title") != want:
                stale.append(f"{f.name}: hint_title should be '{want}'")
    for line in stale:
        print("WARNING", line)


def rune_maps():
    rng = random.Random(SEED)
    maps = []
    for _ in RADII:
        runes = RUNES[:]
        rng.shuffle(runes)
        maps.append(dict(zip(SYMBOLS, runes)))
    return maps


def label(code, maps):
    """Runes as they read left to right in the window: wheel IV (inner) to I."""
    return "".join(maps[i][code[i]] for i in reversed(range(4)))


def glyph(c, bounds, font, ch, x, y, rotation, height, colour):
    """Draw one character centred on (x, y) by its real outline, rotated."""
    if ch == BLANK:
        return
    cx, cy, h = bounds[font][ch]
    size = height / h
    c.saveState()
    c.translate(x, y)
    c.rotate(rotation)
    c.setFillColor(colour)
    c.setFont(font, size)
    c.drawString(-cx * size, -cy * size, ch)
    c.restoreState()


def polar(cx, cy, r, deg):
    from math import cos, sin, radians
    return cx + r * cos(radians(deg)), cy + r * sin(radians(deg))


def wheel(c, bounds, maps, i, cx, cy, turn=0):
    """Draw wheel i; turn rotates it by whole slots (the symbol at 9 o'clock)."""
    c.saveState()
    c.translate(cx, cy)
    c.rotate(turn * STEP)
    cx = cy = 0
    R = RADII[i] * MM
    inner = (RADII[i] - BAND) * MM
    c.setLineWidth(0.8)
    c.setStrokeColor(INK)
    c.setFillColor(PARCHMENT)
    c.circle(cx, cy, R, stroke=1, fill=1)
    c.setFillColor(RUNE_BAND)
    c.circle(cx, cy, R - SPLIT * MM, stroke=0, fill=1)
    c.setLineWidth(0.4)
    c.circle(cx, cy, R - SPLIT * MM, stroke=1, fill=0)
    # Covered by the wheel above (or the hub on wheel IV).
    c.setFillColor(HUB if i == 3 else white)
    c.circle(cx, cy, inner, stroke=1, fill=1)
    for k, sym in enumerate(SYMBOLS):
        theta = 180 - STEP * k
        x0, y0 = polar(cx, cy, inner, theta + STEP / 2)
        x1, y1 = polar(cx, cy, R, theta + STEP / 2)
        c.setLineWidth(0.3)
        c.line(x0, y0, x1, y1)
        rot = theta - 180
        font = "Digit" if sym.isdigit() else "Cinzel"
        sx, sy = polar(cx, cy, R - SYM_R * MM, theta)
        glyph(c, bounds, font, sym, sx, sy, rot, 5.2 * MM, INK if sym.isdigit() else RED)
        rx, ry = polar(cx, cy, R - RUNE_R * MM, theta + 180)
        glyph(c, bounds, "Rune", maps[i][sym], rx, ry, rot, 4.6 * MM, INK)
    # Assembly note in the covered area.
    c.setFillColor(INK)
    if i < 3:
        c.setFont("Cinzel", 11)
        c.drawCentredString(cx, cy + 8 * MM, f"Wheel {NAMES[i]}")
        c.setFont("Helvetica", 7)
        c.drawCentredString(cx, cy - 10 * MM, f"Under wheel {NAMES[i + 1]}")
    else:
        c.setFont("Cinzel", 7)
        c.drawCentredString(cx, cy + 9 * MM, "IV")
    pin(c, cx, cy)
    c.restoreState()


def pin(c, cx, cy):
    c.setStrokeColor(INK)
    c.setLineWidth(0.4)
    c.circle(cx, cy, 1.5 * MM)
    c.line(cx - 3 * MM, cy, cx + 3 * MM, cy)
    c.line(cx, cy - 3 * MM, cx, cy + 3 * MM)


def arm(c, bounds, cx, cy):
    """Top arm: code windows on the left, rune windows on the right."""
    from math import pi
    half = (RADII[0] + 3) * MM
    w = 18 * MM
    holes = []
    for R in RADII:
        sym_pitch = 2 * pi * (R - SYM_R) / len(SYMBOLS)
        h = min(0.8 * sym_pitch, 11) * MM
        x0, x1 = cx - (R - 1) * MM, cx - (R - SPLIT + 0.5) * MM
        holes.append((x0, cy - h / 2, x1 - x0, h))
        rune_pitch = 2 * pi * (R - RUNE_R) / len(SYMBOLS)
        h = min(0.8 * rune_pitch, 11) * MM
        x0, x1 = cx + (R - BAND + 0.5) * MM, cx + (R - SPLIT - 0.5) * MM
        holes.append((x0, cy - h / 2, x1 - x0, h))
    path = c.beginPath()
    path.roundRect(cx - half, cy - w / 2, 2 * half, w, w / 2)
    for hole in holes:
        path.rect(*hole)
    c.setFillColor(HUB)
    c.setStrokeColor(INK)
    c.setLineWidth(0.8)
    c.drawPath(path, stroke=0, fill=1, fillMode=FILL_EVEN_ODD)
    c.roundRect(cx - half, cy - w / 2, 2 * half, w, w / 2, stroke=1, fill=0)
    c.setDash(2, 1.5)
    c.setStrokeColor(RED)
    c.setLineWidth(0.6)
    for hole in holes:
        c.rect(*hole, stroke=1, fill=0)
    c.setDash()
    # 14 Oct 2026 (designer, PR-007 option 2): the arm carries the three steps, each beside the
    # windows it refers to, so the rule is in front of players every time they set a code (L1
    # only gives the first try). Was just "CODE" and "RUNES". The strips above and below the
    # windows are 3.5 mm (arm 18 mm, windows at most 11 mm), so the text sits outside them.
    c.setFillColor(INK)
    c.setFont("Cinzel", 6)
    c.drawRightString(cx - 4 * MM, cy + 6.2 * MM, "1  SET THE CODE")
    c.drawString(cx + 4 * MM, cy + 6.2 * MM, "2  READ THE RUNES")
    c.drawString(cx + 4 * MM, cy - 7.9 * MM, "3  OPEN THE ENVELOPE WITH THESE RUNES")
    # 17 Oct 2026 (Q-063): the blank-first rule was only on the designer key. Wording is Codex's
    # proposal (leading 0 does not work: 0532 shows different runes from _532), set under the code windows.
    c.setFont("Cinzel", 5.4)
    c.drawRightString(cx - 4 * MM, cy - 7.9 * MM, "THREE DIGITS? LEAVE THE FIRST WINDOW BLANK")
    c.setFont("Cinzel", 6)
    pin(c, cx, cy)


def header(c, title, lines):
    c.setFillColor(INK)
    c.setFont("Cinzel", 13)
    c.drawString(12 * MM, PAGE_H - 14 * MM, title)
    c.setFont("Helvetica", 8)
    for n, line in enumerate(lines):
        c.drawString(12 * MM, PAGE_H - (20 + 4 * n) * MM, line)


def scale_bar(c, x, y):
    c.setStrokeColor(INK)
    c.setLineWidth(0.5)
    c.line(x, y, x + 50 * MM, y)
    for t in (0, 50):
        c.line(x + t * MM, y - 1.5 * MM, x + t * MM, y + 1.5 * MM)
    c.setFont("Helvetica", 6.5)
    c.drawString(x + 52 * MM, y - 1 * MM, "50 mm: check at 100%")


def labels_page(c, bounds, maps, locks):
    header(c, "Envelope runes", [
        "Cut on the solid line and stick one label on the front of each envelope. "
        "The grey line under each label is for you only and gets cut away.",
        "Runes read left to right exactly as they show in the arm's right-hand window.",
    ])
    cols, lw, lh, gx, gy = 3, 58 * MM, 22 * MM, 7 * MM, 12 * MM
    x0 = (PAGE_W - cols * lw - (cols - 1) * gx) / 2
    top = PAGE_H - 36 * MM
    for n, (lock, code, _) in enumerate(locks):
        col, row = n % cols, n // cols
        x, y = x0 + col * (lw + gx), top - row * (lh + gy) - lh
        c.setFillColor(PARCHMENT)
        c.setStrokeColor(INK)
        c.setLineWidth(0.8)
        c.roundRect(x, y, lw, lh, 2 * MM, stroke=1, fill=1)
        runes = label(code, maps)
        for j, r in enumerate(runes):
            glyph(c, bounds, "Rune", r, x + lw * (j + 0.5) / 4, y + lh / 2, 0, 12 * MM, INK)
        c.setFillColor(HexColor("#8A8A8A"))
        c.setFont("Helvetica", 7)
        shown = code.replace(BLANK, "_")
        c.drawCentredString(x + lw / 2, y - 4 * MM, f"Envelope {lock} · {shown}")


def key_page(c, maps, locks):
    header(c, "Designer key: do not pack", [
        "Envelope N is opened by the code of step N (PR-007). 3-digit codes start with the blank (shown _).",
        f"Rune maps are fixed by SEED = {SEED} in build_cypher_wheel_pdf.py; "
        "change the seed and every label changes.",
    ])
    y = PAGE_H - 38 * MM
    cols = [12, 30, 52, 82]
    c.setFont("Helvetica-Bold", 8.5)
    for x, t in zip(cols, ["Envelope", "Code", "Runes", "Holds"]):
        c.drawString(x * MM, y, t)
    y -= 8 * MM
    for lock, code, box in locks:
        c.setFont("Helvetica", 9)
        c.drawString(cols[0] * MM, y, str(lock))
        c.drawString(cols[1] * MM, y, code.replace(BLANK, "_"))
        c.setFont("Rune", 13)
        c.drawString(cols[2] * MM, y - 1, " ".join(label(code, maps)))
        c.setFont("Helvetica", 9)
        for n, line in enumerate(simpleSplit(box, "Helvetica", 9, PAGE_W - (cols[3] + 12) * MM)):
            c.drawString(cols[3] * MM, y - n * 3.8 * MM, line)
        y -= 9 * MM
    y -= 6 * MM
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(12 * MM, y, "Full rune table (symbol → rune per wheel)")
    y -= 7 * MM
    for i in range(4):
        c.setFont("Helvetica", 8)
        c.drawString(12 * MM, y, f"Wheel {NAMES[i]}")
        for k, sym in enumerate(SYMBOLS):
            x = (32 + k * 8.4) * MM
            c.setFont("Helvetica", 7)
            c.drawCentredString(x, y + 4 * MM, sym if sym != BLANK else "_")
            c.setFont("Rune", 11)
            c.drawCentredString(x, y - 1.5 * MM, maps[i][sym])
        y -= 14 * MM


def preview(bounds, maps, locks):
    """Assembled wheel, one page per lock, set to that lock's code (checks the windows)."""
    c = canvas.Canvas(str(PREVIEW), pagesize=(PAGE_W, PAGE_W), pageCompression=1)
    c.setTitle("Rune cypher wheel: assembled preview")
    for lock, code, _ in locks:
        cx = cy = PAGE_W / 2
        for i in range(4):
            wheel(c, bounds, maps, i, cx, cy, turn=SYMBOLS.index(code[i]))
        arm(c, bounds, cx, cy)
        c.setFillColor(INK)
        c.setFont("Helvetica", 9)
        text = f"Envelope {lock} · code {code.replace(BLANK, '_')} · envelope runes "
        c.drawString(10 * MM, 10 * MM, text)
        c.setFont("Rune", 11)
        c.drawString(10 * MM + pdfmetrics.stringWidth(text, "Helvetica", 9), 10 * MM,
                     " ".join(label(code, maps)))
        c.showPage()
    c.save()
    print(PREVIEW)


def main():
    bounds = register_fonts()
    locks = read_codes()
    maps = rune_maps()
    labels = [label(code, maps) for _, code, _ in locks]
    assert len(set(labels)) == len(labels)
    assert [n for n, _, _ in locks] == list(range(1, len(locks) + 1)), "envelopes must be numbered 1..N"
    check_hint_titles(labels)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUT), pagesize=(PAGE_W, PAGE_H), pageCompression=1)
    c.setTitle("Rune cypher wheel")
    c.setAuthor("Escape Backpack")

    header(c, "Rune cypher wheel · wheel I", [
        "Print all pages at 100% on cardstock. Cut out wheels I-IV and the arm (page 3), "
        "then cut out the arm's 8 red-dashed windows.",
        "Stack from the bottom: I, II, III, IV, arm. Push a brass fastener through all the centres.",
        "To use: turn the wheels until the left windows show the code, then read the runes in the right windows.",
    ])
    scale_bar(c, 12 * MM, 12 * MM)
    wheel(c, bounds, maps, 0, PAGE_W / 2, PAGE_H / 2 - 12 * MM)
    c.showPage()

    wheel(c, bounds, maps, 1, PAGE_W / 2, PAGE_H - 12 * MM - RADII[1] * MM)
    wheel(c, bounds, maps, 3, PAGE_W / 2, 14 * MM + RADII[3] * MM)
    c.showPage()

    wheel(c, bounds, maps, 2, PAGE_W / 2, PAGE_H - 14 * MM - RADII[2] * MM)
    arm(c, bounds, PAGE_W / 2, 40 * MM)
    c.setFont("Helvetica", 7)
    c.setFillColor(INK)
    c.drawCentredString(PAGE_W / 2, 26 * MM, "Arm: cut out, then cut out the 8 red-dashed windows. It goes on top.")
    c.showPage()

    labels_page(c, bounds, maps, locks)
    c.showPage()
    key_page(c, maps, locks)
    c.showPage()
    c.save()
    print(OUT)
    preview(bounds, maps, locks)
    for (lock, code, _), lab in zip(locks, labels):
        print(lock, code.replace(BLANK, "_"), lab)


if __name__ == "__main__":
    main()
