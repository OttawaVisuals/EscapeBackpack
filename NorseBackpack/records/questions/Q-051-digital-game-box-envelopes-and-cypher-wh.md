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

**18 Oct 2026: V2 built, V1 kept (Claude, designer asked for "a V2 of the digital game to reflect the new game").** New files beside the old game, which still plays the backpack: `Digital/Raven_V2.html`, `raven2.js`, `raven2.css`, `raven2-data.js`, `table-layout2.js`, `raven2-sizes.js` and `build_raven2_assets.py` (renders the live print PDFs to `Digital/assets/v2/` and writes each prop's real size). Tests: `node --test NorseBackpack/Digital/raven2.test.cjs` (13 pass).

Choices made for the four questions above (V2 defaults, easy to change):
1. **Code entry:** an on-screen cypher arm: four rings (0-9, blank, the nine letters; type or ▲/▼), four code windows, four rune windows (same rune maps as `build_cypher_wheel_pdf.py`, seed 1021; all 13 labels checked against PR-007). Text copied from the printed arm ("1 SET THE CODE", "2 READ THE RUNES", "3 Open the envelope with these runes", the blank-first line).
2. **The box:** 13 rune-marked envelopes loose in a box in the side panel, in a fixed mixed-up order; the player clicks the one whose runes match the wheel. Opened ones lie open and empty.
3. **Wrong codes:** the wheel shows their runes and says whether any envelope carries them; a wrong try is logged only when an envelope is clicked.
4. **Decoys:** none yet (Q-050 is undecided).

Also in V2: the new order and codes (1021, BOOK, 1576, MEAD, 532, 562, 4865, SOLE, 1486, 120, 2134, 2648, 1972); hints and solutions word for word from the puzzle records; L1 and Liv's notes card on the table at the start; the magnifier button appears when envelope 2 opens; Liv's printed ruler card (LONGSHIP edge, Flip for SPEAR, each turning about its own 0); 19 dark Hnefatafl pieces; envelope 12 gives the four hop-ticket pages and three flight bookings; envelope 13 the plane ticket, Liv's last letter and the medallion. No luggage tags or journal page.

Not done: the rune glyphs rely on the viewer's fonts (Segoe UI Historic / Noto Sans Runic); not published (`escapepack-site/tools/build_leif.cjs` still ships V1); the online AUD confirmation from Liv's last letter; play-test on a touch device; the 120 reading on the ruler was checked by size only (the card is drawn at its printed size), not by measuring the two map icons on screen; room play (Play together) untested for V2.
