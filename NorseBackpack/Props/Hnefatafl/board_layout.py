"""Shared hnefatafl board data (PZ-01, PZ-07).

Single source of truth for the fixed attacker/defender squares, the throne and
the four corners, so the map-back setup panel and the museum ticket's mirrored
offset panel can never drift out of registration with each other or with the
interactive board designer (Props/Hnefatafl/board_designer.html), whose export
panel produced this exact layout.

11x11, superseding the earlier 7x7 layout (PZ-01, board size changed for
realism). Columns A-H (x = 0..7) stay visible on the map back. Columns I-K
(x = 8..10) are lost to the ink stain (PZ-07) and recovered, mirrored, on the
ticket's offset panel -- verified by search: assuming those three columns are
empty still finds 31 candidate three-move escapes, so the puzzle correctly
refuses to resolve rather than resolving wrongly.
"""

from reportlab.lib.colors import HexColor

SIZE = 11
CELL = 0.4 * 72  # 0.4in per cell, shared by both printed panels

ATTACKERS = {
    (0, 3), (0, 4), (0, 7), (1, 0), (3, 10), (3, 5), (4, 10), (5, 0),
    (5, 10), (5, 8), (6, 0), (6, 7), (7, 4), (8, 5), (10, 3), (10, 7),
}
DEFENDERS = {
    (2, 4), (4, 7), (5, 4), (5, 7), (6, 4), (6, 6),
}
BLOCKS = ATTACKERS | DEFENDERS
assert len(ATTACKERS) == 16
assert len(DEFENDERS) == 6
assert len(BLOCKS) == 22

THRONE = (5, 5)
CORNERS = {(0, 0), (0, 10), (10, 0), (10, 10)}
SOLUTION_PATH = [(5, 5), (7, 5), (7, 10), (10, 10)]  # F6 -> H6 -> H11 -> K11, legs 2/5/3, code 253

VISIBLE_COLS = range(0, 8)    # A-H, stays on the map
HIDDEN_COLS = range(8, 11)    # I-K, lost to the stain / recovered on the ticket


def coord_label(x: int, y: int) -> str:
    return chr(65 + x) + str(y + 1)


# Shared palette, matching the other paper props (Rouen/L'Anse tickets).
PAPER = HexColor("#EFE3C4")
INK = HexColor("#283B34")
RUST = HexColor("#B56A2A")
RULE = HexColor("#A99A7B")
CREAM = HexColor("#F4EEDD")
STAIN = HexColor("#8C7A52")  # translucent-looking tea/ink stain tone
