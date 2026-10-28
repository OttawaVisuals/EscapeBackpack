---
id: PR-007
title: A mailer box with rune-marked envelopes
type: premise
# idea | candidate | decided | built | parked
status: decided
# sender | player goal | story | tone | ending | other
aspect: other
# Any related record IDs, e.g. [PZ-002, Q-004]
links: [PP-047, PP-045, Q-001, Q-046, Q-047, Q-048, Q-049, Q-050, Q-051]
# Set to an ID when this record is replaced. It then moves to the Parked tab.
superseded_by:
tags: []
---

**Decided 11 Oct 2026 (designer), after friends' feedback that padlocks are heavy and expensive.** The game is no longer a backpack with locked pockets and pouches.

- **The backpack becomes a box.** Updated 14 Oct 2026 (designer, for every adventure; backpack-kit GUIDE.md, Packaging): an **art-printed corrugated mailer box**, inside about **12 ⅛ × 9 ¼ × 2 in** (the standard letter-size "literature mailer"), so letter-size maps lie flat. It ships inside a poly or kraft mailer bag that carries the real address, so the box art never shows an owner's address when the game is lent. This replaces the board-game box: the 13 Oct rectangular board-game box and the 11 Oct 11.5 × 11.5 × 2 in square box (Q-046). Not yet checked with a sample box; printer and bag type not chosen. The fireside-table cover direction (AS-065) was drawn for a board-game box lid and needs re-checking for a mailer.
- **Pockets and pouches become envelopes.** There are no padlocks. Each of the 13 codes has one envelope, marked on the front with four runes. Updated 14 Oct 2026: **string-and-button kraft envelopes in two sizes**, 9 × 12 in for letter-size paper (designer's estimate: 5 or 6 for Norse) and a postcard size (6 × 9 in suggested, not confirmed). Decoys should come in both sizes so size alone gives nothing away. All envelopes sit loose in the box (Q-046); a few decoy envelopes may be added (Q-050).
- **Codes go into a cypher, which points to the next envelope.** Players set a code on the rune cypher wheel (PP-047) and read four runes; the envelope with those runes is the one to open.

The puzzles, codes and their order are unchanged. Envelope N holds exactly what lock N used to close (Q-001's 9 Oct table), so the release order and the Flow tab stay the same. Envelopes rely on players playing fair: nothing stops a team opening an envelope early.

| Envelope | Code | Runes | Holds |
|---|---|---|---|
| — | — | — | In the box from the start, loose on top: L1 (gives `1021` as a worked example, PZ-001) and the cypher wheel. ~~Luggage tags outside (Q-047)~~ (no tags since 14 Oct 2026) |
| 1 | `1021` | ᚷᛉᚦᛉ | AD, Aud's comb |
| 2 | `BOOK` | ᛉᛖᚠᛁ | L2, L3, magnifier |
| 3 | `1576` | ᛒᛚᛟᛉ | H2, H3, HD |
| 4 | `MEAD` | ᚱᛒᛚᚷ | A2, Aud's map, Aud's Treasure Museum ticket |
| 5 | `_532` | ᛈᚹᛟᛇ | R1, R6, RD |
| 6 | `_562` | ᛈᛏᛟᛇ | Leif's map, LD, Brattahlíð museum ticket |
| 7 | `4865` | ᚺᛏᛏᚦ | A1, A3, coin hoard, treasure tally |
| 8 | `SOLE` | ᛏᚾᚠᛖ | Rollo's map, R2, Rouen ticket |
| 9 | `1486` | ᛒᚠᛞᛉ | R3, R4, R5, ruler |
| 10 | `_120` | ᛁᛉᚲᛇ | Harald's map, H1, hnefatafl board + pieces, Oslo ticket |
| 11 | `2134` | ᛚᚹᚲᛏ | H4, H5, raven's flights card |
| 12 | `2648` | ᚲᛟᛉᛏ | H6 (with the large raven), 18 hop tickets (one page per journey) ~~and the 3 flight bookings~~ (PP-039; bookings dropped 20 Oct 2026, the ticket dates give the journey order) |
| 13 | `1972` | ᛈᛚᚹᛉ | Plane ticket (Ottawa to Stockholm, summer 2027), Liv's final letter (the AUD puzzle), adventure medallion |

**15 Oct 2026 (designer): envelopes 1 to 3 reordered.** The comb puzzle (PZ-003) now comes first, so Aud's decoy card AD is the first card players open after L1. Envelope 1 (`1021`) holds AD and the comb; solving it gives `BOOK`, which opens envelope 2 (L2, L3, magnifier); the joined top edge (PZ-002) then gives `1576`, which opens envelope 3 (H2, H3, HD). Each envelope keeps the runes of the code that opens it, so no rune strings changed, only which cards sit behind them. Codes 4 to 13 are unchanged. The designer also wants to scramble the legs further so players must sort the cards back into legs later; not designed yet (Q-059).

Runes come from `Props/CypherWheel/build_cypher_wheel_pdf.py` (seed 1021); rebuild it after any code change and the labels follow. `_` is the wheel's blank.

**What this supersedes:** the backpack and its pockets (PP-045 candidates), the pouches, all 13 padlocks, the lock number stickers (PP-046), and the compartment map in Q-001. Older text in those records describes the earlier format and is marked so.

**Not changed yet:** puzzle records keep `lock` (now just the code's format) and `reset_display`, because the kit's reset page is built around locks (Q-048). `container_in` was removed 11 Oct 2026 since nothing nests. Which envelope gets which size is open (Q-049). The two tight fits were settled 14 Oct 2026 (designer): maps are plain paper, not laminated, and lie flat in 9 × 12 envelopes; the ruler becomes a shorter printed card (PP-025, Q-052). ~~The luggage tags need a place on a box (Q-047).~~ No tags since 14 Oct 2026: L1 gives the first code (PZ-001). The digital game still plays the backpack version (Q-051).
