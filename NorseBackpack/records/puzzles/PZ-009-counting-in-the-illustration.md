---
id: PZ-009
title: Counting in the illustration
type: puzzle
# idea | candidate | decided | built | parked
status: decided
# The structure beat this puzzle belongs to (one ID)
beat: ST-003
# Props the player needs, e.g. [PP-001]
props: [PP-005, PP-010, PP-011]
# Puzzles that must be solved first, e.g. [PZ-002]
needs: [PZ-006]
# cipher | physical | search | logic | wordplay | other
mechanic: search
# 1 (easy) to 3 (hard)
difficulty: 2
# Lock it opens: 3-digit | 4-digit | 4-letter | 3-digit-colour (blank if none)
lock: 3-digit
answer: 562
# Compartment this lock closes (shown on the Locks tab)
container: Large pouch, in the main compartment
reset_display: 000
container_in: PZ-004
# What players call this lock on the hint page, e.g. "The luggage tag" (spoiler-free)
hint_title: Lock 6
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
tags: [old-PZ-19]
---

## How it works

Three Rollo-trail fronts each hide a count of one repeated object. Their Fun Facts fix the order.

Lock 9 of 13 in the release order decided 7 Oct 2026 (Q-005). Difficulty 2 of 3 is Claude's estimate from the mechanism (number of props and steps), not playtest data.

**9 Oct 2026 (designer, Q-001):** now lock 6 of 13. Compartment: large pouch, in the main compartment.

## Player notices

Postcards R1 (Châlus), R6 (Roumare Forest) and the decoy RD (Walcheren). Nothing else.

## Player does

Count the repeated object on each front. Read each card’s typed Fun Fact for its date, put the three in chronological order, and read the counts in that order.

## Player obtains

Code **562**. Opening this lock releases PP-004, PP-029, PP-024.

## Story reason

Gives the only three Rollo-trail cards without a lock job one, satisfying PZ-013’s rule that every card gates a lock. The doubling step keeps it from being plain counting.

## Clue wording

Each handwritten message names the counted object in passing without stating a number. Roumare’s message alone adds an in-voice hint that its count is doubled. All three messages are built.

## Hints

1. Look closely at the pictures on three of the postcards. Each message mentions something small in passing.
2. Count the Viking boats at Walcheren, the wild boars in Roumare Forest and the crossbow bolts at Châlus. Use the magnifier: some hide well. Read Roumare’s message again before you settle on its number.
3. The Fun Facts on the backs date each place. Put the counts in date order. Liv thinks there were twice as many boars as she saw.

## Solution

Walcheren **5** boats (before 911), then Roumare **3** boars doubled to **6** (911), then Châlus **2** crossbow bolts (1199): **562**.

## Solution notes

Design-side solution text, kept when the player-facing Solution above was written for the hint page (9 Oct 2026).

Walcheren **5** boats (before 911) → Roumare **3** boars drawn, doubled to **6** per the card’s hint (911) → Châlus **2** crossbow bolts (1199). Code **562**. The order mirrors the Rollo → William → Richard family line already carried by the Bayeux/Winchester/Battle cards.

## Open risks

Walcheren and Roumare rest on weak history — `stops.js` rates them *uncertain* and *context*. Both cards hedge in message and Fun Fact rather than stating the association as fact. Châlus is solidly documented.

## Releases (as worded on the old page)

**Superseded 9 Oct 2026** by the compartment map in Q-001; the current release list is under Player obtains.

**Since 7 Oct 2026 (Q-005):** lock 9; releases postcards A1 and A3 and the mixed coin hoard.

Lock as recorded: Three-digit lock. Old page status: Decided.

## Design notes (PZ-009: Code decided (562), all three messages built, 16 Sept 2026)

**"Counting in the illustration": a lock fed by Châlus, Roumare and the Walcheren decoy together — the only three Rollo-trail cards without an assigned lock job (PZ-013's "every card gates a lock" rule).**

**Mechanism revised, 16 Sept 2026.** The sorting job moved from the handwritten message to the typed Fun Fact: each card's Fun Fact states a real date/century, and reading the three in chronological order gives the digit order. The handwritten message instead just carries the counted object in passing (boats/boars/bolts, no number stated) — and, on Roumare only, an in-voice hint that the count shown is doubled for the actual digit, adding a step beyond plain counting. This replaces the "in-voice sequencing phrase" version below, which put the ordering job in the handwriting instead.

**Mechanism, decided in chat.** Each of the three front illustrations hides a count of one small repeated object; players read the count off the art (Roumare's is doubled per its message's hint). Concatenating the three digits, in the order fixed by each card's Fun-Fact date, is the lock code.
**Order decided, real (if uneven) history behind it:Walcheren → Roumare → Châlus.** This mirrors the existing Rollo → William → Richard family-line thread already carried by the Bayeux/Winchester/Battle cards.

- **Walcheren (earliest — "before 911").** Some accounts (via Dudo of Saint-Quentin) place Rollo raiding or wintering in Frisia/Zeeland before he became Duke of Normandy in 911. Evidence category `uncertain` in `stops.js` — real but shaky, and the card's message hedges ("the old chronicles are to be believed") rather than stating it as settled fact. Fun Fact rewritten 26 Sept 2026 to stop echoing that same hedge in almost the same words — it now states the "before 911" turning point directly, still without over-claiming Rollo's presence.
- **Roumare (middle — 911).** A forest just outside Rouen, Rollo's own capital, granted to him in 911. Its Rollo association is a local naming legend, not an established fact — evidence category `context` in `stops.js`, the weakest tier. The message hedges ("nobody can really pin the story down"). Fun Fact rewritten 26 Sept 2026 to stop echoing that hedge ("no source can confirm it") — it now states the 911 Saint-Clair-sur-Epte treaty itself, which anchors the date without repeating the message's shrug.
- **Châlus (latest — 1199).** Solid, well-documented history: Richard the Lionheart, Rollo's descendant five generations down, was fatally wounded by a crossbow bolt during the 1199 siege here. Evidence category `supported` — no hedging needed, and already the target of Bayeux's CROSSBOW BOLT rebus (PZ-011), so the place is already "live" in players' heads before this lock. Fun Fact rewritten 26 Sept 2026 — the message already tells the full bolt/shoulder/gangrene story, so the Fun Fact was just retelling it; it now states the lineage span instead, still anchored to 1199.

**What each illustration counts, and the doubling twist:Decided 16 Sept:** Walcheren is 5 Viking boats (read as-is), Roumare is 3 boars in the art but the message hints to double it to 6, and Châlus is 2 crossbow bolts (read as-is); the decided code, in the Walcheren → Roumare → Châlus order, is **562**. Checked against every other code in the page (`1021`, `1576`, `1972`, `231`, `253`, `427`, `582`, `2468`) — no collision. Walcheren's 5 was deliberately not doubled: 5×2=10 isn't a valid single lock digit, so only Roumare (3→6) or Châlus (2→4) could take the twist; the user chose Roumare as easier to weave into the text naturally.

- **Roumare = 3 drawn, reads as 6.** Codex's art has three wild boars at three different visibility levels (one clear in the right foreground, one crossing the path in the background, one mostly hidden in ferns at bottom left). The card's message closes with "for every one I actually saw, I'd bet good money there was a second one just out of sight" — the in-voice cue to double the drawn count.
- **Châlus = 2 crossbow bolts, read as-is.** One small bolt is lodged in the left round tower's sunlit masonry and one lies on the low foreground wall. Both are deliberately subtle but countable; no doubling here.
- **Walcheren = 5 Viking boats, read as-is.** Five individually findable longships are spread across the North Sea above the dune foreground.

**All three messages and Fun Facts built,** in `build_postcard_{R1,R6,RD}_pdf.py`: R1 Châlus (plain historical statement, since evidence is `supported`), R6 Roumare (hedged legend plus the doubling hint) and RD Walcheren (hedged, ties to Rollo's own disputed pre-Normandy raiding, placed as a detour before her real Rollo-trail stops per Q-016). Backs, print PDFs and gallery entries are built for all three.
**Still open:** what physical lock this feeds (Q-001); and placing the built double-sided-axe decoy mark on Walcheren without contradicting this illustration-counting job.
