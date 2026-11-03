"""Build and validate Metricool createScheduledPost payloads from an inventory piece (the MCP call itself is made by Claude).

Output is {"blogId", "date", "info"}: pass `date` and `blogId` as the tool arguments and `info` (JSON string) as `info`.
Drafts: draft=true, autoPublish=false. The tool requires a date even for drafts, so we use the real planned publish date.
"""
import json

from . import brand

S = brand.load("settings")
P = brand.load("platforms")["networks"]


def compose_text(piece, network):
    text = piece["captions"][network].strip()
    cta = piece.get("cta", {}).get(network, "").strip()
    tags = piece.get("hashtags", {}).get(network, [])
    if cta:
        text += "\n\n" + cta
    if tags:
        text += "\n\n" + " ".join(tags)
    return text


def validate(piece, network, text, media):
    errs = []
    spec = P[network]
    limit = spec.get("caption_max") or spec.get("description_max")
    if limit and len(text) > limit:
        errs.append(f"{network} text {len(text)} chars > {limit}")
    tags = piece.get("hashtags", {}).get(network, [])
    if network == "instagram" and len(tags) > spec["hashtags_max"]:
        errs.append(f"too many hashtags ({len(tags)})")
    if network == "instagram" and len(media) > spec["carousel_max"]:
        errs.append(f"carousel has {len(media)} items > {spec['carousel_max']}")
    if piece["format"] == "reel" and network == "youtube" and not piece.get("titles", {}).get("youtube"):
        errs.append("youtube needs titles.youtube")
    if not media:
        errs.append("no media urls")
    return errs


def build(piece, target, blog_id=None):
    net = target["network"]
    media = [f["url"] for f in piece["files"] if f.get("role", "media") == "media"]
    text = compose_text(piece, net)
    errs = validate(piece, net, text, media)
    if errs:
        raise ValueError("; ".join(errs))
    local = target["date"]  # e.g. 2026-11-09T12:00:00-05:00
    info = {
        "autoPublish": False, "descendants": [], "draft": True,
        "firstCommentText": piece.get("first_comment", {}).get(net, ""), "hasNotReadNotes": False,
        "media": media, "mediaAltText": piece.get("alt", []),
        "providers": [{"network": net}],
        "publicationDate": {"dateTime": local[:19], "timezone": S["metricool"]["timezone"]},
        "shortener": False, "smartLinkData": {"ids": []}, "text": text,
    }
    reel = piece["format"] == "reel"
    if net == "instagram":
        info["instagramData"] = {"type": "REEL" if reel else "POST", "collaborators": [], "carouselTags": {}, "showReelOnFeed": True}
    elif net == "facebook":
        info["facebookData"] = {"type": "REEL" if reel else "POST"}
        if reel:
            info["facebookData"]["title"] = piece.get("titles", {}).get("facebook", piece.get("headline", ""))[:100]
    elif net == "threads":
        info["threadsData"] = {}
    elif net == "youtube":
        info["youtubeData"] = {"title": piece["titles"]["youtube"][:100], "type": "short", "privacy": "public", "tags": [],
                               "madeForKids": False, "isAiGeneratedContent": False}
    return {"blogId": blog_id or S["metricool"]["blogId"], "date": local, "info": json.dumps(info, ensure_ascii=False)}
