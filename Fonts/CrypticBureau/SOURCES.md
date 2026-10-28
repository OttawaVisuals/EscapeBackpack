# Bureau typefaces

Downloaded from the Google Fonts repository for the Bureau one-pager on 2026-10-13:

- Cormorant Garamond: https://github.com/google/fonts/tree/main/ofl/cormorantgaramond
- Source Sans 3: https://github.com/google/fonts/tree/main/ofl/sourcesans3

Original variable fonts and their OFL license files are retained here. The build script creates static weight instances with fontTools: Cormorant 600; Source Sans 400 and 600. These are embedded by ReportLab in the PDF. Rebuild with `Brand/CrypticBureau/build_onepager.py` (requires reportlab and fonttools).
