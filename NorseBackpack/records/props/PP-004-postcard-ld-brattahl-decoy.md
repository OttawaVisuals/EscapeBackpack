---
id: PP-004
title: Postcard LD · Brattahlíð (decoy)
type: prop
# idea | candidate | decided | built | parked
status: built
# physical | printed | digital
form: printed
# make | buy | print | 3d-print
source: print
# The play-test page shows the body's "## Player sees" section, or this prop's image asset.
# Where the player gets it: start (in the backpack) or the puzzle whose lock releases it, e.g. PZ-004
found_in: PZ-009
envelope: PZ-009
# Physical pocket/container or location; availability remains in found_in above.
container: Envelope 6
after_game: return
reset_name: Postcard: Brattahlíð
# Any related record IDs, e.g. [PZ-002, Q-004]
links: []
# Set to an ID when this record is replaced. It then moves to the Parked tab.
superseded_by:
tags: []
---

**11 Oct 2026 (PR-007):** the backpack is now a box, and pockets and pouches are envelopes. Where this record mentions the bag, a pocket, a pouch or a lock, that is the earlier format; the `container` field gives the envelope.

Postcard LD, Brattahlíð (decoy). 5 × 3.5 in, printed front and back. Message and Fun Fact are built by `Postcards/build_postcard_LD_pdf.py`. Print file: [Postcard_LD_Brattahlid_Print.pdf](../Web/pdf/Postcard_LD_Brattahlid_Print.pdf).

## From the old Postcards tab

#### LD · Brattahlíð (decoy)

Greenland · Leif's decoy card, not one of his three real trail stops · message, Fun Fact and the real beasts-chain imprint built

[View PDF](../Web/pdf/Postcard_LD_Brattahlid_Print.pdf)

![Front of the Brattahlíð decoy postcard](Web/Postcards/Postcard_LD_Brattahlid_Front.webp)Front

![Back of the Brattahlíð postcard with Aunt Liv's message, the Fun Fact box and the real Vinland Editions Series F No. 1 imprint](Web/Postcards/Postcard_LD_Brattahlid_Back.webp)Back · real message and Fun Fact (Q-019), the real `Vinland Editions · Series F, No. 1` beasts-chain imprint (old page PZ-10/PZ-013); postmark carries place only, no date (Q-006/old page PC-03/old page PC-04)

## Starting state

In its release pouch (see found_in).

## Reset

There are 22 postcards: each goes back with the lock it came from, as listed below.

## Replacement

Reprint from the print file if damaged.

**16 Oct 2026 (designer):** LD's line "I hope you enjoy this puzzle, there might be a few steps to get the final code." is the existing Liv-about-the-puzzles line (Q-061). Spelling "Brattahlid" in the message differs from Brattahlíð elsewhere; to look at in the envelope 6 text pass. Nothing changed.

**16 Oct 2026 (designer, envelope 6 text pass):** message first line now has a comma (“Brattahlid, Greenland, where Leif actually grew up.”). Tried “Brattahlíð” in the handwriting font: the ð renders badly, so the plain “Brattahlid” stays (the typed parts of the card use Brattahlíð). Fun Fact shortened to “Leif's mother built Greenland's first church here, a tiny turf one.” Imprint changed to `Vinland Editions · Series A, No. 6` (points to the wolf at A6, PZ-005 answer 4865). Rebuilt.


## 17 Oct 2026: LD imprint readability draft (Codex)

**Superseded in part by the designer feedback below.**

Designer requested a more legible imprint. Draft keeps the **6 x 4 in postcard**, artwork, message, underlined "spell", Fun Fact, stamp and absence of raven. The footer receives 30 pt more depth: the vertical divider and Fun Fact box end higher, leaving a separate publisher line at **10 pt** and the existing illustration credit at **8 pt**. Imprint remains exactly **Vinland Editions · Series A, No. 6** (A6, WOLF, 4865). It stays regular-weight dark ink, without a clue badge or highlighted A/6. The source footer is suppressed at draw time so no duplicate tiny/hidden text remains.

Review and print pack pages **7-8**. Text-token comparison confirms all existing text retained; front rendering is pixel-identical to the current live PDF. The larger imprint is more noticeable and should be checked in the next playtest for appropriate discovery difficulty. Proposed replacement only.


Shared source: `Props/ReadabilityDrafts/build_readability_drafts.py`. Outputs at repository root: `NorseBackpack/Print/_pdf_source/Readability_Redesign_Drafts/Readability_Drafts_Review.pdf` and `NorseBackpack/Print/_pdf_source/Readability_Redesign_Drafts/Readability_Drafts_Letter_Print.pdf`. These are separate review/print drafts; live sources, print masters, website copies and print-test DOCX files are unchanged. No new AI artwork was generated. Print the Letter pack at 100%, long-edge duplex. Paper readability, envelope fit and printer registration have not been tested.


## 17 Oct 2026: Designer correction - restore the hidden corner imprint

**The enlarged 10 pt imprint and deeper footer are rejected.** This is a deliberately small mark to discover in a postcard corner, not ordinary instructional text. The designer explicitly allows the magnifier to be needed. Making this card's footer larger than the others undermines that discovery.

The draft now calls the live LD front/back drawing functions unchanged: **original 6 pt Series A, No. 6 imprint, original credit, divider and Fun Fact box positions, original shallow footer**. Both faces compare pixel-identically to the current production PDF. No live file needed reverting because only the draft had been changed. Review pages **6-7**; Letter pages **7-8**.
