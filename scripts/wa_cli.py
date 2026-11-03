#!/usr/bin/env python3
"""West Apadana production CLI.  Run:  python3 -I scripts/wa_cli.py <command> ...   (see docs/BATCH_RUNBOOK.md)

  brand-check                         contrast ratios for approved text/background pairs
  verify <network> <file...>          check images/videos against platform specs (add --not-reel for non-9:16 video)
  contact <video> <out.png>           8-frame contact sheet for visual review
  loudness <video>                    integrated loudness (target about -16 LUFS)
  dup "<text>"                        compare a hook/headline/concept with all previous work
  budget <YYYY-MM>                    Free-plan network-post budget used/remaining for a month
  calendar <YYYY-MM-DD> <kind...>     planned dates per piece (kinds: reel carousel showcase graphic story)
  status                              inventory summary
  payload <piece-id> <network>        Metricool draft payload for a piece
  publish <batch-id> <file...>        copy to media/<batch>/, commit, push, verify remote HEAD
  shots-latest                        newest Framer screenshot files in this sandbox
  shots-ingest <src> <slug> "<title>" <project-id> [breakpoint]
  crops <image> [window_h]            candidate section offsets for screenshot crops/scroll stops
  record-draft <piece> <network> <draft_id> <uuid> [status] [planner_url]
"""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from wa import brand, inventory, payload, publish, shots, verify  # noqa: E402


def main(a):
    if not a:
        print(__doc__)
        return
    cmd, rest = a[0], a[1:]
    if cmd == "brand-check":
        out = brand.check_palette()
    elif cmd == "verify":
        net, files = rest[0], [f for f in rest[1:] if not f.startswith("--")]
        reel = "--not-reel" not in rest
        out = [verify.verify_image(f, net) if f.lower().endswith((".png", ".jpg", ".jpeg")) else verify.verify_video(f, net, reel) for f in files]
    elif cmd == "contact":
        out = verify.contact_sheet(rest[0], rest[1])
    elif cmd == "loudness":
        out = verify.loudness(rest[0])
    elif cmd == "dup":
        out = inventory.check_duplicates(" ".join(rest)) or "no similar previous work"
    elif cmd == "budget":
        out = inventory.monthly_counts(rest[0])
    elif cmd == "calendar":
        out = inventory.plan_calendar(rest[0], rest[1:])
    elif cmd == "status":
        out = inventory.summary()
    elif cmd == "payload":
        inv = inventory.load()
        piece = next(p for b in inv["batches"] for p in b["pieces"] if p["id"] == rest[0])
        target = next(t for t in piece["targets"] if t["network"] == rest[1])
        out = payload.build(piece, target)
    elif cmd == "publish":
        out = publish.publish(rest[1:], rest[0])
    elif cmd == "shots-latest":
        out = shots.latest()
    elif cmd == "shots-ingest":
        out = shots.ingest(rest[0], rest[1], rest[2], rest[3], rest[4] if len(rest) > 4 else "Desktop")
    elif cmd == "crops":
        out = shots.candidate_offsets(rest[0], int(rest[1]) if len(rest) > 1 else 900)
    elif cmd == "record-draft":
        out = inventory.record_draft(*rest[:4], *( [rest[4]] if len(rest) > 4 else []), *([rest[5]] if len(rest) > 5 else []))
    else:
        print(__doc__)
        return
    print(out if isinstance(out, str) else json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main(sys.argv[1:])
