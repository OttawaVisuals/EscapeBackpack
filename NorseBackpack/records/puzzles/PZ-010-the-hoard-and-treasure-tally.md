---
id: PZ-010
title: The hoard and treasure tally
type: puzzle
# idea | candidate | decided | built | parked
status: decided
# The structure beat this puzzle belongs to (one ID)
beat: ST-004
# Props the player needs, e.g. [PP-001]
props: [PP-012, PP-014, PP-037, PP-031, PP-030, PP-026]
# Puzzles that must be solved first, e.g. [PZ-002]
needs: [PZ-005]
# cipher | physical | search | logic | wordplay | other
mechanic: physical
# 1 (easy) to 3 (hard)
difficulty: 3
# Lock it opens: 3-digit | 4-digit | 4-letter | 3-digit-colour (blank if none)
lock: 4-letter
answer: SOLE
# Compartment this lock closes (shown on the Locks tab)
container: Large pouch, in the main compartment
reset_display: LOCK
container_in: PZ-004
# What players call this lock on the hint page, e.g. "The luggage tag" (spoiler-free)
hint_title: Lock 8
# Explicit opt-in for the PUBLIC hint page. Candidates are never published.
publish_hints: yes
# Independent of design/build status: untested | passed | changes-needed
test_status: untested
# physical | digital (a digital walkthrough does not verify a physical prop)
test_method:
# Optional stable Clue Library technique link
technique:
# Any related record IDs, e.g. [PZ-002, Q-004]
links: []
# Set to an ID when this record is replaced. It then moves to the Parked tab.
superseded_by:
tags: [old-PZ-03]
---

## How it works

Sort three real-history coin piles, convert the Viking pile's values, add to 3705, and turn the total upside down to find a word.

Lock 10 of 13 in the release order decided 7 Oct 2026 (Q-005). Difficulty 3 of 3 is Claude's estimate from the mechanism (number of props and steps), not playtest data.

**9 Oct 2026 (designer, Q-001):** now lock 8 of 13. Compartment: large pouch, in the main compartment.

## Player notices

Loose mixed hoard of 12 coins (dirham, denier, Norse), the museum ticket’s Coin Room key, the three icon marks on Aud’s map, A1/A3, calculator or four-wheel tally.

## Player does

Sort the loose coins by face against the ticket’s Coin Room. The fehu rune beside the treasure cave on Aud’s map matches the ticket’s Norse group; add those three coins’ values ($5 + $100 + $3,600 = 3705) and rotate the entire tally 180 degrees.

## Player obtains

Code **SOLE**. Opening this lock releases PP-006, PP-032, PP-033.

## Story reason

Preserves physical sorting and the word reveal without a calibrated scale, and gives each currency's rarity a real-history basis instead of an arbitrary number.

## Clue wording

A1 (rewritten 25 Sept 2026): historical coins that ‘fetch a pretty penny’. A3: ‘my head is spinning’. The cache mark is not stated on any card — players match the map’s icons to the ticket’s.

## Hints

1. Your museum ticket has a coin room. Sort the coins into its three groups.
2. The treasure hunt ended at a cave. Look at the mark beside it on Aud’s map, then find the same mark on the ticket: only those coins count.
3. Add up what those coins are worth on the ticket and set the total on the treasure tally.
4. Turn the whole tally upside down and read the four characters from left to right.

## Solution

The marked group adds up to **3705**, which reads **SOLE** upside down.

## Solution notes

Design-side solution text, kept when the player-facing Solution above was written for the hint page (9 Oct 2026).

3705 in suitable calculator-style digits reads **SOLE** upside down. No decimal or discarded digit.

## Open risks

Display choice remains open (PP-026). Check SOLE on the actual rotated display. Decoy marks (camel at G1, fleur-de-lis at C4) give a wrong route a wrong pile: 980 or 1320, neither a word.

## Releases (as worded on the old page)

**Superseded 9 Oct 2026** by the compartment map in Q-001; the current release list is under Player obtains.

**Since 7 Oct 2026 (Q-005):** lock 10; releases postcards R3, R4 and R5. ~~Decoy card AD and Aud’s comb (step 8 of old page PC-18). Updated 25 Sept 2026; the reviewed flow sent SOLE straight to Harald with the comb optional.~~

Lock as recorded: Dedicated four-letter lock; check dial letters. Old page status: Tally approved · coins and display need proof.

## Design notes (PZ-010: Mechanism approved · print changes pending)

**Aud’s coin-value tally gives SOLE.**

Three piles, one per real-history currency (dirham/denier/Viking), each its own small natural find with a common-to-rare spread. The cache mark (the fehu rune beside the treasure cave, matched to the ticket’s Coin Room key, 24 Sept 2026) selects the Viking pile from the loose hoard; its three coins (rates 5, 100, 3600) convert to 3705, recorded and rotated to read SOLE. A1 and A3 messages rewritten by the user and rebuilt, 25 Sept 2026 (“pretty penny”, “head is spinning”). See Approved changes and [the hoard prop] for the full currency/coin design. Device choice and physical coin fabrication remain open (PP-026/25).

**Superseded specification · before 22 September 2026**

PZ-010 Answer decided; card assignment revised 16 Sept 2026

Aud’s coin weight supplies the owned four-letter-lock answer.

**Revised 16–17 Sept 2026.** The weighing instruction moved from Hvammur to Dögurðarnes, since Hvammur was reassigned to the treasure-map code step (PZ-006). Esjuberg’s half is unchanged. The map code is now the three-digit plot sum `467` (redesigned 17 Sept 2026, superseding `4816`); its clue copy and final artwork remain open.

**Changed from a five-letter to a four-letter lock:** the owned lock takes `SOLE`; `KAMBR` (5 letters) is dropped from this slot and `MEAD` is superseded (now a pinned idea for Harald’s trail instead, PZ-004).
**Mechanism:** after the treasure-map code opens the hoard, players sort all released coins into their three types. The treasure square’s cache mark identifies the one pile to weigh. Dögurðarnes gives the weighing task; Esjuberg’s upside-down art and Liv’s scale-display sketch, with the final digit crossed out, tell players to read `370.56` as `370.5`, then upside down as `SOLE`.
**Still open:** exact route clues, coin designs/counts and physical mass calibration (PZ-006, PP-037).
