"""Content inventory, creative history (anti-repetition) and Free-plan posting budget."""
import datetime as dt
import json
import re
import zoneinfo

from . import brand

ROOT = brand.ROOT
INV = ROOT / "inventory" / "inventory.json"
HIST = ROOT / "inventory" / "history.json"
S = brand.load("settings")
CAP = brand.load("platforms")["free_plan"]["monthly_publish_cap"]
TZ = zoneinfo.ZoneInfo(S["metricool"]["timezone"])
STOP = set("the a an and or of to in on for with your you our is are it this that be as at by from we".split())


def _load(p, default):
    return json.loads(p.read_text()) if p.exists() else default


def _save(p, obj):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def load():
    return _load(INV, {"version": 1, "batches": []})


def save(inv):
    _save(INV, inv)


def history():
    return _load(HIST, {"entries": []})


def tokens(s):
    return {t for t in re.findall(r"[a-z0-9']+", s.lower()) if t not in STOP}


def similarity(a, b):
    ta, tb = tokens(a), tokens(b)
    return len(ta & tb) / max(1, len(ta | tb))


def check_duplicates(text, threshold=0.5):
    """Compare a proposed hook/headline/concept with everything already made. Returns hits (empty list = fresh)."""
    hits = []
    for e in history()["entries"]:
        for field in ("hook", "headline", "concept"):
            if e.get(field):
                s = similarity(text, e[field])
                if s >= threshold:
                    hits.append({"similarity": round(s, 2), "field": field, "batch": e["batch"], "piece": e["piece"], "text": e[field]})
    return sorted(hits, key=lambda h: -h["similarity"])


def log_history(batch_id, piece):
    h = history()
    h["entries"].append({
        "batch": batch_id, "piece": piece["id"], "format": piece["format"], "concept": piece.get("concept", ""),
        "hook": piece.get("hook", ""), "headline": piece.get("headline", ""), "theme": piece.get("theme", ""),
        "layout": piece.get("layout", ""), "source": piece.get("source", ""),
        "logged": dt.datetime.now(TZ).isoformat(timespec="seconds"),
    })
    _save(HIST, h)


def monthly_counts(month):
    """Network-posts planned/scheduled/published for a calendar month (YYYY-MM). Test batches (id starting '_') are ignored."""
    counts = {}
    for b in load()["batches"]:
        if b["id"].startswith("_"):
            continue
        for p in b["pieces"]:
            for t in p.get("targets", []):
                if t["date"][:7] == month and t.get("status") in ("planned", "draft", "scheduled", "published"):
                    counts[t["network"]] = counts.get(t["network"], 0) + 1
    total = sum(counts.values())
    return {"month": month, "by_network": counts, "total": total, "cap": CAP, "remaining": CAP - total}


def plan_calendar(start_date, kinds):
    """First post on start_date, then every days_between_pieces. Returns per-piece targets with local ISO datetimes."""
    d0 = dt.date.fromisoformat(start_date)
    out = []
    for i, kind in enumerate(kinds):
        day = d0 + dt.timedelta(days=i * S["schedule"]["days_between_pieces"])
        targets = []
        for net in S["allocation"][kind]:
            hh, mm = S["schedule"]["posting_slots"][net].split(":")
            local = dt.datetime.combine(day, dt.time(int(hh), int(mm)), tzinfo=TZ)
            targets.append({"network": net, "date": local.isoformat(timespec="seconds"), "status": "planned"})
        out.append({"kind": kind, "targets": targets})
    month_totals = {}
    for p in out:
        for t in p["targets"]:
            month_totals[t["date"][:7]] = month_totals.get(t["date"][:7], 0) + 1
    return {"pieces": out, "per_month_network_posts": month_totals, "cap": CAP}


def summary():
    inv = load()
    rows = []
    for b in inv["batches"]:
        st = {}
        for p in b["pieces"]:
            for t in p.get("targets", []):
                st[t.get("status", "?")] = st.get(t.get("status", "?"), 0) + 1
        rows.append({"batch": b["id"], "pieces": len(b["pieces"]), "target_status": st, "note": b.get("note", "")})
    return rows


def record_draft(piece_id, network, draft_id, uuid, status="draft", planner_url=None):
    """Store the Metricool id/uuid (ids change on every update; uuid is stable) and status for a piece's network target."""
    inv = load()
    for b in inv["batches"]:
        for piece in b["pieces"]:
            if piece["id"] == piece_id:
                for t in piece["targets"]:
                    if t["network"] == network:
                        t.update({"draft_id": str(draft_id), "uuid": str(uuid), "status": status})
                        if planner_url:
                            t["planner_url"] = planner_url
                        save(inv)
                        return t
    raise KeyError(f"{piece_id}/{network} not found")
