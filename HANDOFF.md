# Project Handoff

Last updated: 2026-09-09 by Claude Code

## Current Task and Status

Norse puzzle, clue and prop design. The user asked for design direction on puzzles, clues and props, explicitly deprioritising container and lock placement until the backpack and pouches are bought.

A new design spec exists at `NorseBackpack/Norse_Puzzle_Design.html`. It is a proposal, not approved content. Nothing in it has been copied into `Norse_Brainstorm.html` and no props have been built.

Eight design decisions were taken with the user this session:

- Hnefatafl: escape path drives a directional lock, **and** the board gets a hidden compartment under the throne square opened by the king piece.
- Decoding tools in the bag: magnifier, red acetate filter, UV pen and blacklight.
- Cipher backbone: branch runes (kvistrúnir), Younger Futhark, left branches = group and right branches = position.
- Difficulty: a notch harder than the Hiking backpack.
- Postcards: one per route stop, so 18 cards.
- Postcard size: approx. 5 x 3.5 in, down from the current 6 x 4 in.
- Postcard design elements are split into two layers. **Universal, on all 18:** a per-trail series motif and a postmark carrying date and place. **Sparse, on small subsets:** denominations on about 4 cards, extra printed text on about 5, stamp angle on about 4, anomaly stamps on about 3.
- Non-lock redirect clues: three, in the roles teach / tool / hinge.

The prior Codex session's postcard and route-map work remains uncommitted and untouched. Its open item is unchanged: postcards 02 and 03 still have placeholder backs.

## Files Changed

- `NorseBackpack/Norse_Puzzle_Design.html` — new. Clue-craft standard, postcard system, branch-rune cipher with the HRAFN encoding, hnefatafl, coins and balance, comb grille, tool assignments, redirect clues, ordered next steps, prototype list, open questions and a verification list. Visuals: a labelled postcard-anatomy diagram, an 18-card corpus worksheet, two convergence flow diagrams, the 7 × 7 board, and the five HRAFN branch runes drawn to spec.
- `NorseBackpack/Norse_Brainstorm.html` — updated. Header now links to the build spec and carries the difficulty tag; the props list gains the rune stick, comb, coins and balance, and reader tools; the hnefatafl and postcard entries reflect the new decisions; "Open design choices" is split into "Decided" and "Still open"; the difficulty target is recorded under Audience.
- `HANDOFF.md` — this handover.

No other file was modified. The uncommitted Codex postcard/route work and the unrelated local Aurora and `AGENTS.md` changes were left alone and are **not** part of this commit. `index.html` was not touched, since it deliberately links only to the brainstorm page — the build spec is reached from there.

## Decisions

- A design element on every card carries structure; a design element on only a few cards carries a puzzle, because its scarcity is the signal. Size each sparse set to the lock it feeds — four cards bearing a price is a 4-digit lock announcing its own shape.
- The postmark is on all 18 cards and is the ordering key, both for the endgame and within each trail.
- Sparse-element puzzles are late-game by necessity: scarcity is invisible until players hold enough cards to see that most lack the element. Early puzzles must work from a single card or from the physical props.
- Teach each channel once with a diegetic pointer, then rely on learned fluency for later uses.
- Five or six of the 18 cards carry active clues. The rest are deliberately quiet, so that finding an active card feels like discovery.
- The anomaly mechanic is the primary hard postcard puzzle, and its job is to be a **selector rather than a data channel** — it answers "where do I look?" while a sparse data element answers "what do I take?" and the postmark answers "in what order?"
- Deliberate overlap between sparse sets (a card carrying both a price and an anomaly stamp) is where late-game difficulty lives. Save it for the last postcard puzzle before the map.
- The five-letter answer is HRAFN, encoded in branch runes across three props: the stick carries the characters, a museum accession label carries the group table, and the aunt's letter hides the reading direction.
- The UV pen's primary job is writing the four trails' reading order on the map. This replaces the current arbitrary "left to right" rule and preserves the 1972 code.
- Do not print digits on the hnefatafl squares. The escape path outputs directions instead.
- Historical claims in the new page are unverified and are marked as such on the page itself.

## Checks

- `Norse_Puzzle_Design.html` opened locally in the browser: renders, no console errors.
- Branch-rune SVGs generate correctly: 5 glyphs, 26 line elements, matching the intended group/position counts for H-R-A-F-N.
- No horizontal page overflow at 1200 px or 420 px width; none of the five tables overflow at either.
- All 11 sections present with their expected headings.
- Corpus worksheet renders all 18 cards under 4 trail headings, numbered 01 Helluland to 18 Asia Minor.
- Both figures render at their intended sizes (postcard 560 × 380, board 340 × 340) after an initial bug where the SVGs stretched to full container width; the board contains its 10 rects, 12 grid lines and king.
- `Norse_Brainstorm.html` after editing: 6 nav buttons and 6 views intact, both build-spec links present, "Decided" and "Still open" both render, no console errors.
- Screenshot inspection was **partial**. The preview pane timed out intermittently, so the postcard diagram and the corpus worksheet were confirmed by eye but the board diagram and several sections were verified programmatically only. Worth a manual look.
- No print test, no prop built, no physical validation of any kind.

## Next Action

Assign the sparse sets — decide which of the 18 cards carry a price, an extra printed line, a tilted stamp and an anomaly stamp, using the worksheet in the build spec. It is a pure design decision needing no purchase or test, and all postcard artwork depends on it.

The full ordered list is in the build spec's "Next steps, in order" section: assign sparse sets → design the four stamp series → re-render the three existing fronts at the new size → write the aunt's letters → solve the hnefatafl board → prototype the final map → run print and filter tests → source-check the history.

## Open Design Issues

- The 18-card postcard set needs its artwork re-rendered, not rescaled. Current fronts are 1536 x 1024 px (3:2); 5 x 3.5 in at 300 dpi is 1500 x 1050 px (10:7). `SIZE` and `PAGE` in `Postcards/build_postcard_collection.py` must change together, and the three existing fronts must be re-rendered from `Postcards/References/`.
- The hnefatafl board layout has not been generated. A layout with a provably unique four-move escape must be found by search before printing.
- The final map mechanic is deliberately undecided: cards pinned to the map, pins and cord, or a transparent overlay. Prototype pin spacing and digit legibility at true print size first; the family "9" is the riskiest shape.
- The red filter needs a home-printer colour test before any puzzle depends on it.
- HRAFN is currently assigned to the five-letter lock, but it also fits a five-ring cryptex. Only one of the two can use it.
- Which five or six of the 18 cards are active is unassigned, as is the membership of each sparse set: which ~4 cards carry a price, which ~5 carry extra text, which ~4 carry a tilted stamp and which ~3 carry an anomaly stamp.
- Both the tilted-stamp set and the hnefatafl escape now feed directional locks. That is workable and arguably good — the lock type gets taught once — but it needs two directional locks, or one of the two must be reassigned.
- The wording of the three redirect clues is unwritten.
- Every historical claim in the new page needs source-checking before it reaches a prop. The list is in the page's final section.
- Carried over from the prior session: postcards 02 and 03 still need their message and travel date, and the main compartment's opening mechanism and answer are still undecided.
