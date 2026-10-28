---
id: PP-039
title: Travel tickets (hops and flights)
type: prop
# idea | candidate | decided | built | parked
status: decided
# physical | printed | digital
form: printed
# make | buy | print | 3d-print
source: print
# The play-test page shows the body's "## Player sees" section, or this prop's image asset.
# Where the player gets it: start (in the backpack) or the puzzle whose lock releases it, e.g. PZ-004
found_in: PZ-012
envelope: PZ-012
# Physical pocket/container or location; availability remains in found_in above.
container: Envelope 12
after_game: return
reset_name: The travel tickets (18 hop tickets)
# Any related record IDs, e.g. [PZ-002, Q-004]
links: []
# Set to an ID when this record is replaced. It then moves to the Parked tab.
superseded_by:
tags: []
---

Three transition tickets in the final bundle; each documents the move from one trail's last stop to the next trail's first (see the archived Final riddle tab). Print file: `Transition_Tickets_Print.pdf`.

**12 Oct 2026 (designer, Q-055):** kept. Since Q-054 they no longer carry the solve: they show the journeys' order (Leif → Rollo → Aud → Harald), which is also the play order, as story.

**17 Oct 2026 (designer, Q-062): reworked.** The three itinerary receipts stay, with invented carriers (Nordic Air, Viking Rail, Longship Buses) and now carry the journey order (digits 1-9-7-2). New: one **hop ticket** per move between stops, decoys included, one printed page per journey (Leif's flights and ferry, Rollo's rail pass, Aud's Iceland buses, Harald's mixed), in scrambled order so players chain them. They give each journey's stop order; the raven mark on the cards tells real stops from decoys. Print file: `Hop_Tickets_Print.pdf`; builder `Props/Tickets/build_hop_tickets_pdf.py`. Stop order and decoy positions in Q-062.

## Starting state

### 19 October 2026 Viking Rail trains on coral paper

Designer requested trains next and selected **coral paper #E57E6B**. Created `Print/Print_VikingRail_Trains_Coral_Paper.docx`: six single-sided **3.5 × 1.75 inch** tickets on one Letter page, two columns by three rows, with a 1-inch calibration line. Same modern Source Sans family and information hierarchy as the flights; charcoal text, burgundy brand/rules and a separate train-cab/V-rail logo with small copper accents. No printed paper fill. Place names 14 pt, carrier 12 pt, labels/passenger 9 pt, service/date values 10 pt.

**Superseded 19 Oct 2026 (dates on every ticket, see below):** Exact routes and source scrambled order retained: Walcheren → Chalus (VR 6120), Battle → Roumare Forest (VR 5588), Rouen → Bayeux (VR 3412), Winchester → Battle (VR 5530), Chalus → Rouen (VR 3340), Staraya Ladoga → Kyiv (VR 9021). Every hop shows DATE OPEN; no invented calendar dates or decoy emphasis. Existing three connecting itinerary bookings, including their dated rail segments, remain unchanged.

Builder `Props/Tickets/build_viking_rail.py` reads existing hop literals. Exact-size source `Print/_pdf_source/Viking_Rail_Trains_Coral_Paper.pdf`; preview `Props/Tickets/Viking_Rail_Coral_Final_Preview.png` (coral substrate shown only in preview). Logo `Props/Tickets/Viking_Rail_Logo_v1.png`, raw built-in ImageGen output in `Sources/`, exact prompt `Viking_Rail_Logo_v1_prompt.txt`. Production typography is separate from the generated mark.

Checked all six PDF pages for route/service/date text, exact dimensions, no endpoint overflow and no full-page paper fill. One-page Word export visually reviewed. Canonical renderer absent (no LibreOffice); Word export succeeds. Actual contrast, small logo reproduction and print legibility remain physically untested. Print on coral Letter paper at 100%, single-sided; cut outer borders and leave the stub attached.

### 19 October 2026 flight services and existing date status confirmed

Designer supplied the authoritative 18-hop table plus all three connecting bookings. All route/service pairs match the current source data. Hop flights remain open-dated: NA 722 Battle Harbour → Brattahlid; NA 730 Brattahlid → Qikiqtarjuaq; NA 455 Constantinople → Hedeby; NA 463 Hedeby → Aci Castello. Connecting booking RX7T2Q remains 26–28 Sep 2024, M4KD8B 8–9 May 2025, QN2V6H 5–6 Jun 2025; the full multi-mode itineraries and individual segment dates are retained. Decoy names are not visually distinguished on player tickets.

**Superseded 19 Oct 2026 (dates on every ticket, see below):** New polished flight print master `Print/Print_NordicAir_Flights_Sage_Paper.docx` contains the four hop flights on one Letter page, **4 × 1.75 inches** each, with original service numbers and DATE OPEN in the attached right-hand stub. No invented calendar date. Actual Source Sans 3: 14 pt endpoints, 12 pt wordmark, 9 pt labels/passenger and 10 pt service/date values. Dark navy text, teal rules, copper-accent bird/aircraft logo, no printed paper background. Print on light sage cardstock at 100%, single-sided; keep the stub attached. Original monochrome sheet retained.

Builder `Props/Tickets/build_nordic_air_sage.py` reads existing source literals, verifies services and unchanged endpoints/order, and retains the three bookings without splitting them into hop tickets. Source PDF `Print/_pdf_source/Nordic_Air_Flights_Sage_Paper.pdf`; sage-colour preview `Props/Tickets/Nordic_Air_Sage_Final_Preview.png` (sage fill is preview-only). Transparent logo `Props/Tickets/Nordic_Air_Logo_Transparent_v1.png`; raw built-in ImageGen extraction retained in `Sources/`; exact extraction prompt in `Nordic_Air_Logo_Transparent_v1_prompt.txt`. Exact typesetting is separate from the generated logo; the original mark is placed using a PDF viewport without changing its pixels.

Checked all four PDF pages for exact size, route/service/date text and absence of a page background rectangle. One Letter Word page exported and visually checked. Canonical renderer unavailable (LibreOffice absent); Microsoft Word export succeeded. Physical paper colour/contrast and print readability untested. Connecting receipts, other carriers and the final boarding pass remain unchanged.

### Flight paper colour selected 19 October 2026

Designer chose **light sage green paper, image-sampled HEX #ADBD98**, for the Nordic Air flights. The HEX represents the supplied paper photograph, not a guaranteed physical colour match. The intended polished flight direction uses the new bird/aircraft logo concept, dark navy text, restrained teal/copper accents and no printed background; sage is the paper substrate. The latest colour comparison remains a proposal and the polished coloured-logo print master is not yet typeset. The earlier `Print_NordicAir_Flights.docx` is background-free but retains its initial black/grey identity. Future flight print instructions should specify sage paper rather than white; route names must remain legible at the actual 4 × 1.75 inch size.

### 19 October 2026 modern Nordic Air tickets

Designer selected simple modern elegant travel tickets, one carrier per transport type, and requested flight design first followed by its final version. New `Print/Print_NordicAir_Flights.docx` contains four existing air hops on one Letter page, at 4 × 1.75 inches each. Typeset in actual Source Sans 3: 12 pt carrier, 14 pt place names, 9 pt labels/passenger. Black on white, fine grey rules, native geometric aircraft, decorative stub divider; no date, barcode or arbitrary reference number. Passenger LIV ERICSON retains the current identity.

Routes, filtered directly from the existing scrambled hop print order: Brattahlid → Qikiqtarjuaq; Battle Harbour → Brattahlid; Constantinople → Hedeby; Hedeby → Aci Castello. Builder `Props/Tickets/build_nordic_air_flights.py` reads the original data with AST; it does not run the old builder. Exact-size source `Print/_pdf_source/Nordic_Air_Flights_Redesign.pdf`; production preview `Props/Tickets/Nordic_Air_Final_Preview.png`. Existing mixed hop master, connecting itinerary receipts and final boarding pass retained while other modes are designed.

All four endpoints and exact page dimensions checked; final Word sheet exported to one Letter page and visually reviewed. Canonical renderer absent (no LibreOffice); Microsoft Word export succeeded. Physical print readability remains untested. Print white Letter paper, 100%, single-sided. A 1-inch calibration line is included; cut ticket outer borders only.

Not recorded yet.

### 19 October 2026 dates on every ticket (designer)

**Supersedes the "DATE OPEN" and "no invented calendar dates" notes above.** Designer asked for a date on every ticket, with each stop 1 day to 1 week long, and dropped the old "over a couple of years" travel year. One calendar, **8 Sep to 12 Dec 2025**, kept in `Props/Tickets/ticket_dates.py`. Every date is a departure date. Claude's choice, to flag: the first draft ran June to September; it was shifted 92 days into autumn because card L3 has Leif watching the northern lights in Qikiqtarjuaq (no darkness in June) and card R4 says Winchester is "freezing". Oslo gets the full 7 days because card H1 says "a whole week in Oslo", so Harald's tickets sit 3 days later than first drafted.

| # | Ticket | Hop | Date |
|---|---|---|---|
| 1 | LF 11 | L'Anse aux Meadows → Battle Harbour | 08 Sep 2025 |
| 2 | NA 722 | Battle Harbour → Brattahlid (decoy) | 11 Sep |
| 3 | NA 730 | Brattahlid (decoy) → Qikiqtarjuaq | 17 Sep |
| – | RX7T2Q | Qikiqtarjuaq → Iqaluit → Ottawa → Amsterdam → Walcheren | 21–23 Sep |
| 4 | VR 6120 | Walcheren (decoy) → Chalus | 28 Sep |
| 5 | VR 3340 | Chalus → Rouen | 30 Sep |
| 6 | VR 3412 | Rouen → Bayeux | 07 Oct |
| 7 | LF 204 | Bayeux → Winchester | 10 Oct |
| 8 | VR 5530 | Winchester → Battle | 15 Oct |
| 9 | VR 5588 | Battle → Roumare Forest | 16 Oct |
| – | M4KD8B | Roumare Forest → Rouen → Paris CDG → Reykjavik → Dogurdarnes | 20–21 Oct |
| 10 | LB 31 | Dogurdarnes → Hvammur | 24 Oct |
| 11 | LB 47 | Hvammur → Bjarnarhofn (decoy) | 26 Oct |
| 12 | LB 52 | Bjarnarhofn (decoy) → Esjuberg | 01 Nov |
| – | QN2V6H | Esjuberg → Reykjavik → Oslo | 06–07 Nov |
| 13 | LF 810 | Oslo → Staraya Ladoga | 14 Nov |
| 14 | VR 9021 | Staraya Ladoga → Kyiv | 20 Nov |
| 15 | LF 377 | Kyiv → Constantinople (decoy) | 27 Nov |
| 16 | NA 455 | Constantinople (decoy) → Hedeby | 02 Dec |
| 17 | NA 463 | Hedeby → Aci Castello | 05 Dec |
| 18 | LB 90 | Aci Castello → Patara | 12 Dec |

Built: `build_hop_tickets_pdf.py` (mixed master, dates in the stub), `build_nordic_air_sage.py` and `build_viking_rail.py` (date split over two lines in the stub, "17 SEP" then "2025", because one line ran past the ticket edge), `build_transition_tickets_pdf.py` (the three bookings, with a check against `ticket_dates.py`). Word masters rebuilt. Previews checked. **Not updated:** the earlier black-and-grey `Print_NordicAir_Flights.docx` (no date, superseded by the sage version); ferry and bus tickets have no polished design yet. Not paper-tested.

**Resolved 19 Oct 2026 (designer):** card L1 now says “I spent months travelling”. The old museum-ticket dates (2 Feb, 17 Mar, 13 Apr, 28 Apr) were never printed on any ticket; they only appear in the retired design notes, so nothing needed changing. Still true: the dates give players a second way to order each journey, so the puzzle gets easier.

## Reset

Not recorded yet.

## Replacement

Not recorded yet.

### Longship Buses print design 19 October 2026
- User requested the bus tickets following flights and trains. Golden-yellow stock #F7B048 is the proposed bus colour for review, not a separately confirmed paper selection.
- Four existing bus hops, in existing scrambled print order: LB 47, LB 52, LB 31, LB 90. Dates read from ticket_dates.py. Connecting-booking bus segments stay in their existing multi-mode itineraries.
- Same modern ticket family: 3.5 by 1.75 inches, Source Sans route names 14 pt, wordmark 12 pt, labels 9 pt, service/date 10 pt. Simple vector bus with longship prow; charcoal and dark olive ink; production background unprinted.
- Word master: Print/Print_LongshipBuses_Yellow_Paper.docx, four tickets on one Letter page. Builder: Props/Tickets/build_longship_buses.py. Source PDF: Print/_pdf_source/Longship_Buses_Yellow_Paper.pdf. Colour proof: Props/Tickets/Longship_Buses_Yellow_Final_Preview.png.
- PDF route/service/date/dimensions and no-background assertions passed. Word exported and one-page layout visually inspected. Physical printing untested.

### Longship Ferries print design 19 October 2026
- User requested ferries next. Dark-green #678468 is the proposed remaining paper colour for review; no separately confirmed selection yet.
- Four existing ferry hops in their existing filtered print order: LF 11, LF 204, LF 810, LF 377. Routes and dates read from the existing hop source and ticket_dates.py; no new travel data.
- Same modern family: four 3.5 by 1.75 inch tickets on one Letter sheet. Source Sans route names 14 pt, carrier 12 pt, labels 9 pt, service/date 10 pt. Near-black #111914 lettering and rules, simple vector ferry/prow and waves logo, no printed background.
- Master: Print/Print_LongshipFerries_Green_Paper.docx. Builder: Props/Tickets/build_longship_ferries.py. Source PDF: Print/_pdf_source/Longship_Ferries_Green_Paper.pdf. Simulated paper preview: Props/Tickets/Longship_Ferries_Green_Final_Preview.png.
- Builder assertions passed for routes, services, dates, exact trim dimensions, text fit and absent background fill. One-page Word export visually inspected; physical contrast and printing untested.

### Carrier identity selections 19 October 2026
- Designer selected coloured ferry logo option A, the navy/copper dragon longship, from Sources/Longship_Ferries_Colour_Concepts_v1_ImageGen.png. Exact generation prompt is retained alongside the image. This supersedes the simple ferry icon; production application is pending.
- Designer selected Northway Buses as the bus carrier name, superseding Longship Buses. No service-code change was requested; existing LB services remain.
- Northway icon comparison produced with built-in ImageGen: A road/N/north arrow, B coach and north star, C compass and road. Navy with copper/forest accents on simulated golden-yellow paper. Concepts and exact prompt: Props/Tickets/Sources/Northway_Buses_Colour_Concepts_v1_ImageGen.png and Northway_Buses_Colour_Concepts_v1_prompt.txt. No icon selected yet; current bus print master still has the earlier identity pending the chosen replacement.

### Selected logos applied 19 October 2026
- Designer chose Northway Buses option B, the navy coach with forest-green north star. Applied to all four bus-hop tickets, with the Northway Buses name. Existing LB services and calendar dates unchanged.
- Also applied the previously selected Longship Ferries option A, navy dragon-prow longship and copper sail, to all four ferry-hop tickets. This completes the production application noted as pending above.
- Current bus master is Print/Print_NorthwayBuses_Yellow_Paper.docx; the earlier Print_LongshipBuses_Yellow_Paper.docx is obsolete for this redesigned set. Bus builder retains its existing filename build_longship_buses.py to preserve references. Current bus source PDF and preview use Northway_Buses_Yellow names. Ferry master retains Print_LongshipFerries_Green_Paper.docx.
- Transparent logo assets: Props/Tickets/Northway_Buses_Logo_B_v1.png and Longship_Ferries_Logo_A_v3.png. Built-in ImageGen raw outputs and exact extraction/refinement prompts retained alongside the concept boards in Props/Tickets/Sources. Old ferry preview moved to Norse_Archive with a log entry.
- Both Word sheets remain one Letter page with four 3.5 by 1.75 inch tickets. Production files print no paper background. Source PDF route/date/service/dimension assertions passed; both Word exports visually checked. Physical ink reproduction untested.
- This updates the redesigned hop-ticket sheets. Older generic mixed-hop and connecting-itinerary sheets have not been rebuilt with the new bus identity.

### Nordmark Rail identity options 19 October 2026
- Designer accepted Nordmark Rail as the replacement name for Viking Rail and requested icon options. Existing VR services and dates remain; no code changes requested.
- Built-in ImageGen comparison offers A N/track/north-arrow monogram, B modern train and mountain peaks, C north compass and tracks. Dark inks and restrained copper/burgundy/forest accents on simulated coral stock.
- Comparison and exact prompt retained in Props/Tickets/Sources/Nordmark_Rail_Colour_Concepts_v1_ImageGen.png and Nordmark_Rail_Colour_Concepts_v1_prompt.txt. Superseded selection status: designer chose B (train and mountain peaks) in the prior chat; applying the choice was interrupted by Bad Request. Current train builder still uses Viking Rail; name and logo application remain pending.
### Nordic Air logo exploration 19 October 2026
- Continued the failed chat's request for Nordic Air logo options using built-in ImageGen. Comparison on selected sage paper #ADBD98: A swept wing/N, B bird with copper accent, C north star and flight arc. Designer subsequently selected B, navy bird with copper accent. Selection recorded; current flight masters unchanged and logo application pending.
- Visually inspected the generated board. Concept C reads more as a compass and arrow than an aircraft. This is a concept preview; physical print contrast untested.
- Comparison: Props/Tickets/Sources/Nordic_Air_Colour_Concepts_v2_ImageGen.png. Exact prompt retained alongside in Nordic_Air_Colour_Concepts_v2_prompt.txt.
- Exact generation prompt: Create ONE professional logo concept comparison board for fictional Scandinavian airline NORDIC AIR, a refined contemporary airline identity for small printed travel tickets. Three spacious horizontal rows labelled A B C, each with a large standalone emblem at left and the same emblem smaller paired with exact uppercase wordmark NORDIC AIR at right. A: elegant swept aircraft wing forming a subtle N, strong sculptural navy shape with restrained teal accent; confident graceful aerodynamic silhouette. B: distinctive streamlined bird in flight whose silhouette also suggests an aircraft viewed from above, navy with a restrained burnt copper accent; elegant and recognisable, no detailed feathers. C: refined north-star and ascending aircraft emblem, four-point north star integrated with a sweeping flight arc, navy and deep teal, compact balanced geometry. Distinct thoughtfully designed premium airline logos, not generic clip art. Modern tasteful sans-serif lettering, NORDIC prominent AIR secondary. Every row panel uses uniform light sage paper simulation #ADBD98, warm off-white outer board and gutters. Inks deep navy #142B36, deep teal #245F60, copper #98452F. Flat solid fills with sharp vector-like edges, no gradients, shadows, metallic effects, photographs, texture, tiny detail, white or pale elements within marks. Negative space reveals sage paper. Good readability for an emblem approximately 0.4 inch high on a home printed ticket. Avoid ships, trains, buses, Viking helmets, ornate knotwork, circular text and slogans. Only text A B C and NORDIC AIR. Wide landscape composition. Preview concept board, not a print-ready ticket sheet.

### Nordic Air fancy ticket proposal 19 October 2026
- Designer requested a fancy air-ticket preview. Built-in ImageGen used selected logo B as reference: navy bird/copper wing, sage stock, fine double border with shaped corners, serif route typography, copper flight path and attached service/date stub. Existing sample data: Brattahlid to Qikiqtarjuaq, NA 730, 17 SEP 2025, Liv Ericson.
- Visually inspected the concept; image proportions are wider than the requested 4 by 1.75 inch production format. This is a proposal, not an adopted layout or print master. Exact-size typesetting and physical readability remain to be checked if adopted.
- Board and exact prompt: Props/Tickets/Sources/Nordic_Air_Fancy_Ticket_Concept_v1_ImageGen.png and Nordic_Air_Fancy_Ticket_Concept_v1_prompt.txt. Prompt file contains the full generation instructions; input reference was Nordic_Air_Colour_Concepts_v2_ImageGen.png, option B only.

### Approved fancy Nordic Air tickets applied 19 October 2026
- Designer approved the fancy ticket concept for the air tickets. Applied to all four existing air-hop tickets via build_nordic_air_sage.py, preserving routes, print order, flight numbers, dates and LIV ERICSON. Supersedes the earlier modern sage layout and pending air-logo application status.
- Final design: selected bird B in navy/copper, double inward-curved border, Cormorant Garamond 600 route names up to 18 pt, Source Sans labels, copper flight arc and attached flight/date stub. Exact size remains 4 by 1.75 inches. Sage #ADBD98 is the physical paper; production background is unprinted.
- Current Word master: Print/Print_NordicAir_Flights_Sage_Paper.docx, four tickets on one Letter page. Exact-size four-page PDF: Print/_pdf_source/Nordic_Air_Flights_Sage_Paper.pdf. Sage proof: Props/Tickets/Nordic_Air_Sage_Final_Preview.png. Reusable transparent logo: Props/Tickets/Nordic_Air_Logo_B_v2.png; raw extraction and exact prompt retained in Sources/Nordic_Air_Logo_B_v2_ImageGen.png and Nordic_Air_Logo_B_v2_prompt.txt. Built-in ImageGen isolated the approved logo; ticket text and ornament are typeset programmatically.
- Previous sage proof moved to Norse_Archive/NorseBackpack/Props/Tickets/Nordic_Air_Sage_Before_Fancy_20261019.png and logged. Former initial logo retained because older print sources reference it.
- Checks: all four source-PDF routes/services/dates/dimensions/no-background assertions pass; logo RGBA and transparent corners checked. Inspected sage proof and every ticket on the Letter sheet. Packaged render_docx.py failed because LibreOffice is absent; Microsoft Word export succeeded, verified one page and visually inspected its rendered PNG. Physical printing untested.
- Ran build_web_assets.py to refresh local web copies and generated ignore rules. This applies to the four hop tickets; connecting itineraries and final boarding pass remain separate designs.

### Fancy Nordmark Rail ticket proposal 19 October 2026
- Designer requested a fancy rail-ticket preview. Built-in ImageGen used selected Nordmark B train/mountains logo and approved fancy air-ticket concept as references. Coral paper, navy/burgundy ink, serif route names, fine double shaped-corner border, attached train/date stub and railway-track flourish.
- Existing sample: Walcheren to Chalus, VR 6120, 28 SEP 2025, Liv Ericson. Board visually inspected; text and reference logo are recognisable. Generated ticket is wider than the requested 3.5 by 1.75 inch production proportions; exact-size typesetting/readability must be checked if adopted. Physical printing untested.
- Saved preview and full exact prompt to Props/Tickets/Sources/Nordmark_Rail_Fancy_Ticket_Concept_v1_ImageGen.png and Nordmark_Rail_Fancy_Ticket_Concept_v1_prompt.txt. Proposal only; rail print masters unchanged.

### Fancy Northway Buses ticket proposal 19 October 2026
- Designer requested fancy bus-ticket preview. Built-in ImageGen used selected B coach/north-star logo and approved fancy air-ticket style reference. Golden-yellow paper, navy/forest-green accents, serif place names, fine double border, winding-road ornament and attached bus/date stub.
- Existing sample: Hvammur to Bjarnarhofn, LB 47, 26 OCT 2025, Liv Ericson. Visually inspected the board; text and chosen logo are recognisable. Generated proportions are wider than requested 3.5 by 1.75 inches; exact-size typesetting and physical readability require checking if adopted.
- Board/full exact prompt: Props/Tickets/Sources/Northway_Buses_Fancy_Ticket_Concept_v1_ImageGen.png and Northway_Buses_Fancy_Ticket_Concept_v1_prompt.txt. Proposal only, existing bus print masters unchanged. Physical printing untested.

### Fancy Longship Ferries ticket proposal 19 October 2026
- Designer requested fancy ferry preview. Built-in ImageGen used adopted dragon-longship A v3 logo and approved fancy air-ticket style as references. Dark-green paper #678468, navy/copper, serif place names, fine double cornered border, wave ornament and attached ferry/date stub.
- Existing example: Bayeux to Winchester, LF 204, 10 OCT 2025, Liv Ericson. Visually inspected: text and chosen logo recognisable, matching family appearance. Generated proportions wider than requested 3.5 by 1.75 inches; exact-size typesetting and physical contrast/readability require checking if adopted.
- Saved board/full exact prompt: Props/Tickets/Sources/Longship_Ferries_Fancy_Ticket_Concept_v1_ImageGen.png and Longship_Ferries_Fancy_Ticket_Concept_v1_prompt.txt. Proposal only; ferry production masters unchanged. Physical printing untested.

### All fancy travel hop tickets adopted and built 19 October 2026
- Designer authorised all tickets with the approved fancy designs. The production set is 18 existing hops: 4 Nordic Air, 6 Nordmark Rail, 4 Northway Buses and 4 Longship Ferries. This adopts the preceding rail/bus/ferry proposals and supersedes their pending production status. Existing routes, passenger, scrambled sheet order, dates and NA/VR/LB/LF service codes retained. Connecting itinerary receipts and the final boarding pass are separate props, outside these four carrier sheets.
- Shared fancy_travel_ticket.py typesets the rail/bus/ferry family: Cormorant Garamond 600 route names at 14–18 pt, double shaped-corner borders, Source Sans labels at 8 pt, dates at 11.5 pt, compact original mode-specific ornaments and attached service/date stubs. Small ornaments preserve long place-name readability at 3.5 by 1.75 inches. Air remains the approved 4 by 1.75 inch fancy layout.
- Current one-page Letter Word masters: Print/Print_NordicAir_Flights_Sage_Paper.docx; Print/Print_NordmarkRail_Trains_Coral_Paper.docx; Print/Print_NorthwayBuses_Yellow_Paper.docx; Print/Print_LongshipFerries_Green_Paper.docx. Former Print_VikingRail_Trains_Coral_Paper.docx is a refreshed compatibility copy with Nordmark branding. Existing Viking_Rail source-PDF/preview filenames remain stable for old links; their content now reads Nordmark Rail.
- Reused selected Northway B and Longship A v3 transparent logos. New transparent Nordmark B master: Props/Tickets/Nordmark_Rail_Logo_B_v1.png; raw built-in ImageGen extraction and full exact prompt in Sources/Nordmark_Rail_Logo_B_v1_ImageGen.png and Nordmark_Rail_Logo_B_v1_prompt.txt. Pre-fancy previews and three builders archived at Norse_Archive/NorseBackpack/Props/Tickets/Before_Fancy_20261019/ and logged.
- Checks: all 18 distinct service codes exactly match ticket_dates.py; every PDF page checked for existing route/passenger/service/date text, exact dimensions and no printed full-page background. All four Letter Word sheets exported through Microsoft Word, confirmed one page each, rendered and visually inspected. Reviewed all three new coloured proofs. Packaged render_docx.py cannot run without LibreOffice; Microsoft Word export provided successful independent layout verification. Local web assets regenerated. Physical ink contrast/printing untested.
- Printing: one Letter sheet per carrier, single-sided, actual size/100%, sage/coral/golden-yellow/dark-green respectively. Verify each one-inch calibration line before cutting. Background is supplied by the paper.

### Full adventure page refreshed 19 October 2026
- Designer requested Full_Adventure.html updated with the new ticket designs. Updated build_full_adventure.py so the PP-039 card in envelope 12 shows the four current fancy carrier Letter sheets first, followed by the three existing itinerary receipts. Removed the former mixed-hop sheet previews from this card.
- Added current Word and PDF print-sheet links, paper colours and actual-size instructions. The travel card spans the content width with larger preview columns. No prop moved between envelopes.
- Four carrier builders now save their Letter PDF sheets under Print/_pdf_source using Nordic_Air_Letter_Print, Nordmark_Rail_Letter_Print, Northway_Buses_Letter_Print and Longship_Ferries_Letter_Print names. Copied the verified current sheets to those persistent paths and to Web/pdf. Full adventure builder now uses available pypdfium2 for rendering; PyMuPDF is absent from the bundled runtime. Web PDFs retain full print-quality bytes; regular web asset/link update completed after those copies were supplied.
- Rebuilt page and preview PNGs. Verified four Word and four PDF links plus seven preview targets exist, and the old mixed-hop previews are absent from PP-039. Visually checked the page over localhost in the in-app browser; screenshot in C:/EscapeBackpack/output/fancy-travel/adventure-ticket-update.png.


**20 Oct 2026 (designer): production print size** — hop tickets → business card 3.5 × 2 in; transition receipts → bookmark 2 × 6 in. Decided in Q-052 (standard print sizes); not rebuilt yet. **Reopened later on 20 Oct** (designer: museum tickets smaller and all one size; travel tickets smaller, cheap and all one size); see Q-052.
### Business-card prototype Word sheets approved 20 October 2026
- Designer requested home-print DOCX versions at the discussed standard business-card size. All 18 hop tickets are now exactly 3.5 by 2 inches (252 by 144 PDF points), including the attached service/date area. This supersedes earlier 4 by 1.75 inch air and 3.5 by 1.75 inch rail/bus/ferry dimensions for the current prototype masters.
- Preserved the adopted fancy designs, all route names, calendar dates, passenger, service codes and scrambled print order. Air now uses the same shared layout as other carriers with its bird/flight-arc identity; all cards have pale exact-size cutting rectangles outside the decorative border.
- Four existing current DOCX paths retained: Print_NordicAir_Flights_Sage_Paper.docx, Print_NordmarkRail_Trains_Coral_Paper.docx, Print_NorthwayBuses_Yellow_Paper.docx and Print_LongshipFerries_Green_Paper.docx in Print/. One Letter page per carrier, two columns: 4 air, 6 rail, 4 bus and 4 ferry cards. Existing source PDFs and Word compatibility rail copy updated. These are for plain coloured Letter paper, not aligned to any pre-perforated business-card stock template.
- Printed instructions specify actual size/100%, single-sided; cut pale outer rectangles, leaving service/date stubs attached. Each sheet has a one-inch calibration rule. Sage/coral/golden-yellow/dark-green paper supplies the background; no printed background fill.
- Archived four preceding previews/builders in Norse_Archive/NorseBackpack/Props/Tickets/Before_Business_Cards_20261020, logged in archive README. Updated fancy_travel_ticket.py and four builders.
- Verified all 18 unique hops, existing text and exact 252 by 144 dimensions. Exported all four DOCX files via Microsoft Word; each is one Letter page and every rendered sheet visually inspected without clipping. Physical printing untested. Existing standard renderer limitation (LibreOffice absent) remains; Word supplied layout verification.


**20 Oct 2026 (designer): production size decided** — all travel tickets → business card 3.5 × 2 in: hops (built 20 Oct), itinerary receipts (not rebuilt; double-sided proposed). See Q-052.

**20 Oct 2026 (designer): the three itinerary receipts (flight bookings between journeys) are dropped.** Every hop ticket carries a date (19 Oct) and each journey's dates form their own block (Leif 8–17 Sep, Rollo 28 Sep – 16 Oct, Aud 24 Oct – 1 Nov, Harald 14 Nov – 12 Dec), so the hop tickets alone give both the stop order and the journey order (1-9-7-2). Fewer pieces and less reading in the finale. Print master `Print/Print_TransitionTickets.docx` moved to `Norse_Archive/NorseBackpack/Print/Itinerary_Receipts_Dropped_20261020/` and removed from `Props/build_printables_docx.py`; the receipts no longer show in `Full_Adventure.html` or on the repacking letter (rebuilt). `build_transition_tickets_pdf.py` and its `_pdf_source` PDFs stay, because `build_nordic_air_sage.py` reads the booking data from that builder. Superseded: the 20 Oct size decision for the receipts (business card, double-sided).
