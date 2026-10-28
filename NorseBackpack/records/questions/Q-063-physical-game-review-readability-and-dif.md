---
id: Q-063
title: Physical game review: readability and difficulty progression
type: question
# open | answered | parked
status: open
# Records this question is about, e.g. [PZ-003]
about: [PR-007, PP-047, PZ-006, PZ-008, PZ-013]
# Leave empty while open
answer:
# Any related record IDs, e.g. [PZ-002, Q-004]
links: [Q-050, Q-062, PP-025, PP-031, PP-033, PP-043, PP-048]
# Set to an ID when this record is replaced. It then moves to the Parked tab.
superseded_by:
tags: []
---

## Follow-up review after live adoption, 17 October 2026 (Codex)

**Latest assessment; earlier review below is historical where superseded here. Recommendations only. No game assets, rules or order changed.**

The physical game is more coherent and readable after the adoption. Keep the vintage postcard fronts, personal handwriting, institutional museum tickets, modern travel receipts and cleaned maps: they feel like different objects collected by one traveller. The larger museum map works; Liv's latest portrait notes have better spacing. Keep LD's deliberately tiny corner imprint exactly as approved; it is a discovery clue and may require the magnifier.

### Confirmed improvements

- Live Brattahlid/Aud tickets are 3.5 x 6 in; Rouen is 3.5 x 5.5 in. Functional ticket text is substantially larger. Liv's live note is now 4 x 6 portrait, one side, with 10 pt handwriting and 8 pt bold labels (the designer's later tuning).
- The live 34 mm wheel arm teaches blank-first entry for three-digit codes. All 13 codes map to distinct labels; current hint titles and the printed packing key match their envelope sequence.
- H1 explicitly says a dark move, then the king, each round, and asks for exactly four king moves. The solver still finds only F6-H6-H7-K7-K11 (2134), no shorter escape and none without the fourth dark move, under its stated scripted-attacker/king-only rules.
- Leif, Rollo and Harald cleanup maps are live. Aud retains the detailed v15 map and the comb emblem. Rollo's cleanup source preserves the icon boxes, projection and town data, so it does not intentionally change the lookup or measuring geometry.
- The final letter's family clue now specifically echoes AD, avoiding the earlier loose reference to family.

### Remaining improvements, in priority order

1. **Make the Baffin Island / Qikiqtarjuaq connection explicit (PP-003, PP-039, PZ-013).** L3's front and postmark say Baffin Island; its note says Helluland. The hop and transition tickets use Qikiqtarjuaq, as does the map's town dot. There is enough geographical context to infer the connection, but it introduces an avoidable extra inference into ticket matching. Proposed small change: add "Qikiqtarjuaq, Baffin Island" to the card's postmark or note, preserving the sky artwork and join. No geography knowledge should be needed to match the same stop across props.
2. **Bring the hint source up to date before independent play.** PZ-013's current Hints/Solution still refer to the retired journal, multiple family symbols and caption order. Replace those with ticket chaining, raven filtering and the three transition receipts. Smaller text corrections: PZ-012 calls RAVEN underlined when it is capitalized; PZ-006 hint 3 still says A2 tells the direction as well as the road, although the card only supplies the forest-road cue. PZ-001 and PZ-003 retain historical material inside their Hints/Solution sections; keep it outside publishable sections. This is a source audit, not a claim about the deployed site. The handoff explicitly defers online work, so these are completion tasks rather than reasons to stop a supervised paper test.
3. **Give the AUD epilogue a clear finish (PP-043).** The improved clue is sound, but the letter supplies no way to confirm AUD and the intended online confirmation remains recorded as unbuilt. Complete that destination and show players how to reach it, or provide an offline reveal. H6 promises one more puzzle before the reward; frame the family discovery as a bonus after winning so it does not feel like the finish moved.
4. **Finish the two decoy envelopes (Q-050).** Count is decided; labels and contents are still open, and the live sheet contains only the 13 real labels. Prefer labels using the same rune alphabet as the wheel, distinct from all real labels and from one another. Off-wheel runes would make a decoy identifiable by inspection. Include a brief recovery note for an accidental opening; avoid extra puzzles. Match the two envelope sizes and avoid a uniquely bulky reward envelope. Specific labels/content remain the designer's decision.
5. **Check remaining small functional print, without restarting the redesign.** Aud's map legend is 6.5 pt; map place names are 7.4 pt; Oslo's hnefatafl rules are 7.4 pt. The transition receipts have 7.8 pt intermediate places, with the important endpoints at 8.4 pt. These are measured PDF sizes, not proof of illegibility. Test those on paper first; enlarge only what readers struggle with. Liv's 8 pt bold labels are deliberately adopted and need a paper check, not another automatic reflow. Small ticket reference numbers, credits and LD's hidden clue are not equivalent to ordinary instructions.
6. **Provide a short start/handling rule and an unambiguous player print set.** L1 teaches the wheel; Liv's notes say to keep that card handy. Neither gives a general keep-everything rule, permission to draw on the maps, or a route to hints. One small out-of-story instruction can cover those choices without filling another postcard. The current `Aud_Ticket_Print.pdf` still includes the designer's answer as page 3; its two-page Letter file is player-only. Keep the answer in a separate file, or make the packer's page selection explicit. The wheel key also omits a loose-at-start row; include L1, Liv's notes and the assembled wheel in the packing checklist. This is prevention of a packing mistake, not a claim that the user's assembled prototype includes the answer.

### Difficulty and playability

Judgment from the material, not measured playtest results: **medium overall, with a hard late section**. The tutorial, comb and joined skies make a sensible opening. Aud's six-leg route is the first attention-heavy jump. The ruler and especially hnefatafl carry the greatest late burden. H1's new turn rule materially helps; do not simplify the board before observing players with it.

Keep the current order for the next fresh-team test. The earlier counting-wolf-route reorder remains an option only if Aud causes an early stall; changing order now would make it harder to tell what the newly clarified props achieved. Easier stretches between harder puzzles are useful.

The finale's risk is workload: 18 hop tickets, 3 transition receipts, 22 postcards and 4 maps. Observe whether matching feels satisfying or administrative. If sorting drags, keep tickets together by journey while shuffling their hops, so several players can work on maps in parallel. Preserve the accepted route geometry; test the four digits without showing the answer banners, particularly Harald's less conventional 2. Do not assume the shape will be obvious because a designer knows 1972.

### Evidence and limits

- Read current puzzle/prop records, live adoption scripts and relevant builders. Rendered 82 PDF pages: all 44 postcard faces; 32 ticket/note/wheel/map pages; ruler and raven flights; four map answer fronts. Visually inspected them and the existing comb overlay. PDF text-bounds checks found no out-of-page text on the checked postcard and main prop pages.
- Checked 13 unique wheel mappings and hint titles without regenerating production files. Ran the existing hnefatafl solver. Inspected the actual revised maps and answer routes. Print-size assertions in source are not a physical measurement test.
- `kit.py check` still reports the same 141 migration/configuration problems. The dedicated wheel is consistent, but the generic kit still lacks this cipher configuration; do not treat its generated hints/reset pages as verified.
- The adopted print pipeline still relies on draft builders plus copying selected pages; old builders can overwrite approved output. Before creating a distributable set, consolidate one documented build/packing path. No production rebuild was run during this review.
- No new physical playtest, coin/tally handling test, printer registration test, historical fact check, live website audit or timing data. The best next evidence is a fresh team using the current physical set without designer coaching: note first hint/stall, route counting, board setup/turns, final sorting and digit recognition.

## Earlier review, 17 October 2026 (Codex)

Requested: review the updated physical game for readability, clarity, puzzle fit, difficulty progression and playability. **Recommendations only; nothing below is an adopted design change.** Props, artwork, puzzle rules and order were not edited.

**Opinion:** keep the souvenir-postcard style and the rune-wheel/envelope format. They fit Liv's travel story well. The game has useful variety and satisfying reuse of earlier objects. The main remaining risks are inconsistent packing/hint information, small functional text, an unusually demanding hnefatafl section, and the amount of sorting in the finale. This looks like a medium-to-hard family/adult puzzle game, subject to a fresh physical test; it is not uniformly easy family play.

## Basis and limits

- Read current puzzle/prop records and the actual local print masters in `NorseBackpack/Print/_pdf_source/`, not the frozen brainstorm or the outdated digital game.
- Rendered 82 PDF pages with Poppler. Inspected all 22 postcard fronts and backs, the four player maps and answer routes, relevant ticket faces, ruler, glossary, wheel preview, final letter and boarding pass. Also inspected the comb overlay, tally glyph check, medallion preview and current cleanup-map previews.
- Checked the wheel's 13 current answers and unique rune labels with its own code. Ran the existing hnefatafl solver against the current board.
- Physical card stock, lighting, cut accuracy, wheel friction, coin recognition and actual player behaviour cannot be verified on screen. No new physical playtest, timing or success-rate data was collected. Existing records describe earlier family/friend feedback, but the latest revisions are mostly still marked untested.
- Historical claims, actual transport availability, live hint deployment and the digital game were not audited. Cleanup drafts remain separate from the live print masters.

## Fix before another unattended playtest

### 1. Reconcile the packing key and current order

`Cypher_Wheel_Print.pdf`, page 5, gives correct current codes but **old contents for envelopes 1-3**:

| Envelope | Key currently says | Intended current contents |
|---|---|---|
| 1, 1021 | L2, L3, magnifier | AD, comb |
| 2, BOOK | H2, H3, HD | L2, L3, magnifier |
| 3, 1576 | AD, comb | H2, H3, HD |

This is a real failure if a host packs from that key. Prop `container` fields reflect the new order, while their `found_in` fields still describe the old order; the wheel builder reads `found_in`. Rebuilding the wheel alone will reproduce the mismatch.

PR-007's main table still says **521** and the old runes for envelope 5. The current Aud ticket answer, puzzle answer and wheel label use **532**, giving **ᛈᚹᛟᛇ**. PZ-009's hint title also still points at the old label. The wheel check explicitly reported that mismatch.

Envelope 12's printed key still lists the journal and crest note. Its current bundle should reflect H6, the hop tickets and the journey-to-journey receipts. PZ-013's publishable Hints/Solution still describe the superseded journal-mark ordering. Update the current instructions and packing relationships together; retain old material only as clearly marked history.

The generic kit is also incompletely migrated: `kit.py check` reports 141 existing problems, including no configured cipher (falls back to shapes) and legacy lock/prop fields. The dedicated wheel has 13 distinct valid labels, but that does not validate the kit's generated packing/hint pages. Do not replace this wheel's positional mapping with a generic rune preset without a separate design decision.

### 2. Teach three-digit codes on a player prop

L1's worked example is good. The wheel arm says set code, read runes, open envelope. However, **the blank-first rule is only in the designer instructions**, not the player explanation inspected here.

Proposed wording: **“For a three-digit answer, leave the first window blank.”** A leading zero does not work with the current mapping: `_532` gives ᛈᚹᛟᛇ, whereas `0532` gives ᛈᚹᛟᚲ. PP-047's suggestion that a leading zero would also work is incorrect for this build.

Also suggest a short start rule: **“Keep everything you find. Open only the envelope whose four runes match, in the same order.”** This explains reuse and supports the decoys without making another puzzle out of the interface.

## Readability and prop fit

**Postcards:** the 6 × 4 format, illustrated fronts, consistent title bands, handwritten voice and separate typed facts work together. Most handwriting is substantially easier to read than the tiny reference text elsewhere. The family raven is a useful single filter. A close-up audit confirmed **18 marked real cards and four unmarked decoys**. An initial suspicion of missing marks from overview images was disproved; no mark repair is recommended. AD's comb overlay exposes BOOK, and its matching registration circles make it a sensible first puzzle. Preserve exact text placement when changing this card.

**Small text is the clearest visual weakness.** Sizes below were extracted from the PDFs, not estimated from screen zoom:

| Functional content | Current size | Recommendation |
|---|---|---|
| Rouen ticket word pairs | 5.8 pt; indices 5.6 pt | First enlargement priority: this is routine matching, not a hidden-detail puzzle. |
| Brattahlid visitor index | 6.2 pt; letters 6.6 pt | Enlarge the reference list or ticket. |
| Aud treasure-route directions | 6.8 pt | Enlarge the directions; avoid making the map task depend on reading tiny text. |
| Wheel's three operating steps | 6 pt | Give the repeated-use instructions more visual prominence. |
| Liv's glossary | 9.2 pt handwriting; 6.8 pt term labels | Keep the friendly heading/intro, but consider plain type for reference definitions. |

As a design target, try roughly 9-10 pt for ordinary ticket instructions and verify a real print. That is a proposed target, not a tested accessibility guarantee. The magnifier can serve the intentionally tiny sky fragments; it should not be needed for every ordinary rule. LD's very small publisher imprint is also a likely bottleneck: this is an inference puzzle already, so finding A6 need not additionally be an eyesight test.

**Maps:** Aud's v15 has a readable legend and distinct roads, streams and landmarks, but six-leg tracking is appreciably harder than the early tactile discoveries. I can follow the intended route on screen; physical counting and the forest-road choice still need a fresh test. The current A2 text names the forest road but does not say “south,” despite PZ-006 still claiming it gives both clues. Update that claim; only strengthen the actual clue if players choose the wrong crossing.

The Leif and Rollo cleanup drafts improve icon contrast and cramped labels. Harald's draft reverse makes the note markedly easier to read. Those are useful improvements without increasing puzzle complexity. **Aud's cleanup draft needs a consistency check:** its title-band emblem looks like two upright pillars, while Aud's postcards and live map show a comb. Since stamp matching identifies the journeys in the finale, use recognizably matching artwork. Do not adopt that symbol change merely for visual consistency with the other title bands.

**Tickets and ruler:** museum tickets feel like souvenirs, and modern travel receipts fit a present-day traveller collecting historical clues. The ruler is attractive and its offset zero makes cutting less critical. Its LONGSHIP edge is itself a long-arrow + sheep rebus, so R5's ship drawing does not remove all decoding. Keep this as a late puzzle and test whether players find the intended edge and measure dot-to-dot. The builder targets 120 at 83.126 mm; that is a calculated distance, not a measurement of a print.

**Physical pieces:** the comb overlay and seven-segment SOLE preview work visually. Coin matching depends on seeing the distinguishing crown/script/ship/raven details, and the ticket's yellow relief on grey is low contrast. Test those with the actual coins, not only their artwork. The medallion gives the finish a tangible payoff; its successful physical print is reported in PP-044, not independently tested here.

## Current difficulty progression

These are review judgments from the steps and prop burden, not measured ratings. “Envelope” means the one just opened; the answer opens the next one.

| Stage | Puzzle / answer | Expected difficulty and fit |
|---|---|---|
| Start | Worked wheel example / 1021 | Tutorial. Good: teach the repeated action before testing it. |
| 1 | Comb / BOOK | Easy tactile discovery. Keep first. |
| 2 | Joined skies / 1576 | Easy-medium; recognizing the join and upside-down orientation is the hurdle. |
| 3 | Three drink clues / MEAD | Medium in principle, easier with Liv's glossary. |
| 4 | Aud's six-leg route / 532 | Medium-hard attention task; the first noticeable jump. |
| 5 | Count illustrations, double boars, sort years / 562 | Medium. A welcome visual change, not just simple counting. |
| 6 | Imprint → map wolf → ticket index / 4865 | Medium. Good introduction to a short multi-prop chain. |
| 7 | Coin selection, sum, rotate tally / SOLE | Medium-hard; satisfying return to Aud's earlier map and ticket. |
| 8 | Rouen word matching and grid distances / 1486 | Harder combination of text, reference and map. |
| 9 | Rebuses, choose ruler edge, measure / 120 | Hard; several deductions, then physical precision. |
| 10 | Reconstruct board and king's escape / 2134 | Hardest individual section; possible bottleneck. |
| 11 | Branch runes → HRAFN → flights / 2648 | Hard chain, but structured. Reasonable relief after the board. |
| 12 | Tickets, raven filter, four route shapes / 1972 | Medium-hard synthesis; workload is the main concern. |
| 13 | Reward and AUD family clue | Easy epilogue; should feel optional after the main victory. |

**Suggested order change for discussion:** after MEAD, try **counting → wolf → Aud route → coins** instead of route → counting → wolf → coins. This introduces grid lookup before six-leg navigation and places the coin payoff directly after finding the treasure. It preserves the existing puzzle answers and mixed journeys, but requires coordinated changes to envelope contents, dependencies, packing and hints. Nothing has been reordered in this review.

I would keep the later sequence initially. Growing complexity with short easier stretches is more playable than making every successive step strictly harder. Keep the finale as a satisfying combination of familiar tools rather than making its individual deductions harder than hnefatafl.

## Hnefatafl: preserve the challenge, clarify the contract

Rebuilding the smudged setup, understanding the ticket transfer, finding four dark moves, navigating the king and recording distances are several substantial tasks in one section. The story treatment is good, but setup uncertainty can bury the actual puzzle.

The existing solver confirms one escape under the intended scripted-black/king-only rules: **F6 → H6 → H7 → K7 → K11 = 2134**. It finds none in fewer king moves and none without the fourth dark move. This establishes logic under those assumptions, not that players will infer the assumptions.

Propose a concise rule on the ticket or note: **“Move one attacker as my clues show, then move the king. Repeat four times; the other light pieces stay where they are.”** The current ticket says dark moves first and describes how every piece moves, but does not explicitly state that puzzle turn sequence. Keep the hidden move deductions. Use the clearer draft reverse, and observe whether players struggle with setup, rules or solving before simplifying the board.

## Finale and decoys

The current tickets replace the earlier complicated sentence/calendar reconstruction with visible FROM→TO relationships. That is a sound improvement. There are **18 hop tickets plus three transition receipts**, alongside 22 postcards and four maps. The danger is a long administrative sort after the hardest puzzles.

Suggested first test: keep the four journey bundles held together with simple bands/clips, with hops shuffled within each bundle. This lets a group split up the four maps without presorting the actual routes. The receipts can still establish journey order. If testing shows that identifying the steps, rather than solving them, is the problem, use a staged hint: link the tickets, retain raven-marked stops, join the retained stops in order. Do not restore the retired journal-mark solution.

The map digits remain the working payoff. Harald's existing 2 was explicitly accepted by the designer, so no geography redesign is proposed. Its shape is still less conventional than the others; test recognition without the answer banner or a spoken suggestion of the year.

**Q-050 proposal:** start with two extra envelopes, one of each used size, with clearly distinct rune strings that do not match a real solution. This is a prototype recommendation, not a settled count. They prevent the final envelope becoming automatic by elimination. Check the packed box too: the medallion's weight/bulk should not make the real final envelope obvious. Avoid deliberately labelling decoys with common wrong answers in the first test; that adds false progress and more recovery instructions. No additional decoy postcards are needed: the four existing ones already do useful work in earlier puzzles and the epilogue.

The final letter reuses AD well, but H6 promises one more puzzle and the reward letter then introduces another. Present AUD as a **bonus family discovery after winning**. The online confirmation is recorded as unbuilt, and the letter itself gives no confirmation destination. Choose a clear destination or an offline reveal before expecting an independent team to finish that epilogue. “One of them says something about family” is slightly broad because LD's Fun Fact mentions Leif's mother; a more precise proposed clue is **“On one of those cards I wondered whether someone was actually our family.”**

## Focused next test

After reconciling the packing/key/hint data, run the revised physical set with a fresh team. Record where they stall and which hint they use; do not infer a playing time from this review. Priorities: first blank-leading code; ordinary ticket readability; Aud route counting; hnefatafl turn order; finale sorting burden and unprompted digit recognition. Keep the current main-game completion separate from the optional AUD epilogue in those observations.

One next design decision: whether to try the proposed counting → wolf → route middle section. The wider visual style does not need a redesign.

**17 Oct 2026 (Claude, verification of this review):** the A2 claim is confirmed. PZ-006's Player-does line said A2 gives the direction (south); the card text never does, so the record was corrected to match the card (forest cue only). Whether the cue is enough is untested: strengthen the card only if players choose the wrong crossing (H3/G3 instead of H9).

**17 Oct 2026 (designer):** blank-first rule added to the wheel arm (PP-047); hnefatafl turn order added to the H1 postcard (PP-016); contents list and packing key fixed; A2 claim corrected in PZ-006 (card left as is). Open: small text sizes, AUD clue wording.

**17 Oct 2026 (designer):** AUD clue changed (PP-043). Still open: small text sizes; the AUD confirmation destination (online page, not built).

**17 Oct 2026 (designer):** Rouen ticket word list now 10 pt (PP-033). Still small: Brattahlid index, Aud directions, wheel steps, glossary labels, LD imprint.

**17 Oct 2026 (designer):** adopted the Brattahlid, Aud and Rouen tickets, the LD postcard (draft identical to live) and the wide wheel arm into live print files. Liv's notes card held back. Still untested: paper print, envelope fit, duplex alignment, wheel turning.

**End of day, 17 Oct 2026: state of this review.** Done: packing key and found_in for envelopes 1-3 (key rebuilt), 521 to 532, PP-047 leading-zero line, blank-first rule (now Codex's wheel arm), hnefatafl turn order on H1, A2 claim corrected in PZ-006 (card left as is), AUD clue reworded, small print fixed by the adopted readability redesign (Brattahlid, Aud, Rouen tickets, notes card, wheel arm; LD unchanged), all four maps adopted in the cleaned style. Not done: paper print and envelope-fit tests, the suggested middle-section reorder (not adopted, nothing changed), Q-050 decoy contents, the shape codes on the hint page, digital game.
