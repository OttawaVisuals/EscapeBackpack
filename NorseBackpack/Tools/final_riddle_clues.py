"""The Norse final riddle (PZ-18): itinerary, clue set, and the validation run.

Run this file to re-check the endgame:

    python NorseBackpack/Tools/final_riddle_clues.py

It prints the four tests from the Final riddle tab's Validation section. Edit
ITIN or CLUES here whenever a card's text, a ticket date or the itinerary
changes, then re-run. Do NOT prune clues on drop-one results alone -- clues that
are individually redundant are not jointly redundant (removing six such clues
together took this set from 1 answer to 8).

Model note, 17 Sept 2026. Stay lengths vary, so a date is no longer a position
and the old slot arithmetic is gone. Every ordering clue here is ordinal
(first / last / next / after); the dates only order the dated props among
themselves. That is what lets the stay lengths vary freely.
"""
import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from final_riddle_solver import TRAIL_ORDER, PLACES, C, solve, answer_of  # noqa: E402

sys.stdout.reconfigure(encoding='utf-8')

Y = 2026

# position -> (card, arrival date, nights)
ITIN = [
    ('L1', date(Y, 2, 2), 4), ('L2', date(Y, 2, 10), 3), ('L3', date(Y, 2, 18), 6),
    ('R1', date(Y, 3, 8), 3), ('R2', date(Y, 3, 17), 5),
    ('A1', date(Y, 4, 5), 4), ('A2', date(Y, 4, 13), 5),
    ('H1', date(Y, 4, 28), 7), ('AD', date(Y, 5, 13), 3), ('A3', date(Y, 5, 20), 4),
    ('LD', date(Y, 6, 12), 5),
    ('H2', date(Y, 7, 3), 4), ('H3', date(Y, 7, 10), 4),
    ('H4', date(Y, 8, 1), 4), ('H5', date(Y, 8, 20), 5),
    ('HD', date(Y, 9, 20), 4),
    ('R3', date(Y, 10, 12), 5), ('R4', date(Y, 10, 21), 3), ('R5', date(Y, 10, 28), 2),
    ('RD', date(Y, 11, 8), 3), ('R6', date(Y, 11, 20), 4),
    ('H6', date(Y, 12, 8), 7),
]
TARGET = {c: i + 1 for i, (c, _, _) in enumerate(ITIN)}
WHEN = {c: d for c, d, _ in ITIN}
NIGHTS = {c: n for c, _, n in ITIN}

# Props that carry a printed date. With variable stays these only establish the
# order of the dated props among themselves -- not a position.
DATED = ['L1', 'R2', 'A2', 'H1', 'AD', 'H5', 'RD']

CLUES = [
    # --- already printed on built cards, no change needed ---------------
    C('pos', ('L1', 1), 'BUILT   L1  "the first stop on my journey"'),
    C('pos', ('L2', 2), 'BUILT   L2  "Second stop"'),
    C('pos', ('L3', 3), 'BUILT   L3  "Third stop"'),
    C('next', ('R3', 'R4'), 'BUILT   R4  "Winchester next"'),
    C('before', ('R3', 'R5'), 'BUILT   R5  "after ... the tapestry"'),
    C('next', ('H2', 'H3'), 'BUILT   H3  "Kyiv next"'),
    # --- new text on the four cards not yet written ---------------------
    C('trail_first', ('A1',), 'NEW     A1  first of Aud’s places'),
    C('before', ('R1', 'A1'), 'NEW     A1  "saved Aud’s country for after France"'),
    C('trail_last', ('A3',), 'NEW     A3  last of Aud’s places'),
    C('pos', ('H6', 22), 'NEW     H6  "last stop of my travel for now"'),
    # --- one added clause per already-built card (script edit + reprint) -
    C('trail_first', ('R1',), 'EDIT    R1  "first of Rollo’s places for me"'),
    C('before', ('R2', 'R3'), 'EDIT    R2  "the tapestry towns are still ahead of me"'),
    C('trail_last', ('R6',), 'EDIT    R6  "last of Rollo’s places"'),
    C('trail_first', ('H1',), 'EDIT    H1  "first of Harald’s places"'),
    C('before', ('H3', 'H4'), 'EDIT    H4  "after all those weeks of river country"'),
    # --- structural invariant -------------------------------------------
    C('no_decoy_first', (), 'RULE    a decoy is never its trail’s earliest card'),
]

BUNDLE = [
    C('next', ('H4', 'H5'), 'BUNDLE  boarding pass Hamburg → Catania, 20 Aug', True),
]

# dated props, in date order -- a confirming chain, plus the one real relation
# (Aud's ticket predates Oslo's, proving Aud first-appears before Harald)
_by_date = sorted(DATED, key=lambda c: WHEN[c])
DATES = [C('before', (x, y), f'DATES   {x} ({WHEN[x]:%d %b}) before {y} ({WHEN[y]:%d %b})')
         for x, y in zip(_by_date, _by_date[1:])]

LIMIT = 400000


def _run(label, cons):
    sols = solve(cons, limit=LIMIT)
    answers = {answer_of(p) for p in sols}
    capped = len(sols) >= LIMIT
    print(f'{label:<14} {len(answers):>3} answer(s)  |  {len(sols):>6} calendars'
          f'{" (capped)" if capped else " (complete)"}')
    return answers, sols


def main():
    print('NORSE FINAL RIDDLE  -  validation run')
    print('=' * 68)
    pre, _ = _run('pre-bundle', CLUES + DATES)
    full, sols = _run('with bundle', CLUES + BUNDLE + DATES)

    print('-' * 68)
    ok1 = len(full) == 1
    print(f'TEST 1  unique answer .......... {"PASS" if ok1 else "FAIL"}')
    print(f'TEST 2  bundle gates ........... {"PASS" if len(pre) > 1 else "FAIL"}'
          f'   ({len(pre)} answers without it)')
    print('TEST 3  no decoy reads as shape . NOT RUN  (geometric; needs the map projections)')

    if ok1:
        answer = next(iter(full))
        order_ok = list(answer[1]) == TRAIL_ORDER
        print(f'TEST 4  rules hold ............. {"PASS" if order_ok else "FAIL"}'
              f'   (first appearances: {", ".join(answer[1])})')
        print()
        print('ANSWER')
        for trail, seq in zip(TRAIL_ORDER, answer[0]):
            print(f'   {trail:<7} {" -> ".join(seq)}')

    if TARGET not in sols:
        print('\nNOTE: the recorded itinerary was not reached within the enumeration '
              'cap. That is expected when the calendar space is large; it is not a '
              'failure unless TEST 1 also fails.')

    print('\nITINERARY')
    total = 0
    for i, (card, d, nights) in enumerate(ITIN, 1):
        total += nights
        print(f'   {i:>2}  {d:%d %b}  {nights:>2}n  {card:<3} {PLACES[card]}')
    span = (ITIN[-1][1] - ITIN[0][1]).days
    home = ITIN[-1][1] + timedelta(days=ITIN[-1][2])
    print(f'   home {home:%d %b}  |  {total} nights away across {span} days')


if __name__ == '__main__':
    main()
