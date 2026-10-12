# Norse keepsake - one-piece medallion v3

Current model: [Norse_Medallion_OnePiece_v3.stl](STL/Norse_Medallion_OnePiece_v3.stl).
[Complete print package](Medallion_Print_Files.zip).
Import in millimetres at 100%. One connected solid; no glue or assembly.

## What changed
At the designer's request on 2026-10-05, the back now uses the approved Space
medallion layout. "ESCAPE BACKPACK" has 4.0 mm capital height, Arial Regular
outlines, and wider spacing. The closest brand-letter pair is 0.831 mm apart.
The main words have 4.6 mm capital height. Text, compass and border are engraved
0.4 mm deep. Minimum text-to-border clearance is 1.321 mm.

The raven, shield, feather channels and ornaments on the front are retained
from v2. The build compares the top front profile extracted from both exported
STLs and requires their symmetric difference to be effectively zero. The
existing top-side body groove is also retained. Earlier v2 files remain at
their original paths; [README_v2.md](README_v2.md) records that revision.

## Print setup
- Diameter: 50 mm. Body: 3.8 mm. Front relief: 0.6 mm. Total: 4.4 mm.
- Print **engraved back DOWN, raven front UP**, at full size.
- Shared-kit assumption: stock 0.4 mm nozzle on a Prusa i3 MK3S+.
  Use the profiles for the actual printer and material.
- Use 0.20 mm layers, including the first layer; supports and raft OFF.
- Dark-blue body, yellow front: add one manual colour change immediately before
  layer 20 / Z = 4.00 mm. The body ends at 3.80 mm. Single-colour printing needs
  no pause. STL files contain neither colour assignments nor G-code.
- Review the first two layers and the engraving roof in the slicer.
  The small solid centres of A/B/P are intentional. Extra material across
  letter grooves can also come from first-layer spreading or short bridges.
  Enlarged text is a geometry improvement, not a guaranteed printer fix.

## Lettering test first
[Back-only trial](STL/Norse_Back_Lettering_Test_1.2mm_v3.stl): a 50 mm disk,
1.2 mm thick, using the same back at full size. Print engraved back DOWN.
At 0.20 mm layers it reproduces the first six body layers with no colour change.
Check S, B and K before printing the complete keepsake.

## Validation and rebuilding
The model and trial STL pass exported-mesh closure, winding, connectivity,
non-degenerate facet and positive-volume checks. Mesh volume is compared with
the analytic polygon layers. The geometry preview and readable back SVG are
screen-reviewed. **No printer-profile slice or physical test of v3 is recorded.**

Rebuild: `python NorseBackpack/Props/Medallion/build_medallion_v3.py` from the
repository root, or run `build_medallion.py` beside the model.
Shared geometry: `Tools/medallion_cad.py`; front trace: `build_medallion_v2.py`.
Requires numpy, Pillow, OpenCV, matplotlib, Shapely 2.1+ and Windows Arial fonts.

- `Medallion_v3_Preview.png`: exact front/back geometry preview.
- `Front_Relief_v3.svg`, `Back_Engraving_v3.svg`: 50 mm profiles.
- `geometry_report_v3.json`: measured text gaps and v2 front comparison.
- `mesh_check_v3.json`, `lettering_test_mesh_check_v3.json`: mesh validation.
- `sources/Crest_Detailed_v2.png`: retained manufacturing mask.
- `Medallion_Print_Files_v2.zip`: preserved earlier print package.

Official references: [colour change](https://help.prusa3d.com/article/color-change_1687),
[first-layer compensation](https://help.prusa3d.com/article/elephant-foot-compensation_114487).
