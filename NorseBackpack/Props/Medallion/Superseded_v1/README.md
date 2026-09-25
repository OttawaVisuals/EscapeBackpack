# Norse adventure medallion — first printable prototype

This is a 50 mm diameter concept model based on the selected raven-shield front and compass / “ADVENTURE COMPLETE” back.

## Files

- STL/Norse_Medallion_Front.stl — raven and shield side.
- STL/Norse_Medallion_Back.stl — compass, “ADVENTURE COMPLETE” and “ESCAPE BACKPACK” side.
- Norse_Medallion.scad — editable OpenSCAD source; the default view compares both printable faces; set PART to "assembly" to view them glued together.

## Print and assembly

This version uses two halves so each decorated face can be printed face-up, giving both sides raised relief without supports. Print each half flat on its plain back, relief facing up. Each half is 2.2 mm thick (1.6 mm core + 0.6 mm relief). Glue their plain backs together; assembled thickness is 4.4 mm. Keep the front/back orientation aligned when joining.

Designed around the Prusa i3 MK3S+ with its stock 0.4 mm nozzle. The model uses 0.6 mm relief (three 0.2 mm layers) and aims for at least 0.8 mm width on major raised marks. Small maker lettering is finer than that and needs a physical legibility check. No material or slicer profile is specified; use the normal profile for the chosen filament and inspect the first print.

This is a first geometry pass, not a tested final. The raven and compass are simplified interpretations of the chosen concept art. Small text, face details and glue alignment should be reviewed on the physical print.

## Regenerate

Open Norse_Medallion.scad in OpenSCAD and set PART to "front" or "back", or run python build_medallion.py to export both STLs.
