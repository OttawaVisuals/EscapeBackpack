---
id: PP-037
title: The coin hoard
type: prop
# idea | candidate | decided | built | parked
status: decided
# physical | printed | digital
form: physical
# make | buy | print | 3d-print
source: 3d-print
# The play-test page shows the body's "## Player sees" section, or this prop's image asset.
# Where the player gets it: start (in the backpack) or the puzzle whose lock releases it, e.g. PZ-004
found_in: PZ-005
# Physical pocket/container or location; availability remains in found_in above.
container: Inside lockable pocket 1 (lock 7)
after_game: return
# Any related record IDs, e.g. [PZ-002, Q-004]
links: []
# Set to an ID when this record is replaced. It then moves to the Parked tab.
superseded_by:
tags: [old-PR-25, old-PR-20, old-PR-02]
---

## From the old Props & specs tab

Approved replacement · 22 September 2026, coin design decided 23 September 2026

### The hoard and treasure tally

After the 521 treasure-route gate, release A1/A3, three coin piles, a merchant’s value key and a labelled treasure tally. The cache mark selects one pile by currency. Convert and add that pile's coin values to **3705**; display the total, then rotate the whole device 180 degrees to read **SOLE**.

The display can be a calculator or four independently settable 0–9 wheels. Label it *“Use this to tally treasure.”* A1 must instruct adding values; A3 must refer to the tally. Revised copy is in Approved changes. There is no scale, decimal point, discarded digit or mass target.

#### Three piles, one per real-history currency

**Superseded in part, 24 Sept 2026:** the three currencies now arrive loose and mixed; players sort them against the ticket’s Coin Room key and the fehu cache mark picks the Norse group (note below). The currencies, counts and values are unchanged. Not one mixed hoard sorted by a single mark — three separate small piles, each a plausible "natural find" with a common-to-rare spread. The cache mark says which pile's currency is the one that matters; the other two are decoys with no target total. Currency choice and rarity tiers are loosely modelled on what actually turns up in Viking hoards, though the specific values below are fictional game numbers, not a historical exchange-rate claim.

| Pile | Coins | Role | Real-history basis |
|---|---|---|---|
| **Islamic dirhams** | 5 (mixed common + 1 rare) | Decoy — no target sum | The most common foreign silver actually found in Viking hoards (e.g. the Spillings hoard), traded in via eastern routes. |
| **Carolingian deniers** | 4 (mixed common + 1 rare) | Decoy — no target sum | Frankish trade silver, present in hoards but far less common than dirhams. |
| **Viking/Norse coins** | 3, one per rarity tier | **Target — converts to 3705** | See below — includes a real callback to the game's own raven motif. |

#### The Viking pile — the puzzle's answer

One coin per rarity tier, each a different real (or real-inspired) Norse-era coin:

- **Common — Hedeby coin, rate 5.** Early Viking trading-town Hedeby minted crude local silver; historically the everyday find.
- **Mid — York imitation penny, rate 100.** Norse-minted imitation of Anglo-Saxon coinage from the Viking kingdom of York.
- **Rare — Anlaf Guthfrithsson "raven" penny, rate 3600.** A real coin type minted at York under Anlaf Guthfrithsson bearing a raven — very few survive. Doubles as a deliberate callback to the game's HRAFN/raven thread.

**5 + 100 + 3600 = 3705** — three coins, three tiers, real addition (not one multiplication), and few enough coins to keep fabrication simple.

**The merchant’s key is on the museum ticket, decided 24 Sept 2026.** The front of Aud’s Treasure Museum ticket now carries “The Coin Room — what each coin was worth in Aud’s day” (**changed 25 Sept 2026** to “What each coin is worth today”, values in dollars: $20, $900, $40, $1,200, $5, $100, $3,600 — the Norse coins still total 3705): all seven coins, each with a small picture drawn as it prints (gray blank, black relief for common, yellow for rare) and its value. It replaces the separate key prop and the ticket’s placeholder lozenge, tagline and opening hours. **Ticket reworked 25 Sept 2026:** resized from 2×5.5 in to **3×4 in**; shorter title band with the name on one line; the ADMIT ONE block (valid / admission / guide rows) and the “Turn over for the treasure hunt” line removed; coin pictures enlarged to 21 pt (title band cut to 44 pt to make room), which also fixes the low-contrast rare coins noted below. The front now holds only the title and the Coin Room. The back keeps its six legs and tally boxes, with larger text (6.8 pt) and boxes to fill the new size. **Two wording fixes, same day:** leg 1 now reads “Start at the northernmost chapel and follow the road east to the next chapel” — the start (C2, the northernmost of six chapels) had not been stated anywhere since the 18 Sept route redesign dropped the start panel; leg 4 says “standing stone by the **chapel**” instead of “church”, matching the map legend. All seven are listed so the key does not reveal which pile counts — the cache mark does that.

**The cache mark, decided 24 Sept 2026.** Each currency group on the ticket has an icon on its divider: **camel** for dirhams (eastern trade), **fleur-de-lis** for deniers (Frankish), **the fehu rune ᚠ** for Norse coins (the rune means wealth). Aud’s map repeats only the fehu rune, in Aud purple, beside the treasure cave at I9 — the end of the ticket’s route. Players match it to the ticket and keep the Norse group. The icons avoid every final-riddle element and every coin face. **Decoy marks, same day:** the other two icons also appear on the map, each beside a cave where a misread route would plausibly end — the **camel at the G1 cave** (by the H2 ruin and wood, near the lookalike “village at the crossing” at G3, echoing leg 6’s “ruin, then the wood beyond”) and the **fleur-de-lis at the C4 cave** (in the wood by the B5 ruin). A wrong route therefore picks a wrong pile and totals 980 or 1320, never a word. The E7 and I4 caves stay unmarked: no ruin near them. **The coins are released loose and mixed** in the 521 pouch, so sorting by face against the ticket is part of the puzzle. Built: `build_trail_maps_pdf.py` (`draw_aud_cache_mark`) and `Props/AudTicket/build_group_icons.py` (camel and fleur-de-lis rendered from Segoe UI Symbol into `icons/`; fehu is drawn as vector on both).

| Coin | Value | Pile total |
|---|---|---|
| Dirham · Dirham, old mint (rare) | 20 · 900 | 4×20 + 900 = 980 (decoy) |
| Denier · Denier, crowned (rare) | 40 · 1200 | 3×40 + 1200 = 1320 (decoy) |
| Hedeby ship coin · York penny · Raven penny (rare) | 5 · 100 · 3600 | **3705** (target) |

Decoy totals were chosen so neither reads as a word upside down (980 → “086”, 1320 → “OZEI”). Built: `Props/AudTicket/build_aud_ticket_pdf.py` → [View PDF](../Web/pdf/Aud_Ticket_Print.pdf). The ticket arrives at step 6, a step before the coins, so the values sit unexplained until the hoard opens. **Still open:** rare coins read low-contrast (yellow on gray) at 14 pt; accepted for now, recheck on the printed ticket.

#### Coin face designs

Simple and flat, so piles sort by eye before players ever check the value key. Design rule: strike quality scales with rarity — crude → clean → finest.

| Coin | Design |
|---|---|
| Common dirham | Silver, no figures — concentric rings of Kufic-script-style lettering, plain center. |
| Rare dirham | Same script style, different inner ring pattern (different mint), slightly darker/worn tone. |
| Common denier | Plain cross motif, dot border, generic ruler-name lettering. |
| Rare denier | Same cross motif with a small crown or portrait bust added above it. |
| Hedeby coin (common) | Crude, asymmetric ship silhouette, no border, deliberately rough strike. |
| York penny (mid) | Plain cross, small circular border, moderately clean strike. |
| Raven penny (rare) | Raven with spread wings, centered, clean strike — finest of the set. |

#### Codex art prompts

Kept deliberately vague so Codex isn't steered into unnecessary detail:

- **Common dirham:** "Simple Viking-era silver Islamic coin, worn, Arabic-style script pattern, no figures, flat top-down view."
- **Rare dirham:** "Same style as a common dirham but visibly older/rarer mint variant, slightly different inner pattern, darker tone."
- **Common denier:** "Simple medieval Frankish silver coin, plain cross design, worn, flat top-down view."
- **Rare denier:** "Same style as a common denier but with a small crown or ruler's bust added above the cross, cleaner strike."
- **Hedeby coin:** "Crude early Viking silver coin, rough asymmetric ship shape, no border, deliberately rough strike."
- **York penny:** "Simple Viking-era silver coin, plain cross, small circular border, moderately clean strike."
- **Raven penny:** "Viking-era silver coin, raven with spread wings centered, clean strike, rarest and finest of the set."

#### Coin face artwork · generated 23 September 2026

Artwork built · physical print pending Seven simplified faces following the designs above. SVG files contain closed filled contours for extrusion; PNGs are matching 2000 × 2000 black-and-white previews. Black means raised detail. These are face profiles, not complete 3D coins. [Download all coin artwork (ZIP)](../Props/Coins/Coin_Face_Artwork.zip) · [Import notes](../Props/Coins/README.md).

Import a face, scale it to the chosen coin size, extrude the black regions and join them to a solid circular blank. The 1000-unit square canvas represents the coin diameter; artwork fits within 92% of that diameter. SVGs include no background rectangle, raster image or font dependency. Diameter, thickness, relief height, reverse faces and printer tolerances remain open under PP-037. No physical print or slicer test is claimed.

Common/rare differences are geometric: the rare dirham adds a central pattern and double rings; the rare denier adds a crown. The script-like marks are decorative geometry, not readable Arabic or historical inscriptions. These are game-prop interpretations, not exact replicas. The Viking values remain on the merchant's key, not engraved into these images.

[![Common dirham black relief profile](Props/Coins/01_dirham_common.svg)](../Props/Coins/01_dirham_common.png)**Common dirham**
[SVG profile](../Props/Coins/01_dirham_common.svg) · [PNG preview](../Props/Coins/01_dirham_common.png)

[![Rare dirham black relief profile](Props/Coins/02_dirham_rare.svg)](../Props/Coins/02_dirham_rare.png)**Rare dirham**
[SVG profile](../Props/Coins/02_dirham_rare.svg) · [PNG preview](../Props/Coins/02_dirham_rare.png)

[![Common denier black relief profile](Props/Coins/03_denier_common.svg)](../Props/Coins/03_denier_common.png)**Common denier**
[SVG profile](../Props/Coins/03_denier_common.svg) · [PNG preview](../Props/Coins/03_denier_common.png)

[![Rare denier black relief profile](Props/Coins/04_denier_rare.svg)](../Props/Coins/04_denier_rare.png)**Rare denier**
[SVG profile](../Props/Coins/04_denier_rare.svg) · [PNG preview](../Props/Coins/04_denier_rare.png)

[![Hedeby ship black relief profile](Props/Coins/05_hedeby_ship.svg)](../Props/Coins/05_hedeby_ship.png)**Hedeby ship**
[SVG profile](../Props/Coins/05_hedeby_ship.svg) · [PNG preview](../Props/Coins/05_hedeby_ship.png)

[![York penny black relief profile](Props/Coins/06_york_cross.svg)](../Props/Coins/06_york_cross.png)**York penny**
[SVG profile](../Props/Coins/06_york_cross.svg) · [PNG preview](../Props/Coins/06_york_cross.png)

[![Raven penny black relief profile](Props/Coins/07_raven.svg)](../Props/Coins/07_raven.png)**Raven penny**
[SVG profile](../Props/Coins/07_raven.svg) · [PNG preview](../Props/Coins/07_raven.png)

**Exact generation prompts and conversion method**

Built-in ImageGen tool. Each original prompt is recorded in full below. Source PNGs are preserved in `Props/Coins/sources/`; `build_coin_art.py` regenerates the vectors and previews. Conversion composites transparency over white, thresholds at luminance 128, traces closed contours with 0.7 source-pixel tolerance, removes specks below 24 and counters below 160 source-pixel area, validates polygon geometry, and scales the result within a circular safe area. This is geometry validation, not proof of printability at an unspecified scale.

##### Common dirham

```
Create a single flat monochrome coin-face RELIEF MASK for a 3D-printed escape-game prop. Square white canvas, perfectly top-down orthographic, centered design contained within a circular area occupying 80% of canvas. Pure solid BLACK raised motifs on pure WHITE background, sharp bold silhouette edges. White is recessed/empty. No grey, gradients, lighting, metallic texture, shadows, perspective, lettering outside coin, mockup, dimensions or watermark. Generous spacing and thick details, no tiny dots or hairlines, designed to trace into closed SVG shapes and extrude onto a solid coin blank. The circular blank is NOT black-filled; keep white background. Historical-inspired simplified game prop, not a replica. Common dirham: two concentric bands of simple angular Kufic-inspired geometric pseudo-script around a plain empty circular center. Sparse, chunky angular marks, no real words or religious text, no figures. Modest irregularity of the marks suggests a crude strike, but every contour remains bold and crisp. Clear circular organization.
```

##### Rare dirham

```
Create a single flat monochrome coin-face RELIEF MASK for a 3D-printed escape-game prop. Square white canvas, perfectly top-down orthographic, centered design contained within a circular area occupying 80% of canvas. Pure solid BLACK raised motifs on pure WHITE background, sharp bold silhouette edges. White is recessed/empty. No grey, gradients, lighting, metallic texture, shadows, perspective, lettering outside coin, mockup, dimensions or watermark. Generous spacing and thick details, no tiny dots or hairlines, designed to trace into closed SVG shapes and extrude onto a solid coin blank. The circular blank is NOT black-filled; keep white background. Historical-inspired simplified game prop, not a replica. Rare dirham: concentric bands of bold angular Kufic-inspired geometric pseudo-script, no real words or religious text, no figures. Clearly distinguish this variant by a thick DOUBLE circular ring surrounding a centered four-part angular geometric rosette, while the common variant has a plain center. Sparse large marks, no fine detail.
```

##### Common denier

```
Create a single flat monochrome coin-face RELIEF MASK for a 3D-printed escape-game prop. Square white canvas, perfectly top-down orthographic, centered design contained within a circular area occupying 80% of canvas. Pure solid BLACK raised motifs on pure WHITE background, sharp bold silhouette edges. White is recessed/empty. No grey, gradients, lighting, metallic texture, shadows, perspective, lettering outside coin, mockup, dimensions or watermark. Generous spacing and thick details, no tiny dots or hairlines, designed to trace into closed SVG shapes and extrude onto a solid coin blank. The circular blank is NOT black-filled; keep white background. Historical-inspired simplified game prop, not a replica. Common Frankish denier: one plain bold equal-arm cross centered, surrounded by a circular border of twelve large separated round pellets and a sparse band of coarse angular pseudo-letter marks suggesting an old ruler legend. No actual names, words or numerals. Worn/simple strike expressed only by slight contour asymmetry, not texture.
```

##### Rare denier

```
Create a single flat monochrome coin-face RELIEF MASK for a 3D-printed escape-game prop. Square white canvas, perfectly top-down orthographic, centered design contained within a circular area occupying 80% of canvas. Pure solid BLACK raised motifs on pure WHITE background, sharp bold silhouette edges. White is recessed/empty. No grey, gradients, lighting, metallic texture, shadows, perspective, lettering outside coin, mockup, dimensions or watermark. Generous spacing and thick details, no tiny dots or hairlines, designed to trace into closed SVG shapes and extrude onto a solid coin blank. The circular blank is NOT black-filled; keep white background. Historical-inspired simplified game prop, not a replica. Rare Frankish denier: one bold equal-arm cross in the middle-lower center, a separate small unmistakable three-point CROWN directly above the cross. A circular border of twelve large separated round pellets. Sparse coarse angular pseudo-letter marks suggesting an old ruler legend, no actual names, words or numerals. Clean contours. Crown must be large enough to print.
```

##### Hedeby ship

```
Create a single flat monochrome coin-face RELIEF MASK for a 3D-printed escape-game prop. Square white canvas, perfectly top-down orthographic, centered design contained within a circular area occupying 80% of canvas. Pure solid BLACK raised motifs on pure WHITE background, sharp bold silhouette edges. White is recessed/empty. No grey, gradients, lighting, metallic texture, shadows, perspective, lettering outside coin, mockup, dimensions or watermark. Generous spacing and thick details, no tiny dots or hairlines, designed to trace into closed SVG shapes and extrude onto a solid coin blank. The circular blank is NOT black-filled; keep white background. Historical-inspired simplified game prop, not a replica. Common Hedeby coin: a crude asymmetric Viking SHIP silhouette, one simple mast, one chunky square sail, curved hull with a raised prow and stern. No circular border, no lettering, no sea lines, no rigging, no tiny oars. Hand-struck asymmetry only in the large shapes. Instantly recognizable boat with sail.
```

Correction prompt, using the first generated image as reference:

```
Create a single flat monochrome coin-face RELIEF MASK for a 3D-printed escape-game prop. Square white canvas, perfectly top-down orthographic, centered design contained within a circular area occupying 80% of canvas. Pure solid BLACK raised motifs on pure WHITE background, sharp bold silhouette edges. White is recessed/empty. No grey, gradients, lighting, metallic texture, shadows, perspective, lettering outside coin, mockup, dimensions or watermark. Generous spacing and thick details, no tiny dots or hairlines, designed to trace into closed SVG shapes and extrude onto a solid coin blank. The circular blank is NOT black-filled; keep white background. Historical-inspired simplified game prop, not a replica. Edit the provided Hedeby ship mask: REMOVE the entire outer circular border, leaving only the boat. Remove the two thin white decorative stripes inside the hull, so the hull is a solid chunky silhouette. Keep the square sail, mast and raised ends. Preserve slight asymmetry. Pure black silhouette on opaque white.
```

##### York penny

```
Create a single flat monochrome coin-face RELIEF MASK for a 3D-printed escape-game prop. Square white canvas, perfectly top-down orthographic, centered design contained within a circular area occupying 80% of canvas. Pure solid BLACK raised motifs on pure WHITE background, sharp bold silhouette edges. White is recessed/empty. No grey, gradients, lighting, metallic texture, shadows, perspective, lettering outside coin, mockup, dimensions or watermark. Generous spacing and thick details, no tiny dots or hairlines, designed to trace into closed SVG shapes and extrude onto a solid coin blank. The circular blank is NOT black-filled; keep white background. Historical-inspired simplified game prop, not a replica. York imitation penny: a single plain thick equal-arm cross at the center, surrounded by one small clean circular ring. Restrained moderately clean strike, slightly handmade. No dot border, no crown, no lettering, no other decoration. Plenty of white around the ring.
```

##### Raven penny

```
Create a single flat monochrome coin-face RELIEF MASK for a 3D-printed escape-game prop. Square white canvas, perfectly top-down orthographic, centered design contained within a circular area occupying 80% of canvas. Pure solid BLACK raised motifs on pure WHITE background, sharp bold silhouette edges. White is recessed/empty. No grey, gradients, lighting, metallic texture, shadows, perspective, lettering outside coin, mockup, dimensions or watermark. Generous spacing and thick details, no tiny dots or hairlines, designed to trace into closed SVG shapes and extrude onto a solid coin blank. The circular blank is NOT black-filled; keep white background. Historical-inspired simplified game prop, not a replica. Rare raven penny: centered recognizable RAVEN with both wings spread symmetrically, head in side profile facing right, strong beak, fan tail, two simple sturdy feet. Broad connected black silhouette, only three or four broad separated flight-feather tips on each wing, no internal feather texture. Cleanest finest strike in the set through balanced composition, not complexity. No circular border or lettering. Raven head and beak distinctly visible above the wing line, not an eagle.
```

Correction prompt, using the first generated image as reference:

```
Create a single flat monochrome coin-face RELIEF MASK for a 3D-printed escape-game prop. Square white canvas, perfectly top-down orthographic, centered design contained within a circular area occupying 80% of canvas. Pure solid BLACK raised motifs on pure WHITE background, sharp bold silhouette edges. White is recessed/empty. No grey, gradients, lighting, metallic texture, shadows, perspective, lettering outside coin, mockup, dimensions or watermark. Generous spacing and thick details, no tiny dots or hairlines, designed to trace into closed SVG shapes and extrude onto a solid coin blank. The circular blank is NOT black-filled; keep white background. Historical-inspired simplified game prop, not a replica. Edit provided bird to clearly represent a RAVEN rather than a heraldic eagle. Replace the hooked eagle beak with a long STRAIGHT wedge-shaped raven beak, blunt angular head profile, little shaggy throat. Simplify talons into two short thick legs with blunt two-toed feet; NO sharp hooked talons. Retain spread wings but simplify to FOUR broad feather lobes on each side and a chunky fan tail. Enlarge eye opening slightly. Connected black silhouette, all on opaque white, no border.
```

**Confirmed, 23 September 2026: these coins are 3D-printed** on the user's own printer — a **Prusa i3 MK3S+** (stock 0.4mm nozzle, FDM) — not printed paper/card discs.

**STL generation, 23 September 2026:** `Props/Coins/build_coin_stl.py` extrudes each relief SVG onto a cylindrical blank and exports STL via the OpenSCAD CLI. Defaults: **28mm diameter, 2mm blank, 0.6mm relief height** (3 layers at 0.2mm). It first checks each design's thinnest stroke against a 0.5mm minimum feature width (roughly one nozzle-width) — at 28mm, the two dirham faces measured just under that (0.40mm and 0.47mm) and were automatically thickened by a few pixels before tracing; the other five designs were already safe. All 7 STLs exported to `Props/Coins/STL/` on 23 September 2026 via [OpenSCAD](https://openscad.org/downloads.html) (installed via winget). Geometry only — no physical print has been done.

**Colours, decided 24 September 2026:** every coin has a **gray** base (reads as silver). The 9 common coins (common dirhams and deniers, Hedeby, York) get **black** relief for contrast; the 3 rare coins (rare dirham, rare denier, raven penny) get **yellow** relief so they read as valuable at a glance. Yellow implies gold although the real coins were silver — accepted as a game-prop liberty. Green, red and blue were rejected as not reading as metal. Two print plates, `STL/Plate_Common_9.stl` and `STL/Plate_Rare_3.stl` (built by `build_coin_plates.py`), each need one colour change at the first relief layer (z = 2.2mm at 0.2mm layers).

**Open:** device choice for the tally (PP-026), an actual physical print test of one coin per rarity tier (PP-037), the cache/selection mark, and physical legibility of the upside-down word. SOLE and MEAD require separate word locks.

[Full tally specification and postcard drafts]

**Superseded hoard and balance design**

Prop

### The hoard: coins and balance

The most Hiking-like puzzle in the set, and the only one that introduces a genuinely new physical verb: weighing.

Decided in principle · recorded 2026-09-15 Aud’s existing journey map becomes the treasure map; no separate smaller sheet. It keeps its final-route role, but also gains a close-up treasure layer: grid, contour lines, river, paths and named local features. This supersedes the earlier Rollo/Harald mint-city concept.

- **Dögurðarnes:** Liv’s directions take players through four unambiguous map features. Each destination square contains one hidden digit; together they open the lock that releases the hoard.
- **Hoard:** all coins release at once, mixed together. There are several coins of each of three visually distinct types; players must sort them into three piles.
- **Treasure selection:** the final route square carries a cache mark matching one coin type, so the map selects which sorted pile matters.
- **Hvammur + Esjuberg:** Hvammur tells players to weigh the selected pile. Esjuberg’s upside-down art and Liv’s scale-display sketch show the final digit crossed out: `370.56 g` becomes `370.5`.
- Turn `370.5` upside down to read `SOLE`, the decided answer for the owned four-letter lock.

**Dögurðarnes + map**
4 feature stops → 4 digits

→

**Coin-cache lock**
mixed 3-type hoard

→

**Map cache mark**
select one sorted pile

+

**Hvammur + Esjuberg + scale**
`370.56 g` → `370.5`

→

`SOLE`
4-letter lock

The scale must be replaced: the current linked 200 g / 0.01 g model is insufficient. The replacement needs capacity above `370.56 g` and 0.01 g resolution. Exact coin counts, designs and controlled ballast remain open until the physical scale and coin blanks are chosen and tested.

## Design notes (PP-037: Decided design · coin print test open)

**Coin inventory, currencies and values are decided; physical coins, marks and the merchant's key still need to be built.**

**Decided, 23 Sept 2026:** coins are 3D-printed on the user's **Prusa i3 MK3S+** (stock 0.4mm nozzle), not printed paper/card discs — matching the comb and hnefatafl pieces elsewhere in the kit. Codex's seven relief-mask designs ([gallery in the hoard prop]) assume this medium. `Props/Coins/build_coin_stl.py` extrudes them to STL at 28mm diameter, 2mm blank, 0.6mm relief — see the hoard prop for the pipeline and which two designs needed thickening for the nozzle. All 7 STLs exported 23 Sept 2026. **Colours decided, 24 Sept 2026:** gray base; black relief on the 9 commons, yellow relief on the 3 rares; one plate each, one filament change per plate. **Still needed: a physical print test** — geometry has not been printed or checked on the real printer.
**Decided, 23 Sept 2026:** three piles by currency — 5 Islamic dirhams, 4 Carolingian deniers (both decoys, no target sum), and 3 Viking coins (Hedeby rate 5, York rate 100, Anlaf raven-penny rate 3600, summing to 3705). Full design and Codex art prompts are in [the hoard prop]. No historical exchange-rate claim — rates are fictional game values loosely modelled on real rarity. **Still open:** physical coin fabrication (7 distinct faces across the 3 piles), the cache/selection mark, and the printed merchant's value key. ~~A1/A3 drafts are in Approved changes; PDFs and gallery backs still need regeneration.~~ **Updated, 25 Sept 2026:** A1/A3 were rewritten and rebuilt, and the page images were refreshed. The cache mark is built (fehu beside the treasure cave, with camel and fleur-de-lis decoys, drawn by `draw_aud_cache_mark()`). The value key is the “Coin Room” front of Aud’s ticket. The only open item is the physical coin print test.

## Design notes (PP-037: Revised · to design)

**Coin faces and inventory need defined values and selection marks.**

Make the selection mark distinct from denomination marks. Supply a merchant’s value key and record exact quantities for reset. Test that the selected set totals 3705. No ballast or calibrated mass is required. Track the remaining work under PP-037.

**Superseded specification · before 22 September 2026**

PP-037 To build

The hoard's coins (PZ-010 hoard-and-balance lock) need to be 3D-modelled and printed with calibrated weights.

Design intent is recorded under [the hoard prop]: three visually distinct coin types, several of each, mixed together for players to sort; the cache-marked pile must weigh `370.56 g` exactly (crossed-out final digit → `370.5` → upside down → `SOLE`). Nothing has been modelled or printed yet, and this is blocked on PP-037's scale purchase — the replacement scale (capacity above 370.56 g, 0.01 g resolution) needs to be bought and tested before a target per-coin weight and count can be fixed. **Still needed:** design three distinguishable coin faces, choose a coin count and per-coin weight for the target pile that hits `370.56 g` exactly (controlled ballast if the print material alone can't hit it), print, and confirm on the actual replacement scale that the target pile reads correctly and the two decoy piles read distinctly different numbers.

## Design notes (PP-037: Revised · values, not weight)

**Coin puzzle uses a tally; no scale purchase.**

The chosen coins must total 3705 in fictional values. Calculator or four-wheel counter replaces the scale. PP-026 tracks the display choice; PP-037 tracks the coin inventory and selection/value marks.

**Superseded specification · before 22 September 2026**

PP-037 Test

Aud’s mixed coin hoard and replacement-scale specification.

**Decided chain:** Aud’s journey map supplies a four-digit treasure-route code to release the hoard. All coins arrive mixed at once: several coins from each of three distinct types. The final treasure square selects one type, so players sort the hoard and weigh only that pile. Its target total is `370.56 g`. Esjuberg’s drawn display crosses out the final `6`, leaving `370.5`, which reads `SOLE` upside down for the four-letter lock.
**Hardware constraint:** the current 200 g / 0.01 g pocket scale cannot measure this result. Buy and test a scale with capacity above 370.56 g and 0.01 g resolution. Only after choosing the actual scale and coin blanks should the individual coin count/design and any controlled ballast be set; confirm that the selected pile repeatedly reads the target and the two decoy piles are distinct.

## Starting state

Not recorded yet.

## Reset

Put every coin back, not only the ones that made the treasure.

## Replacement

Not recorded yet.
