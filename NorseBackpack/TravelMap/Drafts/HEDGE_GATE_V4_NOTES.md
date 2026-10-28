# Aud hedge and gate v4 — 16 Oct 2026

## Scope and outputs
Hedge/gate refinement only; v3 woodland, water, roads, landmarks and bridges retained. Live map and geometry unchanged.
- render_baseline/Aud_Hedge_Gate_Draft_v4.pdf and hedge-gate-map-v4.png.
- render_baseline/Aud_Hedge_Gate_Detail_v4.pdf and hedge-gate-detail-v4.png: enlarged previous/revised field corner and asset samples.
- render_hedge_gate_v4.py reproduces the map; --detail builds the close-up.

## Changes
The previous hedge stamped horizontal strips down a vertical curve. V4 overlaps larger irregular leaf clumps aligned with the actual smoothed hedge tangent. A low connecting under-stroke prevents visual breaks. The complete hedge layer is clipped out of a 4.8pt radius around the existing gate location, so overlap cannot fill the passage.

The new open gate has a broad two-rail leaf and a separate latch post. It is uniformly scaled and rigidly rotated around measured post-base anchors; no shear. The passage midpoint stays at the JSON gate location. Upper-frame clearance slightly reduces its maximum artwork size to avoid clipping the swung-open leaf; other icons remain at the v3 size. Gate orientation still derives from the original crossing_angles function.

## Checks and limits
20 features loaded. Draft JSON, live aud_layer.py, aud_features.json and map builder hashes checked before/after; unchanged. Both PDFs rendered and visually inspected. Poppler fallback-font warnings persisted; labels readable. No physical print proof. Soft generated halos remain, bounded by source-image clipping.

## Exact ImageGen prompts
Built-in ImageGen, separate call per asset. Style references: Aud_Icon_Concepts_v1.png and Aud_Terrain_Concepts_Yellow_v1.png. Transparent backgrounds requested; source files copied without pixel modification.

### Aud_Gate_Open_v4.png

```text
Create ONE isolated OPEN WOODEN FIELD GATE map icon in the vintage hand-drawn style of the supplied purple-and-ivory icon sheet. This must read as a gate with an OPEN PASSAGE. Two stout SHORT posts stand vertically upright on the page. The line between their bases descends STEEPLY from upper-left to lower-right, almost vertically, about 65–70 degrees from horizontal: upper post base around (43% width,30% height), lower post base around (62% width,77% height). Gate leaf is hinged on the UPPER post and swung fully OPEN to its LEFT so the broad gate face is visible out to the left side of the icon, leaving a very clear empty gap to the lower post. The open gate leaf has TWO broad horizontal rails and one diagonal brace, no pickets and no dense planks. Keep the wood posts squat and the leaf broad; do not make a tall palisade or fence panel. Elevated three-quarter view with practical map readability. Dark muted purple #614773 outline, warm ivory #F4EEDD opaque wood interiors. Actual TRANSPARENT background; no halo, shadows, gradients, paper, labels, plants, ground, hedge or surrounding scene. All artwork within generous margins. Do not draw a closed gate. Do not rotate or shear a conventional front-facing gate.
```

### Aud_Hedge_Clump_v4.png

```text
Create ONE isolated compact low hedgerow bush-cluster map texture in the same style as the HEDGE sample of the supplied yellow terrain sheet. Three irregular joined leafy mounds with a broad uneven crown and scalloped edges, seen slightly from above; outline dark olive #496038, foliage medium olive #81905C with a few simple darker leaf strokes. Short squat rounded silhouette, roughly twice as wide as tall. Clearly a dense low hedge, not a tree: no trunk. This will be repeated and rotated along a map path with overlaps to make one continuous curving hedge, so keep texture natural and asymmetric, avoid separate disconnected bushes and avoid a scallop border or geometric circles. Crisp thick but restrained hand-drawn outline, flat colour. Actual transparent background, no yellow rectangle, no glow, shadows, gradients, label, paper or scenery.
```

