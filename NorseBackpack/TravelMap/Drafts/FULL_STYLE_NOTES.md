# Aud full-style v2 proof — 16 Oct 2026

## Deliverables
- `render_baseline/Aud_Full_Style_Draft_v2.pdf` and `full-style-preview-v2.png`.
- `render_baseline/Aud_Full_Style_Comparison_v2.pdf` and `full-style-comparison-v2.png`: original draft versus illustrated version, plus artwork samples on yellow.
- `render_full_style.py`: isolated full-style renderer; run normally, render its PDF to `full-style-preview-v2.png`, then run with `--comparison`.
- New individual assets and exact built-in ImageGen prompts: `../../Art/MapIcons/FULL_STYLE_GENERATION.md`.

## Changes from first proof
Every draft landmark/crossing now uses an illustrated PNG, including chapel, ruin, gate and the two bridge views. Wood, hedge and marsh use generated tree/bush/reed artwork. Road, water, field and ditch remain paths driven by the JSON; no landmark or vegetation falls back to basic geometric artwork.

Crossing artwork has measured deck-end/post-base anchors. A placement shear matches the existing crossing_angles direction while retaining upright posts. The source PNGs are unchanged. The legend uses untransformed artwork sized to its row.

## Validation
20 JSON features loaded; draft JSON, live aud_layer.py and live aud_features.json hashes checked before and after; unchanged. Existing crossing-angle results preserved. Asset usage recorded in `render_full_style/validation.json`. Both final one-page PDFs rendered and visually inspected. Poppler emitted fallback-font warnings for Symbol and ArialUnicode; visible labels were readable.

## Remaining limits
Fine detail is small at the retained symbol size classes. Steep bridge/gate perspectives become narrow and need a print check before approval. Some generated soft halos remain, limited by renderer clipping. Top-edge locations and all source geometry were retained. The supplied partial draft has no wall, ford, moor or footpath, so it cannot demonstrate those styles. No physical print test or live-map integration.

