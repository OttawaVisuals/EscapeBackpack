---
id: Q-062
title: Envelope 12: new props for the Patara envelope
type: question
# open | answered | parked
status: answered
# Records this question is about, e.g. [PZ-003]
about: [PZ-012, PZ-013, PR-007]
# Leave empty while open
answer: Envelope 12 = H6 (large raven, new text) + travel tickets (18 hop tickets, 3 flight tickets); small raven on the 18 real cards, decoys unmarked; envelope 13 = plane ticket, final letter (AUD puzzle), medallion (17 Oct 2026)
# Any related record IDs, e.g. [PZ-002, Q-004]
links: [PP-021, PP-039, PP-040, PP-041, Q-057, Q-061]
# Set to an ID when this record is replaced. It then moves to the Parked tab.
superseded_by:
tags: []
---

The question, and the options on the table.

Opened 17 Oct 2026 (designer), at the start of the envelope 12 text pass, to be worked in its own chat.

**What envelope 12 holds today** (opened by `2648`, the answer to PZ-012): H6 · Patara (PP-021), the three transition tickets (PP-039), Liv's journal page “Family iconography” (PP-040) and the family logo and crest note (PP-041). H6 sets up the last puzzle (PZ-013, the route hidden in plain sight; envelope 13 holds the plane ticket and letter and the adventure medallion).

**Decision (designer):** the H6 postcard is fine as it is; the **props need re-working, new props for it**. What the new props should be is still open and is the job of the new chat.

**Current props, for reference:**
- *Transition tickets:* three itinerary receipts (Qikiqtarjuaq to Iqaluit to Ottawa to Amsterdam to Walcheren is the first, then the legs between Rollo, Aud and Harald); only dates, places, carriers and references, no prose. Since Q-054 they show the journeys' order (Leif, Rollo, Aud, Harald), which is also the play order, as story, not as the solve (PP-039).
- *Liv's journal page:* “Family iconography. Everything I could find of ours, finally drawn out properly. To retrace my steps, follow only the places that carry one of our family's marks. On each journey I met them in the order written under each drawing.” Under it, the symbol (three: raven, longship, sun-wheel) and the crest (six: bearded axe, round shield, wolf, anchor, drinking horn, valknut). The card marks on the postcards are crops of these drawings (PP-040, PP-041).
- *H6 · Patara* message: “Patara is the last stop of my travels for now. / I had so much fun exploring the Vikings and Norse travels! / For your university summer break, I would love for you to join me on my next adventure. You have one more puzzle to solve and you will get your rewards! / Now you should have all you need to retrace my steps!” Fun Fact: “Archaeologists discovered a Viking sword at the Patara excavation site. It almost certainly belonged to a soldier of the Varangian Guard, of which Harald was a prominent member.”

**Small items pending for H6 (offered, not applied):** Fun Fact softened to “A Viking sword was found at Patara in 2018, possibly from a soldier of the Varangian Guard.” (not source-checked, the 2018 find is from memory) and the held Liv line “Nearly there. I knew you'd get this far.” (Q-061). Apply them in the new chat if still wanted.

**Not started.**

**17 Oct 2026 (designer): direction chosen, tickets built.** Replaces the family-iconography idea (symbol, crest, six crest marks):
- **Only the raven remains** as family iconography. All 18 real stops get a raven mark on their postcard (a simple, sketch-style raven); the 4 decoys carry none. Liv's note says to retrace only the steps relevant to our family history. Codex redraws two ravens: a large detailed hand-drawn one for the last postcard (H6), with Liv's note that this is the family's icon, and a smaller, simpler one for the card marks. **Not started** (waiting on Codex; H6 wording of the note not written).
- **The order now comes from tickets, not marks.** One ticket per hop, **decoys included**, grouped into one prop per journey (Leif's flights and ferry, Rollo's rail pass, Aud's Iceland buses, Harald's mixed) plus the three journey-to-journey flight bookings on one prop. Hop tickets carry only from, to, mode, service number and "OPEN" for the date, no extra clues. Built: `Props/Tickets/build_hop_tickets_pdf.py` to `NorseBackpack/Print/_pdf_source/Hop_Tickets_Print.pdf` (4 pages, stubs in a scrambled print order). Invented operators: Nordic Air, Viking Rail, Longship Buses, Longship Ferries.
- **Decoy positions (designer approved):** Leif: L'Anse aux Meadows, Battle Harbour, Brattahlid (decoy), Qikiqtarjuaq. Rollo: Walcheren (decoy), Chalus, Rouen, Bayeux, Winchester, Battle, Roumare Forest. Aud: Dogurdarnes, Hvammur, Bjarnarhofn (decoy), Esjuberg. Harald: Oslo, Staraya Ladoga, Kyiv, Constantinople (decoy), Hedeby, Aci Castello, Patara. Plot: `Art/FinalPuzzle/Journeys_With_Decoys_Draft.png`.
- **Digit order** 1-9-7-2 comes from the flight bookings (journey order). The journal page and crest note are to be replaced by the raven note (not built).
- **Envelope 13:** still opened by 1972; holds the plane ticket, the medallion and Liv's letter, with a line saying she thinks she found one of our ancestors and leaves a final puzzle whose answer is **AUD** (Q-058). The AUD puzzle is **not designed and may not be built**; the letter wording is the designer's to give.
- **Still pending for H6:** the large raven and the "retrace my steps" note; the Fun Fact and "Nearly there" items.
- **Open:** ~~dates on hop tickets (none, "OPEN")~~ **answered 19 Oct 2026: every ticket now has a date, PP-039**; passenger name ERICSON / LIV unchanged (Q-058: points at Leif, not Aud); carriers on the three transition receipts renamed.

**17 Oct 2026 (designer, Q-062): raven art chosen and wired in.** Large raven = `Art/Raven/Raven_Profile_Knotwork_Pencil_v2.png` (H6, beside the signature, 82 pt). Small raven = `Art/Raven/Raven_Profile_Pencil_28pt_Frame_v1.png` (pencil sketch in a thin knotwork ring, 28 pt, under the postmark) on the 18 real cards; the 4 decoys carry no mark. `Postcards/postcard_marks.py` and `build_postcard_H6_pdf.py` updated, all 22 card PDFs rebuilt. Not yet written: Liv's raven note and the "retrace" line on H6.

**17 Oct 2026:** H6 text and Fun Fact applied, Fun Fact source-checked (PP-021). The held line “Nearly there. I knew you'd get this far.” was not used. Still to build: the envelope 13 letter (AUD teaser) and the optional AUD puzzle.

**17 Oct 2026 (designer): envelope 13.** Plane ticket (Ottawa to Stockholm, summer 2027) and Liv's letter built (PP-043); medallion printed and works (PP-044). The AUD reveal is the letter's puzzle: the four unmarked decoy cards, only AD (Aud's trail) says it feels like family. Answer confirmed on the online page (not built). Possible weakness: LD says Leif “actually grew up” at Brattahlid; not tested with players.

**Summary of the day's decisions (17 Oct 2026):** (1) only the raven stays as family iconography; crest, symbol marks and journal page retired (PP-040, PP-041 parked). (2) Stop order comes from tickets, journey order from the flight tickets; decoys appear on the tickets. (3) H6 text and Fun Fact applied (PP-021). (4) Envelope 13: plane ticket Ottawa to Stockholm, summer 2027, and Liv's letter on white lined paper with the raven and Cryptic Bureau logo; the AUD puzzle is the unmarked decoy cards (only AD speaks of family); confirmed on the online page, not built (PP-043). (5) PZ-013 hints and solution rewritten (hint page rebuilt). **Still open:** online AUD confirmation page; paper tests (tickets, small raven at 10 mm, letter, wheel arm); two decoy envelopes' contents and rune labels (Q-050); digital game (Q-051).

**20 Oct 2026 (designer): the three itinerary receipts (flight bookings between journeys) are dropped.** Every hop ticket carries a date (19 Oct) and each journey's dates form their own block (Leif 8–17 Sep, Rollo 28 Sep – 16 Oct, Aud 24 Oct – 1 Nov, Harald 14 Nov – 12 Dec), so the hop tickets alone give both the stop order and the journey order (1-9-7-2). Fewer pieces and less reading in the finale. See PP-039.
