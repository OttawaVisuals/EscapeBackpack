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
MARKS = {}
for _trail, _cards, _set in (('L', 3, SYMBOL), ('R', 6, CREST), ('A', 3, SYMBOL), ('H', 6, CREST)):
    for _n, _element in enumerate(_set, start=1):
        MARKS[f'{_trail}{_n}'] = _element
    MARKS[f'{_trail}D'] = None

_FILES = {}
_FILES.update(SYMBOL)
_FILES.update(CREST)


def mark_path(card):
    return None if MARKS[card] is None else ART / _FILES[MARKS[card]]


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
MARK_X, MARK_Y, MARK_SIZE = 232, 205, 23


def draw_mark(c, card, x=MARK_X, y=MARK_Y, size=MARK_SIZE):
    """Draw the card's element mark centred on (x, y). Decoys have none: nothing is drawn."""
    p = mark_path(card)
    if p is None:
        return
    if not p.exists():                       # fail loudly rather than print a blank card
        raise FileNotFoundError(f'{card}: element mark missing at {p}')
    c.drawImage(ImageReader(str(p)), x - size / 2, y - size / 2, size, size,
                preserveAspectRatio=True, mask='auto')


def check():
    """Assert the assignment still satisfies the filter and order rules."""
    for trail, allowed in (('L', SYMBOL), ('R', CREST), ('A', SYMBOL), ('H', CREST)):
        got = [MARKS[f'{trail}{n}'] for n in range(1, len(allowed) + 1)]
        assert got == list(allowed), f'{trail}: marks {got} are not in the page order {list(allowed)}'
        assert MARKS[f'{trail}D'] is None, f'{trail}D: a decoy carries a mark'
    for card in MARKS:
        p = mark_path(card)
        assert p is None or p.exists(), f'{card}: missing art {p}'
    return f'{len(MARKS)} cards, marks in page order, decoys unmarked, all art present'


if __name__ == '__main__':
    print(check())
