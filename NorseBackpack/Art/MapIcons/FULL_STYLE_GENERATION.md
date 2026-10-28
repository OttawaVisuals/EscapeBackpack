# Aud full-style assets — 16 Oct 2026

Generated with built-in ImageGen, one call per asset. Two style references: Aud_Icon_Concepts_v1.png and Aud_Terrain_Concepts_Yellow_v1.png. Original assets retained.

## Exact shared prompt
```text
Create ONE isolated game-map icon, not a sheet or scene. Use supplied images as STYLE REFERENCES only: the purple-and-ivory sheet defines landmarks; the yellow terrain sheet defines vegetation. Match the approved vintage hand-drawn illustrated cartography, strong confident outlines, very simple broad details that survive 5–7 mm print size, slightly elevated three-quarter perspective. Actual transparent background outside the silhouette. No paper, checkerboard, label, lettering, border, gradient, glow, drop shadow or diffuse coloured halo. Flat opaque interiors. Center with ample margins. Generate only this subject: 
```

Append the corresponding subject below to the shared prompt:

## Aud_Chapel_v2.png

A small intact chapel matching the reference chapel: one pitched roof, small prominent cross above its roof, dark door, one side window. Dark muted purple #614773 lines, warm ivory #F4EEDD interior. Very few roof strokes. No belfry or extra scenery.

## Aud_Ruin_v2.png

A roofless ruined building matching the reference ruin: broken low irregular stone walls, an incomplete doorway, a short taller broken wall behind. Dark muted purple #614773 lines, warm ivory #F4EEDD interior. Clearly broken masonry, no intact roof and no cross. No extra scenery.

## Aud_Bridge_Steep_v2.png

A short timber footbridge matching the reference bridge with four broad planks, two side rails, four short posts kept vertically UPRIGHT. Dark muted purple #614773 outlines, ivory #F4EEDD deck. The deck travel axis runs STEEPLY from TOP LEFT to BOTTOM RIGHT, approximately 60 degrees down from horizontal in the image. View from above so both ends are visible and their midpoint is the icon center. The image itself must not be tilted: posts stay vertical while the bridge is drawn in this specific perspective. No river, banks, rocks, vegetation or ground. Open transparent surroundings.

## Aud_Bridge_Shallow_v2.png

A short timber footbridge matching the reference bridge with four broad planks, two side rails, four short posts kept vertically UPRIGHT. Dark muted purple #614773 outlines, ivory #F4EEDD deck. The deck travel axis runs SHALLOWLY from TOP LEFT to BOTTOM RIGHT, approximately 28 degrees down from horizontal in the image. View from above so both ends are visible and their midpoint is the icon center. Posts remain vertical. No river, banks, rocks, vegetation or ground. Open transparent surroundings.

## Aud_Gate_Steep_v2.png

A compact open wooden gate matching the reference gate: two sturdy vertically UPRIGHT posts with a gate leaf swung open between them, two broad rails and one diagonal brace. Dark muted purple #614773 outlines, ivory #F4EEDD interior. The imaginary fence axis joining the bases of the two posts runs steeply from TOP LEFT to BOTTOM RIGHT, 68 degrees down from horizontal in the image. One post is behind and left, the other ahead and right. Keep actual posts vertically upright, not rotated diagonally. Gate leaf hinges to the rear-left post, swings away from the passage. No fence extensions, bushes, river, ground or scenery.

## Aud_Tree_v2.png

One small rounded leafy birch-like tree matching the WOOD sample, seen in elevated three-quarter view. Broad irregular lobed canopy with two foliage masses, dark olive outline #47603C, medium muted green fill #859367, short visible brown trunk and two simple branches. Few internal strokes. No forest patch, background, shadow, roots, ground or extra objects.

## Aud_Hedge_Bush_v2.png

One low broad rounded hedge bush matching the HEDGE sample, seen slightly from above. Three joined irregular lobed leaf masses, dark olive outline #496038 and medium green fill #81905C. Compact horizontal silhouette, few interior strokes. No visible tree trunk, ground, scenery or shadow. Intended to repeat along a curving hedge.

## Aud_Marsh_Reeds_v2.png

One small marsh reed tuft matching the MARSH sample: five broad tapered blades and two short visible stems, dark teal-green #386D66, with two short flat muted-teal water strokes at its foot. Crisp simple silhouette seen slightly from above. No enclosing water patch, ground, scenery, background or shadow.

## Renderer use
The assets are placed by TravelMap/Drafts/render_full_style.py. JSON geometry is authoritative. Trees, hedge bushes and reeds are repeated within existing geometry. Crossing artwork is placed with vertical shear to align measured deck/post-base anchors with the existing crossing_angles directions while keeping posts upright. This is a placement transform; source PNGs are unchanged. Some generated soft halos remain, limited by renderer clipping. Print-size readability and steep-crossing appearance need a physical proof.

