"""Frame-exact video rendering: an HTML page exposes window.setT(t); we screenshot each frame and encode."""
import pathlib
import shutil
import subprocess
import tempfile

from . import audio, render


def render_reel(r, template, ctx, out_mp4, duration, fps=30, size=(1080, 1920), score=None, keep=False, crf=20):
    """r: render.Renderer. score: dict of audio.synth kwargs (None = silent, NOT recommended for FB/Reels)."""
    out_mp4 = pathlib.Path(out_mp4)
    out_mp4.parent.mkdir(parents=True, exist_ok=True)
    work = pathlib.Path(tempfile.mkdtemp(prefix="reel_"))
    html = render.env.get_template(template).render(**render.context({**ctx, "duration": duration}, size))
    hp = work / "reel.html"
    hp.write_text(html)
    pg = r.page(size)
    n = int(round(duration * fps))
    try:
        pg.goto(f"file://{hp}")
        pg.evaluate("window.__ready || document.fonts.ready")
        pg.wait_for_timeout(200)
        for i in range(n):
            pg.evaluate("t => window.setT(t)", i / fps)
            pg.screenshot(path=str(work / f"f_{i:05d}.jpg"), type="jpeg", quality=92)
    finally:
        pg.close()
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(fps), "-i", str(work / "f_%05d.jpg")]
    wav = None
    if score is not None:
        wav = work / "score.wav"
        score = dict(score)
        engine = score.pop("engine", "ambient")
        (audio.strike_score if engine == "strike" else audio.synth)(duration, wav, **score)
        cmd += ["-i", str(wav)]
    cmd += ["-c:v", "libx264", "-preset", "veryfast", "-crf", str(crf), "-pix_fmt", "yuv420p", "-r", str(fps)]
    if wav:
        cmd += ["-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-c:a", "aac", "-b:a", "128k", "-ar", "44100", "-ac", "2", "-shortest"]
    cmd += ["-movflags", "+faststart", str(out_mp4)]
    subprocess.run(cmd, check=True)
    if not keep:
        shutil.rmtree(work, ignore_errors=True)
    return str(out_mp4)
