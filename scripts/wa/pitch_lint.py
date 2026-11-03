"""Education-first lint (decided 2026-11-03): no promotional endings in content that teaches.

Allowed: saves, shares, questions, an occasional follow invitation.
Not allowed: DM keywords, booking or inquiry requests, offers (CHECK, REBUILD, BRIEF, free review), hire-us language.
Offers live on profiles and the landing page, never in a piece.
"""
import json
import re

from . import brand, inventory

PATTERNS = [
    (r"\bdm\b|\bdirect message\b|\bmessage us\b|\bmessage me\b", "DM / message request"),
    (r"\bbook (a|an|your|now|today)\b|\bbooking (a )?call\b|\bschedule a (call|chat|consult)", "booking request"),
    (r"\bfree (homepage )?(review|audit|assessment|consult\w*|quote|mockup)\b", "free-offer language"),
    (r"\b(get|request) (a|your) (quote|proposal|estimate)\b", "quote request"),
    (r"\b(contact|email|call|hire|work with) (us|me)\b", "contact / hire request"),
    (r"\bsend us\b|\bsend me\b", "send-us request"),
    (r"\b(inquir\w+|enquir\w+) (now|today)\b", "inquiry request"),
    (r"\blink in (the )?bio\b|\blink in my bio\b", "link-in-bio pointer"),
    (r"\bsign up\b|\bsubscribe\b|\bwaitlist\b|\blimited (spots|slots|availability)\b", "sign-up / scarcity"),
    (r"\bwe (can|will) (fix|rebuild|redesign|build) (your|yours)\b", "service pitch"),
    (r"\b(check|rebuild|brief)\b(?=[^.]*\b(offer|keyword|reply|comment)\b)|\bcomment ['\"“]?\w+['\"”]? (below|and)\b", "keyword prompt"),
]
CAMEL = re.compile(r"\b(CHECK|REBUILD|BRIEF)\b")


def lint_text(text):
    hits = []
    low = text.lower()
    for pat, label in PATTERNS:
        for m in re.finditer(pat, low):
            hits.append({"rule": label, "match": text[m.start():m.end()]})
    for m in CAMEL.finditer(text):
        hits.append({"rule": "offer name (CHECK/REBUILD/BRIEF belong on profiles only)", "match": m.group(0)})
    return hits


def lint_calendar(path=None):
    path = path or (brand.ROOT / "content" / "calendar.json")
    cal = json.loads(path.read_text())
    problems, notes = [], []
    pcs = cal["pieces"]
    for p in pcs:
        for f in ("title", "hook", "takeaway"):
            for h in lint_text(p[f]):
                problems.append(f"piece {p['n']} {f}: {h['rule']}: '{h['match']}'")
        if p["ground"] not in cal["grounds"]:
            problems.append(f"piece {p['n']}: unknown ground {p['ground']}")
        if not p.get("evidence", {}).get("needs"):
            problems.append(f"piece {p['n']}: no evidence requirements")
        if p["evidence"]["tier"] not in cal["evidence_tiers"]:
            problems.append(f"piece {p['n']}: unknown evidence tier")
    mix = {}
    for p in pcs:
        mix[p["ground"]] = mix.get(p["ground"], 0) + 1
    month = {}
    for p in pcs:
        m = p["date"][:7]
        month[m] = month.get(m, 0) + len(p["networks"])
    cap = inventory.CAP
    for m, n in month.items():
        if n > cap - 2:
            problems.append(f"{m}: {n} network-posts exceeds cap {cap} minus 2 reserve")
    notes.append(f"mix: {mix}; planned test mix: {cal['test_mix']}")
    notes.append(f"network-posts per month: {month} (Free cap {cap}, reserve 2)")
    dates = [p["date"] for p in pcs]
    if len(set(dates)) != len(dates):
        problems.append("duplicate dates")
    dups = []
    for p in pcs:
        if p["n"] <= 3:
            continue  # built samples are already in history
        for f in ("hook", "title"):
            for h in inventory.check_duplicates(p[f]):
                dups.append(f"piece {p['n']} {f} ~ {h['piece']} ({h['similarity']})")
    cross = []
    from itertools import combinations
    for a, b in combinations(pcs, 2):
        for f in ("hook", "title"):
            s = inventory.similarity(a[f], b[f])
            if s >= 0.5:
                cross.append(f"pieces {a['n']} and {b['n']} {f} similarity {round(s,2)}")
    problems += [f"duplicate vs history: {d}" for d in dups] + [f"duplicate within calendar: {c}" for c in cross]
    return {"problems": problems, "notes": notes, "ok": not problems}


def lint_pieces():
    """Lint each built piece's CTA field and the closing paragraph of every caption.
    Example copy inside slides for invented businesses (e.g. 'Book a repair' for a made-up bike shop) is exempt: it is the lesson, not our pitch."""
    out = {}
    for f in sorted((brand.ROOT / "content" / "pieces").glob("*.json")):
        d = json.loads(f.read_text())
        hits = []
        for net, text in (d.get("cta") or {}).items():
            hits += [{"where": f"cta.{net}", **h} for h in lint_text(text)]
        for net, cap in (d.get("captions") or {}).items():
            tail = cap.strip().split("\n\n")[-1]
            hits += [{"where": f"caption.{net} (last paragraph)", **h} for h in lint_text(tail)]
        out[d["id"]] = hits or "clean"
    return out


def render_calendar():
    """Write docs/CALENDAR.md from content/calendar.json (generated; edit the JSON)."""
    cal = json.loads((brand.ROOT / "content" / "calendar.json").read_text())
    import datetime as dt
    o = ["# 20-piece content calendar (revision 4, PROPOSED)", "",
         "> GENERATED from `content/calendar.json` by `wa_cli.py calendar-render`. Edit the JSON, not this file.",
         "> Status: " + cal["status"], "",
         "Window: %s. Initial test mix %s education / %s demonstration / %s story (a hypothesis, not a limit)." % (cal["window"], cal["test_mix"]["education"], cal["test_mix"]["demonstration"], cal["test_mix"]["story"]),
         "Voiceover: " + cal["voiceover"], "",
         "| # | Date | Series | Title | Format | Ground | Networks |", "|---|---|---|---|---|---|---|"]
    for p in cal["pieces"]:
        d = dt.date.fromisoformat(p["date"]).strftime("%a %d %b")
        o.append("| %d | %s | %s | %s | %s | %s | %s |" % (p["n"], d, p["series"], p["title"], p["format"], p["ground"], ", ".join(p["networks"])))
    o += ["", "## Briefs", ""]
    for p in cal["pieces"]:
        o += ["### %d. %s" % (p["n"], p["title"]), "",
              "- **Ground / area:** %s / %s" % (p["ground"], p["area"]),
              "- **Hook:** %s" % p["hook"], "- **Takeaway:** %s" % p["takeaway"],
              "- **Evidence tier:** %s" % p["evidence"]["tier"]]
        o += ["- **Evidence needed:** " + n for n in p["evidence"]["needs"]]
        if p.get("was"): o.append("- **Replaces:** " + p["was"])
        if p.get("status"): o.append("- **Status:** " + p["status"])
        if p.get("notes"): o.append("- **Notes:** " + p["notes"])
        o.append("")
    (brand.ROOT / "docs" / "CALENDAR.md").write_text("\n".join(o) + "\n")
    return "wrote docs/CALENDAR.md"
