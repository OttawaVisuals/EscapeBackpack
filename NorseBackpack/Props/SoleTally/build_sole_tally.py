"""Build the SOLE treasure-tally counter ring.

1. Extracts the reference counter ring (body only) from reference/4-digit_counter.3mf.
2. Runs OpenSCAD on sole_tally_ring.scad to export the ring body and the digit inlay.
3. Renders preview PNGs, including the 3705 face row turned 180 degrees (should read SOLE).
"""
import re
import struct
import subprocess
import zipfile
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
REF = HERE / "reference"
OUT = HERE / "STL"
OPENSCAD = Path(r"C:\Program Files\OpenSCAD\openscad.com")


def read_3mf_parts(path, member):
    text = zipfile.ZipFile(path).read(member).decode()
    parts = {}
    for m in re.finditer(r'<object id="(\d+)".*?</object>', text, re.S):
        block = m.group(0)
        v = np.array(re.findall(r'<vertex x="([^"]+)" y="([^"]+)" z="([^"]+)"', block), float)
        f = np.array(re.findall(r'<triangle v1="(\d+)" v2="(\d+)" v3="(\d+)"', block), int)
        parts[int(m.group(1))] = (v, f)
    return parts


def write_stl(path, verts, faces):
    tri = verts[faces]
    normals = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
    normals /= np.maximum(np.linalg.norm(normals, axis=1, keepdims=True), 1e-12)
    with open(path, "wb") as fh:
        fh.write(b"counterring_body".ljust(80, b"\0"))
        fh.write(struct.pack("<I", len(faces)))
        for n, t in zip(normals, tri):
            fh.write(struct.pack("<12fH", *n, *t.ravel(), 0))


def extract_reference():
    # object 2 in object_8.model is the ring body (digits cut, click arms);
    # object 1 is the old two-colour digit band, which we do not reuse.
    parts = read_3mf_parts(REF / "4-digit_counter.3mf", "3D/Objects/object_8.model")
    v, f = parts[2]
    write_stl(REF / "counterring_body.stl", v, f)
    # Base and end cap are used unchanged. Each also has a small second-colour marker
    # part (the reading line); single-colour printing skips it and leaves a paintable groove.
    for member, part, name in [("3D/Objects/object_17.model", 4, "SOLE_base.stl"),
                               ("3D/Objects/object_16.model", 8, "SOLE_endcap.stl")]:
        v, f = read_3mf_parts(REF / "4-digit_counter.3mf", member)[part]
        write_stl(OUT / name, v, f)


def read_stl(path):
    data = Path(path).read_bytes()
    if data[:5] == b"solid":
        tri = np.array(re.findall(rb"vertex\s+(\S+)\s+(\S+)\s+(\S+)", data), float).reshape(-1, 3, 3)
    else:
        n = struct.unpack("<I", data[80:84])[0]
        rec = np.frombuffer(data[84:84 + 50 * n], dtype=np.dtype([("n", "<3f4"), ("v", "<9f4"), ("a", "<u2")]))
        tri = rec["v"].reshape(-1, 3, 3).astype(float)
    return tri


def face_coords(pts):
    """Per point: face index k, distance from centre along the face normal d, tangent t."""
    ang = np.degrees(np.arctan2(pts[..., 1], pts[..., 0])) % 360
    k = np.floor(ang / 36).astype(int)
    c = np.radians(18 + 36 * k)
    d = pts[..., 0] * np.cos(c) + pts[..., 1] * np.sin(c)
    t = -pts[..., 0] * np.sin(c) + pts[..., 1] * np.cos(c)
    return k, d, t


def render_check():
    """Unwrapped faces of the printed ring, plus the 3705 row as seen and turned 180 degrees."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.collections import PolyCollection

    body = read_stl(OUT / "SOLE_ring_body.stl")
    inlay = read_stl(OUT / "SOLE_ring_inlay.stl")
    apothem = 12.02 * np.cos(np.radians(18))  # FILL_R in the .scad

    def digit_polys(tri, want_d, tol):
        k, d, t = face_coords(tri)
        polys = {}
        for i in range(len(tri)):
            if k[i, 0] == k[i, 1] == k[i, 2] and np.all(abs(d[i] - want_d) < tol):
                # view from outside with the digit upright: right = +z, up = -t
                polys.setdefault(k[i, 0], []).append(np.c_[tri[i, :, 2], -t[i]])
        return polys

    cut = digit_polys(body, 10.85, 0.03)      # cut floors in the ring body
    top = digit_polys(inlay, apothem, 0.03)   # visible inlay surface
    fig, ax = plt.subplots(3, 10, figsize=(16, 6.5))
    for v in range(10):
        k = 9 - v
        for row, polys in ((0, cut), (1, top)):
            a = ax[row, v]
            a.add_collection(PolyCollection(polys.get(k, []), facecolor="k"))
            a.set_xlim(-2.6, 2.1); a.set_ylim(-3.7, 3.7); a.set_aspect("equal"); a.set_xticks([]); a.set_yticks([])
        ax[0, v].set_title(f"digit {v}")
    ax[0, 0].set_ylabel("cut in body"); ax[1, 0].set_ylabel("inlay")
    for a in ax[2]:
        a.axis("off")
    for j, v in enumerate([3, 7, 0, 5]):
        for side, flip in ((0, 1), (5, -1)):
            a = ax[2, side + (j if flip == 1 else 3 - j)]
            polys = [flip * p for p in top.get(9 - v, [])]
            a.add_collection(PolyCollection(polys, facecolor="#8a5a00"))
            a.set_xlim(-2.6, 2.6); a.set_ylim(-3.7, 3.7); a.set_aspect("equal")
    ax[2, 1].set_title("3705 as set", loc="left")
    ax[2, 6].set_title("turned 180 degrees", loc="left")
    fig.tight_layout()
    fig.savefig(HERE / "SOLE_ring_check.png", dpi=110)


def openscad(*args):
    subprocess.run([str(OPENSCAD), *args], cwd=HERE, check=True)


def main():
    OUT.mkdir(exist_ok=True)
    extract_reference()
    scad = "sole_tally_ring.scad"
    openscad("-o", "STL/SOLE_ring_body.stl", "-D", 'PART="ring"', scad)
    openscad("-o", "STL/SOLE_ring_inlay.stl", "-D", 'PART="inlay"', scad)
    render_check()
    with zipfile.ZipFile(HERE / "SOLE_Tally_Print_Pack.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for name in ["SOLE_ring_body.stl", "SOLE_base.stl", "SOLE_endcap.stl"]:
            z.write(OUT / name, name)
        z.write(HERE / "PRINTING.md", "PRINTING.md")
        z.write(HERE / "SOLE_ring_check.png", "SOLE_ring_check.png")


if __name__ == "__main__":
    main()
