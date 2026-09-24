# Coin face artwork

Seven designs from Norse_Brainstorm.html, Props & specs → The hoard and treasure tally.

- `*.svg`: closed vector profiles, black shapes only, suitable for extrusion.
- `*.png`: 2000 × 2000 pure black-and-white previews, matching the vectors.
- `Coin_Faces_Overview.png`: labelled contact sheet; do not use as a relief mask.
- `sources/`: original ImageGen outputs, retained for rebuilding.

Import an SVG into your modelling software. Scale it to your chosen size, then extrude
the black shapes and union them with a solid circular coin blank. The white/transparent
areas are empty space in the artwork, not holes through the finished coin. Preserve
the empty counters inside rings and letters. No background rectangle is included.

The SVG canvas is 1000 × 1000 units; artwork fits within radius 460 around (500,500).
Use the canvas as the intended coin diameter, or fit imported artwork within 92% of
the blank's diameter. Physical diameter, blank thickness, relief height, reverse face,
printer type and minimum printable feature size have not been specified. These are
art profiles, not STL models or verified ready-to-slice coins. Inspect narrow gaps and
pointed tips at final scale and test one coin before printing the set.

Packing implied by the current page: 4 common + 1 rare dirham; 3 common + 1 rare denier;
1 Hedeby, 1 York and 1 raven. The Viking game values remain 5, 100 and 3600. Values are
not engraved into the artwork. Decoy exchange rates and the merchant's key are still open.

The geometric pseudo-script is decorative, not readable Arabic or a historical inscription.
The designs are simplified game props, not historical replicas.

Built with the built-in ImageGen tool, then traced at luminance 128 into closed polygon
profiles (0.7 source-pixel contour tolerance; specks below 24 and counters below 160
source-pixel area removed). SVG loops have opposite winding for holes, use solid fills, and contain
no strokes, fonts, raster images or external dependencies. Original prompts and correction
prompts are in generation_manifest.json and the main brainstorming HTML.

Rebuild: `python build_coin_art.py` (Pillow, numpy, opencv-python-headless, shapely).

## STL generation (3D printing)

Printer: **Prusa i3 MK3S+**, stock 0.4mm nozzle, FDM. Confirmed 23 September 2026 — coins
are 3D-printed, not printed paper/card discs.

`build_coin_stl.py` (same dependencies as above) turns the flat SVGs into printable STLs:

1. Measures each design's thinnest stroke against the target coin size. At the default
   28mm diameter, `01_dirham_common` and `02_dirham_rare` measured below the 0.5mm safe
   minimum for a 0.4mm nozzle (0.40mm and 0.47mm); the script dilates just those two by a
   few canvas pixels and re-traces them to `*_print.svg`, leaving the flat-art SVGs above
   untouched. The other five designs were already thick enough as generated.
2. Writes one parametric `STL/<id>.scad` per coin: a cylinder blank union'd with the
   relief, linear-extruded from the (possibly thickened) SVG.
3. Shells out to the `openscad` CLI to export each `.scad` to `STL/<id>.stl`.

Defaults: 28mm diameter, 2mm blank thickness, 0.6mm relief height (3 layers at 0.2mm),
0.5mm minimum feature width. All four are constants at the top of the script.

Requires [OpenSCAD](https://openscad.org/downloads.html) (free) on PATH. Installed via
winget (`OpenSCAD.OpenSCAD`, 2021.01) on 23 September 2026; all 7 STLs exported to
`STL/*.stl` that session. `stl_report.json` records the measured stroke widths and which
designs were thickened. Re-run `python build_coin_stl.py` to regenerate after any change
to the source art or the parameters above.

## Print plates and colours

`build_coin_plates.py` combines the per-coin STLs into two plates, centred on the
MK3S+ bed (run it after `build_coin_stl.py`):

| Plate | Coins | Base | Relief |
|---|---|---|---|
| `STL/Plate_Common_9.stl` | 4 common dirham, 3 common denier, 1 Hedeby, 1 York | gray | black |
| `STL/Plate_Rare_3.stl` | 1 rare dirham, 1 rare denier, 1 raven | gray | yellow |

In the slicer, add one colour change at the first relief layer (z = 2.2mm at 0.2mm
layers). The MK3S+ pauses at that point (the M600 command) so the filament can be swapped.

No coin diameter, thickness or relief height beyond these defaults has been confirmed by
a physical print test — print one coin of each rarity tier before committing to the full set.
