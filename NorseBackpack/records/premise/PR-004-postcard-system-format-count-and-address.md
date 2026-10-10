---
id: PR-004
title: Postcard system: format, count and address
type: premise
# idea | candidate | decided | built | parked
status: decided
# sender | player goal | story | tone | ending | other
aspect: other
# Any related record IDs, e.g. [PZ-002, Q-004]
links: []
# Set to an ID when this record is replaced. It then moves to the Parked tab.
superseded_by:
tags: []
---

Moved from the Design spec, 17 Sept 2026

### Format, count and address

One card per route stop, giving 18 cards across the four trails. At this volume the cards stop being individual clues and become a corpus, which is a better toy: it supports grouping, sorting and a much larger final reveal.

**Partly superseded.** The sparse-channel model below — a quiet majority of cards with data on a few — has been replaced by the all-active model in the [Postcard system tab], which is the current spec. What stays true here is the count, size, format, address, stamp-series idea and the mechanics list. The anomaly and tilted-stamp channels are dropped.

| Decision | Value |
|---|---|
| Count | 18 real stops in `TravelMap/Norse_Aunt_Route_Plan.json` (Leif 3, family 6, Aud 3, Harald 6), plus 4 candidate decoys — see [Final riddle tab] |
| Size | Approx. 5 × 3.5 in (vintage postcard proportion) |
| Universal design elements | Series motif (trail identity), postmark (place), a titled Fun Fact block, her handwriting, and — candidate — a small element mark (crest/logo membership) placed away from the stamp and postmark, not UV |
| Ordering key | Candidate change Reconstructed from ticket dates, postcard statements and the final bundle, not the postmark — see [Final riddle tab] |
| Active clue cards | All 22 (candidate) — superseded, see the [Postcard system tab] |
| Format | Purchased but never sent — addressed and stamped like a real postcard, just not mailed |
| Recipient address | John Ericson, 24 Longship Way, Ottawa ON K1L 1S1, Canada — same on all 18 cards |

#### Format: purchased, never sent

Each card is addressed and stamped like a real postcard rather than a plain note, which is what makes an unmailed stamp collection plausible in the first place: travellers buy postcards and never send half of them. It also earns back an address block as usable clue space, which a note-card format would give up for nothing.

The recipient is fictional: **John Ericson, 24 Longship Way, Ottawa ON K1L 1S1, Canada.** "Longship Way" doesn't exist as an Ottawa street, so the address can't collide with a real occupied building regardless of the postal code. Ericson doubles as a quiet nod to Leif without being tied to his trail specifically — it reads as the family surname.

The same stamp series is reused across countries within a trail; explained, if it ever needs explaining, as the aunt buying a batch of stamps at the first post office of each leg. This is ordinary traveller behaviour and doesn't need to be stated in-fiction.

**First-card layout, built:** the writing side is split vertically, with Aunt Liv's existing message on the left and, on the right, the Leif longship stamp and postmark, a shrunk boxed address, and a boxed, titled Fun Fact block underneath it — matching the current spec in the [Postcard system tab]. The stamp sits at roughly 20 × 24 mm. **Superseded, 16 Sept 2026:** the circular mark's date half (**07 JUL**, with an underlined day left over from the superseded 0734 mechanism) is dropped entirely — postmarks carry the place only now (Q-006/old page PC-03/old page PC-04). Card L1's back still needs rebuilding to drop the date; the mark itself also still needs redrawing as a real cancel rather than a clean graphic (Q-013).

**Parked idea.** One postcard could carry a *different* recipient address as a "look here" signal. Still parked, and now the only surviving piece of the dropped anomaly idea — with every card active there is nothing left for such a signal to select, so it would need a new job before it is worth using.

#### Superseded: the sparse-channel model

This section used to specify a quiet majority of cards with data carried on small subsets — four price cards, five extra-text cards, four tilted stamps and three anomaly stamps — together with the card-by-card worksheet that assigned them.

It has been replaced by the all-active model: every one of the 18 cards does a job besides the final ordering, the data lives in a titled Fun Fact block rather than in a sparse channel, and the anomaly and tilted-stamp channels are dropped. The reasoning and the new assignment are in the [Postcard system tab].

Kept as a note rather than deleted silently, because the argument it made — that scarcity is itself a signal — is sound and may be worth reviving if the deck ever grows past 18 cards.

#### Other postcard mechanics worth using

- **Grille overlay.** A card with windows cut in it laid over a message, exposing only certain words. One grille rotated or flipped decodes several cards. See the comb prop below.
- **Hole-punch stack.** Punched holes plus a registration notch; stacked in the right order against a window, only certain letters on the bottom card stay visible. The order is the puzzle, and it rehearses the skill the final map needs.
- **Edge continuation.** Horizon lines that continue between cards, with something written across the seams and legible only when the joint is closed.
- **Fold lines.** A crease brings two halves of a message together to form a sentence present in neither half.
- **Counting in the illustration.** Boats, birds, windows. Trivial on its own — only ship it with a non-obvious ordering rule attached.

**Artwork consequence of the size change.** Done for cards L1–L3: the illustration sources and generated fronts are 1500 × 1050 px (10:7), reframed without aspect distortion. The remaining production change is in `build_postcard_collection.py`, where `SIZE` and `PAGE` must change together before cards L2/L3 and the full collection PDF are rebuilt.
