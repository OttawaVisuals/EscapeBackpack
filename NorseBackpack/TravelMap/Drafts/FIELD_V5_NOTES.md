# Aud field v5 — 16 Oct 2026

Field-only update requested by the designer. Other v4 artwork and the JSON geometry are retained.

## Deliverables
- render_baseline/Aud_Field_Draft_v5.pdf and field-map-v5.png.
- render_baseline/Aud_Field_Detail_v5.pdf and field-detail-v5.png.
- render_field_v5.py: isolated renderer. Run normally for the map; --detail for before/after.

## Treatment and validation
A light wheat wash, curved paired furrows and sparse illustrated dry grass replace the horizontal stripes. Everything is clipped to the original field polygon. Furrow ink is excluded from a 26 x 20pt ellipse centered on the unchanged farmhouse. The legend uses the same new field treatment.

20 source features loaded. Draft JSON and the three live renderer/map source files were checked by SHA-256 before/after and are unchanged. Final map and close-up PDFs rendered and visually inspected; no layout defects observed. Poppler fallback-font warnings persist; labels readable. Physical print proof not performed.

## Asset prompt
Built-in ImageGen; reference Aud_Terrain_Concepts_Yellow_v1.png; transparent background requested. Copied unmodified to Art/MapIcons/Aud_Field_Grass_v5.png.

```text
Create ONE isolated tiny dry field-edge grass tuft for an illustrated Norse game map, matching the FIELD sample in the supplied terrain style sheet. Five short uneven ochre-brown blades with one small seed stem, squat broad silhouette, dark umber #927044 outlines with muted wheat #B69561 interiors. Confident simple vintage hand-drawn cartography, few broad strokes readable at tiny size. No green bush, roots, soil patch, backdrop, shadow, glow, gradients, labels, frame or scene. Actual transparent background, crisp edges. Intended for sparse repetition along a field boundary on yellow land #EFE3C4.
```

