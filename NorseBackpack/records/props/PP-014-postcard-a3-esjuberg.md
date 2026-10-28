---
id: PP-014
title: Postcard A3 · Esjuberg
type: prop
# idea | candidate | decided | built | parked
status: built
# physical | printed | digital
form: printed
# make | buy | print | 3d-print
source: print
# The play-test page shows the body's "## Player sees" section, or this prop's image asset.
# Where the player gets it: start (in the backpack) or the puzzle whose lock releases it, e.g. PZ-004
found_in: PZ-005
envelope: PZ-005
# Physical pocket/container or location; availability remains in found_in above.
container: Envelope 7
after_game: return
reset_name: Postcard: Esjuberg
# Any related record IDs, e.g. [PZ-002, Q-004]
links: []
# Set to an ID when this record is replaced. It then moves to the Parked tab.
superseded_by:
tags: []
---

**11 Oct 2026 (PR-007):** the backpack is now a box, and pockets and pouches are envelopes. Where this record mentions the bag, a pocket, a pouch or a lock, that is the earlier format; the `container` field gives the envelope.

Postcard A3, Esjuberg. 5 × 3.5 in, printed front and back. Message and Fun Fact are built by `Postcards/build_postcard_A3_pdf.py`. Print file: [Postcard_A3_Esjuberg_Print.pdf](../Web/pdf/Postcard_A3_Esjuberg_Print.pdf).

## From the old Postcards tab

#### A3 · Esjuberg

Iceland · message and Fun Fact built, 18 Sept 2026 — closes Aud’s trail; **message rewritten by the user, 25 Sept 2026** — “my head is spinning” nudges players to turn the tally upside down (PZ-010); **art prints upside down relative to the back, 28 Sept 2026** (user request; `ART_EXTRA_ROTATE` in `build_print_test_docx.py`, print file `PrintTest_A2_A3.docx` only — the PDFs are unchanged); **29 Sept 2026:** the single and Letter PDFs now print it upside down too (rotated in `build_postcard_A3_pdf.py`)

[View PDF](../Web/pdf/Postcard_A3_Esjuberg_Print.pdf)

![Esjuberg postcard front with Akrafjall rising across a blue bay](Web/Postcards/Postcard_A3_Esjuberg_Front.webp)Front · 1500 × 1050 px

![Back of the Esjuberg postcard with Aunt Liv's message closing Aud's trail and the upside-down reading instruction](Web/Postcards/Postcard_A3_Esjuberg_Back.webp)Back · real message and Fun Fact; message rewritten 25 Sept 2026: “Esjuberg today. Another beautiful place that Aud the Deep-Minded visited, my head is spinning with all the amazing landscapes! Still amazed by the treasures I found!” The Helgi story now lives only in the Fun Fact; postmark carries place only, no date (Q-006/old page PC-03/old page PC-04)

**Source:** photograph by Diego Delso, [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Monta%C3%B1a_volc%C3%A1nica_Akrafjall,_Akranes,_Vesturland,_Islandia,_2014-08-14,_DD_003.JPG), [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).

## Starting state

In its release pouch (see found_in).

## Reset

There are 22 postcards: each goes back with the lock it came from, as listed below.

## Replacement

Reprint from the print file if damaged.

**16 Oct 2026 (designer, Q-057):** Fun Fact shortened to “Esjuberg is where Laxdæla saga has Aud meet her brother Helgi, and turn down his offer to settle.” Message last paragraph now: “Still amazed by the treasures I found! I added it all up on my trusty old counter, and my head is still spinning.” (the designer's wording; tells players the four-wheel treasure tally, PP-026, is for entering the total; “my head is spinning” in the paragraph above is kept as the turn-it-upside-down clue). A3 is in envelope 7. Rebuilt.
