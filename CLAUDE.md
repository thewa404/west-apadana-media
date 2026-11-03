# West Apadana: social content production system

West Apadana is an independent digital design studio (premium websites and digital experiences). This repo is its production
system: templates, scripts, config, bundled fonts, content inventory and creative history, plus the public media host
(GitHub Pages: https://thewa404.github.io/west-apadana-media/).

## Trigger
When the user says "Claude, create a new batch" (or anything similar), follow `docs/BATCH_RUNBOOK.md` start to finish. Do not
rebuild tooling. Use `scripts/wa_cli.py`, `scripts/build_batch.py` and `scripts/wa/*`. Brand, voice and format rules are in
`docs/CREATIVE_SYSTEM.md`. What is proven vs untested is in `docs/PIPELINE_STATUS.md`: read it first and do not claim more than it says.

## Content principles (permanent, owner decision 2026-11-03)
1. **Education first.** West Apadana teaches, faceless, in the general spirit of educational personal brands (a reference for philosophy, never for scripts, personality or branding). Topics: websites, marketing, branding, customer acquisition, conversion, AI tools, automation, business growth. Original insight, not generic advice. Strong hook in the first 1-2 seconds, anyone can follow it, a viewer can act on it.
2. **Starting mix 70/20/10** (education / creative demonstrations and portfolio / brand storytelling). It is a test hypothesis, NOT a limit. The first 20-piece test is 14 / 4 / 2. Adjust on real performance data. Every piece carries a `ground` field (education, demonstration, story). The old growth / authority / lead taxonomy is retired.
3. **No pitch inside a piece.** Educational pieces teach and then end naturally. No promotional endings, no DM keywords, no booking or inquiry requests, no offers. Saves, shares, genuine questions and an occasional follow invitation are fine. Run `wa_cli.py pitch-lint` on every caption ending and `pitch-lint-pieces` / `calendar-check` before approval packages.
4. **Offers live on profiles and the landing page only.** CHECK, REBUILD and BRIEF are optional offers reachable from bios, the link destination or a landing page. They never close an educational video or carousel. Free homepage reviews are not the main message of any profile.
5. **Real third-party sites may be analysed for education** only when the example is publicly accessible, every claim is verifiable by the viewer, the analysis is fair and the source is shown (URL, capture date). Never invent performance data, never imply a company hired us or knows us, no traffic/conversion/revenue claims about a site we do not run. Each piece records its evidence requirement (`content/calendar.json`).
6. **Voice.** Reels are voiceless (captions plus original sound design) unless the owner approves a voice after listening to the test in `docs/PIPELINE_STATUS.md`. An AI voice is used only if it sounds convincing, natural and right for the brand, and is then disclosed with the posting tool's AI flags.
7. **Volume is not capped at 20 a month.** 20 pieces is the first test. Metricool Starter is under consideration (owner decision pending; no subscription without approval). On the Free plan keep at least 2 published-post slots a month in reserve (plan uses 18).
8. **Test posts are not campaign posts.** The disposable posts in the Metricool planner are pipeline tests (see `docs/PIPELINE_STATUS.md`). Never reuse or count them as content.
9. The three sample pieces (`media/samples-s1/`) are NOT approved for full production until the owner has reviewed the actual files and the reel audio.

## Hard rules
1. NEVER publish or schedule a Metricool post without the user's explicit approval of that specific batch. Create drafts only
   (`draft: true`, `autoPublish: false`). The approval request must also state the delivery mode (manual push notification vs automatic).
2. NEVER claim an integration works until it was tested. Record every test result in `docs/PIPELINE_STATUS.md`.
3. Honesty: no fake testimonials, invented client results, made-up statistics or fabricated screenshots. ALL of the user's Framer portfolio sites are
   concept/demo projects (owner confirmed 2026-11-03; registry in `assets/portfolio.json`). They may be used in West Apadana's marketing, are labelled
   "Concept project, not client work", and must NEVER be implied to have been commissioned by real clients. Projects flagged `review_needed` need the owner's OK before featuring.
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
- Scheduling (verified 2026-11-03): `updateScheduledPost` with `draft: false` turns a draft into a scheduled post. Send back every field exactly as `getScheduledPosts` returned it,
  including the Metricool-hosted media URLs (no re-ingestion). Provider status stays "Pending" for drafts and scheduled posts alike; `draft: false` is the flag. The `id` changes on every update, the `uuid` does not.
  `autoPublish: false` = manual delivery (push notification). `autoPublish: true` = automatic API publishing and is UNTESTED: the first real approved post must be monitored.
- Metricool tools load via ToolSearch (`select:` the names). Brand `blogId` 6728476, timezone America/New_York, networks: instagram, facebook, threads, youtube.
