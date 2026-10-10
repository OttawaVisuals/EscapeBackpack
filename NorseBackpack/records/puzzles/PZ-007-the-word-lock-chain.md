---
id: PZ-007
title: The word-lock chain
type: puzzle
# idea | candidate | decided | built | parked
status: decided
# The structure beat this puzzle belongs to (one ID)
beat: ST-003
# Props the player needs, e.g. [PP-001]
props: [PP-006, PP-033, PP-032]
# Puzzles that must be solved first, e.g. [PZ-002]
needs: [PZ-010]
# cipher | physical | search | logic | wordplay | other
mechanic: wordplay
# 1 (easy) to 3 (hard)
difficulty: 3
# Lock it opens: 3-digit | 4-digit | 4-letter | 3-digit-colour (blank if none)
lock: 4-digit
answer: 1486
# Compartment this lock closes (shown on the Locks tab)
container: Small pouch, in the main compartment
# What players call this lock on the hint page, e.g. "The luggage tag" (spoiler-free)
hint_title: Lock 9
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
tags: [old-PZ-15]
---

## How it works

Four English word pairs split along the Norman Conquest’s class line. The Rouen card fixes the order, the ticket turns pairs into coordinates, the map turns coordinates into a square-count.

Lock 7 of 13 in the release order decided 7 Oct 2026 (Q-005). Difficulty 3 of 3 is Claude's estimate from the mechanism (number of props and steps), not playtest data.

**9 Oct 2026 (designer, Q-001):** now lock 9 of 13. Compartment: small pouch, in the main compartment.

## Player notices

Postcard R2 (Rouen), the Musée Ducal de Rouen ticket, and Rollo’s trail map with its word icons.

## Player does

Read the four Saxon-register words out of the Rouen message in the order they appear. For each, find its Norman partner on the ticket — the Norman column gives a letter, the Saxon column a number, together a grid coordinate. Find that word’s icon already drawn on Rollo’s map, and count the squares between the icon and the coordinate. Four counts, one per dial of the lock.

## Player obtains

Code **1486**. Opening this lock releases PP-007, PP-008, PP-009.

## Story reason

Gives Rollo’s map a second job besides the final route, and makes the Conquest’s language history the puzzle rather than the flavour. Swapping the directional lock for a numeric one keeps the same props, ticket and map work, just cheaper, more common hardware.

## Clue wording

Postcard R2 uses the four Saxon words in passing, plus a rule-line planting counting as Liv’s habit ("Can’t walk anywhere without counting my steps — always have."). The order they appear in is the solve order. The card text is built. **28 Sept 2026 (postcard update):** that rule line is gone; R2 now closes with “Maybe I should count the distances between my stops to show how many steps I took.” The order fight → people → poultry → inn is unchanged, and no new sentence uses a word from the ticket list.

## Hints

1. Read the Rouen postcard next to the back of the Rouen museum ticket. Some of Liv’s words have a partner on the ticket.
2. The ticket pairs everyday Saxon words (numbered) with their Norman partners (lettered). A matched pair gives a letter and a number: a square on the Granted Lands map.
3. Liv mentions fighting, people, poultry and an inn, in that order. For each word, find its square on the map and count the squares to the little drawing for that word.

## Solution

Fight: **1** square. People (folk): **4**. Poultry (hen): **8**. Inn: **6**. In the postcard’s order the code is **1486**.

## Solution notes

Design-side solution text, kept when the player-facing Solution above was written for the hint page (9 Oct 2026).

Pairs in use: combat/fight, poultry/hen, tavern/inn, people/folk (beef/cow and forest/woodland dropped from the solve, icons left in place, inert). Icon positions and targets: fight H6 → I6 (**1** square), hen I3 → A3 (**8** squares), inn H9 → B9 (**6** squares), folk F11 → F7 (**4** squares) — all four pairs already share a row or column, so the count needed no remeasuring. In the card’s reading order (fight, people, poultry, inn) the code is **1486**.

## Open risks

**No numeric lock is owned yet.** Until one is bought or built, this chain has no destination. Six map icons are placed by `ROLLO_WORDLOCK_ART` in `TravelMap/build_trail_maps_pdf.py`; adding them cost six secondary scenery labels to the sheet’s collision-avoidance. Hastings was already dropped for collision before this puzzle existed. The ticket and print PDF still reflect the old six-word chain and need rebuilding.

## Releases (as worded on the old page)

**Superseded 9 Oct 2026** by the compartment map in Q-001; the current release list is under Player obtains.

**Since 7 Oct 2026 (Q-005):** lock 7; releases postcard H1, Harald’s map, the hnefatafl board kit and the Oslo hnefatafl museum ticket. Which pocket holds it follows Q-001’s remap.

Lock as recorded: 4-digit numeric combo lock — hardware not owned yet. Old page status: Code decided · lock hardware open.

## Design notes (PZ-007: Mechanism redesigned, 19 Sept 2026 — 4-digit numeric lock, code decided)

**The word-lock chain: a Norman/Saxon word-pair puzzle spanning a Rouen postcard, a new museum ticket, and six new icons on Rollo’s map, now ending in a 4-digit numeric lock.**

**Redesigned, 19 Sept 2026 — directional lock dropped for a 4-digit combo lock.** The directional (arrow) lock was judged expensive and finicky hardware. Two changes, made together: (1) the postcard's forest/cow sentence is cut, dropping those two word-pairs from the chain and leaving four (**fight, people/folk, poultry/hen, inn**); (2) the readout changes from "direction from icon to coordinate" to "count the squares between icon and coordinate" — both already lie on a shared row or column, so no remeasuring was needed, only a different reading of numbers already on record.
**The code is `1486`.** In message order: fight (H6→I6) = **1** square, people/folk (F11→F7) = **4** squares, poultry/hen (I3→A3) = **8** squares, inn (H9→B9) = **6** squares.
**Teaching the rule:** R2's message gains a rule-line in the same family as LD's "every little detail counts" (old page PZ-10) — "Can't walk anywhere without counting my steps — always have." (Q-019) — planting counting as Liv's habit rather than stating the mechanism outright. **Replaced 28 Sept 2026:** R2 now closes with “Maybe I should count the distances between my stops to show how many steps I took.”
**The cow and forest icons stay on the map**, per the user's call — inert now, no clue text points at them, left as harmless decoration rather than removed or folded into the ticket's filler pairs.

**The idea.** Several English word pairs split along the Norman Conquest's class line survive into modern English — the peasant raised the animal, the lord ate the Norman word for its meat (*cow/beef*), and the same split runs through law, buildings and everyday verbs. Six pairs were chosen: **beef/cow, poultry/hen, combat/fight, forest/woodland, tavern/inn, people/folk**. **Four now feed the lock** (`combat/fight, people/folk, poultry/hen, tavern/inn`); beef/cow and forest/woodland remain on the map and ticket but are no longer part of the solve.
**Mechanism, three steps.** (1) A postcard uses the four Saxon-register words in passing; the order they appear in is the solve order. (2) A ticket lists all fifteen Saxon words (numbered) against fifteen Norman words (lettered) in two independently-shuffled columns; matching a pair yields a grid coordinate — letter from the Norman side, number from the Saxon side. (3) A new icon for that word already sits on Rollo's map; the number of squares between the icon and the matched coordinate is one dial of the numeric lock.
**Six map icons, built (four now load-bearing, two decorative).Leader lines and towns added, 1 Oct 2026 (PZ-011):** each icon now has a grey dotted line to a real town added for it, which must lie in the **same grid square** as the icon, so counting squares from the town gives the same digit as counting from the icon. Chosen as the largest nearby town meeting that rule with its dot clear of the drawing: cow D1 → Manchester, hen I3 → Eindhoven (Antwerp and Brussels are in H3), fight H6 → Troyes, forest E7 → Saumur (Angers’ dot falls under the trees), inn H9 → Vichy (Clermont-Ferrand’s dot falls under the inn), people F11 → Montauban (Toulouse is in G11). The icons did not move. The coordinates are approximate, from general knowledge, like the sheet’s other added towns (`icon_towns` in `TravelMap/build_trail_maps_pdf.py`). A few labels cross a grid line (Saumur, Vichy, Troyes), but every dot is inside its icon’s square. `ROLLO_WORDLOCK_ART` in `TravelMap/build_trail_maps_pdf.py` places Codex-generated rust-brown icons (cow, hen, combat, forest, inn, folk) on Rollo's sheet — beef/cow at D1, poultry/hen at I3, combat/fight at H6, forest at E7, tavern/inn at H9, people/folk at F11. Each box is offset by a different random amount within its grid cell rather than centred, so six identically-centred icons don't read as a deliberate overlay. Adding them cost six secondary scenery labels to the sheet's own collision-avoidance (Château Gaillard, Coutances, Dives estuary, Le Havre, Pevensey, Évreux) — none are trail stops. Separately, and not caused by this change: **Hastings was already dropped for collision before this puzzle existed** — a pre-existing gap worth a look regardless of this puzzle's fate.
**Six answer coordinates, directions and distances, checked consistent.** Cow → D2 (down, 1 square, unused), Hen → A3 (left, **8 squares**), Fight → I6 (right, **1 square**), Inn → B9 (left, **6 squares**), Forest → E10 (down, 3 squares, unused), Folk → F7 (up, **4 squares**). Each was verified against the icon's actual map position above. These six coordinates fix six of the ticket's thirty tags: Norman letters combat=I, beef=D, poultry=A, tavern=B, forest=E, people=F; Saxon numbers fight=6, cow=2, hen=3, inn=9, woodland=10, folk=7.
**The museum, decided: Musée Ducal de Rouen** ("The Ducal Museum") — fictional, ties to Rollo becoming the first Duke of Normandy rather than a generic conquest reference. Checked against Rouen's real museums (Musée des Beaux-Arts, Historial Jeanne d'Arc, Musée Le Secq des Tournelles) — no collision.
**The ticket, built.** 2 × 3 in, smaller than the museum ticket's 2 × 5.5 in (L'Anse at the time; Brattahlíð since 28 Sept 2026) (PP-024) — this list is 15 rows against that one's 26, so the narrower card still fits two legible columns, unlike the L'Anse back which had to drop to one column once its real front art pinned the physical size. Front: bilingual header, and Codex's `Rollo_Chateau_Robert_Le_Diable_Line_v1.png` castle-outline icon recoloured from black to the shared ink green at build time. Back: headed "WORD GALLERY / peasant speech, Norman French" — plausible exhibit copy that doesn't tip the mechanism, matching how PP-024's ticket hides behind an ordinary-sounding visitor index. The nine filler word pairs (mutton/sheep, venison/deer, flame/fire, table/board, vision/sight, liberty/freedom, serpent/snake, escape/flee, assemble/gather) take the remaining tags, several deliberately spilling past column I or row 11 as camouflage that can never resolve to a real square — the same trick PP-024's A–Z index uses. Built by `Props/RouenTicket/build_rouen_ticket_pdf.py` (PP-033). **Not yet updated for the redesign** — still needs to be checked/rebuilt against the four-word chain.
**Order-clue text, decided — and the puzzle now has a real answer.** The Rouen postcard (stop 2, postcard R2) carries it — see Q-019 for the full message and Fun Fact. Current embedded order: **fight, people, poultry, inn**. Resolved against the coordinates and squares-distances above, that fixes the numeric lock's actual combination in solve order: `1486`.
**Superseded record, kept for history:** the original six-word order (fight, forest, cow, people, poultry, inn) and the directional-lock reading it produced (`RIGHT, DOWN, DOWN, UP, LEFT, LEFT`) are dropped in favour of the above.
**Still open:** which physical lock the numeric clue feeds, and what it releases (Q-001); whether six dropped scenery labels on Rollo's sheet are an acceptable cost or need the icon boxes shrunk; and rebuilding the ticket/postcard print PDFs against the new four-word chain and message text.
