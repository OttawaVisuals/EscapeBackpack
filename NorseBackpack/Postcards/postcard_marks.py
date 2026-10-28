"""The element mark each postcard carries, and one helper to draw it.

This is the crest/symbol filter from PZ-18. The final bundle's "Family
iconography" page shows two drawings: a three-element symbol (raven, longship,
sun-wheel) and a six-element crest (battle-axe, round shield, wolf, anchor,
drinking horn, valknut). A card carrying none of the nine is not one of Liv's
trail stops, and that is the whole of the decoy filter.

The rules the assignment has to satisfy (12 Oct 2026, Q-054)
------------------------------------------------------------
  * Each three-stop leg (Leif, Aud) uses the SYMBOL set, each element once.
  * Each six-stop leg (Rollo, Harald) uses the CREST set, each element once.
  * The n-th stop of a leg carries the n-th element in the page's caption order, so the
    page gives the visit order.
  * Decoys carry no mark.

Superseded: the flavour pairings, the "any bijection works" rule, and the horned-helmet /
double-axe decoy marks. The marks are now crops of the page's own drawings, not Codex's
separate hand-drawn set (PR-22), which stays in the art folder unused.
"""
from pathlib import Path

from reportlab.lib.utils import ImageReader

ART = Path(__file__).resolve().parents[1] / 'Art' / 'FinalPuzzle' / 'PostcardMarks'

# 12 Oct 2026 (playtest 1, Q-054): the marks are now crops of the iconography page's own
# drawings (Art/FinalPuzzle/build_iconography_marks.py), so a card matches the page at a glance.
# The *_HandDrawn_v1.png marks they replace are kept in the same folder, unused.
# Key order matters: it is the order the page's captions list them in, and the visit order.
SYMBOL = {
    'raven':     'Symbol_Raven_Iconography_v1.png',
    'longship':  'Symbol_Longship_Iconography_v1.png',
    'sun_wheel': 'Symbol_Sun_Wheel_Iconography_v1.png',
}
CREST = {
    'battle_axe':    'Crest_Battle_Axe_Iconography_v1.png',
    'round_shield':  'Crest_Round_Shield_Iconography_v1.png',
    'wolf':          'Crest_Wolf_Iconography_v1.png',
    'anchor':        'Crest_Anchor_Iconography_v1.png',
    'drinking_horn': 'Crest_Drinking_Horn_Iconography_v1.png',
    'valknut':       'Crest_Valknut_Iconography_v1.png',
}

# card -> element, or None for a decoy (no mark at all).
# 12 Oct 2026 (designer, Q-054): the marks now also give the ORDER. On each trail, the stops
# carry the page's elements in the order its captions list them, so the n-th stop carries the
# n-th element -- players order a trail's cards by the iconography page instead of rereading
# card text. Decoys carry no mark (they used to carry a horned helmet or a double axe).
# The flavour pairings that used to be here are superseded.
# 17 Oct 2026 (designer, Q-062): the crest, the symbol's longship and sun-wheel and the order they
# gave are retired. Every REAL stop carries the one small raven (a simple pencil sketch in a thin
# knotwork ring, drawn for a 28 pt slot); decoys carry nothing. Stop order now comes from the hop
# tickets (Props/Tickets/build_hop_tickets_pdf.py). The old marks above stay in the art folder, unused.
RAVEN_SMALL = Path(__file__).resolve().parents[1] / 'Art' / 'Raven' / 'Raven_Profile_Pencil_28pt_Frame_v1.png'
RAVEN_LARGE = Path(__file__).resolve().parents[1] / 'Art' / 'Raven' / 'Raven_Profile_Knotwork_Pencil_v2.png'

MARKS = {}
for _trail, _cards in (('L', 3), ('R', 6), ('A', 3), ('H', 6)):
    for _n in range(1, _cards + 1):
        MARKS[f'{_trail}{_n}'] = 'raven'
    MARKS[f'{_trail}D'] = None

_FILES = {'raven': RAVEN_SMALL.name}


def mark_path(card):
    return None if MARKS[card] is None else RAVEN_SMALL


# Where the mark sits, in card points, identical on all 22 cards.
#
# The card's right half is built from fixed furniture: the divider at x=184, the
# address box topping out at y=188, and the postmark circle centred (278, 204)
# with r=23. That leaves a clear pocket of roughly x 186..253 by y 190..220,
# between the divider and the postmark and above the address box. Because every
# one of those elements is at the same place on every card, this position is
# free by construction rather than by luck.
#
# It replaces a first attempt that put the mark beside the signature. That spot
# was free too, but it sat in the message half among Liv's own margin drawings --
# on R3/R4/R5 it read as another piece of the Bayeux rebus, and on H4 it crowded
# the branch-rune key. Up here the mark is unmistakably part of the card's
# printed furniture, not part of anything she drew.
#
# 13 Oct 2026 (6 x 4 in card, layout B): the divider is at x=276 of 432 and the postmark
# circle is centred (334, 230) with r=27.6; the stamp's bottom-left corner is (340, 170) and the
# Fun Fact box starts at y=164. The pocket is now left of the stamp, under the postmark,
# x 278..338 by y 166..202. The mark is 1.2x (about 10 mm, was 8).
MARK_X, MARK_Y, MARK_SIZE = 304, 185, 28
#
# 14 Oct 2026 (designer, Q-057): narrow right side. The divider moves to x=298, so the mark moves
# right, under the postmark (whose left edge is x 306): x 306..334 by y 171..199, clear of the stamp
# (x >= 340) and of the Fun Fact box (now mid-card down). Cards move over one at a time
# (apply_narrow_layout.py); once all 22 have, this becomes MARK_X.
NARROW_MARK_X, NARROW_MARK_Y = 320, 185


def draw_mark(c, card, x=MARK_X, y=MARK_Y, size=MARK_SIZE):
    """Draw the card's element mark centred on (x, y). Decoys have none: nothing is drawn."""
    p = mark_path(card)
    if p is None:
        return
    if not p.exists():                       # fail loudly rather than print a blank card
        raise FileNotFoundError(f'{card}: element mark missing at {p}')
    c.drawImage(ImageReader(str(p)), x - size / 2, y - size / 2, size, size,
                preserveAspectRatio=True, mask='auto')


def draw_large_raven(c, x, y, size):
    """The large detailed raven (family icon) with its lower-left corner at (x, y). Used on H6."""
    c.drawImage(ImageReader(str(RAVEN_LARGE)), x, y, size, size, preserveAspectRatio=True, mask='auto')


def check():
    """Assert 18 real cards carry the raven, the 4 decoys carry nothing, and the art exists."""
    for trail in 'LRAH':
        assert MARKS[f'{trail}D'] is None, f'{trail}D: a decoy carries a mark'
    real = [k for k, v in MARKS.items() if v]
    assert len(real) == 18, f'{len(real)} real cards carry the raven, expected 18'
    assert RAVEN_SMALL.exists() and RAVEN_LARGE.exists(), 'raven art missing'
    return f'{len(MARKS)} cards, 18 raven marks, decoys unmarked, art present'


if __name__ == '__main__':
    print(check())
