# Aud v15 finishing corrections

- All ocean, river, stream and lake borders are drawn in one shared vector-boundary pass: #59635D at 0.55pt. Removed the old river casing widths and separate lake border. Legend water samples use the same colour and weight.
- Removed the small visible land remnant below the legend using a local geometry subtraction, clipped to the map frame.
- Transparent comb artwork replaces the cream stamp-paper image only in this draft PDF. Original postcard stamp retained. Purple line art shows over the existing #DCE7E4 title band.
- Renderer: render_finish_v15.py. Outputs: render_full_map_v15/Aud_Full_Map_v15.pdf and Aud_Changes_Review_v15.pdf, PNGs and validation logs.
- Counting symbols, irregular moor/marsh and other v14 styling retained. No physical print/count test.

## Built-in ImageGen prompts

Input edit target: NorseBackpack/Postcards/Stamps/Stamp_Aud_Comb_v1.png. First cutout saved as Aud_Comb_Ink_v15.png (superseded if cleanup selected).

Use case: background-extraction. Edit target: the attached Aud comb postage-stamp image. Remove ALL cream/yellow paper and texture, including cream areas within the comb engraving, so those areas become fully transparent. Preserve the existing purple engraved comb ink, all its knotwork, teeth, original shape, exact orientation, proportions, location and scale within the image canvas. Preserve purple ink of the perforated stamp outline if present; do not invent a new border. Output a transparent-background cutout of the same purple printed artwork; no new drawing, no added shadows, no halo, no text, no coloured backdrop. This will be printed over an existing pale blue map band, which must show through wherever the paper was.

Cleanup edit target: the first generated cutout.

undefined


Selected final cleanup: `Aud_Comb_Ink_v15_final.png` (built-in ImageGen). The first cutout is retained as a discarded intermediate. Final output contains purple engraving on transparency; the PDF supplies the exact blue background.
