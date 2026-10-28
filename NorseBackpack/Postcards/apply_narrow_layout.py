"""Move one postcard builder to the narrow-right-side layout (14 Oct 2026, Q-057).

    python apply_narrow_layout.py L1 [L2 ...]

The designer chose it from a mock-up of L1: the divider moves from x 276 to 298 of 432, the
family mark moves under the postmark, and the Fun Fact box is anchored to the bottom and starts
at mid-card, growing upward toward the stamp only if a fact needs more than 7 lines. Cards are
moved one at a time, as each puzzle is reviewed, because most of today's facts are too long for
the narrower box: give a card its short fact (drafts in Q-057) in the same pass.

Plain text replacements on lines every builder shares; it refuses a card that does not match.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

NOTE = (
    "    # 14 Oct 2026 (designer, Q-057): narrow right side. Divider x 276 -> 298 (message column\n"
    "    # 250 -> 272 pt); mark under the postmark; Fun Fact box from mid-card to the bottom.\n"
)

OLD_BOX = (
    "    funfact_top, funfact_bottom = stamp_y - 6, 37\n"
    "    c.setStrokeColor(FUNFACT)\n"
    "    c.setLineWidth(0.6)\n"
    "    c.rect(divider + 10, funfact_bottom, box_right - (divider + 10), funfact_top - funfact_bottom, fill=0, stroke=1)\n"
    "    c.setFillColor(FUNFACT)\n"
    "    c.setFont(\"Helvetica-Bold\", 8.5)\n"
    "    c.drawString(address_x, funfact_top - 13, \"FUN FACT\")\n"
    "    c.setFillColor(INK)\n"
)
OLD_TEXT_START = "    fact_y = funfact_top - 26\n"
NEW_TEXT_START = (
    "    # 14 Oct 2026 (Q-057): the box sits on the bottom (y 37) and starts at mid-card; a fact longer\n"
    "    # than 7 lines raises its top, up to just under the stamp.\n"
    "    funfact_bottom = 37\n"
    "    fact_lines = wrap_text(fact_text, fact_font, fact_size, box_right - address_x - 6)\n"
    "    funfact_top = max(H / 2, funfact_bottom + 35 + fact_leading * (len(fact_lines) - 1))\n"
    "    if funfact_top > stamp_y - 6:\n"
    "        raise SystemExit(f\"Fun Fact is {len(fact_lines)} lines; too long for the box (Q-057)\")\n"
    "    c.setStrokeColor(FUNFACT)\n"
    "    c.setLineWidth(0.6)\n"
    "    c.rect(divider + 10, funfact_bottom, box_right - (divider + 10), funfact_top - funfact_bottom, fill=0, stroke=1)\n"
    "    c.setFillColor(FUNFACT)\n"
    "    c.setFont(\"Helvetica-Bold\", 8.5)\n"
    "    c.drawString(address_x, funfact_top - 13, \"FUN FACT\")\n"
    "    c.setFillColor(INK)\n"
    "    fact_y = funfact_top - 26\n"
)


def convert(card):
    path = HERE / f"build_postcard_{card}_pdf.py"
    raw = path.read_bytes().decode("utf-8")
    crlf = "\r\n" in raw
    s = raw.replace("\r\n", "\n")
    if "NARROW_MARK_X" in s:
        print(f"{card}: already converted")
        return
    steps = [
        ("from postcard_marks import draw_mark\n",
         "from postcard_marks import NARROW_MARK_X, NARROW_MARK_Y, draw_mark\n"),
        ("    divider = 276\n", NOTE + "    divider = 298\n"),
        (f'draw_mark(c, "{card}")', f'draw_mark(c, "{card}", NARROW_MARK_X, NARROW_MARK_Y)'),
        (OLD_BOX, "    c.setFillColor(INK)\n"),   # the box is now drawn once the fact is wrapped
        (OLD_TEXT_START, NEW_TEXT_START),
    ]
    for old, new in steps:
        if s.count(old) != 1:
            raise SystemExit(f"{card}: expected one {old.strip()[:50]!r}, found {s.count(old)}")
        s = s.replace(old, new)
    path.write_bytes((s.replace("\n", "\r\n") if crlf else s).encode("utf-8"))
    print(f"{card}: converted")


if __name__ == "__main__":
    for card in sys.argv[1:]:
        convert(card)
