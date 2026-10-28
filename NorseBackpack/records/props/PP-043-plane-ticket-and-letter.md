---
id: PP-043
title: Plane ticket and letter
type: prop
# idea | candidate | decided | built | parked
status: decided
# physical | printed | digital
form: printed
# make | buy | print | 3d-print
source: print
# The play-test page shows the body's "## Player sees" section, or this prop's image asset.
# Where the player gets it: start (in the backpack) or the puzzle whose lock releases it, e.g. PZ-004
found_in: PZ-013
envelope: PZ-013
# Physical pocket/container or location; availability remains in found_in above.
container: Envelope 13
after_game: return
# Any related record IDs, e.g. [PZ-002, Q-004]
links: []
# Set to an ID when this record is replaced. It then moves to the Parked tab.
superseded_by:
tags: []
---

The last container's contents: the fictional plane ticket and Liv's letter (see the ending premise).

**17 Oct 2026 (designer): plane ticket built.** A Nordic Air boarding pass, passenger by last name only (ERICSON, the surname already on the other tickets; Q-058 notes it points at Leif), Ottawa (YOW) to Stockholm (ARN), SUMMER 2027, open one-way; flight NA 901 is invented dressing, no exact date given. Print file `Plane_Ticket_Print.pdf`, builder `Props/Tickets/build_plane_ticket_pdf.py`. **Letter not written:** designer's start is "Congratulations! I'm so excited to see you this summer and continue our adventures! During my research, I think I found who could be one of our ancestors. I'll leave you that final puzzle to figure it out." (“something like”); the puzzle that reveals AUD is being designed (Q-062).

**17 Oct 2026 (designer): letter built, puzzle for AUD chosen (option 2: the cards with no raven).** Handwritten on lined paper with the family raven (large v2) and the Cryptic Bureau logo (approved raster concept B). Text: “Congratulations! I'm so excited to see you this summer and continue our adventures! / During my research, I think I found who could be one of our ancestors. I'll leave you that final puzzle to figure it out. / Remember the cards you set aside, the places without our raven? I didn't forget about them. One of them says something about family. Whose name is it? / I could use someone who notices what everyone else walks past. / With love, Aunt Liv.” (first two paragraphs the designer's; the third drafted by Claude and approved in chat; the closing line is PR-001's; “With love,” added by Claude to match the postcards.) **The answer is AUD:** only the decoy AD (Bjarnarhofn, on Aud's journey) says “she feels like family (and she actually maybe was)”; the other decoys (LD, RD, HD) make no family claim. Players confirm the answer on the online page (designer), not yet built. Print file `Liv_Final_Letter_Print.pdf`, builder `Props/Tickets/build_liv_final_letter_pdf.py`. Not paper-tested.

**17 Oct 2026 (designer, later):** the letter opens “My dear explorer,” (the designer typed “My dear explorer”; the comma is Claude's) and is on white office-stock lined paper (light blue rules, pink margin line), not cream.

**17 Oct 2026 (designer, Q-063): clue changed.** The third paragraph now reads “Remember the cards you set aside, the places without our raven? I didn't forget about them. On one of those cards I wondered whether someone was actually our family. Whose name is it?” (was “One of them says something about family.”). Reason: LD's message and Fun Fact also sound familial (Leif “grew up” there, “Leif's mother built…”); this echoes AD's “she actually maybe was”. Letter rebuilt, raven made slightly smaller and the text moved up one line so “Aunt Liv” clears the page bottom.

## Starting state

### 19 October 2026 Bureau memo paper

Designer selected memo-paper option 3 (Archive Sheet), with the word “Correspondence” removed. White paper, small burgundy Bureau envelope/keyhole logo and wordmark at upper left, copper margin rule and short header divider, small envelope footer emblem, and a separate black raven/knotwork stamp at upper right added by Liv. Body remains blank; text will be considered later. This supersedes the lined-paper direction for the intended revision; the existing production letter remains unchanged pending the new text/layout.

Designer subsequently set the final memo trim size to **4 × 6 inches, portrait**, to fit the small envelope. This replaces the proposed 5.5 × 8.5 inch half-Letter size. Reflow the selected layout to these dimensions when creating the Word print master; the existing concept PNG remains a proportion reference, not a physically sized print file. Physical envelope fit remains to be checked.

**19 October 2026 text added:** designer requested adding the text. Reused the current final-letter wording verbatim, including the revised decoy-card question and “With love, Aunt Liv.” New print master: `Print/Print_LivFinalMemo_4x6.docx`; exact-size source: `Print/_pdf_source/Liv_Final_Memo_4x6_Print.pdf`; builder: `Props/Tickets/build_liv_final_memo.py`. The 4 × 6 inch memo is placed on one Letter page at 100%, with a fine trim outline. Actual Cormorant Garamond header, original approved envelope logo, original family raven rendered black through its alpha, copper rules, plain white paper; handwriting is Nothing You Could Do at 12.5 pt with 16 pt leading. No Correspondence heading or background fill. All current paragraphs verified against source; final signature baseline is 71 pt above trim bottom. Both exact-size layout and Microsoft Word page export visually checked. Standard renderer unavailable because LibreOffice is absent; Word export used successfully. Prior letter retained; no website copies changed. Physical print, envelope clearance and 12.5 pt handwriting readability remain untested.

Built-in ImageGen visual preview: `Props/Tickets/Bureau_Memo_Archive_No_Label_v1_Preview.png`; raw output in `Props/Tickets/Sources/`; exact prompt in `Props/Tickets/Bureau_Memo_Archive_No_Label_v1_prompt.txt`. Preview has been visually checked: no Correspondence label or body text. Production should use original Bureau/raven assets and actual typesetting rather than treating the generated lettering as a print master.

Not recorded yet.

## Reset

Not recorded yet.

## Replacement

Not recorded yet.

**20 Oct 2026 (designer): production print size** — plane ticket → bookmark 2 × 6 in (was 7 × 2.9); memo stays 4 × 6. Decided in Q-052 (standard print sizes); not rebuilt yet. **Reopened later on 20 Oct** (designer: museum tickets smaller and all one size; travel tickets smaller, cheap and all one size); see Q-052.

**20 Oct 2026 (designer): production size decided** — final plane ticket → business card 3.5 × 2 in (was 7 × 2.9; not rebuilt); final note stays postcard 4 × 6, one side. See Q-052.
