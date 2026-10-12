---
id: PR-007
title: A board-game box with rune-marked envelopes
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

- **The backpack becomes a box**, 11.5 × 11.5 × 2 in, like a board-game box (Q-046).
- **Pockets and pouches become envelopes.** There are no padlocks. Each of the 13 codes has one envelope, marked on the front with four runes. All envelopes sit loose in the box (Q-046); a few decoy envelopes may be added (Q-050).
- **Codes go into a cypher, which points to the next envelope.** Players set a code on the rune cypher wheel (PP-047) and read four runes; the envelope with those runes is the one to open.

The puzzles, codes and their order are unchanged. Envelope N holds exactly what lock N used to close (Q-001's 9 Oct table), so the release order and the Flow tab stay the same. Envelopes rely on players playing fair: nothing stops a team opening an envelope early.

| Envelope | Code | Runes | Holds |
|---|---|---|---|
| — | — | — | In the box from the start: L1; luggage tags outside (Q-047); the cypher wheel |
| 1 | `1021` | ᚷᛉᚦᛉ | L2, L3, magnifier |
| 2 | `1576` | ᛒᛚᛟᛉ | AD, Aud's comb |
| 3 | `BOOK` | ᛉᛖᚠᛁ | H2, H3, HD |
| 4 | `MEAD` | ᚱᛒᛚᚷ | A2, Aud's map, Aud's Treasure Museum ticket, ruler |
| 5 | `_521` | ᚷᛉᛟᛇ | R1, R6, RD |
| 6 | `_562` | ᛈᛏᛟᛇ | Leif's map, LD, Brattahlíð museum ticket |
| 7 | `3212` | ᛈᛞᛁᛟ | A1, A3, coin hoard, treasure tally |
| 8 | `SOLE` | ᛏᚾᚠᛖ | Rollo's map, R2, Rouen ticket |
| 9 | `1486` | ᛒᚠᛞᛉ | R3, R4, R5 |
| 10 | `_104` | ᛚᚷᚲᛇ | Harald's map, H1, hnefatafl board + pieces, Oslo ticket |
| 11 | `_253` | ᛊᚲᛁᛇ | H4, H5, raven's flights card |
| 12 | `2648` | ᚲᛟᛉᛏ | H6, transition tickets, Liv's journal, crest note |
| 13 | `1972` | ᛈᛚᚹᛉ | Plane ticket and letter, adventure medallion |

Runes come from `Props/CypherWheel/build_cypher_wheel_pdf.py` (seed 1021); rebuild it after any code change and the labels follow. `_` is the wheel's blank.

**What this supersedes:** the backpack and its pockets (PP-045 candidates), the pouches, all 13 padlocks, the lock number stickers (PP-046), and the compartment map in Q-001. Older text in those records describes the earlier format and is marked so.

**Not changed yet:** puzzle records keep `lock` (now just the code's format) and `reset_display`, because the kit's reset page is built around locks (Q-048). `container_in` was removed 11 Oct 2026 since nothing nests. Envelope sizes are open (Q-049): the laminated maps and a 30 cm ruler are the tight fits. The luggage tags need a place on a box (Q-047). The digital game still plays the backpack version (Q-051).
