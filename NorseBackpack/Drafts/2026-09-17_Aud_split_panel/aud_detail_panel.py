"""Aud's Dalir/Hvammur detail panel: the data, and the check that keeps it solvable (PZ-17).

This module is the single source for the detail panel's survey numbering, its landmark
placements and the seven-stop treasure route.  `build_trail_maps_pdf.py` draws from it; running
this file verifies it.  Keeping both in one place is deliberate -- the numbers and the check
drifting apart is the failure this module exists to prevent.

The mechanic (PZ-17, redesigned 17 Sept 2026, superseding digits-baked-into-the-artwork):

    Every cell of the 6x10 detail grid carries a small two-digit survey plot number, printed
    quietly in one corner.  Repeats across the grid are fine -- the numbers are a lookup table,
    not a signal.  Players follow a six-hop clue chain from landmark to landmark, record each
    stop's plot number on the museum ticket's reverse, and the lock code is their SUM.

Two invariants, both learned by breaking them:

  1. EVERY STOP IS A DIFFERENT LANDMARK TYPE.  Addition is order-independent, so two stops
     sharing a type can be swapped for free and still total correctly.  A first pass with
     sheepfolds at stops 4 and 6 produced three wrong routes summing to exactly the answer.

  2. NO WRONG ROUTE MAY LAND WITHIN `MARGIN` OF THE ANSWER.  "Wrong" means each stop swapped
     for any same-type landmark drawn elsewhere on the panel.  The same first pass had a wrong
     route two away from the target -- indistinguishable from an arithmetic slip.

Re-run this module after changing ANY plot number or landmark placement:

    python aud_detail_panel.py

It exits non-zero if either invariant breaks.
"""

import itertools
import sys

COLS, ROWS = 6, 10
MARGIN = 15          # no wrong route may land this close to the real sum

# Survey plot numbers, rows 1..10 top-down, columns a..f left-to-right.
# Cells carrying a stop or a same-type decoy were solved for by search; the rest are filler
# chosen only to look like a real parcel survey.
PLOTS = (
    (14, 62, 37, 85, 21, 58),
    (73, 29, 46, 12, 90, 34),
    (55, 18, 67, 71, 24, 81),
    (89, 49, 63, 15, 45, 31),
    (31, 76, 48, 38, 21, 95),
    (66, 13, 51, 39, 26, 25),
    (24, 94, 59, 79, 17, 83),
    (22, 29, 60, 44, 30, 78),
    (91, 36, 86, 28, 57, 11),
    (45, 68, 19, 74, 86, 30),
)

# (kind, col, row) -- col 0 == 'a', row 0 == grid row 1.  dx/dy offsets used for drawing live
# in the build script; only the cell matters to the puzzle.
#
# Kinds that appear in ROUTE are puzzle-bearing: every extra placement of such a kind is a real
# decoy that a careless clue read can land on.  The remaining kinds are scenery and carry no
# puzzle weight, so they may repeat freely.
FEATURES = (
    ("ford",   2, 6),
    ("mill",   3, 6), ("mill",   4, 4),
    ("falls",  4, 3),
    ("fold",   3, 2), ("fold",   4, 5), ("fold",   0, 6),
    ("chapel", 1, 3), ("chapel", 1, 7),
    ("cairn",  2, 8), ("cairn",  5, 3), ("cairn",  3, 4), ("cairn", 4, 7),
    ("stone",  5, 7), ("stone",  2, 5),
    ("naust",  1, 1), ("naust",  1, 2),
    ("farm",   2, 2), ("farm",   3, 1), ("farm",   4, 9), ("farm", 0, 8), ("farm", 5, 9),
    ("birch",  2, 3), ("birch",  1, 6), ("birch",  4, 1), ("birch", 3, 0),
    ("marsh",  3, 8), ("marsh",  1, 9),
)

# The seven stops, in walking order.  Stop 1 is pre-filled on the museum ticket's reverse, so
# only six clue hops need writing.  Stop 3 (falls) has no same-type decoy on purpose: one free
# hop as a breather.  Stop 5 (chapel) is the one deliberately ambiguous hop, resolved only by
# postcard A2's in-person observation (the inland birch hollow, not the coast).
ROUTE = (
    ("ford",   2, 6),
    ("mill",   3, 6),
    ("falls",  4, 3),
    ("fold",   3, 2),
    ("chapel", 1, 3),
    ("cairn",  2, 8),
    ("stone",  5, 7),
)


def ref(col, row):
    """Grid reference as printed on the panel, e.g. (2, 6) -> 'c7'."""
    return "%s%d" % ("abcdef"[col], row + 1)


def plot(col, row):
    """The survey number printed in that cell."""
    return PLOTS[row][col]


def route_sum():
    """The treasure lock's code: the seven stops' plot numbers, added."""
    return sum(plot(col, row) for _, col, row in ROUTE)


def placements(kind):
    """Every cell on the panel carrying this landmark type."""
    return [(col, row) for k, col, row in FEATURES if k == kind]


def check(margin=MARGIN):
    """Verify both invariants. Returns (ok, lines_to_print)."""
    out = []
    ok = True
    target = route_sum()

    kinds = [k for k, _, _ in ROUTE]
    out.append("route  %s" % "  >  ".join("%s %s" % (ref(c, r), k) for k, c, r in ROUTE))
    out.append("sum    %d" % target)

    if len(set(kinds)) != len(kinds):
        dupes = sorted({k for k in kinds if kinds.count(k) > 1})
        out.append("FAIL   repeated stop type(s): %s" % ", ".join(dupes))
        out.append("       a sum is order-independent, so same-type stops swap for free")
        ok = False
    else:
        out.append("types  %d stops, %d distinct kinds -- no free swap" % (len(kinds), len(set(kinds))))

    for k, c, r in ROUTE:
        if plot(c, r) < 20:
            out.append("FAIL   stop %s carries %d; a stop under 20 puts 'omit one stop' "
                       "within the margin" % (ref(c, r), plot(c, r)))
            ok = False

    if not (100 <= target <= 999):
        out.append("FAIL   sum %d is not a three-digit lock code" % target)
        ok = False

    alts = [placements(k) for k, _, _ in ROUTE]
    real = [(c, r) for _, c, r in ROUTE]
    worst, count = None, 0
    for combo in itertools.product(*alts):
        if list(combo) == real:
            continue
        count += 1
        gap = abs(sum(plot(c, r) for c, r in combo) - target)
        if worst is None or gap < worst[0]:
            worst = (gap, combo)
    if worst is None:
        out.append("WARN   no decoys at all -- every stop is the only one of its kind")
    else:
        gap, combo = worst
        out.append("decoys %d wrong-but-plausible routes; closest lands %d away" % (count, gap))
        if gap <= margin:
            out.append("FAIL   closest wrong route %s sums to %d, within %d of %d"
                       % (" ".join(ref(c, r) for c, r in combo),
                          sum(plot(c, r) for c, r in combo), margin, target))
            ok = False

    seen = {}
    for k, c, r in FEATURES:
        if (c, r) in seen:
            out.append("FAIL   two features share cell %s: %s and %s"
                       % (ref(c, r), seen[(c, r)], k))
            ok = False
        seen[(c, r)] = k
    out.append("panel  %d features across %d cells" % (len(FEATURES), COLS * ROWS))

    return ok, out


if __name__ == "__main__":
    ok, lines = check()
    for line in lines:
        print(line)
    print("OK" if ok else "CHECK FAILED")
    sys.exit(0 if ok else 1)
