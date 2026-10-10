---
id: PZ-004
title: What’s in the horn
type: puzzle
# idea | candidate | decided | built | parked
status: decided
# The structure beat this puzzle belongs to (one ID)
beat: ST-005
# Props the player needs, e.g. [PP-001]
props: [PP-017, PP-018, PP-022]
# Puzzles that must be solved first, e.g. [PZ-002]
needs: [PZ-003]
# cipher | physical | search | logic | wordplay | other
mechanic: wordplay
# 1 (easy) to 3 (hard)
difficulty: 2
# Lock it opens: 3-digit | 4-digit | 4-letter | 3-digit-colour (blank if none)
lock: 4-letter
answer: MEAD
# Compartment this lock closes (shown on the Locks tab)
container: Main compartment
# What players call this lock on the hint page, e.g. "The luggage tag" (spoiler-free)
hint_title: Lock 4
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
tags: [old-PZ-20]
---

## How it works

Three postcards each hide one attribute word behind a different riddle technique; only one drink fits all three.

Lock 4 of 13 in the release order decided 7 Oct 2026 (Q-005). Difficulty 2 of 3 is Claude's estimate from the mechanism (number of props and steps), not playtest data.

**9 Oct 2026 (designer, Q-001):** now lock 4 of 13. Compartment: main compartment.

## Player notices

Postcard H3 (Kyiv), postcard H2 (Staraya Ladoga) and postcard HD (Constantinople) — HD stops being a pure decoy and takes on this leg’s third lock, closing the “Constantinople still needs one assigned” gap in the [Final riddle tab].

## Player does

Solve each card’s riddle for its one word — HONEY, DRINK, FERMENTED — using a different technique per card so no two feel the same, then combine the three attributes: the only drink that is honey, fermented and a drink is `MEAD`.

## Player obtains

Code **MEAD**. Opening this lock releases PP-013, PP-030, PP-031, PP-025.

## Story reason

Closes the last open lock of Harald’s leg (PZ-004) without touching the map, which the rune-and-perch branch already uses. Gives HD the real puzzle job every decoy is required to carry ([Final riddle tab]) instead of leaving Constantinople unassigned. H3 and HD are linked by real Rus’-Byzantine history, not only by this puzzle: Oleg of Novgorod made Kyiv the Rus’ capital and, per the Primary Chronicle, sailed on Constantinople in 907 — the treaty that followed gave Rus’ merchants trading rights there. That fact carries H3’s Fun Fact, deliberately not honey/bees, since the riddle itself already is the honey content and a Fun Fact repeating its own answer would break Q-015’s one-fact-per-voice rule. ~~HD’s Fun Fact (Harald’s own Varangian Guard service, 1034–1043, funding his later claim to Norway) is gestured at in its message (“this is where he made his fortune”) but not stated there, so the two never repeat the same content either.~~ **Superseded 26 Sept 2026:** on review this was judged too close after all — same core claim (fortune made here funded the throne), just with dates added. HD’s Fun Fact is now unrelated Constantinople trivia (Varangian runic graffiti in the Hagia Sophia) instead.

## Clue wording

**29 Sept 2026:** H2 and H3 were rewritten in the postcard update (see PZ-004); the riddles and the DRINK acrostic still hold, but the quotes below are the earlier text. **H3 (Kyiv), definition riddle:** “Kyiv next, and it might be the most beautiful city on this whole trip — golden domes catching the light on every hill. Stopped by St. Michael’s this morning and lit a candle for you. Cheesy, I know. Here’s a little riddle for you, the kind we used to trade back and forth: *I’m sweet, but no fruit tree grew me. I’m gold, but no smith ever cast me. Thousands of tiny workers made me and set six-sided walls to guard me.* Love, Aunt Liv.” **H2 (Staraya Ladoga), acrostic:** “Days here move slower than I expected, and I love it. Rurik supposedly ruled from right here, if the old chronicles are true. I climbed up on the fortress wall for a look at the whole river bend. Nobody warned me how far this feels from anywhere else. Keeping my postcards dry has become a full-time job in this weather.” **HD (Constantinople), rebus:** “Constantinople — well, Istanbul now, but I like the old name for this trip. Impossible not to think about Harald everywhere here; this is where he made his fortune, long before Norway ever heard of him. Found this in a little shop near the Hippodrome, couldn’t resist:” followed by a drawn rebus — dotted sugar cubes on a spoon + a yeast packet → a fizzing flask.

## Hints

1. Three cards, three words, one drink.
2. What do you get when honey ferments?
3. Each card hides its word a different way — read one, count one, look at one.

## Solution

Staraya Ladoga spells **DRINK** with the first letter of each of its five sentences. Kyiv’s riddle (sweet but not fruit, gold but not metal, made by thousands, six-sided walls) is **HONEY**. Constantinople’s picture puzzle (sugar feeding yeast, a bubbling flask) means **FERMENTED**. A fermented honey drink is **MEAD**.

## Solution notes

Design-side solution text, kept when the player-facing Solution above was written for the hint page (9 Oct 2026).

H3 → **HONEY** (the riddle: sweet but not fruit, gold but not metal, made by thousands, six-sided walls = honeycomb). H2 → **DRINK**, spelled by the first letter of each of its five sentences (D, R, I, N, K). HD → **FERMENTED**, read from the rebus (sugar feeds yeast, and the bubbling flask depicts the reaction that ferments it). Honey, fermented, and a drink — only `MEAD` fits all three.

## Open risks

All three cards built, front and back, 17 Sept 2026 — see the Postcard system tab gallery for PDFs. H3’s Fun Fact was swapped from an early bees/honey draft to the Oleg-of-Novgorod/Constantinople fact, since a Fun Fact repeating the riddle’s own answer would break Q-015. **29 Sept icon review:** HD’s three small squares do not clearly read as sugar cubes. A [rough yeast + airlock jar + hourglass sketch](../Postcards/HD_Fermentation_Sketch.svg) was a first alternative. Of the four [chemical reaction icons](../Postcards/HD_Reaction_Icon_Options.svg), the user chose **A, the fizzing flask**. After reviewing four [sugar icon options](../Postcards/HD_Sugar_Icon_Options.svg), the user supplied a spoon holding three cubes and asked for small sugar dots on the cubes. The [dotted spoon icon](../Postcards/HD_Sugar_Spoon_Dotted.svg) and [full rebus sketch](../Postcards/HD_Rebus_Sketch_v2.svg) show that direction; that earlier layout still included an hourglass and is now superseded. An ImageGen raster reference was also made from the attached example (the printed icon is vector, redrawn from it). Exact prompt, 29 Sept 2026: *Use case: precise-object-edit Asset type: simple line icon for a small printed escape-game postcard. Primary request: Use the attached spoon-with-three-sugar-cubes icon as the composition reference. Keep one spoon holding three three-dimensional sugar cubes in the same arrangement, with the handle extending to the right. Add a few tiny, sparse dot marks on the visible faces of each cube to suggest sugar crystals. Preserve the clean bold outline and generous empty space. Make the line art dark ink (#263f3a), with no fill shading, no other objects, no words, no border, and no watermark. The dots should be visibly smaller than the outline and should not obscure the cube edges. Output a transparent background.* The print card now uses dotted sugar cubes on a spoon + yeast + a fizzing flask, with no hourglass. **Layout review, 29 Sept (Claude Code):** the spoon handle was shortened to about half so the three icons are similar widths; the packet label is now lettered in Aunt Liv’s hand (“Yeast”) instead of a typeset label; the icons are spaced evenly and centred in the box. **Then, at the user’s request:** the sugar dots are larger (0.4 → 0.63 pt radius) so they survive printing, and the second sign is now an arrow, so the rebus reads sugar + yeast → reaction; both signs are drawn as matching 0.9 pt strokes. Still open: at print size the dotted cubes can look like dice, which the reader test should watch for; and the “Found this in a little shop” lead-in, which does not describe a flask. An unprompted reader test and paper print remain to do. A bottle/glass was also considered but overlaps H2’s DRINK clue. Card order/placement within Harald’s own travel story (per Q-016) is still not chosen for H2, H3 or HD.

## Releases (as worded on the old page)

**Superseded 9 Oct 2026** by the compartment map in Q-001; the current release list is under Player obtains.

**Since 7 Oct 2026 (Q-005):** lock 4; releases decoy postcard LD and Leif’s map. ~~H1, hnefatafl board and pieces, Oslo hnefatafl museum ticket (step 11 of old page PC-18)~~

Lock as recorded: Owned four-letter word lock. Old page status: Decided and built, 17 Sept 2026.

## Design notes (PZ-004: Decided — step 11 of old page PC-18)

**A four-letter word lock on Harald's trail could take `MEAD` as its answer.**

**H2 rewritten, 29 Sept 2026 (user).** The acrostic still spells DRINK, now from “Dinners take hours here…”, “Rurik…”, “I climbed…”, “Nobody…” and “Keeping up with new puzzles for you is starting to be a challenge!”. At the user’s request every wrapped line and the sign-off are indented half a space (about 2.5 pt; first 10 pt, cut later on 29 Sept), so only the five first letters sit on the margin. H3 drops its candle line (the riddle is unchanged); HD is only resized.

Pinned as a candidate, 16 Sept 2026, while reviewing leg 3 (Aud). `MEAD` was the original candidate for the owned four-letter lock before PZ-010 replaced it with `SOLE` for Aud's trail — rather than drop it, the user proposed reusing it on Harald's trail instead. Fits thematically: Harald's crest element set already includes a drinking horn (old page PZ-16). **Not yet designed:** which mechanism produces it — a second physical 4-letter lock (not yet confirmed to exist), a new use for the comb prop (still without a job on Harald's trail per PZ-002), or something else entirely. Deliberately left open rather than forcing a mechanism before leg 4 gets its own review pass.
**Superseded, 23 Sept 2026:** this row was out of date. The mechanism was designed and built on 17 Sept 2026 as “What’s in the horn” (three riddles on H3, H2 and HD give HONEY, DRINK, FERMENTED → `MEAD`; see the Puzzles tab). old page PC-18 puts it at step 11, where it opens the hnefatafl pouch. It uses its own four-letter word lock (Q-026, bought).

PR

### Props and production
