---
id: PZ-011
title: The rebus distance
type: puzzle
# idea | candidate | decided | built | parked
status: decided
# The structure beat this puzzle belongs to (one ID)
beat: ST-003
# Props the player needs, e.g. [PP-001]
props: [PP-007, PP-008, PP-009, PP-025, PP-032]
# Puzzles that must be solved first, e.g. [PZ-002]
needs: [PZ-007]
# cipher | physical | search | logic | wordplay | other
mechanic: wordplay
# 1 (easy) to 3 (hard)
difficulty: 3
# Lock it opens: 3-digit | 4-digit | 4-letter | 3-digit-colour (blank if none)
lock: 3-digit
answer: 120
envelope_marks: ᛁᛉᚲᛇ
# Compartment this lock closes (shown on the Locks tab)
container: Envelope 10
reset_display: 000
# What players call this lock on the hint page, e.g. "The luggage tag" (spoiler-free)
hint_title: Just opened ᛒᚠᛞᛉ
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
tags: [old-PZ-14]
---

## How it works

The Bayeux card explains why Liv’s postcards start carrying tapestry-style drawings — and carries the first rebus itself. Winchester carries the second. Battle names which ruler scale to use.

Lock 11 of 13 in the release order decided 7 Oct 2026 (Q-005). Difficulty 3 of 3 is Claude's estimate from the mechanism (number of props and steps), not playtest data.

**9 Oct 2026 (designer, Q-001):** now lock 10 of 13. Compartment: large pouch, in the main compartment.

**11 Oct 2026 (designer, PR-007):** no locks or pockets any more. This code, set on the rune cypher wheel (PP-047), points to envelope 10, which holds what lock 10 used to close.


**11 Oct 2026 (playtest 1 feedback, built same day):** **rebus icons now pencil style.** Players found the coloured icons did not read as Liv's own drawings. `Postcards/pencil_rebus.py` turns the existing icons into graphite sketches (outlines + diagonal hatching, no colour) at build time; R3, R4 and R5 use it, and R5's colon dots are graphite too. Source PNGs untouched. Chosen in chat as the quick fix for the next playtest; Codex may still redraw them as true pencil art (swap the filenames).

**15 Oct 2026 (playtest feedback, designer): redesign decided, not built.** Players found the ruler step poor, and did not know "crossbow bolt". Direction chosen in chat:
- **Ruler is a cheap printed cardboard card** (PP-025) with a scale on each long edge, labelled with a **picture rebus instead of "1:125"**. Edges for now: **LONGSHIP** (long + sheep, the correct edge) and **SPEAR** (pear + the letter S, a decoy). A second face with more edges may come later. Scales are no longer real map scales, so the ruler is built to fit the map as it is.
- **Whole-number landing:** on the correct edge, the Châlus to Saint-Clair-sur-Epte dot-to-dot distance (83.1 mm, calculated) lands exactly on a numbered mark (the target is the 100 mark, to be fixed when the ruler is drawn). Decoy edges are spaced so the same 83 mm lands between marks, so a wrong edge looks wrong. Tolerance about ±4 mm. This replaces the 0.1 m reading (0.8 mm) in the risks below; **the code 104 and the 10.4 m reading are no longer the plan.** No map nudge is needed.
- **Battle card (R5):** the SCALE 1:125 rebus (hand, die, Roman V) is replaced by a drawing of a **longship** that matches the right edge. R5's message line about the "right scale" will need rewording. Not drawn yet.
- **Crossbow bolt** is defined on Liv's notes card (PP-048), which comes with L1, and R1 already uses the phrase. Simplifying the Bayeux rebus to CROSSBOW (dropping the lightning bolt) was offered and is not decided.
- **Code set to 120, 15 Oct 2026 (designer):** 120 or 130 was preferred to 100 (too round). The ruler is built with the Châlus to Saint-Clair distance (83.126 mm) on the numbered **120** mark of the LONGSHIP edge: 6.93 mm per 10 units, about ±3.5 mm of tolerance. Switching to 130 is one constant (`TARGET` in `Props/LivRuler/build_ruler_pdf.py`, 6.39 mm per 10, about ±3.2 mm). `answer` above and the code in Q-001 and Q-005 now read 120; the old 104 and the 10.4 m reading elsewhere on this page are history. Still to check: the rune markings for this envelope (PR-007, PP-047) and any print files that show 104.

## Player notices

Rollo’s Bayeux, Winchester and Battle postcards (all built), his trail map with its story icons, and the architect’s scale ruler already in the kit.

## Player does

Read each card’s rebus as a word or phrase, find the map icons the first two name, set the ruler to the scale the third names, and measure the distance between the two points.

## Player obtains

Code **104**. Opening this lock releases PP-016, PP-034, PP-035, PP-036.

## Story reason

Gives two props that currently have no job a job together, and gives the margin drawings an in-fiction reason to exist rather than reading as unexplained publisher art.

## Clue wording

None of the three cards states its rebus outright; all three just carry the drawings. **28 Sept 2026 (postcard update):** R3 now asks “can you find what it means?”; R4 adds “I got to enjoy the local custom of a scone and hot beverage” (a nudge towards the teacup); R5 (built 28 Sept 2026) keeps “measure up” and adds “Good thing I packed my old ruler: my maps only make sense at the right scale.” (“they” became “my maps” on 1 Oct 2026) See PZ-011.

## Hints

1. The Bayeux, Winchester and Battle postcards each end with a little picture puzzle. Read them as words.
2. Two of the picture puzzles point to places on the Granted Lands map; the third tells you which scale of the ruler to use.
3. Measure between those two places on the Granted Lands map, dot to dot, with Liv’s ruler. Use the edge that matches the drawing on the Battle postcard.

## Solution

Bayeux: cross + bow + lightning bolt = CROSSBOW BOLT, so Châlus. Winchester: tree + tea = TREATY, so Saint-Clair-sur-Epte. Battle: a drawing of a longship, so use the LONGSHIP edge of the ruler (the other edge, SPEAR, is a decoy). Châlus to Saint-Clair-sur-Epte reads **120** on the LONGSHIP edge: **120**.

## Solution notes

Design-side solution text, kept when the player-facing Solution above was written for the hint page (9 Oct 2026).

Bayeux: cross + bow + lightning bolt = CROSSBOW BOLT → Châlus, where Richard I was fatally wounded by one. Winchester: tree + teacup = TREATY → Saint-Clair-sur-Epte, site of the 911 grant of Normandy. Battle: fish (“scale”) + Roman numeral I + arrow (“to”) + die showing 5 = SCALE 1 TO 5 (**28 Sept 2026:** target changed to 1:125; the drawing still shows 5 until redrawn). Both target places already carry a matching icon on Rollo’s map. The measured distance between them at 1:125 is the code: 10.4 m, so **104** (measured on a 100% print, 2 Oct 2026).

## Open risks

**Tight reading.** The code 104 needs the distance read to 0.1 m, which is 0.8 mm on paper; the true distance is about 0.3 mm from reading as 103. Check with a fresh player. All nine rebus icons are assigned (Q-011); the tenth, the arrow/2 hybrid, was dropped.

## Releases (as worded on the old page)

**Superseded 9 Oct 2026** by the compartment map in Q-001; the current release list is under Player obtains.

**Since 7 Oct 2026 (Q-005):** lock 11; releases postcards H4 and H5 and the raven’s flights card.

Lock as recorded: Numeric lock, digit count unknown. Old page status: Candidate · cards built, code not measured.

## Design notes (PZ-011: Built · code 104)

**The rebus-distance lock: Rollo’s Bayeux card introduces Liv’s tapestry-style habit and carries the first rebus; Winchester carries the second; Battle carries a third rebus naming which ruler scale to use; the distance between the two map points, read at that scale, is the code.**

**Postcard update, 28 Sept 2026 — still to do on this puzzle.**

- **R5 message line — decided and built, 28 Sept 2026.** The user wanted R5 to help a little with the measuring step (besides “measure up”). Chosen from three options (option B): “I hope you’re enjoying my drawings! Good thing I packed my old ruler: they only make sense at the right scale.” The drafted “use that attached tool” line was dropped because the ruler is loose, not attached. **Reworded 1 Oct 2026:** “they” became “my maps” (“…my old ruler: my maps only make sense at the right scale.”), so the hint points at the map and its dots rather than at the drawings. Chosen from four options; “the distances between places” was judged too close to stating the mechanism. The same day, the km scale bar was removed from Rollo’s map so the 1:125 ruler is the only scale on the sheet, and then from the other three maps too, so all four sheets match (only that corner of each sheet changed). The Aud designer’s exported “scale bar” keep-out box now just reserves empty space. The rebus art was redrawn 28 Sept 2026 and now reads SCALE 1:125.
- **Scale reading — decided, 28 Sept 2026: 1:125** (the ruler carries both 1:25 and 1:125). R5 now reads “scale” + one raised finger + colon + one-pip die + two raised fingers + Roman V: SCALE 1:125. This replaces SCALE 1 TO 5. The Châlus–Saint-Clair distance has still not been measured, so the code stays open.
- **Art redo:R4 — done, 28 Sept 2026:** the hot-tea cup (three wavy steam lines, Codex’s draft) is now on the card as `Rebus_Teacup_Hot_Bayeux_v3.png`, normalised with `prepare_r5_scale_icons.normalize` and drawn at 28 pt (was 26) so the cup stays about the same size under the steam. TREE + TEA still reads TREATY. R5’s scale ratio art was rebuilt 28 Sept 2026 for 1:125; the hand, die and Roman numeral encode the digits.
- **Measuring end points — decided, 1 Oct 2026: dotted leader lines.** Each of the seven story icons stays where it was and gets a thin dotted line, in the town dots’ own grey (`#59635D`), running from its nearest inked edge to its town’s dot. The dot is then the one clear end point. The treaty scroll moved down below Saint-Clair-sur-Epte (box from 370.49, 458.92 to 384.70, 436.50) so its line has visible length; the longship’s line goes to Battle, since Hastings is no longer on the sheet. Built in `TravelMap/build_trail_maps_pdf.py` (`ROLLO_LEADER_TOWN`, `draw_leader`, `LEADER_INK`). Chosen from mock-ups of “icon beside its dot at a fixed gap” (2.5 and 6 pt) and solid vs dotted leaders; the solid line read too much like a drawn route leg. Mid-grey, dark ink and teal were compared for the dots; mid-grey was built. **Same day, the six word-lock icons (PZ-007) got lines too**, each to a real town added for it: cow → Manchester, hen → Eindhoven, fight → Troyes, forest → Saumur, inn → Vichy, people → Montauban. See PZ-007 for the same-square rule. **Superseded below, kept as history:** the first decision that day, each icon’s point sits on its town dot. On the current map the end points are unclear. The crossbow bolt sits about 12 mm below the Châlus dot. The treaty scroll covers one unlabelled town dot and has a second one just below it, while the labelled Saint-Clair-sur-Epte dot is to its right. From the render (assuming a letter page at 144 dpi, not checked), dot to dot is about 83 mm (about 10.4 m at 1:125). Icon to icon is about 92 mm (about 11.5 m). That is a whole metre apart. Chosen from three options: (1) icon point on the town dot; (2) measure dot to dot and leave the icons where they are; (3) add a centre dot to each icon. Option 3 was rejected because it adds more possible end points, not fewer, and makes the icons look like targets. The fix: **the bolt’s tip touches the Châlus dot** (the bolt “hits” Châlus, as it hit Richard I), and **the treaty’s wax seal sits on the Saint-Clair-sur-Epte dot**. Then whether a player measures from the icon or from the place, the reading is the same to within about 1 mm. Nothing new is printed, so the clue stays subtle.
**Pinning tried and reverted, 1 Oct 2026.** All seven story icons were briefly pinned to their stop dots (bolt tip on Châlus, seal on Saint-Clair, needle on Bayeux, coronet on Rouen, crown on Winchester, longship prow on Hastings, boar snout on Roumare forest). **The user reverted it the same day:** moving the icons breaks another puzzle (not named yet). All seven went back to their earlier boxes. **Resolved the same day by the dotted leader lines described above.Kept: towns removed** (user’s call, two rounds on 1 Oct 2026): Caen, Falaise, Chichester, Château Gaillard, Dives estuary, Le Havre, Lewes, Pevensey, Salisbury, Southampton; then Coutances, Évreux, Hastings, Amiens, Calais, Chartres, Alençon, Avranches, Limoges and Dover. None is a route stop or used by any puzzle (“Hastings” on the postcards names the battle, not the dot). The list is `omit_towns` in the Rollo config in `TravelMap/build_trail_maps_pdf.py`. 24 towns remain, each label right beside its own dot, and none dropped. The remaining non-stop dots still act as decoys among which players find the stops by name. Châlus to Saint-Clair dot to dot: 235.6 pt = 83.1 mm, about 10.39 m at 1:125 (calculated, not measured on paper).
**Code — decided, 2 Oct 2026: 104.** The user printed `Norse_Trail_Maps_Print.docx` (page 2, Rollo) at 100% and measured Châlus to Saint-Clair-sur-Epte, dot to dot, on the ruler’s 1:125 edge: **10.4 m**, matching the calculated 10.39 m. The code is the reading with the decimal point dropped: **104** (three digits). **Risk, not yet tested:** reading to 0.1 m means 0.8 mm on paper. The true distance (10.39 m) is about 0.3 mm from reading as 10.3 and 0.5 mm from 10.5, so a player who measures from the edge of a dot instead of its centre, or a printer that scales slightly, could get 103 or 105. Worth checking with a fresh player before the lock is final. Superseded: the earlier note here said the code should only use whole metres, with about ±3 mm of tolerance; the measured reading was chosen instead.

**Designed in chat, revised three times.** First pass put CROSSBOW BOLT on Winchester and TREATY on Battle. Second pass moved CROSSBOW BOLT onto Bayeux itself. Third pass moved TREATY onto Winchester, freeing Battle for pure history. Fourth pass gave Battle a different rebus job: the scale clue.
• **Bayeux (stop 3) — introduces the habit and carries CROSSBOW BOLT.** Cross + bow + lightning bolt, scattered in the blank space below her signature, read as **CROSSBOW BOLT** — pointing to Châlus, where Richard I was fatally wounded by one. Message names William the Conqueror as Rollo’s descendant and the Bayeux Tapestry’s subject (Q-019). **Built** — front and back, in `build_postcard_R3_pdf.py`.
• **Winchester (stop 4) — carries TREATY.** Tree + teacup, scattered below her signature, read as **TREATY** — pointing to Saint-Clair-sur-Epte, where the 911 grant of Normandy was made. Message names Richard the Lionheart’s 1194 recoronation and loops back toward “one deal, centuries earlier” without naming the place outright, so the rebus keeps its own job. **Built** — front and back, in `build_postcard_R4_pdf.py`.
• **Battle (stop 5) — ties to William the Conqueror’s victory and carries the scale clue.** Message names the 1066 Battle of Hastings explicitly and loops back to the Bayeux Tapestry from card R3 (“after spending hours looking at the tapestry”); its Fun Fact does the same, questioning the Tapestry’s famous arrow-in-the-eye scene. Below the signature: overlapping fish scales + one raised finger + colon + a one-pip die + two raised fingers + Roman V, read as **SCALE 1:125**, rebuilt 28 Sept 2026. This is what tells players which of the architect’s scale ruler’s six marked scales to use when measuring the Châlus–Saint-Clair-sur-Epte distance (corrected 25 Sept 2026 from “Bayeux–Winchester”: the rebuses on those cards point to Châlus and Saint-Clair, and the map icons measured are there). **Built** — front and back, in `build_postcard_R5_pdf.py`.
Both rebus target places already carry a matching icon on Rollo’s map (crossbow bolt, treaty scroll — Q-023). The distance between those icons, measured at the scale Battle’s card specifies (1:125), is the lock input. (Refined 1 Oct 2026: icons and town dots are made to coincide — bolt tip on Châlus, seal on Saint-Clair — so “between those icons” and “between those places” give the same reading. See the note above.)
The original nine icons (cross, bow, lightning, tree, teacup, fish-scales, Roman I, arrow, die-5) remain documented below; R5’s scale rebus was replaced 28 Sept 2026 by a scale patch, one- and two-finger hands, a one-pip die and Roman V. The colon is punctuation.
**Code decided 2 Oct 2026: 104** (measured on paper, see the note above). **Still open:** a fresh-player check of the 0.1 m reading, which lock takes the code (three digits), and what it releases (Q-001).
See the [Puzzles tab] for the player-facing writeup of this mechanism.

## Playtest evidence

**Playtest 1** (feedback relayed by the designer 11 Oct 2026; playtest date, team and hint use not recorded). Rebus should look hand-drawn: no colours, pencil style. Changed as above; retest needed.

**16 Oct 2026 (designer, envelope 9 text pass):** the 15 Oct redesign is now built on the card side. **R5 carries a longship drawing** (Codex, pencil style, `Postcards/RebusIcons/Rebus_Longship_Pencil_Codex_v1.png`) in place of the SCALE 1:125 rebus. R5's last message line now reads “Good thing I packed my old ruler: my maps only make sense when I pick the right side.” (the designer typed “my map only make sense”; “maps” kept from the old line). **The ruler (PP-025) moves to envelope 9** with R3, R4 and R5. The crossbow-bolt rebus on R3 stays as it is (the glossary on Liv's notes card, PP-048, defines it). Player-facing hint 3 and the Solution above now describe the longship edge and 120. Fun Facts of R3, R4, R5 not yet touched (drafts offered). Not retested with players. Digital game still shows the old 1:125 / 104 version (Q-051).

**18 Oct 2026 (folder cleanup, open):** `Postcards/RebusIcons/prepare_r5_scale_icons.py` still prepares four die icons (`Rebus_Die_1_Perspective_Bayeux_v2/v3/v4/v6.png`), but no postcard builder or record uses any of them. Is a die still part of the R5 rebus? The files stay until the designer decides.

**20 Oct 2026:** the ruler is now a 2 × 6 in bookmark with the same scales; 120 is still 83.126 mm from 0 on the LONGSHIP edge (PP-025).

**20 Oct 2026 (production-size design proof):** matching 5.5 × 8.5 Rollo map and ruler built under C:/EscapeBackpack/output/other-maps-half-letter/. New measured map distance about 71.329 mm; new ruler LONGSHIP 120 is the same distance, so the answer stays 120. Existing Letter prototype and ruler unchanged. See PP-025/PP-032. Physical reading/player test outstanding.
