# Project Handoff

Last updated: 2026-09-10 by Claude Code

## Current Task and Status

Norse puzzle, clue and prop design, continued from the prior session. This session's task was purely structural: merge the standalone design spec into `Norse_Brainstorm.html` as a new tab, per the user's stated preference to keep each project's brainstorming in one HTML file rather than splitting into a second document. No design content changed — the merge is a mechanical move plus an ordered next-steps list already present in the source.

**User preference, now recorded in `AGENTS.md`:** keep each project's brainstorming and design content in that project's single main HTML file, added as a new tab/section, rather than a second standalone HTML file. Don't create a new file for this kind of content unless the user asks for a separate document.

The eight design decisions from the prior session are unchanged (see the prior handoff in git history, commit `6a51694`, for the full list): postcard corpus and sparse/universal element split, branch-rune cipher answering HRAFN, hnefatafl escape-plus-compartment, coins and balance, comb grille, three reader tools, three redirect clues, difficulty a notch above Hiking.

The prior Codex session's postcard and route-map work remains uncommitted and untouched (that work was actually committed in `98c36ee` before this session started — a prior handoff had incorrectly called it uncommitted). Its open item is unchanged: postcards 02 and 03 still have placeholder backs.

## Files Changed

- `NorseBackpack/Norse_Brainstorm.html` — the standalone `Norse_Puzzle_Design.html` content is now folded in as a 7th tab, "Design spec" (`id="design"`), following the page's existing nav-button/hidden-`section.view` pattern. All of the spec's CSS is scoped under `#design ...` selectors so it cannot leak into or be affected by the other six tabs (verified — see Checks). The header's separate link to the old file was removed; the "Decided / Still open" panel in Props & choices now links to the in-page tab instead. The two small scripts that draw the HRAFN branch runes and the 18-card corpus worksheet were appended to the page's existing bottom `<script>` block as self-contained IIFEs.
- `NorseBackpack/Norse_Puzzle_Design.html` — deleted (`git rm`). Its content lives entirely in the brainstorm page's Design spec tab now.
- `AGENTS.md` — added one line to Working Rules recording the single-file preference above. Staged as its own hunk with `git add -p`; the user's separately in-progress, unrelated Aurora-note edit to this same file was deliberately left unstaged and is **not** part of this commit.
- `HANDOFF.md` — this handover.

No other file was modified. The unrelated local Aurora changes (`Station_Aurora_Map_Base.png`, `Station_Aurora_Vector.svg`, `convert_dxf_to_svg.py`, `Station_Map.html`, and the AGENTS.md Aurora paragraph) were left alone and are not part of this commit.

## Decisions

- One HTML file per project for brainstorming/design content, going forward. This session is the first application of that rule — the Norse project now has exactly one such file again (`Norse_Brainstorm.html`), matching the pattern before the previous session split it.
- Scope all page-specific CSS added to a shared multi-tab HTML file under that tab's container id (here, `#design ...`) rather than introducing bare classes, so new content can never silently restyle existing tabs and vice versa.
- Reused the existing `.eyebrow` class for section kickers in the new tab instead of importing a duplicate `.kicker` class, since they serve an identical role — keeps the merged page's CSS from growing two parallel systems for the same thing.

## Checks

- `Norse_Brainstorm.html` opened locally in the browser: 7 nav buttons, 7 `section.view` elements, `#design` present, no console errors.
- Corpus worksheet renders all 18 cards under 4 trail headings; 5 HRAFN rune SVGs generate correctly.
- No horizontal overflow at 1200 px width.
- Both diagrams in the Design spec tab render at their intended sizes (560×370 and 340×340), not stretched.
- Clicking the "Design spec" nav button correctly shows only that tab (verified via `hidden` attribute state, not just visually).
- Scoping verified directly: after adding `#design`-scoped rules, the Prototype & tests tab's own (unrelated, pre-existing) `.runes` element was re-checked and still computes its original styling (35px font, block display, 7px letter-spacing) — confirming the new scoped CSS did not leak into or override the older, same-named class used elsewhere on the page.
- The in-page link from the Props & choices tab ("Design spec tab") was clicked programmatically and correctly switched the active view.
- No print test, no prop built, no physical validation of any kind — unchanged from before, since no design content changed this session.

## Next Action

Unchanged from the prior session — this was a structural merge only. The next content step is still: assign the sparse sets — decide which of the 18 cards carry a price, an extra printed line, a tilted stamp and an anomaly stamp, using the worksheet in the Design spec tab. It's a pure design decision needing no purchase or test, and all postcard artwork depends on it.

The full ordered list is in the Design spec tab's "Next steps, in order" section: assign sparse sets → design the four stamp series → re-render the three existing fronts at the new size → write the aunt's letters → solve the hnefatafl board → prototype the final map → run print and filter tests → source-check the history.

## Open Design Issues

Unchanged from the prior session (all still live in the Design spec tab of `Norse_Brainstorm.html`):

- The 18-card postcard set needs its artwork re-rendered, not rescaled. Current fronts are 1536×1024 px (3:2); 5×3.5 in at 300 dpi is 1500×1050 px (10:7). `SIZE` and `PAGE` in `Postcards/build_postcard_collection.py` must change together, and the three existing fronts must be re-rendered from `Postcards/References/`.
- The hnefatafl board layout has not been generated. A layout with a provably unique four-move escape must be found by search before printing.
- The final map mechanic is deliberately undecided: cards pinned to the map, pins and cord, or a transparent overlay. Prototype pin spacing and digit legibility at true print size first; the family "9" is the riskiest shape.
- The red filter needs a home-printer colour test before any puzzle depends on it.
- HRAFN is currently assigned to the five-letter lock, but it also fits a five-ring cryptex. Only one of the two can use it.
- Which five or six of the 18 cards are active is unassigned, as is the membership of each sparse set: which ~4 cards carry a price, which ~5 carry extra text, which ~4 carry a tilted stamp and which ~3 carry an anomaly stamp.
- Both the tilted-stamp set and the hnefatafl escape now feed directional locks. That is workable and arguably good — the lock type gets taught once — but it needs two directional locks, or one of the two must be reassigned.
- The wording of the three redirect clues is unwritten.
- Every historical claim in the Design spec tab needs source-checking before it reaches a prop. The list is in the tab's final section.
- Carried over from earlier sessions: postcards 02 and 03 still need their message and travel date, and the main compartment's opening mechanism and answer are still undecided.
