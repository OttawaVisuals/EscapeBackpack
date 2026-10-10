---
id: PP-028
title: Aud's comb
type: prop
# idea | candidate | decided | built | parked
status: decided
# physical | printed | digital
form: physical
# make | buy | print | 3d-print
source: 3d-print
# The play-test page shows the body's "## Player sees" section, or this prop's image asset.
# Where the player gets it: start (in the backpack) or the puzzle whose lock releases it, e.g. PZ-004
found_in: PZ-002
# Physical pocket/container or location; availability remains in found_in above.
container: Locked pouch inside the front pocket (lock 2)
# Any related record IDs, e.g. [PZ-002, Q-004]
links: []
# Set to an ID when this record is replaced. It then moves to the Parked tab.
superseded_by:
tags: [old-PR-19]
---

## From the old Props & specs tab

Prop

### The comb grille

A printed or 3D-printed comb with broken teeth, laid across a postcard message so that only certain words show through the gaps. Rotated or flipped, one comb decodes several cards. **Back on Aud’s trail, 16 Sept 2026** — it had briefly moved to Harald’s journey in an earlier session, but the user moved it back: Aud’s own stamp motif and Q-032 already tie a comb to her documented saga story (Landnámabók’s account of the comb she lost at Kambsnes), which fits better than an unconnected Harald assignment ever did.

Combs are among the most common Viking finds and broken teeth are entirely plausible, so the object hides in plain sight. **Superseded, 18 Sept 2026:** the comb is no longer a family heirloom Liv carries in; it's Aud's own comb, found on the trip and kept — see AD's message below.

**Job, decided 16 Sept 2026:** laid across decoy card AD’s (Bjarnarhöfn) message, released at the end of Aud’s treasure-hoard chain (PZ-006). The letters it exposes open a lock gating entry to Harald’s leg — Aud’s whole trail must be finished before Harald’s can start. The 3D-printed tooth spacing is engineered to expose chosen letters on AD. **BOOK was decided 25 Sept 2026**, confirming the reading/kinship idea in AD's message rather than naming it outright. Superseded: an earlier plan reset the SOLE lock for this job. BOOK now has its own four-letter lock (Q-026).

**AD's message, decided 18 Sept 2026:Superseded, 25 Sept 2026:** the first line below was reworded on 20 Sept 2026 to “At her brother’s harbor — the one Aud wintered in.” The built card (`build_postcard_AD_pdf.py`) uses the new line.

At her brother’s harbor — the one Aud wintered in.
I’ve read everything I could find about her this trip, to the point that she feels like family (and she actually maybe was).
It was so awesome to find that comb alongside the coins, and the museum let me keep it!
This is actually the real treasure, a piece of history that we can use!
With love,
Aunt Liv

Built: `Postcards/build_postcard_AD_pdf.py` → `output/pdf/Postcard_AD_Bjarnarhofn_Print.pdf`. See [Postcards · AD] for the rendered card.

~~**Still open:** which specific letters in this text the comb's teeth expose to spell BOOK, and the physical tooth-cutting itself.~~ **Resolved 25 Sept 2026** — see below.

**Mechanism decided and comb modelled, 25 Sept 2026.** The comb lies **upright** on AD’s back: handle in the left margin (overhanging the card edge by about 5.5 mm), teeth pointing right across the message. **One tooth per line**, at the message’s own line spacing, so each intact tooth covers its whole line. Four teeth are broken short and stop just before a chosen letter, so with the comb in place only four lines show:

| Line | What shows | Broken tooth |
|---|---|---|
| 1 | **b**rother’s harbor — the one Aud | 10.5 mm |
| 3 | **o**uld find about (the o of “could”) | 29.5 mm |
| 8 | **o**ngside the coins, and the museum let (“al” covered) | 3.1 mm |
| 9 | **k**eep it! | 5.2 mm |

First visible letters, top to bottom: **BOOK**. An upright comb was the user’s call: it puts the broken teeth in reading order. A tilted comb was tried first and rejected — its spine and alignment marks would have fallen off the card.

**Alignment.** Two Viking **ring-and-dot** marks are printed on AD’s back in the left margin, one above line 1 and one below the signature, 49 mm apart (`COMB_MARKS` in `build_postcard_AD_pdf.py`). The comb’s flared ends carry matching carved ring-and-dots whose centres are 2 mm through-holes; players sit each printed dot in its hole. AD’s own stamp shows the same comb with a ring-and-dot at each end, so the stamp quietly shows how the comb goes on.

**Handle carving**, after the stamp: flared ends with ring-and-dots, a knotwork band along the middle, a small dot at each end of the band, and a border line, all cut 0.6 mm into the top face. **Built 26 Sept 2026:** the final black-and-white band is `Props/Comb/knotwork.png`; `build_knotwork.py` traces its SVG from the retained `knotwork_source.png`. The comb builder imported that SVG and regenerated the STL. The source drawing has some narrow crossing gaps, so the 0.6 mm detail target needs checking on a physical print with the intended 0.4 mm nozzle. Finish suggestion: print in bone-white and rub dark wax or paint into the grooves.

**Sizes:** about 65 × 55 mm overall; teeth 2.2 mm wide, 1.6 mm thick, intact teeth 52.7 mm long, gaps 0.85 mm; handle 3.0 mm thick, outer corners rounded to 2.5 mm (the carved border follows them); the inside corners where the flared ends meet the handle get only a 0.3 mm fillet, because anything larger closes the gap to the first tooth below 0.75 mm. Flat bottom, printed face up, no supports.

**Built:** `Props/Comb/build_comb.py` reads the line positions and target letters straight from the built AD print PDF (so the comb cannot drift from the card), checks the four letters still spell BOOK, and writes `Aud_Comb.scad`, `Aud_Comb.stl`, `comb_geometry.json` and `Aud_Comb_on_AD.png` (the comb drawn over the real card). **Re-run it after any change to AD’s back.Still open:** a test print against a real printed AD (fit, tooth strength, carving clarity, whether the marks survive trimming).

![Aud's comb laid upright on AD's back: only four lines of the message show, starting with b, o, o and k](Props/Comb/Aud_Comb_on_AD.png)The modelled comb drawn over the real AD back. Only “brother’s harbor…”, “ould find about”, “ongside the coins…” and “keep it!” show.

![Two broad interlaced black ribbons with curled ends for Aud's comb handle](Props/Comb/knotwork.png)The built handle knotwork, shown flat before it is carved into the 3D-printed comb.

Original knotwork brief

```
Use case: flat relief artwork for 3D printing, to be traced into a vector.
Reference: NorseBackpack/Postcards/Stamps/Stamp_Aud_Comb_v1.png - match the knotwork band on that comb's handle.
Create one horizontal Viking-age ribbon interlace band, as carved on a bone comb handle: two ribbons
weaving over and under each other along the band, with a small curled terminal at each end.
Pure black shapes on a pure white background. No grey, shading, texture, outline border, text or
frame. Show every under-crossing with a clear white gap either side of the ribbon passing under.
Proportions: exactly 8:1 (it will be printed about 38 x 4.8 mm). Every ribbon at least 1/8 of the
band height wide, and every white gap at least as wide, so no line is thinner than 0.6 mm at print size.
Output: PNG, 3200 x 400 px.
Then: threshold at luminance 128 and trace to closed polygons as for the coin faces
(Props/Coins/build_coin_art.py), save as Props/Comb/knotwork.svg, and re-run build_comb.py.
```

Exact ImageGen prompt used, 26 Sept 2026

```
Use case: logo-brand. Asset type: flat relief artwork to trace into a vector for a 3D printed Viking Age bone comb. Reference image role: style and motif reference only; isolate the interlaced ribbon band on the comb handle, excluding the rest of the stamp. Create one horizontal Viking Age ribbon interlace band matching that handle: two broad ribbons weaving over and under along a single row, with a small curled terminal at each end. Pure solid black shapes on a pure white background. Show each under crossing with clear white gaps on both sides of the ribbon passing under. Exact 8:1 artwork aspect ratio, intended final scale 38 x 4.8 mm. Every black ribbon and every white gap at least one eighth of the band height wide, so no detail becomes thinner than 0.6 mm at print size. No gray, antialias-like texture, shading, hatching, outline border, text, frame, comb, stamp, dots, extra objects, or surrounding decorative field. Produce a clean simple production-ready flat silhouette.
```

Reference: `Postcards/Stamps/Stamp_Aud_Comb_v1.png`. The generated transparent source was composited over white, thresholded at 128, fitted to 3200 × 400 px, and traced by `Props/Comb/build_knotwork.py`. The requested minimum white-gap width was not guaranteed by ImageGen; validate the grooves on a print.

## Design notes (PP-028: Artwork built · test print pending (26 Sept 2026))

**The comb (PZ-010 comb-grille lock) needs a physical print test.**

**Regenerated, 29 Sept 2026.** AD’s message went to 9.5 pt / 10.6 pt leading and the wider column (text now starts at `x 15`), so `Props/Comb/build_comb.py` was re-run against the new AD print PDF: tooth root at `x 13.5` (was 18.5), teeth 2.47 mm wide (was 2.19) with 1.27 mm gaps, intact teeth reach `x 180`. The same four words still give the answer — line 1 **b**rother, line 3 c**o**uld, line 8 al**o**ngside, line 9 **k**eep → BOOK. The printed ring-and-dots moved: upper mark raised to y 16 (was 19.5) so the flared end clears the first tooth, lower mark moved to y 186 (was 158.5) because the old spot now sat on the signature; holes are 60 mm apart (was 49). New `Aud_Comb.stl`, `Aud_Comb.scad`, `Aud_Comb_on_AD.png` and `comb_geometry.json`. **Any comb already printed must be reprinted.**

Design intent is recorded under [the comb prop]: a 3D-printed comb with broken teeth, tooth spacing engineered so laying it over decoy card AD's message exposes exactly the letters that spell `BOOK`. **Modelled 25 Sept 2026** — upright comb, one tooth per line, BOOK read from lines 1, 3, 8 and 9, aligned by two ring-and-dot marks. **Knotwork built 26 Sept 2026** as a traced SVG and included in the rebuilt STL. **Still needed:** print the comb and AD at actual size; confirm fit, tooth strength, readable letters, and trim tolerance. The artwork's narrowest white gaps still need a physical print check at the selected nozzle/finish.

## Starting state

Not recorded yet.

## Reset

Not recorded yet.

## Replacement

Not recorded yet.
