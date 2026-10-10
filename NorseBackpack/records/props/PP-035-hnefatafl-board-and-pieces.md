---
id: PP-035
title: Hnefatafl board and pieces
type: prop
# idea | candidate | decided | built | parked
status: decided
# physical | printed | digital
form: physical
# make | buy | print | 3d-print
source: 3d-print
# The play-test page shows the body's "## Player sees" section, or this prop's image asset.
# Where the player gets it: start (in the backpack) or the puzzle whose lock releases it, e.g. PZ-004
found_in: PZ-011
# Physical pocket/container or location; availability remains in found_in above.
container: Large pouch, in the main compartment (lock 10)
after_game: return
# Any related record IDs, e.g. [PZ-002, Q-004]
links: []
# Set to an ID when this record is replaced. It then moves to the Parked tab.
superseded_by:
tags: [old-PR-08]
---

## From the old Props & specs tab

Prop

### Hnefatafl: escape path and museum ticket

Three connected pieces — a setup split across two sheets of paper, a three-move escape, and a code read from the king's own travel. Arrives with Harald's trail, via the Oslo postcard (stop 1).

#### The rules, and where they come from

The rules are **printed matter, not her handwriting**: an admission ticket from the Hnefatafl Museum in Oslo, tucked into the bag with the Oslo postcard. That keeps the voice rule intact — printed pages carry real history, her hand carries the task. **The ticket explains the real historical game only** — it does not describe this puzzle's own house rules, and gives no hint that this board's dark pieces never move.

Light pieces defend the king at the centre. Dark pieces start around the edges and try to trap him. Every piece slides any distance in a straight line, like a rook in chess. Trap an enemy piece between two of your own to capture it. The king escapes by reaching a corner. The attackers win by trapping him first.

The ticket can say honestly that no complete Viking-Age tafl ruleset survives and that these rules are one reconstruction. Its text is subject to old page HI-05 before it is printed. The museum is invented deliberately; the real Oslo institution is the Viking Ship Museum, and the prop should not borrow it.

**Her task, on the Oslo postcard, in her own words:** “We like to play our own rules though: can you get the king to escape to a corner in exactly three moves?” The word **exactly** is what forces the solution to be unique.

Built: `Props/Hnefatafl/build_ticket_pdf.py` → `output/pdf/Hnefatafl_Ticket_Print.pdf`.

![Hnefatafl ticket, front](Props/_Renders/Hnefatafl_Ticket_Front.png)Front

![Hnefatafl ticket, back, mirrored board strip](Props/_Renders/Hnefatafl_Ticket_Back.png)Back · mirrored strip

#### The setup: one board across two papers

**Approved 25 September 2026 — hand-drawn setup and mirrored wet-ticket transfer (PP-036).** The board now uses Liv's existing *Nothing You Could Do* handwriting, gently uneven pen lines, irregular outlined pieces and hand-shaded dark pieces. The approved smudge artwork is unchanged. Her note now reads Oops - ticket was still wet when I set it down here. Sorry, past me. - L; the earlier glue explanation is superseded. Columns I–K still omit three attackers and two corner markers. The museum ticket's reverse is rebuilt from the same original strokes, reflected horizontally in full, including the handwriting and shading, so reading it through the paper restores their orientation. The shared 0.4-inch cell pitch and all piece positions are unchanged. Both panels use `Props/Hnefatafl/hand_drawn_board.py`; grid intersections stay fixed while pen curves vary only between them. A physical hold-to-light and laminate test remains open.

![Current hand-drawn hnefatafl setup with the approved wet-ticket smudge over columns I to K](Props/_Renders/Hnefatafl_Board_Setup_Insert_Insert.png)Current handwritten setup · approved smudge retained; hidden tokens are absent.

![Matching hand-drawn mirrored ticket reverse with reflected K J I labels, three dark pieces and two corners](Props/_Renders/Hnefatafl_Ticket_Back.png)Matching ticket reverse · the actual pen strokes and letters are mirrored.

[Open matching ticket PDF](../Web/pdf/Hnefatafl_Ticket_Print.pdf) · [Open Letter ticket print sheet](../Web/pdf/Hnefatafl_Ticket_Letter_Print.pdf)

[Open insert PDF](../Web/pdf/Hnefatafl_Board_Setup_Insert.pdf) · [Open Harald map PDF](../Web/pdf/Trail_Map_4_Harald_Print.pdf) · [Open answer PDF](../Web/pdf/Trail_Map_4_Harald_ANSWER.pdf). Source overlay: `Props/Hnefatafl/Hnefatafl_Glue_Smear_v1.png`, copied unchanged from the built-in ImageGen output, with its alpha preserved and drawn at 72% PDF opacity. Rebuild `Props/Hnefatafl/build_board_setup_pdf.py` and `Props/Hnefatafl/build_ticket_pdf.py`, then `TravelMap/build_trail_maps_pdf.py harald`; refresh the insert, ticket-back and Harald-back previews using `build_page_images.py`. Print at 100% / actual size, with no fit-to-page scaling.

**Original ImageGen prompt — texture retained; glue explanation superseded**

```
Use case: illustration-story
Asset type: isolated transparent raster overlay for a printable escape-game board setup.
Primary request: a believable dried glue-and-lifted-ink smear left after a long narrow paper ticket was stuck onto a cream notebook page and peeled away. Generate ONLY the residue, not the paper or board.
Composition: tall portrait 1:3 canvas. One continuous elongated vertical swath occupying most of the height and width, nearly full width through its middle; gently uneven parallel sides, softly rounded ragged ends, tiny feathered fibres and irregular rubbed edges. The silhouette must read as a long ticket contact area, but must have no straight rectangular border, sharp polygon corners or pointed ends. Leave a narrow fully transparent margin all around.
Materials: thin translucent warm honey-beige dried adhesive, mottled pale milky fibres, faint dragged grey-green ink in soft irregular rubbed streaks. Restrained flat scan-like material texture. A few darker soft traces toward the right edge; no distinguishable symbols. Keep the centre light and translucent enough that a printed grid underneath remains readable.
Palette: muted warm tan, pale ochre, grey-green ink; suitable over #EFE3C4 paper with #283B34 print.
Constraints: genuine alpha transparency outside AND varied translucency within the residue. No background sheet, paper rectangle, checkerboard, board, grid, squares, circles, tokens, letters, numerals, text, watermark, objects, hand, brush, photograph of a desk, shadow, raised 3D ridges, coffee ring, liquid puddle, splashes, blood or black mass. No overall parchment texture. Only this single organic glue residue overlay.
```

Liv wrote the piece positions on the back of Harald's Oslo trail map. The ticket was still wet when it was set down on the drawing, and the right-hand strip **lifted off** — what is left on the map is an illegible stain, and the clean copy is on the ticket's blank back panel, **mirrored**.

- **The gap announces itself.** The grid lines and column letters run into the stain, so the board is eleven columns wide, with A–H readable and I–K visibly damaged. The earlier seven-column/two-column description is superseded. Nobody has to deduce that a second sheet exists; the stain is the shape of the object that took the ink.
- **Reading it:** hold the ticket to the light and read the offset through the paper — mirrored twice, so it reads correctly — then butt it against the map. The offset must therefore land on an otherwise blank panel with no printing opposite it, on stock thin enough to show through (PP-036).
- **Registration is self-verifying.** The grid lines cross the join, so only one alignment makes them continue. A one-square misalignment is visible rather than silent.
- **Guessing does not produce a wrong answer.** Verified by search: the full board has exactly one three-move escape, but if a player assumes the hidden strip is empty the current 11 × 11 layout has **31** candidate routes (the earlier 18-route count belonged to the superseded prototype). The puzzle refuses to resolve instead of resolving wrongly — the failure mode you want in a bag nobody can debug mid-play.

Both the stain and the offset are **printed**, not real ink, so the prop is stable and reprintable. This also gives the built Harald map a job before the final puzzle: players handle it mid-game and get used to it, without learning what it is finally for.

![Liv's hand-drawn incomplete eleven by eleven hnefatafl setup on plain white document paper, with the rightmost three columns reduced to pale broken and offset ink remnants](Props/Hnefatafl/Hnefatafl_Incomplete_Board_Sketch_v3.png) **Earlier incomplete setup sketch · v3, retained as a study.** The current production render is shown above (25 September 2026). This ImageGen study is a 1254 × 1254 px PNG: another sheet blotted and lifted the still-wet ink from columns I–K, leaving mostly white paper with broken grid fragments, offset ghosts and small dragged marks. The information is missing rather than covered. The visible A–H setup remains exact; v1 and v2 are retained as superseded directions.

**Exact ImageGen prompt**

```
Use case: precise-object-edit
Asset type: revised game-prop artwork
Image 1: edit target. Preserve the white paper, the 11×11 board, and every visible token exactly.
Primary request: Change only the heavy dark damaged area over the rightmost three columns. Replace it with a restrained, realistic area of ink that was blotted/lifted when another sheet touched the still-wet drawing and was peeled away.
Damaged-area appearance:
- white paper must remain visually dominant—roughly 70–80% of the I–K area should still look white;
- most original grid ink in I–K has transferred away, leaving pale broken line segments, incomplete square fragments, small offset ghost marks, tiny feathered edges, and a few short directional drag streaks;
- use sparse, low-density green-grey remnants rather than a continuous dark shape;
- no large dark patch, no solid coverage, no dramatic splatter, no brown color;
- the information is unreadable because key strokes are missing, interrupted, doubled, and displaced—not because anything covers them;
- the damage boundary is subtle and irregular around the H/I edge, with column H and its H5 attacker still fully readable.
Hard invariants:
- do not alter the clean plain white/off-white document paper elsewhere;
- do not redraw, move, add, remove, resize, or restyle the grid or any visible mark in columns A–H;
- keep exactly 11×11 cells;
- keep visible attackers exactly at A4, A5, A8, B1, D11, D6, E11, F1, F11, F9, G1, G8 and H5;
- keep visible hollow defenders exactly at C5, E8, F5, F8, G5 and G7;
- keep the rust king at F6 and rust diamonds at A1 and A11;
- no new visible tokens;
- I–K must remain too incomplete to reconstruct reliably, including the hidden I6, K4, K8, K1 and K11 marks.
No text, labels, numbers, title, caption, logo, watermark, hands, second sheet, parchment, tea/coffee stain, dense black mass, rectangular block, heavy splatter, perspective change, or decorative additions.
```

![The separate white paper carrying a mirrored three-column by eleven-row transferred-ink strip, with three dark pieces and two rust corner diamonds](Props/Hnefatafl/Hnefatafl_Transferred_Ink_Paper_v1.png) **Earlier transferred-ink companion paper · v1, superseded as a production asset.** Use the matching handwritten ticket PDF above; this image is retained as a study. ImageGen render, 1254 × 1254 px PNG. Only the lifted strip appears: columns K–J–I from left to right, with K8, K4 and I6 plus the K11/K1 corner diamonds. The contact face is horizontally mirrored, ready to be read through or flipped back into alignment.

**Exact companion-paper ImageGen prompt**

```
Use case: illustration-story
Asset type: high-resolution companion paper prop for the incomplete hnefatafl setup
Image 1: style and geometry reference only. Do not reproduce its full 11×11 board. Create the separate sheet that touched its damaged right side and received the transferred ink.
Primary request: Show a single plain white/off-white piece of paper, viewed straight overhead. On it is only the transferred impression of the original board's rightmost three columns. The transferred strip is a narrow 3-column by 11-row hand-drawn grid fragment, mirrored horizontally relative to the original board: visual column order K, J, I from left to right. Rows remain 11 at top to 1 at bottom.
Exact transferred marks:
- In mirrored column K, place dark filled square attackers at row 8 and row 4, plus rust open diamonds at row 11 and row 1.
- Mirrored column J is empty.
- In mirrored column I, place one dark filled square attacker at row 6.
- No king and no defenders appear on this sheet.
Transfer appearance: the second sheet absorbed most of the still-wet ink. The 3×11 grid and five marks are readable enough to reconstruct, but imperfect: slightly doubled edges, feathered ink, small missing flecks, faint offset ghosts and a few short drag streaks. Keep individual cell boundaries and token identities clear. It should visibly correspond to the pale missing fragments in Image 1.
Composition: the narrow vertical transferred strip occupies the central area of the white sheet with generous blank paper around it; square overall canvas; no other board columns.
Style/medium: casual transferred pen ink, matching Image 1's handmade line weight and dark ink-green #283B34. Rust #B56A2A transfers for the two diamonds, slightly faded and imperfect. Ordinary white document paper, not parchment.
Physical logic: this is the inked contact face after the top paper has been lifted and turned over for viewing, so the transferred strip is horizontally mirrored. It is an accidental offset print, not a newly drawn clean copy.
Text: none.
Constraints: exactly 3 columns and exactly 11 rows; exact token positions listed above; no additional tokens or marks; high-resolution PNG; straight overhead.
Avoid: full 11×11 board, letters, numbers, labels, title, caption, logo, watermark, hands, desk props, second paper, parchment, tea/coffee stains, dense black mass, dramatic splatter, polished modern diagram, perspective distortion.
```

**Current production files, approved 25 September 2026:** `Props/Hnefatafl/board_layout.py` defines the 11 × 11 geometry at 0.4-inch cell pitch; `hand_drawn_board.py` supplies identical pen strokes to both builders. `build_board_setup_pdf.py` makes the standalone proof insert and supplies the drawing composited onto page 2 of Harald's Print and ANSWER map PDFs. `build_ticket_pdf.py` makes both the trimmed ticket and Letter print sheet with the reflected I–K strip. **Superseded:** the earlier 0.5-inch pitch, standalone-only status and claim that Harald's map was missing. The diagram below is an older seven-by-seven study, not the current print geometry.

![Three panels: the back of the trail map with five board columns and a smear over the missing two; the museum ticket carrying the mirrored offset of those two columns alongside its printed rules; and the two lined up, showing the complete board and the king's three-move escape](Art/Diagrams/Diagram_Board_Setup_Transfer.svg) **The setup, split (illustrative only — superseded by the built panels above).** Left: the map back keeps columns A–E; the grid lines and column letters run into the stain, so the missing two columns are visible rather than inferred. Centre: the ticket’s blank back panel holds the offset, its column letters reading **G F** right to left. Right: flipped, read through the paper and aligned on the grid lines, the board completes and the only three-move escape resolves — legs of 2, 3 and 1 squares, code `231`. Its 14-blocker prototype and rectangular blot are superseded; the current props use the 11 × 11 layout and approved organic smudge shown above.

#### The escape, and the code

On the 11×11 layout in the Prototype tab (the user's own final design) the unique solution is **F6 → H6 → H11 → K11**. The legs measure **2, 5 and 3** squares, so the code is `253`.

**Nothing is printed on the board.** The earlier plan — digits on the landing squares, or four moves into a directional lock — is superseded (PZ-008). Reading the code off the king's own travel works on a bought board as well as a built one, and it stops the board from announcing itself as a puzzle prop.

#### What the board feeds, and what buying it costs

**The throne compartment is dropped.** No cavity, no cavity-key king piece. The board is just the puzzle: solve the three-move escape, read the leg lengths off the king's own travel, get `253`. That code feeds a padlock elsewhere in the bag, same as any other lock (PP-035). Buying a board is now unconstrained by any compartment requirement.

Board size is now **11 × 11**, a commoner size than the earlier 7 × 7 (Brandubh) plan — likely easier to buy off the shelf. A stock 11 × 11 set's exact piece count (kings/defenders/attackers included) still needs checking against this layout's 1 king, 6 defenders and 16 attackers before a specific listing is chosen.

![Seven by seven hnefatafl board showing the throne square and four gold corner squares](Art/Diagrams/Diagram_Hnefatafl_Board.svg) 7 × 7 board, gold corners, king on the throne. **The dark blocking pieces are deliberately not shown** — their placement is what makes the three-move escape unique, and it has to be found by search rather than drawn by hand. The playable layout is in the [Prototype tab].

Needs work The board layout must be solved, not eyeballed, and it is now downstream of one decision. A layout with a *provably unique* three-move solution has to be verified by search *for whichever board size is bought* (PP-035), and the map/ticket split has to be checked against it — the hidden strip must leave the visible board unresolvable rather than merely incomplete.

## Design notes (PP-035: 3D printed, 29 Sept 2026)

**Hnefatafl board: which one to buy.**

**The throne compartment is dropped** — no cavity, no cavity-key king piece. The board is a straightforward bought prop: solve the escape, the leg lengths feed a padlock elsewhere. **Target size changed to 11 × 11** (PZ-008), a commoner size than the earlier 7 × 7 (Brandubh) plan — likely an easier size to buy off the shelf, though piece-count fit (king + attackers + defenders against whatever a stock set includes) still needs checking once the user's final layout in [the board designer](../Props/Hnefatafl/board_designer.html) settles how many of each piece it actually uses. ~~Current listings have not been checked.~~ **Resolved, 29 Sept 2026:** not bought — the user 3D-printed the board instead.

## Starting state

Not recorded yet.

## Reset

Take every piece off the board and pack the pieces with the board.

## Replacement

Not recorded yet.
