"""Automated media checks against config/platforms.json. Visual review is still done by looking at the output."""
import json
import pathlib
import subprocess

from PIL import Image

from . import brand

SPEC = brand.load("platforms")["networks"]


def verify_image(path, network="instagram"):
    p = pathlib.Path(path)
    s = SPEC[network]["image"]
    im = Image.open(p)
    w, h = im.size
    issues = []
    if im.format not in s["formats"]:
        issues.append(f"format {im.format} not in {s['formats']}")
    mb = p.stat().st_size / 1e6
    if mb > s["max_mb"]:
        issues.append(f"{mb:.2f} MB exceeds {s['max_mb']} MB")
    ratio = w / h
    if not (s["min_ratio"] <= ratio <= s["max_ratio"]):
        issues.append(f"aspect {ratio:.3f} outside {s['min_ratio']}-{s['max_ratio']}")
    if w < s["min_w"] or w > s["max_w"]:
        issues.append(f"width {w} outside {s['min_w']}-{s['max_w']}")
    if im.mode not in ("RGB", "RGBA", "P", "L"):
        issues.append(f"unusual colour mode {im.mode}")
    return {"file": p.name, "kind": "image", "network": network, "format": im.format, "size": [w, h], "mb": round(mb, 3), "ok": not issues, "issues": issues}


def probe(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-print_format", "json", "-show_streams", "-show_format", str(path)],
        capture_output=True, text=True, check=True).stdout
    return json.loads(out)


def verify_video(path, network="instagram", reel=True):
    p = pathlib.Path(path)
    s = SPEC[network]["video"]
    info = probe(p)
    v = next((x for x in info["streams"] if x["codec_type"] == "video"), None)
    a = next((x for x in info["streams"] if x["codec_type"] == "audio"), None)
    issues, warns = [], []
    if v is None:
        return {"file": p.name, "kind": "video", "ok": False, "issues": ["no video stream"]}
    w, h = int(v["width"]), int(v["height"])
    num, den = (int(x) for x in v["r_frame_rate"].split("/"))
    fps = num / den
    dur = float(info["format"]["duration"])
    mb = p.stat().st_size / 1e6
    mbps = float(info["format"].get("bit_rate", 0)) / 1e6
    if v["codec_name"] != "h264":
        issues.append(f"codec {v['codec_name']} (need h264)")
    if v.get("pix_fmt") != "yuv420p":
        issues.append(f"pix_fmt {v.get('pix_fmt')} (need yuv420p)")
    if not (s["fps"][0] <= fps <= s["fps"][1]):
        issues.append(f"fps {fps:.1f} outside {s['fps']}")
    if mb > s["max_mb"]:
        issues.append(f"{mb:.1f} MB exceeds {s['max_mb']} MB")
    if mbps > s["max_mbps"]:
        issues.append(f"bitrate {mbps:.1f} Mbps exceeds {s['max_mbps']}")
    lo = s.get("min_s", 1)
    hi = s.get("short_max_s", s.get("max_s", 900)) if network == "youtube" else s.get("max_s", 900)
    if not (lo <= dur <= hi):
        issues.append(f"duration {dur:.1f}s outside {lo}-{hi}")
    if reel and abs(w / h - 0.5625) > 0.01:
        issues.append(f"not 9:16 ({w}x{h})")
    if "max_w" in s and w > s["max_w"]:
        issues.append(f"width {w} > {s['max_w']}")
    if a is None:
        issues.append("no audio track (Facebook expects AAC audio; Reels without sound perform poorly)")
    elif a["codec_name"] != "aac":
        issues.append(f"audio codec {a['codec_name']} (need aac)")
    return {"file": p.name, "kind": "video", "network": network, "size": [w, h], "fps": round(fps, 2), "duration_s": round(dur, 2),
            "mb": round(mb, 3), "mbps": round(mbps, 2), "video": v["codec_name"], "audio": a["codec_name"] if a else None,
            "ok": not issues, "issues": issues, "warnings": warns}


def contact_sheet(video, out_png, cols=4, rows=2, width=270):
    dur = float(probe(video)["format"]["duration"])
    interval = dur / (cols * rows)
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", str(video), "-vf",
         f"fps=1/{interval:.3f},scale={width}:-1,tile={cols}x{rows}", "-frames:v", "1", str(out_png)], check=True)
    return str(out_png)


def loudness(video):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(video), "-af", "ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True)
    lines = [ln for ln in r.stderr.splitlines() if "I:" in ln and "LUFS" in ln]
    return lines[-1].strip() if lines else "n/a"
