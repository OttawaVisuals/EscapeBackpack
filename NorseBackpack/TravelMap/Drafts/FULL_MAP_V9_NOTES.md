# Aud full-map proof v9 — 16 Oct 2026

## Input and deliverables
User-supplied 102-feature JSON preserved byte-for-byte as `aud_features_full_2026-10-16.json`.
Renderer: `render_full_map_v9.py`.
Outputs: `render_full_map_v9/Aud_Full_Map_v9.pdf`, matching PNG and `validation.json`.
This is a full-layout draft proof. Live renderer/map files are unchanged.

## Ticket marker mapping
- `coin1` at (565.07,749.89): ticket's original camel PNG.
- `Coincorretc` at (573.15,230.98): Fehu rune, using `draw_fehu` imported from the actual ticket builder. The misspelling is preserved in source JSON and treated as the intended correct marker.
- `Coin2` at (374.66,127.89): ticket's original fleur PNG.
The two decoys were assigned in source order. Marker labels and correctness are not printed on the player map. All symbols remain at their source coordinates.

## Full-layout support
Approved styling carried forward for all features. Standalone well and ford artwork plus wall segment added. Standing stones and cairns use previously generated PNGs. Moor, lake and path styles added to this full-layout renderer, with matching legend samples. Bridges/gates use the established direction calculations and existing artwork placement; each orientation still warrants print review.

Landings attach to coastline: first keeps approved v6 override; remaining three attach to nearest coast points. Six hull samples per landing verified on sea. Source port positions are retained in JSON. Four edge-adjacent landmark illustrations are fitted inward to avoid crop, recorded in validation.json; point/path coordinates themselves remain unchanged. ÍSLAND/Iceland country label moved west into clear land in scratch config; bay caption retains its prior scratch placement.

## Validation and limitations
All 102 source features loaded. Three markers verified to be exactly camel/fehu/fleur; marker source labels absent from PDF text. SHA-256 before/after checks leave source JSON, live renderer, live features, live builder and exported base unchanged. One-page PDF rendered and visually inspected; decorative country-label overlap corrected. Poppler Symbol/ArialUnicode fallback warnings persisted; labels readable.

Full-map crossing totals are 12 bridge symbols, 5 fords and 7 gates, NOT a route solution. The new route has not been hand-walked or confirmed against the current museum-ticket directions; no claim that the previous 521 answer is preserved. Physical print proof outstanding.

## Exact new asset prompts
Built-in ImageGen, separate calls. References: Aud_Icon_Concepts_v1.png and Aud_Terrain_Concepts_Yellow_v1.png. Transparent backgrounds requested; PNGs copied without pixel edits into Art/MapIcons.

### Aud_Well_Full_v9.png

```text
One isolated small stone well for a printed Norse map. Round low stone rim with a dark opening, two wooden upright posts supporting a small pitched roof. Match the WELL in supplied style sheet: muted purple #614773 clean bold hand-drawn lines, opaque warm ivory #F4EEDD interiors, simple elevated three-quarter perspective. Very few stone divisions and roof planks. Recognisable at 9mm across. Actual transparent background, no scenery, ground, shadow, halo, gradients, text or border.
```

### Aud_Ford_Full_v9.png

```text
One isolated map FORD symbol in the same illustrated style as the FORD in supplied reference: five broad irregular low stepping stones in a short row. Row axis goes from upper-left to lower-right diagonally about 30 degrees from horizontal. Stones seen slightly from above, ivory #F4EEDD tops and dark muted purple #614773 clean outlines; almost no raised side faces, so the small icon can be rotated to fit a crossing. NO water, river, banks, building, bridge, ground, shadow, glow, labels or gradients. The map will supply water. Actual transparent background.
```

### Aud_Wall_Clump_v9.png

```text
One isolated SHORT stone-wall texture segment matching STONE WALL on the supplied terrain sheet. Five irregular broad grey stones in a low dry-stone wall, slight elevated perspective. Grey-green #A6A897 faces, charcoal-grey #666354 clean dark outlines, broad simple top facets. Short squat horizontal silhouette about three times as wide as tall. This will overlap and rotate along a map path, so avoid a finished scene or large end posts. Opaque stones, actual transparent background. No grass or ground patch, no scenery, shadow, glow, gradients, text or border.
```

