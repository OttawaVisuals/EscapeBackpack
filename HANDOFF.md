# Project Handoff

Last updated: 2026-09-11 by Claude Code

> Session continuity only. Open design questions are **not** tracked here — they live in the
> Open questions tab of `NorseBackpack/Norse_Brainstorm.html`, each with a stable ID.
> See "Where Design State Lives" in `AGENTS.md`.

## Current Task and Status

**Session scope:** rework the postcard back-of-card structure (from the new mockup slide in
`Norse_Ideas.pptx`), close the resulting open question, then write and build card 01 as the
template card. Two connected pieces of one session, not a whole-game review.

Done, part 1 — structure rework:

1. Read the new "Postcard design" slide in `Norse_Ideas.pptx` (via its raw slide XML — no
   LibreOffice in this environment) and proposed the change in chat first: the mockup's "Fun
   fact" box is a rename/relocation of the existing printed-caption zone, not a new one; its
   voice was initially left to vary per card (typed or handwritten).
2. Reworked the "Four zones" schematic in the Postcard system tab to match: handwritten note
   full-height on one side; stamp, shrunk address, and a titled "FUN FACT" block stacked on the
   other. Renamed "printed caption" &rarr; "Fun Fact" everywhere it refers to this zone (jobs
   list, voices panel, verb D, coverage-matrix family D, PC-07, next steps, Design spec tab).
   Widened the diagram's viewBox 840&rarr;920 to stop legend text clipping (pre-existing issue,
   fixed while the figure was already being redrawn).
3. Logged `PC-12`: letting Fun Fact's voice vary per card meant her handwriting could carry two
   different jobs (trivia and task) on one card with no visual tell between them.

Done, part 2 — closing PC-12 and building card 01:

4. User decided PC-12 always-typed. Updated the voices panel, diagram legend/figcaption, and
   verb D to drop the "varies per card" language; closed `PC-12` in the register as **Decided**.
5. Discussed Fun Fact content for card 01 (L'Anse aux Meadows) and settled on the butternut-wood
   find (real, verifiable, ties naturally to the sagas' "Vinland"), on the user's steer away from
   number-bearing trivia — the opening/endgame codes come from elsewhere.
6. User kept the existing handwritten letter on card 01 exactly as written, including "the first
   stop on my journey" — overriding my earlier proposed rewrite. This also settles `PC-08`
   differently than its original note assumed: "first stop" reads as the first postcard *sent*,
   not a claim about trail date order, so no contradiction with the route plan after all. Closed
   `PC-08` as **Decided** on that reading.
7. Rebuilt `NorseBackpack/Postcards/build_postcard_01_pdf.py`'s back-of-card layout to match the
   new spec: address block shrunk into a bordered box, a new bordered, titled "FUN FACT" block
   added underneath it with the butternut-wood text (typeset). Left the front card and the
   handwritten message untouched.
8. Regenerated `output/pdf/Postcard_01_LAnse_Print.pdf`, `output/pdf/Postcard_01_LAnse_Letter_
   Print.pdf`, and `NorseBackpack/Postcards/Postcard_01_LAnse_Back.png` (1500×1050, matching the
   existing file's resolution) from the rebuilt script.
9. Updated the Postcard system tab's "first-card layout prototype" note (now "built", describing
   the actual boxes), job 2's card text, and the Next steps list to reflect card 01 as done.

## Files Changed

- `NorseBackpack/Norse_Brainstorm.html` — Postcard system tab (diagram, terminology, PC-08 and
  PC-12 register entries, next steps, job-2 card text) and the matching Design spec references.
- `NorseBackpack/Postcards/build_postcard_01_pdf.py` — back-card layout: address box shrunk,
  Fun Fact block added with the butternut-wood text; new `FUNFACT` colour constant.
- `NorseBackpack/Postcards/Postcard_01_LAnse_Back.png` — regenerated from the rebuilt script.
- `output/pdf/Postcard_01_LAnse_Print.pdf`, `output/pdf/Postcard_01_LAnse_Letter_Print.pdf` —
  regenerated.
- `NorseBackpack/Norse_Ideas.pptx` — read only (slide 5 XML), not edited. Was already showing as
  modified in git status at session start (the user's own edit adding that slide); still modified.

Not touched: `Postcard_01_LAnse_Front.png`, the other postcards, the stamp artwork, the
travel-map files, and anything on the uncommitted Aurora side.

## Checks

- Element balance in `Norse_Brainstorm.html` after all edits: 638 `<div>`/`</div>`, 11
  `<section>`/`</section>`, 16 `<figure>`, 10 `<svg>`, 8 `<table>` — all paired.
- Visual check in-browser: Postcard system and Open questions tabs render correctly, no console
  errors, PC-08 and PC-12 show as Decided.
- Visual check of the rebuilt card: rendered both PDF pages and the two-up letter sheet to PNG
  with PyMuPDF (`fitz`) at print resolution and inspected them directly. First attempt had the
  "Canada" address line overflowing its box into the Fun Fact title — found and fixed by
  resizing both boxes properly, re-rendered clean on the second pass. Confirmed the front card
  is unchanged and the regenerated `Postcard_01_LAnse_Back.png` matches the PDF back page.
- **Not run:** LibreOffice (`soffice`) is not installed in this environment, so the pptx skill's
  normal slide-image QA path is unavailable — the mockup slide was read from its raw XML instead
  (exact shape positions and text, not a visual render).
- Not run: a source check of the butternut-wood fact itself, or a print test of the rebuilt card.

## Next Action

Write the remaining 17 Fun Facts (`PC-07`, 1 of 18 done) and postmark dates (`PC-03`/`PC-04`)
using card 01 as the template — same two-box back layout, same typed-only Fun Fact voice. After
that: build the continuation set on paper, then solve family D (`PC-05`).

## Blockers and Notes

- Nothing is blocked on a purchase.
- Working tree is not clean: `NorseBackpack/Norse_Ideas.pptx` was already modified before this
  session started (the user's own edit) and remains modified. This session's changes to
  `Norse_Brainstorm.html`, `build_postcard_01_pdf.py`, the regenerated PDFs, and
  `Postcard_01_LAnse_Back.png` are also uncommitted. Not committed or pushed — user has not
  asked for that yet.
- If a future session needs to visually QA a `.pptx` again, install LibreOffice first, or read
  the slide XML directly as done here.
