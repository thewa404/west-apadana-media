# West Apadana: social content production system

West Apadana is an independent digital design studio (premium websites and digital experiences). This repo is its production
system: templates, scripts, config, bundled fonts, content inventory and creative history, plus the public media host
(GitHub Pages: https://thewa404.github.io/west-apadana-media/).

## Trigger
When the user says "Claude, create a new batch" (or anything similar), follow `docs/BATCH_RUNBOOK.md` start to finish. Do not
rebuild tooling. Use `scripts/wa_cli.py`, `scripts/build_batch.py` and `scripts/wa/*`. Brand, voice and format rules are in
`docs/CREATIVE_SYSTEM.md`. What is proven vs untested is in `docs/PIPELINE_STATUS.md`: read it first and do not claim more than it says.

## Hard rules
1. NEVER publish or schedule a Metricool post without the user's explicit approval of that specific batch. Create drafts only
   (`draft: true`, `autoPublish: false`).
2. NEVER claim an integration works until it was tested. Record every test result in `docs/PIPELINE_STATUS.md`.
3. Honesty: no fake testimonials, invented client results, made-up statistics or fabricated screenshots. Showcases use real
   Framer screenshots of the user's own projects, labelled "Concept project, not client work" unless the user says a project is paid client work.
4. NEVER silently substitute static images for requested video. If a video cannot be produced, stop and report.
5. No duplicate posts: check `wa_cli.py status` and Metricool `getScheduledPosts` before creating drafts; run `wa_cli.py dup` on every hook, headline and concept.
6. Metricool Free allows 20 published network-posts per calendar month, counted per network. Run `wa_cli.py budget <YYYY-MM>`.
7. The user does no manual file handling. Media path: sandbox file -> `git push` -> GitHub Pages URL -> Metricool draft.
8. Every file passes `wa_cli.py verify` AND is looked at (Read the image or contact sheet) before it is published.
9. The repo is public. No tokens, passwords or private client data. Unpublished captions in `inventory/` are public.
10. Report failures accurately and name the smallest fix.

## Environment facts (verified 2026-11-03)
- Python via `python3 -I`; Playwright/Chromium, ffmpeg (libx264, aac), Jinja2, numpy, PIL are installed. Fonts are bundled in `fonts/`.
- Brand display font: Inter Display (stand-in for Neue Haas Grotesk, which is commercial and not installed). Body: DM Sans.
- Shell and WebFetch cannot reach github.io, static.metricool.com or most other hosts (network allowlist). Do not try to work around it.
  A successful Metricool draft (media re-hosted on static.metricool.com) is the proof a Pages URL is publicly fetchable.
- GitHub Pages deploys 1-2 minutes after a push. Never put media in folders starting with `_` or `.`.
- Repo write access: call `add_repo` for `thewa404/west-apadana-media` with `access: push`, clone once with a generous timeout, then `register_repo_root`.
  Export `WA_TRAILER` with the commit attribution lines the session provides so `publish.py` appends them.
- Framer: `open_project`, then `exec` with `api.tree.screenshot(<breakpoint id>)`. It is read-only and the image also lands as a file under
  `/tmp/claude-tool-results/`. Ingest with `wa_cli.py shots-ingest`. The Framer projects are currently unpublished concept sites.
- Metricool MCP: no delete tool (the user deletes test drafts in the planner), no upload tool (public URLs only), one caption per post
  (one post per network), a date is required even for drafts, updates change the post `id` but keep the `uuid`.
- Metricool tools load via ToolSearch (`select:` the names). Brand `blogId` 6728476, timezone America/New_York, networks: instagram, facebook, threads, youtube.
