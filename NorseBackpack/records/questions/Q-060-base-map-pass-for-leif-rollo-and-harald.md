---
id: Q-060
title: Base-map pass for Leif, Rollo and Harald sheets (towns, names, dots)
type: question
# open | answered | parked
status: answered
# Records this question is about, e.g. [PZ-003]
about: [PZ-006, PZ-005, PZ-007, PZ-008]
# Leave empty while open
answer: "Applied 16 to 17 Oct 2026 to Aud, Leif, Rollo and Harald (single names, clustered towns dropped, bold dots and names). See the dated notes."
# Any related record IDs, e.g. [PZ-002, Q-004]
links: [PZ-006, PR-007]
# Set to an ID when this record is replaced. It then moves to the Parked tab.
superseded_by:
tags: []
---

The question, and the options on the table.

Opened 16 Oct 2026 (designer). The Aud sheet got a base-map pass (PZ-006): one name per place, fewer clustered towns, dots moved ashore, bolder dots and names (`TravelMap/build_trail_maps_pdf.py`, settings `display_names`, `omit_towns`, `PLOT_NUDGE`, `bold_towns`). The same pass is wanted on the other three sheets. **Remind the designer when working on the puzzles that use these maps** (Leif and Rollo maps, Harald's map; the Rollo word-lock icons and their leader towns).

**Audit and proposal, 16 Oct 2026 (not yet approved or applied):**

- **Leif (24 places):** single name Brattahlíð (the ticket's name), not Qassiarsuk. Drop St. Anthony (6 pt from L'Anse aux Meadows), Red Bay, Blanc-Sablon, Narsarsuaq (1 pt from Brattahlíð), Twillingate, Hopedale. Dots in the sea (Port aux Basques, Cartwright, Rigolet, Nain, Nuuk, Sisimiut, Paamiut) are about 1 pt at this scale: leave. Battle Harbour (a stop, 8.2 km out, 2 pt) stays.
- **Rollo (31 places):** no double names. Drop Portsmouth (in the sea, 19 pt from Winchester) and Saint-Malo (in the sea). The icon towns (Manchester, Eindhoven, Troyes, Saumur, Vichy, Montauban) are leader-line targets for the word-lock icons and stay.
- **Harald (16 places):** single names Staraya Ladoga, Novgorod, Constantinople (the card name), Solund. No clusters; sea dots under 1 pt, leave. Open question: Denmark and Sweden print as town dots; propose dropping them, if no puzzle uses them (not decided).
- **All three:** apply the bolder dots and names (`bold_towns`).

The designer's reply to the proposal was to record it and come back to it when working on those puzzles.

**Leif's sheet applied, 16 Oct 2026 (designer approved):** dropped St. Anthony, Red Bay, Blanc-Sablon, Narsarsuaq, Twillingate, Hopedale; single name Brattahlíð; bolder dots and names (`omit_towns`, `display_names`, `bold_towns` in the `leif` config). Sea dots and Battle Harbour left as proposed. Print and answer PDFs and web copies rebuilt. Looks fine; the bigger names are a little tight around Corner Brook, Gander and the GULF OF ST. LAWRENCE label. **Still to do: Rollo and Harald sheets (remind the designer when working on their puzzles).**

**Rollo's sheet applied, 16 Oct 2026 (designer):** Portsmouth and Saint-Malo dropped, Walcheren kept, icon towns kept, bolder dots and names, fixed label for Roumare forest. Done: Leif, Rollo. **Still to do: Harald (remind the designer at its puzzles).**

**Harald's sheet applied, 17 Oct 2026 (designer):** single names Staraya Ladoga, Novgorod, Constantinople and Solund (the names the cards use); Denmark and Sweden dropped (country dots no puzzle or card uses; H4's Fun Fact mentions Denmark in text only); bolder dots and names (`omit_towns`, `display_names`, `bold_towns` in the `harald` config). No sea dots moved (all under 1 pt at this scale). Print and answer PDFs and web copies rebuilt; the shield icon (I10) and the branch-rune stems are untouched and no label collides with them. **All four sheets are done; this question is closed.**
