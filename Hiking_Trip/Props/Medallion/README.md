# Hiking keepsake - one-piece medallion v1

Current model: [Hiking_Medallion_OnePiece_v1.stl](STL/Hiking_Medallion_OnePiece_v1.stl).
[Complete print package](Hiking_Medallion_Print_Files_v1.zip).
Import in millimetres at 100%. One connected solid; no glue or assembly.

## Selected design
The designer selected mountains, a winding trail and pine trees on 2026-10-05.
The generated front concept uses navy/yellow low relief and is traced into a
flat manufacturing profile. Illustration texture and lighting are not geometry.
The back is identical to the approved Space back: ADVENTURE / COMPLETE around
the compass, with ESCAPE BACKPACK in larger, widely spaced 4.0 mm capitals.
The smallest brand-letter separation is 0.831 mm. Main words have 4.6 mm capitals.
Back engraving is 0.4 mm deep. The front-art interpretation awaits physical review.

## Print setup
- Diameter: 50 mm. Body: 3.8 mm. Front relief: 0.6 mm. Total: 4.4 mm.
- Print **engraved back DOWN, hiking front UP**, at full size.
- Shared-kit assumption: stock 0.4 mm nozzle on a Prusa i3 MK3S+.
  Use the profiles for the actual printer and material.
- Use 0.20 mm layers, including the first layer; supports and raft OFF.
- Dark-blue body, yellow front: add one manual colour change immediately before
  layer 20 / Z = 4.00 mm. The body ends at 3.80 mm. Single-colour printing needs
  no pause. STL files contain neither colour assignments nor G-code.
- Check the first two layers and short bridges across the engraving in the slicer.
  First-layer spreading can still close grooves. Larger lettering is not proof
  of print quality.

## Lettering test first
[Back-only trial](STL/Hiking_Back_Lettering_Test_1.2mm_v1.stl): the same back on a
50 mm disk, 1.2 mm thick. Print engraved back DOWN, at 100%, with the actual
printer/material settings. At 0.20 mm it reproduces the first six body layers
and needs no colour change.

## Validation and rebuilding
Both exported STLs pass closure, winding, connectivity, non-degenerate facet
and positive-volume checks; mesh volumes match the analytic polygon layers.
CAD preview and profiles are screen-reviewed. **No printer-profile slice or
physical print test is recorded.**

Rebuild: `python Hiking_Trip/Props/Medallion/build_medallion_v1.py` from the
repository root. Shared geometry: `Tools/medallion_cad.py`.
Requires numpy, Pillow, OpenCV, matplotlib, Shapely 2.1+ and Windows Arial fonts.

- `Hiking_Medallion_v1_Preview.png`: exact front/back geometry preview.
- `Front_Relief_v1.svg`, `Back_Engraving_v1.svg`: 50 mm profiles.
- `geometry_report_v1.json`: dimensions and measured clearances.
- `mesh_check_v1.json`, `lettering_test_mesh_check_v1.json`: mesh checks.
- `sources/Hiking_Front_Concept_v1.png`: built-in ImageGen front concept.
- `sources/front_prompt_v1.txt`: exact prompt and reference.
- `front_trace_mask_v1.png`: manufacturing-trace intermediate.

Official references: [colour change](https://help.prusa3d.com/article/color-change_1687),
[first-layer compensation](https://help.prusa3d.com/article/elephant-foot-compensation_114487).
