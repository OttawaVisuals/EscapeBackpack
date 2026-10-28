---
id: AS-065
title: Rectangular box cover - fireside table
type: asset
# idea | candidate | decided | built | parked
status: candidate
# image | audio | text | print
kind: image
# The prop this asset is for (one ID)
for: PP-045
# Generator or tool used
tool: Built-in ImageGen
# Path from the project folder once made, e.g. assets/star-chart.png
file: Art/Box/Raven_Inheritance_Box_Cover_Fireside_v2.png
# Any related record IDs, e.g. [PZ-002, Q-004]
links: [PR-007, PR-002, Q-029, Q-049, AS-064]
# Set to an ID when this record is replaced. It then moves to the Parked tab.
superseded_by:
tags: [packaging, kickstarter, concept]
---

## Requested direction

### Low ink prototype cover approved 19 October 2026

Designer approved a black-only bookplate treatment for dark green paper: raven and knotwork emblem, title, existing tagline and credits, and a slim ornamental frame. The fireside illustration is retained as an earlier concept. This print variant uses transparent artwork, with no printed green background.

- Word print master: `Print/Raven_Inheritance_Box_Cover_Letter_Black.docx`.
- Artwork: `Art/Box/Raven_Inheritance_Box_Cover_Black_Transparent_v1.png`; raw built-in ImageGen output retained in `Art/Box/Sources/`.
- US Letter landscape, 11 × 8.5 inches, half-inch page margins; artwork fitted proportionally to 7.35 inches high. Embedded picture has a grayscale effect and automatic image compression disabled.
- Verified by Microsoft Word PDF export and visual inspection: one landscape page, readable complete artwork, no clipping. Standard LibreOffice renderer unavailable on this Windows host. Physical print and actual paper contrast not yet tested. Print at 100%, one page per sheet, black/grayscale.

Exact built-in ImageGen background-extraction prompt, with the approved green-paper preview as reference and `transparent_background: true`:

```text
Use case: background-extraction. Remove the green paper background completely from this approved print design. Preserve the exact complete black artwork, title, raven, frame, ornaments, lettering, layout, aspect ratio and spelling. All green areas including between feathers, inside letters and within knotwork must become genuinely transparent. Every visible artwork pixel must be black (#000000) with alpha antialiasing only. No green, white, grey or other color fills; no shadows, no paper texture, no backdrop. Do not redesign, recompose, add or remove anything. Full flat landscape cover, no cropping. Exact text THE RAVEN INHERITANCE / Follow the postcards. Uncover your family’s secret. / A COOPERATIVE PUZZLE ADVENTURE / THE CRYPTIC BUREAU. Return high-resolution transparent PNG suitable for black-ink-only printing.
```

13 October 2026: designer requested a rectangular box to fit an envelope carrying letter-size paper, keeping the raven emblem, title font and The Raven Inheritance name. New scene: cozy wooden table by a fire, several kraft envelopes, some current postcards, a magnifying glass and a notepad. This replaces the square cover direction in AS-064. The rendered concept remains awaiting review.

![Rectangular fireside cover concept](Art/Box/Raven_Inheritance_Box_Cover_Fireside_v2.png)

## Format and copy

Landscape, approximately 4:3 for this exploration; this ratio is not a supplier dimension. Exact internal/external box size, envelope size, clearance and depth are unresolved in Q-049. The previous 11.5 × 11.5 × 2 in assumption is superseded (PR-007). No dieline, side panels or bleed prepared.

- THE RAVEN / INHERITANCE
- Follow the postcards. Uncover your family's secret.
- A COOPERATIVE PUZZLE ADVENTURE
- Small publisher credit: THE CRYPTIC BUREAU

Retains the Norse cover's cream Cinzel-like title and forest-green/copper atmosphere. The shared Bureau Archive identity does not replace the adventure's existing title treatment in this draft.

## Inputs and review

1. Previous cover: `Art/Box/Raven_Inheritance_Box_Cover_A_v1.png` (title/style reference).
2. Raven: `Art/Raven/Raven_Profile_Knotwork_Frame_v1.png`.
3. Current L1 front: `Postcards/Postcard_L1_LAnse_Front.png` (6 × 4 in design).
4. Current H1 front: `Postcards/Postcard_H1_Oslo_Front.png` (6 × 4 in design).

Visually inspected full-size generated output: landscape composition; correctly readable title, tagline, descriptor and Bureau credit; visible fireplace, envelopes, magnifier and notepad. Both postcards retain recognizable reference scenes and correct main place names. ImageGen reinterprets the postcard art and raven rather than embedding exact production files. The notebook has decorative scribbles; it does not provide a puzzle clue. The mug, pencil, notebook and room dressing are illustrative and do not establish included contents. No gameplay changes made.

Raster artwork and text are not print masters. Exact postcard/raven compositing, separate typesetting, supplier dieline and physical envelope fit remain unverified. Source assets preserved.

## Exact generation prompt

Built-in ImageGen, four reference images in the order listed above; `transparent_background: false`.

```text
Use case: compositing.
Asset type: revised flat rectangular landscape board-game box LID artwork for THE RAVEN INHERITANCE, a cooperative physical puzzle adventure.
Input image 1: previous square cover, use ONLY as reference for established cream Cinzel-like title typography, exact title, engraved illustrated finish, deep green and warm copper palette. Replace the old scene and layout.
Input image 2: established profile raven in circular knotwork frame; faithfully retain this emblem, recognizable raven profile and knotwork, modestly sized above the title.
Input image 3: real current L'Anse aux Meadows postcard front, showing two distinctive green patinated abstract sculptures near a coastal boardwalk, pale sky, dark blue caption band.
Input image 4: real current Oslo postcard front, showing golden-lit Akershus fortress against deep blue dusk, dark blue caption band.
Primary request: a cozy wooden table beside a visible glowing fireplace in a welcoming home. A handful of simple kraft paper envelopes of different sizes, including one large rectangular document envelope, are loosely spread/stacked on the table with the two supplied postcards, a hand magnifying glass with a dark wooden handle and round brass rim, and a modest open paper notepad with a pencil. These are ordinary tangible tabletop objects; make the large document envelope visibly larger than the 6x4 postcard props. The postcards should retain the source compositions, colours and recognizable landmarks, not become generic Nordic landscapes. Their only caption text is their original place names. Notebook is mostly blank with faint casual unstructured scribbles, no puzzle solutions or codes. Envelopes simple unmarked kraft, no wax seals or ornate bindings.
Composition: landscape rectangle approximately 4:3 (wider than tall), NOT square. This is the flat full-bleed front artwork itself, not a photograph or 3D mockup of a box. Lower 55 percent dominated by the inviting wooden tabletop and physical items, composed as a lived-in puzzle-solving moment. View the table from a gently elevated seated angle so postcard faces, envelopes and notepad are visible. Soft fireplace glow and a glimpse of its stone surround in the right background, amber firelight grazing the wood. Upper central/left region calm deep forest-green shadows blending naturally into the room; generous uncluttered space for title. Raven emblem above title in this calm region. Title large on two lines, balanced clear hierarchy, all text well inside edges. Avoid covering the postcards with text or the magnifier. No distant fjord panorama.
Exact main text, same styling as previous cover:
"THE RAVEN"
"INHERITANCE"
Tagline below: "Follow the postcards. Uncover your family's secret."
Bottom narrow forest-green footer: "A COOPERATIVE PUZZLE ADVENTURE"
Small discreet publisher credit within footer below descriptor: "THE CRYPTIC BUREAU"
No other added text, no player count, ages, durations, measurements, QR code, barcode, awards or fake badges.
Mood: cozy, curious, believable family mystery, polished richly illustrated board-game art. Warm wood and firelight, deep forest greens, cream serif lettering, restrained copper. Preserve inviting readability rather than excessive tiny detail. No backpack, treasure chest, padlocks, compass, map covering the table, candles, lantern, fantasy runes, floating objects, people, weapons, magic or scary imagery. Paper envelopes are the central packaging motif. Output one finished landscape lid concept.
```
