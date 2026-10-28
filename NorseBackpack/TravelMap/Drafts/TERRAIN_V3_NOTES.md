# Aud terrain revision v3 — 16 Oct 2026

## Request addressed
Previous preview under-delivered the approved concept: one repeated tree and plain line-based water. Designer requested mixed tree shapes and richer terrain, grid under trees, corrected river-bridge perspective, and 30% larger icons except bridges.

## Output
- `render_baseline/Aud_Style_Draft_v3.pdf` / `style-preview-v3.png`.
- `render_baseline/Aud_Style_Comparison_v3.pdf` / `style-comparison-v3.png`.
- `render_terrain_v3.py` isolated renderer, importing previous renderer helpers without changing them.
- Three new assets in `../../Art/MapIcons/`: Conifer_v3, Birch_v3 and Bridge_River_v3.

## Method
Mixed woodland uses broadleaf, birch and conifer assets, varied size and deterministic irregular spacing. Areas remain clipped to JSON polygons. Textures leave clearance around existing landmark centers. River uses teal banks, pale short current strokes and sparse bank reeds. Field furrows curve across the existing polygon; paths carry small brown surface marks.

Grid and symbol-layer blocks are reordered only in the builder function held in memory. The on-disk live builder is unchanged. Grid now draws before terrain and symbols; labels still draw last.

Map landmark widths/heights and the gate span are multiplied by exactly 1.3; woodland and marsh motifs also use 1.3. Bridges retain a 16pt deck travel span. Legend swatches fit their original rows. Map positions are unchanged.

The river bridge uses newly generated artwork with a rigid uniform scale and rotation about its deck midpoint, replacing the vertical shear that distorted the previous bridge. This preserves artwork proportions; upright details rotate with the asset slightly. It is a visual draft, not a physical crossing proof.

## Checks
20 draft features loaded. Hashes checked before and after for draft JSON, live aud_layer.py, live aud_features.json and live build_trail_maps_pdf.py; unchanged. Source grid block ordering asserted. Existing crossing angles retained. Both PDFs rendered for full-page visual review. Poppler fallback-font warnings persist; visible labels readable. Physical print check remains outstanding.

## Exact ImageGen prompts
Each asset used two style references: Aud_Terrain_Concepts_Yellow_v1.png and Aud_Icon_Concepts_v1.png. Built-in ImageGen; separate call per asset; transparent background requested; source PNGs retained unmodified.

### Aud_Conifer_v3.png

```text
Create one isolated evergreen fir tree icon matching the WOOD sample of the supplied terrain sheet. Narrow triangular silhouette with three broad layered drooping tiers, visible short brown trunk, dark olive #47603C contour, muted green #788958 fill. Elevated perspective, crisp vintage hand-drawn outline, minimal detail. Transparent background. No ground, shadow, halo, labels, gradients or other trees.
```

### Aud_Birch_v3.png

```text
Create one isolated small birch tree icon matching the WOOD sample of the supplied terrain sheet. Airy rounded crown with three large lobed foliage masses, clearly visible slim pale ivory trunk with two tiny dark bark strokes and forked branches. Dark olive #47603C contour, sage-olive #98A174 foliage. Different silhouette from a broad dense oak. Elevated perspective, crisp vintage hand-drawn outline, minimal detail. Transparent background. No ground, shadow, halo, labels, gradients or other trees.
```

### Aud_Bridge_River_v3.png

```text
Create ONE illustrated timber bridge icon for a map viewed from nearly overhead, retaining a slight three-quarter perspective. Match the purple and ivory bridge style of reference image 2. IMPORTANT: deck travel axis must descend from TOP LEFT to BOTTOM RIGHT at 60 DEGREES from horizontal, not a conventional 30-degree isometric bridge. Far deck end center at about (35% canvas width,25% canvas height), near deck end center at (65% canvas width,77% canvas height). A short broad rectangular deck, only four broad cross-planks, low side rails, four SHORT posts vertically upright on the page. Deck is foreshortened with a clearly visible broad surface: travel length only twice deck width, not a long thin catwalk. Dark muted purple #614773 outline and opaque ivory #F4EEDD interiors. Crisp clean simplified hand-drawn cartographic illustration. No water or banks because map supplies them. Actual transparent background. No ground, shadows, glow, gradients, labels or extra objects. Do not tilt a conventional isometric image; draw the bridge natively for this screen direction.
```

