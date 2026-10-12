"""Norse box parts list (bill of materials), drafted from the prop records on 11 Oct 2026.

The rows are a hand-checked reading of NorseBackpack/records/props (PP-023..PP-047),
PR-007 (box and envelopes) and Q-052 (low-cost production ideas); they are not
regenerated from the records automatically. Prices are left blank to fill in from quotes.

Output: NorseBackpack/Production/Norse_Parts_List.xlsx. Refuses to overwrite an existing
file (it may hold typed-in quotes) unless run with --force.
"""
import sys
from pathlib import Path

from openpyxl import Workbook
from openpyxl.comments import Comment
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

OUT = Path(__file__).with_name("Norse_Parts_List.xlsx")

# (envelope, item, record, qty per box, prototype now, production idea, size/spec, status/open)
ROWS = [
    ("Box", "Box", "PP-045", 1, "Not bought", "Board-game-style box",
     "11.5 × 11.5 × 2 in (outside)", "Inside size not measured (Q-049). What it is in the story: Q-047."),
    ("Box", "Luggage tags", "PP-023", 2, "Lewis N. Clark tags, bought ($9.95 CAD each retail)", "Printed card parcel tags on twine (Q-047 option)",
     "4.25 × 2.5 in", "How tags attach to a box is open (Q-047)."),
    ("Box", "Luggage tag inserts", "PP-023", 2, "Printed business cards", "Same, or printed straight on the card tag",
     "Business card", ""),
    ("Box", "Rune cypher wheel (4 disks + arm)", "PP-047", 1, "Cardstock print, hand cut", "Die-cut cardboard",
     "Disks 196, 156, 116, 76 mm; arm 202 × 18 mm", "Prototype not yet printed or assembled."),
    ("Box", "Brass fastener for the wheel", "PP-047", 1, "Brass split pin", "Brass split pin or plastic rivet",
     "Through all 5 layers", ""),
    ("Box", "Rune labels for envelopes", "PP-047", 13, "Printed sheet, cut by hand", "Printed straight on the envelopes",
     "58 × 22 mm", "Decoy envelopes would add labels (Q-050)."),
    ("Box", "Envelopes, paper", "PR-007", 9, "—", "Kraft or cream envelopes",
     "6 × 9 in assumed (folded maps fit)", "Assumption: envelopes 2, 3, 4, 5, 6, 8, 9, 11, 12. Sizes open (Q-049)."),
    ("Box", "Envelopes, padded or gusseted", "PR-007", 4, "—", "Padded envelopes",
     "Fits 1, 7, 10, 13", "Assumption: magnifier, coins + tally, game pieces, medallion. Sizes open (Q-049)."),
    ("Various", "Postcards (18 stops + 4 decoys)", "PP-001–PP-022", 22, "Printed, double-sided", "Printed card stock",
     "5 × 3.5 in, double-sided", "L1 starts loose in the box; the rest are spread over envelopes 1–12."),
    ("1", "Magnifier", "PP-027", 1, "Candidate: 90 mm glass, wooden handle", "Flat Fresnel card magnifier",
     "Credit-card size (production idea)", "Must make the branch runes and the 1576 top edge readable. Not tested."),
    ("2", "Aud's comb", "PP-028", 1, "3D print", "Die-cut cardboard grille",
     "Sits over postcard AD", "Tooth gaps must still expose the BOOK letters."),
    ("4", "Architect's scale ruler", "PP-025", 1, "Ruler on hand (length not recorded)", "Printed card ruler (Claude's idea, not the designer's)",
     "Needs 1:25 and 1:125 scales", "A 30 cm ruler won't lie flat in the box (Q-049)."),
    ("4, 6, 8, 10", "Trail maps", "PP-029/030/032/034", 4, "Letter sheets, laminated", "Not laminated, folded in half",
     "8.5 × 11 in; Harald's is double-sided", "Check Harald's back still reads without lamination."),
    ("4", "Aud's Treasure Museum ticket", "PP-031", 1, "Printed", "Printed card", "Size not recorded", ""),
    ("6", "Viking Museum of Brattahlíð ticket", "PP-024", 1, "Printed", "Printed card", "About 2 in wide", "Front/back registration drift seen in a test print."),
    ("7", "Coin hoard", "PP-037", 12, "3D print", "Open: not discussed",
     "5 dirhams, 4 deniers, 3 Norse coins", "Cheap options to price: stock replica coins, wooden or card discs."),
    ("7", "Treasure tally", "PP-026", 1, "3D-printed four-wheel counter", "Cardboard wheels in windows",
     "Seven-segment digits", "3705 must read SOLE upside down."),
    ("8", "Musée Ducal de Rouen ticket", "PP-033", 1, "Printed", "Printed card", "2 × 3 in", "To re-print (record, 29 Sept)."),
    ("10", "Hnefatafl board", "PP-035", 1, "3D print / printed", "Printed cardboard board", "11 × 11 squares; size not recorded",
     "Must fit the box (fold if needed)."),
    ("10", "Hnefatafl pieces", "PP-035", 23, "3D print", "Stock wooden pawns",
     "16 dark, 6 light, 1 king", "King must look different (taller piece)."),
    ("10", "Hnefatafl Museum ticket, Oslo", "PP-036", 1, "Printed", "Printed card", "Size not recorded",
     "Mirrored back must read through when held to the light; test on chosen stock."),
    ("11", "The raven's flights card", "PP-038", 1, "To print", "Printed card", "Half letter (proposed)", ""),
    ("12", "Transition tickets", "PP-039", 3, "Printed", "Printed card", "Size not recorded", ""),
    ("12", "Liv's journal", "PP-040", 1, "Printed", "Printed", "Letter; page count not recorded", ""),
    ("12", "Family logo and crest note", "PP-041", 1, "Printed", "Printed", "Size not recorded", ""),
    ("13", "Plane ticket and letter", "PP-043", 1, "Printed", "Printed", "Size not recorded", "Counted as one set (ticket + letter)."),
    ("13", "Adventure medallion", "PP-044", 1, "3D print", "Open: not discussed", "50 mm × 4.4 mm",
     "Cheap options to price: struck metal coin, wooden token."),
    ("Box", "Hint page card (QR code)", "—", 1, "—", "Printed card", "Business card",
     "Not in the records: Claude's suggestion. Hint page address is known."),
    ("Box", "How to use the cypher wheel", "—", 1, "—", "Printed card or print on the box lid", "Not set",
     "Not in the records: Claude's suggestion."),
]

ARIAL = "Arial"
HEAD_FILL = PatternFill("solid", fgColor="283B34")
INPUT_FILL = PatternFill("solid", fgColor="FFFF00")
BAND_FILL = PatternFill("solid", fgColor="F3EBD8")
THIN = Side(style="thin", color="BFBFBF")
BOX = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
WRAP = Alignment(wrap_text=True, vertical="top")
MONEY = '$#,##0.00;($#,##0.00);"-"'

HEADERS = ["Envelope", "Item", "Record", "Qty per box", "Prototype now", "Production idea (Q-052)",
           "Size / spec", "Status / open", "Unit cost @500 (CAD $)", "Unit cost @1,000 (CAD $)",
           "Line cost @500 (CAD $)", "Line cost @1,000 (CAD $)", "Supplier / quote notes"]
WIDTHS = [11, 30, 17, 9, 30, 30, 26, 44, 14, 14, 14, 14, 30]


def parts_sheet(ws):
    ws.title = "Parts list"
    for col, (h, w) in enumerate(zip(HEADERS, WIDTHS), 1):
        cell = ws.cell(row=1, column=col, value=h)
        cell.font = Font(name=ARIAL, bold=True, color="FFFFFF")
        cell.fill = HEAD_FILL
        cell.alignment = Alignment(wrap_text=True, vertical="center")
        cell.border = BOX
        ws.column_dimensions[cell.column_letter].width = w
    ws.row_dimensions[1].height = 32
    first = 2
    for i, row in enumerate(ROWS):
        r = first + i
        for col, value in enumerate(row, 1):
            ws.cell(row=r, column=col, value=value)
        ws.cell(row=r, column=11, value=f"=IF(I{r}=\"\",\"\",D{r}*I{r})")
        ws.cell(row=r, column=12, value=f"=IF(J{r}=\"\",\"\",D{r}*J{r})")
        for col in range(1, 14):
            cell = ws.cell(row=r, column=col)
            cell.font = Font(name=ARIAL, size=10)
            cell.alignment = WRAP
            cell.border = BOX
            if col in (9, 10, 13):
                cell.fill = INPUT_FILL
            elif row[0] in ("Box", "Various"):
                cell.fill = BAND_FILL
            if col in (9, 10, 11, 12):
                cell.number_format = MONEY
        ws.cell(row=r, column=4).alignment = Alignment(horizontal="center", vertical="top")
    last = first + len(ROWS) - 1
    total = last + 2
    ws.cell(row=total, column=8, value="Cost per box (priced lines only)")
    ws.cell(row=total, column=11, value=f"=SUM(K{first}:K{last})")
    ws.cell(row=total, column=12, value=f"=SUM(L{first}:L{last})")
    ws.cell(row=total + 1, column=8, value="Lines still without a price")
    ws.cell(row=total + 1, column=11, value=f"=COUNTBLANK(I{first}:I{last})")
    ws.cell(row=total + 1, column=12, value=f"=COUNTBLANK(J{first}:J{last})")
    for r in (total, total + 1):
        for col in (8, 11, 12):
            cell = ws.cell(row=r, column=col)
            cell.font = Font(name=ARIAL, bold=True, size=10)
            cell.border = BOX
        ws.cell(row=r, column=11).number_format = MONEY if r == total else "0"
        ws.cell(row=r, column=12).number_format = MONEY if r == total else "0"
    ws.cell(row=total, column=11).comment = Comment(
        "Sums only lines with a unit cost typed in. Check 'Lines still without a price' below before trusting it.", "Claude")
    ws.freeze_panes = "C2"
    ws.auto_filter.ref = f"A1:M{last}"


def notes_sheet(wb):
    ws = wb.create_sheet("Notes")
    ws.column_dimensions["A"].width = 26
    ws.column_dimensions["B"].width = 100
    lines = [
        ("How to use", None),
        ("Fill in", "Yellow cells on 'Parts list': unit costs at 500 and 1,000 units (CAD, per single piece, as quoted), and supplier notes. Line costs and totals calculate themselves."),
        ("Qty per box", "How many of that item go in one box. A quote for '500 boxes' of coins is 500 × 12 coins."),
        ("Example", "Hnefatafl pieces · Qty 23 · Unit cost @500: 0.04 · Line cost @500: 0.92 (example values only, not a quote)."),
        ("Sources", None),
        ("Records", "Drafted 11 Oct 2026 from the prop records (PP-023–PP-047), PR-007 (box and envelopes) and Q-052 (production ideas). Prices typed here do not flow back to the records."),
        ("Only known price", "Luggage tag, $9.95 CAD each retail (PP-023). Listed under 'Prototype now', not as a unit cost, because it is a one-off retail price."),
        ("Assumptions", None),
        ("Envelope split", "9 paper + 4 padded is Claude's assumption, based on Q-052's cardboard comb, tally and board and unlaminated folded maps. Sizes are open (Q-049)."),
        ("Production ideas", "From the designer (Q-052) except the printed card ruler, the hint card and the wheel instructions, which are Claude's suggestions and marked so."),
        ("Not included", None),
        ("Parked", "Wet-erase marker (PP-042) and lock number stickers (PP-046) are parked, so not listed."),
        ("Decoys", "Decoy envelopes (Q-050) are undecided; add rows once decided."),
        ("Shipping, fees", "Not in this sheet: freight, fulfilment, packaging outside the box, Kickstarter and payment fees."),
    ]
    for r, (a, b) in enumerate(lines, 1):
        ws.cell(row=r, column=1, value=a)
        if b is None:
            ws.cell(row=r, column=1).font = Font(name=ARIAL, bold=True, size=11, color="283B34")
        else:
            ws.cell(row=r, column=1).font = Font(name=ARIAL, bold=True, size=10)
            cell = ws.cell(row=r, column=2, value=b)
            cell.font = Font(name=ARIAL, size=10)
            cell.alignment = WRAP


def main():
    if OUT.exists() and "--force" not in sys.argv:
        sys.exit(f"{OUT} exists and may hold quotes; rerun with --force to replace it.")
    wb = Workbook()
    parts_sheet(wb.active)
    notes_sheet(wb)
    wb.save(OUT)
    print(OUT, len(ROWS), "rows")


if __name__ == "__main__":
    main()
