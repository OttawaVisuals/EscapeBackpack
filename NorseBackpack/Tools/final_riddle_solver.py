"""SUPERSEDED 20 Sept 2026 -- kept as history, not used by anything.

This solved the INTERLEAVED calendar: all four trails woven across one year, so
22 cards had to be placed into 22 global positions. That model is gone. Liv now
completes each leg before starting the next, which makes the legs independent
and the search small enough to run exhaustively -- see final_riddle_clues.py,
which no longer imports this file.

Worth remembering why: the space here was large enough that the run capped at
400,000 calendars, and a capped run can report a pass that is not real. It did
exactly that once, on a variant that dropped two of Leif's position clues.

Original docstring follows.

Constraint solver for the Norse final riddle (PZ-18).

Checks the tests named in the Final riddle tab's Validation section:
  1. unique answer (per-trail order of real cards + first-appearance order)
  2. the final bundle actually gates (without it, >1 answer)
  4. rules hold (stated gaps are multiples of 3 days; first appearances run
     Leif, Rollo, Aud, Harald)

Solves slot-by-slot (1..22) so ordering clues prune immediately.
"""
import sys
from datetime import date, timedelta

sys.stdout.reconfigure(encoding='utf-8')

N = 22
START = date(2026, 3, 1)
SLOT_DAYS = 3

TRAILS = {
    'leif':   (['L1', 'L2', 'L3'], 'LD'),
    'rollo':  (['R1', 'R2', 'R3', 'R4', 'R5', 'R6'], 'RD'),
    'aud':    (['A1', 'A2', 'A3'], 'AD'),
    'harald': (['H1', 'H2', 'H3', 'H4', 'H5', 'H6'], 'HD'),
}
TRAIL_ORDER = ['leif', 'rollo', 'aud', 'harald']

CARDS, TRAIL_OF, IS_REAL = [], {}, {}
for _t, (_reals, _decoy) in TRAILS.items():
    for _c in _reals:
        CARDS.append(_c); TRAIL_OF[_c] = _t; IS_REAL[_c] = True
    CARDS.append(_decoy); TRAIL_OF[_decoy] = _t; IS_REAL[_decoy] = False

PLACES = {
    'L1': "L'Anse aux Meadows", 'L2': 'Battle Harbour', 'L3': 'Qikiqtarjuaq',
    'LD': 'Brattahlid  [decoy]',
    'R1': 'Chalus', 'R2': 'Rouen', 'R3': 'Bayeux', 'R4': 'Winchester',
    'R5': 'Battle', 'R6': 'Roumare Forest', 'RD': 'Walcheren  [decoy]',
    'A1': 'Dogurdarnes', 'A2': 'Hvammur', 'A3': 'Esjuberg',
    'AD': 'Bjarnarhofn  [decoy]',
    'H1': 'Oslo', 'H2': 'Staraya Ladoga', 'H3': 'Kyiv', 'H4': 'Hedeby',
    'H5': 'Aci Castello', 'H6': 'Patara', 'HD': 'Constantinople  [decoy]',
}


def slot_date(s):
    return START + timedelta(days=SLOT_DAYS * (s - 1))


def fmt(s):
    return slot_date(s).strftime('%-d %b') if sys.platform != 'win32' \
        else slot_date(s).strftime('%d %b').lstrip('0')


class C:
    def __init__(self, kind, args, src, bundle=False):
        self.kind, self.args, self.src, self.bundle = kind, args, src, bundle

    def __repr__(self):
        return f'{self.kind}{self.args}'


def solve(cons, limit=500000):
    """Place cards into slots 1..N in ascending slot order."""
    fixed = {}
    for con in cons:
        if con.kind in ('fix', 'pos'):   # 'pos' = position stated in card text
            c, s = con.args
            if c in fixed and fixed[c] != s:
                return []          # contradictory anchors
            fixed[c] = s
    slot_fixed = {s: c for c, s in fixed.items()}
    if len(slot_fixed) != len(fixed):
        return []                  # two cards on one slot

    befores = [a for con in cons if con.kind == 'before' for a in [con.args]]
    nexts = [con.args for con in cons if con.kind == 'next']
    gaps = [con.args for con in cons if con.kind == 'gap']
    t_first = [con.args[0] for con in cons if con.kind == 'trail_first']
    t_last = [con.args[0] for con in cons if con.kind == 'trail_last']
    no_decoy_first = any(con.kind == 'no_decoy_first' for con in cons)

    pred_of = {y: x for x, y in nexts}          # y must sit at slot(x)+1
    succ_of = {x: y for x, y in nexts}
    must_follow = {}                            # y -> set of x that precede y
    for x, y in befores:
        must_follow.setdefault(y, set()).add(x)
    gap_pred = {y: (x, d) for x, y, d in gaps}

    out = []
    pos = {}

    def ok_place(c, s, placed):
        if c in fixed and fixed[c] != s:
            return False
        if s in slot_fixed and slot_fixed[s] != c:
            return False
        for x in must_follow.get(c, ()):        # everything before c is placed
            if x not in placed:
                return False
        if c in pred_of:                        # c must sit right after pred
            p = pred_of[c]
            if pos.get(p) != s - 1:
                return False
        if c in gap_pred:
            p, d = gap_pred[c]
            if pos.get(p) != s - d:
                return False
        if c in succ_of and s == N:             # no room for its successor
            return False
        reals = TRAILS[TRAIL_OF[c]][0]
        if c in t_first:                        # nothing real of its trail before
            if any(r in placed for r in reals if r != c):
                return False
        for r in reals:                         # a trail_first sibling must come first
            if r != c and r in t_first and r not in placed and IS_REAL[c]:
                return False
        if c in t_last:                         # every real sibling already placed
            if any(r not in placed for r in reals if r != c):
                return False
        for r in reals:
            if r != c and r in t_last and r in placed and IS_REAL[c]:
                return False
        if no_decoy_first and not IS_REAL[c]:
            if not any(r in placed for r in reals):
                return False
        return True

    def bt(s, placed):
        if len(out) >= limit:
            return
        if s > N:
            out.append(dict(pos))
            return
        cands = [slot_fixed[s]] if s in slot_fixed else \
            [c for c in CARDS if c not in placed and c not in fixed]
        for c in cands:
            if c in placed:
                continue
            if not ok_place(c, s, placed):
                continue
            pos[c] = s
            placed.add(c)
            bt(s + 1, placed)
            placed.discard(c)
            del pos[c]

    bt(1, set())
    return out


def answer_of(p):
    per = tuple(tuple(sorted(TRAILS[t][0], key=lambda c: p[c]))
                for t in TRAIL_ORDER)
    first = tuple(sorted(TRAILS, key=lambda t: min(p[c] for c in TRAILS[t][0])))
    return (per, first)


def show(p):
    inv = {s: c for c, s in p.items()}
    for s in range(1, N + 1):
        c = inv[s]
        print(f'  {s:2}  {fmt(s):>7}  {c:3} {PLACES[c]}')
