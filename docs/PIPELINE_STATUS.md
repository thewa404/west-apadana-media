# Pipeline status

Last updated: 2026-11-03 (scheduling test added). Rule: nothing below is claimed beyond its evidence. Update this file whenever a test is run.

## VERIFIED
| Capability | Evidence |
|---|---|
| Media delivery: sandbox file -> `git push` -> GitHub Pages URL -> Metricool | 14 files so far (images, 3 reels, carousels, dry-run batch). sha256 of repo copy equals original; remote HEAD equals local HEAD; fresh clones matched byte for byte (2026-11-03). Metricool re-hosted every file on static.metricool.com. |
| Instagram single-image draft | OK |
| Instagram carousel draft (3 images, order preserved) | OK, read back |
| Instagram Reel draft (video) | OK, with and without audio; also the website scroll-through reel |
| Facebook image-post draft | OK |
| Threads image-post draft | OK |
| YouTube Short draft (title, `madeForKids: false`, `privacy: private`) | OK |
| Editing a draft (text, media, network, type) with `updateScheduledPost` | OK. The post `id` changes on every update, the `uuid` is stable. |
| Read-back of drafts via `getScheduledPosts` | OK, drafts are returned |
| Draft -> scheduled flip (`updateScheduledPost`, `draft: false`, `autoPublish: false`, far-future date) | OK 2026-11-03 on one disposable test post (approved by the owner). Read-back: `draft: false`, `autoPublish: false`, same date, 3 media unchanged (no re-ingestion), same `uuid`, new `id`. The other test draft was untouched. Provider status still reads "Pending" (as for drafts), so `draft: false` is the evidence; the owner confirmed the planner display separately. |
| Still renderer: DM Sans + Inter Display, slide kinds statement/cover/point/compare/story/cta, showcase | OK, visually reviewed; contrast pairs pass `brand-check` |
| Animated typography reel + original synthesized score | OK locally: 1080x1920, 30 fps, h264 + AAC, about -15 LUFS; typography reel accepted by a YouTube Short draft |
| Website scroll-through reel from a REAL Framer screenshot | OK locally; accepted by an Instagram Reel draft |
| Real website screenshots (Framer `exec` -> file in sandbox -> ingest) | OK for one project (TORQ). Read-only. |
| Toolkit: duplicate check, budget math, calendar planner, payload builder, `build_batch.py` build/publish/payloads | OK on a 4-piece dry-run batch (removed afterwards) |

## UNTESTED (do not rely on these)
1. **Actual publishing in either mode**: manual delivery (push notification at the scheduled time) and automatic (`autoPublish: true`, API publish). Never run. The first real approved post must be monitored.
2. Reverting a scheduled post back to a draft.
3. Facebook Reel, Instagram audio selection, first comment, alt text.
4. Screenshots of the other 8 Framer projects, and Phone-breakpoint captures.
5. Fetching Pages URLs from the sandbox (blocked). Metricool ingestion is the proof instead.
6. Metricool review/approval tools (need an Advanced plan), analytics feedback loop (needs published posts).
7. How Metricool Free behaves when more than 20 network-posts are scheduled in a month (its docs say only 20 publish).
8. Long-term repo growth (GitHub recommends <= 1 GB). JPEG slides keep a batch to roughly 10-30 MB.

## KNOWN LIMITS
- No live-action footage and no AI video generation: reels are typographic / motion-graphic / website scroll-throughs. No licensed music (original synthesized score only). Audio is verified by levels, not by listening.
- Neue Haas Grotesk is not installed (commercial). Inter Display is the stand-in; drop licensed files into `fonts/` and edit `config/brand.json` to switch.
- Metricool MCP: no delete tool, no upload tool, one caption per post, a date is required even for drafts.
- Shell/WebFetch cannot reach github.io or static.metricool.com.
- Framer projects are unpublished; screenshots are Framer renders of the project pages.
- Pages media in folders beginning with `_` or `.` may not be served (the first carousel attempt failed that way; fixed by renaming the folder and committing `.nojekyll`; cause not isolated from deploy timing).
- Free plan: 20 published network-posts per calendar month, per network.

## Test posts currently in the Metricool planner (delete when done; Claude has no delete tool)
- Instagram carousel, SCHEDULED test (manual delivery, `autoPublish: false`, 1 June 2027 10:00 ET): https://app.metricool.com/planner/calendar?blogId=6728476&openWithPostUuid=-6781590428065772322
- Instagram Reel test DRAFT (website scroll-through, 1 June 2027 11:00 ET): https://app.metricool.com/planner/calendar?blogId=6728476&openWithPostUuid=4351194295856021551
