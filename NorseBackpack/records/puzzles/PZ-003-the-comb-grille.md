---
id: PZ-003
title: The comb grille
type: puzzle
# idea | candidate | decided | built | parked
status: decided
# The structure beat this puzzle belongs to (one ID)
beat: ST-004
# Props the player needs, e.g. [PP-001]
props: [PP-015, PP-028]
# Puzzles that must be solved first, e.g. [PZ-002]
needs: [PZ-001]
# cipher | physical | search | logic | wordplay | other
mechanic: physical
# 1 (easy) to 3 (hard)
difficulty: 1
# Lock it opens: 3-digit | 4-digit | 4-letter | 3-digit-colour (blank if none)
lock: 4-letter
answer: BOOK
envelope_marks: ᛉᛖᚠᛁ
# Compartment this lock closes (shown on the Locks tab)
container: Envelope 2
reset_display: LOCK
# What players call this lock on the hint page, e.g. "The luggage tag" (spoiler-free)
hint_title: Just opened ᚷᛉᚦᛉ
# Explicit opt-in for the PUBLIC hint page. Candidates are never published.
publish_hints: yes
# Independent of design/build status: untested | passed | changes-needed
test_status: untested
# physical | digital (a digital walkthrough does not verify a physical prop)
test_method:
# Optional stable Clue Library technique link
technique:
# Any related record IDs, e.g. [PZ-002, Q-004]
links: []
# Set to an ID when this record is replaced. It then moves to the Parked tab.
superseded_by:
tags: []
---

## How it works

Aud’s comb, laid upright on the decoy card’s message, covers every line except the four its broken teeth leave open.

Lock 3 of 13 in the release order decided 7 Oct 2026 (Q-005). Difficulty 1 of 3 is Claude's estimate from the mechanism (number of props and steps), not playtest data.

**9 Oct 2026 (designer, Q-001):** now lock 3 of 13. Compartment: left pocket (seen from the front).

**11 Oct 2026 (designer, PR-007):** no locks or pockets any more. This code, set on the rune cypher wheel (PP-047), points to envelope 3, which holds what lock 3 used to close.


**13 Oct 2026 (6 × 4 in card, PR-004):** AD's message rewraps in the wider column, so “alongside” now starts its line and can't give the second O. The comb now opens c**o**uld (line 3), s**o** (line 6, “It was so awesome…”) and **k**eep (line 8, which now starts its line, so that tooth is broken off at the root); the first B is unchanged. The answer is still **BOOK**. The comb grew with the card: 101 × 75 mm overall (was 69 × 66), 12 teeth (was 13), 90 mm long (was 59) and 3.0 mm wide (was 2.5), 1.55 mm gaps. The printed ring-and-dots moved to (24, 20) and (24, 214) pt. **Test print pending** at the new size.
## Player notices

The comb and decoy postcard AD (Bjarnarhöfn), both in envelope 1, opened by `1021` from L1 (since 15 Oct 2026, PR-007); ~~both released by lock 2 (1576), 7 Oct 2026 (Q-005)~~; ~~both released by SOLE~~.

## Player does

Sit the comb’s two end ring-and-dots over the two printed on AD, handle in the left margin, teeth across the message. One tooth covers each line. Read the first letter showing on each line that is not covered.

## Player obtains

Code **BOOK**. Set on the wheel, it opens envelope 2 (L2, L3, magnifier: PP-002, PP-003, PP-027). ~~Opening this lock releases PP-017, PP-018, PP-022.~~

## Story reason

Gives the comb a job as an instrument rather than a keepsake, and gives the Aud decoy a reason to be kept rather than discarded.

## Clue wording

AD’s message (15 Oct 2026): "Bjarnarhöfn today, / One of the stops on my way to follow the path of Aud the Deep-Minded. / She sailed here with her family and a shipful of followers, then claimed land of her own. / I’ve read everything I could find about her this trip, to the point that she feels like family (and she actually maybe was). / During my expedition, I managed to find a comb that might have belonged to her. So cool! A piece of history we can use! / With love, Aunt Liv". The ring-and-dots on AD match the ones on the comb (and on AD’s own stamp).

**Superseded 15 Oct 2026:** "At her brother’s harbor — the one Aud wintered in. I’ve read everything I could find about her this trip, to the point that she feels like family (and she actually maybe was). It was so awesome to find that comb, and the museum let me keep it! This is actually the real treasure, a piece of history that we can use!"

## Hints

1. The two ring-and-dots on the card match the two on the comb.
2. Line the comb up so its holes sit over the printed dots — handle on the left, teeth over the writing.
3. Some teeth are broken. Read the first letter you can see on each line they leave open, from top to bottom.

(Unchanged by the 15 Oct 2026 message rewrite.)

## Solution
With the comb in place only four lines show: **B**jarnarhöfn today, / **o** follow the / **o**f followers, then claimed land of her / **k**e (the end of “feels like”). Reading the first visible letter of each, top to bottom: **BOOK**. (Changed 15 Oct 2026 with AD's new message; the lines are 1, 2, 5 and 8.)

**Superseded 15 Oct 2026:** **b**rother’s harbor… / c**o**uld… / **o** awesome to find that comb / **k**eep it!

**Superseded 13 Oct 2026** (5 × 3.5 in card): With the comb in place only four lines show: **b**rother’s harbor… / **o**uld find about / **o**ngside the coins… / **k**eep it! Reading the first visible letter of each, top to bottom: **BOOK**.

## Solution notes

Design-side solution text, kept when the player-facing Solution above was written for the hint page (9 Oct 2026).

**Decided 25 Sept 2026.** With the comb in place only four lines show: **b**rother’s harbor… / **o**uld find about / **o**ngside the coins… / **k**eep it! — B O O K, top to bottom. BOOK links to **Landnámabók** ("Book of Settlements"), the source Q-032 cites for Aud’s comb, and to "I’ve read everything I could find".

## Open risks

Test print pending: the seven intact teeth are 52 mm long and 2.2 mm wide, and the marks sit 4.5 mm from the card edge, so trimming must be accurate. The comb is generated from AD’s printed layout by Props/Comb/build_comb.py — any change to AD’s back needs a comb rebuild. Since 15 Oct 2026 the B tooth is a 0.74 mm stub and tall/low letter tails peek between teeth (see the render note).

## Releases (as worded on the old page)

**Superseded 9 Oct 2026** by the compartment map in Q-001; the current release list is under Player obtains.

**Since 7 Oct 2026 (Q-005):** lock 3; releases postcards H2, H3 and HD. ~~H4, H5, Harald’s map and the raven’s flights card — entry to Harald’s leg (step 9 of old page PC-18)~~

Lock as recorded: Four-letter word lock (one of the three owned, Q-026). Old page status: Mechanism decided · comb modelled, test print pending.

**14 Oct 2026 (designer, box + envelopes):** AD drops “alongside the coins” (AD now arrives in envelope 2, before the coins in envelope 7). The message is one line shorter (9 lines + sign-off, 11 teeth), and “keep” now sits mid-line 7 (“the museum let me keep it!”), so its tooth is an ordinary broken tooth. Visible text: **b**rother’s harbor… / **o**uld find about her… / **o** awesome to find that comb, and / **k**eep it! Still **BOOK**. Comb outline unchanged at 100.7 × 75.1 mm; marks unchanged. Test print pending.

**15 Oct 2026 (designer, PR-007):** the comb grille moves to the front. AD and the comb are now in envelope 1 (opened by `1021` from L1); `BOOK` opens envelope 2 (L2, L3, magnifier). PZ-003 now needs only PZ-001; PZ-002 needs PZ-003. Aud's decoy is the first card players open after L1. The puzzle itself is unchanged. AD's message ("alongside the coins" already dropped) still reads correctly this early. Test print of the comb still pending.

**15 Oct 2026 (designer): AD's message rewritten (PP-015).** ~~The comb is not updated yet~~ (superseded by the next note: the comb was rebuilt). The old line-start letters (b, o, o, k) are gone, so the current comb no longer spells BOOK on the new card, and `Props/Comb/build_comb.py` will fail its BOOK check until the comb is redesigned. The lower ring-and-dot mark also moved (y 250 pt), so the holes are further apart than the printed comb. Open: choose which first-visible letters give B, O, O, K in the new text, then rebuild the comb (and the digital copy). The “Solution” and “Clue wording” above describe the old message.

**15 Oct 2026 (designer, later): comb letters chosen and the comb rebuilt for the new AD message (PP-015).** Visible line starts: line 1 **B**jarnarhöfn (first letter; the tooth is a 0.74 mm stub), line 2 “way t**o** follow”, line 5 “shipful **o**f followers”, line 8 “feels like”, with “li” covered so that **k**e shows. Answer still **BOOK**. The comb has 14 teeth (12 message lines + 2 signature), 100.7 × 87.8 mm, holes 81.1 mm apart (lower mark at y 250 pt). **Not checked:** how the long hanging letters (g, y, p tails, ascenders) peek out under intact teeth in the render, whether the 0.74 mm B stub survives printing, and the player-facing Solution, Clue wording and hints above, which still describe the old message. Test print pending.

**15 Oct 2026 (render check):** full-card overlay `Props/Comb/Aud_Comb_on_AD.png` (now the whole card; the old fixed crop had cut off the revealed text) reads **B**jarnarhöfn today, / **o** follow the / **o**f followers, then claimed land of her / **K**e. Teeth cover everything else except small tails of tall and descending letters (g, y, p, l, k) that show in the gaps; they do not form words. Line 1 shows its whole line because the B tooth is a 0.74 mm stub (weak on a print). Screen render only; test print pending.
