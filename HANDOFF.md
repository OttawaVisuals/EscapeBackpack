# Project Handoff

Last updated: 2026-09-11 by Claude Code

> Session continuity only. Open design questions are **not** tracked here — they live in the
> Open questions tab of `NorseBackpack/Norse_Brainstorm.html`, each with a stable ID.
> See "Where Design State Lives" in `AGENTS.md`.

## Current Task and Status

**Session scope:** review the Norse backpack as a whole (the user's prompt asked for it explicitly — this is not the usual one-piece-per-session mode), then fold the agreed direction into the project page and the shared agent docs.

Done:

1. Reviewed the eight existing tabs of `Norse_Brainstorm.html`, `HANDOFF.md`, `AGENTS.md`, the route-plan JSON, the build scripts and the commit history. Looked at all four stamps and the three postcards at full size. Re-ran an exhaustive search over the hnefatafl blocker layout.
2. Proposed a review and a postcard architecture in chat first, per the propose-before-editing rule. The user made four decisions during that discussion, then corrected the direction once — the first postcard proposal used abstract data channels (a digit on every denomination, a letter in every imprint), which was rejected in favour of cards that carry real trivia and clues in their own voice.
3. Rewrote the Story & sequence tab: deliberately incomplete, with only the two settled anchors.
4. Added three tabs — **Postcard system**, **Open questions**, **Options** — bringing the page to eleven tabs.
5. Removed the container structure everywhere: the packing table, the codes in the puzzle entries, and the container names in rewards and reset notes.
6. Reconciled the Design spec tab with the new direction (27 targeted edits) so no superseded model is still asserted as current.
7. Added the session-working rules and the Norse design invariants to `AGENTS.md`.

## Decisions

Taken with the user this session:

| # | Decision |
|---|---|
| 1 | **The postcards are the main mechanic.** Everything else in the bag is an instrument that acts on them. |
| 2 | **All 18 cards are active** — each does a job besides the final ordering. Supersedes "five or six active, the rest quiet". |
| 3 | **Containers are unfrozen.** The six named containers and their codes are removed; they get decided once the puzzles exist. |
| 4 | **Cards arrive a few at a time** (two or three per opening), not front-loaded and not strictly one per stage. |
| 5 | **Opening puzzle rewritten.** Two luggage tags on the bag, two stand-out digits each. Postcard 01 names L'Anse aux Meadows; the tag showing that place reads first. Supersedes the `0734` postmark-plus-circled-34 mechanism. |
| 6 | **Final puzzle:** four printed maps, one per trail, plus all 18 cards. Drawing each trail's legs in order gives the four digits (candidate `1972`). |
| 7 | **Dates are interleaved** across trails, so the endgame needs splitting by stamp before ordering by date. |
| 8 | **Anomaly stamps dropped**, and the tilted-stamp channel with them. |
| 9 | **Two stamps to be redrawn** on historical grounds: Harald's labrys → a Dane axe; Aud's high-seat pillars → a comb. |
| 10 | Each card carries **two voices** — a printed publisher's caption (real trivia, and where numbers hide) and her handwriting (voice, tasks, and the selection and ordering rules). |

## Files Changed

- `NorseBackpack/Norse_Brainstorm.html` — 120 KB → 166 KB.
  - Nav: three new tabs; eleven total.
  - **Story & sequence** rewritten: premise, the two settled anchors, an explicit note that the middle and the containers are open. Packing table gone.
  - **Postcard system** (new): the three jobs, the two-voice card with an annotated diagram, the seven card verbs, the continuation-set worked example, the six-family coverage matrix over all 18 cards, the interleaved-dates figure, and what carries over unchanged.
  - **Open questions** (new): 33 entries across ST / PC / PZ / PR / HI with status pills.
  - **Options** (new): candidate middle puzzles, card mechanics (in use / available / dropped), lock and opening types, endings.
  - **Puzzle details**: `puzzles` array rewritten — a `status` field added, the opening puzzle replaced, and every container name and intermediate code removed.
  - **Props & choices**: Decided list rewritten, Still-open list replaced by a pointer to the register, packing table replaced by a "Containers and release — not decided, on purpose" note, luggage-tag and scale entries updated.
  - **Design spec**: sparse-channel model, anomaly mechanic, 18-card worksheet and wrong-trail variants replaced by a short superseded note; stamp table, gallery captions and illustration briefs updated for the Dane axe and the comb; redirect clues 1 and 2 updated; Next steps rewritten; Unresolved list replaced by a pointer.
  - Script: the corpus-worksheet generator removed (its `#corpus` host is gone).
- `AGENTS.md` — 4.2 KB → 9.0 KB. New sections: How These Sessions Work, Where Design State Lives, Agent Roles, and Norse Backpack design invariants. The HTML validation rule now says a visual browser check is possible and expected.
- `HANDOFF.md` — this file, reduced to session continuity.

Not touched: the postcard PDFs and PNGs, the build scripts, the stamp artwork, the travel-map files, and the uncommitted Aurora changes.

## Checks

- Element balance after all edits: 632 `<div>` / 632 `</div>`, 11 `<section>` / 11 `</section>`, 16 `<figure>`, 10 `<svg>`, 8 `<table>`, 6 `<style>` — all paired.
- All eleven `data-view` buttons resolve to an existing section; no orphans.
- Grepped for every removed concept (`RAVEN pouch`, `CROWN pouch`, `WELL pouch`, `archive case`, `0734`, `main compartment`, `sparse`, `anomaly stamp`, `tilted stamp`). Every surviving mention is either an explicit "this was removed / is superseded" note or a genuine reference to the physical backpack. Two stale ones found and fixed: a hint-ladder example naming the archive case, and a parked-idea note that depended on the anomaly channel.
- **Visual check done in the browser**, which previous handoffs recorded as impossible. Confirmed rendering of the rewritten Story tab, the journey steps with their new status line, the Postcard system tab (all four SVG figures, the voices panel, the coverage matrix), the Open questions register and the Options tab. Figure geometry read back from the DOM to confirm the SVGs size correctly (649 × 193–286 px inside 695 px cards).
- Hnefatafl escape counts re-derived by exhaustive search over the layout in the page: **exactly three moves has one solution** (D4 → F4 → F7 → G7); **exactly four moves has six**. Recorded in the page as `PZ-01`.
- Not run: any print test, the red-filter test, or a source check of the historical claims. The history findings in this session were checked against general knowledge only — `HI-05` still stands.

## Next Action

Build the **continuation set** on paper: four postcards, one sentence running across the seams, scissors. It proves the format, and if it does not feel good in the hand the rest of the postcard system is not worth building. Cards proposed: Markland, Bayeux, Esjuberg, Sicily — one per trail, spelling `WEIGH WHAT SHE TRADED`.

After that, in order: write card 01 properly (caption + corrected message + her voice) as the template for the other seventeen; settle the date span (`PC-03`) and assign all eighteen dates (`PC-04`); solve family D's missing selection rule (`PC-05`).

## Blockers and Notes

- Nothing is blocked on a purchase. Everything in the next action is paper and scissors.
- The uncommitted Aurora changes (`Station_Aurora_Map_Base.png`, `Station_Aurora_Vector.svg`, `convert_dxf_to_svg.py`, `Station_Map.html`, and the Aurora paragraph in `AGENTS.md`) remain exactly as found — a separate in-progress thread, untouched and unverified across several sessions now. Worth committing or stashing so it stops appearing in every `git status` review.
- Nothing has been committed. All changes are unstaged.
