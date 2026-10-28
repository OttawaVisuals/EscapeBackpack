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
# The play-test page shows the body's "**14 Oct 2026 (designer, box + envelopes, PR-007):** the arm now prints the three steps beside the windows they refer to: “1 SET THE CODE” above the code windows, “2 READ THE RUNES” above the rune windows, “3 OPEN THE ENVELOPE WITH THESE RUNES” below them (was just CODE and RUNES). L1 gives the first code as a worked example (PZ-001). Starts loose in the box, on top, with L1.

## Player sees" section, or this prop's image asset.
# Where the player gets it: start (in the backpack) or the puzzle whose lock releases it, e.g. PZ-004
found_in: start
envelope: start
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
- **3-digit codes start with the blank:** 532 is set as `_532`. (A leading 0 does **not** work: `0532` shows different runes from `_532` and opens nothing; corrected 17 Oct 2026 after Codex's review, Q-063.)
- **Runes:** each wheel gives every symbol its own Elder Futhark rune (20 of 24; ansuz, mannaz, jera and ingwaz left out as look-alikes). Each code therefore reads as its own rune string, and a wrong code never shows an envelope's runes. Rune maps are fixed by a seed in the builder.
- **How it's built:** stacked disks (I at the bottom, 196 mm; IV on top, 76 mm) and a top arm with 8 windows: the left four show the code, the right four the runes. A brass fastener through the centres.
- **Known weakness:** players can work backwards from an envelope's runes to its code. That is no bigger a shortcut than tearing an envelope open; envelopes rely on players playing fair anyway.
- **Not flat:** coins, comb, board pieces and other non-flat contents won't fit an envelope; those would need marked pouches. Not worked out.
- **Lock stickers (PP-046)** would no longer be needed if this replaces the locks.
- Codes and lock numbers come from the puzzle records (`answer`, `hint_title`), so the labels follow any code change after a rebuild.
- Builder: `Props/CypherWheel/build_cypher_wheel_pdf.py` → `NorseBackpack/Print/_pdf_source/Cypher_Wheel_Print.pdf` (wheels, arm, envelope labels, designer key) and `NorseBackpack/Print/_pdf_source/Cypher_Wheel_Assembled_Preview.pdf` (the assembled wheel set to each of the 13 codes, as a check).
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

**17 Oct 2026 (Q-063):** the blank-first rule is now on the player arm, under the code windows: “THREE DIGITS? LEAVE THE FIRST WINDOW BLANK” (wording from Codex's review, not typed by the designer). `Cypher_Wheel_Print.pdf` rebuilt.


## 17 Oct 2026: Wider instruction-arm readability draft (Codex)

Designer requested larger wheel steps. Proposed replacement arm increases height from **18 to 34 mm**; its length, centre fastener and all eight cut-window positions/dimensions remain identical. Existing wheels I-IV can be reused. Steps 1-2 are **12 pt bold**; step 3 and the blank-first reminder are **10.5 pt**. Copy: "1 SET THE CODE" / "2 READ THE RUNES" / "3 Open the envelope with these runes." Beneath the code windows: "Three digits? First window: leave it blank, not zero." Same hub colour and dark ink; no rune mappings, codes, labels or designer packing key changed.

Review pages **9-10** show the assembly at 1021 and blank-532. Letter pack page **9** is the actual replacement-arm cut sheet with 50 mm scale check and assembly instructions; page **10** is its blank reverse (the explanatory text sits outside the arm). **Do not print/cut the assembled review pages as components.**

Verified identical eight-window geometry and pixel-identical contents in all **104 apertures across the 13 current codes** against the live arm. Blank-532 still maps to ᛈᚹᛟᛇ and differs from zero-532. The wider arm's physical turning clearance, stiffness and fastener fit remain untested. Proposed replacement only.


Shared source: `Props/ReadabilityDrafts/build_readability_drafts.py`. Outputs at repository root: `NorseBackpack/Print/_pdf_source/Readability_Redesign_Drafts/Readability_Drafts_Review.pdf` and `NorseBackpack/Print/_pdf_source/Readability_Redesign_Drafts/Readability_Drafts_Letter_Print.pdf`. These are separate review/print drafts; live sources, print masters, website copies and print-test DOCX files are unchanged. No new AI artwork was generated. Print the Letter pack at 100%, long-edge duplex. Paper readability, envelope fit and printer registration have not been tested.


**17 Oct 2026, designer feedback:** the revised wheel is accepted as a design. The arm is unchanged in the corrected draft pack; assembled review pages are now 8-9 (glossary uses one page). Letter arm remains page 9/blank page 10. Adoption into the live wheel PDF and a physical turn test remain separate steps.

**17 Oct 2026 (designer): wide arm adopted.** `build_cypher_wheel_pdf.py` now draws the 34 mm arm (was 18 mm) with the steps at 12 / 10.5 pt and “Three digits? First window: leave it blank, not zero.” (Codex's readability draft); windows, centre and pin unchanged. This replaces my 5.4 pt blank-first line. Old builder kept as `build_cypher_wheel_pdf.2026-10-17_before_wide_arm.py`. Arm caption moved to 14 mm. Needs a paper check: cut, fit and wheels turning freely.
