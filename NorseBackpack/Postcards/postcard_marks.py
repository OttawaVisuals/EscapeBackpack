"""The element mark each postcard carries, and one helper to draw it.

This is the crest/symbol filter from PZ-18. The final bundle's "Family
iconography" page shows two drawings: a three-element symbol (raven, longship,
sun-wheel) and a six-element crest (battle-axe, round shield, wolf, anchor,
drinking horn, valknut). A card carrying none of the nine is not one of Liv's
trail stops, and that is the whole of the decoy filter.

The rule the assignment has to satisfy
--------------------------------------
  * Each three-stop leg (Leif, Aud) uses the SYMBOL set, each element once.
  * Each six-stop leg (Rollo, Harald) uses the CREST set, each element once.
  * Every decoy carries a mark from neither set.

Any bijection satisfying that works identically as a puzzle, so the pairings
below are chosen for flavour only and can be reshuffled freely -- change this
one dict and rebuild; no other file needs touching and no clue depends on it.

Decoy marks are deliberately wrong stereotypical Norse signals: a horned helmet
and a double-bladed axe. Neither appears on either drawing, so a team comparing
a decoy against the page finds nothing -- but only if it thinks to check.

Art by Codex, in Liv's Bayeux-inspired margin-drawing language: loose dark pen
outline, flat muted fills, slight handmade wobble. See PR-22.
"""
from pathlib import Path

from reportlab.lib.utils import ImageReader

ART = Path(__file__).resolve().parents[1] / 'Art' / 'FinalPuzzle' / 'PostcardMarks'

SYMBOL = {
    'raven':     'Symbol_Raven_HandDrawn_v1.png',
    'longship':  'Symbol_Longship_HandDrawn_v1.png',
    'sun_wheel': 'Symbol_Sun_Wheel_HandDrawn_v1.png',
}
CREST = {
    'battle_axe':   'Crest_Battle_Axe_HandDrawn_v1.png',
    'round_shield': 'Crest_Round_Shield_HandDrawn_v2.png',   # v2 = the redesign; v1 was confusable with the sun-wheel
    'wolf':         'Crest_Wolf_HandDrawn_v1.png',
    'anchor':       'Crest_Anchor_HandDrawn_v1.png',
    'drinking_horn': 'Crest_Drinking_Horn_HandDrawn_v1.png',
    'valknut':      'Crest_Valknut_HandDrawn_v1.png',
}
DECOY = {
    'horned_helmet': 'Decoy_Horned_Helmet_HandDrawn_v1.png',
    'double_axe':    'Decoy_Double_Axe_HandDrawn_v1.png',
}

# card -> element. Flavour reasons in the comments; none is load-bearing.
MARKS = {
    # -- Leif, symbol set ---------------------------------------------------
    'L1': 'longship',    # the Vinland landfall itself
    'L2': 'raven',
    'L3': 'sun_wheel',   # the aurora her card describes
    'LD': 'horned_helmet',
    # -- Rollo, crest set ---------------------------------------------------
    'R1': 'valknut',        # Chalus, where Richard the Lionheart's story ends
    'R2': 'anchor',         # Rollo's capital on the Seine, where the dynasty settles
    'R3': 'round_shield',   # the tapestry is full of them
    'R4': 'drinking_horn',  # a second coronation is a feast
    'R5': 'battle_axe',     # Hastings
    'R6': 'wolf',           # the forest and its boar
    'RD': 'double_axe',
    # -- Aud, symbol set ----------------------------------------------------
    'A1': 'longship',    # arriving by sea; the "meal headland" on the way inland
    'A2': 'sun_wheel',
    'A3': 'raven',       # she turns her brother down and pushes on alone
    'AD': 'horned_helmet',
    # -- Harald, crest set --------------------------------------------------
    'H1': 'round_shield',   # founding a city
    'H2': 'wolf',           # "nobody warned me how far this feels from anywhere else"
    'H3': 'drinking_horn',  # the riddle's unwritten answer is HONEY, and mead is made of it
    'H4': 'battle_axe',     # Harald burned Hedeby to the ground
    'H5': 'anchor',         # the long sea leg south
    'H6': 'valknut',        # the journey's end
    'HD': 'double_axe',
}

_FILES = {}
_FILES.update(SYMBOL)
_FILES.update(CREST)
_FILES.update(DECOY)


def mark_path(card):
    return ART / _FILES[MARKS[card]]


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
    """Draw the card's element mark centred on (x, y)."""
    p = mark_path(card)
    if not p.exists():                       # fail loudly rather than print a blank card
        raise FileNotFoundError(f'{card}: element mark missing at {p}')
    c.drawImage(ImageReader(str(p)), x - size / 2, y - size / 2, size, size,
                preserveAspectRatio=True, mask='auto')


def check():
    """Assert the assignment still satisfies the filter's rule."""
    legs = {'leif': ('L1 L2 L3'.split(), 'LD', SYMBOL),
            'rollo': ('R1 R2 R3 R4 R5 R6'.split(), 'RD', CREST),
            'aud': ('A1 A2 A3'.split(), 'AD', SYMBOL),
            'harald': ('H1 H2 H3 H4 H5 H6'.split(), 'HD', CREST)}
    for leg, (reals, decoy, allowed) in legs.items():
        got = [MARKS[c] for c in reals]
        assert set(got) == set(allowed), f'{leg}: expected each of {sorted(allowed)}, got {sorted(got)}'
        assert len(set(got)) == len(got), f'{leg}: an element is used twice'
        assert MARKS[decoy] in DECOY, f'{leg}: decoy {decoy} carries a real element'
    for card in MARKS:
        assert mark_path(card).exists(), f'{card}: missing art {mark_path(card)}'
    return f'{len(MARKS)} cards, assignment valid, all art present'


if __name__ == '__main__':
    print(check())
