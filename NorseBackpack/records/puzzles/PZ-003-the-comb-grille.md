---
id: PZ-003
title: The comb grille
type: puzzle
# idea | candidate | decided | built | parked
status: decided
# The structure beat this puzzle belongs to (one ID)
beat: ST-004
# Props the player needs, e.g. [PP-001]
props: [PP-015, PP-028]
# Puzzles that must be solved first, e.g. [PZ-002]
needs: [PZ-002]
# cipher | physical | search | logic | wordplay | other
mechanic: physical
# 1 (easy) to 3 (hard)
difficulty: 1
# Lock it opens: 3-digit | 4-digit | 4-letter | 3-digit-colour (blank if none)
lock: 4-letter
answer: BOOK
# Compartment this lock closes (shown on the Locks tab)
container: Left pocket (seen from the front)
# What players call this lock on the hint page, e.g. "The luggage tag" (spoiler-free)
hint_title: Lock 3
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
tags: []
---

## How it works

Aud’s comb, laid upright on the decoy card’s message, covers every line except the four its broken teeth leave open.

Lock 3 of 13 in the release order decided 7 Oct 2026 (Q-005). Difficulty 1 of 3 is Claude's estimate from the mechanism (number of props and steps), not playtest data.

**9 Oct 2026 (designer, Q-001):** now lock 3 of 13. Compartment: left pocket (seen from the front).

## Player notices

The comb and decoy postcard AD (Bjarnarhöfn), both released by lock 2 (1576) since 7 Oct 2026 (Q-005); ~~both released by SOLE~~.

## Player does

Sit the comb’s two end ring-and-dots over the two printed on AD, handle in the left margin, teeth across the message. One tooth covers each line. Read the first letter showing on each line that is not covered.

## Player obtains

Code **BOOK**. Opening this lock releases PP-017, PP-018, PP-022.

## Story reason

Gives the comb a job as an instrument rather than a keepsake, and gives the Aud decoy a reason to be kept rather than discarded.

## Clue wording

AD’s message: "At her brother’s harbor — the one Aud wintered in. I’ve read everything I could find about her this trip, to the point that she feels like family (and she actually maybe was). It was so awesome to find that comb alongside the coins, and the museum let me keep it! This is actually the real treasure, a piece of history that we can use!" The ring-and-dots on AD match the ones on the comb (and on AD’s own stamp).

## Hints

1. The two ring-and-dots on the card match the two on the comb.
2. Line the comb up so its holes sit over the printed dots — handle on the left, teeth over the writing.
3. Some teeth are broken. Read the first letter you can see on each line they leave open, from top to bottom.

## Solution

With the comb in place only four lines show: **b**rother’s harbor… / **o**uld find about / **o**ngside the coins… / **k**eep it! Reading the first visible letter of each, top to bottom: **BOOK**.

## Solution notes

Design-side solution text, kept when the player-facing Solution above was written for the hint page (9 Oct 2026).

**Decided 25 Sept 2026.** With the comb in place only four lines show: **b**rother’s harbor… / **o**uld find about / **o**ngside the coins… / **k**eep it! — B O O K, top to bottom. BOOK links to **Landnámabók** ("Book of Settlements"), the source Q-032 cites for Aud’s comb, and to "I’ve read everything I could find".

## Open risks

Test print pending: the seven intact teeth are 52 mm long and 2.2 mm wide, and the marks sit 4.5 mm from the card edge, so trimming must be accurate. The comb is generated from AD’s printed layout by Props/Comb/build_comb.py — any change to AD’s back needs a comb rebuild.

## Releases (as worded on the old page)

**Superseded 9 Oct 2026** by the compartment map in Q-001; the current release list is under Player obtains.

**Since 7 Oct 2026 (Q-005):** lock 3; releases postcards H2, H3 and HD. ~~H4, H5, Harald’s map and the raven’s flights card — entry to Harald’s leg (step 9 of old page PC-18)~~

Lock as recorded: Four-letter word lock (one of the three owned, Q-026). Old page status: Mechanism decided · comb modelled, test print pending.
