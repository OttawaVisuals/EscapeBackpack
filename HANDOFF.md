# Project Handoff

Last updated: 2026-09-10 by Claude Code

## Current Task and Status

Norse postcard stamp design, continued across this session in two parts:

1. Decided the four trail stamp motifs and colours, and wrote a ready-to-use illustration brief per trail for Codex (which will actually produce the stamp artwork — not done here).
2. Started deciding the two remaining anomaly-card wrong-trail motifs (Châlus, Hvammur), but **parked that** at the user's request: it surfaced a real tension in the corpus design (see Open Design Issues) that needs a separate decision first.

Also folded in: this session's sparse-set assignment (previous handoff) is committed and pushed. A process note from the user, now in memory: for creative/design decisions with real degrees of freedom, propose in chat and get input before writing to the file — don't just execute because a step is named "next" in this doc. Both pieces of work in this session followed that (motifs/colours/briefs were proposed and confirmed before being written in).

## Files Changed

- `NorseBackpack/Norse_Brainstorm.html` — in the Design spec tab, inside "The postcard system":
  - New "The four stamp series" table: motif + trail colour (reusing the existing route-map colours) + rationale for each of the four trails.
  - New "Wrong-trail variants for the anomaly cards" table: Kyiv decided (shows Leif's longship); Châlus and Hvammur marked **Parked**, with a note explaining why (depends on the card-density question below) and that it doesn't block stamp artwork.
  - New "Illustration brief for Codex" card: one shared style spec (engraved single-colour line art, cross-hatched shading, cream paper, plain perforated border, no text/denomination yet) plus one ready-to-paste Codex prompt per trail.
  - "Next steps, in order" step 2 updated to "Ready for Codex".
  - (From earlier in this session, already committed as `24e9a7f`): the full sparse-set assignment worksheet and the new Design guide tab (colour/typography/tone/components/icons reference).
- `HANDOFF.md` — this handover.

No other file was touched this session. The uncommitted Aurora changes (`Station_Aurora_Map_Base.png`, `Station_Aurora_Vector.svg`, `convert_dxf_to_svg.py`, `Station_Map.html`, and the Aurora paragraph in `AGENTS.md`) remain exactly as found — still a separate, in-progress thread the user chose not to continue this session.

## Decisions

**Stamp series (motif + colour), all decided:**

| Trail | Colour | Motif |
|---|---|---|
| Leif Erikson | `#216580` | Longship |
| Rollo & descendants | `#a2562d` | The Bayeux comet (Halley's Comet as shown in the tapestry) |
| Aud the Deep-Minded | `#6d528b` | High-seat pillars (öndvegissúlur) |
| Harald Hardrada | `#467444` | A labrys (double-headed axe) — deliberately not his historical raven banner, to avoid competing with the game's own raven/HRAFN emblem |

Illustration style, all four: engraved-line, single ink colour (the trail colour) on cream paper, fine cross-hatched shading, plain perforated border, no text/denomination/date yet. Full Codex prompt text is in the file.

**Anomaly wrong-trail motifs:** Kyiv only (shows Leif's ship, per the design doc's own worked example). Châlus and Hvammur intentionally left undecided — parked, not forgotten.

## Checks

- Opened `Norse_Brainstorm.html` in the browser after each edit; confirmed via `document.body.textContent` / `querySelectorAll` that the new tables and the Codex-brief card render with the expected content, and that the Design spec tab still shows correctly.
- Confirmed (from the sparse-set-assignment work earlier this session) that new CSS stayed scoped and didn't leak into other tabs; no new CSS was added in this stamp-brief pass, only table/card content, so no re-check needed.
- No image has been generated yet — the brief is untested against an actual Codex output. First real check is generating one motif and confirming legibility at true stamp size (~20×24 mm), as noted in the file itself.

## Next Action

Two independent next steps, neither blocking the other:

1. **Take the four Codex prompts (Design spec tab → "Illustration brief for Codex") into Codex**, generate one motif per trail, and sanity-check legibility at true stamp size before producing all 18 cards' stamps from them.
2. **Resolve the card-density question** this session surfaced: the sparse-channel assignment currently loads 15 of 18 cards with at least one marker, which conflicts with the original "five or six active cards" decision and dilutes the anomaly stamp's job as a "look here" signal (see Open Design Issues). Deciding this unblocks the Châlus/Hvammur anomaly motifs and probably also affects whether the current price/text/tilt card assignment (from the previous session) should be revisited.

After either of those: re-render the three existing postcard fronts at true size, write the aunt's letters, solve the hnefatafl board — the rest of the "Next steps, in order" list in the Design spec tab is unchanged.

## Open Design Issues

- **Card density vs. the anomaly signal (new this session, unresolved).** 15 of 18 cards carry a sparse marker under the current assignment, which conflicts with the "five or six active" decision and weakens the anomaly stamp's job (it's meant to flag which few cards matter, but almost all of them already do). Needs a decision: scale back the sparse assignment, or accept the anomaly stamps as "look here first" rather than "the only ones that matter."
- Anomaly wrong-trail motifs for Châlus and Hvammur — parked, depends on the above.
- The tilted-stamp postcard set and the hnefatafl escape both feed a directional lock; needs a second lock or a reassignment.
- HRAFN is assigned to the five-letter lock but also fits a five-ring cryptex; only one of the two can have it.
- The actual digits, letters and directions the price/text/tilt cards carry are unassigned, pending the two lock conflicts above.
- The 18-card postcard set needs its artwork re-rendered, not rescaled (1536×1024 current vs. 1500×1050 target at true print size). `SIZE`/`PAGE` in `Postcards/build_postcard_collection.py` must change together.
- The hnefatafl board layout (a provably unique four-move escape) has not been generated.
- The final map mechanic (pins/cord vs. overlay) is undecided by choice; needs prototyping at print size.
- The red filter needs a home-printer colour test.
- The wording of the three redirect clues is unwritten.
- Every historical claim in the Design spec tab needs source-checking before it reaches a prop.
- Carried over from earlier sessions: postcards 02 and 03 still need their message and travel date; the main compartment's opening mechanism and answer are still undecided.

## Aurora note (not this session's work, left as found)

Uncommitted changes recolor `Space Station Aurora/Station_Map.html` (plus its SVG/PNG/converter script) to a blue-compartments/amber-external/grey-structural scheme, matching a paragraph already added to `AGENTS.md`. That was in progress before this session and remains untouched and unverified — still sitting unstaged in `git status`.
