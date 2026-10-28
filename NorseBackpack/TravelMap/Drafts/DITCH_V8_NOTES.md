# Aud dry ditch v8 — 16 Oct 2026

Designer approved a shallow dry earth channel with rough brown banks, a recessed dark centre and sparse grass, replacing the technical line and ticks.

## Deliverables
- render_baseline/Aud_Ditch_Draft_v8.pdf and ditch-map-v8.png.
- render_baseline/Aud_Ditch_Detail_v8.pdf and ditch-detail-v8.png.
- render_ditch_v8.py isolated renderer; --detail builds before/after.

## Method
Existing ditch path sampled without changing its coordinates or smoothing flag. Irregular offset banks, shaded bank and narrow dark bed are drawn around that centreline. Broken earth highlights and existing Field_Grass_v5 PNG add texture. Grass/highlights are suppressed near crossings; bridge art is unchanged and draws over the channel. The legend uses the same ditch drawing routine.

No new bitmap asset or ImageGen call needed. Other v7 map styling, six enlarged landmarks, landing shore placement, grid order, hedge and gate are retained.

## Validation
20 draft features. Before/after SHA-256 checks for JSON, live layer, live features, live builder and exported base unchanged. Existing crossing_angles reused. Both final PDF pages rendered and visually inspected. Poppler fallback-font warnings persisted; labels readable. No physical print proof.

