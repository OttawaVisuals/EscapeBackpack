"""Report Norse files that break the one-version rule (AGENTS.md, Working Rules).

Read-only: it prints a report and never moves, renames or deletes anything.

    python NorseBackpack/Tools/audit_files.py

Four sections:

1. Images that nothing names. A text file in NorseBackpack/ (script, page,
   record) counts as naming an image if it has the file name, the name
   without its extension, or a pattern that builds it (`Coin_${art}.svg`,
   f"Ruler_Face_{n}.svg", "Card_%02d.png", "Stamp_*.png"). Unnamed files in
   a Sources/ or References/ folder are listed apart: they are masters.
2. Older _vN versions in the same folder as a newer _vN of the same image.
3. Exact duplicates (same bytes), any file type.
4. __pycache__/ folders.

Skipped, as in the 18 Oct 2026 cleanup: site/ (kit build output) and the
frozen Norse_Brainstorm.html. Only text files are read for names; images
and PDFs are only hashed when another file has exactly the same size.
Superseded files go to C:\\EscapeBackpack\\Norse_Archive\\ (see its README).
"""

import hashlib
import re
from collections import defaultdict
from pathlib import Path

NORSE = Path(__file__).resolve().parents[1]
SKIP_DIRS = {"site", "__pycache__", "node_modules", ".git"}
SKIP_SOURCES = {"Norse_Brainstorm.html"}
MASTER_DIRS = {"Sources", "References"}  # raw ImageGen outputs and photo credits
TEXT_EXT = {".py", ".md", ".html", ".js", ".cjs", ".mjs", ".json", ".css", ".txt", ".scad", ".svg"}
IMAGE_EXT = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg", ".tif", ".tiff"}
MAX_TEXT = 5 * 1024 * 1024

EXT_RE = "|".join(e[1:] for e in sorted(IMAGE_EXT))
# A file name, possibly with placeholders: ${x}, {x}, {n:02d}, %s, %02d, *
NAME_RE = re.compile(r"(?:[\w\-.$%*]|\{[^{}\s]*\})+\.(?:" + EXT_RE + r")(?!\w)", re.I)
PLACEHOLDER_RE = re.compile(r"\$?\{[^{}]*\}|%[0-9.]*[sd]|\*")
WORD_RE = re.compile(r"[\w\-]+")
VERSION_RE = re.compile(r"^(.*?)[_\-]v(\d+)(.*)$", re.I)


def walk(root):
    for p in root.iterdir():
        if p.is_dir():
            if p.name in SKIP_DIRS:
                continue
            yield from walk(p)
        else:
            yield p


def rel(p):
    return p.relative_to(NORSE).as_posix()


def size(n):
    return f"{n / 1024 / 1024:.1f} MB" if n >= 1024 * 1024 else f"{max(1, round(n / 1024))} KB"


def pattern_regex(token):
    """Regex for a name with placeholders, or None if it is too broad to mean anything."""
    parts = PLACEHOLDER_RE.split(token)
    stem_literal = "".join(parts).rsplit(".", 1)[0]
    if len(stem_literal.strip("_-.")) < 2:
        return None
    return re.compile("^" + ".+?".join(re.escape(x) for x in parts) + "$", re.I)


def main():
    files = list(walk(NORSE))
    images = [p for p in files if p.suffix.lower() in IMAGE_EXT]

    names, words, patterns = set(), set(), {}
    for p in files:
        if p.suffix.lower() not in TEXT_EXT or p.name in SKIP_SOURCES:
            continue
        if p.stat().st_size > MAX_TEXT:
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        for token in NAME_RE.findall(text):
            if PLACEHOLDER_RE.search(token):
                if token not in patterns:
                    patterns[token] = pattern_regex(token)
            else:
                names.add(token.lower())
        words.update(w.lower() for w in WORD_RE.findall(text))
    pattern_list = [r for r in patterns.values() if r]

    def named(p):
        n, stem = p.name.lower(), p.stem.lower()
        if n in names:
            return True
        # Bare stems only count when they look like file names, not words like "preview".
        if stem in words and re.search(r"[_\-\d]", stem):
            return True
        return any(r.match(p.name) for r in pattern_list)

    unused = sorted((p for p in images if not named(p)), key=rel)

    groups = defaultdict(list)
    for p in images:
        m = VERSION_RE.match(p.stem)
        if m:
            groups[(p.parent, m.group(1).lower(), p.suffix.lower())].append((int(m.group(2)), p))
    older = []
    for versions in groups.values():
        top = max(v for v, _ in versions)
        newest = [p for v, p in versions if v == top]
        older += [(p, newest) for v, p in versions if v < top]
    older.sort(key=lambda x: rel(x[0]))

    by_size = defaultdict(list)
    for p in files:
        s = p.stat().st_size
        if s:
            by_size[s].append(p)
    by_hash = defaultdict(list)
    for s, same in by_size.items():
        if len(same) > 1:
            for p in same:
                with open(p, "rb") as f:
                    by_hash[(s, hashlib.file_digest(f, "sha1").hexdigest())].append(p)
    dupes = sorted((sorted(g, key=rel) for g in by_hash.values() if len(g) > 1), key=lambda g: rel(g[0]))

    caches = sorted(rel(d) for d in NORSE.rglob("__pycache__") if d.is_dir() and "site" not in d.relative_to(NORSE).parts)

    print(f"Norse file audit: {NORSE}")
    print(f"{len(files)} files, {len(images)} images, {len(pattern_list)} name patterns. Nothing was moved.\n")

    masters = [p for p in unused if MASTER_DIRS & set(p.relative_to(NORSE).parts)]
    loose = [p for p in unused if p not in masters]
    print(f"## 1. Images nothing names ({len(loose)}, {size(sum(p.stat().st_size for p in loose))})")
    for p in loose:
        print(f"- {rel(p)}  ({size(p.stat().st_size)})")
    print(f"\n## 1b. Same, but in Sources/ or References/: masters, expected ({len(masters)}, "
          f"{size(sum(p.stat().st_size for p in masters))})")
    for p in masters:
        print(f"- {rel(p)}  ({size(p.stat().st_size)})")

    print(f"\n## 2. Older versions next to a newer one ({len(older)}, {size(sum(p.stat().st_size for p, _ in older))})")
    for p, newest in older:
        note = "" if not named(p) else "  [still named somewhere]"
        print(f"- {rel(p)}  (newer: {', '.join(n.name for n in newest)}){note}")

    extra = sum(g[0].stat().st_size * (len(g) - 1) for g in dupes)
    print(f"\n## 3. Exact duplicates ({len(dupes)} groups, {size(extra)} in extra copies)")
    for g in dupes:
        print(f"- {size(g[0].stat().st_size)} each:")
        for p in g:
            print(f"    {rel(p)}")

    print(f"\n## 4. __pycache__ folders ({len(caches)})")
    for d in caches:
        print(f"- {d}")


if __name__ == "__main__":
    main()
