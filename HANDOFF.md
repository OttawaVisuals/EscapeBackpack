# Project Handoff

Last updated: 2026-09-09 by Codex

## Current Task and Status

The finished L’Anse aux Meadows postcard is now on the local website with exact PNG previews of its printable front and back, an image-credit page, individual postcard PDF and a two-up letter-size PDF.

Nothing You Could Do is the approved handwriting font for Aunt Liv. The letter-size PDF has two 6 × 4 inch fronts on page 1 and two position-matched backs on page 2. The back carries the complete CC BY-SA attribution at a reduced size. Wikimedia Commons is the preferred image source for future postcards, but every file licence must still be checked individually.

## Files Changed

- NorseBackpack/Postcards/Postcard_01_LAnse_Illustration_v2.png — new illustrated front artwork.
- NorseBackpack/Postcards/Postcard_01_LAnse_Style_Study.html — editable title treatment, palette and reusable style rules.
- NorseBackpack/Postcards/Postcard_01_LAnse.html — finished website preview with front, back and printable-file links.
- NorseBackpack/Postcards/Postcard_01_LAnse_Front.png — exact rendered front used by the website.
- NorseBackpack/Postcards/Postcard_01_LAnse_Back.png — exact rendered back used by the website.
- NorseBackpack/Postcards/Image_Credits.html — expandable website credit register for postcard imagery.
- NorseBackpack/Postcards/build_postcard_01_pdf.py — reproducible PDF source.
- Fonts/Nothing_You_Could_Do/NothingYouCouldDo-Regular.ttf and OFL.txt — locally bundled handwriting font and licence.
- NorseBackpack/Postcards/References/LAnse_aux_Meadows_Meeting_of_Two_Worlds_Source.jpg — CC BY-SA source photograph.
- NorseBackpack/Postcards/References/README.md — attribution, license and visual-reference notes.
- output/pdf/Postcard_01_LAnse_Print.pdf — two-page print-ready postcard.
- output/pdf/Postcard_01_LAnse_Letter_Print.pdf — two-up, two-page US Letter duplex print sheet.
- index.html — links to the finished postcard and printable PDF.
- README.md — links the Norse postcard from the project overview.
- HANDOFF.md — current handover.

## Decisions

- Preserve `Postcard_01_Prototype.html` and its harbor artwork as an earlier concept.
- Use landscape 3:2 fronts with one dominant landmark and deterministic HTML lettering.
- Use destination-specific five- or six-colour palettes; the first uses paper, Atlantic navy, patina teal, fog, spruce and ochre.
- Do not use Parks Canada logos, signatures or copied wording/layout.
- Credit D. Gordon E. Robertson and license the adaptation under CC BY-SA 3.0 or a compatible license.
- Put full attribution text on the physical postcard back and maintain a fuller source record on the website.
- Use Nothing You Could Do for Aunt Liv’s handwritten messages.
- Keep the attribution smaller than the message while retaining extractable text and the complete source/licence details.
- Use rendered PDF pages as the website previews so the displayed card matches the printable output exactly.
- Use Wikimedia Commons as the first search source; prefer public-domain, CC0 or CC BY files when suitable to avoid ShareAlike obligations on later artwork.
- Preserve unrelated local AGENTS.md and Aurora map/converter/asset changes.

## Checks

- Source photograph and Canada’s Parks Posters reference inspected.
- Finished website page desktop render — pass; the exact rendered front/back images are visible without clipping.
- Website links — pass; home page, postcard, credits and PDF return HTTP 200.
- Browser console — pass; no warnings or errors.
- PDF structure — pass; two pages, each exactly 6 × 4 inches, with extractable message and attribution text.
- Letter PDF structure — pass; two US Letter pages, with two messages and two attribution blocks extracted from the back page.
- PDF visual inspection — pass on all four affected rendered pages; handwriting, crop marks, alignment, reduced attribution and spacing are clean.
- Physical duplex printing has not been tested.

## Prior Project Context

- Norse route planning is complete in commit `bbbde30`; intended candidate answer is 1972, pending physical recognition testing.
- Norse tone: playful mystery for adults with teens supported; no prior Norse knowledge required.
- Props must reset cleanly. Candidates include museum tickets, rune cryptex, hnefatafl pieces, maps and note facsimiles.
- Cryptex answer/release remain undecided; candidate backpack needs physical fit/hardware checks.
- Aunt Liv’s exact travel dates remain unset.

## Next Action and Open Questions

Print the letter-size PDF double-sided at 100% / Actual Size, flip on the long edge, and check alignment plus the back’s smallest attribution text. Then choose the next route stop and a suitably licensed Wikimedia image.

The current brainstorm page still presents the earlier Seyðisfjörður harbor/314 clue prototype. The new L’Anse aux Meadows art does not yet contain that hidden-code mechanism, so the opening puzzle needs a separate design decision before the old prototype is retired.
