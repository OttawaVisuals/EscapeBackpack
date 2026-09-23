# Norse review — separate session handoff

## Latest follow-up — base-page integration and commit authorization, 2026-09-22

User explicitly requested updating the base HTML and committing/pushing. `../Norse_Brainstorm.html` now contains the same full approved specification and visual, with active puzzle records, prop specifications, sequence and open questions updated. Retired mechanisms are labelled as superseded. Added `sync_base_updates.py`; rebuilding the review synchronizes the shared approved section into the base. Root `../../HANDOFF.md` now records this session. This follow-up supersedes the earlier original-preservation restriction for those files; production PDFs and postcard builders remain unchanged.

Checks passed: full review rebuild and validator, base unique IDs and all inline JavaScript syntax. Browser checks over local HTTP confirmed the base Approved changes tab and rune puzzle render correctly, all 14 puzzle cards exist, and no console warnings/errors or desktop horizontal overflow occur. Earlier review/mobile/hint checks below also passed. No physical test or print proof was performed. User authorized committing and pushing this completed batch to `main`.

Next action: choose calculator versus wheels and define the coin inventory/value key before producing revised A1/A3 and player-only perch/cue print files.

## Current session — approved tally and five-perch designs, 2026-09-22

User accepted the five-perch visual and requested adding it and the coin-tally mechanism to the brainstorming HTML, including what postcards need changing. Updated `../Norse_Brainstorm_Review.html` with an Approved changes tab containing both complete mechanisms, the accepted visual, exact perch-edge table, replacement A1/A3 paragraph drafts, production status and superseded mechanism history. Adventure flow, puzzle audit, decisions, prop checklist, physical checks and reset instructions now agree. RV-20/RV-21 mark the approved mechanisms; other review proposals keep their status. PR-24 (tally device), PR-25 (coins/values/marks), PR-26 (perch print proof) are new open IDs; existing PR-21–23 were not reused.

G7: select coins by cache mark, sum fictional values to 3705, show on calculator or four-wheel counter, turn whole display upside down for SOLE. No weighing, decimals, truncation or calibration. Exact inventory, values, marks and calculator-versus-wheels remain open. G8: corrected map and unchanged H4/H5 yield HRAFN; H–R–A–F–N flight labels give 2648; one four-digit lock directly secures the board pouch. Perch card is released inside G7. No cryptex or extra keyed closure. Updated hardware count: six four-digit, three three-digit and two separate four-letter locks. 3D-printed hnefatafl pieces remain suitable.

Changed sources: `approved_changes.py` (new), `review_content.py`, `build_review_html.py`, `build_review_hints.py`, `validate_review.py`; regenerated review HTML, `Norse_Hints_Review.html` and `validation.json`. The accepted diagram is linked from `../../output/visualizations/norse-five-perches-comparison.png` (created during the preceding visual discussion; preserve the accompanying concept files). Checklist uses a new saved version to prevent a checked retired prop from marking a new prop ready; prior browser data remains intact.

Postcards: A1’s second paragraph requires replacing weighing with value addition; A3’s second paragraph should refer to the tally. Drafts are in the HTML; original production builders, PDFs and gallery backs remain unchanged. H4/H5 need no change. The earlier balance/truncation slip is explicitly superseded everywhere it is offered in the review; a replacement cue is drafted, with revised print file still pending. The perch comparison contains answers and is not a player print file.

Validation passed: full review validator, new HRAFN/perch-code and release-order assertions, links/images/IDs, JavaScript syntax, and whitespace checks. Browser inspection over local HTTP confirms ten tabs, the new specification and loaded visual, updated flow/checklist, RV-20/RV-21 filtering, and both G7/G8 hint solutions. Desktop and 390px layouts checked without page overflow; no console warnings/errors. Physical coin/display tests and print-size proof remain unperformed. No commits or pushes in this session. Original brainstorm and root handoff remain unchanged under the original preservation instruction.

Next action: choose calculator versus wheels and define the coin inventory/value key, then produce the revised A1/A3 and player-only perch/cue print files.

## Latest follow-up — five-perch visual proposal, 2026-09-22

User requested a visual specification of the proposed HRAFN-to-four-digit conversion. Created an interactive conversation visual at `../../output/visualizations/norse-five-perches.html`, with a browser-check wrapper beside it. One proposed half-Letter card shows eight possible perches, twelve numbered undirected connections and four answer boxes. Players use the separately decoded HRAFN to select five stops and read four direct connecting edges: H–R = 2, R–A = 6, A–F = 4, F–N = 8. Proposed code 2648; it is not an adopted lock setting. Player view does not print HRAFN, highlight the route or show the answer. A designer-only toggle adds direction arrows and the code. No geographic map or final shape is involved.

Visual/interaction checks: player/solution toggle works; network has no crossing paths or duplicate labels; desktop and phone views inspected, and overlapping optional stop labels were removed. No console warnings/errors observed. This is a conceptual layout, not a tested print-ready prop. Existing game documents, hints and lock assignments remain unchanged. Next action: user evaluates whether this extra route-reading step is satisfying enough to keep. Nothing committed or pushed in this follow-up.

## Latest follow-up — hint companion design, 2026-09-22

User requested a nicer hint website. Redesigned the new 11-puzzle review companion with a forest/paper/brass field-journal theme, decorative compass, grouped desktop index, mobile puzzle selector, one visible puzzle, native folded hints and a separate two-step answer reveal. All 44 original hint/answer texts and both optional discoveries are retained. Leaving a puzzle closes its hints and answers; reloading starts with all disclosures closed. No external fonts, scripts or images are required.

Changed `Norse_Hints_Review.html`, added `build_review_hints.py` and `hint_companion.template.html`, and updated `build_review_html.py` to call the dedicated hint builder so regeneration preserves the design. `validate_review.py` now explicitly uses UTF-8 and a timeout for JavaScript syntax checking on Windows. The original `../norse-hints.html`, brainstorms, printable props and root handoff remain untouched.

Checks: full existing review validation passes; exact text comparison passes for all 44 hints/answers; unique IDs and local anchors pass; JavaScript syntax and `git diff --check` pass. Visually inspected in the in-app browser over HTTP at desktop, 390px and 320px widths with no horizontal overflow. All 12 index destinations select exactly one panel. Checked keyboard disclosure, mobile selection, deep-link reload, browser Back, closing hints, and the separate solution reveal. No browser console errors or warnings. Viewport override reset; finished page left open. No physical game testing was performed. Without JavaScript the hint disclosures remain usable but solutions require JavaScript, as explained on the page.

The user confirmed the Norse hint page and requested committing and pushing this redesign to `main`. The earlier review batch was committed and pushed as `8caee7b`. Next action: check the refreshed companion on the hosted site after deployment.

## Initial review record

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
