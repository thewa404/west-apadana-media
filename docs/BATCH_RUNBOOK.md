# Batch runbook: "Claude, create a new batch"

Default batch = 10 pieces: 2 cinematic reels, 3 educational carousels, 2 website showcases, 2 bold graphics, 1 brand-story post (a storytelling carousel for the feed at 4:5, not an Instagram Story)
(`config/settings.json -> batch_default`). Default network allocation = exactly 20 network-posts (the Free monthly cap):
reels -> Instagram + YouTube Shorts; carousels, showcases, graphics -> Instagram + Facebook; story -> Instagram + Threads.

## 0. Session setup (once per session)
1. `add_repo thewa404/west-apadana-media access=push`; clone to `/home/claude/west-apadana-media` (one clone, timeout ~10 min); `register_repo_root`.
2. Load tools with ToolSearch: Metricool (`getBrandSettings`, `getScheduledPosts`, `createScheduledPost`, `updateScheduledPost`) and Framer (`open_project`, `exec`).
3. `export WA_TRAILER="<commit attribution lines from the session>"`.
4. Read `docs/PIPELINE_STATUS.md`. Anything marked UNTESTED must not be relied on without testing first (ask before test drafts).

## 1. Plan
1. `python3 -I scripts/wa_cli.py status` and `budget <YYYY-MM>` for each month the batch will touch. Fetch Metricool `getScheduledPosts` to see what is already queued.
2. Choose the start date (default: next free slot, every 3 days) with `wa_cli.py calendar <start> <kinds...>`. Per-month totals must stay <= remaining budget.
3. Write 10 fresh concepts. For each hook, headline and concept run `wa_cli.py dup "<text>"`. Rewrite anything that is similar to history.
   Rotate themes (obsidian, navy, graphite, ivory), layouts and sources versus the last batch (`inventory/history.json`).

## 2. Source material
- Showcases/walkthroughs: pick from `assets/portfolio.json` (all are concept/demo projects; skip any `review_needed` project until the owner approves it). Pick projects not featured in the last batch (`assets/screenshots/index.json` + history `source`).
  `open_project <id>` then `exec`: `const bp=api.tree.get(<page id>).children[0]; return await api.tree.screenshot(bp.id)` (add a Phone breakpoint when it exists).
  `wa_cli.py shots-ingest <file> <slug> "<title>" <project-id> [breakpoint]`; `wa_cli.py crops <file>` suggests section offsets.
- Everything else is rendered from templates (`templates/`): `slide.html.j2` (statement, cover, point, compare, story, cta), `showcase.html.j2`, `reel.html.j2`.

## 3. Build
1. Write `/home/claude/out/<batch>/spec.json` (format in `scripts/build_batch.py`). Captions per platform, hashtags (Instagram 3-8, Facebook 0-3, Threads 0-1),
   subtle CTA, YouTube title, alt text. Use `fmt: "jpeg"` for slides (PNG with grain is 1.5 MB per slide).
2. `python3 -I scripts/build_batch.py build <spec.json>` renders, verifies against `config/platforms.json`, writes review sheets and the inventory.
3. LOOK at the review sheet and at each reel contact sheet (`Read`). Check readability, cropping, overlaps, brand colors, honesty labels. Fix the spec and rebuild. Do not publish unreviewed media.

## 4. Deliver media
`python3 -I scripts/build_batch.py publish <batch_id>`: one commit, `remote_matches: true`, Pages URLs recorded in `inventory/`. Wait until `pages_ready_after` (about 2 minutes).

## 5. Drafts (never scheduled)
1. `python3 -I scripts/build_batch.py payloads <batch_id>` writes one payload per piece/network.
2. For each payload call `createScheduledPost` (`blogId`, `date`, `info` from the file). Draft, `autoPublish: false`, real planned date.
   If media ingestion fails right after a push, wait for Pages and retry ONCE after checking `getScheduledPosts` for duplicates.
3. `wa_cli.py record-draft <piece> <network> <id> <uuid>` for every draft.
4. Read back with `getScheduledPosts` (range covering the batch): verify count, caption text, media URLs now on `static.metricool.com`, media count/order, provider, type (REEL/POST), `draft: true`, `autoPublish: false`.
   Any mismatch is a failure: report it, do not paper over it.

## 6. Approval package
Reply with: the review sheet, a table (piece, format, networks, date/time, caption preview, draft planner link), per-month budget use, anything unverified, and the exact approval sentence the user must reply with.
State the delivery mode being requested: **manual** (`autoPublish: false`, Metricool sends a push notification at the scheduled time) or **automatic** (`autoPublish: true`, Metricool publishes through the API).
Automatic publishing has never been run end to end; say so and offer manual delivery for the first batch. Wait. No approval means no scheduling.

## 7. After approval (flip verified 2026-11-03)
1. Only for the pieces the user approved. Call `getScheduledPosts` first and take every field of each draft exactly as returned (media URLs are already on static.metricool.com).
2. `updateScheduledPost` with the same `id`, `uuid`, `blogId` and the full `info`, changing ONLY `draft: false` (and `autoPublish: true` only if the user approved automatic delivery).
   Do not edit captions or dates in this step. If something must change, tell the user and get approval first.
3. Read back with `getScheduledPosts`: confirm `draft: false`, the `autoPublish` value that was approved, unchanged text, date, media count and provider. Provider status shows "Pending" for drafts and scheduled posts alike, so `draft: false` is the evidence.
4. The `id` changes on every update: `wa_cli.py record-draft <piece> <network> <new id> <uuid> scheduled`, then commit `inventory/` and `inventory/history.json`.
5. Never modify posts that were not part of the approved batch. Report any mismatch immediately; there is no delete tool, so a wrong scheduled post must be removed by the user in the planner.
6. The first real automatic publish is untested: tell the user, and check the planner/analytics after the first post time.

## Failure table
| Symptom | Likely cause | Fix |
|---|---|---|
| `Failed to normalize media` | Pages not deployed yet, or folder starting with `_` | wait 2 min; never use underscore folders; check `.nojekyll` is committed |
| remote HEAD mismatch | push raced/failed | `git fetch && git status`; re-run publish |
| fonts_ok false | font file missing | check `fonts/` vs `config/brand.json` |
| verify issue "no audio" | silent video | pass `score` in the reel spec |
| clone 429 | concurrent git operations | wait 5 s, retry once |

## Verifying hosted media (added 2026-11-03)
The sandbox cannot fetch static.metricool.com. To prove Metricool hosts the exact bytes: ask the owner to allow the built-in browser on https://static.metricool.com (`request_access`), `preview_start` one hosted URL, then run same-origin `fetch` + `crypto.subtle.digest('SHA-256', ...)` in `javascript_tool` for every hosted URL and compare with `SHA256SUMS`. Result on 2026-11-03: all 8 files identical, carousel order preserved. Hashes are of hosted bytes only; this does not prove publishing.
