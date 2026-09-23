# Project Handoff

Last updated: 2026-09-22 by Codex

## Session close — 2026-09-22 — Adopted coin tally and raven perches in both brainstorms

**Task/status:** user approved replacing weighing and the cryptex, requested updating the base HTML as well as the review, and explicitly authorized committing and pushing. Implementation and verification complete. The base-page request supersedes the earlier instruction to preserve that original document.

**Changes:** `NorseBackpack/Norse_Brainstorm.html` now has the full Approved changes tab and matching puzzle records, prop specifications, sequence and open-question entries. Superseded explanations remain labelled as history. The review HTML, review hint companion, checklist and builders agree. `Review_2026-09-22/approved_changes.py` holds the shared approved section; `sync_base_updates.py` keeps it in the base when rebuilding the review. The accepted visual and its concept sources are under `output/visualizations/`.

**Decisions:** selected coin values total 3705; rotate the calculator or four-wheel display for SOLE. Decode HRAFN and follow four numbered flights for 2648 on the board-pouch lock. The perch card is released before that lock. Cryptex, keyed closure and weighing are retired. A1/A3 replacement paragraphs are drafted in both HTML pages; production postcard PDFs, builders and gallery backs remain unchanged. H4/H5 need no changes. Remaining coin/device/print choices are recorded in PR-24–26 in the base page.

**Checks:** rebuilt review and hints; full review validator passed, including unique rune extraction, board solution, final routes, links, JavaScript and new perch-code/release assertions. Base inline JavaScript syntax and unique IDs passed. Visually checked base Approved changes and rune puzzle over local HTTP; all 14 puzzle cards render and no console warnings/errors or desktop page overflow were found. Review and hints were also checked at desktop and 390px. Physical coin/display testing and print-size proofs remain unperformed; no claim of measured play time.

**Next action:** choose calculator versus wheels and define the coin inventory/value key before producing revised A1/A3 and player-only perch/cue print files.

## Session close — 2026-09-21 — Regenerated all 22 postcard back images from the current print PDFs

**Task:** user noticed the postcard gallery's back-of-card images (`Postcards/Postcard_*_Back.png`,
shown in the Postcards tab) didn't reflect the latest message/Fun Fact text — asked to update them.

**Root cause: the gallery `_Back.png` files were never generated from the same data as the PDFs.**
Checked `build_postcard_A1_pdf.py` (representative of all 22 build scripts): `draw_front_card()`
only places `Postcard_*_Front.png` full-bleed with no text, so the Front gallery images are already
byte-identical to the PDF's own source art — those did not need touching. `draw_back_card()` draws
the message, Fun Fact, stamp, postmark and element mark entirely from hardcoded strings in the
script — there is no code path that ever wrote those pixels out to `_Back.png`. That file was a
separate, one-off render that drifted out of sync every time a card's text was revised afterward
(confirmed: re-rendering all 22 changed all 22 — none matched their current PDF).

**Fix:** rendered page 2 (the back) of each `output/pdf/Postcard_*_Print.pdf` to PNG with PyMuPDF at
300dpi (matching the existing 1500×1050 convention exactly) and overwrote the corresponding
`NorseBackpack/Postcards/Postcard_*_Back.png` in place — same filenames, so no HTML changes needed.
This makes the print PDF the one source of truth for both artifacts going forward; any future text
edit only needs a PDF rebuild + this same re-render step to stay in sync.

**Files changed:** 22 PNGs under `NorseBackpack/Postcards/` (`*_Back.png` only — Fronts untouched,
confirmed unnecessary). No PDF, script or HTML changes.

**Checks run:** confirmed all 22 outputs are exactly 1500×1050 RGB, matching the pre-existing
convention. Visually inspected two renders directly (A1 Dögurðarnes, R6 Roumare Forest) — text,
stamp, postmark and Fun Fact box all render cleanly and match the current build-script content.
`git status` confirmed exactly the 22 `_Back.png` files changed, nothing else touched.

**Next action:** none outstanding from this task. If postcard text changes again in a future
session, re-run the same PDF-page-to-PNG render for the affected card(s) rather than hand-editing
the PNG.

## Session close — 2026-09-21 — Fixed broken map images on GitHub Pages; added a consolidated tickets/props gallery

**Task:** two follow-ups in the same day's thread. (1) User reported the trail-map images showing
as broken on the live site. (2) User asked to group all the scattered ticket/prop images (Rouen,
Aud's museum, L'Anse museum, hnefatafl, transition tickets, luggage tags, journal page — previously
spread across four different tabs) into one place.

**(1) Root cause: GitHub Pages runs Jekyll by default, which silently excludes any folder starting
with `_`.** `NorseBackpack/Props/_Renders/` (all 16 rendered map/prop preview PNGs from earlier
sessions) was committed correctly and worked fine locally, but Jekyll's build never published it to
`ottawavisuals.github.io` — every image in that folder 404'd on the live site while working
everywhere else. Fixed by adding `.nojekyll` at the repo root, the standard fix for a plain static
HTML site with no Jekyll templating needs. Also hardened `.gitattributes` with explicit `binary`
markers for `png/jpg/jpeg/docx/pptx/xlsx` as a safety net — `core.autocrlf=true` is set on this
machine and PNGs weren't previously covered, so a checkout on a different machine could in theory
have silently corrupted them even though nothing here showed that actually happening.

**(2) New "All tickets & printed props at a glance" gallery**, added near the top of the Props &
specs tab (`#all-tickets`, right after the historical-claims warning box). Eight cards, reusing the
existing `.postcard-gallery`/`.postcard-item` pattern: Rouen ticket, Aud's Treasure Museum ticket,
L'Anse museum ticket, hnefatafl ticket, hnefatafl board-setup insert, the three transition tickets,
luggage tag inserts, and the journal page. Each card links back to its tab of origin for the full
design write-up — **this gallery is a visual index, not a new source of truth**; none of the
original write-ups in Open questions / Final riddle / Puzzles & locks / Travel routes were moved or
duplicated in substance.

**Files changed:** `.nojekyll` (new), `.gitattributes` (binary markers added),
`NorseBackpack/Norse_Brainstorm.html` (new gallery section, ~80 lines).

**Checks run:** tag-balance parser — same 2 pre-existing mismatches, nothing new. Manual
`python -m http.server` (still the working fallback — `preview_start` remains unreliable across
sessions). No console errors. Confirmed via `document.getElementById('all-tickets')` in the live
page that all 8 cards and 14 images are present, and checked `img.complete`/`naturalWidth` on every
one of the 14 — all loaded successfully, none broken.

**Not done:** did not verify the fix against the actual live `ottawavisuals.github.io` URL — GitHub
Pages needs a minute or two to rebuild after the push, and this session's checks were all against a
local server. Worth a real look at the live site to confirm the map images now load there too.

**Next action:** open the live site and confirm the Travel routes tab's four map images now load
(the original bug report), and glance at the new Props & specs gallery.

## Session close — 2026-09-21 — All 4 trail maps as images; fixed a mis-scoped CSS bug making stamps/icons huge

**Task:** follow-up to the same-day prop-image session. User asked for (1) all four trail maps
shown as images in the Travel routes tab, since PDFs force a download on their work computer, (2)
stamps and other icon sets in the Design guide tab made smaller and laid out side by side instead
of each filling the full width, (3) any remaining "final props" (museum tickets etc.) shown as
images in Props & specs, and (4) a light pass to remove stale entries.

**(1) Maps.** Aud and Harald already had full-sheet renders from the earlier session. Rendered
Leif's and Rollo's sheets the same way (`Props/_Renders/Trail_Map_1_Leif_Print.png` /
`_2_Rollo_Print.png`, PyMuPDF, 2× zoom) and added them as a lead image above their existing vignette
pairs, so all four map gallery entries now show the full sheet without needing the PDF link.

**(2) Stamps/icons — this was a real pre-existing bug, not just a sizing preference.** The four
route stamps and both icon sets (Bayeux rebus icons, Rollo icon set) were rendering at full native
resolution (1145×1374 px stamps, 1024×1024 px icons) stacked one-per-row, because:
- `.stamp-gallery`, `.stamp-card`, `.stamp-card img` and two children rules were all scoped
  `#design .stamp-*`, but the actual stamp gallery markup lives in `<section id="guide">` (Design
  guide tab), not `#design` (Props & specs). The selector never matched anything, so no grid layout
  and no `width:100%` ever applied. Rescoped all five rules to `#guide`.
- Once the grid rule matched, the stamp images still rendered at full native size — a classic CSS
  Grid gotcha: a grid item's default `min-width` is `auto`, which for an image child resists
  shrinking below the image's intrinsic size. Added `min-width:0` to `.stamp-card`.
- Added a new `.icon-grid` modifier class (`minmax(90px,120px)`, small tiles) and applied it to the
  rebus-icon and Rollo-icon `<div class="grid">` containers, which were using the shared `.grid`
  class's `minmax(280px,1fr)` — appropriate for text cards elsewhere but too large for a small icon
  set. Had to scope this rule `#guide .grid.icon-grid` specifically, because an existing
  `#guide .grid{...}` rule (1 ID + 1 class) otherwise outranks a bare `.grid.icon-grid` (2 classes)
  in specificity and silently wins.
- Verified via `getComputedStyle`/`getBoundingClientRect` in the live page (screenshots were
  unreliable again this session — see Checks below): stamps now render at 34×41px inside 60px
  cards, rebus/Rollo icons at 40×40px, all `display:block` as intended.

**(3) Remaining props.** Everything else was already covered by the earlier session's edits.
Found one gap: Luggage Tag Inserts only had a link to the rendered PNG, not an inline `<img>` (it
lives inside a JS string literal for the puzzle-family data, which was a lighter touch at the time).
Converted it to a proper `<div class="prop-preview">` image, consistent with the others.

**(4) Stale-entry pass.** Searched for "Not built yet" / "not yet built" and stray `pill open`
markers across the file. Found only one other "not built yet" claim (a specific in-card sketch
detail, not a separate file — can't verify true/false from the filesystem, left alone) and one
already self-flagged `<span class="pill open">Stale</span>` list item inside the Aud treasure-route
"Decided player flow" — it already explains itself ("This describes the shelved Dalir panel design,
not the current map — see the note above"), which is exactly the AGENTS.md convention (mark
superseded text in place rather than delete it silently), so left it as-is rather than deleting.
**Did not do a deeper cleanup pass** — everything else found was either a legitimately open item
(PR-19/20/21 physical props not yet 3D-printed, PZ-18's "not run" test) or existing superseded-note
history worth keeping. If there's a specific stale section the user has in mind, worth naming it
directly next time rather than me guessing broadly.

**Files changed:** `NorseBackpack/Norse_Brainstorm.html` (CSS scope/specificity fixes, 2 new map
gallery images, 1 prop-preview conversion), 2 new PNGs under `NorseBackpack/Props/_Renders/`.

**Checks run:** tag-balance parser — 2 mismatches, both pre-existing before this session, none new.
Manual `python -m http.server` (same workaround as the previous session — `preview_start` got stuck
in `"starting"` status a third time in a row now, worth investigating outside a single session). No
console errors. `read_network_requests` confirmed all new/existing `_Renders/*.png` and
`Postcards/Stamps/*.png` requests return 200/304. Stamp and icon sizing confirmed via
`getComputedStyle`/`getBoundingClientRect`, not a visual screenshot — the in-app browser's
screenshot tool timed out repeatedly this session regardless of scroll position.

**Next action:** open the page yourself and eyeball the Design guide tab's stamp/icon rows and the
Travel routes tab's four map images — this session's verification was DOM measurements, not a look.

## Session close — 2026-09-21 — Committed the pending Norse batch; added rendered-image previews for printed props

**Task:** user asked (1) whether every postcard/printed document was committed and pushed, and (2)
to update `Norse_Brainstorm.html` so printable props show as images inline, since they're reviewing
the puzzle sequence today from another computer and PDFs are harder to check at a glance than images.

**Part 1 — commit/push.** ~107 modified/new files were sitting uncommitted (all 22 postcard build
scripts, `TravelMap/`, `Tools/`, every `output/pdf/*` and the new `output/docx/*`). One blocker:
`NorseBackpack/TravelMap/NUL` — a 0-byte Windows-reserved filename, almost certainly created by a
stray `> NUL` redirect run under cmd.exe instead of PowerShell — was blocking `git add -A`. Deleted
it (untracked, empty, not real content) and committed everything else in one batch
(`5607a6c`), then pushed. `git status` now shows two more files touched by something outside this
session between the commit and the next status check (`Norse_Brainstorm.html` +1 line, one straight
`'` → curly `’` apostrophe in `stops.js`) — folded into this session's commit since they're trivial
and unrelated to investigate further.

**Part 2 — image previews.** Postcards already had front/back PNGs embedded (83 files, pre-existing).
The actual gaps, found by diffing every `output/pdf/*` against the HTML for a nearby `<img>`:
- Aud's and Harald's trail-map gallery entries had no images (Harald's entry still read "Not built
  yet" even though `Trail_Map_4_Harald_Print.pdf` exists and is tracked — confirmed via
  `build_trail_maps_pdf.py` that page 2 really is the hnefatafl board-setup insert composited onto
  Harald's map back, so that stale-status text is now corrected, not just illustrated).
- Six more built props were mentioned in prose but never linked or shown: `Aud_Ticket`,
  `Museum_Ticket`, `Luggage_Tag_Inserts`, `Hnefatafl_Board_Setup_Insert`, `Hnefatafl_Ticket`,
  `Journal_Family_Iconography`, `Transition_Tickets` (the last two had no `Open PDF` link at all).

Rendered each relevant PDF page to PNG with PyMuPDF (`NorseBackpack/Props/_Renders/`, 15 files,
2–3× zoom) rather than hand-building new art, since these are print-ready layouts, not concept art —
a faithful render is what "easier to see than the PDF" calls for. Added a small `.prop-preview` CSS
class for the inline (non-gallery) insertions and reused the existing `.postcard-pair` gallery
pattern for the two trail-map entries. No puzzle content, wording, or design decisions changed —
this was image display only.

**Checks run:** a lenient HTML tag-balance parser confirms no new mismatches (2 pre-existing
mismatches, both present before this session's edits, unrelated to the touched regions). All 15
new image files confirmed on disk. `preview_start` came up stuck in `"starting"` status again
(same failure mode as the 2026-09-21 session before this one) — worked around with a manual
`python -m http.server 8741` from Bash, same fix that session already found. Loaded
`Norse_Brainstorm.html` over real HTTP, no console errors, and `read_network_requests` confirmed
all 14 embedded `_Renders/*.png` requests returned `200 OK`. Did not get a visual screenshot
confirmation (the in-app browser's `scroll_to` was not moving the viewport this session, screenshots
kept landing at the page top) — network-200 plus DOM presence via `find` is the verification that
exists for this session, not a pixel-level look.

**Files changed:** `NorseBackpack/Norse_Brainstorm.html` (CSS + 9 edit sites), 15 new PNGs under
`NorseBackpack/Props/_Renders/`, plus the full batch from Part 1.

**Not done:** did not touch the `output/pdf/Postcard_Sheet_*` print-layout sheets, the `*_ANSWER.pdf`
trail-map keys, `Postcard_L2_L3_TopEdge_Test.pdf`, or `Trail_Map_1_Leif_ART_GUIDE.pdf` — judged as
production/test/internal-reference files rather than props a player-facing review needs to see, but
this was a judgment call and worth confirming if wrong.

**Next action:** if `preview_start` getting stuck in `"starting"` keeps recurring across sessions,
worth investigating outside a single working session — it's now failed twice in a row.

## Session close — 2026-09-21 — Two broken-markup bugs found by the browser check that was blocked last session

**Task:** remote session, no specific brief. Picked up the previous session's stated next action —
open `Norse_Brainstorm.html` in a real browser and confirm PR-23 renders and the Open questions tab
still works — which the last session could not run because `static-preview` never came up.

**The preview infrastructure works again, but not via `preview_start`.** `preview_start` reported a
server on an auto-assigned port and then nothing listened there (`curl` → connection refused, no
server logs). Starting `python -m http.server 8741 --bind 127.0.0.1` directly from Bash worked
first time and the in-app browser loaded `http://localhost:8741/...` normally. So the blocker last
session was `preview_start`'s spawned process, not the browser, not `file://`, and not the page.
Worth trying the manual server first next time rather than treating HTML checks as unrunnable.

**Bug 1 — `NorseBackpack/TravelMap/stops.js` had a JavaScript syntax error and did not load at all.**
Line 96, the Aci Castello (`h-sicily`) note added by the 2026-09-20 "H5 resolved to Aci Castello
everywhere" session, contained a raw ASCII apostrophe inside a single-quoted string: `'... Harald's
own Sicilian service ...'`. That terminated the string early and threw `SyntaxError: Unexpected
identifier 's'`, which killed the whole file — `window.NORSE_SOURCES`, `window.NORSE_PEOPLE` and all
72 entries of `window.NORSE_STOPS` were undefined on every page that loads it. **This was committed
at `HEAD`**, so it had been shipped and broken for a day. Fixed by changing that one apostrophe to a
typographic `’`, which is the file's own convention everywhere else (28 other instances).

**Bug 2 — one unclosed `<div>` in `Norse_Brainstorm.html`.** The pre-existing 1253-open / 1252-close
imbalance the last session flagged as "worth tracking down" is real markup, not a false positive from
a script template: `<div class="splitdemo">` in `<section id="lab">` (Prototype & tests) was never
closed, so the browser auto-closed it at `</section>`. It rendered correctly by luck. Added the
missing `</div>` before line 2484's `</section>`; the file now balances at 1253/1253, and every other
paired tag (`section`, `details`, `table`, `figure`, `ul`, `ol`) was already balanced.

**Files changed:** `NorseBackpack/TravelMap/stops.js` (one character), `NorseBackpack/Norse_Brainstorm.html`
(one added `</div>`). No design content was touched and no PDFs or assets were rebuilt.

**Checks run, all over real HTTP in the in-app browser:**
- `node --check` on `stops.js` — fails before the fix at line 96, passes after. Also ran it across
  every tracked `.js` outside `vendor/`: no other syntax errors in the Norse files.
- Reloaded the page after the fix: `window.NORSE_STOPS.length` → 72, `NORSE_PEOPLE` → 4, and the
  `h-sicily` record is present and reads "Aci Castello · Sicily". No new console errors across four
  further reloads (the two `SyntaxError` entries in the console log are the stale pre-fix ones).
- Deep links work: `#view-lab`, `#view-routes`, `#view-design`, `#view-questions` each show exactly
  one section.
- Prototype & tests tab after the `</div>` fix: both `.splitdemo > .panel` children present, the
  hnefatafl board renders its 121 cells, the 3 rune buttons are there.
- **PR-23 confirmed rendering** — it lives in the **Open questions** tab (as `#q-PR-23`, correct for a
  `PR-` id), not in Props & specs as the last handoff's wording implied. Pill reads "Decided", body
  text is complete, 697px tall, screenshotted. Open questions tab is healthy: 72 rows
  (ST 5 · PC 19 · PZ 20 · PR 23 · HI 5).

**Also worth knowing:** `git status` on this machine opened the session showing ~106 files as
modified. They were not. A stale index (mtimes touched, contents identical) — the first real
`git status` refreshed it and the tree is clean, one commit ahead of `origin/main` (`8fc1e0f`,
unpushed). Nothing was reset or discarded to get there.

**Not done:** the `Aud_Map_Designer.html` artifact resync noted in the trail-map session is still
outstanding. `Norse_Brainstorm.html` was not given a new question/decision entry for either bug —
both are code defects, not design decisions.

**Next action:** commit these two fixes (nothing is committed yet — the user has not been asked).
The `stops.js` one in particular is a shipped regression worth landing before any further map work.
## Session Close — 2026-09-20 — Trail map printer margins: fixed, then maximised

**Task:** the user's home printer was leaving more blank space on the left of the printed trail
maps than the right. Asked to make the padding even, "knowing the margins of my printer" — then,
once that was done, asked instead to use the print area right up to the margin on every side to
maximise the map, accepting an uneven-looking border as the tradeoff.

**Root cause was not a left/right asymmetry.** Found the printer's real non-printable-area spec
in `Hiking_Trip/Support.xlsx` ("Info" sheet: Canon, https://support.usa.canon.com/kb/s/article/ART163725) —
top 3mm, side 3.4mm (same both sides), bottom 16.7mm. The maps' original margin was a uniform
0.30in (7.6mm) on all four sides, which cleared top and sides but not the 16.7mm bottom. The
print driver's own "fit to printable area" step was almost certainly rescaling/repositioning the
whole page to avoid clipping that edge, which is what read as uneven padding.

**Three passes, same mechanism, different target margins:**
1. First pass: `MARGIN` set to a uniform `16.7mm` on all four sides (the largest of the printer's
   four minimums) — guarantees nothing prints in a non-printable zone anywhere, and keeps the
   border visually even.
2. Second pass, per the user's follow-up: each side now uses its **own** true minimum plus a
   0.5mm safety pad instead of sharing the largest one — `MARGIN_TOP = 3.5mm`, `MARGIN_SIDE =
   3.9mm` (from the Support.xlsx spec's "side 3.4mm"), `MARGIN_BOTTOM = 17.2mm`. Maximises the
   map area but the printed border is no longer even: thin on three sides, thick at the bottom.
3. Printed a diagnostic (see below) that showed the actual margins didn't match pass 2's numbers.
   The user then supplied a corrected, per-edge reading: top 3.0mm, bottom 16.7mm, left 6.4mm,
   right 6.3mm — first treated as rounding noise on one shared 6.35mm value (both were logged as
   "0.25 inch"), so pass 3 set `MARGIN_SIDE = 6.85mm` (6.35 + 0.5 safety) uniformly; top and
   bottom were already correct from pass 2. **This fixed it** — the user confirmed the Canon
   preview now looks right, so the print driver's own "fit to printable area" rescale (see the
   diagnostic finding below) was never a separate bug; it was entirely explained by pass 2's
   `MARGIN_SIDE` (3.9mm) being too small.
4. Fourth pass, cosmetic-only: the user re-supplied the same left 6.4mm / right 6.3mm as two
   distinct values rather than accepting the averaged reading, so `MARGIN_SIDE` was split into
   `MARGIN_LEFT = 6.9mm` and `MARGIN_RIGHT = 6.8mm`. The actual geometry change this causes is
   negligible — the page centre moves 0.14pt (~0.05mm) because the left+right total is unchanged
   (13.7mm either way, just split differently), and the per-trail scale ratio computed out to
   exactly 1.0 for all four maps. Rebuilt anyway for correctness; output was pixel-identical in
   every check (same collision/skip list per trail) to pass 3's, confirming the split really is
   cosmetic at this margin size.

**Both margin changes shrink or reshape the map area**, which is a genuine rescale, not just
cosmetic, and had to be propagated everywhere a page position is hand-placed rather than
computed live. Because pass 2's margins are no longer symmetric top/bottom, the page centre
itself moved vertically (asymmetric top/bottom means the centre is no longer the paper's
geometric centre) — pass 1 got away with a pure scale-about-a-fixed-point; pass 2 needed a
scale-and-shift, computed per trail (the ratio differs per trail now since Aud's own scale
binding flipped from width- to height-bound between the two passes). Every fixed page-point was
put through this exact transform, not re-placed by eye:
- `LEIF_ART`, `ROLLO_ART`, `ROLLO_WORDLOCK_ART` — the hand-placed decorative vignette boxes
  (originally tuned by search to avoid the coastline, route and labels).
- Aud's legend box position.
- Every page point in `aud_features.json` (Aud's 140-feature hand-drawn road/symbol layer,
  exported from the designer at the original geometry) and `aud_base.js` (regenerated fresh via
  `export_aud_base.py` both times, since it derives from the build script directly rather than
  storing points).

**One real regression caught and fixed (pass 1, still holds after pass 2):** the smaller map area
cost Aud's stop label "Dögurðarnes / Dagverðarnes" its last open slot — a genuine trail stop
going unlabelled, not just a decorative town name. Added two more (last-resort, centred,
further-out) candidate positions to `Labeller.place()`'s search list; confirmed against a
baseline rebuild of the unmodified script that no real stop, on any of the four maps, lost its
label in either pass. Decorative corpus-town collisions shift slightly between passes (different
non-stop names get dropped) but never got worse than the original baseline.

**Checked other prop builders** (journal page, tickets, postcards) for the same failure mode:
none of them are exposed to it. They're all a smaller item centred with generous margin on a
Letter sheet and meant to be trimmed, so the printer's non-printable edge falls inside their own
blank border regardless. Only the trail maps print full-bleed to the actual sheet edge as the
final laminated object, so they were the only documents that needed this fix.

**Files changed:** `NorseBackpack/TravelMap/build_trail_maps_pdf.py` (per-side margins, rescaled
art boxes, Aud legend position, extra label-placement fallback tier), `NorseBackpack/TravelMap/
aud_features.json` (814 page points, rescaled twice), `NorseBackpack/TravelMap/aud_base.js`
(regenerated), all eight `output/pdf/Trail_Map_*.pdf`.

**Diagnostic finding (between passes 2 and 3), worth keeping:** the user sent a screenshot of the
Canon IJ print preview after pass 2. Measured it pixel-by-pixel (locating the paper edge via its
hatched non-printable-area pattern vs. the actual map content edges) and found the previewed map
was reproduced at roughly 93% of true size with the left margin visibly bigger than the right —
neither of which matches anything this file asks for. That pointed at the print driver's own
"fit to printable area" pass rescaling/recentring the whole page on top of whatever margins the
PDF already has, which no amount of in-file margin tuning can fully control. Built a `.docx` with
the identical image and identical margins as a cross-check (below), specifically so the user could
tell whether a size/position mismatch is Word-and-Canon-driver behaviour rather than something
wrong in the PDF. The user's pass-3 correction (real numbers from wherever they read the spec)
turned out to explain the visible left/right gap on its own — pass 2's `MARGIN_SIDE` (3.9mm) was
just too small — so the driver's own behaviour is still an open question, not confirmed as a
separate problem.

**Checks run:** all four trails rebuilt clean after each pass, no assertion failures. Compared
collision/skip output against a rebuild of the unmodified script (via `git show HEAD:...`) trail
by trail — no real stop lost its label on any sheet, only decorative corpus-town labels varied.
Rendered all four Print PDFs to PNG at 150dpi after each pass and inspected them: Leif's and
Rollo's vignettes still sit in clear water/land at their intended spots, Aud's hand-drawn
road/symbol layer still lines up exactly with the coastline (proof the point-rescale was exact
every time), the legend box is fully inside the map frame, Harald's board-setup back page is
unaffected (its layout is independent of the margin constants). Pass 3: checked every stored
`aud_features.json` point against the new, slightly tighter `MX0`/`MX1` — a handful of polygon
edge points (woods, lakes near the map's own right edge) now clip about 2mm earlier than before,
same "runs off the edge, stops at the neat line" behaviour the design already relies on elsewhere,
confirmed harmless by rendering. Final margins verified in mm: left 6.900, right 6.800, top
3.500, bottom 17.200 — matching the user's corrected spec plus 0.5mm exactly.

**Printer issue confirmed resolved by the user** via the Canon print preview after pass 3/4's
margins landed. The docx cross-check was then extended into its own small deliverable: the user
asked for a docx of all four maps for printing, then asked to keep it permanently. Saved at
`output/docx/Norse_Trail_Maps_Print.docx` — one page per trail (Leif, Rollo, Aud, Harald, in that
order), each page cropped from the corresponding `Trail_Map_*_Print.pdf` at 300dpi and placed
with the identical page size and margins as the PDFs. Harald's hnefatafl board-setup back page
(page 2 of his PDF) is deliberately not included — it's a separate design not tied to the map
margins. Built with `docx` (npm) via a one-off Node script in this session's scratch directory,
not committed as a reusable build script (the project's other builders are all Python/reportlab;
if this docx needs regenerating after a future map change, redo the crop-and-place from scratch
or ask for a proper Python build script). Still not visually rendered — LibreOffice isn't
installed in this environment; only structural checks (page count, margins, 4 distinct embedded
images) were run.

**Also built, per the user's request:** `Trail_Map_1_Leif_Print.docx` (in this session's scratch
directory, not committed to the repo — it's a diagnostic aid, not a project deliverable) — Leif's
map cropped exactly to the printable area at 300dpi, placed in a Letter-size Word document with
the identical margins as the PDF. Rebuilt three times to track the PDF's margin corrections;
current XML: `pgMar top=198 right=386 bottom=975 left=391` dxa. Not visually rendered before
sending any version — LibreOffice isn't installed in this environment, so only structural checks
(page size, margins, image extent) were possible.

**First attempt at the L1/L2 print docx was wrong, corrected.** Initially read "the L1 and L2
print" as the existing per-card `Postcard_L1/L2_..._Letter_Print.pdf` (each card's own sheet,
same card twice, art then text) and built docx twins of those. The user then pointed at two
reference PDFs from a *different* prior session's scratch directory
(`.../f687f566-af14-4509-a9cb-da929a1e44f2/scratchpad/scratch_art_letter.pdf` and
`scratch_back_4x6.pdf`) to clarify the actual intended layout, which is a different, more
paper-efficient two-pass workflow:
1. **One Letter sheet with BOTH cards' front art together** (L'Anse aux Meadows on top, Battle
   Harbour below, each with its own crop marks) — print this first.
2. **Cut the sheet to separate the two cards**, each still oversized/uncut at this point.
3. **Re-feed each cut piece and print its text side at true trimmed size** — a 2-page document,
   each page exactly 6×4in landscape (one per card, same order as the art sheet), not another
   Letter sheet.
4. **Final trim to exact card size.**

Rebuilt accordingly and replaced the wrong pair: `output/docx/Postcard_L1_L2_Art_Letter_Print.docx`
(1 Letter page, both cards' art, rasterized from the reference `scratch_art_letter.pdf` at 300dpi)
and `output/docx/Postcard_L1_L2_Back_4x6_Print.docx` (2 pages, each a true 6×4in landscape page —
verified in the XML: `pgSz w=8640 h=5760 orient="landscape"` — rasterized from
`scratch_back_4x6.pdf`). The superseded `Postcard_L1_LAnse_Letter_Print.docx` and
`..._L2_Battle_Harbour_Letter_Print.docx` were deleted from `output/docx/` (never committed —
untracked — so no history was lost).

**Not verified:** the two reference PDFs live in another session's scratch directory outside this
repo and outside this session's context, so their own origin/build process is unknown here — I
only rasterized their existing content, I did not check it against the project's postcard data
(voices, Fun Facts, addresses) for correctness. If that reference layout becomes the standard for
all 22 cards, it likely wants a proper build script (probably pairing cards two-at-a-time per
trail) rather than more one-off docx exports.

Same caveats as the other docx files: one-off Node script, not a reusable build script; not
visually rendered before delivery — LibreOffice isn't installed in this environment.

**HTML updated to record all of this**, per the user's explicit ask (`AGENTS.md`'s rule that
durable production decisions belong in the project page, not just chat/HANDOFF): added
`NorseBackpack/Norse_Brainstorm.html`'s `PR-23`, in the "Props and production" section, marked
**Decided**. It records the corrected margin numbers, why the old `Support.xlsx`-sourced side
margin was wrong, the exact rescale mechanics (same scale-and-shift transform used throughout this
session), the Dögurðarnes label-fallback fix, and the new "build a docx twin to isolate PDF-vs-
driver behaviour" practice with pointers to all three files now in `output/docx/`.

**Check not fully run:** tried to open the page in the in-app browser per the usual HTML
validation step, but the `static-preview` server (`python -m http.server`) got stuck at
"starting" with no output and every navigation to it was refused — an infrastructure issue in
this session, not something in the file. Fell back to a text-based tag-balance check instead:
`<div>`/`</div>` count is off by one (1253 open / 1252 close), but that exact same off-by-one
already existed in the last committed `HEAD` version (1096/1095) before this session's edits, so
it predates PR-23 and isn't a regression from this change. Every other paired tag (`section`,
`figure`, `table`, `details`) balances. Worth a real browser check next session regardless, both
to confirm PR-23 renders correctly and to track down the pre-existing div imbalance.

**Not done / out of scope:** the "Aud Map Designer" published artifact
(`https://claude.ai/artifact/26d6YkdDjuSkN2WS5Uc2fL`) still serves an OLD (pre-fix) `aud_base.js`/
`aud_features.json` — if that tool gets reopened to add more hand-drawn features before it's
resynced, new points would be drawn at the wrong scale. Needs its data files re-uploaded, or the
resync deferred until the designer is next used.

**Next action:** open `Norse_Brainstorm.html` in a real browser (once the static-preview
infrastructure issue is sorted) and confirm PR-23 renders and the Open Questions tab still
functions. The printer issue itself is resolved and confirmed by the user; nothing further needed
there unless a physical print still looks off.

## Session close — 2026-09-21 — `Postcard_L1_L2_Back_4x6_Print.docx` clipping fixed

**Task:** the user physically printed the art sheet (fine, alignment good) and the 4x6 back/text
sheet. The back sheet clipped about 5mm off the right edge, into the Fun Fact box's border — this
media (thicker card stock, likely fed via the rear tray) has a bigger non-printable zone than the
Letter paper the trail-map margins were measured against, so the previous zero-margin full-bleed
placement wasn't safe here.

**Fix:** added a real page margin instead of zero — 5.5mm (5mm measured + 0.5mm safety) on the
binding dimension. The card's image is 1.5:1 (6x4in), so an equal-mm margin on all sides would
either distort the image or waste space; instead the image is scaled down uniformly (aspect
preserved exactly) so height gets exactly 5.5mm top/bottom (`312` dxa) and width gets whatever
that same scale factor leaves on left/right (8.25mm, `468` dxa — more than the checked minimum,
which is fine since only the right edge was actually confirmed clipped). Verified in the docx XML:
`pgMar top=312 right=468 bottom=312 left=468`, image extent 5.350in × 3.567in (exact 1.5:1).
Rebuilt, overwrote `output/docx/Postcard_L1_L2_Back_4x6_Print.docx`, resent.

**Not done:** the art-side `Postcard_L1_L2_Art_Letter_Print.docx` was left untouched — no clipping
was reported on that pass, only the back. If it turns out fine on Letter paper via the front tray,
that's consistent with the Letter-specific margins already established for the trail maps.
`Norse_Brainstorm.html` was not updated for this fix — it's a small correction to an already-
recorded deliverable, not a new decision.

**Next action:** print the corrected back sheet and confirm nothing is clipped now. If it still
clips, the true non-printable margin on this media/tray is bigger than 5.5mm and needs a fresh
measurement to tighten the fix.

## Session Close — 2026-09-20 — H5 resolved to Aci Castello everywhere

**Task:** fix the H5 Aci Castello / Syracuse inconsistency.

**It was a three-way disagreement, not a two-way one.** `TravelMap/stops.js` and the route plan said
**Syracuse** at 37.069, 15.288 with a sourced Harald link; `build_final_riddle_visuals.py` said "Aci
Castello" *at Syracuse's coordinates*, which was incoherent and was my own error from the re-dating
pass; and the card carries Aci Castello front art, an ACI CASTELLO postmark and a message about its
Norman castle.

**A bigger problem sat underneath it**, surfaced before deciding: this is the one Harald stop with
**no Harald connection at all**. His Sicilian service is attested at Syracuse and Messina under George
Maniakes in 1038–1040, not here, and the castle on the lava rock is **Norman, built around 1076 — a
decade after Harald died**.

**Decided by the user: keep Aci Castello everywhere, fix only the data.** Chosen over moving the stop
to Syracuse (which would have cost new front art, a new postmark and a rewritten card) and over
re-anchoring the card's text. Coordinates are now 37.5545, 15.1462 in all three files.

**The geometry does not care** — the sites are 55 km apart, which moves H5 about 4 px on a 224 px
panel. Harald's `2` is unchanged. Measured before deciding, so the choice was made on content
grounds rather than on shape.

**The cost is recorded rather than hidden.** The stop's evidence tier in `stops.js` drops from
*supported* to **illustrative**, with a note saying Sicily is on the trail because of the Maniakes
campaign while this particular town is simply where Liv stayed. The Syracuse citation is kept in place
to explain why Sicily is there at all.

**MISTAKE I MADE AND FIXED:** while diagnosing a write failure on the trail-map build I wrote a probe
that opened three PDFs with mode `'wb'` — which truncates. It zeroed `Trail_Map_1_Leif_Print.pdf`,
`Trail_Map_3_Aud_Print.pdf` and `Trail_Map_4_Harald_Print.pdf`. They regenerate from source and all
eight trail maps were rebuilt immediately, verified non-zero and visually checked. No source file was
touched and nothing was lost, but the probe was careless: use `'r+b'` or `os.access` to test
writability, never `'wb'`.

**Files changed:** `TravelMap/stops.js`, `TravelMap/Norse_Aunt_Route_Plan.json`,
`Tools/build_final_riddle_visuals.py`, the regenerated `Tools/final_riddle_visuals.json`, all eight
`Trail_Map_*.pdf`, and `Norse_Brainstorm.html` (the resolution recorded, the old "check before print"
note replaced).

**Checks run:** no `37.069` or "Syracuse · Sicily" coordinate remains in any data file. Visuals
regenerated and the six SVGs re-swapped; the timeline now labels "20 Aci Castello". Solver re-run,
TEST 1 and 2 still pass. Harald's answer map rendered and read — stop 5 is labelled Aci Castello on
Sicily's east coast and the route is unchanged. The map build's own coastline check reports Aci
Castello 0.2 km offshore (0.0 pt at print scale) and Patara 1.8 km (0.4 pt); neither is visible. All
eleven tabs open, console clean.

**Next action:** the full read-through playtest with the real props. Still open: validation TEST 3
(geometric decoy check), whether Liv's surname stands as Ericson, and whether a team notices the
element marks in their new top-right position.

## Session Close — 2026-09-20 — Element marks moved to the top right of every card

**Task:** the user reviewed the printed postcards and rejected the mark placement — beside the
signature interfered with the rebuses. Asked for a consistent top-right position.

**They were right, and the reason is worth keeping.** The signature spot was free space, but it was
free space *in the message half*, among Liv's own margin drawings. On `R3` the round shield read as a
fourth piece of the Bayeux rebus; on `H4` it crowded the branch-rune key. The fix is not a better gap
— it is separating the two by **zone**: her drawings live in the message half, the element marks live
with the card's printed furniture.

**New position, identical on all 22:** the pocket between the divider and the postmark, above the
address box — roughly x 186–253 by y 190–220, mark centred at (232, 205).

**It is free by construction rather than by luck.** I checked every build script: the divider
(x=184), the address box (top y=188) and the postmark circle (centred 278,204 r=23) are at identical
coordinates on all 22 cards, so the pocket exists everywhere regardless of message length. That is
why this placement cannot break the way the old one did.

**Defined once.** `MARK_X, MARK_Y, MARK_SIZE` now live in `postcard_marks.py` and every card calls
`draw_mark(c, "XX")` with no coordinates — moving them all again is a one-line change.

**The proofing risk logged earlier is mostly answered.** The marks and rebuses do share a visual
language, and while the marks sat beside the signature that was a genuine misreading risk. Separated
by zone it largely goes away. **What still wants a playtest** is the opposite question: whether a team
notices the marks at all up there, now that they compete with the stamp and postmark rather than
sitting where the eye already is.

**Files changed:** `postcard_marks.py` (position constants plus the reasoning), all 22
`build_postcard_*_pdf.py` (call sites simplified), all 44 card PDFs and
`Norse_Postcards_Full_Print.pdf` rebuilt, and `Norse_Brainstorm.html` (placement note rewritten, the
proofing warning downgraded to a note).

**Checks run:** `postcard_marks.check()` passes. All 23 build scripts run clean. `R3`, `H4`, `L1` and
`RD` rendered at full size — R3's rebus is now alone in the message half and H4's rune table is
untouched. Contact sheet of the mark area on all 22 confirms identical placement with no collision
against postmark, stamp or address box. Page served over HTTP, all eleven tabs open, board renders,
console clean.

**Next action:** unchanged — a full read-through playtest with the real props, now that the cards,
the four maps, the journal page and the three tickets all exist. Also still open: reconciling `H5`
(Aci Castello vs Syracuse in `TravelMap/stops.js`), validation TEST 3, and whether Liv's surname
stands as Ericson.

## Session Close — 2026-09-20 — The three transition tickets built; every endgame prop now exists

**Task:** build the last props the endgame needs — the three tickets that chain the four legs.

**Built:** `NorseBackpack/Props/Tickets/build_transition_tickets_pdf.py` →
`output/pdf/Transition_Tickets_Print.pdf` (one per page, 5.4 × 2.5 in) and `..._Letter_Print.pdf`
(all three centred on one sheet with trim guides). Machine-set in Helvetica on near-white stock —
these are agency paperwork and should look nothing like the postcards or the journal page.

| Ticket | Closes | Opens | Segments |
|---|---|---|---|
| Leif → Rollo | L3 Qikiqtarjuaq | RD Walcheren | 4, via Iqaluit, Ottawa, Amsterdam |
| Rollo → Aud | R6 Roumare Forest | A1 Dögurðarnes | 4, via Rouen, Paris, Reykjavík |
| Aud → Harald | A3 Esjuberg | H1 Oslo | 2, via Reykjavík |

**Why multi-segment itineraries rather than boarding passes.** None of the endpoints is an airport —
Roumare is a forest, Dögurðarnes and Esjuberg are farmsteads, and there is no direct
Qikiqtarjuaq–Netherlands service. A boarding pass could only name airports, and "which airport serves
which town" is exactly the outside knowledge rule 3 forbids — the same trap that made us reject
naming Ouistreham for the Channel crossing. A booking confirmation lists every waypoint, so the two
place names that carry the clue are printed in full. The first origin and last destination are set
bold so the eye lands on them.

**Load-bearing vs dressing, recorded in the script header and the page:** only the first origin and
last destination of each ticket matter. Carriers, service numbers, booking refs, e-ticket numbers and
intermediate hops are invented for the look and can change freely. The routings are plausible rather
than verified — real services exist on these city pairs, but no timetable was checked and none needs
to be. Place names are printed without diacritics ("Dogurdarnes", "Reykjavik"), which is how airline
systems really do it and reads as authentic.

**One invention that needs a decision: Liv's surname.** The tickets need a passenger name and **none
is recorded anywhere in the project**. She is printed as **ERICSON / LIV**, taking the surname of her
nephew *John Ericson* from the postcard addresses, which also quietly supports the shared-family-crest
premise. It is a single constant at the top of the build script. Nothing else depends on it.

**Also closed:** the "blocking the legs opens work that did not exist before" warning from 19 Sept
listed three gaps — the journal page, the transition tickets, and dating all four museum tickets. All
three are resolved. The third went away on its own: leg order moved to the transition chain, so the
museum tickets need no dates at all.

**Files changed:** the new `Props/Tickets/build_transition_tickets_pdf.py`, its two output PDFs, and
`Norse_Brainstorm.html` (tickets recorded in 2c, the old prop-gap warning replaced).

**Checks run:** all three tickets rendered at full size and read twice — first version, then after
tightening the height and adding the e-ticket column. Letter sheet rendered and confirmed as one page
with the block centred. Page served over HTTP, all eleven tabs open, board and all six SVGs render,
console clean.

**Every prop the endgame model calls for now exists.** Remaining work is verification and reconciling,
not making:
- reconcile `H5` between the visuals (Aci Castello) and `TravelMap/stops.js` (Syracuse, ~60 km away)
- validation TEST 3, the geometric decoy check, still not run
- the rebus/element-mark confusion risk on `R3` wants a real playtest
- decide whether Liv's surname stands

**Next action:** a full read-through playtest of the endgame with the real props — the deck, the four
maps, the journal page and the three tickets — since every piece now exists for the first time.

## Session Close — 2026-09-20 — The "Family iconography" journal page built

**Task:** build the endgame's keystone prop — the page carrying both the decoy filter and four of the
ordering clues.

**Built:** `NorseBackpack/Props/Journal/build_journal_page_pdf.py` → `output/pdf/
Journal_Family_Iconography_Print.pdf` (A5, prints two-up on Letter) and `..._Letter_Print.pdf` (with a
trim guide). Her handwriting throughout on the deck's paper colour — it is her notebook, not a printed
form. Top half: `PR-22`'s two reference drawings as they stand, the crest's blank banner left blank.
Bottom half: "Travel highlights", the four agreed entries grouped by transport.

**The drawings are deliberately large.** The team's actual task is comparing a 23 pt mark on a
postcard against these, so size is usability, not decoration. The first layout left about a third of
the page empty below the entries; art enlarged and sections spread until it filled.

**A fairness bug caught at render and fixed.** The element names are listed under each drawing — they
matter because the card marks are loose doodles while the references are detailed engravings, and a
name bridges that gap. But the first version read **"axe"**, and Rollo's and Harald's decoy mark is a
**double-bladed** axe against the crest's single-bladed one. The drawings show the difference plainly,
but a name list saying "axe" lets a team match the decoy by name and never look — unfair rather than
difficult. Now **"bearded axe"**, and for the same reason **"round shield"** and **"drinking horn"**
rather than "shield" and "horn". The horned helmet has no near-match among the nine.

**The rule line is stated outright**, under the title: "Every place I actually stopped carries one of
these nine." It has to be — without it the drawings are decoration and nothing prompts a comparison.
It says which cards are hers; it does not say which decoys exist, how many, or which element sits
where.

**Two rules recorded in the script header and in the page**, for anyone editing the entries: a journey
entry means the two stops are *consecutive*, not merely in that order, so vet any new or texture entry
against `Tools/final_riddle_clues.py` first; and entries are grouped by transport and deliberately not
in date order — as printed the by-train group runs Harald's leg first and Rollo's second, reversing
the real chronology.

**Files changed:** the new `Props/Journal/build_journal_page_pdf.py`, its two output PDFs, and
`Norse_Brainstorm.html` (the build recorded in section 2c's journal block, and the open-items panel
moved from "partly drafted" to "built").

**Checks run:** page rendered at full size and read three times — first layout, after the rebalance,
and after the name fix. Letter version rendered and confirmed centred with its trim guide. Page served
over HTTP, all eleven tabs open, board and all six SVGs still render, console clean.

**Next action: the three transition tickets** — Leif→Rollo (Qikiqtarjuaq → Walcheren), Rollo→Aud
(Roumare → Dögurðarnes), Aud→Harald (Esjuberg → Oslo). These are the last props the endgame needs.
Note Leif's wants a multi-segment e-ticket itinerary rather than a single boarding pass, since there
is no direct Qikiqtarjuaq–Netherlands service. Still also open: reconciling `H5` between the visuals
(Aci Castello) and `TravelMap/stops.js` (Syracuse, ~60 km away).

## Session Close — 2026-09-20 — Card text rebuilt and element marks applied to all 22

**Task:** apply the six outstanding text edits, then put Codex's hand-drawn element marks on the cards.

**Six text edits applied, every card rebuilt, every back read at full size.** Each script carries a
comment naming the rule it answers.
- `R1` Châlus — deleted "but this is where I began" (rule 1). The Richard-dying-there line stays: it
  is about the family story, not her itinerary.
- `R2` Rouen — deleted "The tapestry towns are still ahead of me" (rule 3; added 17 Sept, rejected).
- `R4` Winchester — "Winchester next" → "Winchester today" (rule 2), matching `L2`'s "Markland today"
  and `H4`'s "Today: Hedeby".
- `R6` Roumare — deleted "The last of Rollo's places on my list" and "to finish" (rule 1); kept the
  Rouen proximity, which is map-verifiable flavour.
- `RD` Walcheren — deleted "Made a detour … before really starting Rollo's own trail" (rule 4).
- `H3` Kyiv — "Kyiv next…" → "Kyiv, and it might be the most beautiful city on this whole trip…"
  (rule 2). Nothing replaces it mechanically; H4's Mediterranean line made the planned Dnieper
  mention unnecessary.

**Element marks assigned and printed on all 22 cards — the last open column of the retired
worksheet.** New shared module `NorseBackpack/Postcards/postcard_marks.py` holds the assignment as a
single dict plus a `draw_mark()` helper, so reshuffling is one edit rather than 22. It also has a
`check()` that asserts the filter's rule still holds (each three-stop leg uses the symbol set once
each, each six-stop leg the crest set, every decoy a mark from neither) and that every image exists.
Any bijection works identically as a puzzle, so the pairings are flavour only — recorded with reasons
in section 3b.

**Placement: beside the signature, not below it.** Below was the obvious choice and does not work —
`H4`'s branch-rune key table fills nearly the whole width of that area, and `R3`/`R4`/`R5` already
carry their Bayeux rebuses there. All 22 backs rendered at full size to confirm; the tightest is `H4`,
where the mark clears the table box by a few points.

**Proofing risk recorded, not solved:** the marks and the rebuses share a visual language — small
hand-drawn icons, same palette — and on `R3` the round shield sits directly above the cross/bow/bolt
rebus. A team could read the shield as a fourth rebus element. The defence is positional consistency
(a mark is always beside the signature; rebuses are scattered below), which only works if a team
compares cards — which the filter asks of them anyway. Worth testing on a real player; a light ring or
fixed tint would separate them without moving anything.

**Files changed:** all 22 `build_postcard_*_pdf.py` (marks, and six of them text too), the new
`postcard_marks.py`, all 44 card PDFs plus `Norse_Postcards_Full_Print.pdf` rebuilt, and
`Norse_Brainstorm.html` — new section 3b with the assignment table, the summary table's element-mark
column closed, and the "still to apply" notes in 2e and 2g replaced with what was done.

**Checks run:** `postcard_marks.check()` passes (22 cards, valid assignment, all art present). All 23
build scripts run clean. Contact sheet of all 22 backs rendered and inspected — every mark present, no
collisions. Close-ups of the two tightest layouts (`H4`, `R3`) inspected separately. Page served over
HTTP, section labels in sequence, all eleven tabs open, board still renders, console clean.

**Next action: the props that do not exist.** The three transition tickets and the "Family
iconography" journal page — the page's top half needs `PR-22`'s two reference drawings, and its bottom
half now has four agreed entries waiting (three for Rollo in 2e, one for Harald in 2g). Also still
open: reconciling `H5` between the visuals (Aci Castello) and `TravelMap/stops.js` (Syracuse, ~60 km
away).

## Session Close — 2026-09-20 — Last two stale blocks retired; Final riddle tab is now internally consistent

**Task:** retire the two blocks that still predated the evidence model, rather than patch them.

**Retired, with a note saying what they claimed and why it is wrong** (AGENTS.md: say so where the old
text was, do not delete silently). Both are replaced by section 3, now titled "Retired":

- **"Clue types and their jobs"** (four panels) said museum tickets were calendar anchors dated
  2 Feb / 17 Mar / 13 Apr / 28 Apr, that postcard statements "carry the whole deduction", and that the
  bundle held two or three cross-trail resolvers. All three are now wrong: leg order moved to the
  three transition tickets, the museum tickets carry no ordering at all and one or two will be
  deliberately undated, and postcard statements are down to two natural cross-references.
- **The per-trail constraint worksheet** listed decoy positions from the interleaved year ("pos. 11,
  June", "pos. 20, Nov") that no longer exist, ticket dates that have all changed, and an order column
  built on `"Winchester next"` and `"Kyiv next"` — the two clues this model removes outright.

**One column of the worksheet was still live and is carried forward.** The element-mark assignment has
not moved: it remains open and still gates the whole endgame, because without the marks a team cannot
tell a real stop from a decoy. It now sits in a new summary table, "The four legs at a glance", which
keeps only the columns that are still true — real stops, decoy and its block position, element mark,
journal entries, and what fixes each leg's order with a link to its section.

**Files changed:** `NorseBackpack/Norse_Brainstorm.html` only.

**Checks run:** page served over HTTP; section labels read 1, 2, 2b–2i, 3 Retired, Summary, 4, 5, 6;
the retired panels are gone from the rendered text and the only surviving "pos. 11, June" is the
retirement note quoting it deliberately; six SVGs and the four-block board still render; all eleven
tabs open; console clean.

**The Final riddle tab now has no stale blocks.** Everything in it either describes the current model
or is explicitly marked as superseded history.

**Next action: production.** Nothing in the endgame is open as design. What does not exist yet:
- the three transition tickets and the "Family iconography" journal page (its top half depends on
  `PR-22`'s two reference drawings)
- five sentence deletions on Rollo's built cards and the `H3` Kyiv rewrite, none applied
- the element-mark assignment for all 22 cards, and the reprint pass that goes with it
- reconciling `H5`: the visuals now say Aci Castello, `TravelMap/stops.js` and the printed Harald
  sheet still plot Syracuse ~60 km away

## Session Close — 2026-09-20 — 2i visuals regenerated; Aud and Harald dated

**Task:** regenerate the generated visuals against the new dates, which first required setting Aud's
and Harald's, still open inside the May–July window.

**Dates set (first pass, and freely movable — no clue depends on them):**
- Aud, May 2025: A1 Dögurðarnes 9 May, AD Bjarnarhöfn 14 May, A2 Hvammur 20 May, A3 Esjuberg 27 May
- Harald, Jun–Jul 2025: H1 Oslo 6 Jun (7 nights, as the card says), H2 Staraya Ladoga 17 Jun,
  H3 Kyiv 23 Jun, H4 Hedeby 1 Jul, H5 Aci Castello 8 Jul, HD Constantinople 15 Jul, H6 Patara 21 Jul

Whole journey: **79 nights away, 24 Aug 2024 to 26 Jul 2025.**

**`Tools/build_final_riddle_visuals.py` redated and fixed.** `Y = 2026` became `Y1, Y2 = 2024, 2025`;
both month grids now walk real month boundaries across two years instead of `range(2, 13)`, and mark
January in rust as the year boundary. **Its output path was a dead reference to a previous session's
temp directory** — now written next to the script as `final_riddle_visuals.json`, so the run is
reproducible.

**Label staggering widened.** Blocked legs bunch the stops into four tight clusters, which the old
three stagger rows could not hold — labels overlapped badly on first render. Now five rows, and a
dense cluster always takes the row whose last label sits furthest left rather than the first that
happens to clear. Verified by eye, not by arithmetic.

**Two captions were saying the opposite of the truth** and are corrected. Panel B's read "This is the
interleaving the endgame asks players to unpick: no trail runs as a clean block" — under this model
every lane *is* a clean block. The figure now reads as the clearest single illustration of the
blocked-leg model in the page.

**Two decoy complaints from 17 Sept turn out to be resolved by the re-dating, not by design work.**
The old note recorded that two decoys barely perturbed their shape, so a team ignoring the crest
filter still traced usable digits. **Brattahlíð** moved from last in Leif's run to third of four, so
an unfiltered trace now runs east to Greenland and back west to Baffin — a V, not a 1. **Walcheren**
now opens Rollo's block instead of sitting late in it, so an unfiltered trace starts far to the
north-east and the loop never closes. **Constantinople is unchanged and remains the weak one** — it
still sits almost on the line between Sicily and Patara, so Harald's is the only decoy a team can
ignore and still get a plausible figure.

**Also noticed:** `H5` is recorded as *Aci Castello* in the visuals data, matching the card's front
art and postmark, but `TravelMap/stops.js` and the printed Harald sheet previously plotted Syracuse,
~60 km away. The drawn shape is unaffected at this scale; flagged in the page to reconcile before
print.

**Files changed:** `Tools/build_final_riddle_visuals.py` (dates, two-year month grids, staggering,
output path), the new `Tools/final_riddle_visuals.json`, and `Norse_Brainstorm.html` — six SVGs
swapped, the 22-row itinerary table regenerated with a credibility-check column, section 2's heading
and intro rewritten, both timeline captions corrected, the shape-analysis note rewritten, and the
staleness warning narrowed again.

**Checks run:** solver re-run (TEST 1 and 2 still pass). Both timelines and all four leg maps
inspected visually in the browser at full size. Decoy positions confirmed in the rendered captions —
Brattahlíð 3 of 4, Walcheren 1 of 7, Bjarnarhöfn 2 of 4, Constantinople 6 of 7. All eleven tabs open,
board still renders with four blocks and fourteen clues, console clean.

**Still stale, and now down to two items:** the constraint worksheet further down the tab, and
section 3's "clue types" panels. Both predate the evidence model in 2c and describe ticket dates and
postcard statements doing jobs they no longer do — they want rewriting or retiring rather than
patching.

**Next action:** retire or rewrite those two blocks, then move to props — the three transition
tickets and the "Family iconography" journal page, neither of which exists.

## Session Close — 2026-09-20 — Solver and solving board rebuilt for the blocked-leg model

**Task:** the solver and the in-page solving board both still encoded the superseded 17 Sept
interleaved model, including the two "next" clues the new spec removes. Both rebuilt against
sections 2c–2g.

**`Tools/final_riddle_clues.py` rewritten, and it got simpler.** The old model wove four trails
across one year, so it placed 22 cards into 22 global positions — a space large enough that the run
capped at 400,000 calendars and **could report a false pass, which it did at least once** (on a
variant dropping two of Leif's position clues). Blocked legs are independent, so each is now
enumerated exhaustively over its own block, at most 7! = 5,040 arrangements. No cap, so no false
pass. The file is self-contained and no longer imports the old solver.

**Current run:**
```
leg       block      cards   +tickets   +journal
leif          4          2          1          1
rollo         7        360         60          1
aud           4          6          1          1
harald        7          6          2          1
```
TEST 1 pass (every leg unique). TEST 2 pass — without the journal, Rollo admits 60 and Harald 2.
TEST 3 still not run (geometric). TEST 4 no longer searched: the three tickets chain leg order
directly. **All fourteen clues are load-bearing** — the script drops each in turn and none is
redundant. Note the two four-card legs close on the tickets alone; the journal is what closes the two
seven-card legs.

**`final_riddle_solver.py` kept but marked superseded** with a header explaining what it modelled and
why the cap mattered. Nothing imports it.

**The solving board rebuilt** (section 6). It was a single row of 22 positions; it is now **four
independent leg blocks** of 4, 7, 4 and 7, each with its own verdict chip, since a leg is judged on
its own. Clue list is the current fourteen, grouped by where each lives (cards / transition tickets /
journal highlights). Shaded end slots mark the two a ticket or permitted card statement pins. The
bundle toggle now withholds ten of the fourteen clues rather than three. `localStorage` key bumped to
`norse-riddle-board-v2` so an old saved board cannot load into the new shape.

**Checks run:** solver executed and read. Board driven through the DOM: empty state correct (4 blocks,
22 slots, 8 shaded ends, 14 clues, 10 withheld); filling the answer turns all fourteen green, all four
leg chips green, and reads `1 9 7 2`. Three violations induced and each caught correctly and in
isolation — swapping H2/H3 breaks only the Staraya Ladoga–Kyiv entry, moving H5 before Hedeby breaks
only H4's Mediterranean clue, moving R4 breaks only the ferry entry. All eleven tabs open, console
clean.

**Page updated to match:** the top banner now says all four legs are settled; section 5 Validation
carries the new run as a table; the staleness warning narrowed to what is still actually stale.

**Still stale, and now explicitly scoped:** the itinerary table in 2i and the "Where she was, and
when" timeline, both generated by `Tools/build_final_riddle_visuals.py` from the old interleaved year;
the constraint worksheet; and section 3's "clue types" panels, which still describe ticket dates and
postcard statements doing jobs they no longer do. The four leg shapes in 2i are unaffected — they come
from stop coordinates, which have not changed.

**Next action:** either regenerate the 2i visuals from the new leg dates (Leif 24 Aug – 16 Sept,
Rollo 28 Sept – 6 Nov, Aud and Harald in May–July of year two, exact dates still open), or start
producing props — the three transition tickets and the "Family iconography" journal page, neither of
which exists yet.

## Session Close — 2026-09-20 — Harald down to one journal entry; endgame design closed

**Task:** continuing the same session. The user spotted a simplification and accepted the remaining
open problem, which closes the endgame design.

**Corrected — only the *real* cards need ordering.** I had been enumerating each leg's full block
including its decoy. **A decoy's position inside its block is never needed by anything**: it is
filtered out before a line is drawn, no ticket lands on it, and the decoy-never-first invariant is
retired. Re-enumerating Harald over its six real cards drops it from two journal entries to **one** —
*Sicily – Constantinople* was only ever placing HD inside the block. The ticket, H6's line and H4's
Mediterranean line leave exactly two orders, differing only in whether Staraya Ladoga or Kyiv came
first.

**The same simplification does not help Rollo, and the contrast is worth keeping.** Rollo's decoy is
genuinely load-bearing, because the Leif→Rollo ticket lands on `RD` Walcheren rather than on a real
card — so *Walcheren–Châlus* is what converts "the block starts at Walcheren" into "Châlus is the
first real stop." Re-enumerated over Rollo's six real cards: all three entries survive, and dropping
any one gives three orders.

**Harald's entry, drafted and written in:**
> *By train — Staraya Ladoga – Kyiv.* "Two days on a train, most of it running alongside the rivers
> they would have rowed. Felt like cheating. Slept through the best of it, naturally."

Deliberately carries **no direction word**. An early draft had her following the water "south", which
would have muddied H4's "from here I'm turning south" — a team could reasonably wonder whether the
turn had already happened.

**Decided — Harald's `2` stands as drawn.** Flagged as broken since 17 Sept: the H3 → H4 leg doubles
back, so the figure reads closer to a zigzag with a spike than a clean 2. **Accepted rather than
fixed.** By that point a team knows it is looking for a digit, and a rough 2 is still the only digit
the figure resembles — recognition is far easier than reading a shape cold. Fixing it would have meant
moving or replacing a stop, invalidating whichever clues named it. This was the last open design
problem in the endgame.

**The journal page is four entries total** — Rollo three, Harald one, Leif and Aud none. Noted in the
page that this is lopsided for a travel document, and that any texture entries added to even it out
must be vetted against the enumerator first, since naming two stops constrains them whether or not
that was intended.

**Files changed:** `NorseBackpack/Norse_Brainstorm.html` only — Harald's section retitled and reduced
to one entry, the correction recorded, the entry drafted in, the broken-`2` warning replaced with the
decision, the journal-page tally added, and the open-items grid's Harald panel replaced with "All four
legs closed".

**Checks run:** both six-stop legs re-enumerated over their real cards only. Page served over HTTP,
section labels in sequence (1, 2, 2b–2i, 3–6), all new blocks render, no stale "shape still broken"
text remains, console clean.

**The endgame design is now closed. What remains is production, not design:**
- `H3` Kyiv still has to lose "Kyiv next" (rule 2). Nothing need replace it mechanically.
- Five sentences still to come off Rollo's built cards (listed in 2e); none applied yet.
- None of the props exist: three transition tickets, the "Family iconography" journal page, and the
  four museum tickets still have no printed dates.
- `Tools/final_riddle_clues.py`, the constraint worksheet, the Validation run and the solving board in
  section 6 all still encode the superseded 17 Sept model and must be rebuilt against sections 2c–2g.

**Next action:** rebuild `final_riddle_clues.py` against the new model, then the solving board's data
block, so the two tools stop contradicting the spec. The clue set is now small enough that this is
mostly deletion.

## Session Close — 2026-09-20 — Harald's leg settled; all four legs now done

**Task:** continuing the same session. Worked leg 4 (Harald), and reverted the bundle design after the
user corrected it.

**Reverted — back to three transition tickets.** Last turn I replaced them with four return
itineraries, arguing a single ticket could not span the winter between Rollo and Aud. The user
resolved it differently: **Liv simply winters abroad rather than flying home**, so the gap is a long
stay, not a break in the chain. Three tickets — Leif→Rollo (L3→RD), Rollo→Aud (R6→A1), Aud→Harald
(A3→H1).

**The chain's two loose ends are covered by cards, and this is now a stated principle.** No ticket
precedes Leif and none follows Harald, so `L1` "the first stop on my journey" and `H6` "Patara is the
last stop of my travels for now" are **the only two cards permitted to state their own position** —
and they are exactly the two ends of the whole journey. A principled exception to rule 1 rather than a
leak. H6's line is therefore *kept*, reversing my earlier plan to delete it.

**Leg 4 Harald — clue set settled. Two journal entries, not three.**
`H1 → H2 → H3 → H4 → H5 → HD → H6`, closed by the Aud→Harald ticket, H6's own line, H4's new
Mediterranean line, and two journal entries: *Staraya Ladoga – Kyiv* and *Sicily – Constantinople*.
*Hedeby – Sicily* was dropped as redundant. Enumerated over all 5,040 arrangements.

**The H4 rewrite is the interesting part.** The old clue, "saltwater again, after all that river
country", was dropped — "river country" only reliably points at Staraya Ladoga, whose card mentions a
river bend, so placing Kyiv before Hedeby needed outside knowledge of the Dnieper. **A plain "heading
south" would not have worked either**: Hedeby is 54.5°N and Kyiv 50.5°N, so Kyiv *is* south and a
latitude reading cannot exclude it. Naming the sea does — Kyiv is the one remaining stop not on a
coast. The difference is **60 possible orders versus 4**, plus a journal entry saved. Final wording,
the user's: "Today: Hedeby — barely a Hedeby left to stand in, just a green ring of earthworks where
the ramparts ran. From here I'm turning south: nothing but Mediterranean weather for the rest of this
trip."

**Two card edits applied, PDFs rebuilt, both backs rendered and checked:**
- `H4` Hedeby — opener replaced. **Its branch-rune key table was the real risk** (the box clamps at
  y=30 and a previous edit to this card pushed its caption out of frame). The new message runs one
  line longer and the table still clears with its caption intact — confirmed by rendering, not by
  arithmetic.
- `H1` Oslo — deleted "and the obvious place to begin with him" (rule 1). Now reads "It's Harald's
  city — so much Viking history."

**Still to do on Harald: `H3` Kyiv must lose "Kyiv next"** (rule 2). Nothing needs to replace it
mechanically — an earlier plan had H3 gaining a Dnieper mention, which H4's Mediterranean line makes
unnecessary. Any new opener just has to carry no ordering content. Recorded as a warning block in 2g.

**Minor:** `build_postcard_H1_pdf.py` uses straight apostrophes where the rest of the deck uses curly
ones. Noted in the page, not fixed.

**Files changed:** `build_postcard_{H1,H4}_pdf.py` (each with a comment recording why), their four
rebuilt PDFs, and `Norse_Brainstorm.html` — bundle section reverted to three tickets, new section 2g
for Harald, sections renumbered (2h "what this model owes", 2i "At a glance"), the open-items grid's
Harald panel replaced with the broken-`2` problem, and every stale itinerary reference reworded except
the two kept as history.

**Checks run:** both rebuilt card backs rendered at full size and read — H4's rune table verified
intact. Page served over HTTP, section labels in sequence (1, 2, 2b–2i, 3–6), all new blocks render,
console clean.

**Next action — the last open problem in the endgame: Harald's `2` does not draw.** The H3 → H4 leg
doubles back up and to the left, giving a zigzag with a spike. The clue work cannot touch this; it is
solved by moving or replacing a stop, which then invalidates whichever clues named it. Do it before
any journal entry is drafted in final form, and before the solver and solving board are rebuilt.

## Session Close — 2026-09-20 — Two-year split; return itineraries; Aud's leg settled

**Task:** continuing the same session. The user split the journey across two calendar years, which
forced a change to the bundle and then unblocked Aud's leg.

**Decided — the journey spans two years.** Leif (24 Aug – 16 Sept) and Rollo (28 Sept – 6 Nov) in
year one; Aud and Harald in **May–July of year two**. A continuous run would have pushed legs 3 and 4
into an Icelandic and Baltic winter. No new justification needed: card L1 already opens "I've spent
the last two years travelling and exploring our family history." It also puts H5's gelato in real
Sicilian summer.

**Superseded — the three transition tickets are now four return itineraries.** A transition ticket
was a single document from the end of one leg to the start of the next, which only works while legs
are back-to-back. They no longer are; no booking spans a six-month gap at home. One return itinerary
per leg — outbound and inbound with dates, which is how people actually book — survives the gap,
pins **both** ends of its leg instead of one, and still gives leg order. All four sit in the bundle,
so rule 5 holds.

**Leg 3 Aud — settled, and it needs no journal entries.** Structurally identical to Leif: the
outbound itinerary pins A1, the inbound pins A3, AD goes to the crest filter, and A2 is the only real
card left for the middle. **One structural condition:** AD must sit second or third in the block,
never at either end — otherwise the itinerary pins a card the filter later removes, which is exactly
Rollo's situation and why Rollo needs a Walcheren–Châlus entry. This is not the retired
decoy-never-first invariant returning; it is a per-leg consequence of where that leg's itinerary
lands.

**Four text changes applied to Aud's built cards, PDFs rebuilt, backs visually checked:**
- `A1` Dögurðarnes — deleted the whole opening paragraph ("First of Aud's places for me. I saved
  Aud's country until after France — save the best for last, right?"). The first sentence breaks
  rule 1. **The second was the serious one:** it revealed Rollo-before-Aud during play, when leg
  order is supposed to live entirely in the bundle (rule 5).
- `A3` Esjuberg — deleted "Last of Aud's places for me." (rule 1).
- `AD` Bjarnarhöfn — "Wintered like Aud did, at her brother's harbor" → "At her brother's harbor —
  the one Aud wintered in." A credibility fix, not a rules one: Aud's leg now runs May–July so Liv
  cannot have wintered there. Agrees with the card's own typed Fun Fact.

**Worth carrying into Harald's audit:** the A1 and A3 clauses were listed in the 17 Sept clue set as
"new card text" still to write. They were in fact already written and shipped. `H1` and `H6` are
listed the same way, so assume they are printed until checked.

**Left open deliberately:** A1 now opens straight into the etymology, having lost its warm opener. It
reads acceptably — R3 Bayeux opens on its subject too — but any replacement must carry no ordering
content. Not invented.

**Files changed:** `build_postcard_{A1,A3,AD}_pdf.py` (each with a comment recording why), their six
rebuilt PDFs, and `Norse_Brainstorm.html` — the return-itinerary section replacing the transition
chain, new section 2f for Aud, sections renumbered (2g "what this model owes", 2h "At a glance"), the
open-items panels updated, and every stale "transition ticket" reference reworded except the three
that are deliberately historical.

**Checks run:** all three rebuilt card backs rendered and read — the deletions are clean and the
layouts unchanged. Page served over HTTP, section labels in sequence (1, 2, 2b–2h, 3–6), no dangling
cross-references after renumbering, all new blocks render, console clean.

**Next action:** Harald's leg — the last and hardest. Six real stops plus a decoy, and its `2` is
already recorded as broken. Audit the seven cards' text first (`H1`/`H6` for printed position
statements, `H3` for "Kyiv next"), then work out where its itinerary lands and what the journal owes
it.

## Session Close — 2026-09-20 — Rollo's journal entries drafted and dated

**Task:** continuing the same session. Drafted the three "Travel highlights" entries for Rollo's leg,
iterated the wording with the user, and set the leg's dates.

**The three entries, agreed and written into section 2e:**
- *By train — Walcheren – Châlus.* "The long one. Three changes, one missed connection, and a man in
  the second carriage who shared his sandwiches after I gave up waiting for the buffet car."
- *By train — Train from Rouen.* "Heading west, a short hop, for a museum I'd been looking forward to
  for months."
- *By sea — English Channel ferry.* "Landed in Winchester after a rocky night, but excited to finally
  see the battlefield itself, after all those hours in front of the tapestry."

**The user pushed the last two toward vagueness, and the two cases behave differently.** Withholding
Bayeux from the Rouen entry is free: *west* + *a short hop* off the map, plus *museum* excluding
Roumare Forest, still resolve it, so the constraint is unchanged and the work goes up. Withholding
the ferry's origin was not free — a fully vague ferry entry leaves 2 orders, the rival being
Châlus → Winchester → Rouen → Bayeux. Closing that by reasoning about Châlus's distance from the sea
would have made a soft map inference load-bearing.

**The user's own fix is better than mine.** Pointing the ferry entry *forward* ("excited to finally
see the battlefield itself, after all those hours in front of the tapestry") carries two facts in one
clause — Bayeux behind, Battle ahead — and closes the leg on its own. It also drops the adjacency
assumption my draft needed, and the tapestry→Battle link is card-internal (R3 names the 1066 story,
R5 names William and Harold).

**Proofing note recorded:** if that entry is misread as "excited to see *the tapestry*", Bayeux moves
after Winchester and the leg yields 3 wrong orders. The wording guards against this twice over and
must not be shortened at layout stage.

**Rollo dated 28 Sept – 6 Nov** (RD Walcheren 28 Sept, R1 Châlus 4 Oct, R2 Rouen 11 Oct, R3 Bayeux
18 Oct, R4 Winchester 24 Oct, R5 Battle 29 Oct, R6 Roumare 3 Nov). Dates are now a *credibility* test
only, never a clue — each row carries its check. Winchester's "freezing here" is defensible in late
October off an overnight crossing; Roumare's beech and oak with boar suits early November.

**Correction to the earlier entry:** the deletion list for Rollo's built cards is **five** sentences,
not four. R2 Rouen's "The tapestry towns are still ahead of me" was added on 17 Sept and is printed,
so rejecting it under rule 3 means it has to come off too. None of the five is applied yet — all five
cards are built and shipped, so this is a text-and-reprint pass.

**Also noted:** the Rouen museum ticket may not need a date at all. Its intra-leg job went to the
Rouen journal entry and its leg-order job went to the transition chain, so it is the leading
candidate to be one of the deliberately undated tickets.

**Files changed:** `NorseBackpack/Norse_Brainstorm.html` only — the three entries with what each pins,
Rollo's date table, the proofing warning, the corrected five-sentence deletion list, and the open-items
panels updated (journal now "partly drafted", dates now "legs 1–2 set").

**Checks run:** all three entries verified by enumeration over the 5,040 arrangements — the agreed set
gives exactly one order, each entry is load-bearing, and the misreading case was confirmed to produce
3 wrong orders. Page served over HTTP, section labels in sequence, all new blocks render, console
clean.

**Next action:** Aud's leg. Note it now opens after 6 Nov, so legs 3 and 4 fall in winter — check that
against Aud's and Harald's card content early, since several of those cards were written for the old
spring/summer dating.

## Session Close — 2026-09-20 — Endgame evidence model rewritten; Leif and Rollo settled

**Task:** continuing 19 Sept. The user rejected `"XXX next"` as a clue — it points at a card other
than the one in hand, so collecting or laying out the deck differently destroys the referent — and
noted the phrasing was simply their voice, never a mechanism. That opened a full rework of how the
endgame carries evidence. Written up as **section 2c of the Final riddle tab**, superseding the
17 Sept clue set in 2b.

**The five rules.** (1) No card states its own position. (2) No deictic clues. (3) Every clue names
its anchor — a place, another prop, or something the map shows; no outside knowledge, including
weather, museum seasons, or which port serves which town. (4) Decoys read as genuine stops — this
reverses the 19 Sept decision. (5) Ambiguity holds until the final bundle.

**Two-layer structure.** During play: postcards with only natural cross-references, museum tickets
(one or two deliberately undated), and the maps. Final bundle: the journal page and three transition
tickets. Leg order lives entirely in the bundle.

**Corrected a mistake from 19 Sept.** I had the four museum tickets carrying leg order. Players
collect those during play, so leg order would have been readable long before the endgame — breaking
rule 5. The three transition tickets chain instead (L3→RD, R6→A1, A?→H?), which puts leg order in
the bundle and frees the museum tickets for intra-leg work.

**The journal page, "Family iconography"** — the keystone. Top half: the crest and symbol drawings,
unannotated (the filter). Bottom half: "Travel highlights", journey entries with a memorable detail
and **no reference to the elements**. An earlier draft tied elements to journeys ("thought of the
horn on the train from Rouen to Bayeux") — the user caught that it implies the horn belongs to one
of those stops, corrupting the filter. Decoupled, it also means the highlights are unusable until
the filter is applied, since some entries name decoy stops. Entries group by transport, not date.

**Modelling point worth keeping:** a journey entry means *consecutive*, not merely *earlier*. Read
weakly, Rollo appeared to need four entries with a Walcheren entry wasted; read correctly, three
entries close the leg and Walcheren is one of them.

**Leg 1 Leif — settled.** L1 states it opens (the one permitted exception to rule 1, since it
launches the game); the L3→RD ticket closes the leg; L2 is second by elimination; LD goes to the
filter. Needs no journal entries. Both self-numbering lines are already deleted and rebuilt.

**Leg 2 Rollo — settled.** RD Walcheren opens the block (L3→RD ticket), R6 closes it (R6→A1 ticket),
Battle's existing tapestry line gives Bayeux-before-Battle, and three journal entries —
Walcheren–Châlus, Rouen–Bayeux, Bayeux–Winchester — close it to one order. Verified by enumerating
all 5,040 arrangements; all three entries are load-bearing. The England-pair inference turns out to
be unnecessary, so nothing rests on it.

**Four deletions pending on Rollo's built cards** (no new prose invented, none applied yet): R1 drop
"but this is where I began" (keep the Richard-dying-there line, which survives rule 1); R6 drop "The
last of Rollo's places on my list"; R4 drop "Winchester next"; RD drop "before really starting
Rollo's own trail". R5 Battle unchanged — it is the model.

**Files changed:** `NorseBackpack/Norse_Brainstorm.html` only — new sections 2c–2f, 2b banner-marked
superseded, "At a glance" renumbered to 2g, and four 19 Sept blocks patched so the page no longer
contradicts itself (the museum-ticket claim, the Leif ticket note, the decoy-never-first invariant,
and LD's position note). Codex's stamp work from the same day is untouched.

**Checks run:** page served over HTTP, Final riddle tab inspected, section labels confirmed in
sequence (1, 2, 2b–2g, 3–6), no dangling cross-references to the pre-renumber labels, all new blocks
present and rendering, console clean, solving board still renders. Rollo's clue set enumerated in
Python — the three-entry set gives exactly one order and each entry is individually load-bearing.

**Not verified visually:** the Browser pane returned blank screenshots throughout (it is hidden), so
layout was confirmed by rendered text and DOM structure rather than by eye.

**STALE and flagged in the page:** the 2g itinerary table, the timeline chart,
`Tools/final_riddle_clues.py`, the constraint worksheet, the Validation run, and the solving board's
clue list — all still describe the 17 Sept interleaved model, including the two "next" clues this
model removes. Rebuild them once all four legs are settled, not before.

**Next action:** work Aud's leg (leg 3) under the new model, the same way Rollo was done — list what
its four cards already say naturally, see what the A1 and A? transition tickets pin for free, then
find the minimum set of journal entries that closes it. Do not write the planned "first/last of
Aud's places" clauses for A1 and A3; they break rule 1 and the tickets already do that job.

## Session Close — 2026-09-20 — Aud/Harald stamps replaced; shield mark differentiated

**Task:** recreate the three art gaps identified in the Norse audit: Aud's obsolete pillar stamp,
Harald's obsolete labrys stamp, and the confusable round-shield/sun-wheel postcard mark.

**Done:** generated a purple engraved Viking-Age comb stamp for Aud and a green engraved
single-bladed Dane axe stamp for Harald. Both preserve the existing 1145 × 1374 transparent,
perforated cream-paper stamp format. All four Aud and all seven Harald postcard builders now use
the replacements; their individual and letter-sheet PDFs were rebuilt. The old pillar and labrys
files remain as superseded history.

The round shield was redesigned instead of the sun-wheel: no spokes or quartering, just a ringed
disc, large domed boss, and one curved two-colour seam. The final production file is 300 × 300 with
transparent corners; the 1254 × 1254 ImageGen source is retained under `PostcardMarks/Sources/`.
The exact three prompts are recorded in `Norse_Brainstorm.html`.

**Files changed:** new `Postcards/Stamps/Stamp_Aud_Comb_v1.png`,
`Stamp_Harald_Dane_Axe_v1.png`, `Art/FinalPuzzle/PostcardMarks/Crest_Round_Shield_HandDrawn_v2.png`
and its source; eleven postcard builder scripts; 22 rebuilt PDFs in `output/pdf/`;
`Norse_Brainstorm.html`; this handoff.

**Checks:** visually inspected all three generated assets. Rendered and inspected all eleven unique
postcard backs plus all 22 pages of the eleven letter-sheet PDFs; both stamps remain clear at card
size, sit correctly under every postmark, and no card-specific clipping appeared. All eleven
builders completed. Served the design page over local HTTP: all four stamp gallery images and
shield v2 load at their expected dimensions; console clean. `git diff --check` passed. Poppler
emitted missing-display-font warnings for Symbol/ArialUnicode while rendering, but the affected
backs showed no missing glyphs or layout damage.

**Next action:** assign the nine real marks and two shared decoy marks to the 22 postcards, then
place and print-proof one representative mark at roughly 0.4–0.5 inches wide.

Previous update: 2026-09-19 by Claude Code

## Session Close — 2026-09-19 — Final puzzle restructured: legs blocked in time; Leif's leg settled

**Task:** the user rejected the `"XXX next"` clue pattern as too fragile — it points at a card that
isn't the one you're holding, so collecting or laying out the deck differently destroys the
referent. They also noted the phrasing was simply how they write, never intended as a mechanism, so
the solver had been promoting incidental voice into load-bearing evidence. They then proposed a new
model and asked to work it leg by leg.

**Decided, 19 Sept 2026 — each leg runs contiguously in time.** Liv finishes Leif's leg, then
Rollo's, then Aud's, then Harald's; no interleaving. Three consequences:

1. **The four museum tickets carry the leg order outright.** Legs no longer overlap, so sorting the
   four dated tickets *is* the digit order. This closes a real delivery gap found earlier in the
   session: `PZ-08` decided the digits read in first-appearance order, but nothing in the game ever
   told a team that — four digits and four maps arrived with no stated reason to order them.
2. **The final bundle becomes transition tickets** — one travel document from the end of each leg to
   the start of the next. Each proves two facts at once (that card closes its leg, that card opens
   the next). Three cover all four legs. Supersedes the old assorted boarding passes and receipts.
3. **Within a leg, month references in her handwriting do the ordering** — a November day against an
   October museum ticket places the card after the museum stop. The month names its own anchor.

**Rule adopted:** an ordering clue must name its own anchor. Dated prop strongest; card text naming
the other place or event is fine; a bare "next"/"then" with no referent is not a clue. Her voice
keeps the phrasing, the clue set stops depending on it.

**Leg 1 settled — Leif moves to 24 Aug – 11 Sept** (L1 L'Anse 24 Aug with the museum ticket, L2
Battle Harbour 30 Aug, LD Brattahlíð 5 Sept, L3 Qikiqtarjuaq 11 Sept). February was chosen to make
L3's aurora work and broke the rest of the leg. The page had already conceded L'Anse's visitor
centre is shut in February and that Battle Harbour is not credible in winter — that compromise is no
longer survivable, because a closed visitor centre cannot issue the dated ticket the leg order now
depends on. A third problem was unrecorded: **LD's "green against the ice" is false in February**;
the Eastern Settlement greens up June–September. The new window satisfies all four cards.

**Leif now needs no ordering text beyond L1's opening line** — L1 states it is first, the transition
ticket out of Qikiqtarjuaq proves L3 closes the leg, L2 is second by elimination, LD is filtered by
the crest. So **L2's "Second stop: Markland" was rewritten to "Markland today"** and rebuilt,
matching L3's earlier change this session.

**Files changed:** `NorseBackpack/Postcards/build_postcard_L2_pdf.py` (opener plus a comment),
`output/pdf/Postcard_L2_Battle_Harbour_Print.pdf` and `..._Letter_Print.pdf` (rebuilt),
`NorseBackpack/Norse_Brainstorm.html` (the decision, the rule, Leif's new leg table, the stale
warning and the new-work warning).

**Checks run:** L2 rebuilt and its back rendered and read — the new opener is correct and the layout
is unchanged. Page served over HTTP, Final riddle tab inspected, all new blocks present, console
clean, solving board still renders.

**STALE — do not trust until the remaining legs are re-dated:** the 22-row itinerary table, the
"Where she was, and when" timeline chart, `Tools/final_riddle_clues.py`'s `ITIN` and clue set, and
the solving board's dates and clue list. All still describe the interleaved February–December year.
The deck, crest filter and four digits are unaffected. This is flagged at the top of the Final
riddle tab.

**New work this model creates:** none of the four museum tickets currently carries a printed date
(checked `Props/MuseumTicket`, `Props/AudTicket`, `Props/Hnefatafl`) — under this model those four
dates *are* the leg order, so all four must be dated and reprinted. The three transition tickets do
not exist yet. Leif's transition wants a multi-segment e-ticket itinerary, since there is no direct
Qikiqtarjuaq–France service.

**Next action:** settle Rollo's leg the same way — pick its window (it must follow 16 Sept, when
Leif's leg ends), check each of the seven cards' text against that season, place the Rouen museum
ticket inside the leg rather than at its start so the month-reference device has something to work
against, and decide which stop the Leif→Rollo transition ticket lands on.

## Session Close — 2026-09-19 — Interactive solving board added to the Final riddle tab

**Task:** the user asked for an interactive part in the Final riddle tab: a calendar timeline, the
clue list with prop names, the postcard names, clickable clue ticks, and postcards that can be moved
onto the timeline.

**Two decisions taken with the user before building:** the board gives **live feedback** (each clue
shows satisfied / broken / not-yet as you place cards) rather than being a silent manipulation
surface; and the timeline is **22 ordered slots**, not a Feb–Dec month strip, because a team deduces
an order rather than a date per card. Month bands would have leaked roughly where each card belongs.
The seven dated props print their dates on their slots as visible anchors.

**Built:** a self-contained block at the end of `#final-riddle` in `Norse_Brainstorm.html` — its own
`<style>`, markup and `<script>`, so it can be found and edited in one place. Deck of 22 cards
coloured by trail with decoys tinted; 22-slot timeline; 19 clue rows grouped by where the clue lives
(built cards / cards still to write / added clauses / dated props / final bundle / structural rule).
Cards move by drag-and-drop or by click-then-click-a-slot; dropping onto an occupied slot swaps.
Controls: Clear board, Clear ticks, a **final-bundle toggle** that withholds or grants the three
bundle items, and Fill recorded answer. A readout shows each trail's order, its digit when the trail
matches the recorded answer, and the first-appearance order. Board state persists in `localStorage`
(wrapped in try/catch, and unknown card ids are discarded on load).

**Deliberate limitation, written into the page and into the script's header comment:** the board
checks one arrangement, it does not enumerate, so it cannot prove uniqueness — that stays
`Tools/final_riddle_clues.py`'s job. The two now hold the same clue data in two places and must be
changed together.

**Files changed:** `NorseBackpack/Norse_Brainstorm.html` (board plus a scope note), and
`.claude/launch.json` — `autoPort: true` and the hardcoded `8734` dropped from `runtimeArgs`, because
port 8734 was held by another session's server.

**Checks run:** served over HTTP and driven through the DOM. Empty state correct (22 cards, 22 slots,
7 dated anchors, 19 clues, bundle rows withheld). Filling the recorded answer with the bundle in hand
turns all 19 rows green, reads `1 9 7 2`, and gives first appearances Leif → Rollo → Aud → Harald,
matching the solver. Violations were induced and caught correctly: moving R4 away from R3 broke
"Winchester next" while correctly leaving "Kyiv next" grey (its other card was unplaced); swapping R1
and R6 broke `R1 opens Rollo`, `R6 closes Rollo` and `Rollo first-appears before Aud` together. Tick
toggling sets and clears `aria-pressed` and the glyph. All eleven tabs still open and the console is
clean.

**Not verified visually in full:** the Browser pane returned blank screenshots for the lower part of
the board while it was hidden, so layout below the clue list was confirmed by geometry and text
rather than by eye. The deck, timeline and clue list were seen rendered and are correct.

**Next action:** open the Final riddle tab and try to solve it from a cleared board with the bundle
withheld — that is the first real use, and it will show whether the clue wording reads as intended
before any of the four unwritten cards are drafted.

## Session Close — 2026-09-19 — L3 no longer numbers itself ("Third stop" → "New stop")

**Task:** the user asked what would change if card L3 stopped saying "third stop", then asked for
the change to be made as "New stop".

**Answer to the question, before the edit:** nothing in the logic. L1 and L2 pin positions 1 and 2
by their own printed text, and L3 is Leif's only other real card, so L3 third is forced by
elimination. Verified by re-running the solver (same 1 answer with the bundle, same 3 without) and
by a direct probe that found **zero** calendars placing L3 before L2 — so this is a real result,
not an artefact of the 400,000 enumeration cap.

**What it does change** is in the room: previously three of the four Leif-stamped cards numbered
themselves, which exposed decoy LD Brattahlíð as "the one with no number" from card text alone.
Two Leif cards now carry no position statement, so the crest filter is needed to tell L3 from LD.
It also partly answers the decoy complaint already recorded in the Final riddle tab — the
unfiltered trace is no longer a single option (L1→L2→LD→L3 reads as a V, not a 1).

**One cost, recorded rather than solved:** the digit itself gains nothing — a 1 has no internal
shape, so either endpoint still draws a plausible stroke. This buys "the crest is needed", not "the
shape self-checks". Open under `PZ-18`.

**L3 keeps both of its jobs.** An earlier draft of this entry claimed the position statement was
L3's only contribution and that the card now failed the 15 Sept "every card's job 3 gates a lock"
rule. That was wrong. L3 is still one of the three map points drawing Leif's 1, still placed third
(by elimination rather than by its own text), and still gates a physical lock — under `PZ-13` the
L2/L3 hold-to-light join opens lock 3, which is independent of the opening sentence. An ordering
statement was never what satisfied job 3 anyway; that rule explicitly excludes "a calendar
statement" on its own. What was removed is a *clue*, not a job.

**Warning recorded in the page:** do **not** also remove L2's "Second stop". Tested this session —
with both anchors gone, L3-before-L2 becomes reachable and Leif's order is no longer forced. The
solver still reports one answer in that configuration, but that is a **false pass**; the reversed
calendars sit beyond the enumeration cap and a direct probe finds them immediately. Future clue cuts
on this leg must be checked with a probe, not with the answer count alone.

**Files changed:**
- `NorseBackpack/Postcards/build_postcard_L3_pdf.py` — message opener, plus a comment recording why
- `NorseBackpack/Tools/final_riddle_clues.py` — removed `C('pos', ('L3', 3))`, left a comment in its place
- `NorseBackpack/Norse_Brainstorm.html` — dropped the L3 row from the clue-set table; reworded the
  Leif row in the constraint worksheet; corrected the "positions 1–3 are locked" note to 1–2; added
  the decision note and the L2 warning to the Final riddle tab; updated the quoted message in `PZ-05`
- `output/pdf/Postcard_L3_Baffin_Island_Print.pdf` and `..._Letter_Print.pdf` — rebuilt

**Checks run:** solver re-run (TEST 1 PASS, TEST 2 PASS 3 answers without bundle, TEST 4 PASS;
TEST 3 still NOT RUN, geometric as before). Reversed-order probe run on both the drop-L3 and
drop-L2+L3 configurations. L3 PDF rendered to PNG and visually inspected — the new opener reads
correctly and the layout is unchanged. Design page served over `localhost:8734`, Final riddle tab
inspected in the browser: the new note and warning render in the right place and the console is
clean.

**Not done:** `NorseBackpack/Postcards/Postcard_L3_Baffin_Island_Back.png` (13 Sept) is a stale
leftover from the old `build_postcard_collection.py` back design and does not contain the message,
so it was left alone — it was already stale before this change.

**Next action:** nothing outstanding on L3 itself. The open items on this leg are the ones that
predate this session: validation TEST 3 (geometric, per-decoy), and the element-mark assignment and
reprint pass that all 22 cards still need.

## Session Close — 2026-09-19 — Two hand-drawn decoy postcard marks added

**Task:** create two simple hand-drawn marks for the decoy postcards: a horned Viking helmet
and a double-sided axe.

**Result:** added two transparent 300 × 300 PNGs in
`NorseBackpack/Art/FinalPuzzle/PostcardMarks/`: `Decoy_Horned_Helmet_HandDrawn_v1.png` and
`Decoy_Double_Axe_HandDrawn_v1.png`. They use the same loose dark outline, muted flat colour and
slight handmade wobble as the nine real marks. The helmet has exactly two horns. The double axe
has two opposing blades and remains visibly distinct from the real single-bladed battle axe.

**Decoy assignment revised, 19 Sept 2026:** Leif/Aud share the horned helmet; Rollo/Harald share
the double-sided axe. This supersedes the earlier Mjölnir/crown choice. Both are intentionally
wrong stereotypical Norse signals, which suits their role as fake elements.

**Production:** the helmet was generated with ImageGen. The double-axe ImageGen request hit the
account usage limit, so the final asset was derived from the approved single-axe mark by reflecting
its existing blade across the haft axis. The exact helmet prompt, attempted axe prompt and actual
construction are recorded under `PR-22` in `NorseBackpack/Norse_Brainstorm.html`.

**Files changed:** the two PNGs above, `NorseBackpack/Norse_Brainstorm.html`, and `HANDOFF.md`.

**Checks:** both PNGs were visually inspected at full size; both are 300 × 300 `Format32bppArgb`
with transparent corners. The updated design page was served over `localhost:8734`; both new marks
render in the `PR-22` gallery and the browser reports no warnings or errors.

**Still open:** redesign one of the confusable round-shield/sun-wheel marks; assign the nine real
marks to individual cards; choose final printed size and treatment; print-proof representative
marks at card size.

**Next action:** redesign either the round shield or sun-wheel silhouette, then make a small
actual-size print proof including one real mark and both decoys.

## Session Close — 2026-09-19 — Hand-drawn postcard crest marks generated

**Task:** correct the six separate crest-element drawings for postcard use. The first pass was too
polished; the user wanted small hand-drawn marks rather than full 1254 px heraldic assets.

**Current reference drawings:** `NorseBackpack/Art/FinalPuzzle/Family_Symbol_Three_Field_v2.png`
is the revised family symbol: one circular knotwork emblem split into three equal compartments,
with the raven, longship and eight-spoked sun-wheel at comparable size and visual weight.
`Family_Crest_Six_Field_v2.png` is the current six-element family crest: a dimensional, elaborate
Norse heraldic achievement with a central two-column by three-row shield carrying axe, round
shield, wolf, anchor, drinking horn and valknut in reading order. Both are 1254 × 1254 transparent
PNGs.

**Current eleven postcard marks:** `NorseBackpack/Art/FinalPuzzle/PostcardMarks/` contains one simple
transparent 300 × 300 PNG for every real element plus two decoys. Crest: battle axe, round shield,
wolf, anchor, drinking horn and valknut. Symbol: raven, longship and eight-spoked sun-wheel.
Decoys: horned helmet and double-sided axe. They match Aunt
Liv's existing Bayeux-inspired margin-drawing language: loose dark pen outline, flat muted
coloured-pencil fills, slight handmade wobble and sparse detail. The existing cross and bow
drawings were used as style references only. No postcard carries one yet. The longship generation
needed a background-extraction pass plus a low-alpha threshold to remove a faint surrounding haze.

**Superseded but retained:** the ornate 1254 × 1254 individual studies in
`NorseBackpack/Art/FinalPuzzle/CrestElements/` were the wrong interpretation for postcard marks.
They remain as a record only. `Family_Crest_Six_Field_v1.png` also remains the superseded simpler
shield-only crest direction. `Family_Symbol_Raven_Crest_v1.png` is also superseded: its raven was
far larger than the longship and sun-wheel, so it did not work as an equal three-item key.

**Design page:** `NorseBackpack/Norse_Brainstorm.html` now shows both current drawings under
`PR-22`, records the equal-three-field symbol revision and its exact ImageGen prompt, shows all nine
current hand-drawn postcard marks, records the three new prompts and longship cleanup, and labels
both earlier directions as superseded where relevant.

**Checks:** confirmed all nine current files are 300 × 300 `Format32bppArgb` PNGs with transparent
corners. Visually inspected the downsized production files; all nine remain clear and distinct.
Served `Norse_Brainstorm.html` over `localhost:8734`; the mark gallery renders cleanly, every image
loads, and the browser console reports no warnings or errors. Also
confirmed the revised 1254 × 1254 family symbol has transparent corners and renders cleanly beside
the crest; its three subjects occupy separate, comparably sized compartments.

**Still open:** user approval of the corrected drawings; the 22 per-card element assignments,
final printed size and physical treatment remain separate `PZ-18` design tasks. A proof at roughly
0.4–0.5 inches wide is suggested, not decided.

**Next action:** after visual approval, assign the nine real elements and two shared fake elements
to the 22 postcards, then place and print-proof one representative mark at actual card size.

## Session Close — 2026-09-19 — Final riddle: visual form of the two reference drawings decided,
generation briefs written for Codex

**Task:** continuing the same session (see the two entries below for Leif/Rollo and Aud/Harald).
Moved to the final route/endgame puzzle (`PZ-18`). The mechanism, itinerary and element *lists*
were already decided (17 Sept); what was still open was what the final bundle's two reference
drawings actually look like, and who builds them.

**Decided with the user, 19 Sept 2026:** the 3-element family logo (raven, longship, sun-wheel) is
drawn as a **raven crest** — an edit of `PR-15`'s existing raven-in-knotwork artwork
(`Art/Raven/Raven_Profile_Knotwork_Frame_v1.png`), with the longship and sun-wheel worked into the
same knotwork ring as two more charges, rather than a new drawing from scratch. The 6-element family
crest (battle-axe, shield, wolf, anchor, drinking horn, valknut) is drawn as a **family coat of
arms** — a new Norse-styled heraldic shield with six fields, one charge each. Confirmed with the
user that a shield-icon charge sitting on a shield-shaped crest is fine (heraldry does this
routinely), not a redundancy to design around.

**This is Codex's job, not Claude Code's**, per the project's existing agent split (image/asset
generation is Codex's lane). Recorded as `PR-22` in `Norse_Brainstorm.html`, with full
Codex-ready generation briefs for both drawings in the project's established prompt format (Use
case / Asset type / Primary request / Style / Composition / Color palette / Constraints) and the
shared two-tone palette (`#283B34` forest green, `#B56A2A` muted rust). The raven crest brief is a
precise-object-edit against the existing PNG; the coat of arms brief is a fresh illustration-story
generation. Both link back to `PZ-18`'s final-riddle mechanism and forward to `PR-15`'s existing
raven asset.

**Files changed:** `NorseBackpack/Norse_Brainstorm.html` only — no image files were generated this
session (that's the point of handing this to Codex). Updated: the final-riddle tab's "Which
drawing covers which trail" panel (visual-form decision + link to `PR-22`); new `PR-22` entry with
both generation briefs.

**Checks run:** served the page over `localhost:8734`, confirmed no console errors after each edit.

**Not done / explicitly out of scope:** no artwork was generated — this session only wrote the
design decision and the handoff brief for whoever runs Codex next. Two things remain genuinely open
and are *not* resolved by these two reference drawings: (1) the per-card element-mark assignment —
which of the 22 postcards carries which of the 9 elements (3 symbol + 6 crest, or one of the 2
shared fakes) — is still undecided; (2) the mark's own physical form (wax seal? picture-border
mark? — deliberately not UV) and its legibility test at card size are still open. Also still
unresolved from earlier passes: validation test 3 (no decoy should draw a plausible rival digit,
which is in tension with decoys needing to draw a *plausible wrong* digit — one of the two has to
give), and AD/HD's decoy card text is written but the two reference-drawing decisions here don't
touch that.

**Next action:** hand `PR-22`'s two briefs to Codex to generate the raven crest edit and the coat
of arms. Once both exist, the natural follow-on is the per-card element-mark assignment — deciding
which element sits on which of the 22 cards, and what the mark itself physically looks like at card
size — which is a Claude Code design-reasoning task, not Codex's.

## Session Close — 2026-09-19 — Aud/Harald recap; synced stale treasure entry; 3 new build-task
notes; composited the hnefatafl board setup onto Harald's map back

**Task:** continuing the same recap-and-tidy session (see the entry below for Leif/Rollo). Recapped
Aud's leg and Harald's leg with the user, synced a stale puzzle-card table entry, logged three
props that are designed but not yet physically built, and implemented the one piece of mechanical
follow-through the user asked for: compositing the hnefatafl board-setup panel onto the real back
of Harald's map sheet.

**Aud's leg recap — no design changes, one sync fix:** the `treasure` entry in
`Norse_Brainstorm.html`'s puzzle-card reference table still described the shelved 18 Sept
split-panel design (code `467`) and had never been updated after `PZ-17`'s two rewrites since.
Rewritten to match `PZ-17`'s actual current state: single portrait map, six legs walked on the real
drawn network, code `521` (5 bridges, 2 fords, 1 gate), and the real outstanding risk (the tally is
confirmed in the routing graph only — never walked by hand on a printed sheet).

**Three build-task entries added, `PR-19`/`PR-20`/`PR-21`:** none of these props have been modelled
or printed yet, all were previously only implied inside design prose rather than tracked as
discrete to-dos.
- `PR-19` — the comb (`PZ-03` grille lock, candidate answer `BOOK`). Needs: pick which letters of
  AD's built message the teeth must expose, derive tooth-gap spacing from the card's actual printed
  text layout, model, print, test-fit against the real card.
- `PR-20` — the hoard's coins (`PZ-03` balance lock, `SOLE`). Blocked on `PR-02`'s scale purchase.
  Needs: three distinguishable coin faces, a count/weight that hits `370.56 g` exactly, print,
  confirm on the real replacement scale.
- `PR-21` — the five-ring cryptex (`PZ-02` rune lock, `HRAFN`). Open design question folded in:
  plain Latin letters on the rings (simple) vs. the branch-rune glyphs themselves (stronger
  in-fiction match, but needs an extra translation step the game doesn't currently teach).

**Harald's leg recap** — all three locks (branch-rune cryptex `HRAFN`, hnefatafl `253`, mead riddle
`MEAD`) already decided and mostly built; nothing changed by the recap itself beyond surfacing the
compositing gap below.

**Hnefatafl board-back compositing, implemented this session:** the board-setup panel
(`build_board_setup_pdf.py`) previously only existed as a standalone insert PDF, sized to its own
small page, never drawn onto Harald's actual map sheet — so the "recover the setup from the back of
the map she gave you" fiction was backed by two loose, unrelated pieces of paper. Fixed in
`NorseBackpack/TravelMap/build_trail_maps_pdf.py`: imports `draw_grid`/`W`/`H` from
`build_board_setup_pdf.py` (`sys.path` extended to `NorseBackpack/Props/Hnefatafl`), and a new
`draw_harald_board_back(c)` fills a full letter page in the shared paper tone and draws the
board-setup content centred on it. Hooked in right after the front page's `c.showPage()`, only for
`key == "harald"`. Both `Trail_Map_4_Harald_Print.pdf` and `_ANSWER.pdf` are now 2-page PDFs, ready
to print duplex and laminate as one object.

**Files changed:** `NorseBackpack/Norse_Brainstorm.html` (`treasure` puzzle-card entry rewritten;
`PR-19`, `PR-20`, `PR-21` added; `hnefatafl` puzzle-card entry and `PZ-09`'s own text updated for
the compositing fix); `NorseBackpack/TravelMap/build_trail_maps_pdf.py` (new import block, new
`draw_harald_board_back` function, one hook in the per-trail save sequence);
`output/pdf/Trail_Map_4_Harald_{Print,ANSWER}.pdf` (rebuilt, now 2 pages each).

**Checks run:** rebuilt Harald's two PDFs in isolation, then reran the full `build_trail_maps_pdf.py`
with no argument to confirm all four trails (Leif, Rollo, Aud, Harald) still build cleanly with no
regressions — same label counts, same digit callouts (1/9/7/2), only Harald gained a page. Read
back both pages of `Trail_Map_4_Harald_Print.pdf`: front renders as before; back shows the title,
grid, stain, pieces, throne and Liv's margin note correctly, on the same paper colour as the front.
Served `Norse_Brainstorm.html` over `localhost:8734` after each edit, no console errors.

**Not done / explicitly out of scope this session:** none of `PR-19`/`PR-20`/`PR-21`'s actual
3D models were built — only the fact that they're unstarted was recorded. `PR-09`'s own open
question (whether the ticket's ink offset reads through real stock while the stain still hides the
original, and whether the front grid or the new back-page ink ghosts through real laminate) remains
untested — the compositing fix makes that test possible but doesn't substitute for it.

**Next action:** print a physical test of Harald's composited sheet (both pages, real stock, real
lamination) and check `PR-09`'s ghosting/registration questions now that there's a real two-sided
object to check them against, rather than a separate insert. Otherwise continue leg-by-leg — Leif,
Rollo, Aud and Harald have all now had a first recap pass this session.

## Session Close — 2026-09-19 — Leif recap closed two risks; Rollo's word-lock redesigned to a 4-digit lock

**Task:** recap Leif's leg with the user (puzzles/props/postcards), close two open risk items on
it, then recap Rollo's leg and redesign its word-lock chain per the user's call that a directional
(arrow) lock is expensive and finicky.

**Leif's leg — two open risks closed, no mechanism change:**
- Bear vs. wolf icon legibility (`PZ-13` risk note) — user confirmed legible and distinct at print
  size. No longer an open risk.
- Leif's trail drawing an almost-shapeless "1" (`PZ-06` shape-check note) — user confirmed fine, a
  1 doesn't need internal shape. No longer a concern to solve.

**Rollo's word-lock chain (`PZ-15`) redesigned, code decided:** the six-word directional lock
(`R D D U L L`) is replaced with a four-word, 4-digit numeric combo lock. Two of the six word-pairs
(beef/cow, forest/woodland) are dropped from the solve by cutting their sentence from postcard R2's
message; the remaining four (combat/fight, poultry/hen, tavern/inn, people/folk) are read the same
way as before (postcard → order, ticket → grid coordinate, map icon → the coordinate), except the
readout changes from "direction from icon to coordinate" to "count the squares between them" — all
four pairs already share a row or column, so no remeasuring was needed. **Code: `1486`**
(fight=1, folk=4, hen=8, inn=6, in message order). The user chose to leave the now-unused cow and
forest map icons in place as inert decoration rather than removing them or repurposing them into
the ticket's filler pairs. R2's message gained a rule-line in the same family as LD's "every little
detail counts" (`PZ-10`) to plant counting as Liv's habit: "Can't walk anywhere without counting my
steps — always have."

**Files changed:** `NorseBackpack/Norse_Brainstorm.html` (`PZ-13` risk note, the shape-check note
under the map-mechanic section, `PZ-15`'s full entry rewritten, the `wordlock` puzzle-card data
object, the Rollo lockflow diagram, and R2's quoted message under `PZ-05`);
`NorseBackpack/Postcards/build_postcard_R2_pdf.py` (forest/cow sentence replaced with the new
rule-line, comment updated); `output/pdf/Postcard_R2_Rouen_{Print,Letter_Print}.pdf` (rebuilt).

**Checks run:** rebuilt R2's PDFs and read them back — text fits the card, no overflow, message
reads correctly in Liv's voice with the new line, solve order (fight, people, poultry, inn) intact.
Served `Norse_Brainstorm.html` over `localhost:8734` and confirmed no console errors and the new
`1486` code renders in the lockflow diagram, `PZ-15`, and the puzzle-card reference table.

**Not done / explicitly out of scope this session:** the Rouen museum ticket
(`build_rouen_ticket_pdf.py`) was not touched — it still lists all fifteen word pairs including
the now-unused beef/cow and forest/woodland, which is correct as-is (they're meant to stay as
valid-but-unused entries, not camouflage). Rollo's trail map was not touched — the cow/forest icons
stay exactly where they are. No physical 4-digit lock has been bought yet (`ST-01` still open on
which container this chain feeds).

**Next action:** recap Aud's leg with the user (puzzles/props/postcards) — in progress as this
entry is written; see the `PZ-17` entry in `Norse_Brainstorm.html` for its current state (treasure
hunt redesigned 17–19 Sept, code `521`, one outstanding verification: print a test sheet and walk
the six legs by hand against the ticket, never yet checked on paper).

## Addendum — same session — Aud's map styling marked final

Checked in on the concurrent Codex session: no further edits since its last entry below (`aud_layer.py`,
`Aud_Map_Designer.html`, `build_trail_maps_pdf.py` all still at their 14:35 mtimes). Its three passes
today (Option A &rarr; hybrid bridge-hiding &rarr; road-join/bridge-restore refinement) are done, and
its own log already tracked `521` throughout (explicitly noted the bridge records were untouched
during the hybrid trial). The canonical `Trail_Map_3_Aud_{Print,ANSWER}.pdf` rebuilt earlier in this
entry already carries that final state.

**Decided with the user:** this is Aud's map, final. Updated `Norse_Brainstorm.html`'s two leftover
"current trial" notes (Option A, hybrid) to read Decided/Superseded instead of "current," and added
an explicit final-styling note pointing at the canonical PDFs and the Drafts folder. Rendered and
checked for console errors after the edit.

## Session Close — 2026-09-19 — H6 built (all 22 postcards complete); output/pdf cleanup

**Task:** draft and build the last unwritten postcard (H6, Patara), then a full inventory check of
`output/pdf/` turned up map/ticket drift from a concurrent Codex session working the same files.

**H6 built:** `build_postcard_H6_pdf.py` (new, from the H5 template), message and Fun Fact per the
user's draft, `Postcard_H6_Patara_Print.pdf`/`_Letter_Print.pdf`/`_Back.png` built and checked.
`Norse_Brainstorm.html`'s gallery card, `PZ-05` and `PC-07` pills updated: **18 of 18 real cards,
22 of 22 total, complete.**

**`output/pdf/` inventory turned up drift, not caused by this session:** a concurrent Codex
session (see the entries below) was iterating on Aud's map styling in parallel and had left three
undecided variants (`OPTION_A`, `HYBRID`, `REFINED`) alongside the canonical
`Trail_Map_3_Aud_Print.pdf`/`_ANSWER.pdf`, none referenced from `Norse_Brainstorm.html`. Also
found `Trail_Map_1_Leif_Print_UPDATED.pdf`, dated 12 Sept &mdash; a week *older* than the
canonical 18 Sept `Trail_Map_1_Leif_Print.pdf` despite the filename.

**Resolved with the user, in chat:** REFINED (Codex's most recent pass, 14:35) is the map to keep;
the 18 Sept `Trail_Map_1_Leif_Print.pdf` is the Leif version to keep. Re-ran
`python build_trail_maps_pdf.py aud` from the current (post-Codex) script state, which regenerated
`Trail_Map_3_Aud_Print.pdf`/`_ANSWER.pdf` under their canonical names with REFINED's content &mdash;
confirmed `aud_features.json` (the route geometry the `521` code depends on) is untouched since 18
Sept, so this is a styling-only refresh, not a geometry change. Rendered and visually checked the
rebuilt canonical PDF.

**Moved to `NorseBackpack/Drafts/2026-09-19_Aud_map_style_options/`** (with a README, same pattern
as the 17 Sept split-panel drafts): `Trail_Map_3_Aud_OPTION_A_{Print,ANSWER}.pdf`,
`_HYBRID_{Print,ANSWER}.pdf`, `_REFINED_{Print,ANSWER}.pdf`, `Aud_Map_Legend_Options.pdf`, and
`Trail_Map_1_Leif_Print_UPDATED.pdf`. `output/pdf/` now holds exactly one Print/ANSWER pair per
trail map.

**Files changed:** `NorseBackpack/Postcards/build_postcard_H6_pdf.py` (new);
`output/pdf/Postcard_H6_Patara_{Print,Letter_Print}.pdf` (new);
`NorseBackpack/Postcards/Postcard_H6_Patara_Back.png` (new); `Norse_Brainstorm.html` (H6 gallery
card, PZ-05/PC-07 pills); `output/pdf/Trail_Map_3_Aud_{Print,ANSWER}.pdf` (rebuilt in place, same
filenames); 8 files moved to the new Drafts folder (not tracked by git yet, so plain `mv`, not
`git mv`).

**Checks run:** H6's PDFs rendered to PNG and inspected (front art intact, message and Fun Fact
both fit, postmark reads PATARA). `Norse_Brainstorm.html` served over `localhost:8734`, images
confirmed loading at full 1500&times;1050, no console errors. Aud's rebuilt canonical map rendered
to PNG and inspected &mdash; label placement clear of roads, legend intact, `521`'s digit-7 shape
unaffected.

**Not done:** did not touch `aud_layer.py`, `Aud_Map_Designer.html` or `build_trail_maps_pdf.py`
themselves &mdash; those are mid-edit in the concurrent Codex session (see below); only re-ran the
existing build to pick up already-committed changes under the canonical output filenames.

**Next action:** none outstanding for Aud's leg or the postcard deck. If picking this up again,
check whether the Codex session below has moved further since &mdash; it was still actively
editing `aud_layer.py` as of this entry.

## Session Close — 2026-09-19 — Aud road joins and crossing refinement

**Task:** merge road geometry cleanly at forks, keep gates in the foreground, restore the original
ford mark, and return bridges with a more natural design that follows the road.

**Changed:** `aud_layer.py` and `Aud_Map_Designer.html` now draw every road casing first and every
road interior second, removing the false overlap line where separate road features meet. Ordinary
landmarks draw before bridges, fords and gates, keeping all countable crossings in front. Ford is
again the original two-bank-ticks and three-stones symbol. Bridge is back in the map, legend and
designer palette with a new bowed deck and light cross-planks; bridge and ford rotate to their
nearest road/track/path, while gates rotate to their barrier. `build_trail_maps_pdf.py` again
reserves bridge marks during label placement. `Norse_Brainstorm.html` records the refinement.

**Outputs:** `Trail_Map_3_Aud_REFINED_Print.pdf` and `_ANSWER.pdf`. Review filenames remain in use
because the stable print PDF has recently been open in PDFgear.

**Checks:** Python compilation passed. Both one-page letter PDFs rendered at 180 dpi and were
visually inspected: forked roads merge cleanly, the H5 gate is legible in the foreground, bridges
follow their local route direction, the requested ford mark is present, and the answer remains 7.
The editable designer loaded over local HTTP with Bridge restored and no console warnings/errors.

**Gate follow-up:** wall blocks within the span of a gate are now omitted in both renderers. A
240-dpi H5 crop confirms a clean opening between the posts without erasing the road underneath;
the refined print/answer PDFs were rebuilt and the designer again reported no console errors.

**Next action:** review the new bridge on paper or at 100% size. If approved, close any stable map
PDF open in PDFgear and rebuild `Trail_Map_3_Aud_{Print,ANSWER}.pdf` from the refined source.

## Session Close — 2026-09-19 — Aud map hybrid icon trial

**Task:** keep the Option A map as the base, remove visible bridges, restore the existing landing
icon, and use Option B for gates, fords and stone walls.

**Changed:** `NorseBackpack/TravelMap/aud_layer.py` and `Aud_Map_Designer.html` now hide bridge
symbols and omit Bridge from the legend/tool palette. The 11 bridge records remain in
`aud_features.json`, so the corrected route logic and code `521` are unchanged. Landing is again
the original anchor; gates, fords and stone walls use Option B. The sage-grey marsh and improved
label placement remain. `build_trail_maps_pdf.py` excludes the now-invisible bridge points from
label obstacles. `Norse_Brainstorm.html` records this hybrid as the current trial.

**Outputs:** `Trail_Map_3_Aud_HYBRID_Print.pdf` and `_ANSWER.pdf`. The usual stable-name print PDF
was open in PDFgear, so this review pair avoids overwriting only one half of the stable pair.

**Checks:** Python compilation passed. Both one-page letter PDFs rendered at 180 dpi and were
visually inspected: no bridge marks or Bridge legend row remain, the requested icon variants are
present, label fixes remain intact, and the answer still reads 7. The editable designer loaded
over local HTTP, showed no Bridge tool, and reported no browser console warnings or errors.

**Next action:** choose whether to keep this hybrid. If approved, close the old print PDF in
PDFgear and rebuild the stable-name `Trail_Map_3_Aud_{Print,ANSWER}.pdf` pair.

## Session Close — 2026-09-19 — Aud's code corrected to 521; legs 5/6 merged; A2 rewritten and built

**Task:** the user walked the printed Aud map (`Trail_Map_3_Aud_ANSWER.pdf`) against `PZ-17`'s leg
table by hand and found it didn't match. Corrected the code, redesigned leg 5's ambiguity around
the fix, and built the postcard that resolves it.

**What was wrong:** leg 4 (landing &rarr; standing stone) crosses 1 bridge only, no ford. My own
coordinate-snapping against `aud_features.json` got this wrong twice in a row (first credited the
ford to leg 4, then wrongly to leg 3) before the user's on-paper count settled it: 2 fords total,
both on leg 2. Corrected tally is **5 bridges, 2 fords, 1 gate &mdash; code `521`**, not `531`.
Everything else in the leg table was already right.

**Redesigned, same session:** legs 5 and 6 merged into one ticket row &mdash; from H5, the
direction is now "Follow the road to the village at the crossing," crossing the H5 gate and the
H7&ndash;H9 bridge together (tally `1 0 1`). The standing stone at H7 is still physically on the
road but is no longer a named stop. The ticket is six legs now, not seven; confirmed with the user
first that seven was never a real constraint (`PZ-17` already called the old row count
"coincidence").

New ambiguity: two village-at-a-crossing landmarks look alike on the sheet &mdash; H9 (real, the
cairn/church/village cluster) and one near H3/G3 (decoy, off-route back near the start). Card A2
resolves it by direction (south) and the wood the correct road runs beside (H5/H6/I5/I6). The old
H5-fork mechanic (open ground vs. the trees, wrong branch scoring `432`) is superseded and marked
so in place, not deleted.

**A2 fully rewritten and built for the first time.** New message (drafted by the user, in Liv's
voice) names the treasure hunt and hints at what to count &mdash; rivers, fords, gates &mdash;
without stating the answer. Built `build_postcard_A2_pdf.py` from the A3 template; A2 had front
art only until now, no back, no print PDF.

**Files changed:**
- `NorseBackpack/Norse_Brainstorm.html` &mdash; `PZ-17`: code `531`&rarr;`521` everywhere (6
  refs), leg table collapsed 7&rarr;6 rows, the H5-fork mechanic marked superseded, A2's message
  and Fun Fact rewritten, "seven legs" references (6 places) corrected to six. Also fixed in
  passing: a duplicated `</i>` tag left by an earlier edit this session, and a stale reference to
  the long-dead `467` code.
- `NorseBackpack/Props/AudTicket/build_aud_ticket_pdf.py` &mdash; `LEGS`/`PER_LEG`/`ANSWER` updated
  to the merged 6-leg, `521` route; docstring updated to match.
- `output/pdf/Aud_Ticket_Print.pdf`, `Aud_Ticket_Letter_Print.pdf` &mdash; rebuilt.
- `NorseBackpack/Postcards/build_postcard_A2_pdf.py` (new) &mdash; back-of-card builder, same
  pattern as A3/AD.
- `output/pdf/Postcard_A2_Hvammur_Print.pdf`, `Postcard_A2_Hvammur_Letter_Print.pdf` (new).

**Checks run:** the ticket script's own `assert` (per-leg tallies sum to `ANSWER`) passed on
rebuild. Both ticket PDFs rendered to PNG and inspected &mdash; 6 rows, `ANSWER 5 2 1` visible, leg
5 reads `1 0 1`. A2's front and back both rendered to PNG and inspected &mdash; front art intact,
back text fits its column, postmark reads HVAMMUR, Fun Fact box doesn't overflow.
`Norse_Brainstorm.html` served over `http://localhost:8734`: no console errors, "village at the
crossing" confirmed present in all three expected spots.

**Resolved same session:** the user confirmed on the printed sheet that A2's forest clue works
&mdash; the wood at H5/H6/I5/I6 reads as "the road follows the forest for a while," distinctly
from the H3/G3 lookalike. No longer open.

**Dropped as dead weight, same session:** the old H5-fork wrong-branch value (`432`) was never
re-verified after the ford correction and no longer serves any puzzle function now that leg 5's
ambiguity is the village-at-the-crossing mechanic, not the fork. Checked the repo for remaining
`432` references &mdash; the two still in `Norse_Brainstorm.html` are unrelated (a page-size
number) or already inside the marked-superseded note, and `build_aud_ticket_pdf.py` never
mentioned it after this session's rewrite. Nothing left to clean.

**Still open:**
- The session below this one (Codex, same day) was editing `Aud_Map_Designer.html`, `aud_layer.py`
  and `build_trail_maps_pdf.py` concurrently with this work. This session did not touch those
  files, but both sessions were changing map-adjacent things at the same time &mdash; worth a
  fresh read together before assuming either is fully caught up on the other.

**Next action:** Aud's leg has nothing outstanding. Next real work across the project is `H6`
(Harald's leg-closing card, PZ-05/PC-07) &mdash; the only one of 22 postcards still unwritten.

## Session Close - 2026-09-19 - Aud map Option A trial and label avoidance

**Task:** try Survey Option A on Aud's map and stop settlement labels from crossing roads and
other feature lines.

**Changed:** `aud_layer.py` and `Aud_Map_Designer.html` now use A across all 25 legend entries.
The prior sage-grey marsh is retained so it stays distinct from the pale blue lake.
`build_trail_maps_pdf.py` now reserves sampled feature linework and point symbols during label
placement, tries positions right/left/above/below at two distances, and keeps labels inside the
map frame. Búðardalur now prints left of its marker instead of through the road; Stykkishólmur's
fallback position remains inside the frame. `Norse_Brainstorm.html` records this as the current
comparison trial, leaving the B note as history.

**Outputs:** `Trail_Map_3_Aud_OPTION_A_Print.pdf` and `_ANSWER.pdf` are the two review PDFs. The
usual `Trail_Map_3_Aud_Print.pdf` was open in PDFgear and Windows denied replacing it, so the
existing stable-name print/answer pair was intentionally left together rather than half-updated.

**Checks:** Python compile passed. Both Option A PDFs are one-page letter sheets, rendered at
180 dpi and visually inspected; labels stay in-frame, Búðardalur is clear of the road, crossings
remain prominent, and the answer still reads 7. The designer loaded over local HTTP with no
console warnings or errors.

**Next action:** choose A or B. If A wins, close the old print PDF in PDFgear and rebuild the
stable-name `Trail_Map_3_Aud_{Print,ANSWER}.pdf` pair from the already-updated A source.

## Session Close - 2026-09-19 - Aud map switched to Saga option B

**Task:** apply Option B from the legend comparison to Aud's map, while making marsh visibly less
blue than lake.

**Changed:** `NorseBackpack/TravelMap/aud_layer.py` and `Aud_Map_Designer.html` now use the full
Saga family across all legend items: twin wheel tracks, walking-tick paths, double-bank rivers,
wave streams, broken double ditches, leaf hedges, linked-stone walls, B crossings, organic terrain
textures and B landmarks. Marsh is sage-grey (`#D9DDD0`, marks `#758676`) while lake remains pale
blue-teal (`#DCE7E4`). Rebuilt `Trail_Map_3_Aud_Print.pdf` and `_ANSWER.pdf`.
`Norse_Brainstorm.html` records the decision and supersedes the 18 Sept styling note.

**Checks:** Python compile passed. Both one-page letter PDFs rebuilt, rendered at 180 dpi and
visually inspected; the map remains legible, crossings remain the strongest marks, the answer
route still reads as 7, and marsh/lake are distinct. The designer loaded over local HTTP and
reported no browser console warnings or errors.

**Next action:** print the new map once at 100% scale and confirm the denser Saga symbols and
walking-tick footpaths remain clear on the intended printer.

## Session Close - 2026-09-19 - Aud legend option sheet

**Task:** create a printable comparison of Aud's current legend marks against the two proposed
replacement families, so the user can choose item by item.

**Built:** `NorseBackpack/TravelMap/build_aud_legend_options_pdf.py` and
`output/pdf/Aud_Map_Legend_Options.pdf`. The two-page letter PDF covers all 25 items currently
shown in the legend. Each row has Current, Option A (Survey) and Option B (Saga), using vector
marks in the existing palette. This is a selection sheet only; the production map is unchanged.

**Checks:** Python compile passed; PDF reports 2 letter-size pages; both pages were rendered at
160 dpi and visually inspected. All rows, headings and marks are present and unclipped.

**Next action:** user chooses Current, A or B for each row; then apply the selected symbols to
both `aud_layer.py` and `Aud_Map_Designer.html` and rebuild the print/answer maps.

## Session Close — 2026-09-18 — Aud map styling pass

**Task:** make Aud's printed treasure map look more polished without changing its route, code or geometry.

**Changed:** `NorseBackpack/TravelMap/Aud_Map_Designer.html` and `aud_layer.py` now use matching terrain textures: sparse tree marks for woods, reeds/ripples for marsh and short strokes for moor. Ordinary landmarks were softened to lavender `#806F96`. The countable puzzle crossings lead visually: bridges/gates are dark plum `#523A70`; fords dark teal `#216866`. The bridge glyph is now two strong abutment strokes rather than a rotated arch. Rebuilt both Aud map PDFs. `Norse_Brainstorm.html` records the styling decision.

**Checks:** Python compile passed; the designer loaded over local HTTP with no console errors. Both print and answer PDFs were rendered at 180 dpi and inspected: texture stays quiet, crossings are distinct, the route still reads as 7, and the legend reflects the new bridge glyph. Poppler reported its existing unavailable Symbol/ArialUnicode display-font warnings only.

**Next action:** print one physical test sheet and walk the seven ticket legs by hand. The graph confirms `531`; it still needs the on-paper usability check.

## Session Close — 2026-09-17 (latest 5) — Final-riddle dates, clue set and solver

**Task:** review of the whole Norse game (sequence, clues/props, what is missing), then a request
to propose dates and clues for the final puzzle, then a redesign of the timeline: start earlier
(2 Feb), vary the stay lengths, finish around December. Ended with the L2 tent→cabin swap and this
write-up, both approved in chat.

**The finding that drove everything.** The Final riddle tab's calendar used a uniform 3-day slot,
which meant a date *was* a position — `(date − start) ÷ 3 + 1` — so one dated ticket excluded every
other card from that slot. That arithmetic carried most of the deduction. Variable stay lengths
destroy it: a date then only orders the dated props among themselves. The 3-day clue set was
re-run under the weaker semantics and **collapsed to 18+ answers over 400,000+ valid calendars**.
The clue set was therefore rebuilt to be **purely ordinal** — the order is carried by what Liv
writes, not by arithmetic on dates. That is what frees the stay lengths to vary. The slot grid and
the "every stated gap is a multiple of 3 days" rule are both retired.

**Built:**
- `NorseBackpack/Tools/final_riddle_solver.py` (new) — constraint solver over the 22 cards and 22
  sequence positions. Places cards slot-by-slot so ordering clues prune immediately.
- `NorseBackpack/Tools/final_riddle_clues.py` (new) — the itinerary and the live clue set; run it
  to re-check the endgame. This is the solver check `PZ-18` had listed as "not started".
  Current run: **TEST 1 unique answer PASS, TEST 2 bundle gates PASS (3 answers without it),
  TEST 3 NOT RUN (geometric), TEST 4 rules hold PASS.**

**Decided and recorded (Final riddle tab):** a 2 Feb → 15 Dec travel year, 22 stops, variable
stays (2–7 nights), 94 nights away across 309 days. First appearances land at positions 1, 4, 6, 8
— Leif, Rollo, Aud, Harald — so the code still reads 1972. Full itinerary table, full clue table
with load-bearing marks, and the four museum-ticket dates (2 Feb / 17 Mar / 13 Apr / 28 Apr) are
all in the tab.

**Season check — the move fixed four already-built cards.** H1 Oslo's "a whole week in Oslo" is
now a true 7 nights instead of contradicting the 3-day slot; LD Brattahlíð's "green against the
ice" moved from March (Greenland is white) to June; L3's aurora sits in February; H5's gelato in
August. One card could not be rescued and was changed instead — see below.

**Changed:** `NorseBackpack/Postcards/build_postcard_L2_pdf.py` — "walked past my tent" →
"walked past the cabin". Battle Harbour is boat-access and shut in winter, and the itinerary puts
it on 10 February. Positions 1–3 are locked to Leif by printed card text, so the journey starts
when Leif starts and the leg could not simply be moved to summer. Rebuilt both PDFs and the
gallery back PNG; joke unchanged.

**Two solver results worth not rediscovering:**
- *Individually redundant clues are not jointly redundant.* Six clues each tested as droppable
  alone; removing all six together took the answer count from 1 to 8. Never prune the clue table
  on drop-one results.
- Two clue-set shapes were tried and **rejected on evidence**: moving Rollo's closing clue into
  the bundle as a dated receipt (17 answers — a date pins R6's position but not its rank, so
  R3–R5 can still follow it), and resolving Harald's tail from the bundle alone with no added card
  clause (6 answers).

**Files changed:**
- `NorseBackpack/Tools/final_riddle_solver.py`, `final_riddle_clues.py` (both new)
- `NorseBackpack/Postcards/build_postcard_L2_pdf.py`, `Postcard_L2_Battle_Harbour_Back.png`
- `output/pdf/Postcard_L2_Battle_Harbour_{Print,Letter_Print}.pdf`
- `NorseBackpack/Norse_Brainstorm.html` — Final riddle tab: section 2 replaced with the itinerary
  and clue set, ticket/statement panels rewritten, constraint worksheet resolved, Validation
  section now records the run. `PZ-18` and `PZ-08` updated; `PZ-05`'s quoted L2 message synced.
  Story tab's "Dates remain open" replaced. **CSS fix:** `.pill` was scoped to
  `#design/#system/#questions/#options/#puzzles/#story` and never `#final-riddle`, so pills in
  that tab had been rendering as unstyled text all along; `#final-riddle` added to all five rules.

**Checks run:** solver run in-repo (results above). L2's rebuilt back page rendered to PNG and
inspected — text reflows correctly, layout and Fun Fact box unaffected. Page served over
`http://localhost:8734` and inspected visually: Final riddle tab renders, 3 tables with 22/19/4
data rows, no console errors, decoy and pass/not-run pills styled correctly after the CSS fix, 0
broken `#view-` links, `PZ-18` renders with its closed items struck through. A stale browser cache
masked the CSS fix on first reload — a `?v=` cache-buster was needed, same trap as an earlier
session.

**Blockers / open questions:**
- **Validation test 3 is still unrun** and needs the map projections, not the solver: no
  decoy-inclusive answer may draw a plausible digit. It is in direct tension with the Guessing
  risks section, which wants each decoy to draw a *plausible* wrong digit so the shape cannot be
  eyeballed off the map. One of the two has to give — a real design decision, not a check.
- The per-card crest/logo element mark is still the one thing blocking the endgame, and all 22
  cards need a re-print for it. That pass is where the marks should land.
- Per-card element-mark assignment (22 of them) remains the one thing blocking the endgame.
- A1, A3, AD and H6 are still unwritten; their clue text is specified in the Final riddle tab.

**Next action:** decide the per-card element-mark assignment (which of the 3 symbol / 6 crest
elements sits on each of the 18 real cards), since that is what still blocks the endgame, and
settle the test-3 vs. Guessing-risks contradiction above.

## Addendum 2 — same session — three visuals added to the Final riddle tab

Requested: a timeline of events, a timeline of cards beneath it, and a per-leg map with numbered
stops and the decoys highlighted. All three are now section **2c - At a glance** in the Final
riddle tab, as static inline SVG generated from the itinerary data by
`NorseBackpack/Tools/build_final_riddle_visuals.py` (new). Re-run it after any date or stop
change so the drawings cannot drift from the table above them.

**What was built:** (1) 22 stops on one dated line, coloured per trail, decoys hollow/dashed,
labels staggered over three rows; (2) the same axis split into four trail lanes, showing the
interleaving; (3) four leg panels, numbered in travel order, north-up Web Mercator at uniform
scale per panel, with the real route solid and the decoy-inclusive route dashed.

**Two findings that came out of drawing it — both worth acting on.**
- **Harald's 2 is confirmed broken.** The H3 -> H4 leg runs back up and to the left, so the
  figure reads as a zigzag with a spike. `PZ-09` had flagged the risk; the panel now shows it.
- **Two decoys do not do their job.** Constantinople sits almost on the line between Sicily and
  Patara, and Brattahlid only adds a hook to the end of Leif's stroke. Both pass validation
  test 3 trivially (neither draws a rival digit) but both fail what Guessing risks asks of a
  decoy: making an unfiltered trace visibly wrong. As drawn, a team that never solves the crest
  filter still traces a usable 1 and a usable (if broken) 2. Aud's and Rollo's decoys do distort
  their shapes properly.

Also recorded: Rollo's 9 is the strongest shape, and it works *because* Roumare lands 3.6 px from
Rouen so the loop closes - the same near-coincidence that killed the pin-and-cord idea. Leif's 1
is effectively a two-point line (L1/L2 are 7.6 px apart on a 224 px trail), so Leif's trail
carries almost no shape information. Aud's 7 reads but its descender is vertical, not slanted.

**A labelling detail worth keeping:** dots are drawn at their true projected position and only
the number badges are pushed apart, with a leader line back to the dot. Rouen/Roumare at 3.6 px
and L'Anse/Battle Harbour at 7.6 px made the badges unreadable otherwise, and moving the dots
themselves would have falsified the shape.

**Known limitation:** the card-lane chart plots the date each card was *sent*, not the order
players receive them. In-game release order is `PC-18` and is still open - Rollo's three puzzles
have no internal order, so a release-order version cannot be drawn without inventing one. Said so
on the page rather than guessing.

**Files changed:** `NorseBackpack/Tools/build_final_riddle_visuals.py` (new),
`NorseBackpack/Norse_Brainstorm.html` (section 2c plus `.legmaps` grid CSS).

**Checks run:** page served over `http://localhost:8734` - 6 SVGs, 4 map panels, exactly one 2c
block (the injector is idempotent), no console errors, 4-column grid at desktop and single column
at 375 px with no horizontal scroll. Each map inspected visually at full size. A temporary
standalone check page was used to work around a pane compositing issue that returns blank
screenshots low down this very tall page; it was deleted afterwards.

## Addendum — same session — the five clauses applied

Applied and rebuilt, after the write-up above. **Solver re-run: TEST 1 unique answer PASS,
TEST 2 bundle gates PASS (3 answers without it), TEST 4 rules hold PASS.** The answer is
unchanged: Leif L1-L2-L3, Rollo R1..R6, Aud A1-A2-A3, Harald H1..H6, first appearances
Leif/Rollo/Aud/Harald.

**As printed:**
- **R1 Chalus** - "Odd place to start his family's story, at the very end of it, but this is
  where I began."
- **R2 Rouen** - "The tapestry towns are still ahead of me - saving those for later."
- **R6 Roumare** - "The last of Rollo's places on my list, and I've ended up right back beside
  Rouen to finish."
- **H1 Oslo** - second sentence now "It's Harald's city and the obvious place to begin with him
  - so much Viking history."
- **H4 Hedeby** - opening now "New stop: Hedeby - saltwater again, after all that river country.
  Barely a Hedeby left to stand in: a green ring of earthworks where the ramparts ran."

**Two layout constraints found, worth knowing before any further card text is added.** Message
panels were measured against the real font metrics before editing rather than after.
- **R2 is the tightest card in the deck** - about one spare line. It also carries the word-lock
  reading order (`PZ-15`), so the new sentence was placed after all six Saxon words and uses none
  of them; fight -> forest -> cow -> people -> poultry -> inn is unchanged.
- **H4 tops out at ten message lines.** It draws the branch-rune key table below the signature,
  and `table_bottom` clamps at `max(30, ...)`, so an eleventh line pushes the table's caption
  outside its own box. First attempt did exactly that (caption baseline 28.2 vs box bottom 30);
  the paragraph was tightened by a few words instead of moving the table.

**Files changed in the addendum:** `build_postcard_{R1,R2,R6,H1,H4}_pdf.py`, their ten
`output/pdf/Postcard_*_{Print,Letter_Print}.pdf`, their five `Postcard_*_Back.png` gallery
images, and `NorseBackpack/Norse_Brainstorm.html` (`PZ-05` records the exact printed wording and
both layout limits; `PZ-18` moves the five edits to its closed list; the clue-set note in the
Final riddle tab now reads as applied).

**Checks run:** all five backs rendered to PNG at 3x and inspected individually - no overflow,
H4's rune key box intact with its caption inside, R2's signature clear of the credit line, all
Fun Fact boxes unaffected. Page re-served over `http://localhost:8734` (cache-buster again): no
console errors, 0 broken `#view-` links, 0 unrendered HTML entities, 11 tabs, 3 tables in the
Final riddle tab, `PZ-05` and `PZ-18` both render.

## Session Close — 2026-09-18 (later) — Aud's treasure hunt designed: route, mechanic and code

**Task:** the user asked for a full adventure to go with the finished map, then chose **A1** for the
mechanic and asked to move the road up to the northern church.

**The mechanic is A1, in a refined form.** The three digits are **bridges, fords and gates** rather
than the abstract water/barrier/junction categories originally proposed — three visually distinct
symbols a player counts on the sheet, so nobody has to know that a ditch counts as a barrier.
Keyspace ~1000 against A2's 35.

**The route was found, not invented.** The layer was turned into a graph (nodes = junctions, dead
ends and landmarks sitting on a track; edges = the stretches between, carrying what they cross) and
every seven-leg walk ending at a cave was enumerated.

| leg | from -> to | crosses |
|---|---|---|
| 1 | northern chapel C2 -> second chapel E3, road 218pt | 1 bridge |
| 2 | -> well B5, road 328pt | 2 fords, 1 bridge |
| 3 | -> landing C6, road 88pt | 1 bridge |
| 4 | -> standing stone H5, road 408pt | 1 bridge, 1 ford |
| 5 | -> second standing stone H7, road 122pt | 1 gate |
| 6 | -> cairn H9, road 123pt | 1 bridge |
| 7 | -> ruin I9, road 106pt; cave 23pt on, in the wood | nothing |

**Code `531`** — 5 bridges, 3 fords, 1 gate. Treasure is the cave in the wood beyond the ruin.

**Road extended to the chapel.** Its head sat 31pt short, which left the northernmost church
unusable as a route step and forced a weaker route scoring `301` (a zero digit, and two legs
stumbling through junctions in the same grid square). Extending the road beat adding a connector:
fewer features, and the chapel becomes a fork where the road meets the footpath already starting
there. New head **(172.25, 672.35)** — 12pt from the chapel, 26.3pt from the Dogurdarnes pin.
Drawn straight at the chapel it would have passed 13.9pt from that pin, inside the 19pt rule, so it
approaches from the south-east.

**The deliberate ambiguity is leg 5 and it is genuine.** H5 is a four-way junction: one road runs
on to a second standing stone (the route, `531`), another drops through a gate toward a well and a
different cave, scoring `432`. Both are fully walkable, so a wrong reading gives a wrong code rather
than a stuck player.

**Found while writing this up:** `PZ-17` still contained the **old seven-leg route table** from the
shelved split-panel sheet (old ford / watermill / falls / sheepfold / ruined chapel / cairn /
standing stone, plot-number code `467`). It sat directly after the new route and contradicted it.
Marked superseded in place rather than deleted, since the two design rules argued above it are still
worth keeping.

**Also established:** card **A2 has front art only** — no back, no print PDF — so its drafted
"inland among birches" chapel line is free to change, and it must, because the wood chapel at E4 is
14.5pt off the network and can never be a route step. And **Aud's museum ticket does not exist**
(the built `Museum_Ticket` is L'Anse's), so the seven-row form is free; the row count survives by
coincidence. The ticket gives **directions only** — listing the crossings would leave nothing to
solve.

**Files changed:** `NorseBackpack/TravelMap/aud_features.json` (road extended);
`NorseBackpack/Norse_Brainstorm.html` (`PZ-17` carries the mechanic, the leg table, the code, the
road extension, the ambiguity, the A2 supersession and the ticket design; old route table marked
superseded; pill now "Route, mechanic and code decided; A2 rewording open").

**Checks run:** re-audited the layer after extending the road — section D still clean (0 over
water, 0 segments crossing water, 0 under 19pt from a pin, 0 icon collisions) and the crossing
counts unchanged at 14 water / 11 barrier. Re-ran the route search on the updated layer and
confirmed the `531` route now starts at the chapel. Tag balance checked inside the `PZ-17` block;
served over `http://localhost:8734` and read the rendered leg table back from the DOM, matching the
intended seven legs, with no console errors.

**A2's replacement line, written 18 Sept 2026:** *"The only place it caught me out was the standing
stone — two roads leave it southward through the same gate, and I took the one that runs on into
the trees. Wrong, of course. It's the open one you want."* The rest of the card is untouched.

Every clause is checkable on the sheet: both roads leave the stone **south**, both cross **wall
#81**, and their crossing points are 11 and 12 pt from the stone — close enough that they **share
one gate symbol**, so the gate distinguishes nothing. That is precisely why an in-person detail is
needed here. The only visible difference is where each road ends: the wrong branch finishes
**inside a wood**, the route's branch in open ground. The card names that and nothing else — not
the destination, not the count, not the code. The wrong branch picks up a second gate at I5 and
scores `432`.

**Two more stale blocks found and marked superseded in `PZ-17`:** the shelved split-panel vignette
spec, which still called the birch icon "load-bearing" for telling the two chapels apart (it is not
— the ambiguous hop is the fork at the standing stone now), and the cross-reference that still
sent readers to the birch hollow.

**Aud's museum ticket is built** — `NorseBackpack/Props/AudTicket/build_aud_ticket_pdf.py`,
outputs `Aud_Ticket_Print.pdf` (3 pages: front, back, answer copy) and `Aud_Ticket_Letter_Print.pdf`
(2-up with crop marks). Same 2x5.5 in stock, palette, header band and outer rule as the L'Anse
ticket. Unlike L'Anse's it has **no ImageGen art** — both faces are vector, so wording changes cost
nothing to re-render.

Front: AUDAR SAFN / Treasure Museum / Hvammur, Dalir, admit-one, "admission incl. treasure hunt",
and a rust roundel standing in for a crest that has no asset yet. Back: the seven legs, one per row,
three tally boxes each, totals blank, row 1 pre-filled in purple as the worked example, and a footer
spelling out BRG/FRD/GTE. Page 3 is an answer copy with every box filled and `ANSWER 5 3 1`.

Two guards in the build: leg text is measured and wrapped before drawing, so a longer direction
raises instead of silently overflowing the card; and an `assert` ties the per-leg answers to the
printed total so they cannot drift.

**Caught in the first render:** the stub number read `No. 531-A` — the answer, printed on the front
of the ticket. Now `No. 209418`, deliberately unrelated.

**The layer reaches paper.** `TravelMap/aud_layer.py` (new) draws `aud_features.json` onto the
sheet; `build_trail_maps_pdf.py` calls it over the coastline but under the grid, the stop pins and
every label, clipped to the map area. Appearance is ported from the designer and the two share no
source, so a symbol changed in one must be changed in the other.

**Aud's frame is now ZOOM_FRAME** (-22.9751..-20.5451, 64.08..65.37). It had to be: the export
stores page points, not coordinates. `assert_frame()` compares the export's frame with the sheet's
on every build and fails loudly rather than printing a sheet whose coastline has slid out from under
its symbols.

**Decorative labels re-set:** Breidafjordur moved out into the bay (65.34, -22.33) after running off
the west edge; Snaefellsnes and DENMARK STRAIT dropped, both projecting well off this sheet. Still
correct for the old wide frame if it is ever restored.

**Two toolchain gaps the first printed sheet exposed, both fixed:**
- `export_aud_base.py` fed the designer only the research corpus, not the sheet's own
  `extra_towns` — so the designer knew **6 town dots while the sheet prints 13**, and its 19 pt
  clearance check never covered Budardalur, Akranes or Stykkisholmur. Symbols were drawn over them.
- The exporter never mentioned the two boxes the sheet reserves for the **scale bar and compass
  rose**, so symbols were being placed underneath both.
Both are now exported; the designer draws the reserved boxes faintly and a new scorecard row
**In a reserved box** counts them. The layer was re-cleared: 4 point symbols moved, largest 16.5 pt,
crossing markers rebuilt. **Brief now 19/20 with section D clean.**

## Session Close — 2026-09-18 (later) — Sheet legibility pass

The first printed sheet read as busy and under-styled. Six fixes:

- **Converging roads now merge.** Each road drew its own casing then its fill, so the next road's
  casing sliced across the previous one's carriageway - four roads meeting printed as a braid.
  Roads now draw in **two passes**, every casing then every fill.
- **Bridges, fords and gates are oriented** to what they cross: a bridge or ford along the route it
  carries, a gate in the line of its wall, angles normalised so nothing prints upside down.
- **Grid steps back** on Aud's sheet only: `#D9CDB2` at 0.3 pt against `TAN` at 0.45.
- **A legend** at (40, 95), 160x200 pt in the clear water bottom-left, listing only the symbols
  actually present; its box is reserved so labels route around it. `FAXAFLOI` moved to
  64.242, -22.108 because it printed across the key.
- **Two self-intersecting polygons repaired** (wood I10, moor H11 - the "broken forest"). 2-opt
  reversal, so vertices are unchanged and only their order is rewritten. **The moor's outline moved
  up to 95 pt** and is meaningfully a different shape than drawn - worth a look before print.
- **Stykkisholmur plotted 16 pt (3.4 km) out to sea**, same coarse-coastline cause as Dogurdarnes.
  Added to `PLOT_NUDGE` at (-0.0324, -0.0480), measured; the nudge now applies to town dots as well
  as stops. Compass reservation gained 14 pt of headroom - a village was printing over its "N".

**Density, measured:** 89 point symbols, mean 1.8 per occupied cell, only 2 cells with 4+. The count
is fine; all 89 being the same purple at the same weight is what makes it read busy. A tone problem,
not a deletion problem.

**Shipped PDFs rebuilt** once the viewer lock cleared. Both `Trail_Map_3_Aud_Print.pdf` and
`..._ANSWER.pdf` now carry the pass — verified 612x792, legend present, Stykkisholmur ashore, and
the answer copy still reading as the digit 7.

**Left for Codex:** area fills (marsh, wood, moor are flat tints where they want texture), the
visual hierarchy, and the `bridge` glyph - now that it rotates correctly it reads awkwardly side-on
and would be better as two abutment strokes than an arch. **The symbol vocabulary lives in two
places with no shared source** - `Aud_Map_Designer.html` (SVG) and `aud_layer.py` (ReportLab) - so
any restyle must change both or the designer and the print will disagree. That belongs in the brief.

**State of Aud's leg is now recorded in `PZ-17`**, not here: a summary table of map / route / code
/ card / ticket / designer with links, the two cosmetic loose ends (the moor at H11 is not the shape
it was drawn, and the cave at I9 is half-clipped by the map edge), and the outstanding verification.
Per AGENTS.md the backlog lives in the project page; this file keeps continuity only.

**Next action:** print a test sheet and walk the seven legs by hand against the ticket. The tally of
5 bridges, 3 fords and 1 gate is confirmed in the routing graph and has never been checked by eye on
paper. Nothing else should be built on top of `531` until it passes.

**Blockers / open questions:**
- A2's replacement wording is undecided; the requirement is fixed, the words are not.
- Which coin pile the cache mark names, for `PZ-03`'s weighing step.
- `aud_features.json` is still not read by `build_trail_maps_pdf.py`, so none of this reaches paper.
- The printed sheet still uses the shipped wide frame while the designer uses `ZOOM_FRAME`.
- Four decorative labels still fall outside the zoomed frame.
- Brief scores 17/19; the two reds (3 crossings sharing a grid cell, 8 stranded landmarks against a
  5-7 range) were judged not worth redrawing for.

## Session Close — 2026-09-18 — Dogurdarnes plotted ashore; sea-check added to the build

**Task:** the user asked whether it was normal that stop 1 sits in the sea. It was not.

**Measured:** Dogurdarnes sat **12.1 pt / 2.6 km** from the coastline — about 4 mm off the shore at
print size. An earlier note in this session blamed Natural Earth resolution for both this and
Bjarnarhofn; that was right for Bjarnarhofn (0.7 km) and **wrong for this stop**, and has been
corrected in `PZ-17`.

**Cause:** `TravelMap/vendor/land.js` is Natural Earth **50m** (1:50 million), generalised to a few
km. Fine on the other three sheets; Aud's is zoomed to 211 m/pt, where it is not. Dogurdarnes is a
headland in Breidafjordur and at 1:50m its peninsula does not exist. `stops.js` already flags the
coordinate `uncertain`, "represents the peninsula, not an exact landing".

**Decision (user chose option 2 of three):** nudge the plotted position, keep the real coordinate.
Re-vendoring `ne_10m_land` was declined.

**Built:**
- `PLOT_NUDGE` in `build_trail_maps_pdf.py` shifts the drawing only; `stops.js` untouched. The stop
  must move 2.6 km to reach any land, so the shift is necessarily large: **3.5 km NE, 900 m
  inshore, ~16 pt** on the zoomed sheet.
- **Effect on the digit 7, measured before committing:** top bar 150.8 -> 138.9 pt (8% shorter),
  angle **+9.3 -> +4.9 deg**. An improvement; a flatter top stroke reads more like a 7. The
  descender is untouched and the grid refs still read **B2, E2, E10**.
- `plot_nudge()` is shared with `export_aud_base.py`, which reads the plan directly — without it
  the sheet was fixed while the designer still drew the stop at sea. Caught during verification.
- **A stop-in-the-sea check.** The old assertion only asked whether a stop lands on the *page*,
  which a stop in the water passes. Stops are now tested against the coastline and reported **in
  points as well as km**, since 8 km is 2 pt on Leif's 500 km sheet and invisible. It immediately
  found two more: **Battle Harbour** (8.2 km, **2.0 pt**) and **Patara** (1.8 km, **0.4 pt**) —
  both invisible at those scales, both left alone.

**Checks run:** all four sheets rebuilt; Aud reports no sea NOTE; `aud_base.js` regenerated and all
three stops verified ON LAND by point-in-polygon against the exact drawn polygon; the Aud ANSWER
sheet rendered at 140 dpi and the stop-1 area cropped at 420 dpi and inspected — the pin sits
clearly on the headland. Page sizes confirmed 612x792 for all four. Artifact republished (version
4) so the hosted designer carries the corrected `aud_base.js`.

**Side effect, a good one:** rebuilding replaced `output/pdf/Trail_Map_3_Aud_*.pdf`, which had been
stuck as the rejected **landscape two-panel** version since the file was locked by an open viewer.
That blocker is now closed.

**Left uncommitted, deliberately:** `NorseBackpack/Norse_Brainstorm.html` carries someone else's
live edit from today — the comb grille lock gaining a candidate answer `BOOK`, with the comb now
planned as 3D-printed. My `PZ-17` note about this fix is in the same file. Both are on disk and
correct; the file was left for its author to commit rather than folded into a commit of mine. Also
still uncommitted: the eight `output/pdf/_*.png` scratch renders.

**Next action:** unchanged — continue the map southward against the brief. Fix the road's last
vertex (10.5 pt from the Hvammur pin), join the two paths through the ditch, draw the watercourses
early, then use "Place crossings".

**Blockers / open questions:** lock mechanic still undecided (A/B/C/D, A recommended, A1 vs A2
open); labels stay empty by design; `aud_features.json` still holds the superseded first layer and
is not read by `build_trail_maps_pdf.py`; the printed sheet still uses the shipped **wide** frame
while the designer uses `ZOOM_FRAME`; and the four decorative labels still fall outside the zoomed
frame.

## Session Close — 2026-09-17 (latest 9) — Pinch-zoom fix: the action bar was sliding off screen

**Task:** the user reported that zooming in Pan mode pushed the Pan button and the rest of the
action bar off screen.

**Cause.** Pan mode set `touch-action:auto`, which let the browser zoom the whole page. Page zoom
shrinks the visual viewport *inside* the layout viewport, and `position:fixed` is pinned to the
layout viewport — so the bottom-pinned bar went with it. General lesson worth keeping: **a
bottom-pinned bar and browser page zoom cannot coexist.**

**Fixed in `NorseBackpack/TravelMap/Aud_Map_Designer.html`:**
- Pan mode now uses `touch-action:pan-x pan-y`: scrolling still works, browser zoom cannot happen.
- **Pinch drives the designer's own zoom control**, so the sheet scales while the interface stays
  put. Two-finger drag pans in the same gesture, so a zoomed-in map no longer needs Pan mode.
- **The map pane is the scroll container on mobile** (`max-height:58dvh; overflow:auto`) rather
  than overflowing the document, so a pan scrolls a known element. It shrinks to the sheet and
  only scrolls once the sheet is taller than 58dvh.
- **Touch taps commit on `pointerup`, not `pointerdown`.** The first finger of a pinch was landing
  a symbol before the second arrived. Mouse input is unambiguous and still acts on pointerdown.
- The bar additionally follows `window.visualViewport` as a fallback for a page zoom this code
  cannot prevent (OS accessibility zoom, desktop browser zoom). Guarded to no-op unless the visual
  viewport is genuinely offset or scaled, so it can never itself misplace the bar.

**Checks run:** `node --check` after each patch — clean. At 375x812 with synthetic
`PointerEvent`s at `pointerType:'touch'`: a two-finger spread from 80 px to 200 px took zoom 50% ->
130% and **placed nothing** (count stayed 15, confirming the deferred-tap fix); sliding both
fingers 80 px left scrolled the stage exactly 80 px with zoom unchanged; the bar stayed
`position:fixed` with an empty transform throughout; a single tap still placed a cairn at E5 and
Undo removed it; Pan mode reports `touch-action: pan-x pan-y` and draw mode `none`. At fit the
stage is 404 px around a 396 px sheet with no scroll and no dead space; zoomed to 150% it caps at
469 px and scrolls both axes; the Fit button returns to 50%. Desktop regression at 1050 px: bar
static, 3-column palette, 120% zoom, mouse still places on pointerdown, Undo works, score 6/19, no
console errors anywhere.

**Measurement caveat:** the in-app browser's mobile emulation reports `innerWidth/innerHeight` as
the pane's real size (931x2016) while `documentElement.clientWidth/Height` correctly report
375x812, and document-level horizontal scrolling does not work there at all. That is what pushed
the design toward scrolling the stage element instead of the document — which is the better
design anyway, but it means `position:fixed` offsets could not be verified numerically in the
emulator. The logic is standard and the guard makes it inert unless a real zoom occurs.

**Published:** artifact version 3 at https://claude.ai/artifact/26d6YkdDjuSkN2WS5Uc2fL

**Next action:** unchanged — the user continues the map southward against the brief. Fix the
road's last vertex (10.5 pt from the Hvammur pin), join the two paths through the ditch, draw the
watercourses early, then use "Place crossings".

**Blockers / open questions:** unchanged — lock mechanic still undecided (A/B/C/D, A recommended,
A1 vs A2 open); labels stay empty by design; `aud_features.json` still holds the superseded first
layer and is not read by `build_trail_maps_pdf.py`; the zoomed frame is exporter-only; four
decorative labels fall outside it; and `output/pdf/Trail_Map_3_Aud_*.pdf` are still the rejected
landscape version — run `python NorseBackpack/TravelMap/build_trail_maps_pdf.py aud`.

## Session Close — 2026-09-17 (latest 8) — Everything committed and pushed; designer made mobile-friendly

**Task:** commit and push the session's work, publish the Aud map designer online, then make it
usable on a phone.

**Committed and pushed** (`b810aae..5e708fb` on `main`), five commits:
- `2786160` Aud map designer, `aud_base.js`, `export_aud_base.py`, `aud_features.json`, portrait
  rebuild of the trail maps, shelved split panel under `Drafts/`
- `595c554` postcards H1-H5, HD, R1, R6, RD plus refreshed L1/L2/R2
- `09303ce` final-riddle tooling under `NorseBackpack/Tools/`
- `b620ac2` `PZ-17` build brief and handoff
- `5e708fb` mobile support for the designer

**Left uncommitted on purpose:** eight scratch QA renders in `output/pdf/` (`_H1_Oslo_p0.png`,
`_harald_print_preview.png` and similar). Referenced by nothing, and no `_*.png` has ever been
tracked. Flagged to the user rather than added.

**Published:** https://claude.ai/artifact/26d6YkdDjuSkN2WS5Uc2fL — private to the account,
`index.html` plus `aud_base.js`. Now at version 2 with mobile support. Republish to that same URL
after any change to the local designer; publishing without the URL would create a second artifact.

**Mobile work, in `Aud_Map_Designer.html`:** the tool was mouse-only — touch could tap but not
drag — and the sheet rendered 734 px wide on a 375 px screen.
- Pointer events replace mouse events. `touch-action:none` on the SVG keeps a drag inside the app
  instead of scrolling the page; a **Pan** toggle switches it back to `auto` when the map needs
  moving.
- Vertex handles gain an invisible 9 pt hit disc behind the visible 2.2 pt dot.
- An action bar (Finish line, Undo, Delete, Fit, Pan) sits in the Tool card on desktop and pins to
  the bottom of the viewport below 780 px. `undo()` and `deleteSelected()` were extracted from the
  keydown handler so both entry points share them.
- Fit-to-width zoom, automatic below 780 px; the zoom floor dropped 60% -> 30%.
- The readout updates on tap as well as move, so a touch draft shows its point count.

**Two pre-existing bugs found while testing, both fixed:**
- **Nine invalid `font:` shorthands.** `font: 11px/1 inherit` is invalid — `inherit` is a CSS-wide
  keyword, legal only as a whole value, never as one component of a shorthand — so Chrome dropped
  each declaration and used its own defaults. The header was rendering at 26 px instead of 14, and
  buttons at 13.3 px instead of 11, **on desktop as well**. Replaced with longhand.
- **The mobile media query had no effect.** It was written beside the layout rules it belonged
  with, but a media query adds no specificity, so the later component rules won every tie. Moved to
  the end of the stylesheet. Worth remembering for any future block in this file.

**Checks run:** `node --check` after each patch — clean. At 375x812: no horizontal overflow
(`scrollWidth` 375 = `clientWidth`), 4-column palette, bar fixed, auto-fit to 50% giving a 306 px
sheet. Computed styles verified after the font fix (h1 13 px on mobile / 14 px desktop, tool
buttons 12/11, family correctly IBM Plex Mono). **Touch interaction tested with synthetic
`PointerEvent`s at `pointerType:'touch'`:** tap placed a cave at D6; a touch drag moved it to F7
with `defaultPrevented` true, confirming the page scroll was suppressed; Undo reverted the drag and
then removed the cave; the Pan toggle flipped `touch-action` none <-> auto; three touch taps plus
the Finish button committed a 3-point footpath; the readout showed "1 pts" then "2 pts" on taps.
Desktop regression checked at 1050 px: bar static, 3-column palette, 120% zoom, long hint shown, no
console errors. All test data removed and the user's 15-feature state restored in browser storage.

**Next action:** unchanged — the user continues drawing the map southward against the brief. Fix
the road's last vertex (10.5 pt from the Hvammur pin), join the two paths through the ditch, draw
the watercourses early, then use "Place crossings".

**Blockers / open questions:** unchanged — lock mechanic still undecided (A/B/C/D, A recommended,
A1 vs A2 open); labels stay empty by design; `aud_features.json` still holds the superseded first
layer and is not read by `build_trail_maps_pdf.py`; the zoomed frame is exporter-only; four
decorative labels fall outside it; and `output/pdf/Trail_Map_3_Aud_*.pdf` are still the rejected
landscape version — run `python NorseBackpack/TravelMap/build_trail_maps_pdf.py aud`.

## Session Close — 2026-09-17 (latest 7) — Aud map rebuild reviewed; 5 symbols and crossing automation added

**Task:** the user started redrawing Aud's map against the brief and pasted the first 15 features
(grid rows 1–2 only) asking whether it was better, then asked two questions and requested three
new symbols.

**Verdict on the new map: yes, markedly.** Measured on rows 1–2 only, so ratios matter, not totals:

| | old map, whole sheet | new, rows 1–2 |
|---|---|---|
| landmarks inside an area | 0 of 29 | **3 of 8** |
| landmarks on a route (<=8pt) | 5 of 29 | **5 of 8** |
| routes through an area | 0 | **1** |
| confusable pair split by context | churches only | **stone x2** (wood vs shore) |

Section D clean apart from clearance. The Port marker sits 0.1 pt off the coastline.

**Three faults reported to the user:**
- Road's last vertex `(281.15, 662.4)` is **10.5 pt from the Hvammur pin** and 17.3 pt from
  Krosshólaborg; the vertex before is 18.8 pt. Suggested ending near `(268, 657)`.
- **The bridge was a gap, not a crossing.** Path A ended 7.5 pt short of the ditch, path B started
  2.4 pt short on the far side, 12.5 pt apart, bridge sitting between. Nothing crossed anything:
  zero barrier crossings and a broken network.
- **No water drawn yet**, and water crossings carry the largest target (5+). Advised drawing
  watercourses early, while the tracks are still soft.
- Also flagged: stranded landmarks now 0 (the opposite of the old map's 7 — target is 5–7), and
  density at 1.9 features/cell against the old map's 0.9, projecting to ~128 features.

**Answers to the two questions, both recorded in `PZ-17`:**
- *Should roads avoid settlements?* The rule is about **labels, not roads**. A road serving a
  village is correct cartography; 19 pt exists only because the build's label placer cannot see
  designer geometry. Keep 19 pt for now, end routes at the outskirts; relax once the export feeds
  the build and the placer reserves designer features — except Hvammur/Krosshólaborg, 8.5 pt
  apart, which can never be threaded.
- *Draw continuous routes and let the tool place bridges?* **Yes** — built it.

**Built in `NorseBackpack/TravelMap/Aud_Map_Designer.html`:**
- Five new symbols: `port` (anchor), `village` (three gables, distinct from the single-house
  `farm`), `cave` (solid arch in a hillside), `ford` (stones between bank ticks), `gate` (two
  posts, two bars). The palette, renderer and exporter all read from `SYMBOLS`, so adding the
  entries was enough.
- **"Place crossings" button** — scans every track x obstacle intersection and inserts the right
  symbol on it: river->bridge, stream->ford, ditch->bridge, hedge/wall->gate. Skips any crossing
  already marked within 10 pt (safe to re-run), pushes undo, reports a tally.
- New scorecard row **"Crossings with no symbol"** (target 0) for the reverse case.
- **Crossing markers excluded from landmark metrics.** `bridge`/`ford`/`gate` no longer count
  toward landmarks-on-a-route, inside-an-area, stranded, or confusable pairs. The old map's
  "5 landmarks on a route" was really 2 landmarks plus 3 bridges. Scorecard is now out of 19.

**Checks run:** `node --check` on the extracted script after each patch — clean (caught one real
bug: the undo helper is `push()`, not `pushUndo()`). Rendered all five new glyphs side by side at
260% zoom and inspected — each is legible and distinguishable from the existing set and from each
other. **Crossing automation tested both ways:** with the user's map as-is it correctly reported
"No route crosses an obstacle yet — draw the line straight over it"; after joining the two paths
into one continuous line over the ditch and adding a test stream and hedge, it placed a ford at
`(300.0, 727.4)` and a gate at `(350.0, 734.3)` — both exactly on the intersections — and
correctly skipped the ditch because the existing bridge was within 10 pt. "Crossings with no
symbol" then read 0. Fixed one cosmetic bug found in testing: `save()` was overwriting the tally
message, so the status line is now written after `save()`. No console errors throughout. All test
data removed and the user's 15-feature state restored in browser storage.

**Next action:** user continues the map southward. Fix the road's last vertex, join the two paths
through the ditch, draw the watercourses early, then use "Place crossings".

**Blockers / open questions:** unchanged — the lock mechanic is still undecided (A/B/C/D, A
recommended, A1 vs A2 open); labels stay empty by design, though the user has one labelled
`marker` reading "Port" (flagged as fine for a start anchor, not as a pattern); `aud_features.json`
still holds the superseded first layer and is still not read by `build_trail_maps_pdf.py`; the
zoomed frame is exporter-only; four decorative labels fall outside it; and
`output/pdf/Trail_Map_3_Aud_*.pdf` are still the rejected landscape version — run
`python NorseBackpack/TravelMap/build_trail_maps_pdf.py aud`.

## Session Close — 2026-09-17 (latest 6) — Designer label fix and live build-brief scorecard

**Task:** the user reported overlapping labels in `Aud_Map_Designer.html` (screenshot showed
Dögurðarnes and Hvammur double-labelled, Krosshólaborg on top of Hvammur) and asked for the build
brief's targets to appear on the designer page as a design aid.

**Cause of the overlap.** Dögurðarnes and Hvammur are each **both a stop and a town** in the
corpus, and the designer drew `B.stops` and `B.towns` naively, so two labels landed on one point.
Krosshólaborg then collided because it sits 8.5 pt from Hvammur. `build_trail_maps_pdf.py` already
solves this (dedupe by name, then a reserve/place pass), so the designer was showing a sheet the
printer would never produce.

**Fixed in `NorseBackpack/TravelMap/Aud_Map_Designer.html`:**
- `planBaseLabels()` / `findSpot()` — a reserve/place pass mirroring the build. Stop pins and town
  dots are reserved first, then stop labels are planned (so the more important label wins the good
  position), then towns, then area names. Eight candidate offsets per label; anything unplaceable
  is pushed to `droppedLabels` and named in the panel rather than silently lost.
- A town whose name matches a stop is labelled once, by the stop — same rule as the build.
- With the current 59-feature layer, **zero labels are dropped**.

**Built: a live Build brief panel.** The `PZ-17` brief's targets are now counted against whatever
is drawn, in the same four sections (A countable events, B navigable skeleton, C ambiguity engine,
D must not break), scored out of 18, each row green when met. Computation is debounced 140 ms off
the render path because crossing detection is O(n²) on segments and would otherwise run on every
drag frame. Two deliberate choices:
- **Targets where more is harmless are minimums** (`5+`, `3+`), not ranges. The first version
  flagged 11 forks as a failure against a "6–8" target, which is wrong for a design aid. Only the
  hard-zero rules and the stranded-scenery count are true ranges. `Norse_Brainstorm.html` was
  edited to match so the two cannot drift.
- **The land test carries 2.5 pt of slack.** A wall or track running down to the shore legitimately
  touches the coastline; without slack the stone wall showed as "over water" every time.

**Current score for the existing layer: 11 of 18.** Short on: water crossings (2, want 5+),
barrier crossings (2, want 3+), landmarks on a route (3, want 18+), landmark at a fork (0, want
3+), routes through an area (0, want 3+), routes alongside a line (0, want 2+), landmarks inside
an area (0, want 8+). All of section D is clean.

**Files changed:** `NorseBackpack/TravelMap/Aud_Map_Designer.html`;
`NorseBackpack/Norse_Brainstorm.html` (`PZ-17` records both changes; the eight range targets
became minimums).

**Checks run:** extracted the inline `<script>` and ran `node --check` — syntax clean. Served over
`http://localhost:8734` and inspected: no console errors, labels now read cleanly with none
dropped, panel renders all four sections. **Live update tested end to end** — clicked the Church
tool and placed one inside a wood: "Landmarks inside an area" went 0 → 1 and the placed count 59
→ 60; the score correctly fell 11 → 10 because that church also pushed stranded landmarks out of
its 5–7 range. Test placement undone with Ctrl+Z and the 59-feature state confirmed restored.
Cross-checked every panel figure against the independent Python analysis run earlier in the
session (crossings 2/2, forks 11, dead ends 12, stranded 7, inside-area 0) — all agree.

**Note:** a backup of the pre-patch designer is at
`<scratchpad>/Designer_backup.html` for this session only; it is not in the repo.

**Next action:** user redraws the map against the panel, aiming to turn section A, B and C rows
green while keeping D at zero. Then export and paste back for an independent re-measurement.

**Blockers / open questions:** unchanged from the previous entry — the lock mechanic is still
undecided (options A/B/C/D put to the user, A recommended, A1 vs A2 sub-choice open); labels stay
empty by design; `aud_features.json` still not read by `build_trail_maps_pdf.py`; the zoomed frame
is still exporter-only; four decorative labels still fall outside it; and
`output/pdf/Trail_Map_3_Aud_*.pdf` are still the rejected landscape version — run
`python NorseBackpack/TravelMap/build_trail_maps_pdf.py aud`.

## Session Close — 2026-09-17 (latest 5) — Aud map build brief written; first symbol layer superseded

**Task:** continuation. After the first symbol layer was verified and corrected, the conversation
moved from "does this export work" to "what should the map contain at all". The user said they
drew the first pass **because it looked nice**, asked what structures a puzzle map actually needs,
then asked for that list to go into the project page as a want-only brief — they are redrawing the
map from scratch.

**What the measurements found** (the brief is derived from these, not invented):

- **Not one of the 29 landmarks sat inside any area.** All in open ground. With 6 ruins and
  6 standing stones on one sheet, no clue could point at a landmark without naming it. This is the
  structural gap that blocked everything else.
- Only **4 route crossings** on the whole sheet (2 water, 2 barrier).
- **No route passed through an area** — 6 skirted, 4 areas (marsh D6, lake H11, moor I5, moor F6)
  touched by nothing at all.
- The path network was **fine**: 12 of 13 routes in one connected component, 11 junctions.
- 64 of 67 land cells already carried a feature, so the sheet was full, not sparse.

**Correction recorded mid-session.** An earlier claim in this conversation — "barely connected,
only one junction" — was wrong. It came from testing endpoint-to-endpoint proximity only, which
misses T-junctions where a path ends *on* a road. Counting those gives 11 junctions and one
connected component. The same error made bridge `#3` at F6 look stranded; paths `#50`/`#51`
actually meet there, 4.8 and 8.3 pt off the river. Conclusion changed from "rebuild the network"
to "the network is fine, add crossings and context".

**Advice given, recorded in the brief:** do *not* add more footpaths. Junctions were already
sufficient; crossings and context were the shortage. One new line drawn across the grain of the
existing tracks earns more than six new paths — a scan of candidate on-land lines found F8 → E3
crossing 5 routes in 5 distinct grid cells. A dense lane network also reads as English enclosure
country rather than settlement-era Dalir.

**Files changed:**
- `NorseBackpack/Norse_Brainstorm.html` — `PZ-17` now carries a **Build brief** in four parts:
  **A** countable events (water and barrier crossings, each in its own grid cell, fords *and*
  bridges), **B** navigable skeleton (landmarks on routes, forks, landmark at a fork, routes
  through areas, routes alongside linear features, dead ends), **C** ambiguity engine (landmarks
  inside areas, confusable pairs with different context, the water-vs-woodland pair card A2 needs,
  both branches walkable, deliberately stranded scenery), **D** composition and production rules
  (on-land sampling method, 19 pt clearance, map-area bounds, 16 pt icon spacing, keep column E
  rows 2–10 quiet for the digit 7, do not add paths for their own sake, page-point/frame contract,
  z-order). Target counts only — **no "have" column**, at the user's request, since the map is
  being redrawn. The first-pass description is retained above the brief and explicitly marked
  superseded rather than deleted. Pill now reads "Build brief written; map being redrawn; lock
  mechanic open".

**Checks run:** tag balance verified inside the `PZ-17` block (all of p/table/thead/tbody/tr/td/th/
ul/li/h4 balanced; the single extra `</div>` is the qrow close outside the slice). Served over
`http://localhost:8734` and inspected all four brief sections rendered — tables styled correctly,
no console errors. Needed a cache-busting query string to see the change, same as the 17 Sept H1
session.

**Next action:** user redraws the map against the brief and exports. Then re-run the same
measurements (landmarks inside areas, crossings per grid cell, routes through areas, forks,
clearances, on-land sampling) and report what is still short before any route legs are written.

**Blockers / open questions:**
- **The lock mechanic is still undecided.** Four options were put to the user — A count-what-the-
  route-crosses, B grid-columns-as-digits, C legend cipher, D scale-bar measurement — with A
  recommended, and inside A a sub-choice between A1 (three tallies: water / barrier / junctions,
  keyspace ~125) and A2 (leg numbers where you cross water, prettier but only 35 combinations,
  brute-forceable). **The user has not chosen.** The brief is deliberately mechanic-agnostic so the
  redraw is not wasted whichever way it goes.
- Labels stay empty by design through the rebuild; naming the repeated symbols would undo the
  ambiguity mechanic.
- `aud_features.json` is the file of record until the rebuild lands, and is still not read by
  `build_trail_maps_pdf.py`.
- The zoomed frame is still exporter-only; the printed sheet uses the shipped wider frame.
- `ÍSLAND`, `DENMARK STRAIT`, `FAXAFLÓI` and `Snæfellsnes` still fall outside the zoomed frame.
- `output/pdf/Trail_Map_3_Aud_*.pdf` are **still the rejected landscape two-panel version**
  (792x612). Files are writable; the rebuild was not run. Run
  `python NorseBackpack/TravelMap/build_trail_maps_pdf.py aud`.

## Session Close — 2026-09-17 (latest 4) — Aud's first symbol layer checked and corrected

**Task:** the user pasted a 59-feature Aud map-designer export into chat and asked whether it
would work as a map, then said to fix what came back. Verification and correction, not new design.

**Verdict: it works.** Frame matches `aud_base.js` exactly, so designer and print cannot drift.
The layer reads as a surveyed valley rather than a scatter of icons, which was the point of
replacing the shelved detail panel.

**How it was checked.** A vertex-only land test is not sufficient and is also misleading: a road
with both ends on land can still span a fjord between two vertices, and Dögurðarnes and
Bjarnarhöfn themselves fall a fraction *outside* the Natural Earth polygon, so they read as "sea".
Every line was therefore sampled every 2 pt and every area on a 30x30 grid against the coastline
polygon. Result: **no feature lies over water**. The stone wall's two ends touch the shoreline,
which is correct for a wall. No two of the 29 point symbols are closer than 16 pt.

**Three placements corrected** (in `NorseBackpack/TravelMap/aud_features.json`):
- River `#1` east end overhung the map area by 1.9 pt and would have bled into the grid band —
  moved to x 577.0.
- Paved road `#13` terminated 3 pt from the Hvammur stop pin and 12 pt from the Krosshólaborg
  dot. Those two dots are only 8.5 pt apart, so *any* approach threads between them; rerouting was
  tried numerically and could not clear both. Trimmed back to `(311.0, 682.6)` instead — it now
  ends in open ground where the footpath network takes over.
- Hedge `#56` (9 pt) and field `#38`'s corner (15 pt) were pulled east, clear of Eiríksstaðir.

Minimum clearance from any stop or town dot is now **19 pt**.

**Files changed:**
- `NorseBackpack/TravelMap/aud_features.json` (new) — the corrected 59-feature export. The
  designer had no repo-side home for its output before this; it lived only in browser storage.
- `NorseBackpack/Norse_Brainstorm.html` — `PZ-17` records the layer, its composition, the
  verification method, the three corrections, why nothing is labelled yet, and a z-order rule for
  whoever wires the export into the build. Status pill now reads "Symbol layer placed and
  verified; labels and lock mechanic both open".

**Checks run:** re-ran the full geometry check on the corrected file (0 features outside the map
area, 0 over water, 0 icon collisions, min clearance 19 pt); reloaded the corrected JSON into
`Aud_Map_Designer.html` over `http://localhost:8734` and inspected the rendered sheet at
1000x1450 — all 59 features draw, no console errors; served `Norse_Brainstorm.html` and confirmed
the new `PZ-17` copy renders in the Open questions tab with no console errors.

**Next action:** decide Aud's lock mechanic — what the seven-stop route has to produce. Still the
single blocker, unchanged.

**Blockers / open questions:**
- **Nothing is labelled, deliberately.** All 59 features carry an empty label. With 6 ruins,
  6 standing stones, 3 mills, 3 churches and 3 wells on one sheet, no clue can name a landmark
  unambiguously until the mechanic is known. Labels and the route trace are the same task as the
  lock, not separate tidying.
- The route itself is not drawn.
- `aud_features.json` is still not read by `build_trail_maps_pdf.py`. Nothing drawn reaches paper.
- The zoomed frame is still exporter-only; the printed sheet uses the shipped wider frame.
- `ÍSLAND`, `DENMARK STRAIT`, `FAXAFLÓI` and `Snæfellsnes` still fall outside the zoomed frame.
- `output/pdf/Trail_Map_3_Aud_*.pdf` are **still the rejected landscape two-panel version**
  (792x612). The file lock from the previous session is gone — the files are writable now — but
  the rebuild was not run this session. Run
  `python NorseBackpack/TravelMap/build_trail_maps_pdf.py aud` to replace them.

## Session Close — 2026-09-17 (latest 3) — 4-up print-sheet combiner for Staples

**Task:** printing/production question, not design — user is ordering duplex prints of the Norse
postcards from Staples and wanted to fit multiple different cards per sheet (page-count pricing)
plus asked whether a Cricut can cut them out. Answered the Cricut question in chat (yes — straight
5x3.5in cuts, crop marks needed for alignment) and built the requested cut-line/multi-up tooling.

**Found:** every `build_postcard_<CODE>_pdf.py` already draws crop marks, but only for its own
2-up sheet (same card twice). Neither existing helper covers multiple *different* cards per sheet:
`build_postcard_collection.py` just concatenates single-card pages; `build_topedge_test_sheet.py`
is an unrelated scale-registration test. No combiner existed for the "4 different cards per
Letter sheet" layout the user wants.

**Built:**
- `NorseBackpack/Postcards/build_postcard_sheet_pdf.py` (new) — imports `draw_front_card` /
  `draw_back_card` from each existing card's own build script (via `importlib`, no duplication of
  card content) and lays 4 cards 2x2 on a landscape Letter sheet, with the same crop-mark style as
  the existing scripts. Chunks all 14 currently-built cards (`CARD_CODES` list in the script) into
  4-per-sheet groups (last group has 2). Outputs to `output/pdf/Postcard_Sheet_0N_*.pdf`.
- **Duplex flip ambiguity:** Staples's online order tool only offers "double sided," no flip-edge
  detail. Rather than guess, the script builds both variants per sheet — `..._LongEdge_Print.pdf`
  and `..._ShortEdge_Print.pdf` — so the user can test-print page 1 of each and keep whichever
  aligns. Long-edge mirrors the two columns on the back page; short-edge mirrors the two rows.
  Note: the existing single-column 2-up sheets (no mirroring at all) are only correct under a
  long-edge assumption — worth keeping in mind if the short-edge variant turns out to be the one
  that aligns at Staples, since that would mean the individual 2-up sheets need the same fix.

**Checks run:** ran the script (all 8 output PDFs generated, no errors). Rendered
`Postcard_Sheet_01_LongEdge_Print.pdf` (both pages) to PNG via PyMuPDF and inspected visually:
front page shows 4 distinct cards (L1/L2/L3/LD) with crop marks at each corner; back page content
and mapping checked by hand against the flip logic — L1's back (front top-left) is drawn in the
back page's top-right slot, which is correct for a long-edge flip (front top-left ends up backed
by back-page top-right before the physical flip lands it in the same physical corner).
Short-edge variant and sheets 02-04 were not individually re-rendered (same code path, lower risk).

**Next action:** user test-prints one page of `Postcard_Sheet_01_LongEdge_Print.pdf` and
`..._ShortEdge_Print.pdf` at Staples to determine which flip-edge assumption matches their
printer, then prints the matching variant for the remaining sheets.

**Blockers / open questions:** none design-related. Only 14 of 18 postcards have build scripts yet
(A1/A3/AD/H2/H3/H6/HD remain, per the prior session's note) — `CARD_CODES` in the new script will
need those appended once they exist.

## Session Close — 2026-09-17 (latest 2) — H1 Oslo built; Harald sequencing recorded

**Task:** continuation of the same session. Decided and recorded Harald's leg sequencing (H4/H5
rune cryptex opens the leg, H1/hnefatafl is next), refreshed H1's Fun Fact with a better-sourced
detail, rewrote H1's stale "Last stop" message to fit its new position and to actually carry the
counting instruction its own lock code depends on, then built H1 the same way as H4/H5.

**Found while updating `PZ-05`:** H1 already had a drafted message and Fun Fact from an earlier
(16 Sept) session — nearly duplicated it before noticing. That old draft opened "Last stop,
and it feels fitting to end where legends get made," written when Oslo was conceived as ending
Harald's trail rather than opening it, and separately claimed the trail map "does not exist yet"
(stale — the map has existed since earlier this session). Surfaced both to the user before
touching anything; they chose to keep the message's core content but rewrite the opening and
add the missing "count how far he travels each time" line, which the `253` code actually depends
on and the old draft never stated.

**Built this session:**
- `NorseBackpack/Postcards/build_postcard_H1_pdf.py` (new) — same template as H4/H5. No credit
  line drawn: H1's front-art ImageGen prompt (Postcard system tab) never recorded a source photo
  credit, unlike H4/H5, so none is invented here. Built both PDFs plus
  `Postcard_H1_Oslo_Back.png` for the HTML gallery.
- `NorseBackpack/Norse_Brainstorm.html` — `PZ-05`'s Harald section rewritten: H4/H5 entries added
  (previously missing from this tracker entirely), H1's entry replaces the stale "Last stop"
  draft and un-blocks it from the map dependency. The `hnefatafl` puzzle-array entry's `clue`,
  `status` and `risk` fields synced to the new message and sequencing (`ST-01` destination,
  not "position undecided"). Postcard system gallery entry for H1 updated to the full front+back
  pattern with a real PDF link. Pill counts bumped: `PZ-05` now 12 of 18 real cards built; the
  Harald trail-group header names all three built cards.

**Checks run:** rendered both H1 PDF pages to PNG and inspected visually — message wraps
correctly, Fun Fact box distinct from the message content, front art unaffected. Served
`Norse_Brainstorm.html` over `http://localhost:8734` (had to hard-navigate past one stale browser
cache mid-check — a `getElementById` probe first returned only the front `<img>`, re-navigating
with a cache-busting query string showed both front and back correctly): no console errors, the
new `Back.png` returns 200, gallery and puzzle-card text match the built card exactly.

**Next action:** design Harald's third lock — directional lock vs `MEAD` (`PZ-20`) — the only
piece of Harald's leg still without a mechanism. H1, H4 and H5 are now fully built; only the
hnefatafl board-setup panel (composite onto the real map back) and cards A1/A3/AD/H2/H3/H6/HD
remain as production work, not design work.

**Blockers / open questions:** `ST-01` (which physical container each Harald lock feeds) is
still unfrozen game-wide, same as every other lock in the bag.

## Session Close — 2026-09-17 (latest) — Harald's branch-rune cipher designed and built, H4/H5 written

**Task:** design the first lock of Harald's leg (3-4 locks across his 7 postcards, decided in
chat), then write and build the two postcards it needs. Landed on: branch-rune cipher (`PZ-02`),
delivered by postcards H4 and H5 plus Harald's own trail map instead of the old
stick-and-museum-label props, which never got built. Also designed, but not yet implemented:
Hnefatafl (already mostly built, `PZ-01`/`PZ-07`) and a map-based lock using either the
directional lock or `MEAD` (`PZ-20`) — still open, next up.

**Mechanism, fully decided:**
- Harald's trail map grid is relettered on this sheet only — `A, C, E, I, K, N, R, T, V` in
  place of the shared `A–I` columns (the other three trail sheets are untouched).
- Five carved rune-stems sit at cells `G6, A10, I9, C3, F2` (displayed under the relettered
  columns as `R6, A10, V9, E3, N2`), among seven decoy stems elsewhere on the sheet with
  plausible but meaningless branch counts.
- Postcard **H4** (Hedeby) carries the decode key: her message sets up that a woodcarver taught
  her the branch-rune convention, and a hand-drawn table on the card (in her handwriting, not the
  typed Fun Fact) gives the three Younger Futhark groups.
- Postcard **H5** (Aci Castello, Sicily) carries the reading order: the word `raven`, drawn
  underlined in her message. Reading the relettered columns in that literal order (R, A, V, E, N)
  visits the five cells in H, R, A, F, N order — the existing `HRAFN` cryptex answer. No separate
  ranking step or reading-direction clue needed; a three-piece mechanism (stick + museum label +
  direction) collapsed to two postcards + the map.
- **H5's place corrected mid-session:** its front art actually depicts Aci Castello (Norman
  castle near Catania), not Syracuse (the site named in `stops.js` for Harald's real 1038–1040
  campaign). User chose to retarget the card's text to Aci Castello rather than change the art.
  Message and Fun Fact are both sourced to Aci Castello specifically (Cyclops-legend rocks,
  1071–1081 castle, later three centuries as a prison).

**Built this session:**
- `NorseBackpack/TravelMap/build_trail_maps_pdf.py` — added the Harald-only `col_letters`
  override, `HARALD_RUNES_REAL`/`HARALD_RUNES_DECOY` cell lists, and `draw_rune_stem`/
  `cell_center` helpers. Rune stems are vector line art (tally strokes), not new image assets.
  Rebuilt `Trail_Map_4_Harald_{Print,ANSWER}.pdf`; the answer copy labels each real cell with
  its decoded letter for designer checking.
- `NorseBackpack/Postcards/build_postcard_H4_pdf.py` and `build_postcard_H5_pdf.py` (new) — full
  message/Fun Fact/address/stamp/postmark backs, matching the standard card template. H4 adds a
  hand-drawn rune-key table under the message (her own copy, not typed reference material). H5
  adds inline underline support so `raven` can be underlined mid-paragraph. Built all four PDFs
  (`Print` and `Letter_Print` each) plus `Postcard_H4_Hedeby_Back.png` /
  `Postcard_H5_Sicily_Back.png` for the HTML gallery.
- `NorseBackpack/Norse_Brainstorm.html` — `PZ-02` now records the delivery mechanism and marks
  it decided and built; `PZ-09` gives Harald's map its front-of-sheet job (was "still unplaced");
  the `prop-runes` design section rewritten to drop the stick/museum-label props and describe the
  map+H4+H5 split; the `puzzles` array (drives both Story and Puzzles & locks tabs) gained a new
  `runes` entry, decided/built — puzzle count is now 13; the Postcard system tab's H4/H5 gallery
  entries updated to the full front+back pattern with real PDF links; the prop-kit list's stale
  rune-stick bullet points at the new design instead.

**Checks run:** rebuilt both Harald trail-map PDFs and all four H4/H5 postcard PDFs, rendered
every page to PNG and inspected visually — relettered grid band correct, all 5 real + 7 decoy
stems placed with no collisions, all 6 real stops still labelled on the map, decoded letters on
the answer copy match the intended cells; H4's rune-key table renders all 3 rows without overlap
(fixed one collision bug caught by this render pass); H5's `raven` underline lands correctly
mid-paragraph; both fronts confirmed unaffected. Served `Norse_Brainstorm.html` over
`http://localhost:8734`: no console errors, both new `Back.png` files return 200, `prop-runes`
anchor resolves, the `runes` card renders correctly in both the reference table and the
full-mechanism list.

**Honest flag, not yet resolved:** at print size the tally-stroke rune stems on the map read
visually close to a small pine tree. Worth a look in person before committing to print — may
want a less tree-like tick angle. Separately, H4's hand-copied rune key substitutes `ö` for `ą`
and `r'` for `ʀ` (the handwriting font has no glyph for either) — noted in `PZ-02`, does not
affect the answer since `HRAFN` never uses those two runes.

**Next action:** design the second Harald lock — directional lock vs `MEAD` (`PZ-20`) — or move
to Hnefatafl's position in the trail sequence. User's call.

**Blockers / open questions:** `ST-01` (which physical container this cryptex feeds) is still
unfrozen game-wide, same as every other lock in the bag.

## Session Close — 2026-09-17 (later) — Aud split-panel shelved; map designer built

**Task:** the split-panel concept was rejected. Shelve it, return Aud to one portrait map, and
start the replacement — the treasure hunt drawn on that single map with proper cartographic
symbols rather than isolated icons.

**Shelved, not deleted** — `NorseBackpack/Drafts/2026-09-17_Aud_split_panel/` with a README
explaining what it was, why it went, and what is worth reusing. It holds `aud_detail_panel.py`,
`normalize_aud_vignettes.py`, the panel drawing code lifted verbatim out of the build script, and
all the art. **Codex finished the ten v2 vignettes in a parallel session and wired them in
minutes before the shelving** — they are intact and have never appeared in a delivered sheet.

**Build script returned to one portrait sheet.** `AUD_PAGE`, `AUD_PANEL`, `AUD_MAIN_*`,
`aud_split`, `_aud_offset`, `_aud_glyph`, `_aud_hachures` and `draw_aud_detail_panel` are all
gone; the `landscape` import is dropped. All four trail maps build portrait again and Aud's route
still traces the digit **7**.

**The scale conflict, measured.** Aud's three stops span 34 km east–west and 110 km
north–south — that spread *is* the 7. Holding all four stops needs a ~143 km frame, which is
**1 pt ≈ 211 m**; a real 500 m hedge would be 2.4 pt. The user's call: keep the one real map and
draw **markers out of scale** rather than invent a new landscape. A hedge on this sheet is tens of
km long in real terms, and that is fine — it is a puzzle prop, not a survey.

**Lock mechanic reopened from scratch.** The plot-number sum is *not* carried forward.

**Built:**

- `NorseBackpack/TravelMap/export_aud_base.py` — runs the real build at the zoomed frame and
  writes `aud_base.js` (coastline, stops, towns, area labels) already in **PDF page points**. The
  projection is never reimplemented in JS, so designer and print cannot drift.
- `NorseBackpack/TravelMap/aud_base.js` — generated; do not hand-edit.
- `NorseBackpack/TravelMap/Aud_Map_Designer.html` — the editor. 9 line symbols, 5 area symbols,
  10 point symbols; click to place or draw, drag vertices, curve smoothing, per-feature width and
  label, grid-reference readout, display zoom, undo, localStorage autosave, JSON export/import.
  Hedges, walls and ditches draw their own ornament along the line.

**Checks run:**

- All four trail maps rebuild; page sizes confirmed 612x792 for every one.
  `build_art_placement_guide.py` still runs.
- Aud rebuilt to a temp directory and inspected at 130 dpi: single portrait map, digit 7 trace
  intact. (The real `output/pdf/Trail_Map_3_Aud_*.pdf` could not be overwritten — see blockers.)
- Designer served over local HTTP and driven in the browser: loads with no console errors, 20
  imported features of every symbol type render correctly, a real click placed a Well at grid E5
  and populated the properties panel, zoom and layout verified, then test data cleared.
- `export_aud_base.py` reports 1 land ring, 3 stops, 6 towns, 4 area labels.

**Frame panned east (later in the session).** `ZOOM_FRAME` is now
`(-22.9751, -20.5451, 64.08, 65.37)`: same span, panned so stop 1 (Dögurðarnes) lands in grid
column B at x 140.2 and far more land is in play. Bjarnarhöfn — decoy card AD's site — was
7 pt off the west edge at exact column-B centre, so the pan is set to keep it 9 pt inside, at A4.
It is a decoy card rather than a visit, so `build()`'s stop assertion does not cover it; the
exporter checks it by hand. Stops now read B2, E2, E10.

**Next action:** decide the puzzle mechanic — it is fully open again. Nothing else should be
drawn on the map until it is known what the route has to produce.

**Blockers / open:**

- `output/pdf/Trail_Map_3_Aud_Print.pdf` is **locked by another process** (open in a viewer), so
  the shipped Aud PDFs are still the landscape two-panel version. Close it and re-run
  `python NorseBackpack/TravelMap/build_trail_maps_pdf.py aud` to replace them.
- The decorative labels `ÍSLAND`, `DENMARK STRAIT`, `FAXAFLÓI` and `Snæfellsnes` fall outside the zoomed
  frame and need repositioning before a zoomed sheet is printed. `export_aud_base.py` drops them
  and prints their names as a reminder.
- The designer's JSON export is not yet read by `build_trail_maps_pdf.py`. Nothing placed in the
  browser reaches paper yet.
- The zoomed frame is only used by the exporter; the printed map still uses the shipped wider
  frame. Switching it over is a one-line change to `TRAILS["aud"]["frame"]` once the labels are
  repositioned.
- `build_trail_maps_pdf.py` has mixed line endings (CRLF throughout, LF in one block), which makes
  whole-file rewrites error-prone.

## Session Close — 2026-09-17 — Aud PZ-17 v2 landmark artwork integrated

**Task:** apply the revised PZ-17 visual instructions to Aud's landscape detail panel.

**Done:** generated and normalized ten reusable purple-only, transparent v2 icons (ford, mill,
falls, fold, chapel, cairn, standing stone, naust, farm, birch). No icon contains a hidden digit
or countable code. The map now uses them in fixed 34 pt bounds; marsh remains deliberate vector
terrain. Rebuilt both Aud PDFs and retained the raw ImageGen renders alongside production PNGs.

**Files changed:** `NorseBackpack/TravelMap/normalize_aud_vignettes.py`,
`NorseBackpack/TravelMap/build_trail_maps_pdf.py`, `NorseBackpack/Norse_Brainstorm.html`, ten
`TravelMap/Art/Aud_*_v2.png` production assets and their source renders in
`TravelMap/Art/Sources/`, plus the two Aud output PDFs.

**Checks:** `aud_detail_panel.py` verifier passes: route `c7 > d7 > e4 > d3 > b4 > c9 > f8`,
sum `467`, 95 plausible wrong routes, closest 20 away. All production icons have visible pixels
only in `#6D528B`, with alpha; the Python sources compile. Rendered and visually inspected both
landscape PDFs at 180 dpi. The PZ-17 HTML page was checked over local HTTP.

**Next:** draft the user-approved ticket/postcard clue copy against the finished map, then run a
true-size physical readability test. Do not invent that copy.

## Session Close — 2026-09-17 — Aud treasure-route mechanic redesigned (PZ-17)

**Task:** redesign Aud's treasure-hunt detail panel after the first Codex pass was rejected, then
build it.

**Done — the mechanic changed, not just the layout:**

- **Digits no longer live in the artwork.** Every cell of the detail panel now carries a small
  two-digit *survey plot number*; players follow a clue chain from landmark to landmark and the
  lock code is the **sum of the stops' plot numbers**. This decouples art from puzzle, so icons
  may repeat freely and Codex draws a landscape rather than digit-bearing icons.
- **Lock drops from four digits to three.** Seven two-digit stops sum to the mid-hundreds; four
  digits is arithmetically unreachable this way. `4816` is superseded by the working sum **`467`**.
- **Two rules the mechanic forces.** (1) Every stop must be a *different landmark type*, because a
  sum is order-independent and two same-type stops can be swapped for free — a first pass with
  sheepfolds at stops 4 and 6 produced three wrong routes summing to exactly the right answer.
  (2) The numbering must be *verified*: all same-type substitutions are enumerated and nothing
  wrong may land within 15 of the answer.
- **Working route:** `c7` ford → `d7` mill → `e4` falls → `d3` sheepfold → `b4` chapel →
  `c9` cairn → `f8` standing stone. Sum **467**, verified against 95 wrong-but-plausible routes,
  closest 20 away.
- **Layout settled.** Sheet turns landscape (792×612 pt). Main map grows to 432×569 pt at scale
  `0.760` (was 381×502 at `0.67`); detail panel grows to 307×569 pt with a 6×10 grid of
  46×50 pt cells and 34 pt icons. Both panels get bigger — the dead space was portrait, not
  the split.
- **Ticket and route-record card merged into one A6 double-sided prop.** Front is the ticket face
  and gives the starting point; reverse is a seven-row `STOP / SITE / PLOT No.` form with row 1
  pre-filled by hand (*the old ford — 59*). Clues split: ticket gives the start, postcard 1 the
  six-hop chain, postcard 2 the chapel disambiguator.

**Files changed:**

- `NorseBackpack/TravelMap/aud_detail_panel.py` (new) — single source for the panel's plot
  numbers, landmark placements and the seven-stop route, plus the check that guards them. Four
  invariants: seven distinct stop types; no wrong route within 15 of the answer; no stop plot
  under 20; no two features in one cell.
- `NorseBackpack/TravelMap/build_trail_maps_pdf.py` — Aud's sheet is now `landscape(letter)`;
  `AUD_MAIN_SCALE` is computed (0.7596) rather than hardcoded 0.67; `AUD_DETAIL_ART` and the old
  `draw_aud_detail_panel` are replaced by `_aud_offset` / `_aud_glyph` / `_aud_hachures` and a
  rewritten panel that imports its data from `aud_detail_panel.py`.
- `output/pdf/Trail_Map_3_Aud_{Print,ANSWER}.pdf` — rebuilt, landscape.
- `NorseBackpack/Norse_Brainstorm.html` — PZ-17 rewritten with the new mechanic, the two rules,
  the route table and the prop consolidation; the old digits-in-art design, the `4816` code, the
  ImageGen prompt set and the split-panel diagram caption are all **marked superseded in place**,
  not deleted. Cross-references updated in PZ-03, PZ-09, PC-A2, the museum-ticket panel, the Aud
  lockflow node and the generated puzzle-card dataset.

**Checks run:**

- Near-miss sweep over all 95 same-type substitution routes: closest wrong sum is 20 from 467.
  Now runs from the repo: `python NorseBackpack/TravelMap/aud_detail_panel.py` — passes.
- Confirmed the check actually catches what it exists to catch, by reintroducing each bug in
  memory: duplicate stop type, a decoy tuned within the margin, and two features sharing a cell.
  All three fail the check.
- `467` re-checked against every other code in the page (`1021`, `1576`, `1972`, `231`, `253`,
  `427`, `582`, `562`, `2468`) — no collision.
- Page served over local HTTP (`static-preview`, port 8734 was already running) and inspected in
  the in-app browser: PZ-17 renders, route table shows 7 rows with the page's own table styling,
  no console errors.
- Rebuilt all four trail maps: all succeed; page sizes confirmed 792x612 for Aud only, 612x792 for
  Leif/Rollo/Harald. `build_art_placement_guide.py`, which imports the build module, still runs.
- Rendered both Aud PDFs at 150 dpi and inspected: main map is vector and larger than before,
  detail panel draws terrain, 28 features, plot numbers and (on the answer key) the numbered route
  with `SUM 467`.
- Checked no glyph can cross a cell line: tightest margin is 13.89 x 16.64 pt at the c6 standing
  stone, against a largest glyph half-extent of 12.5 x 10.0 pt. The budget is written into
  `_aud_offset`'s docstring and must be rechecked if a glyph or the offset range grows.

**Built, this session:** `build_trail_maps_pdf.py` now makes Aud's sheet landscape and draws the
surveyed-valley detail panel from `aud_detail_panel.py`. `AUD_DETAIL_ART` is gone. All four trail
maps rebuild; only Aud is landscape.

**Prompt set written.** PZ-17 now carries the v2 ImageGen prompts for ten vignettes — ford, mill,
falls, fold, chapel, cairn, stone, naust, farm, birch — with kind strings matching
`aud_detail_panel.py`'s `FEATURES`. Marsh stays a vector texture; the farmstead's home-field is
drawn by the script, so that icon is the building only. Two override rules are stated up front: no
hidden counts (a countable detail is now an active red herring), and each icon is reused as-is
across its decoys rather than varied.

**Next action (Codex):** generate the ten vignettes, normalise them with
`normalize_aud_vignettes.py` to flat `#6D528B` with clean alpha, then replace the placeholder
bodies in `_aud_glyph()` with image draws. Keep each inside a 34 x 34 pt box — `_aud_offset`'s
docstring records the clearance budget that stops a glyph crossing a cell line.

**Blockers / open:**

- No clue copy is written. It is drafted against the finished map, not before.
- In the sketch the fjord still reads as a plain diagonal coastline rather than an inlet, and the
  north river branch competes with it at similar line weight.
- All detail-panel icons are placeholder vectors drawn by `_aud_glyph` in the build script. A
  fresh Codex prompt set is needed for a full landscape vocabulary; cairn and standing stone must
  read as clearly distinct, since they are stops 6 and 7. The rejected `Aud_*_v1.png` renders are
  left on disk but are no longer referenced by any code.
- `build_trail_maps_pdf.py` has mixed line endings (CRLF throughout, LF in the block the previous
  session added). Not worth a reflow on its own, but it makes whole-file rewrites error-prone.

## Session Close — 2026-09-17 — Aud two-panel treasure-map pass

**Task:** implement the approved <code>PZ-17</code> map split and its four purple detail-panel
icons. Museum-ticket and postcard clue copy were explicitly out of scope.

**Done:**

- Aud's letter-sized PDF is now two panels. The original full-region map is uniformly reduced
  into the right panel, retaining its original frame bounds, projection, towns/waters and route
  stops; the new left Dalir/Hvammur panel has an independent lowercase <code>a–b</code> / 1–4
  reference grid. This is a 2×4 grid because the sheet cannot fit the original region at its
  former physical width plus a 4×4 close-up; all five landmark placements still occupy separate
  cells.
- Generated and normalized four assets: watermill, Auðarsteinn, sheepfold and one reused ruined
  chapel. Production pixels are flat <code>#6D528B</code> with transparent alpha. Detail
  placements are mill → 4, stone → 8, sheepfold → 1, chapel pair (the inland target → 6;
  the same six-bearing chapel is also the Bjarnarhöfn decoy). The answer PDF labels the four
  relevant counts for designer checking.
- Updated <code>PZ-17</code> and the generated puzzle-card source to state that museum-ticket
  descriptions, A2's distinguishing observation and exact grid refs remain unwritten/open;
  removed the prior invented chapel wording. Exact ImageGen prompts are recorded in PZ-17.

**Files changed:**

- <code>NorseBackpack/TravelMap/build_trail_maps_pdf.py</code>
- <code>NorseBackpack/TravelMap/normalize_aud_vignettes.py</code> (new)
- <code>NorseBackpack/TravelMap/Art/Aud_*_v1.png</code> and
  <code>TravelMap/Art/Sources/Aud_*_ImageGen_Source.png</code> (new)
- <code>output/pdf/Trail_Map_3_Aud_Print.pdf</code> and <code>Trail_Map_3_Aud_ANSWER.pdf</code>
- <code>NorseBackpack/Norse_Brainstorm.html</code>

**Checks:** rebuilt both Aud PDFs; rendered and visually inspected both at 160 dpi; the right
panel visibly retains Dögurðarnes, Hvammur, Esjuberg and Bjarnarhöfn; icons are separated and
the answer-panel labels read 4/8/1/6. Python compile passed. Every visible pixel in all four
production assets is exact RGB <code>(109,82,139)</code>, with real transparent pixels. The live
page loaded through <code>http://localhost:8734</code> with no console errors; PZ-17's generated
puzzle card shows the clue wording is not written. Existing page-wide div balance remains
one unclosed <code>div</code> at line 1052, in the pre-existing postcard/lab area, not introduced
by this pass.

**Next action:** write and test the museum-ticket landmark descriptions plus A2's distinguishing
chapel observation, then choose final real-world placement/grid references before print testing.

## Session Close — 2026-09-17 (continued) — Design spec / Design guide split; Props & choices folded in

**Task:** the deferred item from earlier today — remove the overlap between Design spec, Design guide
and Props & choices. Tabs are now **11** (from 12; 13 before this morning).

**Split rule applied:** the Design guide holds how things *look and sound*; Props & specs holds the
*physical objects and how they are built*; Open questions holds the *backlog*; the Postcard system
tab holds *card mechanics and decisions*. Anything that sat in the wrong one moved.

**Moved out of the Design spec:**

| Content | New home | Why |
|---|---|---|
| "What makes a clue good here" | Puzzles & locks, collapsed at `#clue-standard` | It is a rule for writing puzzles |
| "The postcard system" (count, size, format, recipient address) | Postcard system tab, retitled "Format, count and address" | Card decisions belong with card mechanics |
| "Card back: the standard layout and type scale" | Design guide | Pure type/layout standard |
| "The four stamp series" | Design guide (`#prop-stamps`) | Visual identity per trail |
| "Next steps, in order" | Open questions, top, retitled "Do these next, in this order" | It orders IDs that already live there |
| "What has to be prototyped" | Open questions, foot | Backlog |
| "Unresolved" | Deleted stub; its one observation kept at `#leif-observation` | The stub was already only a pointer |
| "Historical claims needing verification" | Open questions (`#historical-claims`) | Backlog; `HI-05` now points here |

**Props & choices tab removed**, its content folded into Props & specs:

- Core reusable prop kit, candidate pouch, "already at home" locks → `#prop-kit`.
- Containers and release, reset/prototype checks, current assumptions → `#prop-containers`.
- "Basis and limits" sources footer → foot of Props & specs.
- "Presentation direction" → **dropped as a duplicate.** The Design guide's Tone & voice already
  said in its own text that it was the canonical restatement of it; that note now records the fold.
- "Other directions worth keeping" → **dropped as a duplicate of the Options tab**, except that its
  fuller reasoning for retiring the pin-and-cord idea (Rouen and Roumare sit 0.13&nbsp;in apart on a
  letter map, 0.38&nbsp;in on a 24&nbsp;×&nbsp;36 poster) was merged into the Options entry, which
  had only the bare "superseded" line.
- Its "Decided" summary → **kept, not deleted**, as a collapsed "Superseded snapshot" inside
  `#prop-containers`, with a note naming the three claims in it that are now wrong (postmark dates,
  18 vs 22 cards, interleaved-date ordering) and where the current text lives.

**Corrections made while moving, not invented:**

- The prototype test "Tafl solution uniqueness — confirm exactly one **four-move** escape" predated
  `PZ-01`. Marked done, with the real result: one *three*-move escape on 11×11,
  F6→H6→H11→K11.
- "The final map mechanic" test still listed pinning and a transparent overlay as live candidates.
  Marked partly superseded by `PZ-06`; only digit legibility at true print size is still to test.
- The kept observation still used the old `02`/`03` card numbering. Updated to `L2`/`L3` per `PC-17`.

**Bug found and fixed:** this morning's anchoring pass had an off-by-one
(`len('<div class="designsection">')` is 27, not 26) that left a stray `>` rendering as visible text
at the top of all seven anchored prop sections. Removed.

**Navigation:** `Design spec` renamed to `Props & specs` but keeps `id="design"`, so every existing
`data-view="design"` link still works. `#view-build` now aliases to `design` in `VIEW_ALIAS`
alongside `locks` → `puzzles`, so old deep links to the removed tab still resolve.

### Files changed

- `NorseBackpack/Norse_Brainstorm.html` — all of the above. No other file touched.

### Checks run

Served over local HTTP and checked in the in-app browser:

- **No console errors.** No duplicate `id`s. No empty sections.
- **Link check is now tab-aware:** every `data-view`/`data-anchor` pair was verified to resolve *and*
  to point at an element that actually lives inside the named tab — this is what would catch a moved
  block whose inbound links were left behind. Zero failures.
- **Both aliases verified round-trip:** `navigate('build')` lands on `design`, `navigate('locks')`
  lands on `puzzles`.
- **Positional pointers re-scanned.** Phrases like "at the bottom of this tab", "the briefs above",
  "used above" were searched for after the moves; three were stale and were rewritten as real links.
- **Moved content confirmed present and styled** in its new tab (`.panel` and `.card` both resolve
  inside `#design`; the sources footer and the folded prop kit render).
- Nav shows 11 tabs; the generated Puzzles & locks content is unaffected (12 rows, 12 cards, 12 steps).

**Screenshots were unreliable this session** — the browser pane repeatedly returned blank or timed
out, apparently because the app window was backgrounded. Verification was done through
`read_page`/`javascript_tool` measurements instead, which is why the checks above are stated as
measured values rather than "looks right".

### Next action

Read the Props & specs tab end to end as a reader would. The moves are mechanically correct, but the
tab's internal order was never redesigned — it now runs cipher → board → hoard → comb → tools →
redirect clues → prop kit → containers, and the prop kit probably belongs first.

### Blockers / open items

- **Not done:** the Options tab still holds its own short menu of unplaced puzzles alongside the
  generated "Ideas, not actioned yet" list. It links there and says which is canonical, but two
  lists still exist.
- The Postcard system tab now has both its original content and the moved "Format, count and
  address" block. They do not contradict each other, but the tab was not re-ordered after the move.
- Nothing was committed or pushed.

## Session Close — 2026-09-17 — Puzzle details and Locks merged into one generated tab

**Task:** the user reported three kinds of stale content in `Norse_Brainstorm.html` — Story & sequence,
Puzzle details, and an overlap between Design spec and Design guide. Scope agreed in chat: fix the
first two (items 1–3 below) and remove the L2/L3 alignment preview. The Design spec / Design guide
split was explicitly deferred to a later session.

**Root cause found.** One hand-written `const puzzles=[...]` array of 10 entries drove *both* the
Story tab's journey grid and the whole Puzzle details tab. It was frozen at an old design: it listed
the rune relic, the family connection and the saga strips as steps in the live sequence, contained
none of the four decided chains (`PZ-13`, `PZ-15`, `PZ-17`, `PZ-19`), and still gave the hnefatafl
code as `231` on a 7×7 board — superseded by `253` on 11×11 per `PZ-01`. The only current
data lived in the Locks tab table, which nothing else read.

**What changed:**

1. **Puzzle details + Locks merged into one "Puzzles & locks" tab.** Nav is 13 tabs → 12.
   `#view-locks` still resolves, via a `VIEW_ALIAS` map, so old deep links keep working.
2. **The data array was rewritten** with structured fields (`code`, `lock`, `props`, `cards`,
   `releases`, `refs`, `state`) instead of prose-only blobs, and grown from 10 stale entries to 12
   current ones. Content was taken from the Locks table and the `PZ-*` open questions — nothing
   invented. The table, the per-puzzle cards, the ideas list and the Story journey grid are all
   generated from it, so they cannot drift apart again.
3. **The Story journey grid is now generated, not typed.** It renders whatever is in the array, in
   play order, with trail colour, code and status pill. Its intro paragraph says so explicitly.
4. **"Ideas, not actioned yet"** added at the foot of the tab, from a second `ideas` array: `PZ-20`
   MEAD on Harald's trail, the cryptex `HRAFN`, the rune relic, the family connection, the saga
   strips, the wrong museum label. The Options tab's overlapping list now links here and says the
   linked list is the one to edit.
5. **Deep links added throughout.** Every postcard article (`#pc-L1` … 22 of them), seven prop
   specs (`#prop-hoard`, `#prop-comb`, `#prop-hnefatafl`, …) and all 67 open-question rows
   (`#q-PZ-13` …) now carry stable anchors. Navigation was rewritten as a delegated click handler
   with `data-anchor` support, plus a `hashchange` listener, so `#view-puzzles/pz-treasure` works
   from a pasted URL and from generated links alike.
6. **The L2/L3 alignment preview was removed** from the Postcards tab (the two proof images). The
   hold-to-light puzzle itself is untouched — still decided, still `1576`, still Leif's Lock 3. The
   "Edge puzzle decided" paragraph above it was kept, as chosen in chat.

### Files changed

- `NorseBackpack/Norse_Brainstorm.html` — all of the above. No other file touched.

### Checks run

Served over local HTTP (`python -m http.server 8734`, already running) and checked in the in-app
browser, not as a `file://` snapshot:

- **No console errors** on load.
- **No broken navigation:** every `data-view` resolves to a real section and every `data-anchor`
  resolves to a real element (checked programmatically across the whole page). No duplicate `id`s.
- **Render counts correct:** 12 table rows, 12 puzzle cards, 12 journey steps, 6 ideas, 0 alignment
  previews remaining.
- **Deep links verified end to end:** story step → puzzle card, puzzle card prop link → open
  question row, summary-table row → puzzle card, and a pasted `#view-puzzles/pz-hnefatafl` URL. All
  land at 96&nbsp;px from the top, clear of the sticky nav, with the flash highlight applied.
- **Layout:** lockflow diagrams render horizontally again after rescoping the old `#locks` CSS to
  `#puzzles`; status pills render as pills in both new sections; the summary table scrolls inside
  its own container with no page-level horizontal overflow.

**Correction recorded in the page:** the hnefatafl entry now carries `253` and the 11×11
`F6 → H6 → H11 → K11` solution, matching `PZ-01`. The old `231` is described as superseded.

### Next action

Do the deferred item 4: split the Design spec / Design guide overlap. The duplication is concrete —
the Design spec contains its own `<h2>The postcard system</h2>` (a second copy of the Postcard system
tab's), plus "Card back: the standard layout", "The four stamp series" and an illustration brief that
belong in the Design guide; and its "Next steps", "What has to be prototyped", "Unresolved" and
"Historical claims needing verification" sections duplicate the Open questions backlog. Proposed
shape: rename the spec "Props & specs", keep only the prop specs in it, fold in the Props & choices
tab, and leave the Design guide purely visual. That would take 12 tabs to 10.

### Blockers / open items

- **Not verified:** whether the `refs` list on each puzzle card is exhaustive. Each card lists the
  open-question IDs that visibly govern it; a puzzle may be mentioned in a question not listed there.
- The Options tab still carries its own short "Puzzles worked up but not placed" menu. It now points
  at the Ideas list rather than duplicating it silently, but the two lists still need one owner —
  worth folding Options' copy into the generated one in a later pass.
- Nothing was committed or pushed.

## Session Close — 2026-09-16 (continued, 12) — Treasure-route digits picked; A2's text complete

**Task:** picked the four hidden digits for `PZ-17`'s treasure route and wrote A2's missing
distinguishing-detail clue — the last two pieces blocking A2 from being a finished card.

**Digits decided:** mill = 4, Auðarsteinn = 8, sheepfold = 1, chapel (final square, carries the
coin-cache mark) = 6. Route order mill → Auðarsteinn → sheepfold → chapel gives code `4816`.
Checked against every other code in the page — no collision, no repeated digit.

**A2's chapel-distinguishing detail, written:** since the map's icons are plain single-colour
silhouettes with no room for a visual variant between the two chapels, tied the clue to terrain
instead of icon detail — the real chapel sits inland among birches, while the decoy at Bjarnarhöfn
is the coastal one (consistent with that card's own already-built front art, which shows "pale sea
and distant low islands"). Added to A2's message: "The old chapel on the trail was easy enough to
find once I stopped looking by the water and checked the birch hollow instead." No new icon artwork
needed to make this solvable — the two chapel placements are meant to differ by where they sit on
the map, not by looking different.

**Written into `Norse_Brainstorm.html`:** `PZ-17`'s landmark list annotated with each digit and the
resulting code; `PZ-05`'s A2 entry marked complete (back/PDF the only remaining piece) and its status
pill updated; the Locks-tab summary table row and lockflow diagram both updated from "exact code
open" to `4816`.

### Files changed

- `NorseBackpack/Norse_Brainstorm.html` — sections listed above.

### Checks run

- Checked `4816` against every other code in the page (`1021`, `1576`, `1972`, `231`, `253`, `427`,
  `582`, `562`, `2468`) — no collision, confirmed no repeated digit within it either.
- Full-file tag-balance check — all paired (1044 div, 13 section, 36 article, 38 details, 16 ul, 125
  li, 118 a, 11 table, 79 tr, 271 td, 41 th, 260 p, 258 span, 8 ol, 84 figure).
- Served over local HTTP (`static-preview`, port 8734) and confirmed via `document.documentElement.
  innerHTML` checks (the Open questions tab's hidden sections return empty `innerText` even when
  populated, so checked the DOM directly instead) that both `4816` and the birch-hollow clue render.
  No console errors.

### Next action

Build A2's back and print PDF — it's now a complete card, just not yet rendered. Then write the
museum ticket's actual front/back content (it can now reference real digits and a real distinguishing
clue instead of placeholders), then A1, A3 and AD's card text.

### Blockers / open items

- A2's back/PDF not yet built (text is done).
- Museum ticket unbuilt.
- A1, A3, AD card text unwritten.
- Pre-existing backlog (coin types/cache mark, `PR-02`'s scale, actual map-sheet rebuild for the
  split-panel layout, comb's exposed-word mechanism, `PZ-20`'s Harald-trail `MEAD`, Constantinople's
  lock job, `PC-05`, `PC-18`, `ST-01`/`ST-02`, Rollo's rebus-distance measurement) unchanged.

## Session Close — 2026-09-16 (continued, 11) — Aud's treasure-route landmarks and map layout designed

**Task:** designed the actual four-step treasure route for `PZ-17`'s wrinkle (the in-person-only
observation clue), which last session deliberately left open pending this design pass.

**Real scale problem caught before committing to landmarks:** the first landmark proposal (mill,
Auðarsteinn, sheepfold, chapel pair, all clustered near Hvammur) would have collided on the actual
map — checked with real numbers rather than eyeballing it, since Rollo's map already hit exactly
this problem once (Rouen/Roumare, 10 km apart, landed 0.13 in apart on the printed sheet). Computed
Aud's map's real scale from its existing frame and grid (`build_trail_maps_pdf.py`): ~23 km per grid
cell. The whole Dalir area, where all four landmarks would sit, is smaller than that — they'd have
landed in the same one or two cells.

**Fix, decided in chat, sketched before writing:** split the one physical map sheet into two
side-by-side panels instead of spreading the landmarks across the wider region (which would have
lost the "coherent local trek" feel). Sketched the concept twice with the visualize tool before
locking it in — first version put a small corner inset over open water, which wasn't what the user
meant; second version, confirmed correct, shows the sheet split down the middle: a new zoomed detail
panel (Dalir/Hvammur, its own small grid) on one side, the existing full-region map shifted over,
completely unchanged in content, on the other.

**The four landmarks, finalized:**
- The old watermill, Auðarsteinn (real — Laxdæla saga ties this stone to Aud's own death account
  near Hvammsfjörður), and a sheepfold — all findable from the museum ticket's plain description.
- A lookalike chapel pair — the actual wrinkle. One sits at **Bjarnarhöfn**, the decoy card AD's own
  real site, making it a plausible wrong answer since that location is already "in play" as a card.
  The other is the real target. Card A2's message carries the one distinguishing detail (exact
  wording still unwritten) that tells players which chapel is correct.

**Saved a real sketch into the project**, not just chat: `Diagram_Aud_Map_Split.svg`, matching the
existing diagram files' self-contained style (hardcoded hex, no external classes) rather than the
visualize tool's runtime-dependent widget markup, since that widget CSS wouldn't render standalone
in the static page.

**Written into `Norse_Brainstorm.html`:** `PZ-17` gained the finalized four-landmark list and the
new figure/diagram with caption; `PZ-09`'s Aud bullet — still describing the old, dropped
`KAMBR`/Kambsnes idea from before `SOLE` even existed — corrected to point at the real, current job.

### Files changed

- `NorseBackpack/Art/Diagrams/Diagram_Aud_Map_Split.svg` — new.
- `NorseBackpack/Norse_Brainstorm.html` — sections listed above.

### Checks run

- Computed Aud's map's actual km-per-grid-cell from its real frame and grid constants in
  `build_trail_maps_pdf.py`, and the real lat/lon of every candidate landmark's anchor town, before
  proposing any landmark placement — caught the collision risk with numbers, not a guess.
- Full-file tag-balance check, including `figure` (new to this session) — all paired (1044 div, 13
  section, 36 article, 38 details, 16 ul, 125 li, 118 a, 11 table, 79 tr, 271 td, 41 th, 259 p, 260
  span, 8 ol, 84 figure).
- Fetched the new SVG directly over local HTTP — 200 OK, valid content. Scrolled it into view in the
  live page and screenshotted it to confirm it actually renders (not just that the file exists) —
  labels, split line, both panels and the caption all visible. No console errors.

### Next action

Write the actual hidden digits at each of the four landmarks and the resulting code; write A2's
missing distinguishing-detail sentence for the chapel pair (this unblocks A2's back/PDF, held back
since last session); write the museum ticket's front/back content; then A1, A3 and AD's card text.

### Blockers / open items

- No digits or resulting code chosen yet for the four landmarks.
- A2's card still can't be finished until the chapel-pair distinguishing detail is written.
- The museum ticket itself (front/back, "Aud's Treasure Museum") is unbuilt.
- The actual map-sheet rebuild (split-panel layout, new inset artwork) is a production task for
  `build_trail_maps_pdf.py`, not started.
- Pre-existing backlog (coin types/cache mark, `PR-02`'s scale, comb's exposed-word mechanism,
  `PZ-20`'s Harald-trail `MEAD`, Constantinople's lock job, `PC-05`, `PC-18`, `ST-01`/`ST-02`,
  Rollo's rebus-distance measurement) unchanged.

## Session Close — 2026-09-16 (continued, 10) — A2's text drafted; deliberately held back for a treasure-hunt wrinkle

**Task:** started writing Aud's cards, beginning with A2 (Hvammur) and the new museum ticket per
last session's decided sequence. Drafted A2's message and Fun Fact with the user (fact-checked via
WebSearch — Aud's real settlement history, freeing her thralls, Vífilsdalur). Caught and fixed one
redundancy along the way: the first message draft repeated the same fact as the Fun Fact almost
verbatim; the user flagged it, message was rewritten to a different angle (personal/sensory) so the
two don't overlap, matching the established pattern (message = voice/flavour, Fun Fact = trivia).

**New idea raised mid-draft, recorded but not designed:** the user proposed a wrinkle for `PZ-17`'s
treasure hunt — the museum ticket's written clues shouldn't be enough on their own to find the final
spot; one step should need an in-person-only observation (something Liv actually saw, not a fact
anyone could read off a ticket). The user's own instruction was explicit: **store the draft, design
the treasure hunt first, then come back and add the missing clue** — so A2's final message line
("They had a treasure hunt at the Aud museum today... Let's see if you would have been able to
solve it!") is a deliberate placeholder, not filler to be overwritten quietly later.

**Not done, on purpose:** A2's back and print PDF were not built. Building now would mean rebuilding
once the observation clue is added — the user's own sequencing call, not a shortcut taken here.

**Written into `Norse_Brainstorm.html`:** `PZ-05` gained A2's full drafted message/Fun Fact, marked
explicitly incomplete, plus its sources; `PZ-05`'s status pill updated (it was still stuck at "7 of
18 · 1 of 4 decoys," pre-dating last session's R1/R6/RD builds — now correctly "9 of 18 · 2 of 4
decoys · A2 drafted"); `PZ-17` gained a new note recording the in-person-observation wrinkle as a
candidate, not yet designed; A2's gallery-entry subtitle updated to match.

### Files changed

- `NorseBackpack/Norse_Brainstorm.html` — sections listed above. No image/PDF/build-script changes
  this session — text-only, and deliberately incomplete text at that.

### Checks run

- Full-file tag-balance check — all paired (1043 div, 13 section, 36 article, 38 details, 15 ul,
  121 li, 118 a, 11 table, 79 tr, 271 td, 41 th, 258 p, 260 span, 8 ol).
- Served over local HTTP (`static-preview`, port 8734) and confirmed via `document.body.innerText`
  checks (the Open questions tab's content isn't all in the DOM's visible scroll region at once, so
  plain text-search tools undercounted matches) that A2's message, Fun Fact, the updated PZ-05 status
  pill and the new PZ-17 wrinkle note all render. No console errors.

### Next action

Design `PZ-17`'s full four-step treasure route — including which step carries the in-person-only
observation and what that observation actually is — before touching A2 again or starting the museum
ticket's back content. A1, A3 and AD's card text are also still unwritten.

### Blockers / open items

- A2's card is incomplete by design: needs the in-person-observation clue before its back/PDF can be
  built.
- The four-step treasure-map route itself, the museum ticket's back content, the three coin
  types/cache mark, and AD's message are all still unwritten.
- Pre-existing backlog (`PR-02`'s scale, `PZ-20`'s Harald-trail `MEAD` mechanism, Constantinople's
  lock job, `PC-05`, `PC-18`, `ST-01`/`ST-02`, Rollo's rebus-distance measurement) unchanged.

## Session Close — 2026-09-16 (continued, 9) — Aud's full treasure/comb chain redesigned; gates entry to Harald's leg

**Task:** continuing leg 3's review, the user redesigned Aud's whole lock chain in chat to close two
gaps flagged in the review: Aud had no museum ticket, and decoy card AD (Bjarnarhöfn) had no lock
job under the standing "every card gates a lock" rule (`PZ-18`). Worked through the new sequence
with the user step by step before writing anything, per usual practice — this was a mechanism
redesign, not just card text.

**Decided in chat, full new sequence:**
1. Postcard A2 (Hvammur) + Aud's map + a new fictional ticket, **Aud's Treasure Museum** (tied to
   Hvammur; explicitly no historical-accuracy bar, unlike the other three trails' tickets) → give
   the treasure-map's 4-digit code.
2. That code opens a lock releasing the mixed coin hoard **plus postcards A1 (Dögurðarnes) and A3
   (Esjuberg) together** — a change from the old design, where Dögurðarnes alone produced the code
   and only got released later.
3. Since Hvammur's old "weigh it" instruction moved with it to step 1, **Dögurðarnes now carries the
   weighing instruction instead**, pairing with Esjuberg's unchanged upside-down scale-display sketch
   to produce `SOLE` — preserves the original two-card weighing design the user remembered, just with
   the two jobs swapped between cards.
4. `SOLE` opens a lock releasing **decoy card AD (Bjarnarhöfn) and the comb together** — AD's message
   to carry a "to me, this is the real treasure" line (exact wording not yet written).
5. **The comb, laid across AD's message**, exposes words that open a lock **gating entry to Harald's
   leg** — Aud's whole chain must finish before Harald's can start.

**The comb moves back to Aud's trail**, reversing an earlier session's move to Harald's (which had
left it with no exact card set or answer there anyway). The user called this a better fit; checking
the doc confirmed why — `HI-02` already ties a comb specifically to Aud's own documented saga history
(Landnámabók's account of the comb she lost at Kambsnes, which is what names the headland), so an
unconnected Harald assignment was always weaker than this.

**Effect on `PZ-18`'s decoy rule:** Bjarnarhöfn was one of two decoys still short of the "every card
gates a lock" standard (the other being Constantinople, still open). This closes it.

**Written into `Norse_Brainstorm.html`:** `PZ-03` and `PZ-17` rewritten for the new sequence (`PZ-17`
gained a numbered player-flow list); new lockflow diagram for Aud's full chain in the Locks tab,
matching the style of Leif's and Rollo's; two new/updated rows in the Locks-tab summary table plus a
new row for the comb-grille/Harald-gate lock; the card-family matrix's Family C and F rows and its
figcaption; the comb-grille design-guide section flipped back to Aud with its new job description;
the museum-ticket panel and Final-riddle constraint worksheet both updated now that Aud has a ticket;
both `PZ-18`-rule status paragraphs (Story & sequence tab) updated to move Bjarnarhöfn from
"still needs one assigned" to done.

### Files changed

- `NorseBackpack/Norse_Brainstorm.html` — sections listed above.

### Checks run

- Full-file tag-balance check, including `ol` (new to this session's edits) — all paired (1042 div,
  13 section, 36 article, 38 details, 15 ul, 121 li, 116 a, 11 table, 79 tr, 271 td, 41 th, 258 p,
  260 span, 8 ol).
- Served over local HTTP (`static-preview`, port 8734 — an existing server process was still
  running from an earlier session in this same conversation, but the browser pane's own tab
  reference had been lost; opened a fresh tab against the same server rather than starting a
  duplicate) and confirmed the new Aud lockflow diagram renders end to end, all five stages, with
  no console errors.

### Next action

Aud's cards (A1, A2, A3, AD) and the new Aud's Treasure Museum ticket still need to be actually
written and built — same as before this session, but now with a fully decided sequence to write
against instead of an open question. AD's exact message text and the comb's exposed-word mechanism
are the two pieces most tightly coupled to writing the cards themselves, so probably start there.

### Blockers / open items

- No card text exists yet for any of Aud's four cards or the new museum ticket.
- The four-step treasure-map route, its digits, and the three coin types/cache mark are still
  undecided (`PZ-17`).
- The comb's exposed-word mechanism and resulting Harald-gate code are entirely open — needs AD's
  message text to exist first, since the comb reads that message.
- No physical scale (>370.56 g capacity, 0.01 g resolution) bought or tested (`PR-02`).
- Constantinople (Harald's decoy) is now the only decoy still short of a lock job (`PZ-18`).
- Pre-existing backlog (`PC-05`, `PC-18`, `ST-01`/`ST-02`, Rollo's rebus-distance measurement,
  `PZ-20`'s Harald-trail `MEAD` mechanism) unchanged.

## Session Close — 2026-09-16 (continued, 9) — New project: CABER retirement game (online, 5 gates)

**Task:** brainstormed, then built, a short online escape game for a colleague's hybrid retirement
party. Domain is energy efficiency in buildings; premise is repairing a heat pump that is losing
refrigerant. Target play time 10–15 minutes, five gates. This is a new project unrelated to Norse,
Aurora, Lego or Hiking.

**Design agreed in chat:** CABER is both the project codename and the five-stage repair procedure,
one letter per gate — **C**onfirm the unit, **A**ssess the envelope, **B**alance the charge,
**E**valuate performance, **R**estart and hand over. Three facts about the retiree are wired into
the answers: start year 2001 (gate C answer), 25 years of service echoed by the faulty COP of 2.5
(gate E answer), and the retirement date 28 September 2026 (final handover code `280926`). The
closing reveal is that the unit being handed over was never the heat pump. Retiree name: Maria.

**Deliberate design decision — the timer never fails you.** The 20-minute refrigerant gauge drains
and changes the wording of the ending, but floors at 4% and never locks anyone out. A hard lose
state at a party with remote guests was judged worse than no lose state.

**Tone call made without an explicit answer from the user:** they supplied the name but not the
sentimental-vs-teasing preference that was asked for alongside it. Built as warm with one light dig
(the gate E note about nobody listening about writing readings down). Easy to soften — it is a
single `.note` string in the gate E render function.

### Files changed

- `Maria.html` — new, at the repo root. Self-contained single-file game: no backend, no
  network, no build step. Opens from a plain URL on any device. `RETIREE` object at the top of the
  script holds name/start year/end date so the game can be re-skinned for another party.

### Checks run

- Served over local HTTP (`static-preview` config, port 8734 was already occupied by a running
  `python -m http.server`, so navigated to it rather than starting a second copy).
- Played the full five-gate sequence to the finale in the in-app browser. All gates solve, all five
  letters light, finale renders. No console errors at any point.
- Tested the wrong-answer path on every gate that has one: wrong serial, four decoy hotspots on the
  thermal image, all three wrong fault diagnoses, out-of-order procedure.
- Checked at 375×812 (mobile) as well as desktop. No horizontal scroll.
- Hint system exercised: both nudges display, button correctly disappears after the last hint.

### Fixed during verification

- Letters lit one stage early (off-by-one: gate 0 is the briefing).
- `.bar` padding overrode `.wrap` padding, so the header had no side gutter at any width.
- Gauge tiles stacked 1-up on mobile (6 tiles = excessive scrolling); now 2-up.
- Only the top window row had a hotspot, so clicking 2nd/3rd floor windows gave no feedback at all.
- Thermal-bridge hotspots were ~15px tall on a phone; enlarged, and layered above the window
  hotspots so an ambiguous tap resolves in favour of the correct answer.

### Next action

Fill the three placeholder slots on the finale with real photos or messages. The game is committed
and live at https://ottawavisuals.github.io/EscapeBackpack/Maria.html but is NOT linked from
`index.html` — left unlinked on purpose so the landing page does not spoil it before the party.

### Open / not done

- Tone not confirmed by the user (see above).
- The finale has three placeholder slots ("Photo slot 1", "Photo slot 2", "Message from the team").
  Real photos or messages have not been added and no asset work was done.
- Not tested with more than one simultaneous player, and there is no shared state between devices —
  everyone plays their own copy. Fine for a screen-shared party, worth knowing if the plan changes.
- Not hosted anywhere. Delivery method (emailed file, GitHub Pages, or shared screen) is undecided.

## Session Close — 2026-09-16 (continued, 8) — Leg 3 (Aud) reviewed; MEAD pinned as a Harald-trail idea

**Task:** reviewed leg 3 (Aud the Deep-Minded) the same way legs 1 and 2 were reviewed. Found Aud
is the least-built trail so far — all 4 cards (A1, A2, A3, AD) have front art only, zero messages/
backs/PDFs, and Aud has no museum ticket at all (unlike Leif, Rollo and planned Harald). The lock
mechanism and answer (`SOLE`) are decided in principle, but the actual treasure-map route, coin
design and a physical scale check are all still open. Did not start writing Aud's cards this
session — the user redirected mid-review to a smaller, adjacent decision instead.

**Found stale while reviewing:** two leftover references (Props tab, Puzzle-details tab) still
described the owned four-letter lock's answer as "`MEAD` proposed" — pre-dating `PZ-03`'s decision
weeks ago to use `SOLE` for Aud's trail instead. Not caught by whatever swept `PZ-03` at the time.

**Decided in chat:** rather than let `MEAD` disappear as dead history, the user proposed reusing it
on Harald's trail (leg 4) instead — pinned as a new idea, not designed. It has a natural anchor:
Harald's crest-element set already includes a drinking horn (`PZ-16`). Deliberately did not invent
a mechanism for it (a second physical lock? the still-jobless comb prop, per `PC-06`?) — leg 4
hasn't had its own review pass yet, so forcing a mechanism now would be guessing ahead of the
session's own pattern.

**Written into `Norse_Brainstorm.html`:** new `PZ-20` records the `MEAD`-for-Harald idea with its
open mechanism question; both stale `MEAD` references (Props tab's `PR`-adjacent owned-lock note,
Puzzle-details tab's comb-reveal row) corrected to point at `SOLE` (decided, Aud) and cross-link to
`PZ-20` instead of implying `MEAD` was still an open candidate for Aud's own lock.

### Files changed

- `NorseBackpack/Norse_Brainstorm.html` — new `PZ-20`; two stale `MEAD` references fixed.

### Checks run

- Full-file tag-balance check — all paired (1025 div, 13 section, 36 article, 38 details, 15 ul,
  116 li, 116 a, 11 table, 78 tr, 264 td, 41 th, 258 p, 257 span).
- Served over local HTTP (`static-preview`, port 8734) and confirmed all three `PZ-20` mentions
  (the entry itself plus its two cross-links) render. No console errors.

### Next action

Aud's cards (A1 Dögurðarnes, A2 Hvammur, A3 Esjuberg, AD Bjarnarhöfn) still need messages, Fun
Facts, backs and print PDFs — same starting point leg 2's session began from, but Aud has further
to go (zero of four built vs. Rollo's four of seven). The treasure-map route, coin design, and
`MEAD`'s mechanism on Harald's trail (`PZ-20`) are the other open threads, but per this session's
own working pattern, leg 4 gets its own review pass before any of that gets designed.

### Blockers / open items

- Aud has no museum ticket yet, unlike every other trail.
- The four-step treasure-map route, its 4-digit code, and the three coin types/cache mark are all
  undecided (`PZ-17`).
- No physical scale (>370.56 g capacity, 0.01 g resolution) has been bought or tested (`PR-02`).
- `PZ-20`'s mechanism is entirely open — needs leg 4's own review before it can be designed.
- Pre-existing backlog (`PC-05`, `PC-18`, `ST-01`/`ST-02`, Rollo's rebus-distance measurement)
  unchanged.

> Session continuity only. Open design questions are **not** tracked here — they live in the
> Open questions tab of `NorseBackpack/Norse_Brainstorm.html`, each with a stable ID.
> See "Where Design State Lives" in `AGENTS.md`.

## Session Close — 2026-09-16 (continued, 7) — Rollo's three missing cards written and built; two stale-doc sweeps

**Task:** reviewed leg 2 (Rollo's trail) with the user the same way leg 1 was reviewed. Found two
doc-accuracy bugs (fixed) and three unwritten cards (R1 Châlus, R6 Roumare Forest, RD Walcheren) —
the only three Rollo-trail cards with no message/back/PDF, all three feeding `PZ-19`'s
counting-in-the-illustration lock. Wrote and built all three, redesigning the lock's mechanism with
the user along the way.

**Doc bugs fixed (no design change):**
- Locks-tab summary table still listed postcard R2 as `06` (leftover pre-rename numbering).
- `PZ-19`'s counting lock had no row at all in that same summary table, despite being fully decided.

**Mechanism redesigned in chat, then built:** the original `PZ-19` put the sorting job in each
card's handwritten message ("before that," "between the two"). Discussing the draft messages
surfaced a real conflict — the decided read order (Walcheren → Roumare → Châlus) is historical-era
order, not Liv's actual trip order, and moving that logic into "natural" handwriting was getting
contrived. The user's revision: the *sorting* clue moved into each Fun Fact instead, as a real
date/century (checked against the doc's own already-sourced history — Walcheren "before 911" via
Dudo of Saint-Quentin, Roumare "911" via Rollo's own grant, Châlus "1199," Richard's death); the
*handwriting* now just mentions the counted object (boats/boars/bolts) without stating a number.
The user also added a twist: Roumare's drawn count (3 boars) is doubled to 6 for the actual lock
digit, hinted at in-voice rather than stated ("for every one I actually saw, I'd bet good money
there was a second one just out of sight"). Checked first that doubling was even valid on all
three — Walcheren's 5 would double to 10, not a valid single lock digit, so only Roumare or Châlus
could take the twist; the user picked Roumare. **Code changed from the old draft's `532` to `562`**
(5, 6-doubled-from-3, 2) — checked against every other code in the page, no collision.

**Fact-checked before writing** (WebSearch, since Fun Facts are presented as real trivia): Richard
the Lionheart's 1199 death at Châlus-Chabrol (crossbow bolt, gangrene, 6 April, the executed-shooter
detail — trimmed from the final card text for space, not for accuracy); Roumare's genuine wild-boar
wildlife park; Walcheren's real Viking-age history. Deliberately did **not** invent a specific
etymology for "Roumare" itself when a search only turned up the etymology for a different, nearby
forest (Forêt de Rouvray) — the card's Fun Fact hedges the naming legend instead of stating an
unverified origin as fact.

**Built** `build_postcard_{R1,R6,RD}_pdf.py` (new, modelled on `build_postcard_R2_pdf.py` — no
rebus, place-only postmark already matching the earlier session's decision). Two production issues
caught by inspection, not assumed fixed:
- R1's Fun Fact overflowed its box by two lines; trimmed (dropped the executed-shooter sentence).
- R6's and RD's postmark place-names (`ROUMARE`, `WALCHEREN`) were long enough to poke past the
  inner circle rule at the standard 4.8pt — sized down per-card (4.2pt, 3.3pt) until each fit
  cleanly, checked by cropping and inspecting the rendered PNG at each step rather than guessing a
  size and moving on.

**Written into `Norse_Brainstorm.html`:** `PZ-19` rewritten in full (new mechanism, new code, all
three messages/Fun Facts quoted, doubling-twist reasoning); the Locks-tab table's counting-lock row
and the Rollo constraint-worksheet row updated to the new code and mechanism; three postcard gallery
entries got their back image, View PDF link and updated captions; Rollo's trail-grid header changed
from "4 of 6 real built" to "6 of 6 real built · decoy built"; three trail-grid boxes gained
checkmarks.

**Also swept while in there:** the "postmark date still pending" / "postmark has no date yet
(PC-03/PC-04)" caption on L2, L3, LD, R2, R3, R4 and R5 — seven cards, all stale since last
session's decision that postmarks never carry a date at all. Replaced with "postmark carries place
only, no date." L1's caption also still described the now-removed `07 JUL` date and underline;
fixed to match the rebuilt back.

### Files changed

- `NorseBackpack/Postcards/build_postcard_{R1,R6,RD}_pdf.py` — new.
- `output/pdf/Postcard_{R1_Chalus,R6_Roumare_Forest,RD_Walcheren}_{Print,Letter_Print}.pdf` — new.
- `NorseBackpack/Postcards/Postcard_{R1_Chalus,R6_Roumare_Forest,RD_Walcheren}_Back.png` — new.
- `NorseBackpack/Norse_Brainstorm.html` — sections listed above.

### Checks run

- `python -m py_compile` on all three new build scripts — no syntax errors.
- Ran all three scripts; rendered each PDF's back page to PNG at 300 dpi and opened every one
  directly to check layout, wrap and postmark fit — caught and fixed the R1 overflow and the
  R6/RD postmark-circle overflow this way, not by assuming the first render was correct.
- Full-file tag-balance check on the HTML — all paired (1020 div, 13 section, 36 article, 38
  details, 15 ul, 116 li, 116 a, 11 table, 78 tr, 264 td, 41 th, 258 p, 256 span).
- Manually recomputed the Fun-Fact text box's actual usable width in `build_postcard_R1_pdf.py`
  after the first render overflowed — found the wrap-width variable had used the wrong reference
  point (`rule_right` instead of the box's real right edge), explaining the overflow; verified the
  corrected wrap fits in 6 of ~7 available lines before rebuilding.
- Checked `562` against every other code in the page (`1021`, `1576`, `1972`, `231`, `253`, `427`,
  `582`, `2468`) — no collision.
- Served over local HTTP (`static-preview`, port 8734, already running from another session) and
  scrolled to all three new gallery entries plus LD's (spot-checking the caption sweep): images
  load (200 OK), captions read correctly, no console errors.

### Next action

Rollo's trail is now fully built end to end (all 6 real cards + decoy, all with backs and PDFs).
Remaining open items are the same ones flagged after leg 1: which physical lock the word-lock
(`RIGHT, DOWN, DOWN, UP, LEFT, LEFT`) and this new counting lock (`562`) each feed (`ST-01`), and
the rebus-distance lock's code is still unmeasured against the real printed map (`PZ-14`). `PC-05`
(family D's missing selection rule), `PC-18` (in-game release order) and leg 3/4 (Aud, Harald) are
still untouched.

### Blockers / open items

- `ST-01`/`ST-02` (which physical lock each Rollo mechanism feeds) still entirely open.
- `PZ-14`'s rebus-distance code needs a real 1:5 scale measurement against the printed map.
- Pre-existing backlog (`PC-05`, `PC-18`, Harald's Kyiv → Hedeby → Syracuse zigzag) unchanged.

## Session Close — 2026-09-16 (continued, 6) — Leif's leg-1 release order decided; postmark dates dropped entirely; card L1 rebuilt

**Task:** the user asked to review the first leg of the journey (Leif's trail) — what postcards/props/locks exist for it. While reviewing, the user made two decisions in chat: (1) the exact release order for Leif's three-lock opening, resolving `PZ-18`'s open item on where decoy card LD gets released, and (2) drop postmark dates from the design entirely (place-only stamp), superseding the whole "interleaved dates" ordering mechanism.

**Decided in chat:**
- **Leif's release order (`PZ-13`, now fully decided):** card L1 is given at the start → Lock 1 (`1021`) releases decoy card LD + Leif's map + the museum ticket together → Lock 2 (`BEAR 3212`, the beasts chain using LD's imprint) releases cards L2 and L3 together → Lock 3 (`1576`, hold-to-light on L2+L3) opens a fourth container. This changes what Lock 1 and Lock 2 each release — previously Lock 1 sent out card L2 and Lock 2 sent out card L3 alone.
- **Postmarks carry place only, never a date** — not even as flavour, confirmed after asking the user to clarify scope (a full removal of the postmark graphic was the other option; place-only flavour was chosen). This drops the entire "interleaved dates" mechanism and closes `PC-02`/`PC-03`/`PC-04` as moot rather than leaving them open or blocked.

**Written into `Norse_Brainstorm.html`:**
- Leif's lockflow diagram and the Locks-tab lock table updated to the new release order; also fixed stale `01`/`04`/`02 + 03` postcard-column numbering in that table left over from the September `PC-17` rename (should have read `L1`/`LD`/`L2 + L3`).
- `PZ-13` changed from "candidate, re-check needed" to **Decided**; `PZ-10` changed from "superseded (candidate)" to **Superseded** (placement confirmed, no more re-check needed).
- `PC-02`/`PC-03`/`PC-04` changed from Open/Blocked to **Resolved/Removed**, each explaining why (no date field exists at all now).
- The "Interleaved dates" designsection marked **Superseded**, reasoning kept below per `AGENTS.md`'s "say so where the old text was" rule.
- Design spec table's "Postmark date" row removed (struck through, marked Removed).
- Fixed three other stale mentions found while sweeping: `PC-08`'s "once dates are assigned" line, `PZ-08`'s "exact date is open again under the calendar start" line, and the Postcards tab's intro paragraph (still said card LD's release point and postmark dates were both open — both were decided this session).
- Next-steps punch list item changed from "settle the date span, assign all 18 postmark dates" to "rebuild card L1's back to drop its postmark date."

**Rebuilt card L1's back** (`build_postcard_L1_pdf.py`): removed the date-drawing block (`07 JUL` text, the day-underline, the width calculations feeding it) and re-centred the two-line place text (`L'ANSE AUX` / `MEADOWS`) vertically in the postmark circle to fill the space the date left behind. Rebuilt `Postcard_L1_LAnse_{Print,Letter_Print}.pdf` and re-rendered `Postcard_L1_LAnse_Back.png` (300 dpi from the PDF's back page, matching the gallery's existing 1500×1050 size) for the gallery.

### Files changed

- `NorseBackpack/Norse_Brainstorm.html` — sections listed above.
- `NorseBackpack/Postcards/build_postcard_L1_pdf.py` — postmark date removed, place text re-centred.
- `output/pdf/Postcard_L1_LAnse_{Print,Letter_Print}.pdf` — rebuilt.
- `NorseBackpack/Postcards/Postcard_L1_LAnse_Back.png` — rebuilt.

### Checks run

- Full-file tag-balance check on the HTML — all paired (1019 div, 13 section, 36 article, 38 details, 15 ul, 116 li, 113 a, 11 table, 77 tr, 257 td, 41 th, 258 p, 251 span; td dropped by 2 from the postmark-date row's `colspan` collapse, expected).
- `python -m py_compile build_postcard_L1_pdf.py` — no syntax errors; confirmed `pdfmetrics` import still used elsewhere before assuming it was safe to leave in place.
- Rebuilt the PDF and rendered its back page to PNG at 300 dpi; opened it directly and visually confirmed no date, no underline, and the place text sits centred in the circle.
- Served over local HTTP (`static-preview`, port 8734, already running from another session — joined rather than starting a duplicate) and confirmed the gallery image request returns 200 OK with the new file's byte size. The Browser pane's own `<img>` cache initially still showed the old `07 JUL` version after reload; force-refetching the image confirmed the live page does serve the corrected art. No console errors.

### Next action

Leif's leg is now fully consistent front-to-back (art, backs, lock sequence, no dangling date mechanism). Move to another trail or open item — `PC-05` (family D's missing selection rule), `PC-18` (in-game release order across all 22 cards), or the per-trail decoy narrative placement (`PC-16`) are the next unresolved items in the Open questions tab.

### Blockers / open items

- None new from this session. Pre-existing backlog (per-trail decoy slot `PC-16`, in-game release order `PC-18`, Harald's Kyiv → Hedeby → Syracuse zigzag) is unchanged.

## Session Close — 2026-09-16 (continued, 5) — PC-19 fixed: painted the missing title band on Harald's six off-spec fronts

**Task:** the user picked a direction for `PC-19` (six of Harald's fronts had the title baked
straight onto full-bleed art, no blank band underneath, unlike the rest of the series): "build
the strip and text over it" — composite the missing band myself rather than sending the art back
to Codex, since this is a build-script fix, not new asset generation.

**Fixed in `build_postcard_front_images.py`:** added a `NEEDS_BAND` set (the six affected output
filenames) and, in `build_card()`, paint a solid deep-navy rectangle over the lower 20% plus a
thin cream divider line — sampled from the already-correct cards' own bands `(18, 52, 60)` navy,
`(235, 226, 185)` divider, not invented — before the existing title/subtitle drawing code runs.
Scoped to exactly those six by filename check so the sixteen already-correct fronts take the same
code path they always did.

**Rebuilt only the six affected cards**, not the whole deck — ran `build_card()` directly on the
six `NEEDS_BAND` entries rather than `main()` (which reruns all 22 and hit an intermittent Windows
file-lock error partway through on unrelated files, likely antivirus scanning a freshly-written
PNG; retrying the full run didn't help, so it seemed safer to scope down to the six that actually
needed changes anyway). Rebuilt from each card's clean `Illustration_v1.png` source (which never
had a baked title), not by patching the broken `_Front.png` — avoids any leftover double-text
artifact from the old bad composite.

**Verified, not assumed:** hashed the three known-good fronts (`L1`, `H1`, `A1`) before and after —
identical, confirming the fix didn't touch anything outside the six targets. Opened both fixed
images directly and visually confirmed the band and clean title match `H1`'s established look.
Fetched the live served image through the running preview server and sampled a pixel in the band
region — exact navy `(18, 52, 60)`, confirming the server isn't caching the old broken version.

**Written into `Norse_Brainstorm.html`:** `PC-19` changed from "Needs a decision" to **Fixed**,
with what actually happened; removed the "(title-band deviation, PC-19)" flag from all six gallery
captions (no longer true); corrected the Postcards tab intro paragraph, which had said six fronts
had a layout deviation — now says all 22 fronts match the standard layout.

### Files changed

- `NorseBackpack/Postcards/build_postcard_front_images.py` — `NEEDS_BAND` set, band-painting in
  `build_card()`.
- `NorseBackpack/Postcards/Postcard_{H2_Staraya_Ladoga,H3_Kyiv,H4_Hedeby,H5_Sicily,H6_Patara,
  HD_Constantinople}_Front.png` — rebuilt in place with the band.
- `NorseBackpack/Norse_Brainstorm.html` — `PC-19` status and body, six gallery captions, intro
  paragraph.

### Checks run

- `python -m py_compile build_postcard_front_images.py` — no syntax errors.
- MD5 hash of `Postcard_{L1_LAnse,H1_Oslo,A1_Dogurdarnes}_Front.png` before and after the six-card
  rebuild — unchanged, confirming no collateral changes to already-correct cards.
- Opened `Postcard_H2_Staraya_Ladoga_Front.png` and `Postcard_HD_Constantinople_Front.png` directly
  and visually inspected the band/title against `H1`'s known-good layout.
- Full-file tag-balance check on the HTML — all paired (1018 div, 13 section, 36 article, 38
  details, 15 ul, 116 li, 113 a, 11 table, 77 tr, 259 td, 41 th, 258 p, 251 span).
- Fetched the live image through the running `static-preview` server via `fetch`/canvas and
  sampled a band pixel — exact match to the intended navy, confirming the server serves the
  rebuilt file and not a stale cached copy. No console errors on the Postcards tab.

### Next action

Start writing backs/messages for whichever card the user wants next — `PC-19` no longer blocks
that decision for Harald's cards.

### Blockers / open items

- Per-trail decoy slot (`PC-16`) and in-game release order (`PC-18`) are both still unstarted.
- Harald's Kyiv → Hedeby → Syracuse zigzag is still an accepted known risk, unaffected by this
  session.
- Only `H3` Kyiv, `H4` Hedeby and `H5` Sicily were not individually re-opened and eyeballed after
  the rebuild (only `H2` and `HD` were); they ran through the identical code path as those two, but
  a full visual pass on all six before printing is still worth doing.

## Session Close — 2026-09-16 (continued, 4) — Harald's remaining fronts synced; new PC-19: six of them break the title-band spec

**Task:** the user said Codex finished the remaining postcard artwork and asked me to review and
update the design doc's text to match. Found that Harald's six missing fronts (`H2` Staraya
Ladoga, `H3` Kyiv, `H4` Hedeby, `H5` Sicily, `H6` Patara, `HD` Constantinople decoy) now exist —
the trail-grid boxes and counts were already synced (by Codex or a parallel session; not this
one), and the gallery already had full entries with sources and exact prompts for all six. All 22
cards now have front art.

**Real problem found while reviewing, not assumed fixed:** opened all six new fronts (plus `H1`
Oslo as a known-good baseline) to actually look at them rather than trust the "front artwork
built" status line. `H1` correctly reserves the lower ~20% as a blank navy title band, matching
every other card in the series (`PC-13`'s standard). The six new ones do not — the place name and
country are baked directly onto the scenery with a drop-shadow, no band underneath. Checked the
prompts already recorded in the gallery: they explicitly ask for "full-bleed image... the title
band will be added separately," so whatever step was meant to add that band on top either didn't
run for these six or used a different method than the rest of the series. This is a real visual
inconsistency across a third of the deck, not a nitpick — flagged as **new `PC-19`**, cross-linked
from each of the six affected gallery captions. Not fixed here: regenerating/recompositing
artwork is Codex's job per `AGENTS.md`'s role split, so `PC-19` asks for a decision (redo the six,
or accept the deviation and rewrite the other sixteen's captions) rather than picking one myself.

**Also fixed while syncing:** the Postcards tab's intro paragraph still said the decoy-per-trail
card count was "not yet built," which stopped being true once Aud's and Harald's decoys got front
art across earlier sessions. Rewritten to state plainly that front art now exists for all 22, only
Leif's four are fully built end to end, and to point at `PC-19`.

### Files changed

- `NorseBackpack/Norse_Brainstorm.html` — new `PC-19` open item; six gallery captions
  cross-linked to it; intro paragraph corrected.

### Checks run

- Opened `Postcard_H1_Oslo_Front.png` (baseline) and all six new fronts directly and compared
  band treatment by eye — confirmed the deviation on all six, not assumed from one sample.
- Full-file tag-balance check — all paired (1018 div, 13 section, 36 article, 38 details, 15 ul,
  116 li, 113 a, 11 table, 77 tr, 259 td, 41 th, 258 p, 251 span).
- Served over local HTTP and confirmed live: all six new front images return 200 OK, no console
  errors, and all 8 `PC-19` references (1 open-question row, 1 intro paragraph, 6 gallery
  captions) render.

### Next action

Get a decision on `PC-19` — send `H2`–`H6`/`HD` back for a title-band pass, or accept the
full-bleed treatment and update the rest of the series' captions instead.

### Blockers / open items

- `PC-19` needs a decision before any of these six get backs/messages built (building on top of
  an art layout that might still change would be wasted work).
- Per-trail decoy slot (`PC-16`) and in-game release order (`PC-18`) are both still unstarted.
- Harald's Kyiv → Hedeby → Syracuse zigzag (from the Patara swap session) is still an accepted
  known risk, unaffected by this session.

## Session Close — 2026-09-16 — Harald postcard front art

**Task:** build the six remaining Harald postcard fronts from user-selected Wikimedia Commons sources.

**Done:** H2 Staraya Ladoga, H3 Kyiv, H4 Hedeby, H5 Sicily, H6 Patara and HD Constantinople (decoy) now have 1500 × 1050 px, 300 dpi front art and raw ImageGen sources in `NorseBackpack/Postcards/`. The front-image builder, postcard gallery, Harald trail overview and source register are updated. Sources: Hunanuk (CC0); Pannuccis, Александр Байдуков, Rbrechko and Matti Blume (CC BY-SA 4.0); Erp (CC BY 2.5).

**Checks:** visually inspected each source and generated illustration; normalized each to the PC-13 canvas without rescaling.

**Next action:** write Harald postcard backs and print PDFs when their clue text is decided.

## Session Close — 2026-09-16 (continued, 3) — Harald's Asia Minor stop swapped Melitene → Patara

**Task:** the user asked to swap Harald's illustrative Asia Minor stop to Yümüktepe (Mersin),
citing "the recent discovery of a Viking sword there." Checked the claim before touching anything,
per `AGENTS.md`'s "say when you do not know" rule — this is a real-world historical fact being
added to a sourced dataset (`stops.js`'s evidence-category system exists specifically to keep
sourced fact separate from illustrative choice), not a design opinion to take on faith.

**What the fact-check found:** a Viking-age sword really was found at Yümüktepe, but in **2010**,
not recently, and it wasn't tied to Harald specifically (general Byzantine-era Norse/Varangian
evidence in Anatolia). A second, later find at **Patara** (Antalya province, 2018) got the actual
recent news coverage and better matches "recent discovery." Neither sword is attested to Harald
himself — same caveat that already applied to the outgoing Melitene pick. Asked the user which
one they meant and how far to take it; they chose **Patara, full rebuild** (not record-only).

**Decided and changed:** Harald's `h-anatolia` stop is now **Patara · Asia Minor** (36.27, 29.29),
evidence category stays `illustrative` (a real site with genuine Viking-era material evidence, but
still not a sourced fact about Harald's own presence there), sourced to the Daily Sabah article on
the 2018 find.

**Rebuilt Harald's trail map** (`build_trail_maps_pdf.py harald`) since the build script reads
stop coordinates from `stops.js` at build time, not from a hardcoded value — no code change
needed there, just the data swap. **Rendered and inspected the new `ANSWER` PDF directly** rather
than assuming the swap fixed or worsened the shape: Patara sits at nearly the same latitude as
Syracuse, so the final leg (Syracuse → Patara) now draws a cleaner, shorter, flatter rightward
stroke than the old Melitene endpoint did. The route's actual documented problem — the zigzag
between Kyiv → Hedeby → Syracuse (points 3–4–5), which reverses direction instead of continuing
a smooth diagonal — is unchanged by this swap, since it doesn't involve the endpoint that moved.
Still an accepted known risk from an earlier session, not fixed and not worsened here.

### Files changed

- `NorseBackpack/TravelMap/stops.js` — `h-anatolia` entry (name, coordinates, note, source key);
  replaced the now-unused `meliteneHistory` source entry with `pataraSword`.
- `NorseBackpack/TravelMap/Norse_Aunt_Route_Plan.json` — matching update to the embedded
  `visits.harald` copy of the same stop.
- `NorseBackpack/Norse_Brainstorm.html` — three prose mentions (`PZ-09`'s build note, the trail
  map caption, and the Travel routes tab's static source-citation list item, which duplicates
  `stops.js` content by hand per an earlier session's finding that it isn't runtime-driven).
- `output/pdf/Trail_Map_4_Harald_{Print,ANSWER}.pdf` — rebuilt with Patara's real coordinates.

### Checks run

- `python -c "import json; json.load(...)"` — route plan JSON still parses after editing.
- Full-file tag-balance check on the HTML — all paired (995 div, 13 section, 30 article, 32
  details, 15 ul, 116 li, 107 a, 11 table, 77 tr, 259 td, 41 th, 246 p, 255 span).
- Rebuilt Harald's trail map via the real build script (not hand-edited), rendered the `ANSWER`
  PDF page to PNG with PyMuPDF and visually inspected the actual traced route rather than assuming
  the swap's effect on the digit-2 shape check.
- Served over local HTTP and confirmed live: the Travel routes tab's interactive Leaflet mini-map
  (which reads `stops.js` at runtime, unlike the static citation list) shows "Patara" correctly,
  and the hand-edited static citation + source link also render. No console errors.
- Repo-wide `grep` for "Melitene" across the three edited files — zero remaining.

### Next action

Write each decoy's place in Aunt Liv's travel story for its trail (`PC-16`'s open item, unaffected
by this session — carried over).

### Blockers / open items

- Harald's Kyiv → Hedeby → Syracuse zigzag (see above) is still an accepted known risk, not fixed.
- Per-trail decoy slot (`PC-16`) and in-game release order (`PC-18`) are both still unstarted.
- Pre-existing backlog (Walcheren's missing back/PDF, card `LD`'s release point, `AD`/`HD`'s lock
  jobs) is unchanged.

## Session Close — 2026-09-16 (continued, 2) — Postcards renamed to trail-letter + position codes (resolves PC-17); Aud's front art incorporated

**Task:** the user decided the canonical postcard numbering scheme (`PC-17`, left open earlier this
session): each card's code is its trail's first letter plus its 1-based position in that trail
(`L1`, `L2`, `L3` for Leif; `R1`–`R6` for Rollo; `A1`–`A3` for Aud; `H1`–`H6` for Harald), with each
trail's decoy as that letter plus `D` (`LD`, `RD`, `AD`, `HD`). Asked to rename both the HTML and
every file on disk to match. Also noted Codex had just finished Aud's front art in a parallel
session.

**Found already done:** Codex's Aud artwork (`Postcard_11_Dogurdarnes`, `_12_Hvammur`,
`_13_Esjuberg` fronts, plus the `Postcard_D_Bjarnarhofn` decoy front) had already landed on disk
and in the HTML's trail grid (real images, updated counts) before this session touched it — no
separate sync step was needed, just folding it into the rename.

**Renamed on disk** (`git mv` for tracked files, plain `mv` + `git add` for Codex's untracked new
files, since `git mv` refuses untracked paths): every postcard front/back/illustration/ImageGen
source PNG, the two Leif hold-to-light joint files (`Postcard_02_03_*` → `Postcard_L2_L3_*`), all
built print PDFs in `output/pdf/`, the References folder's ImageGen source copies, and all eight
`build_postcard_0X_pdf.py` scripts → `build_postcard_{L1,L2,L3,LD,R2,R3,R4,R5}_pdf.py`. Two
superseded dev-prototype files (`Postcard_01_Harbor_Base.png`, `Postcard_01_Prototype.html`) were
deliberately left unrenamed — they're not part of the live card pipeline.

**Fixed internal references so nothing 404s or fails to build:**
- `build_postcard_{L1,L2,L3,LD,R2,R3,R4,R5}_pdf.py` — `OUT`/`OUT_LETTER`/`FRONT` path constants,
  `setTitle` strings, and the size-check error message, all updated to the new filenames.
  Compile-checked with `python -m py_compile` after editing.
- `build_postcard_collection.py`, `build_postcard_front_images.py` — `CARDS` list entries and
  path comments updated to the new filenames.
- `build_topedge_test_sheet.py` — was still pointing at the old `Postcard_02_Battle_Harbour`/
  `Postcard_03_Baffin_Island` filenames and would have failed to find its input images; fixed.
- `Postcards/References/README.md` — every `Postcard NN`/`Postcard_NN_Name` mention and the stale
  "Postcard 13" mislabel on the Oslo photo (should have said 14 even under the old scheme) fixed.
- `Postcards/Image_Credits.html` — stale `Postcard 01/02/03` headings and a broken
  `href="Postcard_01_LAnse.html"` back-link fixed.
- `Postcards/Postcard_L1_LAnse.html`, `Postcard_L1_LAnse_Style_Study.html` — these old dev-preview
  pages (found while sweeping for stale references) had broken image/PDF links after the rename;
  fixed to point at the new filenames.

**Written into `Norse_Brainstorm.html`:**
- Every `Postcard_NN_*` filename token, `build_postcard_NN_pdf.py` mention, and prose "card
  NN"/"Postcard NN" reference across the whole page (gallery headings, figcaptions, `PZ-05`,
  `PZ-14`, the codes table, etc.) converted to the new codes — done with a scripted regex pass,
  not by hand, then swept twice more for leftovers a first-pass regex couldn't catch (mixed
  "letter + bare old number" forms like "R2–09", and old numbers following an already-converted
  code with no repeated "card" word, like "L2 and 03").
- Trail-grid `pc-num` badges now show the actual code (`L1`, `R6`, `HD`, …) instead of a bare
  per-trail digit — the two were always meant to be the same thing under this scheme, so showing
  both would just invite drift.
- `PC-17` changed from open to **Decided**: full code table for all 22 cards, and a note that this
  deliberately collapses "canonical numbering" and "per-trail order" into one code — there's no
  longer a separate continuous 01–22 sequence.
- `PC-16` updated to point at `PC-17` as resolved.
- **Real, pre-existing bug caught while sweeping, unrelated to the rename itself:** Roumare
  Forest's (`R6`) gallery figcaption still said "held back for the final bundle" — directly
  contradicting this session's earlier no-hold-back decision (`PC-16`). Fixed to "no longer held
  back... (PC-16)".

### Files changed

- ~90 renamed/added files under `NorseBackpack/Postcards/`, `Postcards/References/`, and
  `output/pdf/` (see `git status` — every rename shows as `R` or `RM`, nothing was deleted and
  re-added blind).
- `NorseBackpack/Postcards/build_postcard_{L1,L2,L3,LD,R2,R3,R4,R5}_pdf.py`,
  `build_postcard_collection.py`, `build_postcard_front_images.py`, `build_topedge_test_sheet.py`.
- `NorseBackpack/Postcards/References/README.md`, `Postcards/Image_Credits.html`,
  `Postcards/Postcard_L1_LAnse.html`, `Postcards/Postcard_L1_LAnse_Style_Study.html`.
- `NorseBackpack/Norse_Brainstorm.html` — sections listed above.

### Checks run

- `python -m py_compile` on all eight renamed build scripts plus the two shared scripts — no
  syntax errors.
- Full-file tag-balance check on the HTML (div/section/article/details/ul/li/a/table/tr/td/th/p/
  span) — all paired (995 div, 13 section, 30 article, 32 details, 15 ul, 116 li, 107 a, 11 table,
  77 tr, 259 td, 41 th, 246 p, 255 span).
- Repo-wide `grep` for `Postcard_(0[1-9]|1[0-4])_`/`Postcard_D_`/`build_postcard_0[1-9]_pdf` across
  `.py`/`.html`/`.md` — clean except `HANDOFF.md`'s own historical entries (intentionally not
  retconned) and the two dev-prototype files left unrenamed on purpose.
- Served over local HTTP (`static-preview`, port 8734, joined an already-running server) and
  checked `read_network_requests` on the Postcards tab: every `Postcard_*` image request resolved
  200 OK, none 404. `get_page_text` confirmed the trail grid, gallery headings and figcaptions all
  read the new codes correctly end to end.
- Visual screenshot verification was attempted but the Browser pane returned blank captures for
  this page regardless of scroll position, while `get_page_text`/`read_network_requests`/DOM
  inspection via `javascript_tool` all confirmed correct rendering and content — treated as a
  screenshot-tool issue in this session, not a page bug, but flagging it since it means this
  session's visual check leaned on text/network extraction rather than an actual screenshot.

### Next action

Write each decoy's place in Aunt Liv's travel story for its trail (`PC-16`'s remaining open item —
the per-trail decoy slot depends on this).

### Blockers / open items

- Per-trail decoy slot (`PC-16`) still needs each decoy's narrative placement written.
- In-game release order (`PC-18`) is unstarted.
- Screenshot capture in the Browser pane was unreliable this session (see Checks run) — worth
  retrying cold in a future session before trusting it for a visual-only check.
- Pre-existing backlog (Walcheren's missing back/PDF, card `LD`'s release point, `AD`/`HD`'s lock
  jobs) is unchanged.

## Session Close — 2026-09-16 (continued) — No postcards held back; Brattahlíð's decoy label fixed; three separate orderings named

**Task:** the user made three calls on the Postcards tab: (1) stop holding any postcards back for
the final container, (2) fix Brattahlíð, which was displaying as an ordinary numbered card ("04")
instead of a decoy in the "All 18, by trail" grid, and (3) recognize that postcard order is not one
thing — there's the order within each trail (including where each trail's decoy sits), a canonical
numbering independent of trail, and the order cards actually get released in play. Asked to start
with the decoy-placement question.

**Found while reading the tab:** Brattahlíð was the one decoy not flagged as a decoy — it showed
`04` with a checkmark like Leif's three real stops, while the other three trails' decoys correctly
showed `D` + a rust "Decoy" tag. This was a display bug relative to the other three, not a new
design call.

**Decided in chat:**
- No postcards are held back for the final container. This fully supersedes `PZ-11`'s hold-back
  mechanism (already noted as superseded-by-candidate on 15 Sept; now firmly decided) in favour of
  the one-decoy-per-trail filter (`PZ-18`).
- Each trail's decoy sits wherever it fits Aunt Liv's actual travel story for that leg — not a
  fixed slot (e.g. always last), and not chosen to optimize the map-shape read. The exact slot per
  trail is still open, since it depends on writing each decoy's place in her story, not done yet.
- The other two orderings — canonical 01–22 numbering, and in-game release/reveal order — are
  confirmed as separate questions from each other and from the per-trail order, and were not
  designed this session. Recorded as new open items rather than guessed.

**Written into `Norse_Brainstorm.html`:**
- Fixed Brattahlíð's box in the "All 18, by trail" grid to show `D` + "Decoy" like the other three
  trails, instead of `04` with just a checkmark.
- Removed the live "Held back"/"Held back?" labels from Roumare, Hvammur and Staraya Ladoga's boxes
  and the trail legend's "held back until the final container" line (now just "decoy").
- Rewrote the intro paragraph above the grid to state the no-hold-back decision plainly instead of
  describing a mechanism that's no longer in effect.
- `PZ-11`'s pill changed from "Superseded (candidate)" to plain "Superseded"; its opening line now
  states the 16 Sept decision explicitly.
- New `PC-16` (records both decisions above and flags PC-17/PC-18 as distinct), `PC-17` (canonical
  numbering, open), `PC-18` (in-game release order, open) in the Postcard system tab.

**Deliberately not done:** did not invent where in each trail's story a decoy falls (needs the
decoy's actual travel narrative, unwritten), did not invent a canonical numbering scheme, and did
not map the release order — all three need their own design passes, not a guess to fill space.

### Files changed

- `NorseBackpack/Norse_Brainstorm.html` — sections listed above.

### Checks run

- Served over local HTTP (`static-preview`, port 8734, already running from another session —
  joined rather than starting a duplicate) and viewed the Postcards tab live: all four trail groups'
  decoy boxes now render consistently (`D` + rust "Decoy" tag), no more "Held back" labels anywhere
  in the grid, legend shows "decoy" instead of the old PZ-11 wording. No console errors.

### Next action

Write each decoy's place in Aunt Liv's travel story for its trail (needed before the per-trail
decoy slot in `PC-16` can be pinned down), starting with whichever trail's decoy the user wants to
tackle first.

### Blockers / open items

- Per-trail decoy slot (`PC-16`) needs each decoy's narrative placement written first.
- Canonical numbering (`PC-17`) and in-game release order (`PC-18`) are both unstarted.
- Pre-existing backlog below (Walcheren's missing back/PDF, card 04's release point, Bjarnarhöfn/
  Constantinople's lock jobs) is unchanged.

## Session Close — 2026-09-16 — PZ-19's three counts confirmed; caught and fixed a digit-order bug

**Task:** picked up `PZ-19` (the Châlus/Roumare/Walcheren "counting in the illustration" lock) after
Codex finished all three cards' front art in a parallel session. Verified each count by inspection
rather than trusting the art brief alone, since a puzzle's actual code has to match what's really
drawn.

**Verified by looking at the actual images:**
- **Roumare = 3 boars** — confirmed earlier this session, unchanged.
- **Châlus = 2 crossbow bolts** — Codex's v2 art (replacing the original bolt-free landscape) has
  one small bolt in the left tower's masonry and one on the foreground wall, both subtle but
  countable. The user had said 3 in chat; the art landed on 2, and the user's follow-up confirmed 2
  is correct — recorded as decided, not flagged as a discrepancy.
- **Walcheren = 5 Viking boats** — five individually findable longships spread across the water above
  the dune foreground. Good thematic swap from the earlier windmills/ships brainstorm — longships
  fit the Rollo-raiding legend better than a modern harbor scene, and Codex's choice of 5 (not 3)
  avoided the repeated-triple-digit problem flagged last session.

**Real bug caught and fixed:** Codex's own update to `PZ-19` stated the resulting code as `523`, but
the decided read order is Walcheren(5) → Roumare(3) → Châlus(2), which concatenates to **532**, not
523 — a transcription/arithmetic slip, not a new design call. Fixed in both places it appeared
(the summary line and the closing note). Checked `532` against every other code in the page
(`0734`, `1021`, `1576`, `1972`, `231`, `2468`, `253`, `427`, `582`) — no collision.

### Files changed

- `NorseBackpack/Norse_Brainstorm.html` — `PZ-19`'s pill status and both `523`→`532` fixes.

### Checks run

- Visually inspected `Postcard_05_Chalus_Front.png` (v2) and `Postcard_D_Walcheren_Front.png` to
  count bolts and boats directly rather than trusting the prose description.
- Grepped every `<code>NNNN</code>` in the page to check `532` for collisions — none found.
- Full-file tag-balance check — stayed paired (968 div, 13 section, 26 article, 28 details, 15 ul,
  116 li, 99 a, 11 table, 77 tr, 259 td, 41 th, 238 p, 257 span). `git diff --check` clean.
- Confirmed live over local HTTP: both `532` mentions render, no console errors.

### Next action

Draft the three messages (Walcheren → Roumare → Châlus order, "story goes" framing for the first
two, already drafted once in chat and awaiting final counts — now unblocked). Then decide what
physical lock `PZ-19`'s code feeds (`ST-01`), and whether/when Walcheren gets a real card number
(it's still file-named `Postcard_D_Walcheren_*`, a placeholder, since giving it a real number means
another renumbering pass — cheaper this time since no back/PDF exists yet for it, but Harald's
already-built Oslo card (14) would still need to shift if Walcheren slots in ahead of Aud/Harald).

### Blockers / open items

- The three messages are drafted in chat but not yet written into `build_postcard_0X_pdf.py` scripts
  or the page — final counts were the blocker, now resolved.
- Walcheren has no real card number, back, or print PDF yet.
- Card 04's release point in Leif's lock sequence (from four sessions ago) is still open.
- Bjarnarhöfn and Constantinople (Aud's and Harald's decoys) still have no lock job assigned.

## Session Close — 2026-09-15 (continued, 5) — "Every card gates a lock" rule, and a new combined lock for Châlus/Roumare/Walcheren

**Task:** the user set a stronger standing rule — every postcard, including decoys, must feed an
actual physical lock, not just flavour, a calendar statement, or an element mark. That immediately
flagged five cards with no lock job: Rollo's Châlus and Roumare (blank slates, no mechanism at all
yet), and three of the four decoys (Walcheren, Bjarnarhöfn, Constantinople — Brattahlíð already
qualified via the beasts-chain imprint). Brainstormed options for the first three with the user, who
picked combining all three into one new lock: **"counting in the illustration."**

**Decided in chat:**
- **Mechanism:** each of the three front illustrations hides a count of one small object; the three
  digits, read in the right order, are the lock code. The order comes from natural in-voice
  sequencing phrases in each handwritten message ("before that," "between the two"), not explicit
  numbering — which also doubles as the relative-order calendar statements the Final riddle still
  needs for Rollo's trail.
- **Order: Walcheren → Roumare → Châlus**, mirroring the existing Rollo → William → Richard
  family-line thread. Checked the history first rather than picking arbitrarily: Walcheren ties to
  Rollo's disputed pre-Normandy raiding (evidence category `uncertain` in `stops.js`), Roumare to a
  ducal-forest naming legend near his capital (category `context`, the weakest tier), Châlus to
  Richard the Lionheart's well-documented 1199 death (category `supported`). Flagged in the page
  that the first two need "the story goes" framing in their messages, not stated-as-fact — the
  underlying evidence really is that uneven, and the page already tracks it that way.
- **What each illustration counts:** Châlus = two small crossbow bolts (now built in v2; echoes the
  existing rebus that already points here from Bayeux); Roumare = three wild boars (now built,
  echoing the boar vignette on Rollo's map); Walcheren = five Viking boats (now built). The decided
  order produces code 523.

**Written into `Norse_Brainstorm.html`:** new `PZ-19` with the full mechanism, order, and evidence
reasoning; the Postcard system tab's new rule cross-updated to show Châlus/Roumare/Walcheren as now
assigned (only Bjarnarhöfn/Constantinople still open); same update in the Final riddle tab's decoy
section; Rollo's constraint-worksheet row updated to point at `PZ-19` for its remaining postcard
statements.

**Noted, not reverted:** Codex added Roumare's front art and gallery wiring in a parallel session
(`build_postcard_front_images.py` now has a `Postcard_10_Roumare_Forest` entry) — consistent with
the renumbering from two sessions ago (Roumare is Rollo's 6th real stop, slot 10).

### Files changed

- `NorseBackpack/Norse_Brainstorm.html` — sections listed above; Roumare gallery entry now records
  the v2 three-boar edit and exact prompt.
- `NorseBackpack/Postcards/Postcard_10_Roumare_Forest_Illustration_v2.png` — new source artwork
  with three countable boars; v1 retained.
- `NorseBackpack/Postcards/build_postcard_front_images.py` — Roumare front now builds from v2.
- `NorseBackpack/Postcards/Postcard_D_Walcheren_Illustration_v1.png` and
  `Postcard_D_Walcheren_Front.png` — new CC BY-SA 4.0-derived Walcheren decoy front with five boats.
- `NorseBackpack/Postcards/References/README.md` — Walcheren source attribution and adaptation note.
- `NorseBackpack/Postcards/Postcard_05_Chalus_Illustration_v2.png` and
  `Postcard_05_Chalus_Front.png` — Châlus v2 with two smaller countable crossbow bolts; v1 retained.
- `NorseBackpack/Postcards/Postcard_11_Dogurdarnes_*`, `Postcard_12_Hvammur_*`,
  `Postcard_13_Esjuberg_*`, and `Postcard_D_Bjarnarhofn_*` — Aud's three real postcard fronts and
  Bjarnarhöfn decoy front, all built from newly recorded Commons sources.

### Checks run

- Full-file tag-balance check — stayed paired (965 div, 13 section, 25 article, 27 details, 14 ul,
  113 li, 97 a, 11 table, 77 tr, 259 td, 41 th, 235 p, 257 span; the article/details/li counts moved
  from more than just this session's edits, consistent with Codex's parallel front-art work also
  landing in the same file). `git diff --check` clean.
- Confirmed over local HTTP (a server another session already had running on port 8734, joined
  directly rather than starting a duplicate) that `PZ-19` and its three cross-references render with
  no console errors.

### Next action

Decide the lock jobs and draft the messages for Aud's now-art-complete trail; all four backs and
print PDFs remain to build.

### Blockers / open items

- The illustration count code is fixed at 523. All three messages remain open.
- Which physical lock this feeds is undecided (`ST-01`, same as most other locks).
- Bjarnarhöfn and Constantinople still have no lock job assigned.
- Card 04's release point in Leif's lock sequence (from three sessions ago) is still open and
  unaffected by this session.

## Session Close — 2026-09-15 — Roumare Forest postcard front art

**Task:** create the front art for postcard 10, Roumare Forest, from the user-selected Commons reference.

**Created:** a 1500 × 1050 px, 300 dpi vintage travel-poster front. A young roe deer stands on a fern-lined Normandy woodland track under dappled early-evening light. The front has the series' titled navy band: `ROUMARE FOREST · NORMANDY`. The chosen source is retained as `References/Roumare_Forest_Daguet_Nadine_Toudic_CC-BY-SA-4.0.jpg`, from Nadine Toudic's *Daguet (2)* photo, CC BY-SA 4.0. The original illustrated composition, attribution, licence and exact generation prompt are recorded in the Postcards tab.

**Files changed:** `NorseBackpack/Postcards/Postcard_10_Roumare_Forest_Illustration_v1.png`, `Postcard_10_Roumare_Forest_Front.png`, `References/Roumare_Forest_Daguet_Nadine_Toudic_CC-BY-SA-4.0.jpg`, `build_postcard_front_images.py`, `Norse_Brainstorm.html`.

**Checks:** visually inspected source, illustration and titled front; confirmed final artwork is 1500 × 1050 px at 300 dpi; `git diff --check` passed; `Norse_Brainstorm.html` has 960 matching `<div>` pairs. Live HTTP page check was not completed: the in-app browser's first localhost request was refused while the preview server restarted, then the browser session held its generated error page and rejected a fresh navigation. The direct artifact inspection and source checks passed.

**Next action:** write Roumare's message/Fun Fact, decide its required lock job, then build its back and print PDF. It remains held for the final bundle under the candidate final-riddle direction.

## Session Close — 2026-09-15 (continued, 4) — Card 04's message, Fun Fact, imprint and back built

**Task:** write and build the actual content for decoy card 04 (Brattahlíð), picking up where the
prior session left off. Codex had already generated the front art in a parallel session (found via
the disk-change notice, not reverted — see the session below). Drafted message/Fun Fact in chat,
the user gave exact final wording for the message, and confirmed the drafted Fun Fact as-is.

**Built `build_postcard_04_pdf.py`** (new, modelled on card 02's script, same Leif trail stamp):
- Message and Fun Fact per the user's exact text.
- **Real bug caught and fixed:** the handwriting font (`NothingYouCouldDo`) renders `ð` as a broken
  glyph — confirmed by rendering the card and comparing against the typed Fun Fact box (Helvetica),
  which renders `Brattahlíð` and `Þjóðhildar's` correctly. Fixed by spelling it "Brattahlid" in the
  handwritten message only — Liv's casual handwriting dropping the diacritic while the typed Fun
  Fact keeps it accurate is a deliberate, plausible difference, not a workaround dressed up as one.
- Carries the real `Vinland Editions · Series F, No. 1` imprint (moved here from card 02 last
  session, `PZ-10`/`PZ-18`) and, for the first time on any built card, the "You know me — every
  little detail counts" rule line (`PZ-10`, decided in an earlier session but never actually
  written onto a card) — worked into the message itself ("I really enjoy those small details!")
  rather than printed as a separate line.
- Postmark reads "BRATTAHLÍÐ" (Helvetica renders it fine; only the handwriting font has the bug).
- Rendered `Postcard_04_Brattahlid_Back.png` from the built PDF for the gallery, matching the
  pattern used for other cards' back images.

**Written into `Norse_Brainstorm.html`:** `PZ-05` gained card 04's full message/Fun Fact writeup and
the imprint/rule-line notes; the Postcards toolbar intro, Leif's trail-group count and pc-box, and
a full gallery entry (front + back + View PDF) all updated from "unbuilt" to built. Also fixed two
stale "in their own dedicated scripts" / `build_postcard_collection.py` claims that predated this
card's script.

**Also fixed, found while working:** `References/README.md` had five stale "for Postcard 0X" prose
mentions left over from last session's renumbering (my sweep then only caught literal filenames, not
this prose) — Bayeux/Winchester/Battle/Rouen/Châlus each still claimed their pre-renumbering card
number. Fixed, and added a new README section for the Brattahlíð source photo (Claire Rowland, CC
BY 2.0), which had art but no credit entry yet.

### Files changed

- `NorseBackpack/Postcards/build_postcard_04_pdf.py` — new.
- `NorseBackpack/Postcards/Postcard_04_Brattahlid_Back.png` — new, rendered from the built PDF.
- `output/pdf/Postcard_04_Brattahlid_{Print,Letter_Print}.pdf` — new.
- `NorseBackpack/Postcards/References/README.md` — new Brattahlíð section; five stale card-number
  mentions fixed.
- `NorseBackpack/Norse_Brainstorm.html` — sections listed above.

### Checks run

- Rebuilt the PDF twice (once before, once after the eth-glyph fix) and rendered both at 3× to
  inspect visually — caught the bug on the first pass, confirmed clean on the second.
- Full-file tag-balance check — stayed paired (956 div, 13 section, 24 article, 26 details, 13 ul,
  110 li, 95 a, 11 table, 77 tr, 259 td, 41 th, 233 p, 257 span). `git diff --check` clean.
- Served over local HTTP and checked the Postcards tab: card 04's gallery entry (front + back +
  View PDF) renders, no console errors.
- Deleted temporary preview PNGs from the scratchpad after inspection.

### Next action

Decide where/how card 04 gets released relative to Leif's existing three-lock sequence (`PZ-13`) —
the beasts chain now needs this card in hand, and that's still unplaced. Then start on the other
three decoys (Rollo/Walcheren, Aud/Bjarnarhöfn, Harald/Constantinople), each of which will trigger
its own renumbering cascade like this one did.

### Blockers / open items

- Card 04's release point in the lock sequence is undecided.
- The other three decoy cards have no numbers, art, or text yet.
- Per-stop element-mark assignment and decoy-city shape-checks (from two sessions ago) are still
  open and unaffected by this session.

## Session Close — 2026-09-15 — Brattahlíð decoy postcard front art

**Task:** create the new art for decoy postcard 04, Brattahlíð/Qassiarsuk, from the supplied Wikimedia church reference.

**Created:** a 1500 × 1050 px, 300 dpi vintage travel-poster front: turf-roofed timber church, separate bell frame, Greenland fjord and hills, with the series' blank navy title band. `build_postcard_front_images.py` now generates the titled `Postcard_04_Brattahlid_Front.png`. The source reference is retained locally as `References/Brattahlid_Church_Wikimedia_CC-BY-2.0.jpg` (Claire Rowland, CC BY 2.0). The design page records the source, attribution and exact generation prompt; card 04's trail thumbnail now shows the real front.

**Files changed:** `NorseBackpack/Postcards/Postcard_04_Brattahlid_Illustration_v1.png`, `Postcard_04_Brattahlid_Front.png`, `References/Brattahlid_Church_Wikimedia_CC-BY-2.0.jpg`, `build_postcard_front_images.py`, `Norse_Brainstorm.html`.

**Checks:** inspected the illustration and titled front visually; confirmed 1500 × 1050 px and 300 dpi; rebuilt postcard fronts; `git diff --check` passed; `Norse_Brainstorm.html` has 953 matching `<div>` pairs; served the Postcards tab over local HTTP, confirmed card 04's image loads and page has no console errors.

**Next action:** write card 04's message/Fun Fact, add its real `Vinland Editions · Series F, No. 1` imprint, then build its back and print PDF. Its release position in Leif's lock sequence remains open under `PZ-13`.

## Session Close — 2026-09-15 (continued, 3) — Leif's decoy postcard inserted as card 04; beasts-chain pointer moved off card 02

**Task:** the user's design fix for the beasts-chain lock: postcard 02 was doing two jobs (the
`Series F, No. 1` grid-reference imprint, and half of the hold-to-light 1576 pair with card 03).
Move the imprint job onto the new Leif decoy card, insert it as card 04 (right after Leif's three
real cards), and remove the "every card carries a flavour imprint" camouflage (`PZ-10`) — only card
04 keeps an imprint now. Confirmed with the user this meant renumbering every built card from 04
onward, and to do that renumbering now rather than defer it.

**Renumbered (highest-first via `git mv` to avoid collisions), rebuilt, and verified:**
- Châlus 04→05, Rouen 05→06, Bayeux 06→07, Winchester 07→08, Battle 08→09, Oslo 13→14 — front/back/
  illustration PNGs, `References/*_ImageGen_Source.png`, `build_postcard_0X_pdf.py` scripts (OUT
  paths, FRONT paths, `setTitle` strings), `output/pdf/*.pdf`, `build_postcard_front_images.py`'s
  `CARDS` list, and `References/README.md`'s file-name mentions.
- Rebuilt the four PDFs that have build scripts (Rouen, Bayeux, Winchester, Battle) plus Leif's
  01–03 (imprint removal); Châlus and Oslo are front-art-only, no PDF to rebuild.
- Removed the `Vinland Editions · Series [x], No. [n]` imprint line from all seven existing build
  scripts (01, 02, 03, 06 Rouen, 07 Bayeux, 08 Winchester, 09 Battle) — visually confirmed on a
  re-rendered Rouen card back that the line is gone and nothing else shifted.

**Written into `Norse_Brainstorm.html`:**
- Lock table's beasts-chain row now points to "decoy postcard 04" instead of card 02, marked
  candidate rather than decided.
- `PZ-10` (the imprint mechanism) and `PZ-13` (Leif's opening lock sequence) both marked superseded/
  candidate with a note explaining what changed and what's now unresolved: **card 04 must be in the
  player's hands by the time the beasts chain runs, and where/how it gets released relative to the
  existing three-lock opening is not decided.** The old reasoning is kept below each note, per
  `AGENTS.md`'s "say so where the old text was" rule, not deleted.
- `PZ-05`'s card-02/card-03/Rouen paragraphs updated to say their imprints were removed rather than
  silently dropping the old claims; the historical card-01/card-03 imprint bug note is kept but
  marked no-longer-applicable.
- All stale card-number mentions swept and fixed: gallery headings, `View PDF` links, image `src`
  paths, the Postcard-system lockflow diagram (both Leif's and Rollo's), the Puzzle Details lock
  table's Rollo rows (`05`→`06`, `06,07,08`→`07,08,09`), and three "card 06" mentions that meant
  Bayeux (now card 07).
- Postcards tab: Leif's decoy box now shows the real number `04` instead of a generic placeholder,
  since that number is now decided (the other three trails' decoy boxes stay generic — their
  numbers aren't chosen yet and will shift again when inserted).

**Deliberately not done:** the new card 04's actual message, Fun Fact, and front art (still no
Brattahlíð artwork or written text — this session only secured its number and mechanism role); and
where/how card 04 gets released into play relative to Leif's existing three-lock sequence, flagged
as newly open in `PZ-13`.

### Files changed

- `NorseBackpack/Postcards/*` — renamed image/reference files (see above), edited build scripts
  (`build_postcard_0{1,2,3,6,7,8,9}_pdf.py`, `build_postcard_front_images.py`).
- `NorseBackpack/Postcards/References/README.md` — renumbered filename mentions.
- `output/pdf/Postcard_{01,02,03,06,07,08,09}_*.pdf` — rebuilt.
- `NorseBackpack/Norse_Brainstorm.html` — sections listed above.

### Checks run

- Full-file tag-balance check after every batch of edits — stayed paired throughout (953 div, 13
  section, 23 article, 26 details, 13 ul, 110 li, 93 a, 11 table, 77 tr, 259 td, 41 th, 231 p, 257
  span at the end).
- `git diff --check` on the HTML — no whitespace errors.
- Re-ran all seven affected `build_postcard_0X_pdf.py` scripts — all built cleanly, no exceptions.
- Rendered the rebuilt Rouen card back at 3× and inspected it: message, Fun Fact, postmark, stamp
  and address all intact, no imprint line, nothing else shifted out of place.
- Served over local HTTP (`static-preview`, port 8734) and checked the Postcards and Open Questions
  tabs live: no console errors, decoy boxes and PZ-10/PZ-13's new candidate notes render correctly.
- Grepped the whole page repeatedly for stale `Postcard_0X_Name`/`build_postcard_0X_pdf.py`
  filenames and bare card-number mentions until none remained.

### Next action

Draft the actual Leif decoy card (04, Brattahlíð): message and Fun Fact in Liv's voice, matching the
built-card pattern, carrying the real `Vinland Editions · Series F, No. 1` imprint. Then decide
where/how it's released relative to Leif's existing three-lock sequence, since the beasts chain now
needs it in hand — that's the open item this session added to `PZ-13`.

### Blockers / open items

- Card 04 has no text, front art, or release point in the lock sequence yet.
- The other three decoy cards (Rollo/Walcheren, Aud/Bjarnarhöfn, Harald/Constantinople) are still
  unnumbered and unbuilt — each insertion will trigger another renumbering cascade of everything
  after it, same as this session's.
- Per-stop element-mark assignment and decoy-city shape-checks (from the session below) are still
  open and unaffected by this session's work.

## Session Close — 2026-09-15 (continued, 2) — Crest/symbol elements and four decoy stops decided

**Task:** the user asked to fill in the `PZ-18` open items from the Final riddle v2 session below:
the symbol/crest element designs and the four decoy cities. Proposed a draft in chat first (crest,
symbol, fake elements, decoy cities), the user changed two of the four decoy cities from the draft,
then approved the rest as drafted.

**Decided and written into `Norse_Brainstorm.html`:**
- **Symbol (3 elements, covers Leif + Aud):** raven, longship, compass rose/sun-wheel.
- **Crest (6 elements, covers Rollo + Harald):** battle-axe, shield, wolf, anchor, drinking horn,
  valknut.
- **Fake elements:** Leif/Aud decoys share Mjölnir (Thor's hammer); Rollo/Harald decoys share a
  crown (both trails are about rulers, which is what makes it convincing).
- **Four decoy stops**, all real Liv-visited places already in `stops.js`'s research corpus, just
  not on that trail's six postcard stops: Leif = Brattahlíð/Qassiarsuk (Greenland), Rollo =
  Walcheren (Netherlands, user's choice — not the earlier Caen/Falaise candidates), Aud =
  Bjarnarhöfn (Iceland, user's choice — not the earlier Krosshólaborg candidate), Harald =
  Constantinople/Istanbul.

**Updated:** the Final riddle tab's four panels (element/fake/decoy-city designs stated, no longer
just candidates), the constraint worksheet's decoy-city column, `PZ-18`'s open-items list (elements
and cities struck through as decided), the Postcards tab's "All 18, by trail" boxes (one new decoy
box per trail group, counts relabelled "real built" vs. decoy), and the Travel routes tab's pending
note.

**Deliberately not done:** which specific element sits on which real stop's card (per-stop
assignment), the shape-check of each decoy city against its trail's map projection, and the four
decoy postcards' actual message/Fun Fact text — all still open, the last being the literal "4 new
cards" the user asked for that this session didn't reach.

### Files changed

- `NorseBackpack/Norse_Brainstorm.html` — sections listed above.

### Checks run

- Full-file tag-balance check (div/section/article/details/ul/li/a/table/tr/td/th/p/span) — all
  paired (951 div, 13 section, 23 article, 26 details, 13 ul, 110 li, 93 a, 11 table, 77 tr, 259 td,
  41 th, 231 p, 256 span).
- Served over local HTTP (`static-preview`, port 8734) and checked live: Final riddle tab's four
  updated panels and Postcards tab's four new decoy boxes (Brattahlíð, Walcheren, Bjarnarhöfn,
  Constantinople) render correctly under their trail colours. No console errors.

### Next action

Draft the four decoy postcards' message/Fun Fact text (in Liv's voice, matching the built-card
pattern), then shape-check each decoy city against its trail's real map projection before touching
`stops.js`/`Norse_Aunt_Route_Plan.json` or the trail-map PDFs.

### Blockers / open items

- Per-stop element-mark assignment (which of the 3 symbol / 6 crest elements goes on which real
  card) is unassigned.
- No decoy city is shape-checked yet — a city that doesn't draw a plausible wrong digit would need
  replacing before any art or map work starts.
- The four decoy postcards have no text, front art, or back/print PDF.
- Rest of `PZ-18` (dated-vs-undated decoys, final-bundle contents, the constraint-solver build) is
  unchanged from the session below.

## Session Close — 2026-09-15 (continued) — Final riddle v2 recorded: decoy postcards + crest/logo filter

**Task:** the user supplied a written design update (`Final_Riddle_Update.md`, dated 15 Sept 2026,
their own attached doc, not authored this session) replacing the evidence-led-calendar Final riddle
direction with a richer version: 22 postcards (18 real stops + 4 decoys, one per trail), a family
logo/crest note in the final bundle that filters decoys by element, and the same calendar-
reconstruction mechanism underneath. The doc's own status line says it's a candidate, not proofed,
and gates postcard-text changes behind a solver check that doesn't exist yet — so this session
recorded it as the new candidate direction rather than treating it as decided.

**Written into `Norse_Brainstorm.html`, following the doc's own change table:**
- Full rewrite of the **Final riddle tab**: the deck/filter mechanism (decoys, logo/crest elements,
  paired fake elements, the element-mark design constraint, decoy cities still needing a shape-check),
  the working calendar (22 slots candidate, dated-vs-undated still open), clue types and jobs
  (tickets/postcards/final bundle), the guessing-risk box, and a four-point validation section
  matching the doc's solver checks verbatim (unique answer, bundle gates, no decoy reads as a shape,
  gap/order rules hold).
- **Story & sequence**: "Last puzzle" panel and "Keep the original ending" callout both updated to
  22 cards + the crest/logo filter, both linking to the Final riddle tab as the candidate source.
- **Postcard system tab**: job 1's description, the "every card is active" line, and the "Ordering
  key"/"Count" rows in the carried-over-decisions table updated (postmark now place-only; order
  comes from reconstructed evidence, not a raw sort).
- **Postcards tab**: intro line and the "All 18, by trail" legend both flag the candidate 22-card /
  decoy-filter change without altering the actual card boxes (no decoy city is decided yet, so
  nothing was added to the grid).
- **Design spec tab**: card-layout table's count/design-elements/ordering-key/active-cards rows
  updated to match, including the candidate element-mark field.
- **Open questions**: `PZ-08` reworded (first-appearance rule kept, source changed to the
  reconstructed calendar); `PZ-11` marked superseded in place (old reasoning kept, not deleted, per
  `AGENTS.md`'s "say so where the old text was" rule); `PC-10` reasoning corrected (postmark is no
  longer the ordering key); `PZ-16` got an optional tie-in note (the crest/logo note could be a
  family-tree puzzle's output). **New `PZ-18`** bundles every item the doc's own "Open questions,
  new items" list named: dated-vs-undated decoys, the logo/crest element designs and their two
  fakes, decoy city per trail (shape-check pending), Aud's missing museum ticket, final-bundle
  contents, and the constraint-solver build itself.
- **Travel routes tab**: added a pending note (`PZ-18`) rather than inventing decoy cities or
  coordinates — `stops.js`/`Norse_Aunt_Route_Plan.json` are untouched, since which decoy goes where
  is explicitly still open in the source doc.
- Fixed the codes-reference table's "Final route lock" row, which still said "postmark-date order"
  and "All 18" — a direct, factual consequence of the above, not a new call.

**Deliberately not done:** no postcard text was rewritten (the doc's own gate: the solver check
must pass first), no decoy cities/coordinates were chosen, no crest/logo artwork was designed, no
constraint-solver script was built. All of that stays open under `PZ-18`.

### Files changed

- `NorseBackpack/Norse_Brainstorm.html` — sections listed above.

### Checks run

- Caught and fixed one self-introduced bug: a stray `</p>` instead of `</div>` in the new "Open
  decision: do decoys take slots?" note broke div/p balance (947/946 and 228/229). Full-file
  div/section/article/details/ul/li/a/table/tr/td/th/p/span tag-count check passed after the fix.
- Served over local HTTP (`static-preview`, port 8734) and checked live: Story & sequence's two new
  links land correctly; the rewritten Final riddle tab renders top to bottom including the
  Validation section; the Open questions tab shows the new `PZ-18` row and the superseded `PZ-11`
  pill. No console errors anywhere checked.

### Next action

Per the doc: design and shape-check one trail's decoy city first (probably Rollo, since it's the
6-stop trail with the most map detail already built), then build the constraint-grid solver before
writing any of the 4 decoy postcards or touching existing postcard text.

### Blockers / open items

- Everything under new `PZ-18` (see above) — this session recorded the direction, it didn't resolve
  any of it.
- Pre-existing backlog (postmark dates generally, `PR-05` print-size check, Aud's coin-hoard specifics,
  Oslo hnefatafl weight puzzle, unbuilt cards) is unchanged.

## Session — 2026-09-15 — Aud treasure-map and coin-hoard chain recorded

**Task:** record the approved Aud journey direction and move the comb to Harald.

**Decision:** Aud&rsquo;s existing laminated journey map is also the treasure map. Dögurðarnes gives four feature-route clues; the four destination squares hide a four-digit code that opens the coin cache. All coins release at once, mixed: several coins of each of three visually distinct types. The final treasure square&rsquo;s cache mark selects one sorted pile. Hvammur tells players to weigh it; Esjuberg&rsquo;s upside-down art and a drawn scale display with the final digit crossed out produce `370.56` → `370.5` → `SOLE` upside down. `SOLE` is now the decided answer for the owned four-letter lock. The comb moves to Harald&rsquo;s journey; its exact card set and output remain open.

**Changed:** `NorseBackpack/Norse_Brainstorm.html` — updated the card-family matrix, lock table, PZ-03, new open build item `PZ-17`, `PR-02`, the coin-hoard prop flow, and the comb description.

**Checks:** `git diff --check` passed; paired HTML-tag check passed; served over local HTTP and opened the Design spec tab in the in-app browser. Layout rendered normally and the browser reported no console errors.

**Next action:** design and play-test Aud&rsquo;s four exact map routes, then choose the three coin types/counts and calibrate the selected pile on a replacement scale (>370.56 g capacity, 0.01 g resolution).

## Session — 2026-09-15 — Final riddle direction recorded

**Task:** record the user's replacement direction for the Norse endgame.

**Decision in principle:** all 18 postcards are released before the final clue bundle. Rather than reading a date from every postmark or receiving three held-back cards at the end, players solve an evidence-led travel timeline: recurring dated museum tickets provide anchors; natural postcard statements provide relative-order constraints; a few final travel documents resolve remaining ambiguity. The solved four route orders are then traced on the maps as before, producing the candidate `1972` code.

**Changed:** `NorseBackpack/Norse_Brainstorm.html` — added the **Final riddle** tab with the player flow, an intentionally blank per-trail evidence worksheet, evidence rules, and the uniqueness/play-test risk. It explicitly records that this direction supersedes postmark dates as the endgame ordering key and the held-back-postcard plan. Exact tickets, dates, phrases, and final documents remain open as `PZ-16` work; no content has been invented.

**Checks:** served over local HTTP and opened `Norse_Brainstorm.html#view-final-riddle`; tab selection, final-riddle content and responsive top layout rendered correctly, with no console errors. Ran `git diff --check` successfully.

**Next action:** assign a minimal, unique constraint set for one trail (probably Rollo, using the existing Bayeux → Battle relationship), then test it as a logic grid before writing any player-facing postcard text.

**Revision:** replaced the abstract per-trail timeline emphasis with one shared, simple calendar: 18 slots from 01 March to 21 April at three-day intervals. L'Anse aux Meadows is slot 1; the remaining slots are intentionally unassigned. Museum tickets now anchor exact slots on this calendar, while postcard and final-document clues constrain the rest.

## Session Close — 2026-09-15 — Candidate weight-puzzle branches recorded

**Task:** record the user's two new, separate weight-puzzle directions in the Norse design source.

**Recorded as candidates, not decisions:**
- **Aud treasure cache:** coins arrive during Aud's travel; her smaller map identifies the cache.
  A target reading of `370.56 g` has its final digit crossed out in a supplied drawing, leaving
  `370.5`, which reads `SOLE` upside down for the owned four-letter lock. This explicitly
  supersedes the previous three-mints/weight-order concept.
- **Oslo hnefatafl pieces:** 3D-printed attackers and defenders have concealed controlled weights
  and letters/runes on their bases. Each side is weighed and ordered separately; matching weights
  across colours require correct grouping first. It remains separate from the board-reconstruction
  and king-escape puzzle.

**Files changed:** `NorseBackpack/Norse_Brainstorm.html`.

**Checks:** reviewed the updated source and ran `git diff --check` (no whitespace errors).

**Next action:** choose the exact attacker/defender outputs and prototype the required scale,
ballast and repeatable 3D-print weights. The existing 200 g / 0.01 g scale cannot measure 370.56 g.

## Session Close — 2026-09-15 (continued) — Two postcard builders missed the v2 flat stamp swap

**Task:** following up on the stamp session below (Codex's v2 flat-overlay stamps), checked for
consistency across all builders rather than assuming the swap was complete everywhere.

**Found:** `build_postcard_01_pdf.py`, `05`, `06`, `07`, `08` already pointed at the `_v2_flat`
stamps and had been rebuilt. `build_postcard_02_pdf.py` and `build_postcard_03_pdf.py` — both
Leif's trail, same `Stamp_Leif_Longship` art as card 01 — still pointed at the old `_v1`
photographic stamp (card 01 was updated, 02/03 were missed). A repo-wide `grep` confirmed no other
`_v1` stamp references remained once these two were fixed.

**Fixed:** updated both scripts' `STAMP` path to `Stamp_Leif_Longship_v2_flat.png`, rebuilt
`Postcard_02_Battle_Harbour_{Print,Letter_Print}.pdf` and
`Postcard_03_Baffin_Island_{Print,Letter_Print}.pdf`, then rebuilt `Norse_Postcards_Full_Print.pdf`
via `build_postcard_collection.py` so the combined file picks up cards 02/03's new stamp too (that
combined file currently only bundles cards 01–03 — `CARDS` in the collection script is deliberately
left empty per its own comment, cards 05+ aren't wired into it; pre-existing, not changed here).

### Files changed

- `NorseBackpack/Postcards/build_postcard_02_pdf.py`, `build_postcard_03_pdf.py` — stamp path
  updated to `_v2_flat`.
- `output/pdf/Postcard_02_Battle_Harbour_{Print,Letter_Print}.pdf`,
  `Postcard_03_Baffin_Island_{Print,Letter_Print}.pdf`, `Norse_Postcards_Full_Print.pdf` — rebuilt.

### Checks run

- Rasterized card 02's back page (PyMuPDF) and inspected at full size: the stamp sits flat on the
  cream card stock with no grey photographic background/shadow box, matching cards 01/05/06/07/08.
- `grep -rn "Stamp_.*_v1\.png"` across `.py`/`.html` returned nothing after the fix.

### Next action

Run the planned physical print-size check (`PR-05`), per Codex's session below — unaffected by this
fix, still outstanding.

### Blockers / open items

- None new. `Stamp_Aud_Pillars_v2_flat.png` and `Stamp_Harald_Labrys_v2_flat.png` exist but are
  unused by any build script yet (Aud/Harald postcard builders don't exist), and both motifs are
  already flagged "Superseded — redraw" in the Design guide, unrelated to this fix.

## Session Close — 2026-09-15 — All four stamps converted from photographed objects to postcard overlays

**Task:** review the stamp series and improve the stamp background without changing the icons.

**Built and approved across the four existing motifs:**
- New v2 assets preserve each engraved illustration and trail colour, but remove the photographic
  table/surround and cast shadow. The area outside each perforated edge is transparent (32-bit
  alpha), with a quiet pale-cream internal ground.
- The Design spec gallery points to all four v2 overlays. Exact prompts are recorded there.
- Card 01 and all four built Rollo cards (05–08) now use their matching v2 asset; their PDFs were
  rebuilt. Aud and Harald have no built postcard PDF yet, so their v2 assets are ready for use.

### Files changed

- `NorseBackpack/Postcards/Stamps/Stamp_{Leif_Longship,Rollo_Comet,Aud_Pillars,Harald_Labrys}_v2_flat.png` — new transparent-background overlays.
- `NorseBackpack/Postcards/build_postcard_{01,05,06,07,08}_pdf.py` — built cards now consume v2 assets.
- `NorseBackpack/Norse_Brainstorm.html` — gallery points to v2; treatment and exact prompts added.
- `output/pdf/Postcard_01_LAnse_{Print,Letter_Print}.pdf`, `Norse_Postcards_Full_Print.pdf`, and
  `Postcard_{05_Rouen,06_Bayeux,07_Winchester,08_Battle}_{Print,Letter_Print}.pdf` — rebuilt.

### Checks run

- Inspected all four transparent PNGs at full resolution: 1145×1374, 32-bit ARGB.
- Rendered Card 01 and Bayeux/Card 06 backs from rebuilt PDFs at 3× and inspected them: no
  photographic shadow or dark rectangle remains; postmarks still overlay their stamps correctly.
- HTML paired-tag check passed.
- Local in-app-browser preview failed to attach, so the Design tab itself was not visually checked
  in-browser this session. The image/PDF visual proof was checked directly.

### Next action

Run the planned physical print-size check (`PR-05`) before producing the remaining postcard backs.

## Session Close — 2026-09-15 — Rouen postcard's gallery entry was stale, not actually missing

**Task:** the user reported the Rouen postcard "missing." Investigated rather than rebuilding
blind — `Postcard_05_Rouen_Front.png`, `build_postcard_05_pdf.py`, and both
`output/pdf/Postcard_05_Rouen_{Print,Letter_Print}.pdf` already exist and are complete (message,
Fun Fact, address, stamp, postmark placeholder, word-lock order clue), committed in `e96d06d`. The
postcard itself was never missing.

**Real problem:** the Postcards tab's gallery entry for card 05 (`Norse_Brainstorm.html`) was
stale from before the back/PDF got built — it showed only the front image, no "View PDF" link, and
said "back and print PDF remain to build." A nearby `PZ-15` note also still claimed Rouen's front
art didn't exist and the build script was blocked on Codex. Since the design page is the project's
single source of truth (`AGENTS.md`), a stale entry there reads as the postcard not existing, which
is exactly what was reported. This was mechanical sync to match already-built, already-decided
content — not a new design call — so it didn't need re-proposing first.

**Fixed:**
- Rendered `Postcard_05_Rouen_Back.png` (1500×1050, matches the front) by rasterizing page 2 of the
  already-built `Postcard_05_Rouen_Print.pdf` with PyMuPDF — a direct capture of existing content,
  nothing invented.
- Updated the card 05 gallery entry: added the back figure and a "View PDF" link, corrected the
  status line to "message, Fun Fact and word-lock order clue built; postmark date still pending"
  (matching the pattern used for cards 02/03/06/07/08).
- Corrected `PZ-15`'s stale "Still open" line (dropped the false front-art/Codex-block claim) and
  its status pill (postcard text is no longer open).

### Files changed

- `NorseBackpack/Postcards/Postcard_05_Rouen_Back.png` — new, rasterized from the existing PDF.
- `NorseBackpack/Norse_Brainstorm.html` — card 05 gallery entry (back figure, PDF link, status
  text), `PZ-15` open-items line and status pill.

### Checks run

- Served over local HTTP (`static-preview`, port 8734) and viewed the Postcards tab: front and back
  both render at natural size, "View PDF" opens the correct file, no console errors.

### Next action

None queued from this session. Postmark dates (`PC-03`/`PC-04`) remain open for Rouen along with
every other built card.

### Blockers / open items

- No blocker from this session. Pre-existing backlog (postmark dates, unbuilt cards 04/09–18,
  Hnefatafl placement, etc.) is unchanged.

## Session Close — 2026-09-14 (continued) — Harald's trail map sheet unblocked and built

**Task, same session continued:** start Harald's trail map sheet, which `build_trail_maps_pdf.py`
had listed in `BLOCKED` since stops 5–6 ("Sicily", "Asia Minor") were regions, not named points.

**Researched real, verifiable places for both** (WebSearch, not memory):
- **Sicily → Syracuse.** Confirmed by multiple sources: during the 1038–1040 Byzantine campaign
  under George Maniakes, Harald's forces took part in capturing Messina and Syracuse — a specific,
  well-documented site.
- **Asia Minor → no single city resolves.** Every source describes a broad sweep (~80 strongholds
  captured, advancing to the Euphrates), no named city tied to Harald specifically. Reported this
  honestly to the user rather than inventing one; they chose **"pick a representative city, clearly
  flagged as illustrative."** Chose **Melitene** (modern Malatya) — a real, well-documented
  Byzantine-Arab frontier fortress directly on the Euphrates, explicitly marked as a placement
  choice, not a sourced fact about Harald.

**Updated the sourced data in two places** (both needed — they're separate copies): `stops.js`
(the 72-entry research corpus, plus two new source entries) and `Norse_Aunt_Route_Plan.json`'s
embedded `visits.harald` copies for `h-sicily`/`h-anatolia`. New evidence category `illustrative`
added for the Melitene entry, distinct from `supported`/`saga`/`uncertain`, so it can't be mistaken
for sourced fact later.

**Added `harald` to `TRAILS` and built the sheet** — first attempt succeeded cleanly (no dropped
labels, no collisions): all six stops findable by name. Title `THE VARANGIAN ROAD` is a draft pick,
not yet confirmed with the user. Frame is necessarily much more zoomed out than the other three
sheets (continent-spanning: Norway to Sicily to eastern Anatolia) — a coarser km-per-square is an
accepted consequence, not an oversight.

**Real problem caught: the traced route doesn't read as a digit `2`.** Plotted in visit order, the
path crosses west↔east twice — a zigzag, not a clean 2. Flagged to the user before going further
(this is the core final-puzzle mechanic — traced shapes read as the code). They chose **accept as-is**
over reordering (which would also require re-checking `PZ-08`'s postmark-order constraint and
`PZ-11`'s held-back-card choice).

**Second, independent instance of the same problem found and partially fixed:** the "Travel routes"
tab already had a hardcoded, hand-drawn SVG polyline captioned "Harald route shaped like the digit
2" — an idealized target shape drawn before the real map existed, not derived from any projection,
plus a full duplicate copy of the old Sicily/Anatolia stop text (name, note, source link) that
`stops.js` alone doesn't drive. Updated that duplicate text to Syracuse/Melitene and re-captioned the
SVG as an idealized target that the real map doesn't achieve, rather than leaving the page
contradicting its own answer key.

### Files changed

- `NorseBackpack/TravelMap/stops.js` — `h-sicily`→Syracuse, `h-anatolia`→Melitene (new coordinates,
  evidence/precision/note/source), two new `NORSE_SOURCES` entries.
- `NorseBackpack/TravelMap/Norse_Aunt_Route_Plan.json` — same two stops' embedded copies updated to
  match.
- `NorseBackpack/TravelMap/build_trail_maps_pdf.py` — `BLOCKED` emptied; new `harald` entry in
  `TRAILS` (frame, parallels, title, band colour, minimal/empty regions-areas-waters-extra_towns).
- `output/pdf/Trail_Map_4_Harald_Print.pdf`, `Trail_Map_4_Harald_ANSWER.pdf` — new.
- `NorseBackpack/Norse_Brainstorm.html` — `PZ-09` (Harald's sheet now built, shape risk noted),
  `PZ-11` (Aldeigjuborg hold-back flagged stale, needs re-test against the real projection), `PZ-06`
  (the "loosest of the four" note updated to reflect the real zigzag), the postcard-gallery Harald
  caption, the prop-kit list's "three of four sheets built" line, and the Travel routes tab's
  hardcoded Harald route-card (stale stop text + misleadingly confident SVG shape).

### Checks run

- Ran `build_trail_maps_pdf.py harald`: clean build, no `STOPS NOT LABELLED` line, no label
  collisions reported.
- Rendered both the print and ANSWER PDFs at 200dpi and inspected visually: all six stops labelled
  and findable, coastlines/grid/scale bar/compass all correct, no overlap or dropped content.
- Verified the shape problem by reading the actual projected stop order off the rendered answer
  key, not by assumption.
- Live-checked (served over local HTTP) that both the Travel routes tab's Leaflet mini-map and the
  separate `Travel_Map.html` workshop page pick up the new Syracuse/Melitene data automatically
  (both read `stops.js` at runtime) — no console errors on either page.
- HTML tag balance after all edits: 897 `div`, 12 `section`, 64 `figure`, 23 `details`, 23 `article`,
  13 `ul`, 108 `li`, 80 `a`, 5 `svg`, 7 `ol` — all paired.
- Validated `Norse_Aunt_Route_Plan.json` still parses after editing.
- Deleted temporary preview PNGs after inspection.

### Next action

Re-test `PZ-11`'s Harald hold-back choice (Aldeigjuborg/Staraya Ladoga) against the real built map's
projection — it was chosen on an approximate projection before this sheet existed, and the "one-card-
removed" shape test needs redoing now that six real points exist.

### Blockers / open items

- `PZ-11`'s Harald hold-back card is stale (see Next action).
- Title `THE VARANGIAN ROAD` is an unconfirmed draft pick.
- Harald's sheet has no decorative regions/areas/waters/extra-town labels yet (the other three
  sheets each have 8–25) — currently only the six real stops are labelled.
- The hnefatafl board-setup panel (`Props/Hnefatafl/build_board_setup_pdf.py`) still needs
  compositing onto this sheet's back now that it exists.
- The coin puzzle's three mint-city locations (`PZ-09`) are still unplaced on this sheet.
- `PR-11`-style decorative vignettes (present on Leif's and Rollo's sheets) don't exist for Harald.

## Session Close — 2026-09-14 — Incomplete hand-drawn hnefatafl setup sketch

**Task:** create a square, high-resolution PNG of the final 11×11 board setup as Liv's practical
pen sketch on the blank white back of a document, with columns I–K made unreadable by wet ink
transferred and dragged when another sheet was lifted away.

**Built, then revised:** `Hnefatafl_Incomplete_Board_Sketch_v3.png` is the selected 1254×1254
PNG. It keeps the exact dark-green hand-ruled setup on plain white document paper. Columns I–K
now show restrained lifted ink: mostly white paper with broken grid fragments, offset ghosts and
small dragged marks. The information is missing rather than hidden under a dark mass. The visible
A–H positions were checked cell-by-cell against the user's coordinate list. The heavier v1 and
v2 treatments are retained beside it as superseded directions.

**Companion paper built:** `Hnefatafl_Transferred_Ink_Paper_v1.png` (1254×1254 PNG). It carries
only the transferred 3×11 strip, horizontally mirrored as K–J–I: attackers at K8, K4 and I6,
with rust diamonds at K11 and K1. The grid and marks are readable but retain slight feathering,
missing flecks and offset ghosts so they look transferred rather than freshly redrawn.

**Project-page record:** added both rendered images and their exact built-in ImageGen prompts to
the Hnefatafl setup section in `NorseBackpack/Norse_Brainstorm.html`.

**Checks:** confirmed PNG format and 1254×1254 dimensions for v3; inspected the full render; checked the
11×11 cell count, visible token coordinates, lack of text/labels, and fragmented I–K area. HTML
tag balance and live browser rendering were checked after the edit.

**Next action:** decide whether v3 becomes the actual Harald map-back artwork or remains a
visual direction alongside the existing deterministic PDF panel. No PDF was rebuilt in this
session.

## Session Close — 2026-09-14 (continued) — Board size changed to 11×11; user's final layout solved and all props rebuilt

**Task, same session continued:** the user asked to make the board "more realistic" — first proposed
10×10, then corrected to 11×11 after I flagged that 10×10 has no true centre square (even-sized
board). Built an interactive sandbox so they could design the final layout themselves; they used it
and handed back a finished 22-piece layout (16 attackers, 6 defenders) in the tool's own export
format.

**Built:** `NorseBackpack/Props/Hnefatafl/board_designer.html` — standalone, self-contained 11×11
sandbox with true centre throne (F6), an adapted starting layout (8 defenders in a ring inspired by
Tablut's pattern, 20 attackers in edge rows — not claimed as verified history for this size), slide
movement with custodian captures, a free-form Place/Edit mode, and a live coordinate export.

**Solved the user's final layout by exhaustive search** (not eyeballed): 1 and 2 moves have zero
solutions, **3 moves has exactly one** — `F6 → H6 → H11 → K11`, legs 2/5/3, code `253` — and 4 moves
already has 18. Also verified the hidden-strip property still holds at this size: assuming the three
hidden columns (I–K) are empty finds 31 false candidate routes, so the puzzle still "refuses to
resolve instead of resolving wrongly."

**Rebuilt all three Hnefatafl props at 11×11**, sharing one updated geometry module:
- `board_layout.py` — full rewrite: `ATTACKERS`/`DEFENDERS` tracked as separate sets (not just one
  undifferentiated `BLOCKS`), 11×11 `SIZE`, new throne/corners/solution path, new A–H visible /
  I–K hidden column split (up from A–E/F–G at 7×7).
- `build_board_setup_pdf.py` — map-back panel now draws attackers (dark) and defenders (light,
  outlined) as visually distinct tokens; stain enlarged to 3 columns; caption switched from a full
  coordinate list to counts (19 pieces don't fit legibly on one line the way 10 did).
- `build_ticket_pdf.py` — mirrored offset panel now 3 columns (K, J, I reversed) instead of 2,
  also with distinct attacker/defender tokens; ticket page grew from 2.4×5.6in to 2.6×6.6in to fit.
- The **interactive prototype in the main page itself** (previously left stale at 7×7 in the prior
  entry below) was also updated: 11×11 grid, real attacker/defender sets, corrected corner test,
  reset/hint routes rewritten to the new solution. This was not explicitly requested but leaving the
  page's own demo showing a superseded 7×7 board while every other section described 11×11 would
  have been a real inconsistency.

**`PZ-01` moved from "in progress" back to Decided** (at 11×11) — the 7×7 solution stays visible only
where explicitly marked as a superseded illustration (`PZ-07`'s old SVG diagram caption), not
anywhere it could be mistaken for current.

### Files changed

- `NorseBackpack/Props/Hnefatafl/board_designer.html` — new (from the "in progress" half of this
  session).
- `NorseBackpack/Props/Hnefatafl/board_layout.py` — full rewrite for 11×11.
- `NorseBackpack/Props/Hnefatafl/build_board_setup_pdf.py` — rebuilt for 11×11, attacker/defender
  token distinction.
- `NorseBackpack/Props/Hnefatafl/build_ticket_pdf.py` — rebuilt for 11×11, same token distinction.
- `output/pdf/Hnefatafl_Board_Setup_Insert.pdf`, `Hnefatafl_Ticket_Print.pdf`,
  `Hnefatafl_Ticket_Letter_Print.pdf` — rebuilt in place.
- `NorseBackpack/Norse_Brainstorm.html` — `PZ-01` (finalized 11×11 solution/code, pill back to
  Decided), `PZ-07` (rebuilt-panel details, 3-column split), `PR-08` (11×11 target, piece-count
  note), the codes-reference table row, "What the board feeds" card, the interactive prototype's
  CSS (`.board` grid now 11 columns, new `.cell.defenderblock` style, resized king/token glyphs)
  and JS (`attackers`/`defenders`/`blocks` sets, 121-cell render loop, corrected corner test, new
  reset/hint routes), and its surrounding panel text.

### Checks run

- Ran the uniqueness search in a throwaway script (not committed) over the user's exact layout:
  confirmed 0/0/1/18 solutions at 1/2/3/4 moves, and 31 false candidates assuming I–K empty.
- Rebuilt both PDF props and rendered every page (map insert, ticket front, ticket back) at
  250–300dpi; cross-checked the map panel's visible tokens and the ticket's mirrored panel token-
  by-token against the layout data — all 19 visible + 3 hidden (via the ticket) pieces landed on the
  exact expected squares.
- Loaded the main page's Prototype tab live in the browser, clicked "Show route": rendered
  "Solution: F6 → H6 → H11 → K11. Legs: 2, 5, 3 → code 253." exactly matching the search result, on
  an 11×11 grid with the corners in all four visual corners. No console errors.
- HTML tag balance after all edits: 897 `div`, 12 `section`, 63 `figure`, 22 `details`, 23 `article`,
  13 `ul`, 108 `li`, 80 `a` — all paired.
- Deleted temporary preview PNGs and the scratch solver script after inspection.

### Next action

Decide whether Codex should start Oslo's front artwork now, or wait for Harald's trail map sheet to
exist first — same open call as before, unaffected by the board-size work.

### Blockers / open items

- Harald's trail map sheet still doesn't exist — the real blocker for finishing this puzzle's
  physical props (unchanged from earlier this session).
- `PR-08` (which specific 11×11 board/piece set to buy) is still unchecked against real listings.
- The Oslo postcard's front artwork and print PDF are still unbuilt.
- `PR-09`'s physical print test (does the offset read through the ticket, does the stain hide the
  original) has not been run — the props are sized correctly now but untested on paper.

## Session Close — 2026-09-14 — King's escape (hnefatafl): compartment dropped, moved to Harald, ticket + map-back panel built

**Task:** continue the king's escape puzzle. In chat, the user dropped the throne-compartment
idea entirely (board is now a straightforward bought prop, no cavity), then asked to build the
Oslo museum ticket, the Oslo postcard text, and the map-back setup panel + its mirrored offset —
for **Harald's trail**, not Leif's (reassigning `PZ-07`/`PZ-09`).

**Decided in chat, written into the page:**
- Throne compartment dropped (`PZ-01` candidate summary, `PR-08`, the puzzle-detail card, the
  "Needs work" note, the "build" tab's prop-kit bullet, the 3D-printer inventory line).
- The prop renamed pamphlet → **ticket** throughout (it's flat, not folded — confirmed with the
  user this is the same object, not a second prop).
- Ticket content simplified to the *real* historical rules (light defenders at centre, dark
  attackers, sandwich-capture, king escapes to a corner) — general museum-visitor copy, not this
  puzzle's own house rules (fixed non-moving blockers). Liv's actual task line ("get him to a
  corner in exactly three moves") moved to the **Oslo postcard** instead, in her voice: "We like
  to play our own rules though: can you get the king to escape to a corner in exactly three
  moves?"
- Whole mechanism reassigned from Leif's map to **Harald's Oslo map** (`PZ-07`, `PZ-09`) — Oslo is
  a real, verified stop (`h-oslo`, order 1, Harald's trail opener). Harald's trail map sheet does
  **not exist yet** (`build_trail_maps_pdf.py` has no entry for him, and two of his six stops are
  still regions, not named places) — flagged to the user before drafting, who chose to draft text
  now and let the art wait.
- Oslo postcard message and Fun Fact drafted and written into `PZ-05` (not yet built as a PDF —
  blocked on front art, which is Codex's job, and on Harald's map for context).

**Built — two new Python props, sharing one geometry module so they can't drift apart:**
- `NorseBackpack/Props/Hnefatafl/board_layout.py` — the 14 fixed blocker squares, throne and
  corners, pulled from the exact `blocks` set in this page's own interactive prototype (not
  re-derived by eye). Also the map/ticket split: columns A–E visible, F–G hidden.
- `NorseBackpack/Props/Hnefatafl/build_board_setup_pdf.py` → `output/pdf/Hnefatafl_Board_Setup_Insert.pdf`
  — the map-back panel: grid, throne, corners and the 10 visible blockers, with an irregular stain
  over columns F–G and Liv's margin apology beside it. **Real bug caught and fixed**: the first
  version painted the stain as a translucent overlay, so the hidden blockers showed through as
  darker patches — visually defeating the "hidden" strip entirely. Fixed by never drawing tokens
  in the hidden columns at all, so the stain covers blank paper, not a disguised token.
- `NorseBackpack/Props/Hnefatafl/build_ticket_pdf.py` → `output/pdf/Hnefatafl_Ticket_Print.pdf`
  (+ `_Letter_Print.pdf`) — front: museum branding, a decorative (non-puzzle) mini board icon, and
  the real-rules text. Back: the reconstruction-caveat line plus the mirrored two-column offset
  panel (columns printed G, F — reversed from the map's own F, G order — at the same 0.5in cell
  pitch as the map panel, so the grid lines actually continue when butted together). **Real bug
  caught and fixed**: the first rules draft said "no captures" one line above "the attackers win
  by surrounding him" — a direct self-contradiction, since surrounding *is* a capture in real
  hnefatafl. Rewrote to describe the actual sandwich-capture rule.

### Files changed

- `NorseBackpack/Props/Hnefatafl/board_layout.py` — new.
- `NorseBackpack/Props/Hnefatafl/build_board_setup_pdf.py` — new.
- `NorseBackpack/Props/Hnefatafl/build_ticket_pdf.py` — new.
- `output/pdf/Hnefatafl_Board_Setup_Insert.pdf`, `Hnefatafl_Ticket_Print.pdf`,
  `Hnefatafl_Ticket_Letter_Print.pdf` — new.
- `NorseBackpack/Norse_Brainstorm.html` — `PZ-01`, `PZ-05` (Oslo message + Fun Fact), `PZ-07`
  (reassigned to Harald, both panels marked built), `PZ-09` (hnefatafl job moved off Leif's map
  onto Harald's), `PR-08`, `PR-09`, the codes-reference table row, the puzzle-candidate summary,
  the interactive prototype's caption, the "build" tab's prop-kit list, and the 3D-printer
  inventory line — all updated for the compartment drop, the pamphlet→ticket rename, and the
  Leif→Harald reassignment.

### Checks run

- Ran both build scripts; inspected all three PDF pages (map insert, ticket front, ticket back) at
  300dpi. Caught and fixed the two real bugs above before calling either script done.
- Verified the ticket's mirrored panel against the shared blocker data by hand: G-column blockers
  (G2, G4, G5) land in the left slot, F-column blocker (F2) in the right slot, matching the
  reversed G-then-F column order; corners G1/G7 render as open diamonds in the correct rows.
- HTML tag balance after all edits: 897 `div`, 12 `section`, 63 `figure`, 22 `details`, 23
  `article`, 13 `ul`, 108 `li` — all paired.
- Served over local HTTP (another session's `static-preview` on port 8734, joined directly since
  it serves the same repo checkout) and inspected the Puzzle details tab: heading, rules text and
  prototype caption all show the updated ticket/Harald wording; no console errors.
- Deleted temporary preview PNGs from `output/pdf/` after inspection; the three new production
  PDFs are left in place.

### Next action

Decide whether Codex should start Oslo's front artwork now (independent of the map, like Rouen's
front was built before its map/lock context existed) or wait — either way, Harald's trail map
sheet (`build_trail_maps_pdf.py`) is the real blocker for finishing this puzzle's physical props.

### Blockers / open items

- Harald's trail map sheet does not exist yet — two of his six stops (Sicily, Anatolia) are still
  regional anchors, not named places, which blocks the sheet itself, not just this puzzle.
- `PR-08` (which physical board to buy, 7×7 vs. 9×9/11×11) is still unchecked against real
  listings — now simpler since the compartment requirement is gone, but still unresolved.
- The Oslo postcard's front artwork and print PDF are both unbuilt — this session only wrote the
  message and Fun Fact into `PZ-05`.
- `PR-09`'s print test (does the offset read through the ticket, does the stain hide the original)
  is now buildable/testable since both scripts exist, but no physical print test has been run.

## Session Close — 2026-09-14 — Oslo postcard front

**Task:** create Postcard 13's Oslo front from the user-selected Wikimedia photograph of
Akershus Fortress viewed from the water, matching the approved postcard series.

**Done:** verified Balou46's source and CC BY-SA 4.0 licence, generated a screen-print nighttime
waterfront illustration, normalized it to 1500 × 1050 at 300 dpi, and added the shared
`OSLO / NORWAY` title treatment. The exact prompt, attribution and front-only status are recorded
in the Postcards tab and source register. The back and print PDF were not part of this session.

### Files changed

- `NorseBackpack/Postcards/Postcard_13_Oslo_Front.png` — finished front.
- `NorseBackpack/Postcards/Postcard_13_Oslo_Illustration_v1.png` — print-sized illustration.
- `NorseBackpack/Postcards/References/Postcard_13_Oslo_ImageGen_Source.png` — untouched ImageGen result.
- `NorseBackpack/Postcards/References/Oslo_Akershus_Balou46_Source.jpg` — Wikimedia source.
- `NorseBackpack/Postcards/build_postcard_front_images.py` — Oslo registered in the shared front builder.
- `NorseBackpack/Postcards/References/README.md` — attribution and adaptation notes.
- `NorseBackpack/Norse_Brainstorm.html` — gallery, overview, exact prompt and source summary.

### Checks run

- Inspected the Wikimedia source, generated illustration and titled front at full size.
- Confirmed the final front is 1500 × 1050 at 300 dpi.
- Served the design page over local HTTP and inspected the Oslo overview tile and gallery card in
  the in-app browser. The image loaded at its natural 1500 × 1050 size, the Postcards view was
  active, and the browser console had no warnings or errors. HTML tag counts remain balanced.

### Next action

Decide Postcard 13's message and Fun Fact before building its back and print PDF.

### Blockers / open items

- No front-art blocker remains. The back content and PDF are still unbuilt.

## Session Close — 2026-09-14 — Châlus postcard front

**Task:** create Postcard 04's Châlus front from the user-selected Wikimedia photograph of
Château de Châlus-Chabrol, matching the approved postcard series.

**Done:** verified Fonquebure's source and CC BY-SA 3.0 licence, generated a screen-print castle
illustration, normalized it to 1500 × 1050 at 300 dpi, and added the shared
`CHÂLUS / HAUTE-VIENNE` title treatment. The source photograph's white caption strip was excluded.
The exact prompt, attribution and front-only status are recorded in the Postcards tab and source
register. The back and print PDF were not part of this session.

### Files changed

- `NorseBackpack/Postcards/Postcard_04_Chalus_Front.png` — finished front.
- `NorseBackpack/Postcards/Postcard_04_Chalus_Illustration_v1.png` — print-sized illustration.
- `NorseBackpack/Postcards/References/Postcard_04_Chalus_ImageGen_Source.png` — untouched ImageGen result.
- `NorseBackpack/Postcards/References/Chateau_Chalus_Chabrol_Fonquebure_Source.jpg` — Wikimedia source.
- `NorseBackpack/Postcards/build_postcard_front_images.py` — Châlus registered in the shared front builder.
- `NorseBackpack/Postcards/References/README.md` — attribution and adaptation notes.
- `NorseBackpack/Norse_Brainstorm.html` — gallery, overview, exact prompt and source summary.

### Checks run

- Inspected the Wikimedia source, generated illustration and titled front at full size.
- Confirmed the final front is 1500 × 1050 at 300 dpi.
- Served the design page over local HTTP and inspected the Châlus overview tile and gallery card
  in the in-app browser. The image loaded at its natural 1500 × 1050 size, the Postcards view was
  active, and the browser console had no warnings or errors. HTML tag counts remain balanced.

### Next action

Decide Postcard 04's message and Fun Fact before building its back and print PDF.

### Blockers / open items

- No front-art blocker remains. The back content and PDF are still unbuilt.

## Session Close — 2026-09-14 — Rouen postcard front

**Task:** create Postcard 05's Rouen front from the user-specified Wikimedia Commons photograph
`Rouen Place du Vieux-Marché 05`, matching the approved postcard series.

**Done:** verified Zairon's source photograph and CC BY-SA 4.0 licence, generated a
screen-print-style Old Market Square illustration, normalized it to 1500 × 1050 at 300 dpi, and
added the shared `ROUEN / NORMANDY` title treatment. The prompt, source credit and front-only
status are recorded in the Postcards tab and source register. The back and print PDF are not part
of this session.

### Files changed

- `NorseBackpack/Postcards/Postcard_05_Rouen_Front.png` — finished front.
- `NorseBackpack/Postcards/Postcard_05_Rouen_Illustration_v1.png` — print-sized illustration.
- `NorseBackpack/Postcards/References/Postcard_05_Rouen_ImageGen_Source.png` — untouched ImageGen result.
- `NorseBackpack/Postcards/References/Rouen_Place_du_Vieux_Marche_Source.{jpg,png}` — Wikimedia source and compatibility copy.
- `NorseBackpack/Postcards/build_postcard_front_images.py` — Rouen registered in the shared front builder.
- `NorseBackpack/Postcards/References/README.md` — attribution and adaptation notes.
- `NorseBackpack/Norse_Brainstorm.html` — gallery, overview, exact prompt and source summary.

### Checks run

- Inspected the Wikimedia source, generated illustration and titled front at full size.
- Confirmed the final front is 1500 × 1050 at 300 dpi.
- Served the design page over local HTTP and inspected the Rouen overview tile and gallery card in
  the in-app browser. The image loaded at its natural 1500 × 1050 size, the Postcards view was
  active, and the browser console had no warnings or errors. HTML tag counts remain balanced.

### Next action

Build `build_postcard_05_pdf.py` from the already-decided Rouen message, Fun Fact and word-lock
order clue, then render the back and print PDF.

### Blockers / open items

- No front-art blocker remains. The back, postmark treatment and PDF still need building.

## Session Close — 2026-09-14 — Château de Robert le Diable line icon

**Task:** create a simple black architectural line icon from the user-specified Wikimedia Commons
photograph `2014-Chateau-Robert-LeDiable.jpg`, with a transparent background.

**Done:** downloaded W. Mechelke's 3008 × 2000 original (CC BY-SA 3.0), verified the attribution
and licence on Commons, and used it as the sole structural reference. The accepted drawing keeps
the left round crenellated tower, broken central wall, receding curtain wall, major openings and
the source photograph's cropped right tower while omitting foliage, ground, railings and stone
texture. The first generation baked in a checkerboard; a second ImageGen background-extraction
pass produced genuine alpha. A reproducible cleanup normalizes the final 1536 × 1024, 300 dpi PNG
to exact black over transparency. The icon is not yet placed on Map 2.

### Files changed

- `NorseBackpack/TravelMap/Art/Rollo_Chateau_Robert_Le_Diable_Line_v1.png` — production icon.
- `NorseBackpack/TravelMap/Art/Sources/Chateau_Robert_Le_Diable_WMechelke_Source.jpg` — original
  Wikimedia photograph.
- `NorseBackpack/TravelMap/Art/Sources/Rollo_Chateau_Robert_Le_Diable_Line_v1_ImageGen_Source.png`
  — accepted transparent ImageGen render.
- `NorseBackpack/TravelMap/prepare_chateau_line_icon.py` — reproducible alpha/RGB/canvas cleanup.
- `NorseBackpack/Norse_Brainstorm.html` — gallery, source attribution, CC BY-SA note and exact
  two-stage ImageGen prompts added to the Design guide.

### Checks run

- Inspected the source photo, accepted render and normalized icon.
- Verified production output is 1536 × 1024 RGBA at 300 dpi, alpha extrema 0–255, with only
  `(0, 0, 0)` in visible RGB pixels.
- Served the design page over local HTTP and inspected the icon, caption and source/licence block
  in the in-app browser. The image loaded at its natural 1536 × 1024 size and the browser console
  has no warnings or errors. HTML tag counts remain balanced.

### Next action

User reviews the icon. If approved, decide its exact Map 2 size and location before editing the
map builder; placement must avoid labels and the final drawn-route corridor.

### Blockers / open items

- No technical blocker. Map placement was not requested and remains open.

## Session Close — 2026-09-14 — Six additional Map 2 word icons

**Task:** generate one Rollo/Map 2 icon for each paired English-word concept: Combat/Fight,
Beef/Cow, Forest/Woodland, Poultry/Hen, People/Folk and Tavern/Inn. The pairs are synonyms from
different origins, so the deliverable is six icons, not twelve.

**Done:** generated crossed sword/axe, cow, three-tree woodland, hen, three ordinary townspeople
and timber inn/tankard-sign subjects using the existing Rollo map art as style references. Forest,
folk and inn initially contained baked transparency checkerboards; corrected those with a second
ImageGen background-extraction pass. Ran all six through the existing normalization script so
each production asset is a 1024 × 1024 transparent PNG at 300 dpi with every visible RGB pixel
exactly `#A2562D`. Icons are built but not placed on Map 2.

### Files changed

- `NorseBackpack/TravelMap/Art/Rollo_{Combat,Cow,Forest,Hen,Folk,Inn}_v1.png` — six production
  icons.
- `NorseBackpack/TravelMap/Art/Sources/Rollo_{Combat,Cow,Forest,Hen,Folk,Inn}_v1_ImageGen_Source.png`
  — accepted raw or transparency-corrected renders.
- `NorseBackpack/TravelMap/normalize_rollo_vignettes.py` — six new assets added to the reproducible
  normalization list.
- `NorseBackpack/Norse_Brainstorm.html` — six-icon gallery, status and exact generation/correction
  prompts added to the Design guide.

### Checks run

- Inspected all six source renders and all six normalized assets.
- Verified every production file is 1024 × 1024 RGBA with alpha extrema 0–255 and only
  `(162, 86, 45)` in visible RGB pixels.
- Rendered the set at approximately 0.43 in / 300 dpi on the map's cream colour; all six concepts
  remain recognizable.
- Served the design page over local HTTP and inspected the six-icon gallery in the in-app browser;
  all six images loaded at their natural 1024 × 1024 size, the 3 × 2 layout is clean, and the
  browser console has no warnings or errors. HTML tag counts remain balanced.

### Next action

User reviews the six icons. If approved, decide their actual Map 2 locations before changing the
map builder; placement must respect stop labels and the final drawn-route corridor.

### Blockers / open items

- No technical blocker. Map placement was not requested and remains open.

## Session Close — 2026-09-14 — Battle postcard front artwork

**Task:** continue the postcard image set with the Battle/Hastings stop, using the user-specified
Wikimedia Commons photograph of the wooden archer sculpture at the battlefield and the same
screen-print travel-poster style as the approved fronts.

**Done:** downloaded Richard Cooke's exact Commons source and verified its CC BY-SA 2.0 licence.
Used it as the scene reference alongside four finished postcard illustrations as style/layout
references. The first ImageGen render was accepted: it keeps the carved kneeling archer clearly
wooden, the drawn longbow, open field, tree line, distant Battle Abbey and broad summer sky, with
no reenactment or invented figures. Normalized the 1499 × 1049 render to the exact PC-13 1500 ×
1050 size at 300 dpi, then used the shared builder to add `BATTLE / EAST SUSSEX`. Card 08 is
front-only; its message, Fun Fact, assigned tree/teacup rebus, back and print PDF remain unwritten.

### Files changed

- `NorseBackpack/Postcards/Postcard_08_Battle_Illustration_v1.png` — print-sized illustration.
- `NorseBackpack/Postcards/Postcard_08_Battle_Front.png` — titled postcard front.
- `NorseBackpack/Postcards/References/Battle_Hastings_Sculpture_Source.jpg` — exact source.
- `NorseBackpack/Postcards/References/Postcard_08_Battle_ImageGen_Source.png` — raw render.
- `NorseBackpack/Postcards/References/README.md` — source, licence and adaptation notes.
- `NorseBackpack/Postcards/build_postcard_front_images.py` — Battle added to the shared list.
- `NorseBackpack/Norse_Brainstorm.html` — Rollo overview thumbnail, front-only gallery entry,
  source note and exact production prompt.

### Checks run

- Inspected the photograph, normalized illustration and titled front at full size.
- Confirmed both production PNGs are 1500 × 1050; the illustration records 300 dpi.
- HTML tag balance: 827 `div`, 11 `section`, 47 `figure`, 17 `details` and 19 `article` elements,
  all paired.
- Served over local HTTP and checked the Postcards tab: overview thumbnail and gallery image load
  at natural size 1500 × 1050; the new front lays out cleanly; no browser warnings or errors.

### Next action

Create the next user-selected front. Build Battle's back only after its message and Fun Fact are
approved; the tree/teacup rebus placement is already assigned by `PZ-14`.

### Blockers / open items

- No technical blocker. Battle is not fully built, so the Rollo count remains 1 of 6 and the
  overview correctly shows its artwork without a completion checkmark.

## Session Close — 2026-09-14 — Winchester postcard front artwork

**Task:** continue the postcard image set with Winchester, using the user-specified Wikimedia
Commons photograph of Winchester Cathedral and the same screen-print travel-poster style as the
approved fronts.

**Done:** downloaded Graham Horn's exact Commons source and verified its CC BY-SA 2.0 licence.
Used it as the scene reference alongside cards 01–03 and Bayeux as style/layout references. The
first ImageGen render was accepted: it retains the elevated winter view, long cathedral nave,
square central tower, west front, layered roofs and snow-dusted ridge in the set's flat,
lightly-distressed palette. Normalized the 1499 × 1049 render to the exact PC-13 1500 × 1050 size
at 300 dpi, then used the shared front builder to add `WINCHESTER / ENGLAND`. Card 07 is front-only;
its message, Fun Fact, assigned cross/bow/lightning rebus, back and print PDF remain unwritten.

### Files changed

- `NorseBackpack/Postcards/Postcard_07_Winchester_Illustration_v1.png` — print-sized illustration.
- `NorseBackpack/Postcards/Postcard_07_Winchester_Front.png` — titled postcard front.
- `NorseBackpack/Postcards/References/Winchester_Cathedral_Graham_Horn_Source.jpg` — exact source.
- `NorseBackpack/Postcards/References/Postcard_07_Winchester_ImageGen_Source.png` — raw render.
- `NorseBackpack/Postcards/References/README.md` — source, licence and adaptation notes.
- `NorseBackpack/Postcards/build_postcard_front_images.py` — Winchester added to the shared list.
- `NorseBackpack/Norse_Brainstorm.html` — Rollo overview thumbnail, front-only gallery entry,
  source note and exact production prompt.

### Checks run

- Inspected the photograph, normalized illustration and titled front at full size.
- Confirmed both production PNGs are 1500 × 1050; the illustration records 300 dpi.
- HTML tag balance: 824 `div`, 11 `section`, 46 `figure`, 16 `details` and 18 `article` elements,
  all paired.
- Served over local HTTP and checked the Postcards tab: the overview thumbnail and gallery image
  load at natural size 1500 × 1050; the new front lays out cleanly; no browser warnings or errors.

### Next action

Create the next user-selected front. Build Winchester's back only after its message and Fun Fact
are approved; the cross/bow/lightning rebus placement is already assigned by `PZ-14`.

### Blockers / open items

- No technical blocker. Winchester is not a fully built card, so the Rollo count remains 1 of 6
  and the overview correctly shows its artwork without a completion checkmark.

## Session Close — 2026-09-14 — Bayeux postcard front artwork

**Task:** continue the postcard image set with Bayeux, using the user-specified Wikimedia Commons
photograph of Bayeux Tapestry Scene 57 and the same screen-print travel-poster style as cards
01–03.

**Done:** downloaded the exact Commons source, verified its CC0/public-domain status, and used it
as the scene reference alongside the three finished postcard illustrations as style/layout
references. The first ImageGen render was accepted without a second generation: it preserves the
standing soldier, arrow-struck shield bearer, mounted figure, fallen warrior, inscription and
animal borders in a limited-palette screen-print treatment. Normalized the 1499 × 1049 render to
the exact PC-13 1500 × 1050 size at 300 dpi, then used the shared postcard-front builder to add
`BAYEUX / NORMANDY` in the established title band. Card 06 is front-only; its message, Fun Fact,
imprint, back and print PDF remain unwritten. The generated Latin inscription is decorative and
close to the source, but is not a letter-perfect scholarly transcription.

### Files changed

- `NorseBackpack/Postcards/Postcard_06_Bayeux_Illustration_v1.png` — print-sized illustration.
- `NorseBackpack/Postcards/Postcard_06_Bayeux_Front.png` — titled postcard front.
- `NorseBackpack/Postcards/References/Bayeux_Tapestry_scene57_Harold_death_Source.jpg` — exact
  user-specified source image.
- `NorseBackpack/Postcards/References/Postcard_06_Bayeux_ImageGen_Source.png` — untouched render.
- `NorseBackpack/Postcards/References/README.md` — source, licence and adaptation notes.
- `NorseBackpack/Postcards/build_postcard_front_images.py` — Bayeux added to the shared front list.
- `NorseBackpack/Norse_Brainstorm.html` — Rollo overview thumbnail, front-only gallery entry,
  source note and exact production prompt.

### Checks run

- Inspected the source, normalized illustration and titled front at full size.
- Confirmed both production PNGs are 1500 × 1050; the illustration records 300 dpi.
- Confirmed Bayeux uses the same shared typography routine as cards 01–03 and the title sits fully
  inside the blank navy band.
- HTML tag balance remained valid: 821 `div`, 11 `section`, 44 `figure`, 15 `details` and 17
  `article` elements, all paired. Served over local HTTP and checked the Postcards tab: the Bayeux
  overview thumbnail and full gallery image both load at natural size 1500 × 1050, the new entry
  lays out cleanly, the correct view is active, and the browser console has no warnings or errors.

### Next action

Create the next user-selected postcard front. Bayeux's back should wait until its message and Fun
Fact are approved (`PZ-05`), since this session was image-only.

### Blockers / open items

- No technical blocker. Bayeux is not a complete card yet, so it remains excluded from the
  “fully built” count and has no checkmark in the overview.

## Session Close — 2026-09-14 — Norse hint page copied into the live escape-backpack-games repo

**Task:** follow-up to the prior session's `NorseBackpack/norse-hints.html` (built in this repo,
matching the Hiking Backpack's live hint-companion format). The user asked to copy it into the
actual `escape-backpack-games` repo so it goes live at the real URL.

**Done:** that repo (`OttawaVisuals/escape-backpack-games`, public, flat file structure —
`index.html`, `styles.css`, `assets/`, `hiking-hints.html`, etc. at root) wasn't cloned anywhere on
this machine, so this session cloned it fresh to `C:\EscapeBackpack\escape-backpack-games` (a
sibling of this repo, outside it — not tracked here). Confirmed the repo's own `styles.css` and
`assets/logo.png` are the canonical originals (this repo's copies in `NorseBackpack/` were just a
local preview copy, byte-for-byte the same content), so only `norse-hints.html` itself was copied
in — no need to touch the shared assets. Asked and confirmed two scope questions before pushing:
(1) don't add Norse to `index.html`'s backpack grid or any other page's nav dropdown yet — only 5 of
9 planned puzzle stations are real, so site-wide discoverability is a separate decision for later;
(2) commit and push now rather than leaving it staged. Committed and pushed straight to `main`
(`4fc3519`); GitHub Pages rebuilt within about a minute.

**Live now:** https://ottawavisuals.github.io/escape-backpack-games/norse-hints.html — verified with
no console errors, using the repo's real `styles.css`/logo (not the local preview copies).

### Files changed

- `C:\EscapeBackpack\escape-backpack-games\norse-hints.html` — new, pushed to `main`. **This path is
  outside this repo** — nothing here tracks it; future sessions working on the public hint page need
  to go to that clone (or re-clone it) rather than editing `NorseBackpack/norse-hints.html` and
  expecting it to be the live copy anymore. Keep both in sync by hand until/unless a better workflow
  is set up.
- No changes in this repo this session beyond this handoff entry.

### Checks run

- Diffed the local `NorseBackpack/styles.css`/`assets/logo.png` against the escape-backpack-games
  repo's own copies — content-identical (one added comment line in the CSS, negligible size
  difference in the PNG from a base64 round-trip); used the repo's canonical files rather than
  overwriting them.
- Served the copied file locally against the repo's real assets (temporary `python -m http.server
  8735` in the clone) before pushing: loaded clean, no console errors.
- After pushing, polled the live GitHub Pages URL until it returned 200, then loaded it in the
  browser: correct title, no console errors, matches the pre-push local check.

### Next action

Decide whether/when to make Norse discoverable site-wide (homepage card + nav dropdown on every
other page) — deliberately not done this session. Also decide how the two copies of
`norse-hints.html` (this repo's `NorseBackpack/` original and the pushed one in the separate clone)
should be kept in sync going forward, since they are two different files on disk now.

### Blockers / open items

- `C:\EscapeBackpack\escape-backpack-games` is a separate git repo/clone, not a submodule or
  otherwise linked from this repo — a future session needs to know it exists and where, since
  nothing in this repo's structure points to it.
- Same 4 illustrative-only Norse puzzles (rune relic, family connection, king's escape, saga in
  pieces) and station 3's unwritten in-fiction hint text remain open from the prior session.

## Session Close — 2026-09-14 — Postcards tab: new "All 18, by trail" overview

**Task:** the user asked for a visual overview on the Postcards tab: all four trails with their
colours, one small box per postcard showing the front art (where built), a checkmark on completed
cards, and a highlight on specific postcards. The highlight criterion went through two rounds —
first proposed as "the last stop of each trail" (guessed, per the user's phrasing "to stay out"),
then corrected once the user clarified they meant the cards decided in `PZ-11` to be held back
until the final container, so the map/deck doesn't leak a digit early. Searched
`Norse_Brainstorm.html` for that decision rather than relying on memory, since `PZ-11` isn't
something recorded in Claude Code's cross-session memory.

**Built:** a new "All 18, by trail" block in the Postcards tab, above the existing card gallery.
Four `trail-group`s (Leif `#216580`, Rollo `#a2562d`, Aud `#6d528b`, Harald `#467444`, matching the
stamp-series colours already decided), each showing its real route stops from
`TravelMap/Norse_Aunt_Route_Plan.json`'s `visits` block in order (3+6+3+6 = 18, confirmed against
that file). Built cards (01, 02, 03 — all Leif's) show their real front art with a checkmark badge;
unbuilt stops show a dashed, trail-tinted placeholder box with just the stop name. A rust "Held
back" banner marks the three `PZ-11` cards: **Rollo — Roumare forest** (stop 6), **Aud — Hvammur**
(stop 2), **Harald — Staraya Ladoga** (stop 2, labelled "Held back?" since `PZ-11` itself calls that
one provisional pending Harald's map sheet). Leif's trail carries no held-back badge — `PZ-11`
explicitly excludes it as the deliberate "teaching trail." A legend at the bottom of the block spells
out all three states and links back to `PZ-11`.

### Files changed

- `NorseBackpack/Norse_Brainstorm.html` — new `.trail-overview`/`.pc-box`/`.pc-held` CSS block; new
  "All 18, by trail" markup in the `#postcards` section, with a full pass correcting it from a
  first (wrong) "final leg of trail" framing to the actual `PZ-11` held-back set.

### Checks run

- Served over local HTTP (`static-preview`, port 8734): no console errors. Verified via a
  cache-busted reload (`?cb=2`, same known caching quirk as prior sessions — the shared server
  returns a stale response on a plain re-navigate to an already-visited URL) that all three
  "Held back" badges landed on the correct boxes (Roumare forest, Hvammur, Staraya Ladoga) and that
  Leif's cards carry only the checkmark, no held-back badge.
- Cross-checked the 18-stop count and per-trail split (3/6/3/6) against
  `TravelMap/Norse_Aunt_Route_Plan.json` directly rather than assuming.

### Next action

Nothing queued specifically from this session. If continuing on postcards, cards 04–18 (Rollo, Aud,
Harald) are still entirely unwritten — same backlog as before (`PC-07`/`PZ-05`).

### Blockers / open items

- Harald's held-back card (Staraya Ladoga) is provisional per `PZ-11` itself — re-test once Harald's
  real map sheet exists (`build_trail_maps_pdf.py` currently has no Harald sheet; two of his stops
  are still regions, not named places).
- All the pre-existing blockers below (postmark dates, Hnefatafl placement, 15 unbuilt cards, etc.)
  are unchanged by this session.

## Session Close — 2026-09-14 — Five Bayeux-style postcard margin symbols

**Task:** create a Roman numeral I, an arrow/2 hybrid, a face-on die showing five, a separate plain
right-pointing arrow meaning “to,” and a fish-scale patch meaning “scale,” matching Aunt Liv's
existing multicolour Bayeux-style postcard drawings.

**Done:** generated all five with the built-in ImageGen workflow using
`Postcards/RebusIcons/Sources/Bayeux_Reference_Crop.png` as a style/palette reference. The first
three source renders baked a fake transparency checkerboard into RGB; the plain arrow arrived with
genuine alpha, as did the fish-scale patch. `prepare_bayeux_margin_symbols.py` handles both source types, removes isolated grid
fragments where needed, recentres the artwork and writes genuine 1024 × 1024 RGBA PNGs at 300 dpi.
Updated `PC-15` from five to ten unassigned margin drawings and added the new gallery and exact
prompts to the Design guide. No postcard builder or card-to-symbol assignment was changed.

### Files changed

- `NorseBackpack/Postcards/RebusIcons/Rebus_{Roman_I,Arrow_2,Die_5,Arrow_To,Fish_Scales}_Bayeux_v1.png` — production
  assets.
- `NorseBackpack/Postcards/RebusIcons/Sources/Rebus_{Roman_I,Arrow_2,Die_5,Arrow_To,Fish_Scales}_Bayeux_v1_ImageGen_Source.png`
  — untouched ImageGen renders.
- `NorseBackpack/Postcards/RebusIcons/prepare_bayeux_margin_symbols.py` — reproducible alpha cleanup.
- `NorseBackpack/Postcards/RebusIcons/Bayeux_Margin_Symbols_v1_PrintScale_Preview.png` — 0.45 in
  proof at 300 dpi on the project cream ground.
- `NorseBackpack/Norse_Brainstorm.html` — `PC-15`, gallery, production notes and exact prompts.

### Checks run

- Full-size visual inspection: exactly one I, one right-pointing arrow/2 hybrid, one flat die with
  exactly five pips, one separate straight right-pointing arrow and one seven-scale patch; no extra
  objects or competing meanings of “scale.”
- Pixel checks: each production asset is 1024 × 1024 RGBA at 300 dpi, alpha spans 0–255, has one
  connected visible component and does not touch the canvas edge.
- 0.45 in / 135 px proof inspected: all five remain distinct and readable.
- Served the HTML over local HTTP and inspected the Design guide: all eight gallery images render,
  the new row fits cleanly, and the prompt disclosure is present. HTML tag counts remain balanced.

### Next action

Decide the card-to-symbol mapping and reading order for `PC-15`, then place the selected symbols in
the relevant postcard builders at 0.4–0.5 in and rebuild those PDFs.

### Blockers / open items

- `PC-15` remains open by design; no target postcards were specified.

## Session Close — 2026-09-13 (later still) — Norse public hint-companion page, v1 (5 real stations)

**Task:** start a public player-facing hint page for the Norse Backpack, matching the format of the
live Hiking Backpack hint companion the user pointed to
(`https://ottawavisuals.github.io/escape-backpack-games/hiking-hints.html`). That site is a
**separate GitHub repo** (`ottawavisuals.github.io/escape-backpack-games`), not this one — this
session read its rendered structure and the shared `styles.css`/`assets/logo.png` from the live
site (plus a local reference copy of its full HTML the user provided at
`NorseBackpack/Source_Info/hiking-hints.html`) to reproduce the format here, but did not get push
access to that other repo.

**Format reproduced exactly:** single self-contained HTML file, team-name entry → timer →
station grid → progressive per-station hint modal (Hint #1/#2/#3/Solution, expand-one-at-a-time) →
completion screen, with localStorage session persistence and an optional fire-and-forget Google
Apps Script logger (same shared nav/palette as the live site: forest green + brass + rust, Young
Serif/Inter Tight/JetBrains Mono).

**Content scope — asked and answered before writing anything:** the user chose "5 real stations
only" over including all of Norse's puzzle set. Cross-checked every entry in `Norse_Brainstorm.html`'s
`puzzles` array first and found four of them (`the rune-labelled relic`, `the family connection`,
`the king's unfinished escape`, `the saga in pieces`) explicitly carry **illustrative, not-real**
codes (the array literally says "Values illustrative" against 582/427/2468/231) — publishing those
as if they were real answers would hand players a wrong solution, so they are deliberately left off
this page entirely rather than shown as placeholders. The 5 stations that do appear use only
puzzle-array content that is real:

1. The Opening Puzzle → `1021`
2. The Beasts on the Chart → `3212` (BEAR)
3. The Joined Top Edge → `1576` (real code; the source array's hint text is literally
   `['Not written yet.']` for this one, so hint #1 here states plainly that no in-fiction nudge
   exists yet and just gives the decided physical mechanism instead of inventing flavour text)
4. The Route Hidden in Plain Sight (final) → `1972`
5. See You in Norway (ending, no code)

No invented time estimates or benchmark numbers: the Hiking page's completion screen compares your
time to a benchmark best/average, but Norse has never been playtested, so those numbers would be
fabricated. The Norse completion screen instead shows only your own time plus a note that no
benchmark exists yet. `LOGGER_URL` is left empty (not a fake endpoint) — the existing `logAsync()`
guard already no-ops safely when it's blank, exactly like the Hiking page's own guard against
placeholder URLs.

### Files changed

- `NorseBackpack/norse-hints.html` — new. The public hint-companion page.
- `NorseBackpack/styles.css` — new. Copy of the live site's shared stylesheet, so the page renders
  correctly both here and if later dropped into the `escape-backpack-games` repo.
- `NorseBackpack/assets/logo.png` — new. Copy of the live site's nav brand-mark image.

### Checks run

- Served over local HTTP (`static-preview`, port 8734): no console errors on
  `NorseBackpack/norse-hints.html`.
- Walked the flow live: entered a team name, started the timer, opened hint panels for stations 3
  (2 hint levels) and 5 (1 hint level) and confirmed only the real number of levels renders (no
  phantom "Solution" label when fewer than 4 entries exist) — the hint-count logic scales correctly
  per station.
- Confirmed the nav "Hints" dropdown lists both Hiking and Norse as Live with correct relative
  links, matching the live site's pattern.
- Did not fully exercise the Done→complete-screen confirm flow interactively (a click-coordinate
  mismatch after a viewport resize got in the way, not a code issue) — that logic is unmodified from
  the Hiking page's already-proven implementation, so it was not re-verified line-by-line.

### Next action

Decide whether/how to port this file into the actual `escape-backpack-games` repo (this session has
no access to it) — or keep developing it here until Norse's remaining puzzle stations are decided,
then add them as real stations rather than placeholders.

### Blockers / open items

- No access to the `escape-backpack-games` repo, so this page cannot go live at the same URL as the
  Hiking page without a manual copy-over by the user (or granting access in a future session).
- The 4 illustrative-only puzzles (rune relic, family connection, king's escape, saga in pieces)
  still need real decided answers before they can be added to this page.
- Station 3's hint ladder still has no real in-fiction hint text (`PZ-05` backlog) — only the
  mechanism and solution are written.

## Session Close — 2026-09-13 (later) — Fixed a real stop dropped from Rollo's map; brainstormed the Châlus/Saint-Clair-sur-Epte rebus lock

**Task:** review Codex's newly-built Rollo map icons (previous session below), then design the next
lock mechanism (2+ cards, per the user's request for locks needing more than one card) around a
Bayeux-Tapestry-style rebus.

**Rebus lock designed (not yet written into `Norse_Brainstorm.html` as a `PZ-` entry):** two
postcard rebuses — cross+bow+lightning → CROSSBOW BOLT (Châlus) and tree+teacup → TREATY
(Saint-Clair-sur-Epte) — point players to the matching full icon on Rollo's map; the distance
between those two icons, read with the architect's scale ruler already on hand, is the lock input.
5 postcard rebus icons (cross, bow, lightning, tree, teacup) were generated by Codex in tapestry
style (`NorseBackpack/Postcards/RebusIcons/`, v2/Bayeux palette kept, v1 flat-icon version rejected
as not tapestry-like enough) and a scratch placement mockup was rendered to check legibility on an
actual card back (scratchpad only, not committed — placeholder message text, Rollo's real card copy
is still unwritten per `PZ-05`).

**Real bug found and fixed while inspecting Codex's Rollo map build:** `Trail_Map_2_Rollo_Print.pdf`
was silently dropping the label for **Roumare forest** — one of the six real route stops needed to
draw Rollo's final digit-9 shape — to a label-collision with the newly-added icon boxes. This was
already present in Codex's build before this session touched anything (confirmed by reverting the
file and reproducing it); the console output has always reported dropped labels via a
`STOPS NOT LABELLED ON SHEET` line, but nobody had checked it since the icons were added. Also
opportunistically confirmed neither `Saint-Clair-sur-Epte` nor `Roumare forest` printed on the map
before the fix (contradicts `PZ-09`'s claim that Saint-Clair-sur-Epte is "already labelled" — that
claim is stale and should be corrected next time `PZ-09` is touched).

**Fix:** nudged the treaty-scroll and ducal-coronet icon boxes in `ROLLO_ART`
(`build_trail_maps_pdf.py`) by a small offset found via a brute-force search over nearby positions,
checking the script's own `missing + collided` return value after each try rather than guessing.
The result is zero real stops dropped (only decorative corpus towns — Caen, Hastings, Lewes, etc. —
are dropped, same as before the icons existed). The coronet still isn't perfectly centred on the
Rouen dot — every tighter position tried reopened the Roumare collision — so it reads as "near
Rouen" rather than sitting exactly on it. A cleaner fix would need Codex to re-flow more of the
cluster (Rouen, Roumare, Saint-Clair-sur-Epte, Bayeux icons all sit within ~50pt of each other), not
just a two-box nudge.

### Files changed

- `NorseBackpack/TravelMap/build_trail_maps_pdf.py` — `ROLLO_ART` treaty-scroll and ducal-coronet
  box positions.
- `output/pdf/Trail_Map_2_Rollo_{Print,ANSWER}.pdf` — rebuilt with the fix.
- `NorseBackpack/Postcards/RebusIcons/` (Codex, this session) — 5 rebus icons, v1 and v2, plus
  ImageGen source renders.
- `NorseBackpack/TravelMap/Art/Rollo_*_v1.png` (Codex, this session) — 7 map icons; see Codex's
  session entry below for the generation details.

### Checks run

- Reproduced the pre-existing label-collision bug by reverting the file and rebuilding; confirmed
  it predates this session's edits.
- Ran `build_trail_maps_pdf.py rollo` after the fix: console reports zero real stops in
  `STOPS NOT LABELLED ON SHEET` (that line no longer appears at all).
- Visually inspected the fixed region at 600 dpi: Rouen, Roumare forest and Saint-Clair-sur-Epte all
  print clearly; crossbow bolt (Châlus) and needle-and-thread (Bayeux) were already correctly
  anchored and untouched.
- Rendered the 5 rebus icons (v1 and v2) at print scale; v2 (Bayeux palette) confirmed legible and
  kept, v1 rejected.
- Did not re-run the full HTML QA pass (no `Norse_Brainstorm.html` changes yet — the rebus lock is
  not written up as a `PZ-` entry, see below).

### Next action

Write the crossbow-bolt/treaty rebus lock up as a new `PZ-` entry in `Norse_Brainstorm.html` (design
is agreed in chat but not yet recorded on the page, per `AGENTS.md`'s "Where Design State Lives"
rule), and correct `PZ-09`'s stale claim that Saint-Clair-sur-Epte was already labelled.

### Blockers / open items

- Rollo's card message content is still unwritten (`PZ-05`) — the placement mockup used placeholder
  text only.
- The coronet-vs-Rouen-dot centring is a minor cosmetic gap, not a functional one; leaving it unless
  Codex does a fuller layout pass.
- The user separately raised a possible third rebus (fish = "scale," combined with a ratio number
  from the architect's ruler's marked scales) as a further clue layer on the same lock — still being
  brainstormed, not designed.

## Session Close — 2026-09-13 — Rollo map vignettes

**Task:** add the supplied seven rust-brown story icons to the second printable Norse trail map,
matching the decorative treatment already used on Leif's first map.

**Done:** generated a crossbow bolt, treaty scroll, ducal coronet, needle and thread, royal crown,
longship and boar with the built-in ImageGen tool. The untouched source renders are retained. A
reproducible normalization pass removes ImageGen's low-alpha glow, fits each subject to a consistent
1024 px square canvas, adds 300 dpi metadata and sets every visible pixel to exact `#A2562D` while
preserving transparency. Added all seven to Rollo's print and answer maps at 0.55–0.7 in visible
size, beneath labels and outside the solved route's 26 pt keep-clear corridor. The crown stays on
England and the longship at sea. Exact prompts and the full icon gallery are recorded in the Design
guide; the Travel routes gallery now describes the illustrated Rollo sheet.

### Files changed

- `NorseBackpack/TravelMap/Art/Rollo_*_v1.png` — seven normalized production icons.
- `NorseBackpack/TravelMap/Art/Sources/Rollo_*_v1_ImageGen_Source.png` — seven untouched renders.
- `NorseBackpack/TravelMap/normalize_rollo_vignettes.py` — reproducible cleanup step.
- `NorseBackpack/TravelMap/build_trail_maps_pdf.py` — Rollo placement table and compositing.
- `output/pdf/Trail_Map_2_Rollo_{Print,ANSWER}.pdf` — rebuilt map and designer answer key.
- `NorseBackpack/Norse_Brainstorm.html` — PR-11 state, gallery and exact prompts.
- `HANDOFF.md` — this session record.

### Checks run

- Visually inspected all seven normalized icons together; each subject is recognizable and the
  coronet/closed crown remain distinct.
- Verified all seven production PNGs are 1024 × 1024, 300 dpi, RGBA, alpha 0–255, and use only
  RGB `(162, 86, 45)` / `#A2562D` in visible pixels.
- Rebuilt and visually inspected both one-page US Letter PDFs. Labels remain readable, the longship
  is at sea, the crown is on England, and the answer route does not cross any vignette.
- Served `Norse_Brainstorm.html` over local HTTP. The Travel routes and Design guide entries render,
  all nine Rollo image references load at 1024 × 1024, and the browser reports no console errors.
- Python compile checks and targeted `git diff --check` passed.

### Next action

Print Rollo's map at true size and confirm all seven icons remain recognizable through the intended
lamination and reduced-opacity treatment.

### Blockers / open items

- No implementation blocker. The true-size physical print check remains outstanding.

## Session Close — 2026-09-13 — Aunt Liv's multicolour Bayeux rebus drawings

**Task:** revise the five postcard rebus icons so they read as drawings by Aunt Liv and use the
style and colours of the supplied Bayeux Tapestry reference, rather than the earlier single rust
colour.

**Done:** created a v2 set for cross, horizontal recurve bow, lightning bolt, flattened tree and
teacup. The new drawings use irregular blue-black outlines and restrained terracotta, ochre and
sage-blue fills sampled visually from the reference. They remain compact transparent assets rather
than photographed embroidery. The original one-colour files are retained as v1. Added `PC-15`
because the repo still does not say which postcard carries which symbol or what the rebus order is;
no postcard builder was changed without that mapping.

### Files changed

- `NorseBackpack/Postcards/RebusIcons/Rebus_*_Bayeux_v2.png` — five revised 1024 px assets.
- `NorseBackpack/Postcards/RebusIcons/Rebus_Icons_Bayeux_v2_{Preview,PrintScale_Preview}.png` —
  full-size and true 0.5 in review sheets.
- `NorseBackpack/Postcards/RebusIcons/Sources/*_Bayeux_v2_ImageGen_Source.png` — raw renders.
- `NorseBackpack/Postcards/RebusIcons/Sources/Bayeux_Reference_Crop.png` — lightweight reference crop.
- `NorseBackpack/Norse_Brainstorm.html` — v2 gallery, exact prompts, attribution and `PC-15`.
- `HANDOFF.md` — this session record.

### Checks run

- Visually inspected both five-up previews on the project cream ground; the set reads consistently
  and all five silhouettes remain clear at 0.5 in / 150 px at 300 dpi.
- Verified all five production PNGs are 1024 × 1024, 300 dpi, RGBA, with alpha spanning 0–255.
- Served the design page over local HTTP: the five v2 images render in the gallery, `PC-15` appears
  in Open questions, and the page reports no browser console errors.

### Next action

Decide the card-to-symbol mapping and reading order for `PC-15`, then place the drawings at a true
0.4–0.5 in print size in the relevant postcard builders and rebuild those PDFs.

### Blockers / open items

- `PC-15`: target postcards and rebus order are not recorded.

## Session Close — 2026-09-13 — Bayeux-style postcard rebus icons

**Task:** generate five tiny transparent rebus icons for a printable postcard: cross, bow,
lightning bolt, tree and teacup.

**Done:** created five 1024 × 1024 transparent PNGs at 300 dpi. Each uses only exact rust-brown
`#A2562D` in visible pixels. The silhouettes are intentionally simple at 0.4–0.5 in print size:
plain Latin cross, horizontal strung recurve bow, single jagged bolt, flattened medieval tree and
plain handled teacup on a saucer. ImageGen repeatedly introduced literal yarn texture or tonal glow,
so the accepted flat alpha masks were normalized mechanically to one ink colour on consistent square
canvases. The accepted source renders and exact production prompts are retained.

### Files changed

- `NorseBackpack/Postcards/RebusIcons/Rebus_{Cross,Bow,Lightning,Tree,Teacup}.png` — final icons.
- `NorseBackpack/Postcards/RebusIcons/Rebus_Icons_Preview.png` — cream-background review sheet.
- `NorseBackpack/Postcards/RebusIcons/Sources/*_ImageGen_Source.png` — accepted source renders.
- `NorseBackpack/Norse_Brainstorm.html` — preview gallery, production notes and exact prompts.
- `HANDOFF.md` — this session record.

### Checks run

- Inspected the five-icon montage on the project cream background: all silhouettes read clearly.
- Verified every final file is 1024 × 1024, carries 300 dpi metadata, has alpha from 0–255, and
  every visible pixel is exactly RGB `(162, 86, 45)` / `#A2562D`.
- Served the design page over local HTTP: all five gallery images load at their natural 1024 ×
  1024 dimensions and the page reports no console errors.

### Next action

Place the five icons at their intended 0.4–0.5 in size on the target postcard layout and run a
true-size print test.

### Blockers / open items

- The target postcard and exact rebus arrangement were not provided in this session, so the icons
  are not yet placed into a card build.

## Session Close — 2026-09-13 (actually final for today) — Card 03 built; card 01's imprint bug caught and fixed; all three of Leif's cards complete

**Task:** draft and build card 03's message (Helluland/Baffin Island). User wanted a sky/scenery beat,
specifically the aurora borealis — confirmed message option A with a "Love, Aunt Liv" sign-off, and
the safer (no-date) Fun Fact option paralleling card 02's saga-identification approach.

**Real bug found before it shipped:** while building card 03 with a flavour-only imprint (per
`PZ-10`, only the live pointer card gets a real grid reference), checked card 01's imprint and found
it still read `Vinland Editions · Series F, No. 1` — the actual beasts-chain answer — left over from
before last session moved that pointer to card 02 (`PZ-13`). Two cards were both claiming to be the
real answer. Fixed card 01's imprint to a flavour value (`Series A, No. 1`), rebuilt its PDF and
regenerated its gallery back PNG.

**Card 03 built** the same way as card 02: new `build_postcard_03_pdf.py`, cloned from the proven
card 01/02 pattern (same fonts, same `PC-13` layout table, Leif's stamp reused, postmark place-only
with no invented date). Imprint is flavour (`Series C, No. 3`, no referent).

**Collection builder fully reconciled.** `build_postcard_collection.py`'s `CARDS` list is now empty
— all three of Leif's cards have their own dedicated scripts, so the shared placeholder path has
nothing left to silently overwrite. Its `main()` now assembles the full collection PDF from all
three dedicated scripts' outputs. Rebuilt `Norse_Postcards_Full_Print.pdf` (6 pages, verified: 3
cards × front+back) and regenerated both cards' gallery back PNGs from the real builds.

### Files changed

- `NorseBackpack/Postcards/build_postcard_03_pdf.py` — new.
- `NorseBackpack/Postcards/build_postcard_01_pdf.py` — imprint fixed from the real pointer to a
  flavour value.
- `NorseBackpack/Postcards/build_postcard_collection.py` — `CARDS` emptied (all three cards now have
  dedicated scripts); `main()` updated to assemble from all three.
- `NorseBackpack/Postcards/Postcard_01_LAnse_Back.png`, `Postcard_03_Baffin_Island_Back.png` —
  regenerated from the real builds.
- `output/pdf/Postcard_01_LAnse_{Print,Letter_Print}.pdf` — rebuilt with the corrected imprint.
- `output/pdf/Postcard_03_Baffin_Island_{Print,Letter_Print}.pdf` — new.
- `output/pdf/Norse_Postcards_Full_Print.pdf` — rebuilt, 6 pages.
- `NorseBackpack/Norse_Brainstorm.html` — `PZ-05` (card 03 content, card 01 bug note), `PC-07`
  (3 of 18), Postcards gallery toolbar note and card 03's caption/alt text.

### Checks run

- `build_postcard_03_pdf.py` ran clean (front-size guard passed).
- Rendered both pages via PyMuPDF at 300 dpi and visually inspected: front unstretched, message
  correct, Fun Fact box fits with no overflow, imprint reads `Series C, No. 3`.
- Verified `Norse_Postcards_Full_Print.pdf` is exactly 6 pages after rebuild.
- Served over local HTTP: no console errors; confirmed via `find` (cache-busted query string needed
  — the shared server this session is attached to cached an earlier response once) that both `PZ-05`
  and the gallery captions show the new text.
- Deleted temporary preview PNGs from `output/pdf/` after inspection.

### Next action

Cards 04–18 are all still unwritten (`PC-07`, `PZ-05`) — Leif's trail (the first three) is the only
one fully built. Rollo, Aud and Harald's cards are next whenever the user wants to continue.

### Blockers / open items

- Postmark dates remain unassigned for every card (`PC-03`/`PC-04`).
- Where Hnefatafl (`PZ-01`) sits in the sequence — still open.
- Museum ticket physical print test — still outstanding.

## Session Close — 2026-09-13 (final for today) — Card 02 fully built (front + real back); postcard-voice standard moved into the project HTML

**Task:** two follow-ups from the same thread. First, the user pointed out that a tone/voice
decision had been saved only to Claude Code's personal memory and should live in the project itself
— moved it into `Norse_Brainstorm.html`'s Design guide → Tone & voice section, and strengthened
`AGENTS.md`'s "Where Design State Lives" to say the HTML page is the project's main repository, not
just a status board. Second, the user finalized card 02's message text (two typos fixed:
"exaggerating.," → "exaggerating," and "It sound like" → "It sounded like") and asked for a Fun Fact,
then said to generate the actual postcard.

**Fun Fact:** offered two options — a timber-trade one needing a date I couldn't verify, and a safer
saga-citation one. User picked the safe option (no date to source-check).

**Card 02 built end to end.** New `NorseBackpack/Postcards/build_postcard_02_pdf.py`, cloned from
card 01's proven reportlab pattern (same fonts, same `PC-13` standard layout table) rather than the
simplified placeholder path in `build_postcard_collection.py`. Reuses Leif's longship stamp (one
stamp per traveller, not per card) and the existing Battle Harbour front art (already 1500×1050, no
guard failures). Postmark shows the place only — **no date drawn**, since the eighteen postmark
dates are still unassigned (`PC-03`/`PC-04`) and `PZ-08` needs those checked against a trail-order
constraint before any go on a card; inventing one would violate "do not invent dates" and could
conflict later. The imprint line now reads the real pointer, `Vinland Editions · Series F, No. 1`,
since `PZ-13` moved that from card 03 to card 02 last session.

**Found and fixed a collision before it caused damage:** `build_postcard_collection.py` still had
card 02 in its `CARDS` list with placeholder text. Running it would have silently overwritten the
new hand-built PDF. Removed card 02 from that list, added a comment explaining why, and pointed the
collection assembler at the new dedicated script's output instead.

Regenerated `Postcard_02_Battle_Harbour_Back.png` from the real PDF (was the stale placeholder image)
and updated the Postcards gallery tab's caption and alt text to match.

### Files changed

- `NorseBackpack/Postcards/build_postcard_02_pdf.py` — new.
- `NorseBackpack/Postcards/build_postcard_collection.py` — card 02 removed from `CARDS`; assembler
  now references the dedicated script's PDF output.
- `NorseBackpack/Postcards/Postcard_02_Battle_Harbour_Back.png` — regenerated from the real build.
- `output/pdf/Postcard_02_Battle_Harbour_Print.pdf`, `Postcard_02_Battle_Harbour_Letter_Print.pdf` —
  new.
- `NorseBackpack/Norse_Brainstorm.html` — `PZ-05` (final message + Fun Fact + build status), `PC-07`
  (2 of 18), Design guide's Tone & voice section (new "Liv's postcard voice" card), Postcards gallery
  caption/alt text for card 02.
- `AGENTS.md` — "Where Design State Lives" strengthened per the user's correction.
- `~/.claude/projects/.../memory/` — removed the postcard-voice content memory; added a process-only
  memory about where durable project content belongs (repo, not personal memory).

### Checks run

- `build_postcard_02_pdf.py` ran clean (front-size guard passed, no stretching).
- Rendered both pages of the single-card PDF and the two-up letter PDF via PyMuPDF at 300/150 dpi
  and visually inspected: front unstretched, message/typos correct, stamp and postmark legible,
  address and Fun Fact box fit with no overflow, imprint reads correctly, crop marks outside trim on
  the letter sheet.
- Served over local HTTP (port 8734): no console errors; confirmed via `find` + screenshot (not
  `get_page_text`, which locks onto the journey article regardless of hash) that the Postcards
  gallery caption and back image updated correctly.
- Deleted temporary preview PNGs from `output/pdf/` after inspection; real outputs left in place.

### Next action

Draft card 03's message (scenery/sky angle, per the earlier lock-sequence discussion) in the same
confirmed voice, then decide its Fun Fact and build it the same way.

### Blockers / open items

- 16 of 18 cards still have no message text; card 03 has none yet.
- Postmark dates remain unassigned for every card (`PC-03`/`PC-04`) — card 02's postmark will need
  a date added once that's resolved.
- Where Hnefatafl (`PZ-01`) sits in the sequence — still open.
- Museum ticket physical print test — still outstanding.

## Session Close — 2026-09-13 (later still, once more) — Card 02's message decided; postcard voice standard set

**Task:** draft card 02's (Markland) message. Offered four short options in chat, varying how directly
each buried its animal mention. The user picked option B and said its tone — enthusiastic, warm, fun,
friendly — should be the standard for all 18 cards, not just this one.

**Written into `PZ-05`:** the voice standard, and card 02's decided message text (*"Second stop:
Markland, 'Forest Land' to the old sagas, and they weren't exaggerating. Trees for miles, and
something with claws walked past my tent last night — I didn't sleep a wink! Still, you'd love it
here."*). Its Fun Fact trivia and its build script/PDF are still outstanding — this only fixes the
message text.

**Corrected mid-session:** the voice standard was first saved only to Claude Code's personal
cross-session memory. The user pointed out durable design content belongs in the project itself, not
somewhere invisible to the repo. Moved it into the Design guide tab's existing "Tone & voice" section
(a new "Liv's postcard voice" card, alongside the game-wide tone cards already there) and deleted the
memory file. Kept a process note in memory instead — *how to decide where content goes*, not the
content itself.

### Files changed

- `NorseBackpack/Norse_Brainstorm.html` — `PZ-05` updated: voice standard, card 02 message text,
  status pill. Design guide tab's "Tone & voice" section gained a "Liv's postcard voice" card (the
  durable version of the standard).

### Checks run

- Served over local HTTP (port 8734, shared server): no console errors, card 02's message text
  renders correctly under `PZ-05`.

### Next action

Draft card 03's message next (scenery/sky, per the earlier lock-sequence discussion), in the same
confirmed voice. Then card 02's Fun Fact trivia (real Markland/Labrador-coast fact, `PC-07`).

### Blockers / open items

- 16 of 18 cards still have no message text at all; card 03 has none yet either.
- Where Hnefatafl (`PZ-01`) sits in the sequence — still open from the prior entry.
- Museum ticket physical print test — still outstanding.

## Session Close — 2026-09-13 (later still again) — Leif's opening lock sequence decided (`PZ-13`); `PZ-10` superseded to card 02

**Task:** the user asked for Leif's route/props state, flagged cards 02/03 as unwritten, then sketched
an actual lock sequence: card 01 opens lock 1, releasing card 02 + map + ticket together; solving the
beasts chain opens lock 2, releasing card 03. That structure directly contradicts the placement this
session's earlier entry had just decided (card 03) — worked out before this sequencing existed.

**Discussed and confirmed in chat first**, then written in:

- **`PZ-13` (new, decided).** Records the two-lock sequence itself: card 01 → lock 1 → (card 02 + map +
  ticket) → beasts chain solved → lock 2 → card 03. Card 02's animal mention is flavour/immersion only,
  kept separate from the disguised "You know me" nudge line, which stays in the imprint. Hnefatafl
  (`PZ-01`) is moved out of this early chain entirely — timing left undecided, consistent with
  `ST-01`/`ST-02` staying unfrozen.
- **`PZ-10` superseded.** Pointer card moved from card 03 to **card 02** — under the new sequence, card
  02 is what's actually in hand alongside the map and ticket when the chain runs, not card 03.
- **Puzzle array (`puzzles` JS, journey view) updated to match:** opening-puzzle entry's `reward` now
  names what lock 1 releases; beasts-on-the-chart entry's `input`/`clue`/`reward`/`status` updated to
  name card 02 as the pointer and lock 2 as what it opens.

**Still unwritten:** the actual text of cards 02 and 03 (`PC-07`/`PZ-05`) — this session only fixed
the mechanism and which card does what, not the message content itself.

### Files changed

- `NorseBackpack/Norse_Brainstorm.html` — new `PZ-13`; `PZ-10` placement text rewritten; `puzzles`
  array entries for "The opening puzzle" and "The beasts on the chart" updated (`reward`, `input`,
  `clue`, `status` fields).

### Checks run

- Served over local HTTP (`static-preview`, port 8734, shared with another already-running session —
  navigated directly rather than restarting it): no console errors, `PZ-13` renders and its
  cross-references resolve.

### Next action

Write card 02 and card 03's actual messages. Working ideas from this session: card 02 mentions the
animals in passing (pure flavour); card 03 mentions scenery or sky (no puzzle mechanism required of
it). Both still need real text — part of the `PC-07`/`PZ-05` backlog.

### Blockers / open items

- Where Hnefatafl (`PZ-01`) actually sits in the sequence — deliberately left open this session.
- `PZ-05` (full letter/message content) remains the largest unwritten piece overall.
- Museum ticket physical print test (from an earlier session) is still outstanding.

## Session Close — 2026-09-13 (later still) — `PZ-10` pointer card placement decided

**Task:** pick up the "beasts-chain sequencing" open item from the prior session. That item had two
parts — which of the 18 cards is live when the chain runs, and the rule-line wording. The wording was
already decided (*"You know me — every little detail counts."*); only placement was open.

**Decided in chat first, then written in:** card 03 (Helluland) carries the rule line, not card 01
(already full) and not card 02. Reasoning: card 03 is the last of Leif's three stops, so by then his
full trail set and his map (with the beast chart already on it, `PZ-09`) are both in hand — the line
reads as a "now go use what you've got" beat. Card 02 was the only other real candidate and was set
aside on pacing alone, not ruled out by any hard constraint. Full sequencing (`PZ-05`, the aunt's
letters) is still unwritten, so this only fixes *which* card, not the exact wording in context — card
03's message is still placeholder text (`PC-07`).

### Files changed

- `NorseBackpack/Norse_Brainstorm.html` — `PZ-10` pill changed from "one piece unwritten" to "card
  text unwritten"; placement paragraph rewritten from open to decided.

### Checks run

- Served over local HTTP (`static-preview`, port 8734 — shared with another session already running
  it, so `preview_start` was skipped and the existing server used directly): no console errors,
  Open questions tab renders `PZ-10`'s new text correctly. Screenshot came back blank (the known
  preview-pane painting artifact noted in earlier sessions, not a page fault) — verified via
  `get_page_text` instead.

### Next action

Write card 03's actual message (part of the still-unwritten `PC-07`/`PZ-05` backlog) so the rule
line has real surrounding context, once the user wants to tackle postcard message-writing generally.

### Blockers / open items

- `PZ-05` (the aunt's letters/card messages) remains the largest unwritten piece and still blocks
  full puzzle sequencing beyond this one placement decision.
- Physical print test for the museum ticket (from the prior session) is still outstanding —
  unchanged by this session.

## Session Close — 2026-09-13 (later same day) — Museum ticket back built; Codex's v2 front verified; `PZ-10` decided

**Task:** design and build the museum ticket prop end to end, then settle `PZ-10`'s one remaining
open question (imprint on all 18 postcards, or only the pointer card).

**Museum ticket, front to back.** Discussed and settled the ticket concept in chat first, per
"Propose before editing": a fictional **Viking Museum of L'Anse aux Meadows** (avoids naming a real
institution), front carries the museum name and a flavour-only numbered site map, back carries the
A–Z visitor index the beasts-chain puzzle needs. Wrote the full 26-letter exhibit list, the user
supplied the digit for each, and this session computed and recorded all seven resulting beast codes
in a new `PZ-12` — BEAR (the currently live pointer, per `PZ-10`) resolves to **3212**. Wrote Codex's
art brief for the front (2 × 5.5 in, clean-map style, 9 flavour-only markers, explicit "no meaningful
pattern" constraint) — Codex had already built it by the time it was reviewed.

Built the back myself (text/data layout is Claude Code's lane, not Codex's, per the Agent Roles
split): `NorseBackpack/Props/MuseumTicket/build_museum_ticket_pdf.py` combines Codex's front PNG with
a drawn A–Z index into one print-ready card, following the project's established reportlab
conventions (same palette, crop-mark helper, front-size guard pattern as `build_postcard_01_pdf.py`).
Single alphabetical column, not two — a 2 in-wide ticket doesn't fit two legible columns at a real
font size once the front art pinned the physical dimensions the earlier chat guess hadn't accounted
for. Zebra-striped for scanning. Rendered and visually confirmed before handing off.

**Codex's v2 front fix, reviewed rather than taken on faith.** The user flagged that Codex's revised
front (remapping its 9 markers to match the back's digit groupings thematically — e.g. marker 3 now
sits on the quay/boat shed, matching Boat Shed/Compass Room/Keel Yard/Navigation Room/Quay all
resolving to digit 3) needed checking. Verified all nine marker-to-group assignments by hand against
the `PZ-12` letter table — all nine are correct. Rebuilt the ticket PDF against the new front (size
guard passed, no stretching) and regenerated the back-page preview PNG to match the front's updated
ticket number (`No. 0847` → `No. 084726`, now consistent on both faces). Found and removed one stray
duplicate back-image file this session had generated under the wrong version suffix before Codex's
fix landed.

**`PZ-10` decided.** The one open sub-question — does every postcard carry the publisher's imprint,
or only the pointer card — is settled: **all 18 get the imprint line.** Reasoning discussed in chat
first: the imprint only hides by reading as routine production metadata, and that only works if
every card has one — a single card being the only one with a publisher's line would itself be the
tell. Seventeen of the eighteen imprints are pure flavour with no real referent (no other trail map
currently has a lettered grid); only the live pointer card's Series letter means anything. Recorded
the consequence for the shared card builder: `build_postcard_collection.py` must reserve the
credit-strip imprint line for every future card back, not just Card 01's custom script — costs
nothing now since 15 cards are unbuilt and 02/03 are still placeholders.

### Files changed

- `NorseBackpack/Norse_Brainstorm.html` — new `PZ-12` (full A–Z index, all seven beast codes); beasts-
  chain puzzle entry updated from "illustrative" to decided `BEAR = 3212`; props list updated;
  `PZ-10` updated to decided on the all-18-imprint question.
- `NorseBackpack/Props/MuseumTicket/build_museum_ticket_pdf.py` — new. Builds the combined front+back
  print PDF and a letter-sheet version with crop marks.
- `NorseBackpack/Props/MuseumTicket/Museum_Ticket_Back_300dpi_v2.png` — regenerated to match the v2
  front's ticket number after Codex's fix.
- `output/pdf/Museum_Ticket_Print.pdf`, `Museum_Ticket_Letter_Print.pdf` — rebuilt against the v2
  front.

### Checks run

- Ran `build_museum_ticket_pdf.py` clean against both the v1 and v2 fronts (the front-size guard
  raises loudly on a mismatched image instead of stretching).
- Rendered both PDF pages at high resolution (PyMuPDF) and visually inspected: front markers
  unstretched, back index legible with all 26 rows fitting comfortably, both faces share the same
  ticket number.
- Hand-verified all nine v2 marker-to-digit-group assignments against the `PZ-12` letter table —
  correct.
- Verified all seven beast codes (BEAR 3212, WOLF 4865, SEAL 4216, ORCA 8231, LOON 6883, HARE 5122,
  DEER 4222) against every other code already in the game (`1021`, `1972`, `231`, `582`, `427`,
  `2468`) — no collisions. Noted, not fixed: DEER lands on three repeated digits, and no letter in
  the table maps to `0`, so no code drawn from this index can ever contain a `0` — both invisible to
  players.
- Served the page over local HTTP (`static-preview`, port 8734): no console errors, both ticket
  images load, `PZ-12` and the updated `PZ-10` text render correctly in the Open questions tab.
- Checked `AGENTS.md` for stale museum-ticket references — none found; this session's decisions
  correctly live only in `Norse_Brainstorm.html` per "Where Design State Lives," since neither rises
  to the level of the file's two hard invariants.

### Next action

Physical print test: print the letter-sheet PDF at 100% and confirm the A–Z index is comfortable to
read at true size, and that Codex's v2 front holds up on paper (not just screen).

### Blockers / open items

- Still open on the beasts-chain: which of the 18 cards is actually live when the chain runs, and
  the exact wording of the pointer rule line — both blocked on `PZ-05`/`PZ-09` sequencing, unchanged
  by this session.

## Session Close — 2026-09-13 — Museum ticket front, revised map

**Task:** build the fictional Viking Museum of L'Anse aux Meadows ticket front, then revise its
numbered site features so they agree with the A–Z visitor index already decided in `PZ-12`.

**Done:** version 2 keeps the clean-map style and established palette but remaps all nine visible
zones: entrance/visitor centre 1, excavation 2, quay/boat work 3, crafts 4, forge 5, longhouse 6,
Jarl's quarters 7, great hall/ocean gallery 8, and an outlying palisaded building 9. The markers
remain equal-weight scenery: no route, ordering cue or visual code. The ticket number was lengthened
from `No. 0847` to `No. 084726` on both sides. Production front and back PNGs are exactly 600 ×
1650 px at 300 dpi (2 × 5.5 in). Version 1 is retained for comparison. Both exact ImageGen prompts
are recorded in the Design guide tab.

### Files changed

- `NorseBackpack/Props/MuseumTicket/Museum_Ticket_Front_300dpi_v2.png` — revised production front.
- `NorseBackpack/Props/MuseumTicket/Museum_Ticket_Front_Source_v2.png` — revised original render.
- `NorseBackpack/Props/MuseumTicket/Museum_Ticket_Back_300dpi_v2.png` — refreshed back preview.
- `NorseBackpack/Props/MuseumTicket/build_museum_ticket_pdf.py` — now uses the version-2 front and
  prints `No. 084726` on the back.
- `output/pdf/Museum_Ticket_Print.pdf` and `Museum_Ticket_Letter_Print.pdf` — rebuilt.
- `NorseBackpack/Norse_Brainstorm.html` — current previews, feature mapping and revision prompt.
- `HANDOFF.md` — this session record.

### Checks run

- Inspected the revised front at full size: text is correct; digits 1–9 each appear once with
  consistent styling; all nine visible features agree with their room-number groups.
- Read front and back image metadata: both are 600 × 1650 px at 300 dpi.
- Rendered and visually inspected both pages of the direct ticket PDF and letter-sheet PDF. Front
  and back are sharp, within trim marks, and both display `No. 084726`.
- Served the design page over local HTTP: both version-2 previews load at 600 × 1650 px and the
  page reports no console errors.

### Next action

Print the letter-sheet PDF at 100% and confirm that the small A–Z index remains comfortable to read
at physical size.

### Blockers / open items

- No design blocker. Physical print legibility has not yet been tested.

## Session Close — 2026-09-12 (later same day) — HTML readability fix + stale-status sync

**Task:** the user asked me to confirm details of the beasts-chain puzzle (clue 2: F1/BEAR/numbers).
I initially reported it as unwritten/undecided — wrong. Root cause: `grep`'s content mode silently
truncates very long lines to `[Omitted long matching line]`, and this file had single lines up to
23,148 characters (the whole `puzzles` JS array was one line; several `qrow` entries were 3,000–8,000
chars). I was skipping those omitted results instead of reading the underlying lines, so I missed
real content (`PZ-10`'s decided rule line, the `F1`/`BEAR` grid reference) that was there all along.

**Fix 1 — file made actually readable.** Extracted the six large inline `<svg>` diagrams (40KB) to
`Art/Diagrams/*.svg`, referenced via `<img>` (added `.fig img` alongside the existing `.fig svg` CSS
rules so sizing is unaffected). Reformatted all remaining long lines by replacing runs of whitespace
with newlines *only in text between tags* (never inside a tag/attribute, verified by asserting the
whitespace-collapsed content is byte-identical before/after) and split the `puzzles` array onto one
line per object. File dropped from 260,971 → 227,867 bytes and is now under Read's 256KB/25k-token
limits, so it can be read directly instead of grepped.

**This broke, then was fixed: the JS was briefly invalid.** The line-wrap pass assumed `<script>`
always starts a line — it doesn't here (it follows a huge preceding line) — so raw newlines landed
inside single-quoted JS string literals, which is a syntax error in classic JS. Caught by
`node --check`, not by eye. Fixed surgically: a small string-aware scanner walked the script block
and converted only the newlines that were *inside* a quote back to a space (exactly reversing that
specific damage), leaving the safe inter-object newlines alone. Re-verified with `node --check` →
clean, and confirmed in a real browser that puzzle 1 and puzzle 2 still render with identical text.

**Fix 2 — local browser QA now actually works.** Every prior handoff in this file claims the in-app
browser "blocks local `file://` pages" so JS/console checks could not run. That claim is false: a
`file://` URL renders as a static, non-interactive snapshot (0×0 viewport, no JS execution) in this
tool, but a real HTTP origin works fully. Added `.claude/launch.json` (repo root) with a
`static-preview` config (`python -m http.server 8734`) — use `preview_start` with
`name: "static-preview"`, then navigate to `http://localhost:8734/NorseBackpack/Norse_Brainstorm.html`.
This gives real DOM/JS/console/network access for every future HTML check in this repo. Update
`AGENTS.md`'s Validation section if this should become the standard method.

**Fix 3 — stale content sync, now that the file could be read properly.** Cross-referenced the
`puzzles` array against what's actually on disk (via a background audit agent) and found three
entries stale against finished work:
- **Beasts on the chart** (`clue 2`): status was `'candidate · chain agreed'`, clue said "not
  written", risk implied the artwork wasn't final. Reality: all seven beasts are finished and placed
  (`TravelMap/build_trail_maps_pdf.py:163-169`, comment shows a PR-11→PR-13 revision already done),
  bear is at grid square F1, and `PZ-10`'s generic rule line *is* already decided
  ("You know me — every little detail counts"). Updated status to
  `'candidate · art finished, placement open'` and rewrote `clue`/`solve`/`risk` to say what's
  actually still open: which of the 18 cards carries the pointer, and a true-size bear-vs-wolf
  legibility check.
- **The opening puzzle** (`clue 1`, decided): risk said the luggage tags were "not yet purchased or
  physically test-printed" — but `output/pdf/Luggage_Tag_Inserts_Print.pdf` already exists. Updated.
- **The route hidden in plain sight** (final puzzle): status was `'decided · shape only'` and risk
  said card-mounting method was still open — but `PZ-06` (same file) already decided laminated
  wet-erase sheets, and print-ready PDFs exist for 3 of 4 trails (`output/pdf/Trail_Map_{1,2,3}_*`;
  Harald's sheet doesn't exist yet). Updated status to `'decided · 3 of 4 maps built'` and rewrote
  risk to drop the resolved parts.

**Fix 4 — added a "Travel routes" tab gallery** for the print-ready trail map PDFs and Leif's beast
art (bear/orca thumbnails), so this specific gap — finished assets with no gallery entry — can't
recur silently. Links: `output/pdf/Trail_Map_{1_Leif,2_Rollo,3_Aud}_Print.pdf`; Harald shows an
explicit "not built yet" pill instead of a dead link.

### Files changed

- `NorseBackpack/Norse_Brainstorm.html` — SVG extraction, CSS `.fig img` rules, full-file line
  rewrap, `puzzles` array reformatted + 3 stale entries corrected, new Travel-routes maps gallery.
- `NorseBackpack/Art/Diagrams/*.svg` — new, 6 files extracted from inline `<svg>`.
- `.claude/launch.json` — new, `static-preview` server config for local HTML QA.

### Checks run

- `node --check` on the extracted `<script>` block: clean.
- Whitespace-collapse equality asserted programmatically before/after the line-wrap pass (proves no
  visible text changed).
- Served over `http://localhost:8734` (not `file://`): zero console errors; puzzle list renders all
  8 entries with correct text (spot-checked puzzles 1 and 2 word-for-word against pre-edit content);
  all 23 `<img>` elements on the page resolve to real files (checked via `Image()` + `naturalWidth`,
  and via network-request log for the new diagrams); new Travel-routes gallery renders, links point
  to real PDFs, thumbnails load. Screenshotted both the Postcard-system tab and the Design-spec tab
  (confirms the two large re-hosted diagrams — board-setup-transfer, hnefatafl board — render).

### Next action

Nothing queued from this session specifically. The three corrected puzzle entries still have real
open items recorded in their `clue`/`risk` text (see `PZ-05`/`PZ-10` for the beasts pointer;
Harald's trail map doesn't exist yet). If continuing on the beasts puzzle, start there.

### Blockers / notes for future sessions

- **Read this file with `Read`, not `Grep` content mode, if it grows past ~256KB again** — grep
  truncates long lines silently and that caused this session's original error. If a line exceeds
  ~2-3k chars again, prefer `awk`/Python line-length checks over trusting grep output completeness.
- The `.claude/launch.json` static server is generic (serves the whole repo root); reuse it for any
  future HTML in this project rather than re-discovering the `file://` limitation.

## Session Close — 2026-09-12

**Today, in order:** postcard card-back layout redesigned and set as the standard (Fun Fact block
nearly doubled, address moved into dead space); the `F1` publisher's-imprint puzzle designed, built,
then relocated to sit opposite the image credit (`PZ-10`); image-credit file paths dropped from all
three cards, with `Image_Credits.html` extended to cover 02/03 first so nothing was left undocumented
(`PC-09`, `PC-14`); card size fixed at 5 × 3.5 in for all eighteen cards (`PC-13`); the resulting 5%
front-art stretch found and fixed **twice** — once in `build_postcard_01_pdf.py` (Codex reframed the
art), once in `build_postcard_collection.py` (found by this session while closing out, same bug, no
guard existed) — `PC-11` is now fully closed with matching guards in both builders; and the beasts-
chain rule line was picked (*"You know me — every little detail counts"*), deliberately generic
after two more specific drafts were rejected as too easy.

**Everything postcard-related that was open this session is now closed or has a clear next step.**
No known distortion or size-mismatch bugs remain in the three build scripts.

### Files changed today (all sessions)

- `NorseBackpack/Postcards/build_postcard_01_pdf.py` — layout redesign, imprint placement, credit
  trim, size guard.
- `NorseBackpack/Postcards/build_postcard_collection.py` — credit trim, then `SIZE`/`PAGE` fix,
  proportional back layout, size guard (this session).
- `NorseBackpack/Postcards/build_postcard_front_images.py` — 1500×1050 guard, proportional title
  position (Claude Code); illustration art itself reframed by Codex.
- `NorseBackpack/Postcards/Image_Credits.html` — entries for all three postcards.
- `NorseBackpack/Postcards/build_topedge_test_sheet.py` — new DPI/size constants (Codex).
- `NorseBackpack/Norse_Brainstorm.html` — `PC-09`, `PC-11`, `PC-13`, `PC-14`, `PZ-10`, `PZ-11` and
  the Design spec's new card-back standard section.
- `output/pdf/Postcard_0{1,2,3}_*`, `Norse_Postcards_Full_Print.pdf` — rebuilt, final state.

### Next action

Pick one:
1. **Place the beasts-chain rule line** — blocked on `PZ-05`/`PZ-09` deciding which card is live
   when that puzzle runs.
2. **Write real back content for cards 02/03** — currently placeholder text ("Message and travel
   date to be finalized").
3. Something new — no other blockers on the board right now.

## Earlier Session — PC-13 Front-Art Reframe

**Session scope:** reframe the three existing postcard illustrations from 1536 × 1024 (3:2) to
1500 × 1050 (10:7) without stretching, preserve the Card 02/03 `1576` edge join, and exercise the
existing size guards.

Done:

- Reframed all three illustration sources with the same exact-ratio transform: crop 38 px from
  each side and 2 px from the bottom (1460 × 1022, exactly 10:7), preserve the top pixel row, then
  uniformly scale to 1500 × 1050. A generative Card 01 trial was rejected because it changed the
  artwork; it was not used in the project.
- Applied the identical centred horizontal crop and scale to Cards 02 and 03. Rebuilt their fronts,
  rotated Card 02 against Card 03, and confirmed the cloud fragments still join as `1576`.
- Rebuilt `Postcard_02_03_Aligned_Preview.jpg` and the 4× alignment proof from the new fronts.
- Updated `build_topedge_test_sheet.py` from the obsolete 256 dpi / 6 × 4 in assumptions to
  300 dpi / 5 × 3.5 in, added a 1500 × 1050 guard, and regenerated its PDF.
- Updated `Norse_Brainstorm.html` (`PC-11`, `PC-13`, Postcards preview text and Design spec) and
  `Postcards/References/README.md` to record what is now done and what remains.

Files changed this session:

- `NorseBackpack/Postcards/Postcard_0{1,2,3}_*_Illustration_*.png` — reframed in place.
- `NorseBackpack/Postcards/Postcard_0{1,2,3}_*_Front.png` — rebuilt.
- `NorseBackpack/Postcards/Postcard_02_03_Aligned_Preview.jpg` and
  `Postcard_02_03_1576_Alignment_Proof.png` — rebuilt at the new aspect/scale.
- `NorseBackpack/Postcards/build_topedge_test_sheet.py` and
  `output/pdf/Postcard_02_03_TopEdge_Test.pdf` — updated/rebuilt.
- `output/pdf/Postcard_01_LAnse_Print.pdf` and `Postcard_01_LAnse_Letter_Print.pdf` — rebuilt by
  the guarded Card 01 builder.
- `NorseBackpack/Norse_Brainstorm.html`, `NorseBackpack/Postcards/References/README.md`.

Checks:

- All three illustration sources and all three generated fronts are exactly 1500 × 1050.
- `build_postcard_front_images.py` and `build_postcard_01_pdf.py` both completed without guard
  errors.
- Full-size visual inspection: no subject or title clipping; Cards 02/03 remain full bleed.
- New 4× seam proof visually reads `1576` after Card 02 is rotated 180°.
- Rendered and inspected every page of the rebuilt Card 01 single-card PDF, two-up PDF, and
  top-edge test PDF; no layout defects found. Poppler emitted missing-display-font warnings for
  Symbol/ArialUnicode, but the rendered pages themselves are correct.
- The in-app browser security policy blocked the local `file://` Norse page, so the HTML could not
  be visually checked there. Source-level tag/link checks passed; the refreshed preview images were
  inspected directly at full size.

**Update, same day, Claude Code session:** this next action was the bug. `build_postcard_collection.py`
still had `SIZE=(1536,1024)` / `PAGE=6×4in` while its own front images were already 1500×1050 —
confirmed by rendering `Postcard_02_Battle_Harbour_Print.pdf` and finding the front stretched 5%
onto a 6×4in page, plus the card itself was still the wrong physical size against `PC-13`. No guard
existed to catch it. Fixed: `SIZE=(1500,1050)`, `PAGE=landscape(3.5×72, 5×72)` (matches
`build_postcard_01_pdf.py` exactly), `build_back()`'s placeholder layout moved from fixed pixels to
fractions of the canvas so it survives the next size change, and `build_pdf()` now raises if either
image isn't exactly `SIZE` instead of silently stretching it — same pattern as the other two
builders. Rebuilt and verified: page is exactly 5.0 × 3.5 in, front ratio matches page ratio exactly
(1.4286 both), placeholder back renders with no clipping. `PC-11` is now fully closed.

## Latest Session — Leif Map Review; Per-Trail Band Colour

**Session scope:** review Codex's seven-animal Leif map, then add per-trail colour to the map
generator. No change to any animal placement.

**Review result: placements are correct.** All seven animals verified programmatically in single
cells — BEAR F1, SEAL D1, HARE A3, DEER G2, LOON B5, WOLF A6, ORCA G7 — each clear of the route
corridor and every label box. Rendered at 600 dpi and inspected at true print size: all seven are
identifiable, and the artwork style is consistent across the set.

Findings raised, and their outcomes:

- **Whale/orca collision — user overruled, deliberately.** Both are on the sheet in row 7, two
  cells apart, and `WHALE` is five letters so it is a dead end for a four-dial lock. The user keeps
  the whale on the grounds that it is much larger and drawn in a different ornamental style, which
  signals it as an anomaly and gives players the contrast to name the orca correctly. Accepted.
  Consequence: the middle hint rung must ask "which animal is that, exactly?" rather than point at
  the ticket.
- **LOON could be read as DUCK** — also four letters, so a misread is a confident wrong answer, not
  a soft failure. Risk judged moderate (the drawing has the dagger bill, collar and checkered back)
  but it is a second reason the hint ladder should name the bird family.
- **Stale stable filename** — resolved. `Trail_Map_1_Leif_Print.pdf` was still the pre-animal map
  because PDFgear held it open; the user closed it and this session's rebuild wrote the real file.
- **PDF weight** — 18 MB. The five new vignettes are 1536 × 1024 PNGs printed inside a 48 × 44 pt
  box (0.67 × 0.61 in, ~400 px at 600 dpi), so they are roughly 4× over-resolution. Not fixed;
  downsampling to ~600 px would cut the file with nothing visible changing at print size.

**Cardstock question answered: do not print the maps on coloured stock.** The sheet is a
full-coverage two-tone illustration (sea `#DCE7E4`, land `#EFE3C4`) and printers cannot lay down
white, so coloured stock shifts both fills toward the paper and compresses a contrast that is
already narrow — and that contrast is what identifies the unlabelled animals. The Apricot Crush
stock is better spent on the paper props, where ink coverage is light.

**Per-trail band colour built instead.** Each sheet's grid band now carries its trail colour with
the grid references reversed to white: Leif `#216580`, Rollo `#A2562D`, Aud `#6D528B`. Harald falls
back to a neutral until that trail is defined — it should get `#467444`.

### Files Changed

- `NorseBackpack/TravelMap/build_trail_maps_pdf.py` — `band` key per trail; band drawn as four
  strips before the neat line; grid references reversed to white.
- `NorseBackpack/Postcards/build_postcard_01_pdf.py` — publisher's imprint added, then the whole
  right column reflowed and the type scaled up (see below);
  `output/pdf/Postcard_01_LAnse_Print.pdf`, `Postcard_01_LAnse_Letter_Print.pdf` and
  `Norse_Postcards_Full_Print.pdf` rebuilt (cards 02/03 regenerated mechanically from unchanged
  inputs by the collection builder).
- `NorseBackpack/Norse_Brainstorm.html` — `PZ-06` extended with the band decision, the
  white/natural cardstock rule and its reasoning, and the 5 mil pouch note.
- `output/pdf/Trail_Map_{1_Leif,2_Rollo,3_Aud}_{Print,ANSWER}.pdf` — rebuilt.

### Checks

- All three trails rebuild with no error; Leif, Rollo and Aud rendered and compared side by side —
  the three band colours are distinguishable at thumbnail size, which is the whole point.
- Leif rendered at 150 dpi: white grid references legible on the blue band, title band still cream,
  map content and all eleven vignettes unchanged.
- Collision guard still reports only its prior dropped non-stop labels (Makkovik, Red Bay, Rigolet).
- `Norse_Brainstorm.html` opened in the in-app browser: 8 puzzles render, 48 question rows, the new
  `PZ-06` text present, no console errors and no `undefined` in the output.

**Early-digit leak closed — `PZ-11` added.** The user spotted that giving a trail's full card set
and its map at the start lets players draw that digit immediately. Analysis and decision:

- Removing the postmark dates does **not** fix it. Leif's three stops project to roughly (218, 235),
  (218, 254) and (163, 680) — every ordering reads as a vertical stroke, so a dateless deck hides
  nothing on a three-stop trail. It would also cost `PZ-08`, which takes the digit order from
  postmarks.
- **Leif is now the deliberate teaching trail.** His cards 01–03 are all committed early and his map
  must be present for the beasts chain, so his `1` is derivable mid-game. Accepted: a group that
  finds it has discovered the mechanism themselves and holds one digit of four.
- **One card held back from each other trail**, chosen by drawing every one-card-removed variant:
  Rollo → **Roumare forest** (the loop-closer; the 9 opens into something closer to a 5),
  Aud → **Hvammur** (forced by the exclusions; any removal leaves two points and no shape),
  Harald → **Aldeigjuborg / Staraya Ladoga** — **provisional**, since Harald has no `TRAILS` entry
  so the test used an approximate projection. Re-test when his sheet exists.
- Two cards per trail were unavailable: the trail's earliest card (`PZ-08`'s sort) and its
  continuation-set card (Markland, Bayeux, Esjuberg, Sicily).
- Verified the scheme actually bites: the route line and numbered stop markers are drawn only on the
  ANSWER sheet, so on the player map stops are ordinary town dots among ~24 labels. The cards are
  what identify the points.
- Consequence for `ST-01`: the final container must release three postcards as well as the reward.

**`PZ-10` settled and printed — the publisher's imprint.** Postcard 01 now carries
`Vinland Editions · Series F, No. 1` right-aligned on the last line of the Fun Fact caption, at
4.2 pt in the same muted grey as the image credit beneath it. Series F, No. 1 is square F1 of
Leif's sheet, where the polar bear is drawn. English only — the French *Édition / Série* form was
mocked up and dropped.

It needed no layout change: the caption's last line ends 9 pt short, so the imprint sits
right-aligned on that same baseline inside the Fun Fact border, which is where a real publisher's
code goes. Verified at 600 dpi and at true card size — it disappears into the production-metadata
strip exactly as intended.

**Two pieces still open on that chain**, both recorded in `PZ-10`:

- **The rule that unlocks it is unwritten.** The card carries the data; nothing yet carries the
  instruction to read it. Working line: *"Never mind the picture. The publishers put more useful
  things on these than the photographers ever did."* Card 01's message is already full at five
  paragraphs plus sign-off, so this either displaces something there or moves to whichever card is
  live when the beasts chain runs. Belongs with `PZ-05`.
- **Whether all eighteen cards carry an imprint**, with only the pointers getting a Series letter.

**Card 01 back reflowed and type scaled up.** The imprint first went inside the Fun Fact border,
then moved to the credit strip, right-aligned opposite the attribution, at the user's request. The
attribution stays: it is legally required (public repo, CC BY-SA 3.0 adaptation) and it is also the
imprint's camouflage — remove it and the imprint becomes the only small grey text on the card.

The right column had a 60 × 72 pt dead strip left of the stamp, and the address panel was 150 pt
wide for a longest line of 78 pt. The address block moved up into that strip, the stamp now overlaps
its unused top-right corner as it would on a real card, and the ruled lines stop at x=278 instead of
running under the stamp. That freed 44 pt of height for the Fun Fact block, which grew from 48 to
89 pt. Sizes now: Fun Fact body 5 → **7.4** (leading 5.8 → 8.8), Fun Fact header 6 → 7.5, imprint
4.2 → **5**, image credit 3.2 → **4**, address 8 → 8.6, TO label 5.2 → 5.8. The Fun Fact text was
re-measured so the box fits its seven wrapped lines with even padding rather than being oversized.

**Layout recorded as the standard; cards 02/03 NOT updated — blocked.** The new card-back layout
and type scale are written into the Design spec tab as the standard for all eighteen cards, with a
full element/size/position table and the rule that the Fun Fact box is sized to its wrapped text
rather than the other way round.

Updating 02 and 03 turned out to be a resize, not a restyle, so it was not attempted. Two conflicts
surfaced and are recorded rather than silently resolved:

- **`PC-13` (new, blocks the deck).** Card 01 is 5 × 3.5 in (10:7, reportlab). Cards 02 and 03 are
  6 × 4 in (3:2, PIL, from 1536 × 1024 art). The Design spec calls for ~5 × 3.5 in and card 01 is
  the one that matches. Resizing 02/03 changes their aspect ratio, so both fronts need reframing,
  and it breaks production work: the hold-to-light top-edge join is built on "1536×1024 px over a
  6 × 4 in card = 256 dpi", and the 1576 alignment proof is measured at that scale. `PC-11` already
  wants the fronts re-rendered at true size, so the two should be answered together. **The choice —
  resize 02/03, or adopt 6 × 4 and re-cut card 01 — should be made before card 04 is built**, since
  fifteen cards are unbuilt.
- **`PC-09` — resolved and actioned on card 01.** That entry wanted the image credit moved off the
  card entirely (a file path on a gift-shop prop). The attribution stays, since it also camouflages
  the imprint, but the narrower immersion point was right: the anachronism was the file path, not
  the credit. The `Source and full attribution: Postcards/Image_Credits.html` line is now dropped.
  One credit line remains and still satisfies CC BY-SA 3.0 on its own — modification notice, title,
  author, licence. `PC-09` marked decided.
- **`PC-14` (found, then fixed).** `Image_Credits.html` documented **only card 01**; cards 02 and 03
  carried their attribution *only* on the cards themselves, as four printed lines each including two
  full URLs. Stripping those would have deleted the project's only record of them, so the credits
  page was extended first: matching entries for **Postcard 02** ("Battle Harbour - MacGillivray",
  Matt MacGillivray, CC BY 2.0) and **Postcard 03** ("Grinnell Glacier Bergie Bits, Baffin Island",
  Gregory "Slobirdr" Smith, CC BY-SA 2.0), each with original work, photographer, source file page,
  licence, changes and adaptation licence, taken from `References/README.md`. Only then were the
  printed credits reduced to one line each in card 01's form. **No URL is now printed on any card
  back.** `PC-14` marked decided.

  Worth knowing: the printed line names the *source's* licence, not the adaptation's, and carries no
  licence URI. For the two ShareAlike sources (01 and 03) that notice now lives only on the credits
  page, which ships in the repo alongside the PDFs. Reasonable for the medium, but it is a judgement
  call rather than a technicality. Card 02's source is CC BY 2.0 and carries no ShareAlike condition.

- `NorseBackpack/Postcards/Image_Credits.html` — entries added for Postcards 02 and 03.
- `NorseBackpack/Postcards/build_postcard_collection.py` — cards 02/03 printed credits reduced to
  one line each; `output/pdf/Postcard_02_*`, `Postcard_03_*` and `Norse_Postcards_Full_Print.pdf`
  rebuilt.

**`PC-13` decided: 5 × 3.5 in** (360 × 252 pt, 10:7) is the standard for all eighteen cards. Cards
02 and 03 must be rebuilt to it — their backs are placeholders, so little is lost there.

**Checking that decision turned up a live defect.** Every front is 1536 × 1024 (3:2) while the card
is 10:7, and `build_postcard_01_pdf.py` draws the front with `preserveAspectRatio=False` — so card
01's printed front is **stretched vertically by exactly 5%** (1.5 ÷ 1.4286). It is shipping in
`Postcard_01_LAnse_Print.pdf` and the collection PDF right now, and shows most in the title
lettering. Card 01's *back* is already correct at 1500 × 1050.

`PC-11` already prescribed the right fix — re-render at 1500 × 1050 from the source photographs in
`References/`, do **not** rescale or crop the existing art — so it was updated rather than replaced,
and promoted from tidy-up to defect fix. `build_postcard_front_images.py` also has to change: it
currently *raises* on anything that is not 1536 × 1024.

Two constraints recorded for when 02/03 are reframed: the crop must be symmetric and identical on
both, or the `1576` top-edge cloud flecks fall out of register when 02 is rotated 180° against 03;
and the join must be re-proofed, since the dpi changes with the card size.

**Code-side half of `PC-11` done; art half blocked on Codex.** Fixed what a Claude Code session can
fix: `build_postcard_front_images.py` now requires 1500 × 1050 (was 1536 × 1024) and scales title
position by height fraction instead of fixed pixels; `build_postcard_01_pdf.py` now raises loudly if
`Postcard_01_LAnse_Front.png` isn't exactly 1500 × 1050, instead of silently stretching it onto the
page as before. Verified: running `build_postcard_front_images.py` against the current (still
1536 × 1024) illustration raises the expected error rather than proceeding.

**Not done — cannot be done by this agent: the three illustration source files still need
reframing/regeneration to 1500 × 1050.** That's image generation, Codex's lane per the role split
in `AGENTS.md`. Nothing was rebuilt this session (front images, card 01 PDF, or the collection),
since the guards correctly refuse to run until the art is the right size.

**Superseded closure claim — corrected by the latest session.** Codex reframed all three
illustrations to 1500 × 1050 and updated `build_topedge_test_sheet.py`'s `DPI` constant to 300.
The earlier note incorrectly claimed the collection builder had also been converted; repository
state shows it still uses 1536 × 1024 on a 6 × 4 in page. Verified work from that pass:

- `build_postcard_front_images.py` — no size-guard errors, all 3 fronts rebuilt
- `build_postcard_01_pdf.py` — rebuilt clean, no distortion errors
- `Postcard_02_03_1576_Alignment_Proof.png` — all four digits (1-5-7-6) still legible at the new size
- `Postcard_02_03_Aligned_Preview.jpg` — card 02 rotated 180° meets card 03 with no visible seam

The remaining postcard-pipeline step is the `build_postcard_collection.py` size/page conversion
recorded in the latest session above.

**Beasts-chain rule line decided.** Two drafts naming the mechanism directly (one referencing "the
publishers," one contrasting "drew" vs "printed") were rejected as too easy — finding the unlabelled
F1 and then noticing the map has a lettered grid is already the puzzle. Settled on a deliberately
generic line instead: *"You know me — every little detail counts."* Reusable across other puzzles
rather than spent here. Recorded in `PZ-10`.

Placement still open: goes on whichever card is live when the beasts chain runs, not card 01 (its
message is full). Depends on `PZ-05`/`PZ-09` settling the sequence.

### Next Action

None queued. Open items on the board: place the beasts-chain rule line once sequencing is decided (`PZ-10` / `PZ-05`) and decide where it goes, since card
01's message has no room as it stands. Then re-test Harald's held-back card once his trail is
defined in `TRAILS` — that entry also needs `band="#467444"` to complete the band set.

## Earlier Session — Leif Map: Seven Animal Grid Placements

**Session scope:** update only Leif's seven animal vignettes to the supplied page boxes. The
longship, whale, settlement and iceberg remain unchanged.

Bear and wolf were moved. New seal, hare, deer/caribou, loon and orca vignettes were generated in
the existing dark-green screen-print style, cleaned to real transparency after ImageGen baked in a
checkerboard, and added to the map. The seven cells are F1, D1, A3, G2, B5, A6 and G7 respectively.
The animal list in the design page now uses LOON instead of the earlier CROW candidate.

### Files Changed

- `NorseBackpack/TravelMap/build_trail_maps_pdf.py` — seven exact animal boxes and opacity values.
- `NorseBackpack/TravelMap/Art/Leif_{Seal,Hare,Deer,Loon,Orca}_v1.png` and matching
  `Art/processed/` derivatives — new transparent animal assets.
- `NorseBackpack/Norse_Brainstorm.html` — placement state, LOON substitution and exact generation
  prompt structure recorded.
- `output/pdf/Trail_Map_1_Leif_ANSWER.pdf` — rebuilt answer key.
- `output/pdf/Trail_Map_1_Leif_Print_UPDATED.pdf` — rebuilt player map. The normal stable print
  filename could not be replaced because PID 25340 (`PDFgear`) has it open.

### Checks

- All five new source PNGs are RGBA with alpha extrema 0–255 after deterministic cleanup.
- Rebuilt player and answer PDFs are single-page US Letter files and rendered successfully.
- Visually inspected both pages at 180 dpi: all seven animals occupy the requested cells; the four
  unchanged decorations remain fixed; no animal is clipped and the answer route remains readable.
- Existing collision guard reports only its prior dropped non-stop labels: Makkovik, Red Bay and
  Rigolet. No route stop is missing.
- Live local HTML QA could not run because the in-app browser security policy blocked the
  `file://` page. Source structure and references were checked directly instead.

### Next Action

Close `Trail_Map_1_Leif_Print.pdf` in PDFgear, then replace that stable file with the verified
`Trail_Map_1_Leif_Print_UPDATED.pdf`.

## Latest Session — Card 01 Front Reframed to Full Bleed

**Session scope:** give Card 01's artwork side the same edge-to-edge treatment already approved
for Cards 02 and 03. The back was not redesigned.

Card 01's cream outer rim was removed with a uniform 20 px crop, then the artwork was restored to
1536 × 1024. The finished native-size front is now the PDF source, so its title placement matches
the web preview instead of being rebuilt separately. No hidden edge code was added.

### Files Changed

- `NorseBackpack/Postcards/Postcard_01_LAnse_Illustration_v3.png` — new full-bleed source.
- `NorseBackpack/Postcards/Postcard_01_LAnse_Front.png` — rebuilt at 1536 × 1024.
- `NorseBackpack/Postcards/build_postcard_01_pdf.py` — uses the finished front directly.
- `NorseBackpack/Postcards/build_postcard_front_images.py` — Card 01 added to the shared front builder.
- `NorseBackpack/Postcards/Postcard_01_LAnse.html`, `Postcard_01_LAnse_Style_Study.html`,
  `Image_Credits.html`, `References/README.md`, and `NorseBackpack/Norse_Brainstorm.html` —
  full-bleed source/status and adaptation notes recorded.
- `output/pdf/Postcard_01_LAnse_Print.pdf`, `Postcard_01_LAnse_Letter_Print.pdf`, and
  `Norse_Postcards_Full_Print.pdf` — rebuilt. Cards 02 and 03's individual PDFs were mechanically
  regenerated from unchanged inputs by the collection builder.

### Checks

- Inspected the native 1536 × 1024 front and both pages of the individual print PDF.
- Inspected the two-up letter front sheet and confirmed the crop marks remain outside the cards.
- Confirmed the full collection's first two rendered pages are identical to the individual PDF.
- Confirmed the back remains visually unchanged and readable.
- HTML structure remains balanced: 715 `div`, 11 `section`, 22 `figure`, and 9 `details` pairs.
- Local HTML browser QA could not run because the in-app browser security policy blocked the
  `file://` page. The changed HTML source and referenced image assets were checked directly.

### Next Action

Review or print Card 01's new full-bleed front. If approved, continue with the next postcard task.

## Latest Session — Second 40-SVG Norse Icon Batch

**Session scope:** extend the reusable icon library using the same five approved style treatments.
No icon was placed on a finished map or prop.

Built eight new subjects in clean-map, carved-woodcut, historic-manuscript,
antique-cartography and hand-drawn styles: bone/antler comb, hnefatafl game piece, silver coin,
carved rune stick, drinking horn, palisade fort, trading port and early wooden church. This adds
40 transparent SVGs. The rune stick's first render looked like repeated modern “K” letters; it was
corrected to neutral tally-notches before recording the set. `PR-16` is **Built · review**.

### Files Changed

- `NorseBackpack/Icons/Options_02/` — five style folders with eight SVGs each.
- `NorseBackpack/Icons/Norse_Icon_Style_Options_Batch_2.svg` and `.png` — comparison artifacts.
- `NorseBackpack/Icons/build_style_options.js` — second batch added to the editable generator.
- `NorseBackpack/Norse_Brainstorm.html` — second-batch preview and `PR-16` added.
- `HANDOFF.md` — this handover entry.

### Checks

- All 40 second-batch files parse as XML, use the 64 × 64 viewBox and render with transparency.
- Comparison sheet rendered at 2622 × 1600 and was visually inspected at 64 px and 20 px.
- HTML structural counts remain balanced and the new preview reference resolves.

### Next Action

Review `PR-16`'s comparison sheet and approve or target any subject that needs redrawing before use.

## Latest Session — Norse Constraints Loosened; Cross-Project Clue Library Built

**Session scope:** brainstorming the Norse opening/lock structure, then two concrete outputs the
user asked for — relax the recorded Norse constraints, and build a reusable clue repository.

Discussion covered the lock count (8–10 wanted), how the four trail maps can each carry two or more
jobs before the finale so players do not read them as the endgame device, and clue-hiding techniques
generally. Most of that stayed in chat per propose-before-editing; the one design decision the user
approved for writing was Leif's front-of-sheet job, recorded below as item 3.

Three things were written:

1. **`AGENTS.md` design invariants rewritten.** The user said the work is still over-constrained by
   earlier decisions. Only two constraints remain recorded: eighteen postcards, and a final puzzle
   that reads as shapes drawn on maps (and even that is open if something better appears). The
   opening luggage-tag puzzle, the codes `1021`/`1972`, the six puzzle families, container structure,
   lock hardware and postcard order are now explicitly soft. Anything marked "Decided" in
   `Norse_Brainstorm.html` before 2026-09-12 is a strong candidate, not a constraint.
2. **`clues.html` created** — a cross-project repository of 167 clue and puzzle techniques across
   eight categories (text 30, symbols 24, maps 22, props 26, materials 19, logic 13, combining 21,
   structure 12), each with a plain description, a worked example written for one of our own games, a
   build cost, a 1–5 difficulty rating, optional pitfall note, and a source link. Plus a principles
   page and a sources page citing Nicholson's escape-room papers, The Codex, the Wiemker taxonomy
   paper and MIT Mystery Hunt construction guides.

   The **Combining clues** category was added after a follow-up discussion about composition rather
   than concealment. Its organising idea: locks gate access, pointers gate understanding, so the
   number of puzzles need not equal the number of locks. It covers pointer chains (the lockless
   "the answer names the next prop" pattern, plus the *inert until named* fix for its shortcut
   weakness), rule/data splits, instruments, selection-and-order splits, transformation chains,
   accumulators, convergence and the *burst structure* (a lock releases props, a hardware-free chain
   plays out among them, the last step yields the next code). Seven entries specifically cover
   getting several props to feed one lock — searchable with "several props".
3. **Leif's map given a front-of-sheet job — the "Beasts on the chart" chain**, written into
   `Norse_Brainstorm.html`. Seven unlabelled animal vignettes on the North Atlantic sea chart
   (BEAR, WOLF, SEAL, ORCA, CROW, HARE, DEER), each drawn in a setting only that animal occupies.
   A postcard points to one; identifying it gives a four-letter key; the key is looked up letter by
   letter on an A–Z visitor index printed on the back of the L'Anse aux Meadows museum ticket,
   giving four digits. A transformation chain, not a pointer — neither prop is any use alone.
   This answers the gap `PZ-09` flagged, since Leif's only other job is on the back of the sheet.

   User decisions recorded: beasts are **unlabelled** (context does the identifying, not captions),
   the lookup is a **keyed index on the ticket back**, and there is **no validator** — the lock is
   the check. That last one is deliberate and means a misidentification is only caught by the
   padlock, so the middle hint rung pushes on identification rather than on the lookup.

   `BOAR` was requested and excluded on the native-species test: wild boar are not native to North
   America. It moves to Rollo's map, where it is both correct and apt (Roumare was a hunting
   forest). `DEER` was kept, drawn as a caribou, which is genuinely native to all three Leif stops.

### Files Changed

- `AGENTS.md` — "Norse Backpack — current design invariants" section rewritten and dated.
- `clues.html` — new, cross-project clue/puzzle library with tabbed nav and a live search.
- `index.html` — added a Clue Library card under "Design guides & brainstorming".
- `NorseBackpack/Norse_Brainstorm.html` — new "Beasts on the chart" puzzle entry; `PZ-09` updated
  (Leif now has two decided jobs, boar noted against Rollo); new `PZ-10` for the pointing clue.
  Also fixed three hardcoded puzzle counts in the script (`i===6`, `/ 7`) that would have broken
  the journey and detail nav as soon as an eighth puzzle was added.
- `HANDOFF.md` — this handover entry.

### Checks

- Opened `clues.html` in the in-app browser. JavaScript runs, all 10 nav tabs switch correctly,
  category counts render, and all 167 cards have a source, a worked example, a build cost and a
  valid category.
- Search verified as spanning every category rather than only the open tab ("lamp" returns 6 across
  four categories); empty-state message verified.
- Deep links (`clues.html#view-map`) verified. Fixed a bug found during testing: an unknown hash
  such as `#view-typo` threw a TypeError in `render()`; `navigate()` now falls back to the intro page.
- All PDF links confirmed `target="_blank" rel="noopener"` with no `download` attribute, per the
  house rule. No relative or broken links.
- Card layout verified through the DOM (three-column grid, cards 377 × 392). Screenshots of the
  scrolled grid came back blank — a preview-pane painting artifact, not a page fault, confirmed by
  `elementFromPoint` returning the expected card content at those coordinates.
- Opened `Norse_Brainstorm.html` in the in-app browser. All 8 puzzles render without error, the
  journey grid shows 8 steps with the ending card last, and prev/next disable correctly at both
  ends — verifying the hardcoded-count fix. `PZ-09` and the new `PZ-10` render in Open questions;
  no console errors and no `undefined` in the output.

### Next Action

Settle `PZ-10` — how the postcard points to one square of Leif's chart. The leading candidate is the
typed publisher's imprint every card already carries (*Édition Vinland Nº 14* → *Série F · Nº 1*),
which hides the grid reference in plain sight and keeps the card carrying the rule rather than the
data. Also open in the same question: whether the chart carries a lettered grid or a latitude and
longitude graticule — the graticule is what a sea chart would really have and reads as navigation
rather than as a lookup device.

Codex is picking up the chart artwork (the seven animal vignettes). The constraint to hand over:
all seven must be identifiable at true print size from setting as much as silhouette, and bear
versus wolf is the risky pair — both read as "quadruped" at 8 mm. A test sheet of all seven at size
should come before final artwork.

## Earlier Session — Knotwork Raven Chosen; Matching Profile Icon Built

**Session scope:** choose the adventure's main raven image and derive its matching frame-free icon.

The user chose `Raven_Profile_Knotwork_Frame_v1.png` as the current main image and possible family
symbol. The spread-wing study remains secondary. A new profile icon preserves the same raven's
pose, engraved detail and palette while removing the whole knotwork frame. ImageGen twice returned
a checkerboard baked into RGB instead of real transparency; `remove_checkerboard_background.js`
therefore removes the repeated neutral checker colours deterministically. A cream-background proof
caught and removed an enclosed checker patch between the legs. `PR-15` is now **Main image chosen**.

### Files Changed

- `NorseBackpack/Art/Raven/Raven_Profile_Icon_v1.png` — new, transparent frame-free icon.
- `NorseBackpack/Art/Raven/remove_checkerboard_background.js` — reproducible alpha cleanup.
- `NorseBackpack/Norse_Brainstorm.html` — main image decision, icon preview, edit prompt and alpha
  correction recorded.
- `HANDOFF.md` — this handover entry.

### Checks

- Final icon is 1254 × 1254 RGBA with alpha extrema 0–255.
- Rendered on cream and inspected: frame and checkerboard are fully absent, including between the
  legs; raven silhouette and pale engraved feather detail remain intact.
- Screen-size proof inspected at 64, 128 and 256 px; the profile remains identifiable at 64 px.
- HTML structure remains balanced after the new three-image identity card.

### Next Action

Test the frame-free profile at its intended printed size. It is still intricate hero-derived art;
if a true 20 px map glyph is needed, simplify from this silhouette rather than scaling it blindly.

## Latest Session — Two Intricate Hero Raven Studies

**Session scope:** create the two approved compositions for the adventure's central raven artwork.
No small raven icon derived and no artwork placed into a finished prop.

Generated two transparent 1254 × 1254 PNG studies in the established dark forest-green and muted
rust palette: a symmetrical spread-wing heraldic raven with interlace built into the feathers, and
a profile raven inside a complete circular Norse knotwork frame. Both use adult-raven anatomy cues
(heavy beak, shaggy throat, wedge tail) and avoid the chick-like proportions of the rejected icons.
`PR-15` is now **Built · review**; exact ImageGen prompts and both previews are recorded in the
Design guide.

### Files Changed

- `NorseBackpack/Art/Raven/Raven_Spread_Wing_Emblem_v1.png` — new.
- `NorseBackpack/Art/Raven/Raven_Profile_Knotwork_Frame_v1.png` — new.
- `NorseBackpack/Norse_Brainstorm.html` — `PR-15` updated and hero-study card added with prompts.
- `HANDOFF.md` — this handover entry.

### Checks

- Both files are 1254 × 1254 RGBA PNGs with genuine transparent and opaque pixels.
- Both generated compositions were visually inspected at full size; no text, scenery or extra full
  bird is present, and both read clearly as ravens.

### Next Action

Choose the lead hero composition and request any single targeted refinement before deriving a
simplified small raven icon from it.

## Latest Session — Seven Icon Subjects Approved; Raven Split Out

**Session scope:** record the review of the five icon sets and begin a separate direction for the
adventure's central raven artwork. No new raven artwork generated yet; composition comes first.

The user approved all five style treatments for seven subjects: longship, settlement, longhouse,
runestone, burial mound, round shield and Dane axe. No single global style was chosen; consistency
is required within each finished piece. All five small raven studies are rejected because they
read as chicks. `PR-14` now records the seven-subject approval, while new `PR-15` treats the raven
as intricate hero artwork for *The Raven Inheritance*, with a small derived map icon deferred.

### Files Changed

- `NorseBackpack/Norse_Brainstorm.html` — Design guide approval/rejection recorded; `PR-14`
  rewritten and `PR-15` opened.
- `HANDOFF.md` — this handover entry.

### Checks

- HTML structural counts remain balanced after the two register updates.

### Next Action

Choose the hero raven's composition, then generate a first intricate transparent artwork study and
record its exact prompt under `PR-15`.

## Latest Session — Five Complete Norse Icon Style Options

**Session scope:** rebuild the reusable eight-icon family as five coherent style choices after the
first-pass raven and Dane axe were judged unclear. No icon has been placed on a map or prop.

Built 40 transparent SVGs: the same eight subjects in clean-map, carved-woodcut,
historic-manuscript, antique-cartography and hand-drawn treatments. The raven now uses a dark,
heavier beak and wedge tail instead of the first pass's orange, duck-like beak. The Dane axe now
has one broad crescent blade visibly joined to its long haft. A single comparison sheet shows all
five sets at 64 px and 20 px. The old root-level set remains only as a superseded reference.

### Files Changed

- `NorseBackpack/Icons/Options/` — five folders containing eight SVGs each.
- `NorseBackpack/Icons/build_style_options.js` — editable data-driven source for all 40 SVGs and
  the comparison sheet.
- `NorseBackpack/Icons/Norse_Icon_Style_Options.svg` and `.png` — comparison artifacts.
- `NorseBackpack/Norse_Brainstorm.html` — Design guide preview updated; `PR-14` opened for the
  style choice.
- `HANDOFF.md` — this handover entry.

### Checks

- All generated SVG files parsed as XML and share the intended 64 × 64 viewBox.
- The comparison sheet rendered locally and was visually inspected at both displayed sizes.
- All 40 individual files rendered successfully at 20 px with transparent backgrounds intact.
- No browser check: the in-app browser continues to block local `file://` SVG URLs by policy.

### Next Action

Choose a whole style in `PR-14`, or name any deliberate hybrid choices, before replacing the
superseded root-level set or placing icons on maps.

## Latest Session — Reusable Norse SVG Icon Set

**Session scope:** a small reusable icon family for text and maps. No map placement or puzzle
content changed.

Built eight individual transparent 64 × 64 SVGs: longship, settlement, longhouse, runestone,
burial mound, round shield, Dane axe and raven. They use the existing map-art palette
(`#283B34` with restrained `#B56A2A`) but are deliberately simpler than the large `PR-11` PNG
vignettes so they remain readable at roughly 20–24 px. Added an SVG preview sheet and a rendered
PNG preview. Recorded the set and its construction rules in the Design guide tab.

### Files Changed

- `NorseBackpack/Icons/` — eight individual SVGs plus `Norse_Icon_Set_Preview.svg` and `.png`.
- `NorseBackpack/Norse_Brainstorm.html` — reusable icon-family card added to Design guide.
- `HANDOFF.md` — this handover entry.

### Checks

- All nine SVG files parsed as valid XML.
- Every individual icon rendered to 256 × 256 PNG with real transparent pixels and opaque art.
- The combined preview rendered at 1440 × 780 and was visually inspected; all eight are distinct
  at map size, and the compact text-size row remains legible.
- The in-app browser refused the local `file://` SVG URL under its browser security policy, so a
  live browser check of the standalone SVG was not possible. The local SVG renderer succeeded.

### Next Action

Review the preview, then choose whether a second batch should extend map locations (fort, harbour,
church, trading place) or object/ornament symbols (comb, coin, game piece, drinking horn).

## Latest Session — Leif's Map: Frame Pan, Guard Fix, Art Placed Correctly

**Session scope:** Leif's trail map only, continuing directly from Codex's decoration pass below.
Two connected pieces: panning the frame east per the user's request, and fixing three real defects
in how the six vignettes from that pass were actually sitting on the sheet.

### `PR-13` decided — frame panned one grid column east, same scale

User asked to pan the map one `PR-12` grid column right (map moves left) to trim the empty
Nunavik/Ungava Bay/Québec mass and bring Greenland fully into view. An Iceland-inclusive frame was
tried first and rejected in chat (Qikiqtarjuaq's label collided at that zoom, and two of Aud's
stops leaked onto Leif's sheet by name) before the user asked for the plain one-column pan instead.

**A real bug surfaced by actually building the literal request.** The stop-in-frame guard checks a
stop's raw longitude against the frame's nominal box; Qikiqtarjuaq (67.6°N) reads as just outside
that box after the shift and the guard correctly refused to build — but was wrong to refuse. A
conic projection's meridians converge toward the pole, so the point's real *projected* position
lands 1.83 in inside the printed map. Verified by projecting it, not by trusting either the
assertion or a relaxed copy of it. **Both frame guards (stops, region labels) were rewritten** to
check the projected page position against the printed map area instead of the raw coordinate
against the frame's lon/lat box — the real question was always where the point lands on paper.

The pan itself still cost one region label a real collision, unrelated to the guard question:
HELLULAND's label had to move (68.2,−68.6 → 68.5,−70.0) because its old spot now collided with
Qikiqtarjuaq's own label — caught by the stop-collision guard added in the grid session, exactly
the case it exists for. Bonus: Brattahlíð/Qassiarsuk — Erik the Red's estate, where Leif
historically sailed from — now falls inside the frame and labels for free from the existing corpus.

### Three defects fixed in the art Codex placed

1. **The ship (and iceberg, and polar bear) were made of glass.** Their sails/hull/rock faces had
   fully transparent interiors, so the `PR-12` reference grid printed straight through them. Fixed
   on the pixels, not by re-rendering: new `fill_art_alpha_holes.py` closes tiny linework gaps then
   fills every fully-enclosed transparent hole with a pale paper tone. The whale and settlement came
   back untouched — both are genuinely open line art with no enclosed body, not filled silhouettes
   with a bug. Source assets in `Art/` are untouched; the build now draws from `Art/processed/`.
2. **The longship was too large**, per direct user feedback — shrunk from 2.36 × 1.61 in to
   1.70 × 0.85 in.
3. **The wolf collided with the word "MARKLAND", and the settlement collided with "GRŒNLAND"/Nuuk.**
   The original placement checked distance from named *points* only; it never checked the actual
   footprint of a region label, which is wide (letter-spaced small caps). Re-placed both by a proper
   search: maximise clearance from the printed coastline, then require the candidate box to miss
   every reserved label box from a clean (art-free) build. Final clearances: bear 5.8°, wolf 1.9°,
   settlement 4.1° from the nearest coastline; all three also clear the drawn route by the usual
   26pt halo, and no two vignettes overlap each other.

All six re-verified after the frame pan: inside the printed map area, clear of the route corridor,
clear of every label, clear of each other. Stop-collision guard clean; the three collisions in the
build log (Makkovik, Red Bay, Rigolet) are decoys, checked by name against the route plan.

## Files Changed

- `NorseBackpack/TravelMap/build_trail_maps_pdf.py` — `TRAILS["leif"]` frame/lon0/regions/areas/
  waters/extra_towns updated for `PR-13`; both frame-validity asserts rewritten to check projected
  page position instead of raw lon/lat; `ART_DIR` repointed at `Art/processed/`; `LEIF_ART` boxes
  replaced (smaller ship, bear/wolf/settlement re-placed).
- `NorseBackpack/TravelMap/fill_art_alpha_holes.py` — new. Fills enclosed alpha holes in the six
  vignettes; `Art/processed/` is its output, regenerate after any new or replaced asset.
- `NorseBackpack/Norse_Brainstorm.html` — `PR-13` added as Decided; `PR-11` updated with what was
  actually built and the placement-search method; stale "Chosen for Leif" line (old Baffin/Nuuk
  positions) corrected to match.
- `output/pdf/Trail_Map_1_Leif_{Print,ANSWER,ART_GUIDE}.pdf` — rebuilt. Rollo and Aud rebuilt too,
  as a regression check on the shared guard code; both unchanged (still digits 9 and 7).

## Checks

- Guard clean on all three unblocked trails after the assert rewrite — confirms the fix didn't
  loosen anything for Rollo/Aud, only correct the projection-vs-raw-coordinate mismatch for Leif.
- Every one of the six vignette boxes checked programmatically post-placement: inside the printed
  map area, ≥26pt from the drawn route, zero overlap with any of the ~55 reserved label boxes from
  a clean build, zero overlap with each other.
- Before/after crops of the three alpha-filled assets (longship, iceberg, polar bear) rendered over
  a grid-line backdrop and inspected: interiors read as solid fabric/rock, hatching preserved as ink
  on top of the fill, no artifacts.
- Leif Print and ANSWER rendered at 180 dpi and inspected in full; ANSWER still reads as digit 1.
- Page opened in the in-app browser, Open questions tab clicked, `PR-13` and the rewritten `PR-11`
  read on screen; tag balance 693 `div` / 11 `section` / 19 `figure` / 8 `details` / 8 `table` /
  11 `svg` / 92 `li` / 158 `strong` / 138 `code` / 20 `em` / 84 `b`, all paired.
- Not run: true-size physical print of the new frame or the filled art; no test of whether the pale
  fill tone reads correctly once actually printed and laminated (extends `PR-09`'s open print test).

## Next Action

Print the current Leif sheet true-size and confirm the filled sail/hull/iceberg read as solid on
paper, not just on screen. Aud and Rollo still have no decoration pass — `PR-11` covers Leif only.

## Blockers and Open Items

- The Iceland-edge framing (lon −65.5..−23.0) was built and verified working but not adopted; kept
  only as a rejected option in this session's chat, not written to any file. Revisit only if the
  user asks for Iceland again.
- `fill_art_alpha_holes.py` is a manual re-run step, not wired into `build_trail_maps_pdf.py`'s own
  pipeline — if a new asset lands in `Art/` and the fill script isn't re-run, the build will happily
  draw the old `Art/processed/` copy or fail to find the new file. Worth wiring together later.
- Everything else carried over unchanged from the previous session below (Harald blocked, `PR-10`
  coordinate sourcing, Rollo's decoy thinning, `PZ-09` second jobs).

---

## Previous Session — Leif's Map: Balanced Treasure-Map Decoration

**Session scope:** Leif's trail map only. The user chose the balanced decoration option; no other
map or puzzle was changed.

### `PR-11` built — six restrained vignettes

Leif's sheet now carries a westbound longship in safe sea slot A, a breaching whale in B, and an
iceberg with floes in D. Three smaller land ornaments add the requested treasure-map character: a
polar bear on Baffin Island, a wolf in Labrador / Québec, and a three-building Norse-style cluster
beside Nuuk. The sea pieces remain inside the placement-guide boxes. The land pieces are drawn
under labels and reserve their own boxes before town-label placement, so a label moves rather than
printing through the art. No new settlement name or map point was invented.

All art is transparent PNG, placed at reduced opacity, and uses the existing dark green, grey and
muted rust palette. The exact final ImageGen prompts are recorded in the Design guide tab. A first,
more detailed whale generation was rejected; only the simplified final prompt and asset are part
of the project.

## Files Changed

- `NorseBackpack/TravelMap/Art/` — six new transparent vignette assets.
- `NorseBackpack/TravelMap/build_trail_maps_pdf.py` — Leif-only decoration placement, proportional
  image fitting, opacity and label-box reservation.
- `NorseBackpack/Norse_Brainstorm.html` — `PR-11` marked built / test print; chosen composition,
  placement rule and exact prompts recorded.
- `output/pdf/Trail_Map_1_Leif_Print.pdf` and `Trail_Map_1_Leif_ANSWER.pdf` — rebuilt with decoration.

## Checks

- Leif print and answer PDFs rebuilt; all 22 labels retained and no stop-label guard fired.
- Both one-page PDFs rendered at 180 dpi and visually inspected in full: artwork is transparent,
  the route corridor remains clear, labels remain readable, and the answer stroke stays dominant.
- Source script compiles; both PDFs reopen as one-page letter PDFs.
- HTML structural counts remain balanced: 688 `div`, 11 `section`, 19 `figure`, 8 `details`,
  8 `table`, 11 `svg`, and 1 `pre`.
- Not run: the in-app browser refused the local `file://` URL under its security policy, so the new
  Design guide card was not visually browser-checked and console errors could not be checked.
- Not run: true-size physical print. `PR-11` stays at **Built · test print** until icon detail and
  opacity are judged on paper.

## Next Action

Review the decorated Leif print PDF, then print one true-size copy. Check that the longship does not
dominate, the small bear/wolf/settlement remain recognizable, and the laminated wet-erase route is
still visually strongest.

---

## Previous Session — Leif's Map: the Reference Grid

**Session scope:** Leif's trail map only. The grid, the knock-on re-cut of the art slots, and the
Codex icon brief. No card file, no other puzzle touched.

### `PR-12` closed — a 9 × 11 lettered grid on every sheet

A–I across, 1–11 down, labels repeated on all four sides in a new 12 pt border band. Cells come out
0.84 × 0.86 in — visually square, and the division is **exact**, so there are no runt half-cells.

Four treatments were rendered on Leif's sheet and shown side by side before anything was written:
sea-only lattice, lattice over everything, band-only, and sea-only with a chart-style alternating
border. **User chose the lattice over everything.** Applied with one refinement: the grid is drawn
*over the land* (so a settlement can be given a square reference, which is the point of choosing
this variant) but *under every label*, so no printed line can sit on a clue. Verified at 300 dpi on
the densest cluster — Rigolet has a grid line behind it and still reads clean.

The grid belongs to the **sheet, not the geography** — all four maps carry the identical 9 × 11
whatever frame they use, so a square reference means the same place on the page every time. The
accepted cost is that a square is ~190 km on Leif's sheet and ~55 km on Aud's.

The old 5° degree graticule is **removed**; the grid replaces it. Recoverable from git if wanted.

### It re-framed every sheet, and that had consequences

The band takes 12 pt per side, so the projection rescales on all four maps. Two knock-ons:

1. **Every slot size in `PR-11` went stale.** Measured, not assumed: A 1.88 × 4.50 → 1.62 × 4.25,
   B 1.12 × 2.00 → 1.38 × 1.50, and so on. This is why the grid had to land before Codex was
   briefed, not after.
2. **Two more decoy labels now collide** — Caen and Falaise on Rollo, Krosshólaborg on Aud. Checked
   against the route plan: none is a stop.

That second point exposed a **real defect in the existing build guard**. It only caught stops
*missing from the corpus*; a stop whose label was dropped for collision would have passed silently
and been unfindable on the sheet. With the frame now tighter that is reachable, so the guard was
extended to cross-check `lab.skipped` against the stop names. Clean on all six sheets.

### `PR-11` — slots recut landscape

The greedy largest-rectangle search was maximising area and producing tall columns; against the new
frame the biggest was 1.62 × 4.25 in, which is the worst possible frame for a ship under sail. The
guide now constrains aspect to roughly 1.4:1–2.0:1 via a prefix-sum sweep over candidate sizes.
Result: five usable slots, A 2.50 × 1.75 in down to E 1.25 × 0.88 in. **A, B and C are contiguous**
in the Labrador Sea — filling all three would read as one block, so the brief says take two.

### Two collisions recorded rather than solved

- **Leif's sheet now carries two grids** — this one on the front, the hnefatafl setup on the back
  (`PZ-07`), whose registration instruction is literally "align on the grid lines". `PR-09` was
  extended: its print test now has to read *both* faces, since a front grid ghosting backwards would
  add noise to exactly the lines the offset registers against.
- **`ST-05`'s dig-site plan is gridded too.** Family resemblance or false lead — left open.

## Files Changed

- `NorseBackpack/TravelMap/build_trail_maps_pdf.py` — `BAND`, `GRID_COLS`/`GRID_ROWS`, map area
  inset; graticule block removed; grid drawn between the land fill and the labels; frame/corner-tick
  block replaced by the band and its references; stop-collision guard added.
- `NorseBackpack/TravelMap/build_art_placement_guide.py` — `largest_rects` replaced by
  `landscape_rects` (prefix-sum, aspect-constrained); docstring and legend updated.
- `NorseBackpack/Norse_Brainstorm.html` — `PR-12` added as Decided; `PR-11` slot figures replaced
  and the aspect change recorded; `PR-09` extended with the reverse ghosting direction.
- `output/pdf/` — all six trail-map PDFs rebuilt (`Trail_Map_{1,2,3}_*_{Print,ANSWER}.pdf`) and
  `Trail_Map_1_Leif_ART_GUIDE.pdf` regenerated.

## Checks

- All six sheets rebuilt; stop-label guard clean on every one.
- Dropped decoy labels cross-checked by name against `Norse_Aunt_Route_Plan.json`: Caen, Falaise,
  Hastings, Lewes, Salisbury, Southampton, Krosshólaborg are none of them stops.
- Leif, Rollo, Aud print sheets and Leif's answer key rendered and visually inspected. Leif also
  inspected at 300 dpi over the densest label cluster to confirm no grid line crosses a name.
- New slot figures taken from the guide's own printed output, not estimated.
- `Norse_Brainstorm.html` tag balance after the edits: 687 `div`, 11 `section`, 19 `figure`,
  7 `details`, 8 `table`, 11 `svg`, 92 `li`, 151 `strong`, 135 `code`, 20 `em`, 76 `b` — all paired;
  `br` void.
- Page opened in the in-app browser, Open questions tab clicked, `PR-11` and `PR-12` read on screen
  and confirmed rendering correctly. No console errors.
- Not run: no print test of the grid at true size; no test of whether the front grid ghosts through
  to the back of Leif's sheet (`PR-09`); the four grid variants were judged on screen, not in print.

## Next Action

Write the Codex icon brief into the Design guide tab and generate the art. Proposed set, **not yet
agreed**: longship under sail (two poses), a sea beast for the open Labrador Sea, ice floes for
Davis Strait, an ornate compass rose replacing the script-drawn one, and a title cartouche. Flat
screen-print, *not* the engraved cross-hatched style of the stamps — the map's own line work is
flat. Transparent PNG at 600 dpi minimum; anything with a baked background shows as a box on the
sea tint.

## Blockers and Open Items

- Harald's map still cannot build — "Sicily" and "Asia Minor" are regions with no endpoint.
- `PR-10`: every `APPROX` map coordinate still needs source-checking before a sheet is printed.
- Rollo's south-coast English cluster now drops six decoy labels, one more than before. No stop
  affected, but the list still wants thinning down there.
- The red acetate filter and the UV pen/blacklight remain on the decided tool list with no puzzle
  feeding them.
- `PZ-09`: Aud, Rollo and Harald still need their second job chosen.

---

## Previous Session — Props: Hnefatafl, the Four Maps, the Dig Site

**Session scope:** the prop side, while Codex worked the cards in parallel. No card file was
touched. Four connected pieces: the hnefatafl puzzle, the final map mechanic, the printable maps
themselves, and the dig site.

### 1. `PZ-01` closed — hnefatafl at three moves

A commercial set forces three changes: board size (built for 7 × 7 Brandubh; 9 × 9 and 11 × 11 are
commoner), piece count (a stock 7 × 7 gives 12 non-king pieces against this layout's 14 blockers),
and the readout — nothing can be printed on a bought board. The real cost is the throne
compartment, which no commercial set can have (`PR-08`).

Decided: **three moves**, and the code is **how far the king travels on each leg**. D4 → F4 → F7
→ G7 measures 2, 3 and 1 → `231`. Works bought or built, and retires the objection that digits on
a game board announce it as a puzzle prop.

### 2. `PZ-07` opened — the board setup split across two papers

Liv wrote the piece positions on the back of a trail map; the museum pamphlet was pressed onto wet
ink and lifted the right-hand strip, leaving an illegible smear on the map and a **mirrored** copy
on the pamphlet's blank end panel. The pamphlet is an invented **Hnefatafl Museum, Oslo** leaflet
that also carries the simplified rules, so rules arrive as printed matter and Liv's handwriting
keeps its single job. Verified rather than assumed: the full board has exactly one three-move
escape, but assuming the hidden strip empty yields **18** candidate routes — the puzzle refuses to
resolve instead of resolving wrongly. A three-panel sketch is embedded in the Design spec tab.
**Later in the session the map was chosen: Leif's** (see 6).

### 3. `PZ-06` closed — four laminated letter sheets, wet-erase marker

Printed and laminated at home, gloss pouches, cards laid beside each map in date order, legs drawn
onto the laminate. No pins, cord or overlay.

**Pinned cards was eliminated on geometry, not preference** — the finding worth keeping. Rouen and
Roumare are 10 km apart on a 624 km trail, so they fall 0.13 in apart on letter and still only
0.38 in apart on a 24 × 36 poster. No printable size separates them enough for two postcards.

### 4. The printable maps — built

`NorseBackpack/TravelMap/build_trail_maps_pdf.py` builds all four sheets plus answer keys from one
script, so a key cannot drift from the sheet it answers. Natural Earth 50m coastlines from the
vendored `land.js`, Lambert conformal conic, explicit per-trail frames, postcard palette.
Settlement labels come from `stops.js`, the 72-entry sourced research corpus, so the decoys are
other places from Liv's own research.

Built: **Leif, Rollo, Aud** — print sheets and answer keys. **Harald is blocked** and the script
refuses it: stops 5 and 6 are "Sicily" and "Asia Minor", regions with no endpoint to draw to.

Answer keys confirm the shapes. **Aud's 7 is clean. Rollo's 9 works well** — the Rouen/Roumare
10 km gap turns out to be what closes the loop. **Leif's 1 is confirmed weak**: a single straight
stroke with a stub where L'Anse and Battle Harbour nearly coincide. It survives on the two
backstops only (one lock left, `1972` parses as a year). Worth a play-test early.

### 5. Leif's stops fixed — regional anchors replaced

The route plan had "Markland candidate" and "Helluland candidate" as *regional anchors*, while
postcard 02 is Battle Harbour. With stops unmarked, players locate each stop by name, and a saga
region the size of Spain has no endpoint. Now `l-meadows → l-battle → l-qikiqtarjuaq`.
Qikiqtarjuaq was chosen from four Baffin candidates: most upright long leg (16° off vertical) and
the east-coast approach a ship following the coast would make.

`stops.js` was **left alone** — it is the historical corpus, and Markland/Helluland remain valid
research entries there. Only Liv's itinerary moved. This created a trap that was caught and fixed:
the page's mini-maps resolve IDs against that corpus with `.filter(Boolean)`, so the two new IDs
would have **silently vanished** — three pins quietly becoming one. A supplement now merges
itinerary-only stops into the lookup.

### 6. Map presentation decisions

- Title block **stripped to the title alone**. Cut: the trail name and "Map n of four" (they
  pre-sorted the deck and handed over the digit order), the find-them-by-name instruction
  (designer's voice, not Liv's), the `stops unmarked by design` note, and finally the
  projection/coastline credit. Natural Earth is public domain and asks for no attribution;
  provenance stays in the script and `TravelMap/README.md`.
- `PZ-08` **decided**: the digit order is the postmark dates — sort the deck, the order each trail
  first appears is its digit's order. Composes with the interleaving decision instead of fighting
  it. **Constrains the unwritten dates**: earliest card per trail must fall Leif → Rollo → Aud →
  Harald or the code is not `1972`. Wants a script once the 18 dates exist.
- `PZ-09` **new principle**: every map earns at least one job besides the endgame. Leif decided
  (board setup on the back, which also settles `PZ-07`'s map question). Aud, Rollo, Harald are
  candidates — Aud's is nearly free, since `Kambsnes` is already labelled and `PZ-03` proposes
  `KAMBR` for the five-letter lock.
- `PR-11` **new**: map decoration is Codex's lane.
  `NorseBackpack/TravelMap/build_art_placement_guide.py` computes where art may legally go — sea
  clear of the route corridor, every label box and the title furniture. Leif's four slots: A 1.88
  × 4.50 in, B 1.12 × 2.00 in, C 1.38 × 1.62 in, D 0.75 × 1.75 in. **Re-run the guide after any
  route change**; the corridor moves with the stops.

### 7. `ST-05` opened — the dig site

The ticket and closing letter already say Norway, so Aud's Iceland map cannot locate it. Proposed:
a fifth letter sheet, Liv's gridded **excavation site plan**, in the last container with the
ticket. Real digs use lettered/numbered grids, it keeps the four trail maps clean, and it has
metres-per-square resolution where a grid on Harald's 2,800 km map would be ~200 km per square.
Its job is explicitly **not** a puzzle — pure payoff plus one optional, ungated noticing-reward,
the only thing in the bag that would make the closing line a payoff rather than a compliment.

## Files Changed

- `NorseBackpack/Norse_Brainstorm.html` — `PZ-01`, `PZ-06`, `PZ-08` closed as Decided; `PZ-07`,
  `PZ-09`, `PR-08`, `PR-09`, `PR-10`, `PR-11`, `ST-05` added or extended; Design spec hnefatafl
  section rewritten with an embedded sketch; both affected `puzzles` JS entries rewritten;
  Prototype board's printed digits removed and its messages switched to leg lengths; Options tab
  candidates unblocked or struck through; Props & choices updated; `routeMapPlans` and the static
  route list updated for Leif's new stops.
- `NorseBackpack/TravelMap/build_trail_maps_pdf.py` — new. All four maps plus answer keys.
- `NorseBackpack/TravelMap/build_art_placement_guide.py` — new. Legal art areas for Codex.
- `NorseBackpack/TravelMap/Norse_Aunt_Route_Plan.json` — Leif's stops 2 and 3 replaced.
- `NorseBackpack/TravelMap/README.md` — Leif's route line rewritten with the reasoning.
- `output/pdf/` — `Trail_Map_1_Leif_{Print,ANSWER,ART_GUIDE}.pdf`,
  `Trail_Map_2_Rollo_{Print,ANSWER}.pdf`, `Trail_Map_3_Aud_{Print,ANSWER}.pdf`.
- Deleted `NorseBackpack/TravelMap/build_trail_map_leif_pdf.py`, folded into the general builder.

## Checks

- Tag balance after every edit round; final 682 `div`, 92 `li`, 151 `strong`, 129 `code`, all
  paired; `br` correctly void.
- Exhaustive board search run twice (full layout 1 solution; hidden strip assumed empty 18). The
  `231` legs were read off the verified route.
- Great-circle distances and sheet-area arithmetic computed from the route JSON, not estimated.
- Every PDF rendered and visually inspected. Leif's print sheet re-checked by text extraction
  after the credit removal: no "Lambert"/"Natural Earth" string remains, title intact.
- Build-time guards added and **they caught real defects**: four stops would have been unlabelled
  and therefore unfindable; `ÍSLAND` was placed outside its own frame and silently never drew.
- Simulated `byId` stop resolution against the real 72-entry corpus: all four trails resolve.
- Defects found and fixed mid-session: `height="auto"` invalid on `<svg>` collapsed the page below
  the sketch; auto-framing zoomed Leif out to 33° of mostly empty ocean and was reverted to
  explicit frames; `ENGLAND / England` printed the same word twice.
- **Two invented place names reached a rendered sheet.** "Reyðhol" and "Hvammsýla" are not real
  Icelandic places — faulty recall, caught only on visual inspection. Removed; Reykholt was the
  real place being garbled. This is why `PR-10` exists: every `APPROX` label needs source-checking.

Not run: no check of what hnefatafl sets are actually for sale (`PR-08` figures are general,
listings unverified). No print test of the offset, the smear, the laminated maps, or the
back-of-map grid show-through (`PR-09`). The pamphlet's historical text is unchecked (`HI-05`).
No play-test that the drawn shapes read as `1972`. The Leaflet mini-maps could not be seen
rendering — the preview pane serves the page as a `data:` URL so the vendor scripts do not load
and `initRouteMaps` guards out; resolution logic was verified against the real data instead.

## Next Action

Settle `PR-08` — bought board versus built — since the hnefatafl layout, the map/pamphlet split
and whether the throne compartment exists at all are downstream of it. Checking real listings for
a 7 × 7 Brandubh set is the concrete first step.

## Blockers and Open Items

- **Harald's map cannot build** until "Sicily" and "Asia Minor" become named settlements. Same
  treatment Leif just had.
- `PR-10`: every `APPROX` map coordinate needs source-checking before a sheet is printed for play.
- Rollo's south-coast English cluster drops five decoy labels to collision; no stops affected, but
  the list wants thinning down there.
- The red acetate filter and the UV pen/blacklight are still on the decided tool list with **no
  puzzle feeding them**. Flagged at the start of this session and still true; `ST-05`'s optional
  find is one candidate job for the UV pen.
- `PZ-09`: Aud, Rollo and Harald still need their second job chosen.

---

## Previous Session — Physical Registration Test

The previous session (Codex, below) left one open unknown: whether ordinary printer scaling
and hand-trimming were accurate enough for the 12-px-wide `1576` half-digits to actually
register when Card 02 is rotated and butted against Card 03.

Reviewed Codex's work first: inspected both fronts at normal size (digits genuinely invisible),
zoomed into the four digit positions on `Postcard_02_Battle_Harbour_Front.png` (found the marks
sit right at the top pixel rows, essentially zero safety margin before trim — a real risk worth
flagging, though Codex's own handoff already named this as the next unknown), and confirmed the
alignment preview images render correctly with no HTML regressions.

Built `NorseBackpack/Postcards/build_topedge_test_sheet.py` — a standalone script (not touching
the real card builds) that crops just the top ~1.2 in of each front at the same 256 dpi the
final cards use, lays them on one small PDF sized for a 100%-scale print, with a "cut here = true
top edge" line on each strip and a 6.00 in reference ruler to catch silent printer rescaling.
Output: `output/pdf/Postcard_02_03_TopEdge_Test.pdf`. Sent to the user to print and test by hand.

**User printed it and confirmed: it works.** The zero-margin risk did not materialize in
practice. This closes the open question from Codex's "Next action" below — no further print
testing needed before finalizing these two fronts.

Files changed this session: `NorseBackpack/Postcards/build_topedge_test_sheet.py` (new),
`output/pdf/Postcard_02_03_TopEdge_Test.pdf` (new, test artifact). Also removed four stray
`_qa_*.png` scratch crops from `NorseBackpack/Postcards/` left over from the review.

Next action: the front-art mechanic is now physically validated. Move on to writing and
building cards 02 and 03's backs (Fun Fact + handwritten message, same structure as card 01's
rebuilt layout) — drafts exist in this session's chat log but were not yet written to any file.

---

## Previous Session — Codex, Front Art

**Session scope (Codex):** make the current Card 02 Battle Harbour and Card 03 Baffin Island fronts
full bleed, then hide a split `1576` along their top edges so rotating Card 02 by 180 degrees
and butting the two top edges together reveals the code.

Done:

1. Reframed both 1536×1024 illustration sources with a uniform ~3% crop so the existing
   screen-print artwork reaches every edge without inventing new scenery or changing the palette.
2. Added four 12-pixel-wide complementary half-digits at fixed centres (x = 384, 640, 896,
   1152). Card 02 uses mirrored source positions and pre-inverted marks; after rotation they
   register with Card 03 as `1576`. Pale, distressed ink makes them read as cloud flecks.
3. Regenerated both titled front PNGs and the two individual print PDFs plus the full postcard
   PDF. Updated the source register's existing `Change:` lines and recorded the decided mechanic
   in the Postcards tab.
4. Added an expanded alignment preview to the Postcards tab: the complete cards in their play
   position plus a 4× seam detail. Both preview images are stored with the postcard assets.
5. User then increased the digit width from 6 to 12 pixels. Regenerated both fronts, the
   alignment images and all three affected PDFs without changing the fixed centres. User
   reviewed the updated HTML preview and confirmed the result is good; this session is complete.

Files changed by this session:

- `NorseBackpack/Postcards/Postcard_02_Battle_Harbour_Illustration_v1.png`
- `NorseBackpack/Postcards/Postcard_03_Baffin_Island_Illustration_v1.png`
- `NorseBackpack/Postcards/Postcard_02_Battle_Harbour_Front.png`
- `NorseBackpack/Postcards/Postcard_03_Baffin_Island_Front.png`
- `NorseBackpack/Postcards/Postcard_02_03_Aligned_Preview.jpg`
- `NorseBackpack/Postcards/Postcard_02_03_1576_Alignment_Proof.png`
- `NorseBackpack/Postcards/References/README.md`
- `NorseBackpack/Norse_Brainstorm.html`
- `output/pdf/Postcard_02_Battle_Harbour_Print.pdf`
- `output/pdf/Postcard_03_Baffin_Island_Print.pdf`
- `output/pdf/Norse_Postcards_Full_Print.pdf`

Checks:

- Inspected both full-size illustration sources and titled fronts: full bleed, composition and
  title hierarchy preserved; half-digits are effectively invisible at normal size.
- Built a 4× nearest-neighbour seam proof from rotated Card 02 plus upright Card 03. It reads
  `1576`, and the four centres align exactly.
- Rendered the affected PDF fronts at 150 dpi and inspected them. Full-set pages 3 and 5 are
  byte-identical to the corresponding individual rendered fronts.
- HTML tag balance remains valid after the preview addition: 639 paired `div`s, 11 paired
  `section`s, 18 paired `figure`s and 7 paired `details` elements.
- Browser visual check of the Postcards tab could not run: this session's in-app browser policy
  blocked the local `file://` URL. Source structure and the displayed image assets were checked.

Next action: print the two fronts at final size, trim consistently, and physically test the
top-edge registration. The code is 12 pixels wide per digit, so printer scaling and trim
tolerance are the remaining unknowns.

## Previous Session (retained because its changes are still uncommitted)

**Session scope:** rework the postcard back-of-card structure (from the new mockup slide in
`Norse_Ideas.pptx`), close the resulting open question, write and build card 01 as the template
card, then flip Leif's trail order so L'Anse aux Meadows is genuinely first. Four connected
pieces of one continuous session, not a whole-game review.

Done, part 1 — structure rework:

1. Read the new "Postcard design" slide in `Norse_Ideas.pptx` (via its raw slide XML — no
   LibreOffice in this environment) and proposed the change in chat first: the mockup's "Fun
   fact" box is a rename/relocation of the existing printed-caption zone, not a new one; its
   voice was initially left to vary per card (typed or handwritten).
2. Reworked the "Four zones" schematic in the Postcard system tab to match: handwritten note
   full-height on one side; stamp, shrunk address, and a titled "FUN FACT" block stacked on the
   other. Renamed "printed caption" &rarr; "Fun Fact" everywhere it refers to this zone. Widened
   the diagram's viewBox 840&rarr;920 to stop legend text clipping (pre-existing issue, fixed
   while the figure was already being redrawn).
3. Logged `PC-12`: letting Fun Fact's voice vary per card meant her handwriting could carry two
   different jobs (trivia and task) on one card with no visual tell between them.

Done, part 2 — closing PC-12 and building card 01:

4. User decided PC-12 always-typed. Updated the voices panel, diagram legend/figcaption, and
   verb D; closed `PC-12` as **Decided**.
5. Settled Fun Fact content for card 01 (L'Anse aux Meadows): the butternut-wood find (real,
   verifiable, ties naturally to the sagas' "Vinland"), per the user's steer away from
   number-bearing trivia.
6. User kept the existing handwritten letter on card 01 exactly as written, including "the first
   stop on my journey." This originally led me to close `PC-08` on a reinterpretation (see part 3
   below for why that reinterpretation was superseded).
7. Rebuilt `NorseBackpack/Postcards/build_postcard_01_pdf.py`'s back-of-card layout: address
   block shrunk into a bordered box, a new bordered, titled "FUN FACT" block added underneath it
   with the butternut-wood text (typeset). Front card and handwritten message untouched.
8. Regenerated `output/pdf/Postcard_01_LAnse_Print.pdf`, `output/pdf/Postcard_01_LAnse_Letter_
   Print.pdf`, and `NorseBackpack/Postcards/Postcard_01_LAnse_Back.png` (1500×1050) from the
   rebuilt script. First render had the "Canada" address line overflowing into the Fun Fact
   title — found and fixed by resizing both boxes, re-rendered clean.
9. Updated the Postcard system tab's "first-card layout prototype" note, job 2's card text, and
   the Next steps list to reflect card 01 as done.

Done, part 3 — flipping Leif's trail order:

10. User decided L'Anse aux Meadows should genuinely be first on Leif's trail, superseding my
    earlier PC-08 reinterpretation ("first stop" = first postcard sent). Flipped the trail
    instead of the sentence.
11. Edited `TravelMap/Norse_Aunt_Route_Plan.json`: `routes.leif` and `visits.leif` reordered and
    renumbered to L'Anse aux Meadows (1) &rarr; Markland (2) &rarr; Helluland (3). Markland stays
    in the middle position, so only the two ends actually moved.
12. Swept every other place this order appears: `TravelMap/README.md`'s candidate-plan summary;
    the Postcard system tab's coverage-matrix column labels *and* the per-column "jobs besides
    the maps" digit row (the doubled-job "2" had to move with the L'Anse column — caught this by
    checking the actual x-coordinates, not just the header labels); the Travel routes tab's
    route summary line and its static `<ol class="route-stops">` list; and the page's embedded
    `routeMapPlans` JS object that drives the live Leaflet mini-maps. Rewrote `PC-08` to record
    the actual fix (route flipped, not the sentence reinterpreted).
13. Did **not** change the decorative static SVG route-shape polylines (digit "1" shape, card 01
    hold-to-light figure, etc.) — connecting the same three points in reverse order draws an
    identical line, so nothing to fix there.

## Files Changed

- `NorseBackpack/Norse_Brainstorm.html` — Postcard system tab (diagram, terminology, PC-08 and
  PC-12 register entries, next steps, job-2 card text, coverage-matrix labels and digit row) and
  Travel routes tab (route summary text, ordered stop list, embedded `routeMapPlans`).
- `NorseBackpack/Postcards/build_postcard_01_pdf.py` — back-card layout: address box shrunk,
  Fun Fact block added with the butternut-wood text; new `FUNFACT` colour constant.
- `NorseBackpack/Postcards/Postcard_01_LAnse_Back.png` — regenerated.
- `output/pdf/Postcard_01_LAnse_Print.pdf`, `output/pdf/Postcard_01_LAnse_Letter_Print.pdf` —
  regenerated.
- `TravelMap/Norse_Aunt_Route_Plan.json` — Leif's trail order flipped.
- `TravelMap/README.md` — candidate-plan summary updated to match.
- `NorseBackpack/Norse_Ideas.pptx` — read only (slide 5 XML), not edited. Was already showing as
  modified in git status at session start (the user's own edit adding that slide); still modified.

Not touched: `Postcard_01_LAnse_Front.png`, the other postcards, `TravelMap/stops.js` (a flat
lookup table, not order-dependent), `TravelMap/map.js`, the stamp artwork, and anything on the
uncommitted Aurora side.

## Checks

- Element balance in `Norse_Brainstorm.html` after all edits: 638 `<div>`/`</div>`, 11
  `<section>`/`</section>`, 16 `<figure>`, 10 `<svg>`, 8 `<table>` — all paired.
- `Norse_Aunt_Route_Plan.json` validated as parseable JSON after the reorder.
- Visual check in-browser: Postcard system, Travel routes and Open questions tabs render
  correctly, no console errors. Confirmed the coverage-matrix column swap and the digit-row fix
  by reading the actual on-screen numbers, not just trusting the label swap. Confirmed the
  Travel routes tab's static ordered list reads L'Anse &rarr; Markland &rarr; Helluland via
  `get_page_text` (the in-app browser's `find` missed it over a smart-apostrophe mismatch — not
  a real issue, just a tool quirk).
- The Travel routes tab's *live* Leaflet mini-maps did not render in this browser tool (blank
  grey boxes, no console error) — the page loads via a `data:` URL in this preview tool, which
  has no base URI, so the relative `<script src="TravelMap/vendor/...">` tags can't resolve.
  Same limitation seen earlier this session with the postcard preview HTML's relative `<img>`
  tags. Not a real defect — verified correctness at the source level instead (the embedded
  `routeMapPlans` array and the underlying JSON are both updated and consistent). If a future
  session needs to see the live map actually render, open it from a real `file://` path or a
  local server rather than this tool's snapshot preview.
- Visual check of the rebuilt card: rendered both PDF pages and the two-up letter sheet to PNG
  with PyMuPDF (`fitz`) at print resolution and inspected them directly.
- **Not run:** LibreOffice (`soffice`) is not installed in this environment, so the pptx skill's
  normal slide-image QA path is unavailable — the mockup slide was read from its raw XML instead.
- Not run: a source check of the butternut-wood fact, or a print test of the rebuilt card.

## Next Action

Write the remaining 17 Fun Facts (`PC-07`, 1 of 18 done) and postmark dates (`PC-03`/`PC-04`)
using card 01 as the template. Card 01's postmark should date **first** on Leif's trail now, not
last — worth double-checking when dates are assigned. After that: build the continuation set on
paper, then solve family D (`PC-05`).

## Blockers and Notes

- Nothing is blocked on a purchase.
- Working tree is not clean: `NorseBackpack/Norse_Ideas.pptx` was already modified before this
  session started (the user's own edit) and remains modified. This session's changes to
  `Norse_Brainstorm.html`, `build_postcard_01_pdf.py`, the regenerated PDFs/PNG,
  `Norse_Aunt_Route_Plan.json`, and `TravelMap/README.md` are also uncommitted. Not committed or
  pushed — user has not asked for that yet.
- If a future session needs to visually QA a `.pptx`, install LibreOffice first, or read the
  slide XML directly as done here. If it needs to see the live Travel Map render, don't rely on
  this tool's `data:`-URL snapshot preview for pages with relative script/image references.
