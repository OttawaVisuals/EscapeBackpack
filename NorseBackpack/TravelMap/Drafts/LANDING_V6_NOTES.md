# Aud landing v6 — 16 Oct 2026

## Request and outputs
Designer requested a larger landing and a boat positioned in the water.
- render_baseline/Aud_Landing_Draft_v6.pdf and landing-map-v6.png.
- render_baseline/Aud_Landing_Detail_v6.pdf and landing-detail-v6.png.
- render_landing_v6.py: isolated renderer; --detail builds before/after.

## Placement
The source JSON port is at (247.8,760.43), inland near the upper map edge. The nearest coast point would put the enlarged artwork too close to the frame. A draft-only shoreline attachment at (220.38,752.98), on the existing coastline vertex, is used instead. The jetty landward end is anchored there; the boat is on the northwest sea side. The source JSON is retained unchanged; this adjustment is a renderer placement override, not an approved puzzle-route change.

Visible art targets 26pt width versus the previous 15.6pt bounding width; upper-frame clearance can constrain it slightly. Artwork is uniformly scaled without shear or rotation. Decorative Breidafjordur caption shifted west in scratch config to avoid overlap. Legend uses the new asset.

Six visually selected hull-perimeter samples map to sea, checked against the exported coastline polygons. The close-up and full map were visually inspected. Source hashes checked unchanged for JSON, live renderer, live feature layer, live builder and exported base. 20 draft features retained. Physical print test outstanding. Poppler fallback-font warnings persist; labels readable.

## Exact asset prompt
Built-in ImageGen edit/reference generation using Aud_Landing_Boat_v2.png as style reference; transparent background requested. Saved unmodified as Art/MapIcons/Aud_Landing_Shore_v6.png.

```text
Create ONE isolated illustrated LANDING JETTY WITH MOORED ROWBOAT for a Norse game map. Match the reference icon's dark muted purple #614773 outline and warm ivory #F4EEDD interiors, confident simple vintage hand-drawn cartography, few broad details. New orientation is essential: the jetty's LANDWARD end is at the LOWER RIGHT of the icon and its WATERWARD end is at the UPPER LEFT. Deck travel axis runs diagonally from lower-right toward upper-left at roughly 45 degrees to horizontal. View slightly from above; all mooring posts must remain vertically upright. A short broad jetty deck of three or four planks with two squat mooring posts. A small open wooden rowboat with two bench seats is moored to the LEFT / LOWER-LEFT side of the jetty, clearly separate from its landward end. The boat is fully visible and the hull follows the same diagonal. Keep the silhouette compact, suitable at about 25 mm across on a printed map. No shoreline, land, rocks, ground patch, trees, building, water fill or ripple strokes: the map itself will supply the sea, and we must position every part correctly against it. No people, sail, oars, letters, border, drop shadow, gradients or glow. Actual transparent background outside objects; opaque ivory wood. The reference is STYLE ONLY; do not copy its old jetty direction.
```

