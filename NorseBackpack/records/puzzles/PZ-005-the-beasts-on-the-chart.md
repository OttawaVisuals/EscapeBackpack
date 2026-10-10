---
id: PZ-005
title: The beasts on the chart
type: puzzle
# idea | candidate | decided | built | parked
status: decided
# The structure beat this puzzle belongs to (one ID)
beat: ST-002
# Props the player needs, e.g. [PP-001]
props: [PP-004, PP-029, PP-024]
# Puzzles that must be solved first, e.g. [PZ-002]
needs: [PZ-009]
# cipher | physical | search | logic | wordplay | other
mechanic: search
# 1 (easy) to 3 (hard)
difficulty: 2
# Lock it opens: 3-digit | 4-digit | 4-letter | 3-digit-colour (blank if none)
lock: 4-digit
answer: 3212
# Compartment this lock closes (shown on the Locks tab)
container: Inside lockable pocket 1
# What players call this lock on the hint page, e.g. "The luggage tag" (spoiler-free)
hint_title: Lock 7
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

A hidden imprint on the decoy card points to one square of Leif’s sea chart. The unlabelled animal drawn there names the key to a lookup on the museum ticket.

Lock 5 of 13 in the release order decided 7 Oct 2026 (Q-005). Difficulty 2 of 3 is Claude's estimate from the mechanism (number of props and steps), not playtest data.

**9 Oct 2026 (designer, Q-001):** now lock 7 of 13. Compartment: inside lockable pocket 1.

## Player notices

Leif’s trail map — a North Atlantic sea chart with seven animal vignettes drawn into the empty water and land — decoy postcard LD, which points into it, and the museum ticket (Viking Museum of Brattahlíð since 28 Sept 2026). The card and the map arrive together from lock 4 (MEAD) since 7 Oct 2026 (Q-005); ~~from the hold-to-light lock (lock 2, 27 Sept – 7 Oct 2026)~~. ~~The ticket is in hand from the start.~~ Since 9 Oct 2026 the card, the map and the ticket all arrive together from lock 6 (counting, PZ-009).

## Player does

Follow the decoy card’s imprint to one beast on the chart, identify it from how and where it is drawn, then read its four letters off the A–Z visitor index printed on the back of the ticket. Each letter gives one digit.

## Player obtains

Code **3212**. Opening this lock releases PP-012, PP-014, PP-037, PP-026.

## Story reason

It gives Leif’s map a job on the *front*, using the geography rather than just the paper. It is a transformation chain rather than a pointer: the map’s answer becomes the key that operates the next prop, so neither object is any use alone.

## Clue wording

**27 Sept 2026 (playtest 1):** LD’s message now says “Funny how a name can cast a spell like that”, a subtle nudge that the beast’s name is spelled out on the ticket index. The generic rule line is decided (old page PZ-10): “You know me — every little detail counts.” Card LD carries the specific pointer as a printed imprint, `Vinland Editions · Series F, No. 1` → square F1. **28 Sept 2026 (postcard update):** LD rewritten; the word *spell* is now underlined (the user’s choice, for now) and the card closes with “I hope you enjoy this puzzle, there might be a few steps to get the final code.” The museum ticket is renamed to Brattahlíð to match LD.

## Hints

1. The chart is not empty. Something is drawn where the card is pointing.
2. Are you certain which animal that is? Look at its pose and silhouette, not only its location.
3. It is a bear. Read B, E, A, R off the index on the back of the museum ticket.

## Solution

The postcard points to square F1 on the sea chart, where the bear is drawn. Reading B, E, A, R off the museum ticket’s visitor index gives **3212**.

## Solution notes

Design-side solution text, kept when the player-facing Solution above was written for the hint page (9 Oct 2026).

Seven beasts, each a four-letter word: **BEAR, WOLF, SEAL, ORCA, LOON, HARE, DEER**. None is labelled; each is drawn in a setting or pose that makes it identifiable. Square F1 holds the bear, so the key is BEAR, and B/E/A/R read off the ticket index as **3212**. The other six beast codes are recorded in PP-024 in case the live pointer ever changes. The chart artwork is finished — see `TravelMap/build_trail_maps_pdf.py`.

## Open risks

**No validator, by choice** — the lock is the check. **Bear vs. wolf confirmed legible and distinct at print size, 19 Sept 2026** — no longer an open risk. Artwork is print-ready (`output/pdf/Trail_Map_1_Leif_Print.pdf`).

## Releases (as worded on the old page)

**Superseded 9 Oct 2026** by the compartment map in Q-001; the current release list is under Player obtains.

**Since 7 Oct 2026 (Q-005):** lock 5; releases postcard A2, Aud’s map and Aud’s Treasure Museum ticket. ~~Postcard R2, Rollo’s trail map and the Rouen museum ticket (changed 27 Sept 2026: this is now lock 3, the last of Leif’s leg)~~

Lock as recorded: Four-digit padlock. Old page status: Decided · art finished.
