# Six overlay tiles feasibility test

**Updated direction:** the user prefers patches covering 25–50% of the QR face. A newer prototype in `QR_Patch_Prototype/Aurora_QR_Patches.html` covers **44%** with six connected, non-overlapping patches. It uses the same candidate URLs and fixed masks below, but trims unchanged areas from six horizontal groups. All 64 correctly positioned presence/absence combinations passed the same jsQR check: base URL with no patches, no decode for 62 partial states, target URL with all six. The original full-face layout below is retained as earlier research, not the recommended footprint.

The newer patches cover 275 of 625 QR modules, excluding the quiet zone. Individual areas are 78, 47, 46, 38, 30 and 36 modules. The 275-module footprint contains all 215 changed modules plus 60 unchanged connecting modules. Some connections are only one module wide, so peg placement, structural support and phone-camera testing remain unresolved. Exact occupied cells, master matrices and all decoder outputs are saved in `QR_Patch_Prototype/validated-layout.json`; `build-preview.cjs` reruns those checks and creates the standalone HTML preview using the pinned local libraries.

Proposed alternative to the /k and /s pair. No URLs have been deployed and no existing simulator or guide was changed.

## Candidate that passed the software test

- Base: `https://escapepack.ca/7m2q9v4c`
- Target: `https://escapepack.ca/p6r8t3x5`
- Both URLs: 30 ASCII characters.
- QR version 2, 25 by 25 modules, error correction L.
- Generator: browser QRCode.create from the same qrcode CDN bundle referenced by qr-diff.jsx. Automatic masks were 5 for base and 3 for target. Freeze these masks explicitly when reproducing the design.
- Differing modules: 215. This includes differences caused by the different masks, not just the URL payload.
- Decoder: jsQR 1.4.0, default options.
- Images: opaque black and white, six pixels per module, four-module white quiet zone, 198 by 198 pixels.

## Six connected stepped shapes

Coordinates are zero-based inside the 25 by 25 QR, excluding the quiet zone. Use three column zones and these row boundaries:

| Columns, inclusive | Row boundaries |
|---|---|
| 0 through 7 | 0, 10, 13, 16, 19, 22, 25 |
| 8 through 16 | 0, 9, 12, 16, 20, 23, 25 |
| 17 through 24 | 0, 11, 14, 17, 20, 22, 25 |

Tile i occupies rows from boundary i inclusive to boundary i+1 exclusive in each zone. Join its three zones into one piece. Thus every tile is connected, with stepped edges and a different outline/area. All six pieces together cover the entire QR face. This is a full-face overlay concept, not six small isolated patches. The quiet zone stays uncovered and white.

Each tile prints the target QR's modules within its shape. Absent tiles expose the corresponding base QR modules. Geometry is an ideal 2D pattern only; it does not yet include peg clearances, bevels, print thickness or shadows.

## Results

Tested all 64 correctly positioned presence/absence combinations:

| Arrangement | Count | Decoder result |
|---|---:|---|
| No tiles | 1 | Exact base URL |
| Some but not all tiles | 62 | No decoded QR |
| All tiles | 1 | Exact target URL |

No tested incomplete arrangement decoded the target or another URL.

Earlier six-tile vertical layouts failed this criterion: some five-tile arrangements decoded the target. A simple horizontal layout with row boundaries 0,10,13,16,19,22,25 passed for this candidate and for /fault versus /ready and /offline versus /restore. The stepped geometry above was tested with the random eight-character candidate only.

## Interpretation and limits

More differences can help, but distribution and tile grouping matter. These candidates also use different QR masks. This result is not evidence that URL length alone solves the issue.

This is a successful ideal-image software test, not a physical validation. It does not cover incorrectly placed or rotated pieces, partial overlaps, extra tiles, deliberate URL editing, multiple camera/decoder implementations, scaling, glare, shadows or damaged prints. A reliable physical design needs real phone-camera trials, especially with exactly one tile missing.

Recommended next step: reproduce with fixed generator/version/settings and save both master matrices; create a flat paper prototype; test all six five-tile states and the endpoints on different phones; then design a recessed peg board. Keep shape-fitting from giving away the entire puzzle by adding an explicit in-world placement/repair clue.
