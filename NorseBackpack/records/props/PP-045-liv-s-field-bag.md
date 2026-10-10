---
id: PP-045
title: Liv's field bag
type: prop
# idea | candidate | decided | built | parked
status: decided
# physical | printed | digital
form: physical
# make | buy | print | 3d-print
source: buy
# The play-test page shows the body's "## Player sees" section, or this prop's image asset.
# Where the player gets it: start (in the backpack) or the puzzle whose lock releases it, e.g. PZ-004
found_in: start
# Physical pocket/container or location; availability remains in found_in above.
container: The backpack itself
# Any related record IDs, e.g. [PZ-002, Q-004]
links: []
# Set to an ID when this record is replaced. It then moves to the Parked tab.
superseded_by:
tags: []
---

## From the old Props & specs tab

Prop kit · folded in from the Props & choices tab, 17 Sept 2026

### Make the bag feel like it belongs to her

#### Core reusable prop kit

- The museum ticket — fictional Viking Museum of Brattahlíð (was L’Anse aux Meadows until 28 Sept 2026), decided (PP-024): ordinary admission ticket front, A–Z visitor index on the back that keys the beasts-on-the-chart lookup.
- The raven’s flights card and one four-digit lock set to 2648 directly on the board pouch. HRAFN is the decoded five-perch itinerary. Cryptex and extra keyed closure are superseded (PZ-012, PP-038).
- An 11 × 11 printed hnefatafl board with 23 pieces: 16 dark, 6 light and a distinctive king. The user can 3D-print pieces. Supply the fixed-piece three-move challenge rules with H1; no captures or jumps.
- An admission ticket from the (invented) **Hnefatafl Museum, Oslo** — arrives with the Oslo postcard on Harald's trail. Explains the real historical game (light defenders, dark attackers, sandwich-capture), not this puzzle's own house rules. Its back panel also carries a mirrored offset holding the right-hand strip of the board setup. Built: `Props/Hnefatafl/build_ticket_pdf.py`.
- The back of Harald's Oslo trail map (both faces built, Q-020; the earlier “panel not yet composited” status is superseded), carrying the rest of the setup plus a printed stain where the wet ticket lifted the ink. That map cannot go in an opaque sleeve — laminate both sides instead. A standalone stand-in for this panel is built: `Props/Hnefatafl/build_board_setup_pdf.py`.
- Four printed journey maps, one per trail — letter size, printed and laminated at home in gloss pouches, drawn on with **wet-erase** marker and wiped to reset (PZ-013). No pins, cord or overlay. **All four are now built** by `NorseBackpack/TravelMap/build_trail_maps_pdf.py`. Harald's sheet (Q-020) was the last — his two regional stops now resolve to named, sourced settlements (Syracuse; Patara, explicitly flagged as an illustrative representative point rather than an attested site). Each sheet carries **a title only** — the projection and coastline credit was dropped as well (Natural Earth is public domain and asks for no attribution; provenance stays in the build script and `TravelMap/README.md`). No trail name, no numbering, no instructions (PZ-013), and stops are unmarked so players find them by name. Answer keys build from the same script, so a key cannot drift from the sheet it answers. Label provenance and an invented-name incident are tracked in Q-025.
- ~~A fifth sheet: Liv’s gridded excavation site plan, in the last container with the ticket.~~ Dropped 26 Sept 2026 (old page ST-05) — no fifth sheet.
- Hand-written notes made as replaceable inserts or reusable facsimiles, with a clean master kept for reprinting.
- A set of 18 dated postcards, one per route stop — the spine of the game, released a few at a time. Only the first card starts outside the bag.
- The branch-rune cipher now lives on Harald's trail map itself, not on a separate stick or museum label — see PZ-012 and [Props & specs].
- A comb with broken teeth, used as a grille over postcard messages.
- Mixed coins, a merchant’s fictional value key, and a calculator or four-wheel treasure tally. No scale is required (PP-026/25).
- Reader tools: a magnifier~~, a red acetate filter, and a UV pen with a blacklight~~. **Red filter and UV dropped, 25 Sept 2026** (old page PR-03).
- Replica object labels, family record cards, saga strips, a travel wallet and a fictional boarding pass.

Design for repeat play: no writing on irreplaceable props, all loose pieces inventoried, and every puzzle given a clear reset state.

#### Candidate prop links

- [Vansky 12 LED UV blacklight flashlight](https://www.amazon.ca/gp/product/B011LPWXV6) — ~~candidate for the UV pen/blacklight reader tool above. Confirm battery type and light footprint before committing.~~ Not needed: UV dropped 25 Sept 2026.
- [90mm handheld magnifying glass, wooden handle](https://www.amazon.ca/gp/product/B0FKHHNFJP) — candidate for the magnifier reader tool above.
- [Lewis N. Clark luggage tag](https://www.amazon.ca/gp/product/B00CLUM8SE) — **two are now needed**, both attached to the bag. Each insert is a fictional hotel address in Liv’s hand under the tag’s printed “if found” line; its street number is half the opening code (PZ-001). Print masters in `NorseBackpack/Props/build_luggage_tag_inserts_pdf.py`. Candidate purchase only — not yet bought or test-printed (PP-023).
- [Diyife mini digital pocket scale (200g/0.01g)](https://www.amazon.ca/Diyife-Precision-Palm-Sized-Digital-Medicine/dp/B0GDZD6536) — **superseded, do not buy for this puzzle.** Coin values and a treasure tally replace weighing (PP-026/25).
- [YIWEN handmade leather portfolio, 3-ring binder + zippered padfolio](https://www.amazon.com/Handmade-Portfolio-Zippered-Professional-Organizer/dp/B08DMJZB3B) — candidate for storing the four laminated trail maps flat instead of folded. Has a wraparound zip closure plus a separate inner zip pocket (two zippers, not one), closer to the multi-zipper meeting-folder idea than a single-zip padfolio.
- [Rustictown Kingsman leather padfolio](https://www.rustictown.com/products/business-leather-padfolio-leather-portfolio-professional-organizer-gift-for-men-women-durable-leather-padfolio-easy-to-carry-with-a-zippered-closure-many-slots-compartments-holders) — wraparound zip plus an extra inner zippered pocket, 4 large pockets and a notepad holder. Similar shape to the YIWEN, different look and price point.
- [mygreen A4 document folder, multiple compartments](https://www.amazon.com/mygreen-Document-Compartments-Organizer-Management/dp/B072FQMDWW) — plain file-folder style rather than a leather padfolio, cheaper, keeps A4 sheets flat. Fallback candidate if the padfolio look isn't needed.

Candidates only; none are confirmed purchases or assigned to a final puzzle step. The three folder/portfolio links are for flat map storage, not matched to a specific puzzle step yet.

**Lock purchases to consider once a mechanism needs them** (see "Already at home" for what's already on hand): a directional lock — per the Options tab, only worth buying once something actually feeds it, and nothing does yet; more letter locks — worth it once the 5-letter `KAMBR` lock (or a new 4-letter answer) is decided.

#### Candidate backpack

[View the Koolehaoda vintage canvas backpack](https://www.amazon.ca/koolehaoda-Backpack-Business-Rucksack-L-Coffee/dp/B07VST6YSY)

The listing describes the L-Coffee version as a canvas-and-leather-style 35 L backpack sized 46 × 32 × 20 cm, with a main compartment and several pockets. Its field-bag look suits the story.

Candidate only. Before purchase, confirm current price and availability, then test the actual lock attachment points, pocket access, prop fit, hardware durability and reset workflow. Seller measurements and claims have not been independently verified.

#### Candidate internal pouch

[View the FunOwlet canvas zipper tool bag, 4-pack](https://www.amazon.ca/Utility-Canvas-Zipper-Tool-Bags/dp/B08396NPRM)

A set of four heavy-duty canvas zipper pouches with carabiner clips, meant to fit inside the main backpack. Note: listing describes plain canvas, not wax/waxed canvas. Each pouch would be locked individually (e.g. a small combination lock through the zipper pull) rather than the set sharing one body with built-in compartments.

Candidate only. Confirm pouch sizes and canvas weight fit the props planned for each stage, and test that a chosen mini lock actually passes through the zipper pulls before committing.

#### Already at home

- **1× Master 4-letter combination lock.** No current mechanism outputs 4 letters — the padlock in use is 4-digit (decided) and the word lock candidate is 5 letters (PZ-010, `KAMBR`). Usable if a 4-letter answer gets designed; nothing calls for one yet.
- **Several simple 3-digit locks.** Direct fit — three 3-digit codes already exist in the game (`231`, `582`, `427`).
- **Several 3-digit locks with coloured dials** (red/green/blue, order differs per lock). No puzzle currently outputs a colour order — would need a new mechanism designed around it.
- **1× locker-style lock** (3 numbers, turn one way then the other). A different physical verb from dial locks — candidate for the "second mechanical, non-lock moment" old page PR-06 already wants but hasn't picked (currently just lithophane/shadow-caster/bearing-disc candidates).
- **Bevelled base** (for angles on a map). Matches the bearing-off-the-scale idea noted as a superseded alternative in old page PZ-10 — shelved for being heavier than needed there, not rejected outright. Could resurface on a different map.
- **3-sided architect's scale ruler** (6 scales). Fits the multi-scale map set (Q-024: each trail sheet is a different km-per-square) — candidate tool for a "read the real distance" beat.
- **Recollections 8.5×11in 65lb cardstock, Apricot Crush** ([Michaels, 50 sheets](https://canada.michaels.com/product/85-x-11-65lb-cardstock-paper-pack-by-recollections-50-sheets-10746459)). Already earmarked for the paper props, not the maps — see the cardstock-colour reasoning above (full-coverage map illustrations can't take coloured stock without losing the animal-identifying contrast).
- **Normal (plain copy) paper.** On hand, unassigned to any prop yet.
- **Heavy white cardstock** (heaviest weight on hand, exact lb unconfirmed). Candidate for anything wanting more rigidity than 65lb — e.g. the museum ticket or a lock-adjacent prop that needs to feel sturdier than a postcard.
- **Access to a 3D printer.** Candidate for the four-wheel treasure tally (PP-026) and the hnefatafl pieces. (First noted for the five-ring rune cryptex, superseded 22 Sept 2026.)

Inventory only — nothing here is assigned to a puzzle yet. Recorded so future sessions know what's already on hand before buying more.

## Starting state

Not recorded yet.

## Reset

Not recorded yet.

## Replacement

Not recorded yet.
