---
id: AS-064
title: Box cover A - the mysterious parcel
type: asset
status: candidate
kind: image
for: PP-045
tool: Built-in ImageGen
file: Art/Box/Raven_Inheritance_Box_Cover_A_v1.png
links: [PR-007, PR-002, Q-029, Q-047, Q-052]
superseded_by:
tags: [packaging, kickstarter, concept]
---

## Direction and approval

11 October 2026: the designer selected direction A, "The mysterious parcel": postcards, folded map and rune-marked envelope on a warmly lit wooden table, with the existing raven emblem above the title. Direction B, a large raven on a simple green field, was not selected for this first concept.

The direction is approved for exploration. This generated cover and the copy below remain drafts awaiting review. Working box size: 11.5 × 11.5 × 2 in (PR-007). This is flat square lid artwork only, with no dieline, bleed or side panels.

![First parcel cover concept](Art/Box/Raven_Inheritance_Box_Cover_A_v1.png)

## Front copy — draft used in this concept

**THE RAVEN INHERITANCE**

*Follow the postcards. Uncover your family’s secret.*

A cooperative puzzle adventure

## Back copy — draft for discussion

**Your great-aunt has sent you a box. Naturally, she’s made it a puzzle.**

Aunt Liv has been following your family’s Nordic roots. Inside her parcel are postcards, maps, curious souvenirs—and envelopes marked with runes.

Piece together her clues, discover connections between distant places, and open the next chapter of her journey. Everything she packed might matter. Even something you thought you’d finished with.

**Look closely. Compare your discoveries. Follow where they lead.**

A hands-on mystery inspired by Norse history. No prior historical knowledge needed.

Suggested back layout: this copy beside a photograph of the actual prototype components. No back-panel artwork or component photograph created in this step. Player count, age and duration remain unverified and omitted.

## Scope and checks

- Built-in ImageGen transformed the existing scene and reinterpreted the raven reference; the emblem is not an exact pasted reproduction.
- Full-size visual inspection: square composition; title, tagline and descriptor read correctly; no backpack; envelope, map and postcards visible.
- Map, postcards and envelope marks are illustrative, not actual puzzle assets or envelope labels. No real codes or final route-digit shapes were intentionally supplied.
- The generated compass and wax-style seal are scene dressing, not confirmed box contents. Review before final packaging to avoid implying included components.
- Typography is baked into the raster. Production needs separately typeset text, supplier dieline, bleed and print-resolution/colour proof. None has been done.
- Existing backpack-scene and raven masters are preserved.

## Inputs

1. Scene to transform: `Art/Brand/Norse_Backpack_Scene_v1.png`.
2. Established emblem: `Art/Raven/Raven_Profile_Knotwork_Frame_v1.png`.

## Exact generation prompt

Built-in ImageGen; `transparent_background: false`; both local image paths supplied as references.

```text
Use case: compositing.
Asset type: square illustrated board-game box lid concept, flat full-bleed artwork, for The Raven Inheritance.
Edit targets/supporting inputs: Image 1 is the existing Norse Backpack scene: transform it into the approved mysterious-parcel cover composition. Image 2 is the existing profile raven in a circular Norse knotwork frame: faithfully incorporate this established emblem above the title, preserving its recognizable profile bird, frame and engraved style.
Primary request: Replace the backpack-centered composition with an inviting tabletop mystery made of postcards, a folded map and one large closed kraft envelope bearing four small decorative Norse rune marks. The artwork itself is a square box lid, not a picture of a box. Keep the polished illustrated finish, warm lamplight, rich wood, deep green shadows and cream/copper identity of the reference.
Composition: Square canvas. A calm deep pine-green upper field takes about the upper 45 percent, seamlessly blending into the atmospheric scene below. A modest raven emblem centered near the top; the title is large and dominant below it on two lines. In the lower half, a slightly overhead view of a wooden table with a beautiful open map, a small overlapping fan of vintage landscape postcards (Nordic coast, Icelandic hills, old Norman town), the prominent closed rune-marked paper envelope and twine loosely curling beside it. The rightmost edge may catch the warm glow of a partially cropped lantern. Printed objects are richly illustrated but do not contain readable puzzle answers, traceable digit routes, grids or actual game codes. The envelope is a paper envelope, not a chest. Background setting is subdued; no backpack. Make the envelope and postcards the principal scene objects. Keep props visually organized with believable scale and perspective.
Palette: deep pine green #193B35 / #254C40, warm cream #F3EFE5, restrained copper/amber #B56A2A, warm oak brown. No foil, embossing or expensive finish implied; this is printed art.
Typography: elegant very legible classic Cinzel-like uppercase serif, warm cream. Generous margins so all text is well inside the lid edges. Title visible at thumbnail size. Integrated professional editorial layout, not multiple badges.
Text, exactly:
Top title, on two lines: "THE RAVEN" / "INHERITANCE"
Under title, small but clearly readable: "Follow the postcards. Uncover your family’s secret."
Along the bottom in a clean unobstructed dark-green band: "A COOPERATIVE PUZZLE ADVENTURE"
No other readable text. No player count, ages, duration, publisher logo, Kickstarter logo, fake award, ratings, barcode or watermark.
Mood: warm, intelligent and curious, a family travel mystery with Nordic history. No horror, glowing magic, weapons, helmets, ominous figure or distressed unreadable type. Retain plenty of clear space around the title. Deliver one finished square flat cover concept, high-resolution, opaque background.
```
