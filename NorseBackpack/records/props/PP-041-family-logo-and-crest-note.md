---
id: PP-041
title: Family logo and crest note
type: prop
# idea | candidate | decided | built | parked
status: decided
# physical | printed | digital
form: printed
# make | buy | print | 3d-print
source: print
# The play-test page shows the body's "## Player sees" section, or this prop's image asset.
# Where the player gets it: start (in the backpack) or the puzzle whose lock releases it, e.g. PZ-004
found_in: PZ-012
# Physical pocket/container or location; availability remains in found_in above.
container: Large pouch, in the main compartment (lock 12)
# Any related record IDs, e.g. [PZ-002, Q-004]
links: []
# Set to an ID when this record is replaced. It then moves to the Parked tab.
superseded_by:
tags: [old-PR-22]
---

## Design notes (PP-041: Done · drawings approved · marks assigned and printed)

**The two final-bundle reference drawings (PZ-013): a balanced three-part family symbol and a six-field family crest.**

Built by Codex on 19 Sept 2026. The current 3-element symbol (raven, longship, sun-wheel) is a **circular knotwork emblem with three equal compartments**; the subjects have comparable size and none dominates. The 6-element crest (battle-axe, shield, wolf, anchor, drinking horn, valknut) remains a **family coat of arms** in the approved two-column by three-row layout. Both large drawings are reference-only — shown once in the final bundle so players can tell real cards from decoys. A separate set of eleven simple hand-drawn marks now exists for the postcards: nine real elements plus the horned-helmet and double-sided-axe decoys. **Decided, 25 Sept 2026:** the user checked the shield charge on the crest against the sun-wheel in the symbol and judged them different enough, so neither large drawing is redrawn. ~~Shield/sun-wheel marks confusable, redesign needed.~~ **Closed, 20 Sept 2026 (updated 26 Sept 2026 — this entry lagged the actual work):** per-card mark assignment is done, see [Element marks assigned and printed] — all 22 cards carry their mark and the crest filter exists on paper. ~~Which mark sits on each real card remains open; only open item: which mark goes on each real card.~~

##### Superseded family symbol v1 — raven-led edit brief

Use case: precise-object-edit.
Input image: `Art/Raven/Raven_Profile_Knotwork_Frame_v1.png` (Q-029) — edit target, preserve the raven and the knotwork ring exactly as built.
Primary request: work two more charges into the existing circular knotwork ring, without disturbing the raven or the ring's own weave. Add a small longship in full sail low in the ring, roughly where the raven's talons meet the frame, and a small compass rose / sun-wheel opposite it, high in the ring above the raven's back. Both new charges sit *within* the knotwork strands, at the same scale of detail as the two existing raven-head terminals, not layered on top of them.
Style/medium: match the original exactly — intricate hand-inked Norse ornamental illustration, confident varied line weight, manuscript illumination crossed with fine woodcarving.
Composition/framing: unchanged from the original — centered square emblem, raven facing left, full knotwork ring visible, generous transparent margin.
Color palette: unchanged — dominant dark forest green `#283B34` with restrained muted rust `#B56A2A` accents only.
Constraints: no text, letters, runes, additional border, scenery, crown, human figure, extra full bird, glow, shadow, gradient, paper texture, watermark. The longship and sun-wheel must read clearly as those two objects at small size, not as generic knotwork filler.

##### Family coat of arms — new generation brief

Use case: illustration-story.
Asset type: a Norse-styled heraldic shield for the final-bundle reference note, reusable at both full size (the bundle note) and small size (a per-card legend, if reused there later).
Primary request: a single upright heater-shaped shield, divided into six fields (two columns, three rows, or a per-pale-and-per-fess division — six roughly equal charges, none overlapping), each field carrying exactly one charge: a battle-axe, a round shield emblem, a wolf in profile, an anchor, a drinking horn, and a valknut. Each charge should be simple and legible on its own, in the manner of a real heraldic blazon rather than a busy illustration.
Style/medium: flat hand-inked Norse ornamental illustration, matching the raven crest's line weight and construction — manuscript illumination crossed with fine woodcarving, not a cartoon coat of arms.
Composition/framing: centered square emblem, shield fully visible, generous transparent margin, no enclosing frame beyond the shield's own outline.
Color palette: dominant dark forest green `#283B34` with restrained muted rust `#B56A2A` accents only — matching the raven crest and the rest of the project's two-tone palette; no other colors.
Constraints: genuinely transparent background with alpha; no text, letters, runes, crown, human figure, birds, glow, shadow, gradient, paper texture, or watermark. Each of the six charges must read clearly as its named object at both full size and reduced (roughly 1 in wide) size.

![Balanced circular Norse family symbol divided into three equal compartments containing a raven, longship and sun-wheel](Art/FinalPuzzle/Family_Symbol_Three_Field_v2.png)**Family symbol · v2.** Raven, longship and sun-wheel in three equal compartments. Transparent 1254 × 1254 PNG. The raven-dominant v1 is retained as superseded.

![Elaborate Norse family coat of arms with carved interlace surrounding six fields containing an axe, round shield, wolf, anchor, drinking horn and valknut](Art/FinalPuzzle/Family_Crest_Six_Field_v2.png)**Family crest · v2.** Elaborate full heraldic achievement, with the six charges isolated inside the shield in reading order. Transparent 1254 × 1254 PNG. The simpler v1 shield is retained as the superseded first direction.

**Exact ImageGen production prompts**

```
**Family symbol — v2 balanced three-field revision**
Use case: style-transfer
Asset type: transparent family-symbol reference drawing for a printable Norse escape-game final bundle
Input images: Image 1 is the current family symbol and the style/palette reference; preserve its intricate hand-inked Norse engraving language, forest-green, muted rust, bone-silver highlights, and circular knotwork identity, but replace its unequal raven-dominant composition. Image 2 is the layout-principle reference only: like its six shield fields, each required subject must occupy a clearly separated field and receive comparable visual weight. Do not copy Image 2's shield shape, outer heraldic achievement, extra charges, banner, or sculpted 3D finish.
Primary request: Create one balanced circular Norse family emblem divided into exactly three equal-size compartments arranged as three broad 120-degree sectors around a small central boss. Place exactly one subject in each compartment: (1) an adult raven in clear side profile, (2) a Viking longship in clear side profile under one square sail, and (3) an eight-spoked sun-wheel. Scale and simplify the subjects so their visible silhouettes occupy approximately the same area and none dominates. The raven may be a compact full bird or a strong head-and-shoulders profile, whichever best matches the longship and sun-wheel in size.
Style/medium: intricate hand-inked Norse ornamental illustration; manuscript illumination crossed with fine woodcarving; confident varied line weight; refined and ancestral; flatter and more illustrated than the dimensional family coat of arms.
Composition/framing: centered square canvas; circular emblem fully visible; three equal compartments separated by clean knotwork dividers; one continuous circular Norse knotwork border around all three; generous transparent margin. Keep all three subjects immediately readable when the emblem is reduced to roughly 1 inch wide.
Color palette: dark forest green #283B34, muted rust #B56A2A, and restrained bone-silver engraved highlights only; no other colors.
Constraints: genuine transparent alpha background; exactly three equal compartments; exactly one raven, one longship, and one eight-spoked sun-wheel; all three at approximately equal visual size and weight. No shield shape, coat-of-arms grid, crown, supporters, weapons, anchor, horn, valknut, text, letters, numbers, runes, banner, ribbon, scenery, glow, drop shadow, gradient, paper texture, mockup, or watermark. Do not let the raven overlap the other compartments or become the central dominant subject.

**Family symbol — v1 raven-led edit (superseded)**
Use case: precise-object-edit
Asset type: transparent family-symbol reference drawing for a printable escape-game final bundle
Input image: edit target. Preserve the raven, its anatomy, pose, expression, feather detail, circular knotwork ring, two raven-head terminals, exact engraved style, line weight, palette, square framing, and transparency.
Primary request: Add exactly two small heraldic charges inside the existing circular composition: (1) a small Viking longship in clear side profile under one square sail, placed low inside the ring near the raven's talons; (2) a small eight-spoked sun-wheel, clearly a simple solar wheel rather than a modern navigation compass, placed high inside the ring above and behind the raven's back. Integrate both as ornamental charges that visually belong to the existing knotwork design, but keep each silhouette distinct and readable. They may nest into available negative space; do not cover the raven's head, eye, body, wing, legs, or tail, and do not replace or obscure the two raven-head terminals.
Style/medium: match the source exactly—intricate hand-inked Norse ornamental illustration, confident varied line weight, manuscript illumination crossed with fine woodcarving.
Composition/framing: unchanged centered square emblem; raven facing left; full circular knotwork ring visible; generous transparent margin.
Color palette: only dark forest green #283B34, muted rust #B56A2A, and the source's restrained pale engraved highlights. No new colors.
Constraints: genuine transparent background with alpha; exactly one raven, one longship, one sun-wheel; no text, letters, runes, additional border, scenery, crown, human figure, extra full bird, glow, shadow, gradient, paper texture, watermark, or mockup. Preserve the original artwork everywhere except the minimum additions needed for the two charges. The three subjects must remain recognizable at approximately 1 inch wide.

**Family crest — v1 initial generation (superseded)**
Use case: illustration-story
Asset type: transparent family coat-of-arms reference drawing for a printable Norse escape-game final bundle
Primary request: Create exactly one upright Norse-styled heater shield divided cleanly into exactly six equal heraldic fields arranged as two columns by three rows. Place exactly one bold, distinct charge in each field, in this fixed reading order from top-left to bottom-right: single-bladed battle axe; round Viking shield viewed face-on; wolf in clear side profile; traditional anchor; drinking horn; valknut made from three interlocking triangles. No charge may overlap another field. The six icons must be immediately distinguishable and suitable as a visual key for matching small marks on postcards.
Style/medium: flat hand-inked Norse ornamental illustration matching an intricate engraved raven crest—confident varied line weight, manuscript illumination crossed with fine woodcarving, refined and serious, not cartoonish and not photorealistic.
Composition/framing: one centered, fully visible heater-shaped shield on a square canvas with generous transparent margin. Strong outer outline. The internal division is a clear 2-column by 3-row grid following the shield shape. Each charge is centered and given comparable visual weight.
Color palette: only dominant dark forest green #283B34 and restrained muted rust #B56A2A, with sparse pale negative-space engraving highlights. No other colors.
Legibility: preserve strong silhouettes and uncluttered negative space so every charge reads clearly when the entire shield is reduced to roughly 1 inch wide.
Constraints: genuinely transparent background with alpha; exactly six fields and exactly six charges; one battle axe, one round shield, one wolf, one anchor, one drinking horn, one valknut. No text, letters, numbers, runes, crown, raven, bird, human figure, supporters, helmet, banner, ribbon, motto, surrounding frame, scenery, glow, shadow, gradient, paper texture, mockup, or watermark. The round-shield charge inside the larger heater shield is intentional.

**Family crest — v2 reference-led revision**
Use case: style-transfer
Asset type: elaborate transparent family coat-of-arms reference drawing for a printable Norse escape-game final bundle
Input images: Image 1 is the user's composition, depth, craftsmanship, and richness reference only—match its complete heraldic-achievement feeling, sculpted relief, balanced symmetry, and premium finish, but do not copy its specific ship, wolves, raven, axe arrangement, colors, motto, or text. Image 2 is the content/layout reference—retain its central heater shield divided into exactly six fields and retain the six required charges in the same reading order.
Primary request: Reimagine Image 2 as a much richer, more imposing complete Norse heraldic achievement like Image 1. The centerpiece remains one upright heater shield divided clearly into exactly six fields, two columns by three rows. Fixed field order, top-left to bottom-right: single-bladed battle axe; round Viking shield face-on; wolf in profile; traditional anchor; drinking horn; correct valknut of three interlocking triangles. Build an elaborate symmetrical surround using carved Norse interlace, braided mantling, metal bosses, and two tall abstract knotwork supports flanking the shield. Add a substantial carved ornamental crest above the shield made only from interlace and geometric finials. Add a curled blank ribbon below for visual balance, with absolutely no letters or symbols on it.
Critical puzzle clarity: the six objects inside the shield are the only recognizable pictorial charges in the entire achievement. Do not repeat any of them outside the shield. The surrounding decoration must remain abstract ornament, not birds, wolves, ships, axes, shields, anchors, horns, valknuts, crowns, hammers, or other identifiable objects. Keep the six fields visually separate and every charge unmistakable when the full achievement is reduced to roughly 1 inch wide.
Style/medium: dimensional sculpted heraldic relief with the refined premium finish of Image 1, translated into Norse woodcarving and manuscript-inspired interlace; deep engraved detail, restrained highlights, convincing carved metal and enamel depth; serious and ancestral, not cartoonish.
Composition/framing: centered, upright, symmetrical full achievement on a square canvas; full shield and all ornament visible; generous transparent margin; strong silhouette; no cropping.
Color palette: dominant deep forest green #283B34 enamel and dark metal, muted rust/copper #B56A2A ornament, with restrained bone-silver engraved highlights. No blue, bright gold, or extra colors.
Constraints: genuinely transparent background with alpha; exactly six shield fields and exactly six recognizable charges; no text, letters, numbers, runes, motto, name, crown, helmet, human figure, raven, bird, ship, hammer, animal supporters, scenery, floor, wall, mockup, watermark, rectangular backing, or colored background. No generic fantasy heraldry. Preserve a coherent Norse visual language.
```

##### Eleven hand-drawn postcard marks

Built 19 Sept 2026: six crest elements, three symbol elements and two deliberately false decoy elements. These are simple Aunt Liv margin drawings matching the existing Bayeux-style postcard doodles: loose dark outline, flat muted colour and sparse detail. Each production file is a transparent 300 × 300 PNG. A proof around 0.4–0.5 inches wide is suggested, but placement, final printed size and physical treatment remain open.

![Simple hand-drawn single-bladed battle axe postcard mark](Art/FinalPuzzle/PostcardMarks/Crest_Battle_Axe_HandDrawn_v1.png)Battle axe · hand-drawn v1

![Simple hand-drawn round Viking shield postcard mark with a domed boss and no radial spokes](Art/FinalPuzzle/PostcardMarks/Crest_Round_Shield_HandDrawn_v2.png)Round shield · hand-drawn v2 · redesigned to read apart from the sun-wheel

![Simple hand-drawn wolf in side profile postcard mark](Art/FinalPuzzle/PostcardMarks/Crest_Wolf_HandDrawn_v1.png)Wolf · hand-drawn v1

![Simple hand-drawn anchor and rope postcard mark](Art/FinalPuzzle/PostcardMarks/Crest_Anchor_HandDrawn_v1.png)Anchor · hand-drawn v1

![Simple hand-drawn Norse drinking horn postcard mark](Art/FinalPuzzle/PostcardMarks/Crest_Drinking_Horn_HandDrawn_v1.png)Drinking horn · hand-drawn v1

![Simple hand-drawn valknut made from three interlocking triangles postcard mark](Art/FinalPuzzle/PostcardMarks/Crest_Valknut_HandDrawn_v1.png)Valknut · hand-drawn v1

![Simple hand-drawn raven postcard mark](Art/FinalPuzzle/PostcardMarks/Symbol_Raven_HandDrawn_v1.png)Raven · hand-drawn v1

![Simple hand-drawn Viking longship postcard mark](Art/FinalPuzzle/PostcardMarks/Symbol_Longship_HandDrawn_v1.png)Longship · hand-drawn v1

![Simple hand-drawn eight-spoked sun-wheel postcard mark](Art/FinalPuzzle/PostcardMarks/Symbol_Sun_Wheel_HandDrawn_v1.png)Sun-wheel · hand-drawn v1

![Simple hand-drawn horned Viking helmet decoy postcard mark](Art/FinalPuzzle/PostcardMarks/Decoy_Horned_Helmet_HandDrawn_v1.png)Horned helmet · decoy v1

![Simple hand-drawn double-sided axe decoy postcard mark](Art/FinalPuzzle/PostcardMarks/Decoy_Double_Axe_HandDrawn_v1.png)Double-sided axe · decoy v1

**Decoy marks — ImageGen prompt and production note**

```
**Horned helmet · exact ImageGen prompt**
Use case: style-transfer
Asset type: tiny transparent hand-drawn fake-element mark for a printable decoy postcard
Input images: style and palette references only. Match Aunt Liv's existing postcard marks: loose dark pen outline, simple flat colored-pencil fills, slight handmade wobble, sparse detail, and the same visual weight. Do not copy the shield or raven subjects.
Primary request: Draw exactly one stereotypical Viking helmet viewed straight-on, with a simple rounded metal cap, narrow brow band, small nose guard, and exactly two large symmetrical horns curving outward and upward—one horn on each side. The two horns are essential because this is an intentionally false crest element for a decoy card, not a historically accurate helmet. It should look like Aunt Liv quickly drew it by hand in a postcard margin, not like professional heraldry.
Composition: one isolated centered icon, compact symmetrical silhouette, generous transparent margin, readable at 0.4–0.5 inches wide.
Color palette: dark blue-black/charcoal outline; flat dusty sage-blue or pale grey helmet; pale cream horns; muted terracotta brow band; tiny ochre fasteners if useful.
Constraints: genuine transparent alpha background; exactly one helmet with exactly two horns; simple line drawing with flat fills and very few internal strokes; no head, face, skull, feathers, wings, chainmail, realistic metal texture, battle damage, knotwork, 3D depth, shading, gradient, glow, shadow, shield, frame, border, text, letters, runes, scenery, extra objects, mockup, or watermark.

**Double-sided axe · attempted ImageGen prompt**
Use case: style-transfer
Asset type: tiny transparent hand-drawn fake-element mark for a printable decoy postcard
Input images: style and palette references only. Match Aunt Liv's existing postcard marks: loose dark pen outline, simple flat colored-pencil fills, slight handmade wobble, sparse detail, and the same visual weight. Use the single-bladed axe only to match line style and palette; the new subject must be unmistakably different.
Primary request: Draw exactly one double-sided axe with one straight wooden handle and a single symmetrical axe head carrying exactly two matching broad curved blades—one blade on the left and one on the right. Show it upright or on a slight diagonal so both blades remain equally visible. This is an intentionally false crest element for a decoy card. It should look like Aunt Liv quickly drew it by hand in a postcard margin, not like professional heraldry.
Composition: one isolated centered icon, compact balanced silhouette, generous transparent margin, readable at 0.4–0.5 inches wide.
Color palette: dark blue-black/charcoal outline; muted terracotta-brown handle; dusty sage-blue or pale grey blades; tiny ochre binding accent if useful.
Constraints: genuine transparent alpha background; exactly one axe, exactly one handle, and exactly two opposing blades; simple line drawing with flat fills; no third blade, spear point, hammer face, crossed weapons, realistic metal texture, battle damage, knotwork, 3D depth, shading, gradient, glow, shadow, shield, frame, border, text, letters, runes, hands, people, scenery, extra objects, mockup, or watermark.

**Production note:** ImageGen hit the account usage limit before rendering the double-sided axe. The production asset was therefore derived deterministically from `Crest_Battle_Axe_HandDrawn_v1.png` by reflecting its existing blade across the haft axis. This preserves the approved hand-drawn style without introducing a mismatched second rendering.
```

**Exact ImageGen prompts — three hand-drawn symbol elements**

```
**Raven**
Use case: style-transfer
Asset type: tiny transparent hand-drawn validation mark for a printable postcard
Input images: Images 1 and 2 are style and palette references only. Match Aunt Liv's existing Bayeux-inspired margin drawings: loose dark pen outline, simple flat colored-pencil fills, slight handmade wobble, sparse detail, no literal embroidery. Image 3 is subject reference only for the family symbol's raven; simplify it heavily and do not copy the enclosing emblem.
Primary request: Draw exactly one simple adult raven standing in side profile and facing left, with folded wings, a long heavy slightly hooked beak, a shaggy throat, strong feet, and a wedge-shaped tail. It must read clearly as a raven rather than a crow, eagle, or chick. It should look like Aunt Liv quickly drew it by hand in a postcard margin, not like professional heraldry.
Composition: one isolated centered bird, compact silhouette, generous transparent margin, readable at 0.4–0.5 inches wide; no perch or ground line.
Color palette: dark blue-black/charcoal outline; flat dusty sage-blue and muted grey body; restrained terracotta feather accents; tiny ochre eye if useful.
Constraints: genuine transparent alpha background; exactly one raven; simple line drawing with flat fills and very few internal feather strokes; no realistic plumage, knotwork, 3D depth, shading, gradient, shadow, branch, nest, moon, shield, frame, border, text, letters, runes, scenery, extra objects, mockup, or watermark.

**Longship**
Use case: style-transfer
Asset type: tiny transparent hand-drawn validation mark for a printable postcard
Input images: Images 1 and 2 are style and palette references only. Match Aunt Liv's existing Bayeux-inspired margin drawings: loose dark pen outline, simple flat colored-pencil fills, slight handmade wobble, sparse detail, no literal embroidery. Image 3 is subject reference only for the family symbol's longship; simplify it heavily and do not copy the enclosing emblem.
Primary request: Draw exactly one simple Viking longship in clear side profile, with a high curled prow and stern, one mast, and one square striped sail. Add one restrained pair of wave strokes directly beneath the hull so it reads as a ship rather than a decorative bowl. It should look like Aunt Liv quickly drew it by hand in a postcard margin, not like professional heraldry.
Composition: one isolated centered icon, compact horizontal silhouette, generous transparent margin, readable at 0.4–0.5 inches wide.
Color palette: dark blue-black/charcoal outline; muted terracotta-brown hull and sail stripe; dusty sage-blue sail and waves; tiny ochre accent if useful.
Constraints: genuine transparent alpha background; exactly one longship; simple line drawing with flat fills and very few internal strokes; no realistic wood grain, shields along the hull, oars, crew, second sail, knotwork, 3D depth, shading, gradient, shadow, coast, sky, shield, frame, border, text, letters, runes, scenery, extra objects, mockup, or watermark.

**Longship background cleanup**
Use case: background-extraction
Asset type: tiny transparent hand-drawn validation mark for a printable postcard
Input image: edit target. Preserve the longship itself exactly: its loose dark outline, terracotta hull, striped sage-blue and terracotta square sail, mast, curled prow and stern, ochre accents, and the three simple sage-blue waves.
Primary request: Remove the entire surrounding dark brown, blue-grey, and black haze or glow. Keep only the longship and its attached wave strokes on a genuinely transparent alpha background.
Composition: retain the same centered scale and generous margin.
Constraints: change only the background extraction; do not redraw, simplify, crop, recolor, sharpen, add detail, or alter the ship. No glow, shadow, vignette, backdrop, paper texture, border, text, mockup, or watermark. Every pixel outside the ship and waves must be transparent.

**Sun-wheel**
Use case: style-transfer
Asset type: tiny transparent hand-drawn validation mark for a printable postcard
Input images: Images 1 and 2 are style and palette references only. Match Aunt Liv's existing Bayeux-inspired margin drawings: loose dark pen outline, simple flat colored-pencil fills, slight handmade wobble, sparse detail, no literal embroidery. Image 3 is subject reference only for the family symbol's sun-wheel; simplify it heavily and do not copy the enclosing emblem.
Primary request: Draw exactly one simple eight-spoked Norse sun-wheel: one circular rim, a small central boss, and exactly eight evenly spaced straight spokes. Keep it bold, handmade, and immediately distinguishable from a ship's wheel or modern compass rose. It should look like Aunt Liv carefully copied it by hand in a postcard margin, not like professional heraldry.
Composition: one isolated centered icon, compact circular silhouette, generous transparent margin, readable at 0.4–0.5 inches wide.
Color palette: dark blue-black/charcoal outline; flat muted terracotta spokes and rim; small dusty sage-blue or ochre central boss.
Constraints: genuine transparent alpha background; exactly one sun-wheel with exactly eight spokes; simple line drawing with flat fills; no cardinal-direction points, arrowheads, handles, letters, numbers, runes, realistic metal, knotwork, 3D depth, bevel, shading, gradient, glow, shadow, circle around the object beyond its own rim, shield, frame, border, other symbols, scenery, mockup, or watermark. Do not turn it into a ship's wheel, compass, flower, or multi-ring mandala.
```

**Exact ImageGen prompts — six hand-drawn postcard marks**

```
**Battle axe**
Use case: style-transfer
Asset type: tiny transparent hand-drawn validation mark for a printable postcard
Input images: style and palette references only. Match Aunt Liv's existing Bayeux-inspired margin drawings: loose dark pen outline, simple flat colored-pencil fills, slight handmade wobble, sparse detail, no literal embroidery. Do not copy the cross or bow subjects.
Primary request: Draw exactly one simple single-bladed Norse battle axe with a short straight wooden handle, shown diagonally. Use a broad curved blade and an unmistakable axe silhouette. It should look like Aunt Liv quickly drew it by hand in a postcard margin, not like professional heraldry.
Composition: one isolated centered icon, compact silhouette, generous transparent margin, readable at 0.4–0.5 inches wide.
Color palette: dark blue-black/charcoal outline; muted terracotta-brown handle; dusty sage-blue or pale grey blade; tiny ochre accent if useful.
Constraints: genuine transparent alpha background; exactly one axe; simple line drawing with flat fills; no knotwork engraving, realistic metal texture, 3D depth, shading, gradient, shadow, shield, frame, border, text, letters, runes, hands, people, extra objects, mockup, or watermark.

**Round shield**
Use case: style-transfer
Asset type: tiny transparent hand-drawn validation mark for a printable postcard
Input images: style and palette references only. Match Aunt Liv's existing Bayeux-inspired margin drawings: loose dark pen outline, simple flat colored-pencil fills, slight handmade wobble, sparse detail, no literal embroidery. Do not copy the cross or bow subjects.
Primary request: Draw exactly one simple round Viking shield viewed straight-on, with a central circular boss and four broad spokes. It should look like Aunt Liv quickly drew it by hand in a postcard margin, not like professional heraldry.
Composition: one isolated centered icon, bold circular silhouette, generous transparent margin, readable at 0.4–0.5 inches wide.
Color palette: dark blue-black/charcoal outline; muted terracotta and ochre shield sections; dusty sage-blue boss or alternating section.
Constraints: genuine transparent alpha background; exactly one round shield; simple line drawing with flat fills; no wood grain, rivet counting, knotwork engraving, 3D depth, shading, gradient, shadow, second shield, frame, border, text, letters, runes, weapons, people, mockup, or watermark.

**Wolf**
Use case: style-transfer
Asset type: tiny transparent hand-drawn validation mark for a printable postcard
Input images: style and palette references only. Match Aunt Liv's existing Bayeux-inspired margin drawings: loose dark pen outline, simple flat colored-pencil fills, slight handmade wobble, sparse detail, no literal embroidery. Do not copy the cross or bow subjects.
Primary request: Draw exactly one simple adult wolf standing in side profile and facing right. Use pointed ears, a long muzzle, a shaggy neck, long legs, and a bushy lowered tail so it reads clearly as a wolf rather than a dog or fox. It should look like Aunt Liv quickly drew it by hand in a postcard margin, not like professional heraldry.
Composition: one isolated centered animal, compact horizontal silhouette, generous transparent margin, readable at 0.4–0.5 inches wide; no ground line.
Color palette: dark blue-black/charcoal outline; flat dusty sage-blue and muted grey body; tiny terracotta accent if useful.
Constraints: genuine transparent alpha background; exactly one wolf; simple line drawing with flat fills and very few internal strokes; no realistic fur, 3D depth, shading, gradient, shadow, collar, moon, trees, shield, frame, border, text, letters, runes, scenery, mockup, or watermark.

**Anchor**
Use case: style-transfer
Asset type: tiny transparent hand-drawn validation mark for a printable postcard
Input images: style and palette references only. Match Aunt Liv's existing Bayeux-inspired margin drawings: loose dark pen outline, simple flat colored-pencil fills, slight handmade wobble, sparse detail, no literal embroidery. Do not copy the cross or bow subjects.
Primary request: Draw exactly one simple traditional anchor viewed straight-on and upright, with a top ring, short crossbar, central shank, and two curved flukes. Add one short loose rope loop around the shank, kept secondary. It should look like Aunt Liv quickly drew it by hand in a postcard margin, not like professional heraldry.
Composition: one isolated centered icon, bold upright silhouette, generous transparent margin, readable at 0.4–0.5 inches wide.
Color palette: dark blue-black/charcoal outline; flat dusty sage-blue anchor; muted terracotta-brown rope; tiny ochre accent if useful.
Constraints: genuine transparent alpha background; exactly one anchor; simple line drawing with flat fills; no realistic metal, knotwork, 3D depth, shading, gradient, shadow, ship, water, shield, frame, border, text, letters, runes, scenery, mockup, or watermark.

**Drinking horn**
Use case: style-transfer
Asset type: tiny transparent hand-drawn validation mark for a printable postcard
Input images: style and palette references only. Match Aunt Liv's existing Bayeux-inspired margin drawings: loose dark pen outline, simple flat colored-pencil fills, slight handmade wobble, sparse detail, no literal embroidery. Do not copy the cross or bow subjects.
Primary request: Draw exactly one simple Norse drinking horn with a wide open mouth at upper left and a curved pointed tip sweeping down and right. Add one plain decorative band around the rim. It must read as a drinking vessel rather than a tusk or musical horn. It should look like Aunt Liv quickly drew it by hand in a postcard margin, not like professional heraldry.
Composition: one isolated centered icon, compact curved silhouette, generous transparent margin, readable at 0.4–0.5 inches wide.
Color palette: dark blue-black/charcoal outline; pale cream horn body; muted terracotta rim; small ochre accent if useful.
Constraints: genuine transparent alpha background; exactly one drinking horn; simple line drawing with flat fills and very few internal strokes; no realistic horn texture, knotwork, rope, liquid, hand, stand, animal head, 3D depth, shading, gradient, shadow, shield, frame, border, text, letters, runes, mockup, or watermark.

**Valknut**
Use case: style-transfer
Asset type: tiny transparent hand-drawn validation mark for a printable postcard
Input images: style and palette references only. Match Aunt Liv's existing Bayeux-inspired margin drawings: loose dark pen outline, simple flat colored-pencil fills, slight handmade wobble, sparse detail, no literal embroidery. Do not copy the cross or bow subjects.
Primary request: Draw exactly one simple valknut made from exactly three interlocking triangular loops. Preserve a clear over-under weave and three distinct triangles, but keep the drawing bold and uncomplicated. It should look like Aunt Liv carefully copied the symbol by hand in a postcard margin, not like professional heraldry.
Composition: one isolated centered icon, upright compact triangular silhouette, generous transparent margin, readable at 0.4–0.5 inches wide.
Color palette: dark blue-black/charcoal outline with flat muted terracotta fill; tiny ochre highlight only if needed.
Constraints: genuine transparent alpha background; exactly one valknut made from exactly three interlocking triangles; simple line drawing with flat fill; no 3D depth, bevel, shading, gradient, shadow, circle, shield, frame, border, text, letters, numbers, runes, other symbols, mockup, or watermark. Do not turn it into a triquetra, mountain, or four-triangle symbol.
```

**Superseded — polished heraldic element prompts and 1254 px studies**

The six ornate studies remain in `Art/FinalPuzzle/CrestElements/` as a record of the initial misunderstanding. They are not intended for postcard placement.

```
**Battle axe**
Use case: style-transfer
Asset type: isolated transparent postcard validation mark, part of a six-icon family crest set
Input image: style and subject reference. Match the battle-axe charge in the top-left shield field: its dimensional carved-metal relief, single broad blade, short decorated wooden haft, Norse interlace engraving, forest-green shadows, muted copper/rust ornament, and bone-silver highlights. Do not copy the shield field, border, or surrounding achievement.
Primary request: Create exactly one single-bladed Norse battle axe, isolated and fully visible, in a clean three-quarter side view close to the reference charge. It must read instantly as an axe at approximately 0.5 inch wide on a postcard.
Composition: one centered object on a square transparent canvas with generous even margin; strong compact diagonal silhouette.
Style/medium: premium dimensional sculpted heraldic relief, Norse woodcarving and engraved metal, matching the reference crest exactly.
Color palette: deep forest green #283B34 shadows, muted rust/copper #B56A2A ornament, restrained bone-silver metal highlights; no other colors.
Constraints: genuine transparent alpha background; exactly one axe; no shield, frame, field, border, ribbon, text, letters, numbers, runes, other weapons, hands, people, scenery, floor, shadow, glow, mockup, or watermark. Preserve clarity over tiny decorative detail.

**Round shield**
Use case: style-transfer
Asset type: isolated transparent postcard validation mark, part of a six-icon family crest set
Input image: style and subject reference. Match the round Viking shield charge in the top-right shield field: its dimensional carved-metal relief, circular wooden face, central metal boss, restrained Norse interlace cross-bands, forest-green shadows, muted copper/rust wood, and bone-silver highlights. Do not copy the large heater shield, field border, or surrounding achievement.
Primary request: Create exactly one round Viking shield viewed straight-on, isolated and fully visible. It must read instantly as a round shield at approximately 0.5 inch wide on a postcard.
Composition: one centered object on a square transparent canvas with generous even margin; bold circular silhouette.
Style/medium: premium dimensional sculpted heraldic relief, Norse woodcarving and engraved metal, matching the reference crest exactly.
Color palette: deep forest green #283B34 shadows, muted rust/copper #B56A2A ornament, restrained bone-silver metal highlights; no other colors.
Constraints: genuine transparent alpha background; exactly one round shield; no larger shield behind it, frame, field, border, ribbon, text, letters, numbers, runes, weapons, people, scenery, floor, shadow, glow, mockup, or watermark. Preserve clarity over tiny decorative detail.

**Wolf**
Use case: style-transfer
Asset type: isolated transparent postcard validation mark, part of a six-icon family crest set
Input image: style and subject reference. Match the wolf charge in the middle-left shield field: its alert standing side profile, dimensional carved-metal relief, engraved fur, forest-green shadows, muted copper/rust ornament, and bone-silver highlights. Do not copy the shield field, border, or surrounding achievement.
Primary request: Create exactly one adult Norse heraldic wolf standing in a clean full-body side profile, facing right, isolated and fully visible. Strong pointed ears, long muzzle, deep chest, straight legs, bushy lowered tail. It must read instantly as a wolf—not a dog or fox—at approximately 0.5 inch wide on a postcard.
Composition: one centered animal on a square transparent canvas with generous even margin; compact horizontal silhouette; no ground line.
Style/medium: premium dimensional sculpted heraldic relief, engraved metal and carved detail, matching the reference crest exactly.
Color palette: bone-silver wolf with deep forest green #283B34 shadows and restrained muted rust/copper #B56A2A accents; no other colors.
Constraints: genuine transparent alpha background; exactly one wolf; no shield, frame, field, border, ribbon, text, letters, numbers, runes, collar, harness, moon, trees, ground, scenery, shadow, glow, mockup, or watermark. Preserve clarity over tiny fur detail.

**Anchor**
Use case: style-transfer
Asset type: isolated transparent postcard validation mark, part of a six-icon family crest set
Input image: style and subject reference. Match the anchor charge in the middle-right shield field: its dimensional carved-metal relief, traditional symmetrical anchor shape, short wrapped rope, engraved surfaces, forest-green shadows, muted copper/rust ornament, and bone-silver highlights. Do not copy the shield field, border, or surrounding achievement.
Primary request: Create exactly one traditional maritime anchor viewed straight-on, upright and symmetrical, with a compact short rope wrapped once around the shank. Keep the stock, ring, shank, crown and two flukes unmistakable. It must read instantly as an anchor at approximately 0.5 inch wide on a postcard.
Composition: one centered object on a square transparent canvas with generous even margin; bold upright silhouette.
Style/medium: premium dimensional sculpted heraldic relief, Norse woodcarving and engraved metal, matching the reference crest exactly.
Color palette: bone-silver metal, deep forest green #283B34 shadows, muted rust/copper #B56A2A rope and restrained ornament; no other colors.
Constraints: genuine transparent alpha background; exactly one anchor; rope is attached detail, not a second symbol; no shield, frame, field, border, ribbon, text, letters, numbers, runes, ship, water, scenery, floor, shadow, glow, mockup, or watermark. Preserve clarity over tiny decorative detail.

**Drinking horn**
Use case: style-transfer
Asset type: isolated transparent postcard validation mark, part of a six-icon family crest set
Input image: style and subject reference. Match the drinking-horn charge in the bottom-left shield field: its curved horn silhouette, ornate rim, short wrapped cord, dimensional carved relief, forest-green shadows, muted copper/rust ornament, and bone-silver body. Do not copy the shield field, border, or surrounding achievement.
Primary request: Create exactly one traditional Norse drinking horn, open mouth at upper left and curved pointed tip sweeping to the lower right, isolated and fully visible. Include one broad interlace-decorated metal rim and a short restrained cord wrap. It must read instantly as a drinking horn—not a tusk or musical horn—at approximately 0.5 inch wide on a postcard.
Composition: one centered object on a square transparent canvas with generous even margin; compact curved diagonal silhouette.
Style/medium: premium dimensional sculpted heraldic relief, Norse woodcarving and engraved metal, matching the reference crest exactly.
Color palette: bone-silver horn body, deep forest green #283B34 shadows, muted rust/copper #B56A2A ornament; no other colors.
Constraints: genuine transparent alpha background; exactly one drinking horn; no liquid, hand, stand, animal head, shield, frame, field, border, ribbon, text, letters, numbers, runes, scenery, floor, shadow, glow, mockup, or watermark. Preserve clarity over tiny decorative detail.

**Valknut**
Use case: style-transfer
Asset type: isolated transparent postcard validation mark, part of a six-icon family crest set
Input image: style and subject reference. Match the valknut charge in the bottom-right shield field: a correct three-interlocking-triangle construction rendered as dimensional carved heraldic relief, with muted copper/rust faces, bone-silver bevel highlights, and deep forest-green recesses. Do not copy the shield field, border, or surrounding achievement.
Primary request: Create exactly one correct valknut symbol composed of exactly three interlocking triangles, centered, balanced, and immediately legible. Preserve the continuous over-under weave logic and three distinct triangular loops. It must remain unmistakable at approximately 0.5 inch wide on a postcard.
Composition: one centered compact symbol on a square transparent canvas with generous even margin; upright triangular silhouette.
Style/medium: premium dimensional sculpted heraldic relief, Norse carved-metal ornament, matching the reference crest exactly.
Color palette: muted rust/copper #B56A2A principal faces, restrained bone-silver bevel highlights, deep forest green #283B34 recesses; no other colors.
Constraints: genuine transparent alpha background; exactly one valknut made from exactly three interlocking triangles; no circle, shield, frame, field, border, ribbon, text, letters, numbers, runes, other symbols, scenery, floor, shadow, glow, mockup, or watermark. Do not turn it into a triquetra, knot, mountain, or four-triangle symbol. Preserve clarity over tiny texture.
```

**Resolved, 20 Sept 2026 — round shield redesigned.** The v2 mark removes all spokes and quartering. It is now a plain ringed round shield with a large domed boss and one curved two-colour seam, while the sun-wheel keeps its eight radial spokes. The production file is `Art/FinalPuzzle/PostcardMarks/Crest_Round_Shield_HandDrawn_v2.png`; the full ImageGen source is retained beside it under `PostcardMarks/Sources/`.

**Exact ImageGen prompt — round shield v2**

```
Use case: precise-object-edit
Asset type: tiny transparent hand-drawn validation mark for a printable postcard, legible at about 0.4 inch wide
Input images: Image 1 is the shield to redesign. Image 2 is the sun-wheel that the new shield must remain visually distinct from.
Primary request: Redesign only the round shield so it reads immediately as a plain Viking round shield and cannot be confused with the eight-spoked sun-wheel. Keep the existing loose handmade pen-and-colored-pencil visual language.
Subject: exactly one round shield shown face-on, with a thick outer rim, a large domed central metal boss, and a simple solid wooden face divided into only two broad color areas by one slightly irregular curved seam.
Style/medium: loose dark blue-black hand-drawn outline, flat muted ochre and terracotta colored-pencil fills, subtle handmade wobble, sparse detail.
Composition/framing: centered compact silhouette with generous genuine transparent margin; strong and readable when reduced to 0.4 inch.
Color palette: match the existing mark set—dark blue-black outline, muted ochre, terracotta, and a restrained grey-blue boss.
Constraints: no radial spokes, no cross, no quarters, no wheel structure, no eight-fold symmetry, no compass points, no runes, knotwork, weapons, frame, text, shadow, gradient, 3D scene, background, or extra objects. Genuine transparent alpha background. 300 × 300 PNG.
```

~~Still open: the per-card assignment of the nine real elements, final printed size, and the mark's physical treatment on each card (PZ-013).~~ **Closed, 20 Sept 2026:** per-card assignment, size and placement are all decided and applied — see [Element marks assigned and printed]. All eleven hand-drawn production marks now exist: nine real and two fake. The earlier polished six-mark set, shield v1, and the earlier Mjölnir/crown fake choices are superseded.

HI

### History

## Starting state

Not recorded yet.

## Reset

Not recorded yet.

## Replacement

Not recorded yet.
