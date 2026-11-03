"""Real website screenshots.

Source: Framer `exec` -> api.tree.screenshot(<breakpoint node id>) is READ-ONLY and the returned image also lands as a file in
/tmp/claude-tool-results/<id>/mcp-Framer-blob-*.jpg inside this sandbox. `ingest` copies it into assets/screenshots/ and records
where it came from. Never invent or mock up a screenshot; never describe demo work as client work.
"""
import datetime as dt
import glob
import json
import os
import shutil

from PIL import Image

from . import brand

ROOT = brand.ROOT
IDX = ROOT / "assets" / "screenshots" / "index.json"


def latest(n=10):
    files = glob.glob("/tmp/claude-tool-results/*/mcp-Framer-blob-*.jpg")
    return sorted(files, key=os.path.getmtime, reverse=True)[:n]


def ingest(src, slug, project_title, project_id, breakpoint="Desktop", demo=True, notes=""):
    dest_dir = ROOT / "assets" / "screenshots" / slug
    dest_dir.mkdir(parents=True, exist_ok=True)
    w, h = Image.open(src).size
    dest = dest_dir / f"{breakpoint.lower()}.jpg"
    shutil.copy2(src, dest)
    idx = json.loads(IDX.read_text()) if IDX.exists() else {"screenshots": []}
    idx["screenshots"] = [e for e in idx["screenshots"] if not (e["slug"] == slug and e["breakpoint"] == breakpoint)]
    idx["screenshots"].append({
        "slug": slug, "project_title": project_title, "project_id": project_id, "breakpoint": breakpoint,
        "path": str(dest.relative_to(ROOT)), "size": [w, h], "demo": demo,
        "captured": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "source": "Framer exec api.tree.screenshot (real render of the project page; project may be unpublished)",
        "notes": notes,
    })
    IDX.write_text(json.dumps(idx, indent=2, ensure_ascii=False) + "\n")
    return str(dest)


def candidate_offsets(path, window_h=900, min_gap=700, threshold=28):
    """Source-pixel y offsets where the page background changes (section starts): good starting points for crops/scroll stops."""
    im = Image.open(path).convert("L")
    w, h = im.size
    strip = im.resize((8, h))  # row-wise mean brightness
    rows = [sum(strip.getpixel((x, y)) for x in range(8)) / 8 for y in range(h)]
    offsets, last = [0], 0
    for y in range(40, h - window_h // 2):
        before = sum(rows[y - 40:y - 10]) / 30
        after = sum(rows[y + 10:y + 40]) / 30 if y + 40 < h else rows[-1]
        if abs(after - before) > threshold and y - last >= min_gap:
            offsets.append(y)
            last = y
    return offsets
