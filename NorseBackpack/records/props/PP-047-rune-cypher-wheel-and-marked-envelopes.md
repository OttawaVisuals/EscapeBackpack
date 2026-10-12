---
id: PP-047
title: Rune cypher wheel and marked envelopes
type: prop
# idea | candidate | decided | built | parked
status: decided
# physical | printed | digital
form: printed
# make | buy | print | 3d-print
source: print
# The play-test page shows the body's "## Player sees" section, or this prop's image asset.
# Where the player gets it: start (in the backpack) or the puzzle whose lock releases it, e.g. PZ-004
found_in: start
# Physical pocket/container or location; availability remains in found_in above.
container: In the box
# On the public reset page: return (put back in its container) | keep (the team takes it home) |
# stays (never moves; listed as a final check) | none (not mentioned). Blank = return.
after_game:
# Name on the public reset page, if the title isn't what players call it (optional)
reset_name:
# Any related record IDs, e.g. [PZ-002, Q-004]
links: [PP-046]
# Set to an ID when this record is replaced. It then moves to the Parked tab.
superseded_by:
tags: []
---

**Decided 11 Oct 2026 (designer, PR-007):** the envelopes and cypher wheel replace the locks. The envelope table is in PR-007.

**Proposed 11 Oct 2026 (friends' feedback, designer chose runes in chat):** replace the 13 padlocks, which are heavy and expensive, with marked envelopes plus one cardstock cypher wheel. Players set a code on the wheel and read four runes in a window; the envelope with those runes is the one the code opens. Not yet decided as a replacement for the locks: this is a prototype to build and try.

- **Four wheels, same 20 symbols on each:** 0–9, a blank, and A B D E K L M O S (the letters BOOK, MEAD and SOLE need). Same set on every wheel so the wheel doesn't hint which letters a word starts with. Letters print in red so O and 0 can't be confused.
- **3-digit codes start with the blank:** 521 is set as `_521`. (A leading 0 would also work, since no 4-digit code starts with 0.)
- **Runes:** each wheel gives every symbol its own Elder Futhark rune (20 of 24; ansuz, mannaz, jera and ingwaz left out as look-alikes). Each code therefore reads as its own rune string, and a wrong code never shows an envelope's runes. Rune maps are fixed by a seed in the builder.
- **How it's built:** stacked disks (I at the bottom, 196 mm; IV on top, 76 mm) and a top arm with 8 windows: the left four show the code, the right four the runes. A brass fastener through the centres.
- **Known weakness:** players can work backwards from an envelope's runes to its code. That is no bigger a shortcut than tearing an envelope open; envelopes rely on players playing fair anyway.
- **Not flat:** coins, comb, board pieces and other non-flat contents won't fit an envelope; those would need marked pouches. Not worked out.
- **Lock stickers (PP-046)** would no longer be needed if this replaces the locks.
- Codes and lock numbers come from the puzzle records (`answer`, `hint_title`), so the labels follow any code change after a rebuild.
- Builder: `Props/CypherWheel/build_cypher_wheel_pdf.py` → `output/pdf/Cypher_Wheel_Print.pdf` (wheels, arm, envelope labels, designer key) and `output/pdf/Cypher_Wheel_Assembled_Preview.pdf` (the assembled wheel set to each of the 13 codes, as a check).
- Needs Segoe UI Historic (`C:\Windows\Fonts\seguihis.ttf`) for the runes.
- Not yet printed or assembled.

## Player sees

A round wheel of four rings of numbers and letters, with an arm across it. Turning the rings to a code shows four runes; one envelope carries the same runes.

## Starting state

All four wheels set so the code windows are blank or show 0000.

## Reset

Put each envelope's contents back and re-seal it (unknown: how envelopes are sealed and re-sealed).

## Replacement

Envelopes are likely consumable if they are torn open; spare labels can be reprinted from the builder.
