# Project Handoff

Last updated: 2026-09-12 by Claude Code

> Session continuity only. Open design questions are **not** tracked here — they live in the
> Open questions tab of `NorseBackpack/Norse_Brainstorm.html`, each with a stable ID.
> See "Where Design State Lives" in `AGENTS.md`.

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
