# Escape Backpack — Shared Agent Guide

This file is the shared source of truth for Codex, Claude Code, and other coding agents working in this repository.

## Start Here

1. Read `README.md` for the project overview.
2. Read `HANDOFF.md` for the current task, recent work, and next step.
3. Check `git status` and the recent commit history before editing.
4. Inspect the relevant subproject files; do not assume generated outputs are the source files.

## Project Map

- `index.html` — local landing page linking the projects and design guides.
- `Hiking_Trip/` — completed hiking escape-game materials.
- `Lego/` — Lego backpack materials.
- `NorseBackpack/` — Norse-themed concept and brainstorming materials.
- `Space Station Aurora/` — active space-station escape-game materials.
- `Space Station Aurora/Station_Map.html` — interactive map built from the detailed AutoCAD station plan.
- `Space Station Aurora/StationBluePrint/` — original DWG/DXF/PDF blueprint sources, the layer-preserving SVG converter, and the rendered map base.
- `Fonts/` — local font assets used by project documents.

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

- HTML: open locally and verify links, layout, and obvious console errors.
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
