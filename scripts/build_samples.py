#!/usr/bin/env python3
"""Art-directed sample pieces (world templates).   python3 -I scripts/build_samples.py <command> ...

  frames p01 <t> [<t> ...]      render still frames of the WELCOME reel at the given seconds (fast look-dev check)
  p01                           render the full reel + original score -> /home/claude/out/samples/p01_welcome.mp4
  p02                           render the 7-slide carousel from one continuous strip
  p03                           render the 2-slide TORQ showcase from one continuous strip
"""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from wa import brand, render, video  # noqa: E402

ROOT = brand.ROOT
OUT = pathlib.Path("/home/claude/out/samples")
GRAIN = str(ROOT / "assets" / "textures" / "grain.png")


def welcome_timeline():
    S = {"c1a": (0.60, 0.80, 0.80, 100), "c1b": (0.82, 1.00, 1.00, 85),
         "c2": (2.20, 2.50, 0.85, 95), "c3": (3.20, 3.50, 0.85, 105), "c4": (4.20, 4.50, 0.90, 90)}
    strikes = {k: {"start": a, "hit": b, "amp": amp, "f0": f0} for k, (a, b, amp, f0) in S.items()}
    t0, dt = 5.0, 0.25
    for i in range(6):
        T = t0 + dt * i
        strikes[f"m{i + 1}"] = {"start": round(T + 0.04, 3), "hit": round(T + 0.22, 3),
                                "amp": 0.95 if i == 5 else 0.55, "f0": 140 + 14 * i if i < 5 else 110}
    return {
        "duration": 13.0, "strikes": strikes,
        "scenes": [
            {"id": "c1", "in": -1, "out0": 1.30, "out1": 1.55, "dx": 0, "dy": -1500, "rot": 0},
            {"id": "c2", "in": 1.50, "out0": 2.80, "out1": 3.00, "dx": -1300, "dy": 0, "rot": -8},
            {"id": "c3", "in": 3.00, "out0": 3.75, "out1": 3.95, "dx": 0, "dy": 1500, "rot": 0},
            {"id": "c4", "in": 4.00, "base": "rotate(3deg)", "out0": 4.75, "out1": 4.95, "dx": 1300, "dy": -400, "rot": 6},
        ],
        "pile_t0": t0, "pile_dt": dt, "pile_out0": 6.80, "pile_out1": 7.10,
        "col0": 7.30, "col1": 7.60, "ground0": 7.60, "ground1": 8.30, "morph0": 8.30, "morph1": 9.10,
        "sentence0": 8.55, "sentence_dt": 0.15, "tag0": 10.2, "belly": 170,
        "sentence_top": 820, "underline_dy": 22,
        "hits": [{"t": v["hit"], "amp": v["amp"], "f0": v["f0"]} for v in strikes.values()],
    }


def welcome_score(tl):
    return {"engine": "strike", "hits": sorted(tl["hits"], key=lambda h: h["t"]),
            "swooshes": [(v["start"], v["hit"]) for v in tl["strikes"].values()],
            "drone": {"hz": 55.0, "until": 7.0}, "blow": (tl["pile_out0"], tl["pile_out1"]),
            "bell": {"t": tl["morph1"], "hz": 587.33, "amp": 0.35}, "seed": 11}


def cmd_frames(times):
    tl = welcome_timeline()
    OUT.mkdir(parents=True, exist_ok=True)
    html = render.env.get_template("worlds/reel_welcome.html.j2").render(**render.context({"tl": tl, "grain": GRAIN}, (1080, 1920)))
    hp = OUT / "p01_frames.html"
    hp.write_text(html)
    with render.Renderer() as r:
        pg = r.page((1080, 1920))
        pg.goto(f"file://{hp}")
        pg.evaluate("window.__ready")
        pg.wait_for_timeout(300)
        for t in times:
            pg.evaluate("t => window.setT(t)", t)
            pg.screenshot(path=str(OUT / f"p01_f{t:05.2f}.png"))
        pg.close()
    print("frames:", [f"p01_f{t:05.2f}.png" for t in times])


def cmd_p01():
    tl = welcome_timeline()
    with render.Renderer() as r:
        out = video.render_reel(r, "worlds/reel_welcome.html.j2", {"tl": tl, "grain": GRAIN}, OUT / "p01_welcome.mp4",
                                duration=tl["duration"], score=welcome_score(tl), crf=21)
    print(out)


def cmd_p02():
    OUT.mkdir(parents=True, exist_ok=True)
    with render.Renderer() as r:
        files = r.strip("worlds/field_note_1.html.j2", {"grain": GRAIN}, OUT / "p02_fn01", 7, size=(1080, 1350))
    print(json.dumps(files, indent=1))
    from PIL import Image
    ims = [Image.open(f).convert("RGB").resize((360, 450)) for f in files]
    sheet = Image.new("RGB", (len(ims) * 365, 455), (30, 30, 30))
    for i, im in enumerate(ims):
        sheet.paste(im, (i * 365, 2))
    sheet.save(OUT / "p02_sheet.png")


def cmd_p03():
    OUT.mkdir(parents=True, exist_ok=True)
    crops = OUT / "crops"
    ctx = {"grain": GRAIN, "crop_hero": str(crops / "torq_hero.jpg"), "crop_hero_tall": str(crops / "torq_hero_tall.jpg"), "crop_ivory": str(crops / "torq_ivory.jpg")}
    with render.Renderer() as r:
        files = r.strip("worlds/showcase_tilt.html.j2", ctx, OUT / "p03_torq", 2, size=(1080, 1350))
    print(json.dumps(files, indent=1))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "frames":
        cmd_frames([float(x) for x in sys.argv[3:]])
    elif cmd == "p03":
        cmd_p03()
    elif cmd == "p02":
        cmd_p02()
    elif cmd == "p01":
        cmd_p01()
    else:
        raise SystemExit(__doc__)
