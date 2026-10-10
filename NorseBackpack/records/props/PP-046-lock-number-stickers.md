---
id: PP-046
title: Lock number stickers
type: prop
# idea | candidate | decided | built | parked
status: built
# physical | printed | digital
form: printed
# make | buy | print | 3d-print
source: print
# The play-test page shows the body's "## Player sees" section, or this prop's image asset.
# Where the player gets it: start (in the backpack) or the puzzle whose lock releases it, e.g. PZ-004
found_in: start
# Physical pocket/container or location; availability remains in found_in above.
container: Stuck on each lock body
# Any related record IDs, e.g. [PZ-002, Q-004]
links: []
# Set to an ID when this record is replaced. It then moves to the Parked tab.
superseded_by:
tags: []
---

Longship stickers numbered 1–13, one per lock in solve order (PZ-001 to PZ-013), so the lock numbers match the hint page. Locks were already to be labelled 1–13 directly on the body (Q-001).

**Selected 8 Oct 2026 (designer):** longship concept C from AS-062. The number sits on the cream sail. AS-063 is the blank-sail master, with numbers typeset consistently by the PDF builder. Both the print PDF and existing Word sticker file now contain the longship.

**Superseded earlier direction:** a Norse icon rather than Hiking's backpack silhouette (Hiking: `Hiking_Trip/Stickers_Locks_Numbers.docx`). Claude initially used the round shield from `Icons/round_shield.svg`, with the number in an enlarged cream boss. The designer subsequently selected the longship instead.

- Each longship 1.3 cm wide; two full sets on one US Letter sheet (26 stickers including spares).
- Numbers in Helvetica Bold: Cinzel's "11" read as "ll" at this size.
- Builder: `Props/LockStickers/build_lock_stickers_pdf.py` → `output/pdf/Lock_Stickers_Print.pdf`; Word copy `output/docx/Print_LockStickers.docx` (from `Props/build_printables_docx.py`).
- Not yet printed on sticker paper.
- Both sequences 1–13 checked in the PDF; sheet and embedded Word artwork visually inspected, including two-digit numbers. Native DOCX rendering is unavailable here: LibreOffice and Microsoft Word are absent. The existing one-page image anchor and Letter page layout were preserved exactly.

Lock types by number: 4-digit 1, 2, 5, 7, 12, 13; 3-digit 6, 8, 9, 11; 4-letter 3, 4, 10.

## Player sees

A small longship with the lock number on its sail on each lock.

## Starting state

Stuck on the lock bodies before packing.

## Reset

None needed.

## Replacement

Spare set on the same sheet.
