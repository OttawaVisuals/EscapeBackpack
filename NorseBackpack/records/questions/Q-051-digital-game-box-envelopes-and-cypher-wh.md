---
id: Q-051
title: "Digital game: box, envelopes and cypher wheel"
type: question
# open | answered | parked
status: open
# Records this question is about, e.g. [PZ-003]
about: [PR-007]
# Leave empty while open
answer:
# Any related record IDs, e.g. [PZ-002, Q-004]
links: [PP-047, Q-050]
# Set to an ID when this record is replaced. It then moves to the Parked tab.
superseded_by:
tags: []
---

Opened 11 Oct 2026: the designer wants the digital game (`NorseBackpack/Digital/Leif.html`, published by `escapepack-site/tools/build_leif.cjs` to `/play/norse/leif`) updated to the box-and-envelopes format (PR-007).

What the digital game has now (read 11 Oct 2026, not changed):

- An opening screen with a battered backpack: "Every pocket is locked", "Unbuckle the bag".
- A side panel "Your backpack" with pockets, a lock count, and a padlock dial (digit or letter wheels, ▲/▼, typing) beside the pocket that is current.
- How-to-play and the certificate talk about pockets, padlocks and "opened every pocket of her backpack".
- About 150 mentions of locks and 70 of bag/pocket/pouch across `leif.js`, `leif-data.js` and `Leif.html`.
- The data file's header says its sequence is the old PC-18 order (29 Sept 2026); whether it already follows the 9 Oct lock order was not checked.

Choices to make before changing it:

1. **Code entry:** an on-screen copy of the cypher wheel (turn four rings, read the runes, click the matching envelope), or keep a plain code entry that names the envelope it opens.
2. **The box:** a top-down box with 13 rune-labelled envelopes that open in place, or a list of envelopes in the side panel.
3. **Wrong codes:** show their runes (no envelope matches), or a simple "nothing happens".
4. **Decoys** follow Q-050.

Kept until then: the digital game still plays as the backpack version.
