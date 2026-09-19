# Superseded — Aud map style trial PDFs, 19 Sept 2026

Not shelved for a design reason — these are just intermediate renders from a same-day styling
pass (Codex session, "Aud map Option A trial and label avoidance", see `HANDOFF.md`) that never
got folded back into the canonical filenames. Kept here so the iteration history isn't lost, not
because any of them individually needs revisiting.

## What's here

- `Trail_Map_3_Aud_OPTION_A_Print.pdf` / `_ANSWER.pdf` — first label-avoidance pass, 12:20.
- `Trail_Map_3_Aud_HYBRID_Print.pdf` / `_ANSWER.pdf` — intermediate, 14:11.
- `Trail_Map_3_Aud_REFINED_Print.pdf` / `_ANSWER.pdf` — final pass, 14:35. This is the one the
  user picked as "the latest version."
- `Aud_Map_Legend_Options.pdf` — a legend-styling comparison sheet, undated decision.

## What's canonical instead

`aud_layer.py`, `build_trail_maps_pdf.py` and `Aud_Map_Designer.html` on disk already carry
REFINED's changes (that's what actually produced it) — nothing needed reverting there. The
committed `output/pdf/Trail_Map_3_Aud_Print.pdf` and `Trail_Map_3_Aud_ANSWER.pdf` were re-rendered
from that current script state on 19 Sept 2026, right after this move, so they should match
REFINED's content. `aud_features.json` (the route geometry the `521` code depends on) was not
touched by any of this — it's unchanged since 18 Sept.

## Also moved here

- `Trail_Map_1_Leif_Print_UPDATED.pdf` — dated 12 Sept 2026, a week older than the canonical
  `Trail_Map_1_Leif_Print.pdf` (18 Sept 2026) that `Norse_Brainstorm.html` actually links. Despite
  the filename, it is the stale one.
