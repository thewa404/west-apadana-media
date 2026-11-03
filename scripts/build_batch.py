#!/usr/bin/env python3
"""Spec-driven batch builder.   python3 -I scripts/build_batch.py <command> ...

  build <spec.json> [--dry]    check duplicates -> render every piece -> verify -> review sheets -> inventory (+history) unless --dry
  publish <batch_id>           push all media in one commit, record Pages URLs + sha256, commit inventory
  payloads <batch_id>          write Metricool draft payloads to /home/claude/out/<batch>/payloads/ (Claude pastes them into the tool call)

Spec (JSON):
 {"batch_id": "2026-11-b01", "start_date": "2026-11-09",
  "pieces": [
   {"id": "b01-p01", "format": "reel", "concept": "...", "hook": "...", "headline": "...", "theme": "obsidian",
    "beats": [...], "scroll": {...optional real-screenshot scroll...}, "duration": 9, "score": {"root_hz": 73.42, "bpm": 56, "seed": 11},
    "captions": {"instagram": "...", "youtube": "..."}, "hashtags": {"instagram": ["#..."]}, "cta": {"instagram": "..."},
    "titles": {"youtube": "..."}, "source": "typography | Framer project title"},
   {"id": "b01-p02", "format": "carousel|graphic|showcase|story", "size": [1080, 1350], "fmt": "jpeg|png",
    "slides": [{"template": "slide.html.j2", "kind": "cover", ...template context...}, ...], "captions": {...}, ...}]}
 Screenshot paths in a spec may be repo-relative ("assets/screenshots/torq/desktop.jpg"); they are resolved automatically (keys: shot, scroll.src).
"""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from PIL import Image  # noqa: E402
from wa import brand, inventory, payload, publish, render, verify, video  # noqa: E402

ROOT = brand.ROOT
OUT = pathlib.Path("/home/claude/out")
S = brand.load("settings")


def _abs(p):
    p = pathlib.Path(p)
    return str(p if p.is_absolute() else ROOT / p)


def render_piece(r, piece, outdir):
    files = []
    if piece["format"] == "reel":
        ctx = {"theme": piece.get("theme", "obsidian"), "beats": piece["beats"], "chrome_label": piece.get("chrome_label", "Concept preview")}
        if piece.get("scroll"):
            sc = dict(piece["scroll"])
            sc["src"] = _abs(sc["src"])
            ctx["scroll"] = sc
        files.append(video.render_reel(r, "reel.html.j2", ctx, outdir / f"{piece['id']}.mp4", duration=piece["duration"], score=piece.get("score", {})))
        return files
    size = tuple(piece.get("size", [1080, 1350]))
    fmt = piece.get("fmt", "jpeg")
    n = len(piece["slides"])
    for i, s in enumerate(piece["slides"], 1):
        ctx = dict(s)
        tpl = ctx.pop("template", "slide.html.j2")
        if "shot" in ctx:
            ctx["shot_path"] = _abs(ctx.pop("shot"))
        if n > 1:
            ctx.setdefault("index", i)
            ctx.setdefault("total", n)
        out = outdir / f"{piece['id']}_{i}.{'jpg' if fmt == 'jpeg' else 'png'}"
        res = r.still(tpl, ctx, out, size=size, fmt=fmt)
        if not res["fonts_ok"]:
            raise RuntimeError(f"fonts did not load for {out}")
        files.append(str(out))
    return files


def check_piece(piece, files):
    problems = []
    for net in S["allocation"][piece["format"]]:
        for f in files:
            if f.lower().endswith((".png", ".jpg", ".jpeg")):
                if net == "youtube":
                    continue
                res = verify.verify_image(f, net)
            else:
                res = verify.verify_video(f, net, reel=True)
            if not res["ok"]:
                problems.append(f"{pathlib.Path(f).name} [{net}]: {'; '.join(res['issues'])}")
    return problems


def review_sheet(batch, firsts, outdir):
    thumbs = [Image.open(f).convert("RGB") for f in firsts]
    w = 360
    rows = (len(thumbs) + 4) // 5
    sheet = Image.new("RGB", (w * 5, int(w * 1.78) * rows), (30, 30, 30))
    for i, im in enumerate(thumbs):
        t = im.resize((w, int(im.height * w / im.width)))
        sheet.paste(t, ((i % 5) * w, (i // 5) * int(w * 1.78)))
    p = outdir / f"{batch}_review.png"
    sheet.save(p)
    return str(p)


def cmd_build(spec_path, dry):
    spec = json.loads(pathlib.Path(spec_path).read_text())
    batch = spec["batch_id"]
    outdir = OUT / batch
    outdir.mkdir(parents=True, exist_ok=True)
    for p in spec["pieces"]:
        if p.get("allow_similar"):
            continue
        for field in ("hook", "headline", "concept"):
            hits = inventory.check_duplicates(p.get(field, "")) if p.get(field) else []
            if hits:
                raise SystemExit(f"{p['id']} {field} too similar to previous work: {hits[0]}")
    cal = inventory.plan_calendar(spec["start_date"], [p["format"] for p in spec["pieces"]])
    firsts, report = [], []
    with render.Renderer() as r:
        for p, plan in zip(spec["pieces"], cal["pieces"]):
            files = render_piece(r, p, outdir)
            problems = check_piece(p, files)
            if p["format"] == "reel":
                verify.contact_sheet(files[0], outdir / f"{p['id']}_sheet.png")
                firsts.append(str(outdir / f"{p['id']}_sheet.png"))
            else:
                firsts.append(files[0])
            p["local_files"], p["targets"] = files, plan["targets"]
            report.append({"piece": p["id"], "files": [pathlib.Path(f).name for f in files], "problems": problems})
    sheet = review_sheet(batch, firsts, outdir)
    print(json.dumps({"batch": batch, "review_sheet": sheet, "per_month_network_posts": cal["per_month_network_posts"], "report": report}, indent=2))
    if any(x["problems"] for x in report):
        raise SystemExit("verification problems found: fix before publishing")
    if dry:
        print("dry run: inventory not written")
        return
    inv = inventory.load()
    inv["batches"] = [b for b in inv["batches"] if b["id"] != batch]
    keep = ("id", "format", "concept", "hook", "headline", "theme", "layout", "source", "captions", "hashtags", "cta", "titles", "first_comment", "alt", "local_files", "targets")
    inv["batches"].append({"id": batch, "created": inventory.dt.datetime.now(inventory.TZ).isoformat(timespec="seconds"), "status": "built",
                           "pieces": [{k: p[k] for k in keep if k in p} for p in spec["pieces"]]})
    inventory.save(inv)
    for p in spec["pieces"]:
        inventory.log_history(batch, p)
    print("inventory + history written")


def cmd_publish(batch):
    inv = inventory.load()
    b = next(x for x in inv["batches"] if x["id"] == batch)
    allfiles = [f for p in b["pieces"] for f in p["local_files"]]
    res = publish.publish(allfiles, batch, message=f"Add media for batch {batch}")
    by_name = {r["file"]: r for r in res["files"]}
    for p in b["pieces"]:
        p["files"] = [{"path": by_name[pathlib.Path(f).name]["path"], "url": by_name[pathlib.Path(f).name]["url"],
                       "sha256": by_name[pathlib.Path(f).name]["sha256"], "role": "media"} for f in p["local_files"]]
    b["status"] = "published-media"
    b["pages_ready_after"] = res["pages_ready_after"]
    inventory.save(inv)
    state = publish.commit_push(["inventory", "assets"], f"Update inventory for batch {batch}")
    print(json.dumps({"media_commit": res.get("commit"), "remote_matches": res.get("remote_matches"), "pages_ready_after": res["pages_ready_after"],
                      "files": len(res["files"]), "inventory_commit": state}, indent=2))


def cmd_payloads(batch):
    inv = inventory.load()
    b = next(x for x in inv["batches"] if x["id"] == batch)
    d = OUT / batch / "payloads"
    d.mkdir(parents=True, exist_ok=True)
    rows = []
    for p in b["pieces"]:
        for t in p["targets"]:
            pl = payload.build(p, t)
            f = d / f"{p['id']}_{t['network']}.json"
            f.write_text(json.dumps(pl, ensure_ascii=False))
            rows.append({"piece": p["id"], "network": t["network"], "date": t["date"], "payload": str(f)})
    print(json.dumps(rows, indent=2))


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        print(__doc__)
    elif a[0] == "build":
        cmd_build(a[1], "--dry" in a)
    elif a[0] == "publish":
        cmd_publish(a[1])
    elif a[0] == "payloads":
        cmd_payloads(a[1])
    else:
        print(__doc__)
