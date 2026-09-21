"""The Norse final riddle (PZ-18): the evidence model, and the validation run.

Run this file to re-check the endgame:

    python NorseBackpack/Tools/final_riddle_clues.py

REWRITTEN 20 Sept 2026 for the blocked-leg model. The spec it encodes is
sections 2c-2g of NorseBackpack/Norse_Brainstorm.html. Change a clue there and
change it here, then re-run.

What changed, and why the solver got simpler
--------------------------------------------
The old model interleaved the four trails across one year, so it had to place 22
cards into 22 global positions -- a space large enough that the run was capped at
400,000 calendars and could report a *false* pass, which it did at least once.

Liv now completes each leg before starting the next. That makes the legs
independent: each is enumerated exhaustively on its own (at most 7! = 5040
arrangements), so there is no cap and no false pass. Leg order is not searched at
all -- the three transition tickets chain it directly.

Two rules from the spec drive everything below:

  * A card may not state its own position, and no clue may point at a card other
    than the one in hand. The only two exceptions are L1 and H6, the first and
    last stops of the whole journey, because no ticket precedes Leif and none
    follows Harald.
  * Only the REAL cards need ordering. A decoy's position inside its block is
    never needed: it is filtered out before a line is drawn, and no clue depends
    on where it sat. Enumerating real cards only is what dropped Harald from two
    journal entries to one.
"""
from itertools import permutations
import sys

sys.stdout.reconfigure(encoding='utf-8')

# --------------------------------------------------------------- the deck ----
# leg -> (real cards in the drawn order, decoy, digit)
LEGS = {
    'leif':   (['L1', 'L2', 'L3'], 'LD', '1'),
    'rollo':  (['R1', 'R2', 'R3', 'R4', 'R5', 'R6'], 'RD', '9'),
    'aud':    (['A1', 'A2', 'A3'], 'AD', '7'),
    'harald': (['H1', 'H2', 'H3', 'H4', 'H5', 'H6'], 'HD', '2'),
}
LEG_ORDER = ['leif', 'rollo', 'aud', 'harald']   # fixed by the ticket chain

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

# Harald's H4 names the sea, not a latitude. That matters: Kyiv is south of
# Hedeby (50.5N vs 54.5N), so "heading south" could not have excluded it, while
# "the Mediterranean" does -- Kyiv is the one remaining stop not on a coast.
MEDITERRANEAN = {'H5', 'HD', 'H6'}

# --------------------------------------------------------------- the clues ---
# kind, args, where it lives, what it says. 'src' is one of:
#   CARD    printed on a postcard, readable during play
#   TICKET  one of the three transition tickets, in the final bundle
#   JOURNAL an entry on the "Family iconography" page, in the final bundle
CLUES = [
    # -- Leif ---------------------------------------------------------------
    ('block_first', ('L1',),  'CARD',    'L1  "the first stop on my journey" (permitted exception)'),
    ('block_last',  ('L3',),  'TICKET',  'Leif->Rollo departs Qikiqtarjuaq'),
    # -- Rollo --------------------------------------------------------------
    ('block_first', ('RD',),  'TICKET',  'Leif->Rollo arrives Walcheren'),
    ('block_last',  ('R6',),  'TICKET',  'Rollo->Aud departs Roumare Forest'),
    ('before',      ('R3', 'R5'), 'CARD', 'R5  "after spending hours looking at the tapestry"'),
    ('adjacent',    ('RD', 'R1'), 'JOURNAL', 'Walcheren - Chalus'),
    ('adjacent',    ('R2', 'R3'), 'JOURNAL', 'Train from Rouen (west, short, a museum)'),
    ('adjacent',    ('R3', 'R4'), 'JOURNAL', 'English Channel ferry (tapestry behind, battlefield ahead)'),
    # -- Aud ----------------------------------------------------------------
    ('block_first', ('A1',),  'TICKET',  'Rollo->Aud arrives Dogurdarnes'),
    ('block_last',  ('A3',),  'TICKET',  'Aud->Harald departs Esjuberg'),
    # -- Harald -------------------------------------------------------------
    ('block_first', ('H1',),  'TICKET',  'Aud->Harald arrives Oslo'),
    ('block_last',  ('H6',),  'CARD',    'H6  "the last stop of my travels for now" (permitted exception)'),
    ('med_split',   ('H4',),  'CARD',    'H4  "from here I\'m turning south: nothing but Mediterranean"'),
    ('adjacent',    ('H2', 'H3'), 'JOURNAL', 'Staraya Ladoga - Kyiv'),
]

LEG_OF = {}
for _leg, (_reals, _decoy, _digit) in LEGS.items():
    for _c in _reals + [_decoy]:
        LEG_OF[_c] = _leg


def block(leg):
    reals, decoy, _ = LEGS[leg]
    return reals + [decoy]


def holds(order, kind, args):
    """Does one candidate block ordering satisfy one clue?"""
    pos = {c: i for i, c in enumerate(order)}
    if kind == 'block_first':
        return pos[args[0]] == 0
    if kind == 'block_last':
        return pos[args[0]] == len(order) - 1
    if kind == 'before':
        return pos[args[0]] < pos[args[1]]
    if kind == 'adjacent':
        return pos[args[1]] == pos[args[0]] + 1
    if kind == 'med_split':
        pivot = pos[args[0]]
        return all((pos[c] > pivot) == (c in MEDITERRANEAN)
                   for c in order if c != args[0])
    raise ValueError(kind)


def solve_leg(leg, clues=None, sources=('CARD', 'TICKET', 'JOURNAL')):
    """Every real-card order this leg admits, given the clues in `sources`."""
    clues = CLUES if clues is None else clues
    mine = [c for c in clues if c[1][0] in LEG_OF and LEG_OF[c[1][0]] == leg
            and c[2] in sources]
    reals = set(LEGS[leg][0])
    out = set()
    for order in permutations(block(leg)):
        if all(holds(order, k, a) for k, a, _s, _d in mine):
            out.add(tuple(c for c in order if c in reals))
    return out


def code(per_leg):
    return ' '.join(LEGS[l][2] for l in LEG_ORDER) if per_leg else ''


# ------------------------------------------------------------ validation -----
def main():
    print('NORSE FINAL RIDDLE  -  validation run  (blocked-leg model)')
    print('=' * 72)
    print('Each leg enumerated exhaustively over its own block. No cap, so a')
    print('pass here cannot be an artefact of an enumeration limit.\n')

    levels = [
        ('cards', ('CARD',)),
        ('+tickets', ('CARD', 'TICKET')),
        ('+journal', ('CARD', 'TICKET', 'JOURNAL')),
    ]
    print('orders each leg still admits, as evidence is added')
    print(f'{"leg":<9}{"block":>6}' + ''.join(f'{n:>11}' for n, _ in levels))
    print('-' * 72)
    counts = {}
    for leg in LEG_ORDER:
        row = [len(solve_leg(leg, sources=src)) for _n, src in levels]
        counts[leg] = row
        print(f'{leg:<9}{len(block(leg)):>6}' + ''.join(f'{n:>11}' for n in row))

    full = {leg: solve_leg(leg) for leg in LEG_ORDER}
    unique = all(len(v) == 1 for v in full.values())
    gated = any(counts[leg][1] > 1 for leg in LEG_ORDER)

    print('-' * 72)
    print(f'TEST 1  every leg has one answer ..... {"PASS" if unique else "FAIL"}')
    print(f'TEST 2  the journal actually gates ... {"PASS" if gated else "FAIL"}'
          f'   (without it, Rollo admits {counts["rollo"][1]} and Harald {counts["harald"][1]})')
    print('TEST 3  no decoy reads as a shape .... NOT RUN  (geometric; needs the map projections)')
    print('TEST 4  leg order ..................... not searched -- the three '
          'transition tickets chain it directly')

    if unique:
        print('\nANSWER')
        for leg in LEG_ORDER:
            seq = next(iter(full[leg]))
            print(f'   {leg:<7} {" -> ".join(seq):<34} digit {LEGS[leg][2]}')
        print(f'\n   route code  {code(True)}')

    # Every clue must earn its place: drop it and the leg should get worse.
    print('\nDROP-ONE  (a clue that changes nothing is dead weight)')
    print('-' * 72)
    for idx, (kind, args, src, desc) in enumerate(CLUES):
        leg = LEG_OF[args[0]]
        kept = CLUES[:idx] + CLUES[idx + 1:]
        n = len(solve_leg(leg, clues=kept))
        flag = 'load-bearing' if n > 1 else 'REDUNDANT'
        print(f'   {flag:<13} {src:<8} {desc}')
        if flag == 'REDUNDANT':
            print(f'   {"":13} ^ {leg} still resolves without it -- check the spec')

    print('\nBLOCK ORDERS (real cards plus the decoy, for the record)')
    print('-' * 72)
    for leg in LEG_ORDER:
        reals = set(LEGS[leg][0])
        orders = [o for o in permutations(block(leg))
                  if all(holds(o, k, a) for k, a, _s, _d in CLUES
                         if a[0] in LEG_OF and LEG_OF[a[0]] == leg)]
        real_orders = {tuple(c for c in o if c in reals) for o in orders}
        print(f'   {leg:<7} {len(orders):>3} block arrangement(s) -> '
              f'{len(real_orders)} real order(s)')
        if len(orders) > 1:
            print(f'   {"":7} the decoy floats, which costs nothing: '
                  f'its position is never used')


if __name__ == '__main__':
    main()
