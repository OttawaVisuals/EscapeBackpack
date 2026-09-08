# QR patch placement: proposed player experience

## Recommended first test: maintenance diagram
Included in `output/pdf/Aurora_V2_Paper_Prototype.pdf` (relative to the Space Station Aurora folder).

**Briefing -> find panel, six patches and diagram -> match shapes -> transfer patches -> scan -> HAROLD.**

The diagram has the same 25 x 25 grid and corner markers as the QR. Its six outlines show exact positions and orientations without revealing the final black/white pattern. The player matches the loose shapes, then transfers them using the row/column guides. All diagrams and cutouts use the uploaded V2 geometry, with 3 mm cells.

This is an introductory assembly task. It teaches players to combine physical evidence and repair equipment. It does not require knowing how QR codes work. Keep the diagram in the same open pocket for the first test; hiding it adds searching, not placement logic.

Suggested hints, only if needed:
1. "The three large corner marks identify which way up the diagram goes."
2. "Find an outline that fits one of your pieces. Keep the printed side facing you."
3. "The row and column numbers are the same on both sheets. Move that piece to the same squares."

## Option 2: torn maintenance diagram
Cut the diagram into three large sections and distribute them between the briefing and open pockets. Players reconstruct the diagram using its outer grid, corner markers and continuous patch outlines, then perform the same repair.

This adds a discovery step without extra arithmetic. Test the simple version first. Do not lock any diagram section behind access to HAROLD: repairing this interface is the prerequisite for reaching HAROLD.

## Option 3: station-map routing clue
Use a separate communications inset on the station map, clearly marked as the same 25 x 25 interface grid. Give each patch a subsystem symbol on its reverse and a matching shape silhouette on a maintenance card. A six-entry fault log links those subsystems to the correct footprints on the inset. Players cross-reference the log and map, orient the pieces using the silhouettes, and repair the panel.

This could connect the opener to later station exploration, but needs the final station map and subsystem names before it can be made into a fair, complete clue. Do not assume ordinary room positions translate to QR coordinates. Explicitly show the interface inset and orientation reference. Avoid labeling black/white QR squares or the quiet zone.

## Briefing revision
`Briefing_Refined_Draft.txt` preserves the original premise and names, corrects wording, and gives a concrete first action. The original `1.Briefing.txt` is untouched. Communication failure appears after the essential instructions, so the print failure does not remove information needed to solve the opener.

The explicit instruction paragraph is for the first playtest. If players find it too guided, shorten it to: "The optical interface is damaged. The six repair patches and the maintenance diagram are in the backpack's open pocket. Restore the interface, then scan to reconnect."

## Paper test and accepted limitations
- Print the PDF single-sided at Actual size / 100%; check both 50 mm rulers. Give players pages 1, 2 and 4 plus the cut patches from page 3. Keep page 5.
- Cut every irregular contour accurately, including the recess in F. White cells must cover the base as fully as black cells. Some strips are only 3 mm wide; opaque paper and removable adhesive underneath are preferable to loose curled pieces.
- Record whether errors come from interpreting the clue, transferring positions, cutting, or phone scanning. These call for different fixes.
- V2 contains six patches, covers all 58 changed cells, and uses 133 cells total. Some five-patch combinations can already decode the destination; accepted for this cooperative prototype. This does not prove behavior across phone cameras.
- Neither domain ownership nor the deployment of `/coms` and `/Harold` was verified for this print task. A phone revealing the correct URL is sufficient to test assembly. Before a game, provide an in-world damaged-comms response at `/coms` and the actual HAROLD interface at `/Harold`.

## Rebuild
Run `python build-print-pack.py` from this directory with ReportLab installed. It reads `aurora-qr-layoutV2.json`, writes the five-page PDF and the editable briefing draft. The source V2 JSON is unchanged.
