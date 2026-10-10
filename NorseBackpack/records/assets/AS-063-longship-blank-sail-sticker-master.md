---
id: AS-063
title: Longship blank sail sticker master
type: asset
# idea | candidate | decided | built | parked
status: built
# image | audio | text | print
kind: image
# The prop this asset is for (one ID)
for: PP-046
# Generator or tool used
tool: Built-in ImageGen
# Path from the project folder once made, e.g. assets/star-chart.png
file: Props/LockStickers/Longship_Blank_Sail.png
# Any related record IDs, e.g. [PZ-002, Q-004]
links: [AS-062, AS-061]
# Set to an ID when this record is replaced. It then moves to the Parked tab.
superseded_by:
tags: []
---

Designer selected AS-062 option C on 8 October 2026. This derivative removes its sample numeral so the PDF builder can typeset all numbers consistently. Original concept retained. White exterior preserved; not a transparent cutout. Blank sail and silhouette visually inspected. AI editing may subtly alter pixels; this is not a pixel-identical mask operation.

Exact built-in ImageGen prompt (transparent_background: false):

Use case: precise-object-edit. Edit the supplied approved longship lock sticker. Remove ONLY the large numeral 6 from the cream sail, replacing it seamlessly with the same cream sail surface. Preserve the entire longship exactly: silhouette, sail outline and dimensions, mast, dragon prow, curled stern, hull bands, colours, framing, white background, and all proportions. Do not simplify, redraw, resize, add ornaments, or change any other element. No text or number anywhere. The resulting empty sail will receive typeset lock numbers in a print document.

Production: `Props/LockStickers/build_lock_stickers_pdf.py` places the artwork at 13 mm wide excluding image margins, with Helvetica Bold numbers. Two-digit numbers fit the available sail width. Two copies of each number 1–13 on one Letter page. Existing Word file is a single 300 dpi page image; its page size and anchor are preserved. PP-046 records checks and print limitations.
