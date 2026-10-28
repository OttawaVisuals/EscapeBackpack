---
id: Q-048
title: Hint and reset pages without lock numbers
type: question
# open | answered | parked
status: open
# Records this question is about, e.g. [PZ-003]
about: [PR-007]
# Leave empty while open
answer:
# Any related record IDs, e.g. [PP-046, PP-047]
links: [PP-046, PP-047]
# Set to an ID when this record is replaced. It then moves to the Parked tab.
superseded_by:
tags: []
---

**Hint titles decided 11 Oct 2026 (designer):** each step is named after the envelope players just opened: step 1 is "The box, before any envelope", step N is "Just opened <runes of envelope N−1>" (set in every puzzle's `hint_title`). Players always hold that envelope, so they can find their step. The cypher wheel builder warns if a code change leaves a title's runes stale.

Still open:
- **Kit wording:** the hint page still prints "4-digit lock" under each title and says "the lock you're working on" and "when a lock opens". That text is in backpack-kit (shared with Hiking, which does use locks), so it needs a per-project setting there.
- **Runes on phones:** they render on Windows (Segoe UI Historic). Not checked on iPhone or Android; if a phone lacks a runic font, titles show empty boxes. A web font (e.g. Noto Sans Runic) in the kit would fix that.
- **Reset page:** as below.

Opened 11 Oct 2026 with PR-007. Two published pages still assume padlocks:

- **Hint page** (escapepack.ca/help/norse/hints/): each step is titled "Lock N". Players no longer see lock numbers; envelopes carry runes. Options: title each step by the envelope players just opened ("After ᚷᛉᚦᛉ"), number the envelopes on their backs and say "Envelope N", or use the spoiler-free names proposed 10 Oct (luggage tags, two skies, carved comb…).
- **Reset page**: backpack-kit's reset page says "Close it with lock N … leave it showing 0000". For envelopes it should say "Put these back in envelope N and close it", plus one step to turn the cypher wheel away from the last code. That is a change to backpack-kit (sibling repo), not just to the records.

Until this is answered, puzzles keep `hint_title: Lock N` and `reset_display`. (Since 11 Oct 2026 the cypher wheel builder no longer reads `hint_title`.) Neither page has been rebuilt or republished since PR-007.

**Update 21 Oct 2026:** the kit (main) is envelope-based now, so the "4-digit lock" wording and the reset-page wording are no longer a kit problem. Norse hint and reset pages were rebuilt with it into `escapepack-site/help/norse/` (local copy, not published). Because the kit's cipher cannot express the rune wheel, each puzzle now carries `envelope_marks` (the runes its answer opens, copied from the cypher wheel builder; kit support added in `backpack-kit/kit.py`). If the wheel's seed or an answer changes, those must be regenerated. Open: hints 4 to 6 of PZ-001 are the superseded luggage-tag hints and show on the public page; phone rune fonts unchecked; Norse is not in `escapepack-site/backpacks.txt`, so production will not build it yet.
