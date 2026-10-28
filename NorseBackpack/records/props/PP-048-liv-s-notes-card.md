---
id: PP-048
title: Liv's notes card
type: prop
# idea | candidate | decided | built | parked
status: decided
# physical | printed | digital
form: printed
# make | buy | print | 3d-print
source: print
# Where the player finds it: start (loose in the box) or the puzzle whose answer opens its envelope, e.g. PZ-004
envelope: start
# On the public reset page: return (back in its envelope) | keep (the team takes it home) | none (not mentioned). Blank = return.
after_game: return
# Name on the public reset page, if the title isn't what players call it (optional)
reset_name: Liv's notes
# Any related record IDs, e.g. [PZ-002, Q-004]
links: [PP-001, PZ-004, PZ-006, PZ-009, PZ-011, PP-025]
# Set to an ID when this record is replaced. It is then hidden unless the board's "parked" filter is on.
superseded_by:
tags: []
---

**15 Oct 2026 (designer, playtest feedback):** players did not know "crossbow bolt" and struggled with "mead". Instead of explaining each word inside its own puzzle, one small **notes card from Liv comes with postcard L1** (L1 has no room for it). It gives the full names of the four travellers and a short list of words from the area. Not built yet; wording below is the approved draft.

What it is: a small printed card, same style as the postcards (Liv's handwriting font), loose with L1 at the start. It is a plain reference list, no riddles or hints.

**Rules for the word list**
- Never list or define a lock answer or a rebus answer (BOOK, SOLE, TREATY and so on).
- Longship and spear are on the list on purpose (15 Oct 2026): they are the two ruler edges (PP-025). Listing them makes the ruler a match-up, not a hard decode, and they sit among other words so they don't stand out.
- Only list words some clue actually uses, plus a few look-alikes. More words can be added later without redrawing a postcard.

## Player sees
**Liv's notes**

I've discovered a lot of words I never knew before. They might be useful to you too, so keep this card handy all the way through! *(intro extended 15 Oct 2026, designer)*

**Who's who**
- **Leif Erikson**: Norse explorer who sailed to North America
- **Aud the Deep-Minded**: Viking settler who sailed to Iceland
- **Rollo**: Viking leader, first ruler of Normandy
- **Harald Hardrada**: Norse king who served the emperor in Constantinople

**Words**
- **Chainmail**: flexible armour made from interlocking iron rings
- **Crossbow bolt**: short arrow fired from a crossbow
- **Ford**: a shallow place where you can wade across a river
- **Hoard**: a hidden stash of treasure
- **Longship**: a long, narrow Viking ship with oars and a sail
- **Mead**: a drink of the feasting hall, made with honey
- **Rune**: a letter of the old Norse alphabet, made of straight lines for carving
- **Runestone**: a carved stone with a message
- **Spear**: a long pole with a pointed head, for thrusting or throwing
- **Tapestry**: a large woven cloth that tells a story in pictures

## Open items
- **Descriptions unchecked.** Rollo "first ruler of Normandy" and Harald "served the emperor" come from general knowledge and card text, not checked against sources.
- **Mead wording.** "Made with honey" overlaps the HONEY / DRINK / FERMENTED riddles (PZ-004). The vaguer "a drink of the feasting hall" was offered; the designer kept the honey version in the draft.
- **Filler words.** Chainmail, hoard, runestone and tapestry only stay if some clue or decoy needs them.
- **Layout:** mock-up built 15 Oct 2026, 4 × 6 in portrait, postcard paper, border and fonts (Cinzel terms, Liv's handwriting font for definitions). Script `Props/LivNotes/build_liv_notes_pdf.py`; print PDF `NorseBackpack/Print/_pdf_source/Liv_Notes_Card_Print.pdf`; preview `Props/LivNotes/Liv_Notes_Card_Preview.png`. About 78 pt of free space at the bottom (room for 5 or 6 more words). Card size, paper and a paper print test are not decided.

## Reset
Return to its envelope with L1.

**15 Oct 2026 (designer):** added **Saga**: “an old Icelandic story about heroes and families, written down in the Middle Ages” (between Runestone and Spear). The words list is now eleven. Card rebuilt (`Props/LivNotes/build_liv_notes_pdf.py`, text ends at y 34 pt, border at 12 pt); checked in the PNG render only.


## 17 Oct 2026: Two-sided glossary readability draft (Codex)

**Superseded in part by the designer feedback below.**

Designer requested larger term labels. Proposed revision keeps the **4 x 6 in card** and uses both sides: front carries Liv's existing introduction and four people; reverse carries all eleven glossary terms in the existing order. Person names are **12 pt bold**, definitions remain in Liv's handwriting at 12 pt; glossary labels and handwritten definitions are **11.5 pt**, with 14.5 pt leading. Introduction is 12.5 pt handwriting. Teal labels, rust dividers, cream paper and the border retain the postcard style. Intro, people descriptions and definitions are imported verbatim; the approved honey wording for Mead is unchanged.

Review and print pack pages **5-6**. Front includes "WORDS ON THE REVERSE" so the second side is discoverable. No new definitions or historical claims. Both sides visually checked, all four people and eleven terms verified. Proposed replacement only; physical legibility still needs checking.


Shared source: `Props/ReadabilityDrafts/build_readability_drafts.py`. Outputs at repository root: `NorseBackpack/Print/_pdf_source/Readability_Redesign_Drafts/Readability_Drafts_Review.pdf` and `NorseBackpack/Print/_pdf_source/Readability_Redesign_Drafts/Readability_Drafts_Letter_Print.pdf`. These are separate review/print drafts; live sources, print masters, website copies and print-test DOCX files are unchanged. No new AI artwork was generated. Print the Letter pack at 100%, long-edge duplex. Paper readability, envelope fit and printer registration have not been tested.


## 17 Oct 2026: Designer correction - single-sided Liv notes

**Landscape arrangement superseded by the portrait revision below.**

The designer prefers one side only, no larger than a postcard. The revised draft is **6 x 4 in landscape, one printed side**, with the existing introduction, all four people and all eleven terms retained verbatim. Two columns: Who's who and the first four terms on the left; the remaining seven terms on the right. Term labels use bold teal **10.5 pt** type and definitions retain Liv's handwriting at **10.5 pt / 11.5 pt leading**. The two-sided 4 x 6 layout above is superseded.

Review PDF page **5** holds the entire note. Letter print-pack page **5** is its front; page **6** intentionally leaves the card area blank so the pack can still be printed duplex. Print page 5 alone for a single-sided note. Physical print readability remains untested.

## 17 Oct 2026: Portrait revision requested by designer

The latest draft is **4 x 6 in portrait, single-sided**, with one continuous column: introduction, Who's who, then Words. All original wording, four people and eleven terms are retained. Labels and handwritten definitions remain **10.5 pt**, with **11.5 pt leading**; the portrait reflow does not shrink the text. Cream paper, teal labels, rust section headings and fine border retained.

Shared draft builder and output paths above remain unchanged. Review and Letter page **5** show the revised note; Letter page **6** remains blank inside the crop marks. Print page 5 at 100% / Actual size for a one-sided card. Rendered card and both affected print sheets checked; text extraction confirms all wording and PDF bounds checks pass. Physical print readability remains untested. Production masters are unchanged pending completion of the draft review.

**17 Oct 2026 (designer):** Liv's notes card is **not** adopted with the other readability drafts; the portrait draft's spacing is being worked on in chat.

**17 Oct 2026 (designer): readability redesign adopted into the live print file.** Same text, 4 × 6 in portrait, one-sided. Title 14 pt Cinzel ExtraBold; intro and definitions 10 pt handwriting (line spacing 11 pt); term labels and the two headings 8 pt Helvetica Bold; 2 pt between entries; text ends 13 pt above the border. (Codex's draft was 19 / 10.5 / 9 / 10.5 pt with no spacing; the designer tuned it in chat.) `Liv_Notes_Card_Print.pdf` replaced by `Props/ReadabilityDrafts/adopt_to_live.py`; old PDF kept in `C:\EscapeBackpack\Norse_Snapshots\Norse_2026-10-17_PreReadability\`; the old builder is marked superseded for print. Not paper-tested.

## 20 Oct 2026: Help and code guide reverse (Codex)
**Adopted by the designer on 20 Oct 2026. This supersedes the earlier single-sided specification.** The 4 × 6 in card now has the original names and glossary on the front, with help access and the code-format guide on its back. Warm personal wording from Liv, simple page border, Norse knotwork only around the hint QR, no printed background on the reverse. `Props/LivNotes/Liv_Notes_Back.png` is the transparent 1024 × 1536 PNG (256 dpi). All 13 puzzle formats follow current PR-007 envelope order; answers omitted. Original supplied QR inserted mechanically into the frame, white areas transparent. Built-in ImageGen prompt and raw artwork/QR retained in `Props/LivNotes/Sources/`.

Current print masters: `Print/Print_LivNotesCard.docx` (two aligned Letter pages) and `Print/_pdf_source/Liv_Notes_Card_Print.pdf` (two 4 × 6 in pages). Front unchanged. Print Word at **Actual size, duplex, flip on long edge**. Builder: `Props/LivNotes/build_liv_notes_back.py`; the readability adoption script now retains this reverse when rebuilding the front. Previous single-sided masters archived at `C:/EscapeBackpack/Norse_Archive/NorseBackpack/Props/LivNotes/Before_Help_Back_20261020/`. Full Adventure previews show both faces. Word export checked visually; physical print alignment and phone scan remain untested.

Reverse wording: “If you’re feeling stuck, I’ve put together a little help for you.” / “Scan here for a hint.” / “Not sure what kind of code you’re looking for? I’ve made you a guide.” Signed Liv. Puzzle formats 1–13: 4 digits, 4 letters, 4 digits, 4 letters, 3 digits, 3 digits, 4 digits, 4 letters, 4 digits, 3 digits, 4 digits, 4 digits, 4 digits.

## 20 Oct 2026: Background-free front and raised print placement
Designer requested removal of the remaining front background and moving pictures toward the top. Removed the full-card cream PDF fill; retained all names, glossary wording, text colours and the fine border. Both card faces now have no printed background. Current Print_LivNotesCard.docx places each 4 × 6 inch face at x 2.25 in / y 0.5 in on Letter, aligned for long-edge duplex. This supersedes the earlier vertically centered placement. Current card PDF/front source/previews refreshed; QR artwork unchanged. Both specific and generic Word builders preserve the new placement. Previous masters archived in C:/EscapeBackpack/Norse_Archive/NorseBackpack/Props/LivNotes/Before_No_Background_Top_20261020/. Verified front text, reverse PDF stream and Word anchors; Word-exported pages inspected. Physical print/scan still untested.

**20 Oct 2026 (cut guide requested):** Word print sheet now has a 0.5 pt grey dashed rectangle on page 1 at the exact 4 × 6 inch trim, outside the decorative border. Cut along this outer dashed line. No second cut line on reverse. Both Word builders preserve the guide; placement remains x 2.25 / y 0.5 in on Letter. Word export inspected. Previous Word version archived in Before_Cut_Border_20261020.
