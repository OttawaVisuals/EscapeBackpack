---
id: PZ-002
title: The joined top edge
type: puzzle
# idea | candidate | decided | built | parked
status: decided
# The structure beat this puzzle belongs to (one ID)
beat: ST-002
# Props the player needs, e.g. [PP-001]
props: [PP-002, PP-003, PP-027]
# Puzzles that must be solved first, e.g. [PZ-002]
needs: [PZ-001]
# cipher | physical | search | logic | wordplay | other
mechanic: physical
# 1 (easy) to 3 (hard)
difficulty: 1
# Lock it opens: 3-digit | 4-digit | 4-letter | 3-digit-colour (blank if none)
lock: 4-digit
answer: 1576
# Compartment this lock closes (shown on the Locks tab)
container: Locked pouch inside the front pocket
reset_display: 0000
container_in: PZ-001
# What players call this lock on the hint page, e.g. "The luggage tag" (spoiler-free)
hint_title: Lock 2
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
tags: [old-PC-06]
---

## How it works

Laid together, postcards L2 and L3’s top edges join into a four-digit code, read with the magnifier.

Lock 2 of 13 in the release order decided 7 Oct 2026 (Q-005). Difficulty 1 of 3 is Claude's estimate from the mechanism (number of props and steps), not playtest data.

**9 Oct 2026 (designer, Q-001):** now lock 2 of 13. Compartment: locked pouch inside the front pocket.

## Player notices

Postcards L2 and L3, both in hand once lock 1 has opened (lock 2 until 27 Sept 2026).

## Player does

Lay card L2 against card L3, rotated 180°, so their top edges meet. The cloud fragments printed across the two edges align into four digits; read them with the magnifier. **Changed 7 Oct 2026 (user):** holding the cards up to the light is not needed, the magnifier is enough. ~~Hold card L2 face to card L3, rotated 180° against it, up to a light source.~~

## Player obtains

Code **1576**. Opening this lock releases PP-015, PP-028.

## Story reason

Gives Leif’s trail a third lock from its own cards without adding a fourth card. Establishes early that cards can be combined physically, not just read individually, ahead of harder cross-trail combines later.

## Clue wording

**Written 27 Sept 2026 after playtest 1:** both cards now mention the sky. L2: “The sky here is enormous, though somehow it always looks half finished.” L3: “Between this sky and Markland’s, I think I’ve finally seen the whole thing.” L2’s old “something with claws” line was cut; the tester read it as a beasts clue.

## Hints

1. Read the two new postcards. What do they both say about the sky?
2. Bring the two skies together. The top edges of the cards matter.
3. Turn one card upside down and lay it so its top edge meets the other card’s top edge, both picture side up. Look along the join with the magnifier.

## Solution

Laid top edge to top edge, one card upside down, the cloud fragments across the join read **1576**.

## Solution notes

Design-side solution text, kept when the player-facing Solution above was written for the hint page (9 Oct 2026).

The aligned cloud flecks read **1576**, re-proofed at true 5 × 3.5 in card size and 300 dpi. Since 27 Sept 2026 it opens lock 2 (LD + Leif’s map). ~~Nothing is printed to say what the code opens; it opens the fourth container by fiat until that container is designed.~~ **Artwork method, 27 Sept 2026:** The old 4× join proof shows irregular glyphs about 33–35 px high (about 18–25 px wide) at joined x-centres 350, 620, 880 and 1150 px. On upright L3 those are the source x-centres; on upright L2 they mirror to 1149, 879, 619 and 349 px. For `Illustration_v2`, `Postcards/enlarge_topedge_digits.py` inpaints the old flecks in a 32 × 36 px top-edge working box for each half, extracts their positive pale-on-sky colour difference, and scales that fleck pattern 1.4× in both dimensions around the same x-centre and card-edge seam. This preserves the mottled cloud texture instead of replacing it with solid type. The target visible joined height is about 46–49 px; only the top 50 source rows can change. The v1 sources remain intact. The rebuilt 4× nearest-neighbour proof and 300 dpi top-edge test sheet show 1576 with aligned halves.

## Open risks

~~**No destination yet** — the fourth container’s contents are undesigned. **No in-fiction nudge yet** to try holding two cards together at all.~~ Both resolved 27 Sept 2026 (see release and clue). **Playtest 1:** the digits read too small; the 1.4× artwork enlargement is built and digitally aligned. Physical legibility on the final printed stock still needs retesting. Also the third “line two papers up” gesture in the bag, alongside the hnefatafl offset — worth not adding a fourth.

## Releases (as worded on the old page)

**Superseded 9 Oct 2026** by the compartment map in Q-001; the current release list is under Player obtains.

**Since 7 Oct 2026 (Q-005):** lock 2; releases decoy postcard AD and Aud’s comb. ~~Postcard LD and Leif’s trail map (27 Sept – 7 Oct 2026, playtest 1).~~ ~~The fourth container — contents still undesigned.~~

Lock as recorded: Four-digit padlock. Old page status: Decided · read with the magnifier.

## Design notes (PZ-002: Hold-to-light decided)

**What the hold-to-light pair and the comb-grille set actually yield.**

**Changed 7 Oct 2026 (user):** the L2/L3 join is no longer held up to the light; players lay the two top edges together and read `1576` with the magnifier. It is lock 2 and releases AD + the comb (Q-005).

**Hold-to-light (cards L2/L3) decided:** the `1576` the top-edge join produces is **lock 3** in Leif's sequence (PZ-001) — it opens a fourth container holding new material, not yet designed. **Comb-grille set still has no answer** — cards assigned, mechanism decided, nothing wired to it yet.
