# Shelved — Aud's split-panel treasure map (PZ-17), 17 Sept 2026

Parked, not deleted. The approach was sound on its own terms and the checks passed; it was
shelved because the *concept* was rejected, not because it broke.

## What this was

Aud's trail sheet turned landscape and split into two panels: the existing full-region Iceland
map on the right, and on the left a new zoomed, non-georeferenced "Dalir / Hvammur" survey panel
with its own 6×10 grid. The treasure hunt lived entirely in that left panel.

The mechanic went through two generations:

1. **Digits baked into the artwork** (superseded same day). Four landmark icons each hid a digit
   — four wheel paddles, eight carved marks — reading as `4816`. It failed because the same
   drawing always yields the same digit, so placing a chapel twice meant both chapels carried a
   `6` and the decoy was decorative.
2. **Survey plot numbers** (the version shelved here). Every grid cell carried a small two-digit
   plot number; players followed a six-hop clue chain and the lock code was the **sum** of the
   seven stops' plot numbers — `467`, on a three-digit lock. This decoupled art from puzzle, so
   icons could repeat freely.

## Why it was shelved

- Two panels at two scales on one sheet, when one map was wanted.
- Landscape, when portrait was wanted.
- **Isolated object icons were the wrong vocabulary.** A treasure hunt wants clues like "follow
  the river upstream to the farmer's hedge", and a hedge is a long sinuous *line* symbol, not a
  34 pt stamp. Same for a paved road, a wall, a field boundary. The icon set could not express
  the clues the hunt actually needs.
- The drawn terrain lines read poorly, and the panel lacked the furniture that makes a map feel
  real — contours above all.

## What is in here

| File | What it is |
| --- | --- |
| `aud_detail_panel.py` | The single source for the panel: plot numbers, landmark placements, the seven-stop route, and the check that guarded them. Runnable on its own. |
| `shelved_detail_panel_drawing.py` | The drawing code lifted verbatim out of `build_trail_maps_pdf.py` — `_aud_offset`, `_aud_glyph`, `_aud_hachures`, `draw_aud_detail_panel`. Depends on `AUD_PANEL`/`AUD_PAGE`/`AUD_MAIN_*`, which were removed from the build script at the same time. |
| `normalize_aud_vignettes.py` | Alpha threshold, enclosed-hole fill, flatten every visible pixel to `#6D528B`. **Generic and reusable** — nothing about it is specific to the shelved design. |
| `Art/Aud_*_v2.png` | Ten finished vignettes: ford, mill, falls, fold, chapel, cairn, stone, naust, farm, birch. Generated from the prompt set recorded in `PZ-17`. These were completed and wired in immediately before the concept was shelved, so they have never been used in a delivered sheet. |
| `Art/Aud_*_v1.png` | The four rejected first-pass icons (digits baked in). Superseded by the v2 set even within the shelved design. |
| `Art/Sources/` | The unprocessed ImageGen renders behind both sets. |

## What is worth keeping if the design is revisited

- **The two invariants.** They are properties of *any* sum-based route, not of this layout:
  every stop must be a different landmark type, because a sum is order-independent and two
  same-type stops swap for free; and the numbering must be verified against every same-type
  substitution, with nothing wrong landing within 15 of the answer. `aud_detail_panel.py`
  enforces both and its `check()` is portable.
- **The ticket-as-record-card prop.** The museum ticket's reverse is the seven-row
  `STOP / SITE / PLOT No.` form with row 1 pre-filled by hand. It is independent of how the map
  is drawn, and is described in `PZ-17`.
- **The clue-chain constraints:** never name a grid reference, and describe by position rather
  than appearance.
- **The v2 vignettes**, if the replacement design still wants point symbols alongside its line
  and area symbols.

## Related

`NorseBackpack/Art/Diagrams/Diagram_Aud_Map_Split.svg` is deliberately **not** moved here — it is
linked from `Norse_Brainstorm.html`, and `AGENTS.md` requires linked paths to stay stable. Its
caption in the page marks it outdated.
