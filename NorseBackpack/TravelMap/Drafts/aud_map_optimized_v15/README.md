# Approved Aud v15 - smaller delivery files

The designer selected v15 as the winning map style. Full-resolution master retained at `../render_full_map_v15/Aud_Full_Map_v15.pdf` (33,918,855 bytes).

| File | Bytes | Use |
|---|---:|---|
| Aud_Map_v15_Print_300dpi.pdf | 908,594 | Print / downloadable PDF |
| Aud_Map_v15_Web_200dpi.pdf | 762,687 | Web PDF download |
| Aud_Map_v15_Game_2400.webp | 616,636 | Online game display; 2400 x 3106 px |

PDF method: inspect each image's largest placement, resize once at 300dpi (print) or 200dpi (web), rebuild image and alpha together as a losslessly compressed PNG, remove unused objects and compress PDF streams. Text, fonts, page dimensions and all 751 vector paths are preserved. The PDFs remain zoomable/selectable; embedded artwork has finite resolution. WebP is rendered from the original master at 2400px width, quality 90.

Visual QA: full page and enlarged small-symbol samples inspected. The first trial using rewrite_images mishandled shared images/masks and was discarded; all final files use explicit alpha-preserving replacement. Source SHA256 and output sizes in compression_report.json. Physical print test outstanding.

Rebuild from repository root: `python NorseBackpack/TravelMap/Drafts/optimize_aud_map_v15.py`. The online game has not been rewired or published.
