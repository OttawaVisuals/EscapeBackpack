---
id: PP-044
title: Adventure medallion
type: prop
# idea | candidate | decided | built | parked
status: decided
# physical | printed | digital
form: physical
# make | buy | print | 3d-print
source: 3d-print
# The play-test page shows the body's "## Player sees" section, or this prop's image asset.
# Where the player gets it: start (in the backpack) or the puzzle whose lock releases it, e.g. PZ-004
found_in: PZ-013
# Physical pocket/container or location; availability remains in found_in above.
container: Inside lockable pocket 2 (lock 13)
after_game: keep
# Any related record IDs, e.g. [PZ-002, Q-004]
links: []
# Set to an ID when this record is replaced. It then moves to the Parked tab.
superseded_by:
tags: [old-PR-28]
---

## From the old Props & specs tab

End-of-game keepsake · revised 5 October 2026

### A small adventure medallion

**One solid print, no glue.** A small keepsake with a shared Escape Backpack back and an adventure-specific crest. The selected concept is the right-hand shield raven front and the right-hand compass back.

#### Current model · v3

The designer approved the Space medallion’s more open back lettering and requested the same back here on 5 October 2026. The v2 raven front and top-side body groove are retained. Extracted front profiles from the exported v2 and v3 STLs match exactly.

- **50 mm diameter × 4.4 mm total thickness.** A 3.8 mm body with 0.6 mm raised crest. Thicknesses use 0.2 mm layer increments; the 0.4 mm nozzle constrains feature width.
- **Front faces up:** detailed raven with layered neck, wing and tail feathers, eye and beak, shield and four ornaments. Fine channels widened by 0.16 mm; two isolated fragments too narrow for a 0.4 mm line removed. This is flat relief, without the concept image's metallic texture or sculpted shading.
- **Back faces down:** “ADVENTURE” and “COMPLETE” use 4.6 mm Arial Bold capitals around the compass. “ESCAPE BACKPACK” uses larger 4.0 mm Arial Regular capitals, without the previous outline thickening. The lower arcs are spread out; the closest adjacent brand letters are 0.831 mm apart. Text and compass are engraved 0.4 mm in the body colour. Text clears the engraved border by at least 1.321 mm. Underside geometry is mirrored so the finished back reads normally.
- **Optional crest colour:** Prusa i3 MK3S+ / 0.4 mm nozzle; use 0.20 mm layers including the first layer, then one manual filament swap before layer 20, at Z = 4.00 mm. Body ends at 3.80 mm; crest fills the final three layers. Rim stays the body colour. One print job; no swap needed for a single colour. [Prusa colour-change instructions](https://help.prusa3d.com/article/color-change_1687).

[**Open one-piece STL**](../Props/Medallion/STL/Norse_Medallion_OnePiece_v3.stl) · [Open print-file ZIP](../Props/Medallion/Medallion_Print_Files.zip) · [Print notes](../Props/Medallion/README.md) · [Thin back trial STL](../Props/Medallion/STL/Norse_Back_Lettering_Test_1.2mm_v3.stl)

![Norse v3: unchanged raven shield front and larger, widely spaced engraved back lettering](Props/Medallion/Medallion_v3_Preview.png)Exact CAD profiles. Navy body and yellow relief are illustrative filament colours.

**PP-044 · Physical print pending.** The designer reported poor S, B and K in “ESCAPE BACKPACK” on an earlier print; the exact printed version and settings are unconfirmed. The larger back lettering is approved, but its print quality is untested. Both v3 STLs pass closure, winding, connectivity and volume checks. No printer-profile slice or physical print of v3 yet. Print the 1.2 mm thin back trial first, then check first-layer spread, shallow bridges and feather tips. Start without supports or raft; use the chosen printer/material profile. Add the optional colour-change pause in the slicer.

**Artwork source, exact prompt and build method**

Built-in ImageGen used the [front reference sheet](../Props/Medallion/sources/Selected_Front_Reference.png) (right coin only) to make [the detailed crest mask](../Props/Medallion/sources/Crest_Detailed_v2.png). The [back reference sheet](../Props/Medallion/sources/Selected_Back_Reference.png) informed the lettering and compass arrangement.

**Exact prompt:** Use case: precise-object-edit. Input image is the reference; use ONLY the RIGHT-HAND shield raven medallion. Convert its face artwork into a single clean orthographic black-and-white relief manufacturing mask on a white square canvas. Preserve the distinctive left-facing raven head, strong hooked beak, round eye, layered neck feathers, and all the overlapping wing and tail feather groups; preserve the peaked shield outline and the four geometric ornaments outside the shield. Reconstruct the right coin face head-on, undistorted. No text, no coin outer rim, no coin blank, no shadow, no metal texture, no grey, no gradients, no perspective, no captions. Black means solid raised detail; white means exposed base. Raven must have an elegant cohesive silhouette with internal WHITE grooves separating about 12 to 18 substantial overlapping feathers, an eye cutout, and a beak separation groove. Keep fine details bold enough to be resolved at a 40 mm artwork width with a 0.4 mm nozzle: feather-separating white gaps about 0.5 mm, major raised strokes about 0.8 to 1.2 mm. Maintain the original shield raven character rather than replacing it with a generic cartoon bird. Entire crest plus ornaments centered with generous white margin. Square image, crisp vector-like contours.

`Props/Medallion/build_medallion_v3.py` retains the v2 front trace and uses `Tools/medallion_cad.py` for the shared back and closed polygon-layer mesh. Actual curved glyph clearances are measured. The compass uses outline engraving to keep underside bridges short. [Front SVG](../Props/Medallion/Front_Relief_v3.svg) · [Readable back SVG](../Props/Medallion/Back_Engraving_v3.svg) · [Geometry measurements](../Props/Medallion/geometry_report_v3.json) · [Mesh checks](../Props/Medallion/mesh_check_v3.json).

**Superseded · earlier versions**

[v2 STL](../Props/Medallion/STL/Norse_Medallion_OnePiece_v2.stl), [v2 notes](../Props/Medallion/README_v2.md) and [v2 package](../Props/Medallion/Medallion_Print_Files_v2.zip) remain as history. v3 replaces its back lettering. The first export incorrectly changed the intended single print into two 2.2 mm halves to glue together, oversimplified the crest and did not fit the lettering properly. The user rejected that approach on 25 September 2026. Those files remain in `Props/Medallion/Superseded_v1/`; use the v3 one-piece STL above.

## Design notes (PP-044: To print and test)

**Check the one-piece keepsake on the printer.**

50 mm diameter, 4.4 mm thick; engraved back down, detailed crest up. Check underside letters and feathers on the first print. Optional one filament change for the crest. [Current STL and full specification]. No physical print or printer-profile slice yet.

## Starting state

Not recorded yet.

## Reset

None needed: the team keeps the medallion (designer, 10 Oct 2026).

## Replacement

One new medallion for every team, since each team keeps theirs (designer, 10 Oct 2026).

