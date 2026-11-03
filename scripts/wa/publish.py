"""Binary-safe media delivery: copy -> hash -> git commit/push -> verify -> GitHub Pages URL.

Integrity proof: sha256(repo copy) == sha256(original) AND `git ls-remote` HEAD == local HEAD. Git is content-addressed, so a
matching remote HEAD means GitHub holds exactly the committed bytes. (Proven byte-exact with fresh clones on 2026-11-03.)
Pages needs ~1-2 minutes to deploy after a push; the Metricool draft call is the real end-to-end test of the public URL.
"""
import datetime as dt
import hashlib
import os
import pathlib
import shutil
import subprocess

from . import brand

ROOT = brand.ROOT
S = brand.load("settings")


def sha256(path):
    return hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()


def git(*args, check=True):
    r = subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True)
    if check and r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {r.stderr.strip()}")
    return r.stdout.strip()


def stage_media(files, batch_id):
    # GitHub Pages' default Jekyll build skips folders starting with "_" or "."; never use them in media paths.
    folder = batch_id.lstrip("_.") or "misc"
    dest = ROOT / S["hosting"]["media_dir"] / folder
    dest.mkdir(parents=True, exist_ok=True)
    recs = []
    for f in files:
        f = pathlib.Path(f)
        d = dest / f.name
        if f.resolve() != d.resolve():
            shutil.copy2(f, d)
        if sha256(f) != sha256(d):
            raise RuntimeError(f"hash mismatch after copy: {f}")
        rel = f"{S['hosting']['media_dir']}/{folder}/{f.name}"
        recs.append({"file": f.name, "path": rel, "sha256": sha256(d), "bytes": d.stat().st_size,
                     "url": S["hosting"]["pages_base_url"] + rel})
    return recs


def commit_push(paths, message, trailer=None):
    trailer = trailer if trailer is not None else os.environ.get("WA_TRAILER", "")
    git("add", *paths)
    if not git("status", "--porcelain", "--", *paths):
        return {"committed": False, "note": "nothing to commit"}
    msg = message + (("\n\n" + trailer) if trailer else "")
    git("-c", "user.name=Claude", "-c", "user.email=noreply@anthropic.com", "commit", "-q", "-m", msg)
    git("fetch", "-q", "origin", "main")
    behind = git("rev-list", "--count", "HEAD..origin/main")
    if behind != "0":
        git("-c", "user.name=Claude", "-c", "user.email=noreply@anthropic.com", "pull", "--rebase", "-q", "origin", "main")
    git("push", "-q", "origin", "main")
    head = git("rev-parse", "HEAD")
    remote = git("ls-remote", "origin", "refs/heads/main").split()[0]
    return {"committed": True, "commit": head, "remote_head": remote, "remote_matches": head == remote}


def publish(files, batch_id, message=None, trailer=None):
    recs = stage_media(files, batch_id)
    res = commit_push([r["path"] for r in recs], message or f"Add media for batch {batch_id}", trailer)
    res["files"] = recs
    wait = S["hosting"]["pages_deploy_wait_seconds"]
    res["pages_ready_after"] = (dt.datetime.now(dt.timezone.utc) + dt.timedelta(seconds=wait)).isoformat(timespec="seconds")
    return res
