---
id: PZ-001
title: The opening puzzle
type: puzzle
# idea | candidate | decided | built | parked
status: decided
# The structure beat this puzzle belongs to (one ID)
beat: ST-001
# Props the player needs, e.g. [PP-001]
props: [PP-001, PP-023]
# Puzzles that must be solved first, e.g. [PZ-002]
needs: []
# cipher | physical | search | logic | wordplay | other
mechanic: logic
# 1 (easy) to 3 (hard)
difficulty: 1
# Lock it opens: 3-digit | 4-digit | 4-letter | 3-digit-colour (blank if none)
lock: 4-digit
answer: 1021
# Compartment this lock closes (shown on the Locks tab)
container: Front pocket
reset_display: 0000
# What players call this lock on the hint page, e.g. "The luggage tag" (spoiler-free)
hint_title: Lock 1
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
tags: [old-PZ-13, old-PC-01]
---

## How it works

Two luggage tags on the bag carry four digits between them. The first postcard says which pair comes first.

Lock 1 of 13 in the release order decided 7 Oct 2026 (Q-005). Difficulty 1 of 3 is Claude's estimate from the mechanism (number of props and steps), not playtest data.

**9 Oct 2026 (designer, Q-001):** now lock 1 of 13. Compartment: front pocket.

## Player notices

The first postcard, which is from L’Anse aux Meadows, and the two luggage tags attached to the backpack. Each tag has a printed “If found, please return to” line that Liv never filled in properly — instead she hand-wrote the address of a hotel she stayed at, and the street number is the only number on the tag.

## Player does

Match the place named on the postcard to the tag whose hotel address is in that place. That tag’s street number is the first half of the code; the other tag’s street number is the second half.

## Player obtains

Code **1021**. Opening this lock releases PP-002, PP-003, PP-027. **8 Oct 2026:** also the magnifier PP-027, packed with L2 and L3 in one of the front pockets (Q-045).

## Story reason

The data is in plain sight on both tags; the only hidden thing is which tag goes first, and the postcard hands that over. It teaches the game’s core habit — the card carries the rule, the props carry the data — at its lightest.

## Clue wording

Postcard L1 names L’Anse aux Meadows as the place it comes from. **28 Sept 2026:** L1’s rewritten message no longer names the place; it says only that the card is from the first stop. L’Anse aux Meadows is now named in the typed Fun Fact, the postmark and the front art’s title.

## Hints

1. Everything you need is already outside the bag.
2. Both tags carry a hand-written address. Only one of them is in a place you have seen before.
3. The postcard names L’Anse aux Meadows. That tag goes first.

## Solution

Tag A: Vinland Trail Lodge, 10 Skipper’s Wharf, L’Anse aux Meadows, NL — matches the postcard, so it reads first: 10. Tag B: Hôtel Rollon, 21 avenue Rollo, Rouen, France — reads second: 21. Code **1021**, the year tree-ring dating placed the Norse at L’Anse aux Meadows.

## Open risks

Supersedes the earlier `0734` mechanism. The underlined `07` already printed on card L1 now has no job — see Q-006. A print-ready PDF exists (`output/pdf/Luggage_Tag_Inserts_Print.pdf`); purchase and physical assembly onto real luggage tags is not confirmed done.

![Luggage tag inserts, print sheet](Props/_Renders/Luggage_Tag_Inserts_Sheet.png)Print sheet

## Releases (as worded on the old page)

**Superseded 9 Oct 2026** by the compartment map in Q-001; the current release list is under Player obtains.

Postcards L2 and L3, together (changed 27 Sept 2026 after playtest 1; was LD + Leif’s map + the museum ticket)

Lock as recorded: Four-digit padlock on the bag itself. Old page status: Decided.

## Design notes (PZ-001: Re-ordered, 27 Sept 2026)

**Leif’s opening lock sequence. **Since 27 Sept 2026:** L1 opens lock 1 (L2 + L3), the join opens lock 2 (LD + map), the beasts chain opens lock 3. ~~Old:~~ card L1 opens lock 1 (decoy card LD + map + ticket), the beasts chain opens lock 2 (cards L2 + L3 together), the L2/L3 hold-to-light join opens lock 3 (a fourth container).**

**Changed 27 Sept 2026 after playtest 1:** the order of locks 2 and 3 is swapped. Lock 1 (`1021`) now releases cards L2 + L3; the hold-to-light join (`1576`) is lock 2 and releases decoy card LD + Leif’s map; the beasts chain (`BEAR 3212`) is lock 3 and releases R2 + Rollo’s map + the Rouen ticket. The museum ticket is in the open back pocket from the start either way. The 16 Sept note below describes the old order.

**Decided, 16 Sept 2026 — resolves the release point PZ-013 had left open.** Card L1 is given at the start. Lock 1 releases decoy card LD together with Leif's map and the museum ticket — not card L2. Lock 2 (the beasts chain, using LD's imprint) then releases cards L2 and L3 together, which puts both hold-to-light halves in hand at once for Lock 3. This supersedes the release column below and the older release wording in [Puzzles & locks], which used to send Lock 1 to card L2 and Lock 2 to card L3 alone.

**Decided in chat.** Card L1 (the luggage-tag puzzle, decided) opens the **first lock**. That lock releases decoy postcard LD, Leif’s trail map and the museum ticket *together*.
Solving the beasts chain (identify the beast from LD's imprint, read its letters off the ticket’s A–Z index) opens a **second lock**, releasing postcards L2 and L3 together.
**Lock 3, added once all three real cards existed:** holding cards L2 and L3 together up to light reveals `1576` across their joined top edges (PZ-002/Q-012) — a code that already existed but had no destination. It now opens a **fourth container** holding new material, not yet designed (what's inside, and what it unlocks next, are both open). That makes Leif's trail alone worth three locks from four cards — a deliberate first-trail density; later trails are expected to ask players to combine cards *across* trails, not just within one, to raise the difficulty.
**Hnefatafl (PZ-008) moved out of this chain.** It should come later in the game, not as the beat immediately after cards L2/L3. Exactly where is undecided — consistent with Q-001/Q-002, which stay deliberately unfrozen until more of the puzzle sequence exists.
**Still open:** what the fourth container holds and what it does; where Hnefatafl lands; and how this three-lock opening maps onto Q-001’s eventual container structure.

## Design notes (PZ-001: Decided)

**The four digits of the opening code, and how each luggage tag shows its place.**

Code is `1021` — the year tree-ring dating placed the Norse at L’Anse aux Meadows. Each tag is a fictional hotel luggage tag: a printed “If found, please return to” line Liv never filled in properly, with a hand-written hotel name and address instead. The street number is the only number on the tag, so it stands out without needing extra emphasis. Tag A: Vinland Trail Lodge, 10 Skipper’s Wharf, L’Anse aux Meadows, NL. Tag B: Hôtel Rollon, 21 avenue Rollo, Rouen, France.
