# Norse review — separate session handoff

Task: in-depth review for 2–4 players aged 16+, 60–90 minutes, self-guided with optional hints. Create new review documents only; preserve all existing documents.

Status: review and separate draft props created. No production readiness or user approval of the proposals is implied.

## New outputs

- `../Norse_Brainstorm_Review.html`: nine-tab review, 19 stable findings, 14 original puzzle/ending records, proposed 11-gate flow, all 22 card releases, 30-item persistent checklist, gallery, tests, decisions and source references.
- `Norse_Hints_Review.html`: eleven gate topics with three hints and a hidden solution, plus optional-discovery guidance. Local prototype, not published.
- `Trail_Map_4_Harald_Rune_Review.pdf`: E7 decoy moved to I7; one stem in each RAVEN column. Board back unchanged.
- `Journal_Family_Iconography_Review.pdf`: proposed Letter journal; distinguishes selected route stops from genuine decoy visits and names ordering anchors.
- `Aud_Ticket_PLAYER_ONLY.pdf`: exact original player pages 1–2, omitting answer page 3.
- `Playtest_Clue_Inserts_Review.pdf`: three Letter pages / six cue slips. Balance slip requires a real cache marker and calibrated coins.
- `Previews/`: renders of all eight new PDF pages.
- `review_content.py`, `build_review_html.py`, `build_review_props.py`, `puzzle_source_snapshot.json`, `validate_review.py`, `validation.json`: reproducible new sources and verification record.

## Key findings and proposals

Original map allows HRAFN or HRALN because E3 and E7 both satisfy the RAVEN selection. Fixed board has exactly one three-move path (253), but the printed museum ticket teaches moving/capturing other pieces. The weight puzzle lacks the last-digit deletion sketch and a complete cache/coin selector; calibration is untested. Comb BOOK and ruler distance are not complete mechanisms. A single four-letter lock cannot be preset to SOLE, BOOK and MEAD simultaneously.

Proposed flow retains eleven gates; comb and ruler gates are deferred, with their cards retained for the finale. Rollo has a two-lock join; Harald has parallel rune/MEAD branches then board. H6 releases late with transition tickets. Requires five four-digit, three three-digit, two four-letter locks and a five-letter cryptex, plus a keyed board-kit closure. The user owns some 3-digit, 4-digit and 4-letter locks; quantities and available letters are unknown.

The shared guide says eighteen postcards, but the produced deck has eighteen route cards plus four decoys. Review uses the actual 22-card deck and flags the discrepancy rather than changing the guide. The “Full” postcard PDF contains only three cards; the four LongEdge print-sheet PDFs contain only fourteen card backs. Use the 22 individual PDFs linked in the review.

## Checks

Read current brainstorm design tabs, relevant builders, handoff, guide and hints. Extracted and rendered 69 canonical source PDF pages (including all 44 postcard sides); inspected contact sheets and enlarged critical details. All eight new PDF pages visually inspected. New map back and Aud player pages checked against originals.

Re-ran original exhaustive final-order model and independently searched the fixed 11×11 board. Tested weaker printed Rollo ferry relations: still one real-card order. Tested the revised journal clues: one real-card order per trail. Tested corrected rune selection: HRAFN only. HTML local links, unique IDs, PDF link attributes and JavaScript syntax checked by `validate_review.py`; detailed results in `validation.json`.

Browser checks completed over `http://localhost:8734` in the in-app browser: all nine tabs show exactly one section, no page-level horizontal overflow at the normal desktop viewport, issue search and direct RV links work, checklist category filtering and persistence across reload work, and the gallery trail filter shows seven Harald cards. All 48 original gallery images loaded; no broken images or console warnings/errors found. Checklist test was restored to 0/30. Enlarged gallery, overview, flow, audit and checklist were visually inspected. Separate hint page has eleven closed solutions; opening one hint revealed only that hint and was visually checked. No mobile viewport test was run.

Final automated validation passes. At the end of the review, existing tracked files remained unchanged (`git diff --stat` empty); only the new review HTML and review folder were untracked additions.

## Limitations

No physical prints, stock/laminate light-transmission tests, calibrated coin readings, actual lock/closure fitting, cold team playtest, blind digit-recognition test or measured completion times. Aud’s 521 remains a recorded source tally requiring a real-sheet walkthrough. Historical claims were not comprehensively independently researched. Original historical presentation deck was not needed to resolve current mechanics and was not re-rendered.

Existing `HANDOFF.md` was intentionally left unchanged because the task expressly prohibited direct changes to existing documents. In a follow-up, the user requested committing and pushing the new review files to the current branch, `main`.

Next action: review the proposed Adventure flow and blockers, then choose whether to adopt the 11-gate pilot before buying or bulk-printing materials.
