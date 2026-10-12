---
id: Q-054
title: Playtest 1: the final puzzle asks too much rereading of the postcards
type: question
# open | answered | parked
status: answered
# Records this question is about, e.g. [PZ-003]
about: [PZ-013, PP-040, PP-041, PP-039]
# Leave empty while open
answer: Marks give the order and decoys carry no mark (designer, 12 Oct 2026). Built with iconography-crop marks and stamps on the maps; see PZ-013.
# Any related record IDs, e.g. [PZ-002, Q-004]
links: []
# Set to an ID when this record is replaced. It then moves to the Parked tab.
superseded_by:
tags: []
---

**Playtest 1 feedback (relayed 12 Oct 2026):** going back to the postcards for travel clues (to filter the decoys and to reconstruct the visit order) was too complicated. Ideas the playtesters raised:

1. Don't use the postcards for final clues, apart from the family mark.
2. Make the marks on the postcards look more like the drawings on the iconography page (PP-041). Today they are separate hand-drawn icons in a different style.
3. Add more travel tickets, or a more detailed travel journal (PP-039, PP-040).
4. Make the decoys clearer, e.g. a line like "can you trace back my steps for everything related to our family". Decoys could also be postcards with no mark at all.
5. Put the stamp logos on the maps, to make sorting cards by trail easier.

**Claude's proposal (12 Oct 2026, not decided):** let the icons carry the whole finale. The stamp gives the trail and the mark gives the position, so nobody rereads card text:
- Within each trail every mark is already unique (`Postcards/postcard_marks.py`: the symbol set for the 3-stop trails, the crest set for the 6-stop ones). Reassign the marks so the iconography page's own order (the captions: raven, longship, sun-wheel; axe, shield, wolf, anchor, horn, valknut) *is* the visit order. Liv's page then says so, e.g. "I drew them in the order I met them."
- Make the card marks small copies of the iconography drawings (idea 2).
- Decoys carry no mark (idea 4b), and the journal line names the rule (idea 4).
- Print each trail's stamp on its map (idea 5).
- This retires the order-reconstruction clue set (ticket dates, card statements, `Tools/final_riddle_solver.py`). The code stays 1972, because the shapes and the trail order do not change. Cost: the finale gets easier (difficulty 3 → about 2).

Alternative kept open: idea 3 (more tickets or a detailed journal giving the order directly). That adds props and reading, which is what the feedback was about.

**Decided 12 Oct 2026 (designer):** go with the marks for the order; decoys carry no mark. Built the same day, together with the two other parts of the proposal (iconography-crop marks, stamps on the maps). See PZ-013. The third question, whether the tickets and Travel highlights stay, is Q-055.
