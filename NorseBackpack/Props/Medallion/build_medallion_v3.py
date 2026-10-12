"""Retain the exact v2 raven front; replace only the back with the Space layout."""
from pathlib import Path
import json
import sys
import numpy as np
from shapely.geometry import Point
from shapely import affinity

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(REPO / "Tools"))
import medallion_cad as cad
import build_medallion_v2 as previous


def main():
    front = previous.trace_crest()
    cad.OUT = HERE
    groove = Point(0, 0).buffer(23.4, quad_segs=128).boundary.buffer(.3)
    report, checks = cad.build_model(
        HERE, "Norse", "v3", front, {"method": "unchanged v2 trace_crest function"},
        "Medallion_v3_Preview.png", "Yellow relief: existing raven and shield",
        top_groove=groove)
    # Compare exact front cross-section triangles from the exported old/new STLs.
    def top_area(path):
        raw = path.read_bytes()
        dtype = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
        tri = np.frombuffer(raw, dtype=dtype, offset=84)["v"].astype(float)
        selected = tri[np.all(np.abs(tri[:, :, 2] - 4.4) < 1e-5, axis=1)]
        from shapely.geometry import Polygon
        from shapely.ops import unary_union
        return unary_union([Polygon(t[:, :2]) for t in selected])
    old = top_area(HERE / "STL/Norse_Medallion_OnePiece_v2.stl")
    new = top_area(HERE / "STL/Norse_Medallion_OnePiece_v3.stl")
    difference = old.symmetric_difference(new).area
    if difference > 1e-5:
        raise ValueError(f"Existing front geometry changed: {difference} square mm")
    report["front_symmetric_difference_from_v2_square_mm"] = difference
    (HERE / "geometry_report_v3.json").write_text(json.dumps(report, indent=2) + "\n")
    files = [
        HERE / "STL/Norse_Medallion_OnePiece_v3.stl",
        HERE / "STL/Norse_Back_Lettering_Test_1.2mm_v3.stl",
        HERE / "Front_Relief_v3.svg", HERE / "Back_Engraving_v3.svg",
        HERE / "Medallion_v3_Preview.png", HERE / "geometry_report_v3.json",
        HERE / "mesh_check_v3.json", HERE / "lettering_test_mesh_check_v3.json",
        HERE / "README.md", Path(__file__).resolve(),
        HERE / "build_medallion_v2.py", HERE / "sources/Crest_Detailed_v2.png",
        REPO / "Tools/medallion_cad.py",
        HERE / "STL/Norse_Medallion_OnePiece_v2.stl",
    ]
    cad.package_files(REPO, HERE / "Medallion_Print_Files.zip", files)
    print(json.dumps({"model": "Norse v3", "mesh": checks,
                      "front_difference_square_mm": difference}, indent=2))


if __name__ == "__main__":
    main()
