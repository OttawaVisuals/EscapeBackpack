# Codex brief: smudged ticket strip for the 2134 layout (17 Oct 2026)

Attach two images:
1. **Edit target:** `Props/Hnefatafl/Hnefatafl_Ticket_Back_Clean_2134.png` (887 x 1774 px). The correct strip, drawn cleanly. Rendered from the ticket builder, so the squares are exact.
2. **Style reference:** `Props/Hnefatafl/Hnefatafl_Ticket_Back_Smudged_v2.png` (887 x 1774 px). The smudge look we already like. Its pieces are from the OLD layout and must not be copied.

Save the result as `Props/Hnefatafl/Hnefatafl_Ticket_Back_Smudged_2134_v1.png`.

## Prompt

Use case: style-transfer edit.
Edit target: image 1, a clean hand-drawn mirrored board strip (3 columns by 11 rows) for a Viking museum ticket back: thin wobbly pen grid, five dark hatched squares, two rust-orange diamonds in the corners, mirrored letters K J I above the grid, thin tan border around the card.
Style reference: image 2, the same kind of strip as if the ticket had been wet when it was pressed against another sheet: the ink has bled and smeared sideways in soft horizontal streaks, blooms at the grid crossings, a few faint stray specks, and the rust diamonds smear a little toward the right.
Task: apply the wet-ink smudge look of image 2 to the clean strip in image 1. Keep the strip layout, the paper colour and the thin border exactly as in image 1.
Do not move, add, remove or redraw any piece. The five dark hatched squares must stay exactly where they are in image 1: in the left column (K) second row from the top and eighth row from the top; in the right column (I) third, fourth and sixth rows from the top. The two rust diamonds stay in the left column, first row and last row. Nothing else.
Each dark square must stay clearly readable as a square with hatching, and every grid line must stay continuous enough to count the rows and columns, so the smudge is strong at the edges and around the squares but never covers a whole square or erases a grid line.
Same size as image 1 (887 x 1774 px), same orientation, mirrored letters kept as they are.
No new text, no runes, no extra marks, no shadows, no frame changes, no watermark.

## Check list for Claude when it comes back

- Five dark squares at K10, K4, I9, I8, I6 (left column K, right column I; row 11 at the top).
- Corner diamonds at K11 and K1; no piece at K8.
- Size 887 x 1774, readable at ticket size (2.6 x 5.2 in).
- Then replace the vector strip on the ticket back with this image (or keep the vector strip as the fallback).
