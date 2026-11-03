#!/usr/bin/env python3
"""Social Identity Kit tool.

  python3 -I scripts/social_kit.py check    # verify every option fits its limit and passes the honesty lint
  python3 -I scripts/social_kit.py render   # regenerate docs/social-identity/platforms/*.md and recommended-set.md

Source of truth: docs/social-identity/kit.json. The .md files under docs/social-identity/platforms/ are GENERATED; edit kit.json instead.
"""
import json, re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
DIR = ROOT / "docs" / "social-identity"
KIT = DIR / "kit.json"

# option field -> limit key (per platform)
FIELDS = {
    "instagram": {"display_name": "display_name", "bio": "bio"},
    "threads": {"display_name": "display_name", "bio": "bio"},
    "facebook": {"page_name": "page_name", "intro": "intro", "description": "description"},
    "x": {"display_name": "display_name", "bio": "bio"},
    "linkedin_company": {"name": "name", "tagline": "tagline", "about": "about"},
    "linkedin_founder": {"headline": "headline", "about": "about"},
    "youtube": {"channel_name": "channel_name", "description": "description"},
}
LABELS = {"display_name": "Display name", "bio": "Bio", "page_name": "Page name", "intro": "Intro (short)",
          "description": "Description", "name": "Company name", "tagline": "Tagline", "about": "About",
          "headline": "Headline", "channel_name": "Channel name"}

BANNED = [
    (r"!", "exclamation mark"),
    (r"\b(unlock|game[- ]?changer|elevate your|supercharge|skyrocket|cutting[- ]edge|world[- ]class)\b", "banned marketing phrase"),
    (r"\b(award|awards|award-winning|certified|trusted by|years of experience|since 20\d\d|#1|best in)\b", "unsourced credential"),
    (r"\bwithin \d+|\b24[ /-]?7\b|\b\d+ hours?\b|same[- ]day reply", "response-time promise"),
    (r"\bguarantee[sd]?\b|\bdouble your\b|\b\d+x\b|\bmore leads\b|\bmore sales\b", "outcome promise"),
    (r"\bagency\b|\bour team\b|\bteam of\b", "team/agency claim"),
]

OFFER = re.compile(r"free (homepage )?(review|assessment|audit)|website improvement assessment|project conversation|\b(CHECK|REBUILD|BRIEF)\b|message us|dm us", re.I)
SHORT_FIELDS = {"display_name", "page_name", "bio", "intro", "tagline", "headline", "channel_name", "name"}

def offer_rules(pk, plat, field, text):
    """Education-first identity rule (owner decision 2026-11-03): offers are never the main message."""
    out = []
    if field in SHORT_FIELDS and OFFER.search(text):
        out.append("offer in a short field (offers belong on the link page or in long About text, after the first paragraph)")
    if field in ("description", "about") and OFFER.search(text[:200]):
        out.append("offer within the first 200 characters of a long field")
    return out

def load():
    return json.load(open(KIT, encoding="utf-8"))

def lint(text):
    problems = []
    for rx, why in BANNED:
        if re.search(rx, text, re.I):
            problems.append(why)
    t = re.sub(r"(not|than)\s+client work", "", text, flags=re.I)
    if re.search(r"\bclients?\b|testimonial", t, re.I):
        problems.append("client/testimonial wording (concept work must be labeled 'not client work')")
    if re.search(r"[\U0001F300-\U0001FAFF☀-➿]", text):
        problems.append("emoji")
    return problems

def check(kit):
    bad = 0
    rows = []
    for pk, plat in kit["platforms"].items():
        lims = kit["limits"][pk]
        for ok, opt in plat["options"].items():
            for field, lk in FIELDS[pk].items():
                text = opt[field]
                n = len(text)
                limit = lims[lk][0]
                status = "ok" if n <= limit else "OVER"
                probs = lint(text) + offer_rules(pk, plat, field, text)
                if ok == plat["recommended"] and field in ("bio", "intro", "tagline", "headline", "description"):
                    pass
                if status != "ok" or probs:
                    bad += 1
                rows.append((pk, ok, field, n, limit, status, "; ".join(probs)))
        rec = plat["options"][plat["recommended"]]
        joined = " ".join(str(v) for k, v in rec.items() if k != "label")
        if not re.search(r"premium website", joined, re.I):
            print("RECOMMENDED OPTION of", pk, "never says West Apadana builds premium websites")
            bad += 1
        la = plat.get("long_about")
        if la:
            probs = lint(la)
            rows.append((pk, "-", "long_about", len(la), "n/a", "ok" if not probs else "LINT", "; ".join(probs)))
            if probs: bad += 1
    for r in rows:
        print("%-17s %-2s %-12s %5d / %-5s %-5s %s" % r)
    print("\nPROBLEMS: %d" % bad)
    return bad

def render(kit):
    pdir = DIR / "platforms"
    pdir.mkdir(parents=True, exist_ok=True)
    banner = "> GENERATED from `docs/social-identity/kit.json` by `scripts/social_kit.py render`. Edit the JSON, not this file.\n> Status: %s\n" % kit["status"]
    rec_rows = []
    for pk, plat in kit["platforms"].items():
        lims = kit["limits"][pk]
        o = []
        o.append("# %s\n" % plat["title"])
        o.append(banner)
        o.append("**Purpose.** %s\n" % plat["purpose"])
        o.append("**Recommended option: %s (%s).** %s\n" % (plat["recommended"], plat["options"][plat["recommended"]]["label"], plat["why"]))
        o.append("## Character limits used\n")
        o.append("| Field | Limit | Confidence |\n|---|---|---|")
        for k, (n, src) in lims.items():
            o.append("| %s | %d | %s |" % (LABELS.get(k, k), n, src))
        o.append("\nEvery option below is written to fit the limit. Verify each limit in the live editor at implementation time; where sources disagreed the lower figure was used.\n")
        for ok, opt in plat["options"].items():
            star = "  (RECOMMENDED)" if ok == plat["recommended"] else ""
            o.append("## Option %s: %s%s\n" % (ok, opt["label"], star))
            for field in FIELDS[pk]:
                text = opt[field]
                o.append("**%s** (%d / %d)\n" % (LABELS[field], len(text), lims[FIELDS[pk][field]][0]))
                o.append("```\n%s\n```\n" % text)
        if plat.get("long_about"):
            o.append("## Long About / Overview (all options)\n")
            o.append("Length %d. Facebook's long-form field limit was not verified; this is well under every figure seen.\n" % len(plat["long_about"]))
            o.append("```\n%s\n```\n" % plat["long_about"])
        if plat.get("specialties"):
            o.append("## Specialties\n\n" + ", ".join(plat["specialties"]) + "\n")
        o.append("## Keywords\n\n" + ", ".join(plat["keywords"]) + "\n\n" + plat["keyword_placement"] + "\n")
        o.append("## Call to action\n\n" + plat["cta"] + "\n")
        o.append("## Link strategy\n\n" + plat["link_strategy"] + "\n")
        for l in plat["links"]:
            o.append("- " + l)
        if plat.get("category_label"):
            o.append("\n**Category.** " + plat["category_label"] + "\n")
        o.append("\n## Profile photo\n\n" + plat["photo"] + "\n")
        o.append("## Banner / cover\n\n" + plat["banner"] + "\n")
        o.append("## Also on this platform\n")
        for e in plat["extras"]:
            o.append("- " + e)
        (pdir / (pk.replace("_", "-") + ".md")).write_text("\n".join(o) + "\n", encoding="utf-8")
        rec = plat["options"][plat["recommended"]]
        rec_rows.append((plat, rec))
    # recommended set
    o = ["# Recommended set\n", banner,
         "One cohesive set, tuned to what each platform is for. Voice is the same everywhere: confident, precise, warm, no exclamation marks, no emoji. "
         "The same ideas recur, in this order, so a visitor who meets us on two platforms recognizes us: lessons that can be used the same day, premium websites and digital experiences, concept work that is always labeled, and only then the optional ways to start (never in a short bio). The logo is the existing approved West Apadana logo, currently a missing asset: no mark has been invented.\n"]
    for plat, rec in rec_rows:
        pk = [k for k, v in kit["platforms"].items() if v is plat][0]
        o.append("## %s: option %s (%s)\n" % (plat["title"], plat["recommended"], rec["label"]))
        for field in FIELDS[pk]:
            t = rec[field]
            o.append("**%s** (%d / %d)\n\n```\n%s\n```\n" % (LABELS[field], len(t), kit["limits"][pk][FIELDS[pk][field]][0], t))
        o.append("Why: %s\n" % plat["why"])
    (DIR / "recommended-set.md").write_text("\n".join(o) + "\n", encoding="utf-8")
    print("rendered", len(rec_rows), "platforms")

if __name__ == "__main__":
    kit = load()
    cmd = sys.argv[1] if len(sys.argv) > 1 else "check"
    if cmd == "check":
        sys.exit(1 if check(kit) else 0)
    elif cmd == "render":
        if check(kit):
            sys.exit("fix problems before rendering")
        render(kit)
    else:
        sys.exit(__doc__)
