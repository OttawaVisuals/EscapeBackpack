from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "Norse_Medallion.scad"
STL_DIR = ROOT / "STL"
PROGRAM_FILES = Path(r"C:\Program Files\OpenSCAD")
OPENSCAD = PROGRAM_FILES / "openscad.com"
if not OPENSCAD.exists():
    found = shutil.which("openscad")
    if not found:
        raise SystemExit("OpenSCAD was not found. Install OpenSCAD, then rerun this script.")
    OPENSCAD = Path(found)

STL_DIR.mkdir(exist_ok=True)
for part in ("front", "back"):
    output = STL_DIR / f"Norse_Medallion_{part.title()}.stl"
    result = subprocess.run(
        [str(OPENSCAD), "-D", f'PART="{part}"', "-o", str(output), str(SOURCE)],
        capture_output=True, text=True, check=False,
    )
    if result.returncode or not output.exists():
        sys.stderr.write(result.stderr)
        raise SystemExit(f"OpenSCAD export failed for {part} (exit {result.returncode}).")
    print(f"Wrote {output.name} ({output.stat().st_size:,} bytes)")
