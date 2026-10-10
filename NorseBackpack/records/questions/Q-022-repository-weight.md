---
id: Q-022
title: Repository weight.
type: question
# open | answered | parked
status: answered
# Records this question is about, e.g. [PZ-003]
about: []
# Leave empty while open
answer: Decided, 29 Sept 2026
# Any related record IDs, e.g. [PZ-002, Q-004]
links: []
# Set to an ID when this record is replaced. It then moves to the Parked tab.
superseded_by:
tags: [old-PR-07]
---

Status on the old page: **Decided, 29 Sept 2026**

Stamps are 1145 × 1374 px and 2.2–3.4 MB each, roughly 1450 dpi for a 24 mm print. The postcard PDFs in `output/pdf/` are 9.3 MB each and tracked. Decide what is committed before eighteen cards exist. **Decided, 29 Sept 2026 (user):** for Norse, commit only what the website uses; build scripts and other text sources stay committed. The site now shows 1200 px WebP copies of the postcard images (`Web/Postcards/`) and 150 dpi copies of the print PDFs (`Web/pdf/`), which cut the Norse part of the site from about 398 MB to about 101 MB. The full-size postcard art and the print PDFs in `output/pdf/` stay on the build computer only, as the print masters — print from those, not from the page links. After rebuilding any postcard image or print PDF, run `python NorseBackpack/Tools/build_web_assets.py`: it refreshes the web copies, repoints new links and rewrites the Norse block of `.gitignore`. Old files stay in git history; shrinking `.git` (6.4 GB) would need a history rewrite and is not planned.
