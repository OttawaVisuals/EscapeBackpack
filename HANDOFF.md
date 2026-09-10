# Project Handoff

Last updated: 2026-09-09 by Codex

## Current Task and Status

The Norse website is consolidated around `NorseBackpack/Norse_Brainstorm.html`.

- The retired Seyðisfjörður harbor-postcard prop was removed from the prototype section.
- A new Postcards section shows the front and back of all three current cards.
- Each postcard has its own two-page PDF link.
- A top link opens a combined six-page PDF containing all three cards.
- The Travel routes section now includes four geographic maps with numbered stops, followed by the existing route details and digit previews.
- The root landing page now links only to the consolidated Norse brainstorm page.

## Files Changed

- `NorseBackpack/Norse_Brainstorm.html` — consolidated postcard gallery, PDF links, four embedded route maps and retired-prop cleanup.
- `NorseBackpack/Postcards/Postcard_02_Baffin_Island_Back.png` — placeholder back.
- `NorseBackpack/Postcards/Postcard_03_Battle_Harbour_Back.png` — placeholder back.
- `NorseBackpack/Postcards/build_postcard_collection.py` — reproducible placeholder-back and PDF builder.
- `output/pdf/Postcard_02_Baffin_Island_Print.pdf` — front/back PDF.
- `output/pdf/Postcard_03_Battle_Harbour_Print.pdf` — front/back PDF.
- `output/pdf/Norse_Postcards_Full_Print.pdf` — combined six-page postcard set.
- `index.html` — simplified Norse project link.
- `README.md` — points to the consolidated brainstorm page.
- `HANDOFF.md` — current handover.

The earlier front artwork, source photographs and source-register updates remain part of the same uncommitted work. Unrelated local Aurora and `AGENTS.md` changes remain untouched.

## Decisions

- Do not invent postcard messages or dates. Cards 02 and 03 use explicit placeholder backs until copy is approved.
- Keep individual PDFs and add one combined PDF; all website PDF links open in a new browser tab.
- Use the existing offline Natural Earth coast data and Leaflet for embedded maps.
- Show the selected fictional route order on each map and retain the existing historical-confidence notes beneath it.
- Keep the separate route workshop available only as an optional editing link inside the Travel routes section.

## Checks

- Browser desktop visual inspection: pass for Postcards, Travel routes and Prototype & tests sections.
- All six postcard images loaded at their expected dimensions.
- All four embedded maps rendered; 18 numbered route markers present.
- Browser console after the corrected reload: no new errors or warnings.
- Old harbor-art, prototype-page and 314 mechanism references removed from `Norse_Brainstorm.html`.
- All four PDF URLs return HTTP 200 with `application/pdf`.
- Individual PDFs: two pages each, 6 x 4 inches.
- Combined PDF: six pages, 6 x 4 inches; every rendered page exactly matches its individual source PDF page.
- Full-size render inspection of the four new PDF pages: pass; no clipping, overlap or unreadable text.
- Physical printing has not been tested.

## Next Action

Approve or write the message and travel date for Postcards 02 and 03, then replace the placeholder backs and rebuild the PDFs.

## Open Design Issue

The puzzle-detail and packing sections now mark the replacement opening mechanism and answer as pending. Nothing has been invented to fill that gap.
