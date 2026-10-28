"""Shared hnefatafl board data (PZ-01, PZ-07).

Single source of truth for the fixed attacker/defender squares, the throne and
the four corners, so the map-back setup panel and the museum ticket's mirrored
offset panel can never drift out of registration with each other or with the
interactive board designer (Props/Hnefatafl/board_designer.html), whose export
panel produced this exact layout.

11x11, superseding the earlier 7x7 layout (PZ-01, board size changed for
realism). Columns A-H (x = 0..7) stay visible on the map back. Columns I-K
(x = 8..10) are lost to the ink stain (PZ-07) and recovered, mirrored, on the
ticket's offset panel -- checked by search with hnefatafl_solver.py (17 Oct 2026): with the black moves in BLACK_MOVES the king has exactly
one escape in four moves, F6 H6 H7 K7 K11 (code 2134).
"""

from reportlab.lib.colors import HexColor

SIZE = 11
CELL = 0.4 * 72  # 0.4in per cell, shared by both printed panels

# 17 Oct 2026 (PZ-008, designer): the layout changed with the black moves. 19 dark, 6 light.
# Against the earlier 16-dark layout: D6 -> D7, H5 -> H2, G8 -> H10, K8 removed, E1 added, and
# I8, I9 and K10 added. Hidden columns I-K now hold I6, I8, I9, K4, K10 (the ticket strip).
# The earlier layout is kept in board_layout.2026-10-17_before_2134.py.
ATTACKERS = {
    (0, 3), (0, 4), (0, 7), (1, 0), (3, 10), (3, 6), (4, 0), (4, 10), (5, 0),
    (5, 10), (5, 8), (6, 0), (7, 1), (7, 9), (8, 5), (8, 7), (8, 8), (10, 3), (10, 9),
}
DEFENDERS = {
    (2, 4), (4, 7), (5, 4), (5, 7), (6, 4), (6, 6),
}
BLOCKS = ATTACKERS | DEFENDERS
assert len(ATTACKERS) == 19
assert len(DEFENDERS) == 6
assert len(BLOCKS) == 25

THRONE = (5, 5)
CORNERS = {(0, 0), (0, 10), (10, 0), (10, 10)}
# Dark moves first, then the king, four times (B K B K B K B K). The last dark move frees column K.
BLACK_MOVES = [((4, 0), (4, 5)),    # 1. E1 -> E6   (arrow 1 on the map back)
               ((7, 1), (7, 4)),    # 2. H2 -> H5   (arrow 2 on the map back)
               ((7, 9), (7, 10)),   # 3. H10 -> H11 (Liv's riddle: second-highest row steps up to the top row)
               ((10, 9), (8, 9))]   # 4. K10 -> I10 (the shield icon on Harald's map marks I10)
SOLUTION_PATH = [(5, 5), (7, 5), (7, 6), (10, 6), (10, 10)]  # F6 -> H6 -> H7 -> K7 -> K11, legs 2/1/3/4, code 2134

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
