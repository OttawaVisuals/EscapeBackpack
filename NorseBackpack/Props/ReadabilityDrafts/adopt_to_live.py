"""Adopt the approved readability drafts into the live print files (17 Oct 2026, designer).

Adopted: Brattahlid museum ticket, Aud museum ticket, Rouen ticket (redesign), LD (draft was identical to
live, nothing to change) and the cypher wheel's wide arm (built by Props/CypherWheel/build_cypher_wheel_pdf.py).
Liv's notes card adopted later the same day (title 14 pt, labels 8 pt, text 10 pt). Run build_readability_drafts.py and
Props/RouenTicket/build_rouen_ticket_redesign.py first; this script then copies their pages to the
live names. The old files are kept in ../Norse_Snapshots/Norse_2026-10-17_PreReadability/ (outside the repo).

The old builders (Props/MuseumTicket, Props/AudTicket, Props/RouenTicket/build_rouen_ticket_pdf.py) still
describe the superseded layouts; do not run them for print, they would overwrite these files.
The Aud ticket keeps its old designer answer-copy page as page 3.

Run:  python NorseBackpack/Props/ReadabilityDrafts/adopt_to_live.py
"""
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parents[3]
PDF = ROOT / "NorseBackpack" / "Print" / "_pdf_source"
DRAFTS = PDF / "Readability_Redesign_Drafts"
ROUEN = PDF / "Rouen_Redesign_Draft"
OLD = ROOT.parent / "Norse_Snapshots" / "Norse_2026-10-17_PreReadability" / "output" / "pdf"


def pages(src, first, last, dest, extra=None):
    out = pymupdf.open()
    with pymupdf.open(src) as d:
        out.insert_pdf(d, from_page=first, to_page=last)
    if extra:
        with pymupdf.open(extra[0]) as e:
            out.insert_pdf(e, from_page=extra[1], to_page=extra[1])
    out.save(dest, deflate=True)
    out.close()
    print(dest.name)


pages(DRAFTS / "Readability_Drafts_Review.pdf", 0, 1, PDF / "Museum_Ticket_Print.pdf")
pages(DRAFTS / "Readability_Drafts_Letter_Print.pdf", 0, 1, PDF / "Museum_Ticket_Letter_Print.pdf")
pages(DRAFTS / "Readability_Drafts_Review.pdf", 2, 3, PDF / "Aud_Ticket_Print.pdf", extra=(OLD / "Aud_Ticket_Print.pdf", 2))
pages(DRAFTS / "Readability_Drafts_Letter_Print.pdf", 2, 3, PDF / "Aud_Ticket_Letter_Print.pdf")
pages(DRAFTS / "Readability_Drafts_Review.pdf", 4, 4, PDF / "Liv_Notes_Card_Print.pdf")
# Keep the subsequently approved help reverse when re-adopting the front.
import runpy
_liv = runpy.run_path(str(ROOT / 'NorseBackpack/Props/LivNotes/build_liv_notes_back.py'))
_liv['build'](refresh_front=True)
pages(ROUEN / "Rouen_Ticket_Redesign.pdf", 0, 1, PDF / "Rouen_Ticket_Print.pdf")
pages(ROUEN / "Rouen_Ticket_Redesign_Letter.pdf", 0, 1, PDF / "Rouen_Ticket_Letter_Print.pdf")
