# Project Handoff

Last updated: 2026-09-10 by Claude Code

## Current Task and Status

Norse postcard sparse-set assignment, the next content step flagged by the prior handoff. Two threads were live at session start (this Norse one, and an uncommitted, in-progress Aurora map recolor); the user was asked which to continue and chose Norse. The Aurora changes were left untouched.

Task: decide which of the 18 postcards carry a price, extra text, a tilted stamp and an anomaly stamp (the corpus worksheet in the Design spec tab), per the "Next steps, in order" list. This is a structural design decision — which card gets which channel — not the actual digits/letters/directions those channels will print, which stay open pending two lock conflicts (see Open Design Issues).

## Files Changed

- `NorseBackpack/Norse_Brainstorm.html` — in the Design spec tab:
  - The corpus-rendering script (bottom `<script>` block) now carries a `tags` array per postcard instead of a generic unassigned slot, plus a `tagMeta` color/label map for the four sparse channels.
  - The "18 cards" card's legend, lede and worksheet now show the real assignment, plus a paragraph explaining the reasoning (see Decisions).
  - Added `.pc.quiet` / `.quiet-note` CSS, scoped under `#design`, for the three cards that carry no sparse element.
  - "Next steps, in order" step 1 marked done, with a note that only the card→channel mapping is decided, not the printed values.
  - "Still open" (Design spec tab) and "Still open" (Props & choices tab) updated: removed the now-resolved "which cards are active" items, added the two lock conflicts (tilted-stamp vs. hnefatafl both feeding a directional lock; HRAFN vs. cryptex) and a note that anomaly wrong-trail motifs are fixed only for Kyiv so far.
- `HANDOFF.md` — this handover.

No other file was modified. The uncommitted Aurora changes (`Station_Aurora_Map_Base.png`, `Station_Aurora_Vector.svg`, `convert_dxf_to_svg.py`, `Station_Map.html`, and the Aurora paragraph in `AGENTS.md`) were left alone and are not part of this session's work.

## Decisions

The 18-card assignment (card numbers per the trail order already in the page):

- **Price (4, feeds a 4-digit lock):** 02 Markland, 07 Winchester, 12 Esjuberg, 15 Kyiv.
- **Extra text (5, feeds a word lock):** 01 Helluland, 05 Rouen, 09 Roumare forest, 10 Dögurðarnes, 16 Hedeby.
- **Tilted stamp (4, feeds a directional lock):** 03 L'Anse aux Meadows, 06 Bayeux, 13 Oslo, 18 Asia Minor.
- **Anomaly stamp (3, selector only):** 04 Châlus, 11 Hvammur, 15 Kyiv (wrong motif = Leif's ship series, matching the doc's own worked example).
- **Quiet (3, no sparse element):** 08 Battle, 14 Staraya Ladoga, 17 Sicily.

Reasoning: Leif's trail (the three cards already built) was given one card of each *data*-bearing channel (price, text, tilt) so the already-printed trail teaches all three before players meet the rest — but no anomaly card, since Leif's own ship motif is the one borrowed to mislabel Kyiv, keeping the "true" series clean everywhere it actually belongs. Kyiv is the one deliberate double-duty card (price + anomaly), placed where the anomaly already draws attention, per the design doc's own "overlap belongs on the last postcard puzzle" guidance and its own Kyiv/ship-anomaly example. The two 3-stop trails (Leif, Aud) have no spare card and so are fully loaded; the two 6-stop trails (Rollo, Harald) each keep a couple of genuinely quiet cards.

This assignment surfaced (and is recorded, not resolved) two real conflicts the sparse-channel design creates: (1) the tilted-stamp channel and the hnefatafl board both produce a directional lock — either the corpus needs a second one, or tilt should feed something else; (2) only Kyiv's anomaly wrong-motif is decided — Châlus and Hvammur still need one assigned.

## Checks

- Opened `Norse_Brainstorm.html` in the browser, navigated to the Design spec tab.
- Verified via `document.querySelectorAll` that the corpus renders exactly 18 cards with the correct per-category counts (price 4, extra text 5, tilted stamp 4, anomaly stamp 3, quiet 3) and that series motif/postmark still show on all 18.
- Confirmed CSS scoping held: after the edit, the Prototype & tests tab's pre-existing `.runes` element still computes 35px/block/7px letter-spacing, unchanged.
- No print test, no prop built — unchanged from before, this session touched only the corpus worksheet's data and surrounding text.

## Next Action

Per the (now-updated) "Next steps, in order" list in the Design spec tab: **design the four stamp series** — one motif family per trail (a ship series for Leif, a Byzantine series for Harald, etc.), distinct enough to read at a glance across 18 cards on a table, plus the wrong-trail variant needed for each of the three anomaly cards (Kyiv's is fixed as Leif's ship motif; Châlus and Hvammur still need theirs chosen as part of this step).

## Open Design Issues

- The tilted-stamp postcard set and the hnefatafl escape both now feed a directional lock. Needs a second directional lock in the design, or one of the two reassigned to a different lock type.
- HRAFN is assigned to the five-letter lock but also fits a five-ring cryptex; only one of the two can have it.
- Anomaly wrong-trail motifs: Kyiv is decided (Leif's ship series). Châlus and Hvammur are not yet assigned a wrong series — that's part of the next step (stamp series design).
- The actual digits, letters and directions carried by the price, extra-text and tilted-stamp cards are unassigned — deliberately, since they depend on the two lock conflicts above.
- The 18-card postcard set needs its artwork re-rendered, not rescaled (1536×1024 current vs. 1500×1050 target at true print size). `SIZE`/`PAGE` in `Postcards/build_postcard_collection.py` must change together.
- The hnefatafl board layout (a provably unique four-move escape) has not been generated.
- The final map mechanic (pins/cord vs. overlay) is undecided by choice; needs prototyping at print size.
- The red filter needs a home-printer colour test.
- The wording of the three redirect clues is unwritten.
- Every historical claim in the Design spec tab needs source-checking before it reaches a prop.
- Carried over from earlier sessions: postcards 02 and 03 still need their message and travel date; the main compartment's opening mechanism and answer are still undecided.

## Aurora note (not this session's work, left as found)

There are uncommitted changes recoloring `Space Station Aurora/Station_Map.html` (and its SVG/PNG/converter script) to a blue-compartments/amber-external/grey-structural scheme, matching a new paragraph added to `AGENTS.md`. That work was in progress before this session and was deliberately not touched — the user chose to continue the Norse thread instead. It's still sitting unstaged in `git status` and may not be finished (not verified this session).
