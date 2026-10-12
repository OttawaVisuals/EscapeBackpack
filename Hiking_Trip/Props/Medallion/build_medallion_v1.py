"""Make a Hiking keepsake using the selected front and the approved Space back."""
from pathlib import Path
import sys
import json

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(REPO / "Tools"))
import medallion_cad as cad


def main():
    cad.OUT = HERE
    cad.SOURCE = HERE / "sources/Hiking_Front_Concept_v1.png"
    front, trace = cad.front_profile()
    report, checks = cad.build_model(
        HERE, "Hiking", "v1", front, trace, "Hiking_Medallion_v1_Preview.png",
        "Yellow relief: mountains, trail and pine trees")
    files = [
        HERE / "STL/Hiking_Medallion_OnePiece_v1.stl",
        HERE / "STL/Hiking_Back_Lettering_Test_1.2mm_v1.stl",
        HERE / "Front_Relief_v1.svg", HERE / "Back_Engraving_v1.svg",
        HERE / "Hiking_Medallion_v1_Preview.png", HERE / "geometry_report_v1.json",
        HERE / "mesh_check_v1.json", HERE / "lettering_test_mesh_check_v1.json",
        HERE / "README.md", HERE / "front_trace_mask_v1.png",
        HERE / "sources/Hiking_Front_Concept_v1.png",
        HERE / "sources/front_prompt_v1.txt", Path(__file__).resolve(),
        REPO / "Tools/medallion_cad.py",
    ]
    cad.package_files(REPO, HERE / "Hiking_Medallion_Print_Files_v1.zip", files)
    print(json.dumps({"model": "Hiking v1", "mesh": checks}, indent=2))


if __name__ == "__main__":
    main()
