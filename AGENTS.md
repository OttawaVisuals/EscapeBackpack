# Escape Backpack — Shared Agent Guide

This file is the shared source of truth for Codex, Claude Code, and other coding agents working in this repository.

## Start Here

1. Read `README.md` for the project overview.
2. Read `HANDOFF.md` for the current task, recent work, and next step.
3. Check `git status` and the recent commit history before editing.
4. Inspect the relevant subproject files; do not assume generated outputs are the source files.

## How These Sessions Work

Read this before assuming what a prompt is asking for.

- **Chats are brainstorming, not ticket queues.** The default mode is "here is what we are thinking about — offer ideas, show options, ask clarifying questions," not "a prompt arrived, produce a complete deliverable." Propose, discuss, then write.
- **Propose before editing.** Discuss creative and design decisions with the user in chat before writing them into project files, even when `HANDOFF.md` names something as the next step. The exception is mechanical follow-through on a decision that is already approved (re-rendering at a new size, regenerating a PDF, fixing a typo) — that does not need re-proposing.
- **One piece per session.** A session normally works on a single part of a game. Whole-game reviews happen only when the user's prompt says so. Do not expand scope into other parts because they look unfinished.
- **Unfinished is the normal state.** Open questions are expected and preferred over forcing every decision at once. Leaving something explicitly open, with a reason, is a valid outcome. Adding a new open question is as legitimate a result as closing one.
- **Say when you do not know.** Never invent puzzle rules, answers, dates, measurements or status to fill a gap. Record the gap instead.

## Where Design State Lives

- **Each project's main HTML page is the source of truth for design state** — what is decided, what is open, what the options are. For Norse that is `NorseBackpack/Norse_Brainstorm.html`. Update it as the work happens, in the same session, rather than leaving decisions only in chat.
- **`HANDOFF.md` carries session continuity only**: what this session did, which files changed, what was checked, one next action. It must not hold a backlog of open design questions — that backlog belongs in the project page, and keeping it in two places is how the two drift apart.
- **Every open question gets a stable ID** so chat, the handoff and the page all refer to the same thing. Norse uses `ST-` structure, `PC-` postcards, `PZ-` puzzles, `PR-` props, `HI-` history, listed in the Open questions tab.
- When a decision is taken, move the pill in the page. When something is superseded, say so where the old text was rather than deleting it silently.

## Agent Roles

Not a hard rule, but this is the split that works and it saves rediscovering it each time.

- **Codex** — image and asset generation, and visual layout passes on the artwork itself (stamp illustrations, postcard layouts).
- **Claude Code** — design reasoning, the project HTML and its JavaScript, Python build scripts, cross-file consistency checks, verification, and the handoff.
- Whoever generates an asset records the exact prompt used, in the project page, so the asset can be revised later instead of re-invented.

## Project Map

- `index.html` — local landing page linking the projects and design guides.
- `Hiking_Trip/` — completed hiking escape-game materials.
- `Lego/` — Lego backpack materials.
- `NorseBackpack/` — Norse-themed concept and brainstorming materials.
- `NorseBackpack/Norse_Brainstorm.html` — the single source of truth for the Norse game: story, postcard system, puzzles, open questions, options, props, design spec and design guide, as tabs in one page.
- `Space Station Aurora/` — active space-station escape-game materials.
- `Space Station Aurora/Station_Map.html` — interactive map built from the detailed AutoCAD station plan.
- `Space Station Aurora/StationBluePrint/` — original DWG/DXF/PDF blueprint sources, the layer-preserving SVG converter, and the rendered map base.
- `Fonts/` — local font assets used by project documents.

For the Aurora map, `SpaceStationAurora.dxf` is authoritative. The generated website artwork omits the `Z.Box` construction grid and uses blue for compartments, amber for external systems, and neutral grey for structural connections.

### Norse Backpack — current design invariants

These constrain any Norse work and are easy to get wrong from an older reading of the files.

- **The postcards are the main mechanic.** Eighteen cards, one per route stop. Everything else in the bag is an instrument that acts on them — the comb reads a message, the balance orders three cards, the board's task is set by a card. Design outwards from the deck, not towards it.
- **All eighteen cards are active.** Every card does a job besides the final ordering. The earlier "five or six active cards, the rest quiet" model is superseded, along with the sparse-channel worksheet, the anomaly stamps and the tilted stamps.
- **The number and names of the containers are not decided and will change.** The old six-container list (main compartment, archive case, RAVEN, CROWN, WELL pouches, travel wallet) and its fixed codes have been removed. Do not reintroduce container names or intermediate lock codes. Containers get decided once the postcard puzzles exist, so they can be shaped around the puzzles.
- **The postcard system itself is a work in progress.** The Postcard system tab is the current thinking, not a finished spec. Parts of it are explicitly marked open.
- Two anchors are settled: the opening four-digit code (two luggage tags, postcard 01 names the place on the tag that reads first) and the final puzzle (four maps plus all eighteen cards, drawing each trail's legs in order to give the four digits).

Many deliverables are binary files (`.docx`, `.pptx`, `.pdf`, and images). Preserve their formatting and verify rendered output after changing them.

## Working Rules

- Make the smallest change that fully addresses the task.
- Preserve unrelated user changes. Never discard or overwrite them to obtain a clean working tree.
- Treat editable source files as authoritative. Generated PDFs and images are outputs unless a task explicitly says otherwise.
- Keep paths and filenames stable when they are already linked from HTML or other documents.
- Do not invent puzzle rules, answers, measurements, dates, or project status. Record unknowns clearly.
- Use concise, plain language in project documentation.
- For visual work, follow the relevant existing design guide and compare a rendered result with the source.
- Keep each project's brainstorming and design content in that project's single main HTML file (for example `NorseBackpack/Norse_Brainstorm.html`), added as a new tab/section in the existing single-page structure. Do not split design notes into a second standalone HTML file unless the user asks for a separate document.
- Do not commit, push, or publish unless the user asks.

## HTML PDF Links

All PDF links in existing and new HTML pages must prefer the browser's PDF viewer in a new tab:

```html
<a href="path/to/file.pdf" target="_blank" rel="noopener">Open PDF</a>
```

- Do not use the `download` attribute for PDF links.
- Use link text such as “Open PDF” or “View PDF,” not “Download PDF.”
- Apply the same attributes to embedded `data:application/pdf` links and PDF links created by scripts.
- Preserve intentional downloads for non-PDF source files and editor exports.
- Browser or device settings may still force a PDF download; the page cannot override that preference.

## Validation

Use checks appropriate to the files changed:

- HTML: open the local file in the in-app browser and check it visually, not only as text. The page renders, its JavaScript runs, and deep links work (`Norse_Brainstorm.html#view-puzzles`), so a script-generated tab can be inspected directly. Earlier handoffs claimed a `file://` limitation made this impossible; that was wrong. Verify links, layout and console errors.
- Documents/slides/PDFs: render and visually inspect every affected page or slide.
- Spreadsheets: recalculate, check formulas, and inspect affected sheets.
- Images: inspect at full size and confirm transparency/cropping where relevant.
- Cross-file changes: search for references to renamed or moved files.

If a check cannot be run, state that limitation in `HANDOFF.md` and in the final response.

## Handover Protocol

Before ending a work session or switching agents, update `HANDOFF.md`:

- Record the exact task and current status.
- List files changed and key decisions.
- Record checks run and their results.
- Give one concrete next action.
- Note blockers or unanswered questions.
- Keep only the latest useful session details; durable rules belong here, not in the handoff.

When taking over, verify the handoff against `git status` and the actual files. The repository state wins if the handoff is stale.
