# Pipeline status

Last updated: 2026-11-03 (education-first rules, pitch lint, revised calendar, voiceover test result added). Rule: nothing below is claimed beyond its evidence. Update this file whenever a test is run.

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
| Draft -> scheduled flip (`updateScheduledPost`, `draft: false`, `autoPublish: false`, far-future date) | OK 2026-11-03 on one disposable test post (approved by the owner). Read-back: `draft: false`, `autoPublish: false`, same date, 3 media unchanged (no re-ingestion), same `uuid`, new `id`. The other test draft was untouched. Provider status still reads "Pending" (as for drafts), so `draft: false` is the evidence. How the planner displays it has NOT been confirmed by the owner yet. |
| Byte-exact delivery to Metricool-hosted storage | 2026-11-03, sample set: original sha256 == repo copy == fresh GitHub clone (10 files). Then, in the owner's built-in browser (same-origin fetch + SubtleCrypto SHA-256 on static.metricool.com), the 7 carousel JPEGs and the 13.4 MB reel hosted by Metricool hashed IDENTICALLY to the originals (no re-encoding, correct content-type, HTTP 200). |
| Carousel order preserved | Hosted slide N hashes to local slide N for all 7, in submitted order, after draft creation, after the draft -> scheduled update and on read-back. |
| Scheduled post retains media, caption, date, destination | Two disposable posts (7-slide carousel; reel with soundtrack) flipped `draft: false`, `autoPublish: false`, 2 June 2027. Read-back: same media URLs and order, caption identical (newline, unicode, quotes), 7 alt texts identical, same date/time, destination instagram, type POST / REEL, same `uuid`, new `id`. |
| No manual download or upload | Whole chain ran from the sandbox: render -> git push -> Pages URL -> Metricool ingestion. The owner only had to approve one browser-pane access prompt for the verification step. |
| Still renderer: DM Sans + Inter Display, slide kinds statement/cover/point/compare/story/cta, showcase | OK, visually reviewed; contrast pairs pass `brand-check` |
| Animated typography reel + original synthesized score | OK locally: 1080x1920, 30 fps, h264 + AAC, about -15 LUFS; typography reel accepted by a YouTube Short draft |
| Website scroll-through reel from a REAL Framer screenshot | OK locally; accepted by an Instagram Reel draft |
| Real website screenshots (Framer `exec` -> file in sandbox -> ingest) | OK for one project (TORQ). Read-only. |
| Toolkit: duplicate check, budget math, calendar planner, payload builder, `build_batch.py` build/publish/payloads | OK on a 4-piece dry-run batch (removed afterwards) |

| Profile editing by our tools (read-only investigation 2026-11-03) | CONFIRMED NOT AVAILABLE: the Metricool MCP has no profile-edit tool; no installed connector edits social profiles; the sandbox cannot read instagram.com or youtube.com. Details in `docs/social-identity/30-tool-capability.md`. |

## Voiceover quality test (2026-11-03, limited, existing tools only)
RESULT: **NOT ADOPTED. No voice that meets the premium bar is available with the tools in this environment.**
- Available: the `flite` filter inside ffmpeg (three voices tried: slt, awb, kal16). It is a small rule-based synthesizer from the 2000s. A 28-word test line rendered in 8.8 to 9.8 s at -17 LUFS. It is intelligible, flat and robotic. It is not comparable to a professional voiceover and I did not treat it as a candidate; I kept the sample so the owner can hear the baseline.
- Not available: neural voice engines (the Python and npm package registries were unreachable from this session, so none could be installed), and the optional ElevenLabs add-on tools are not connected. No new subscription was started.
- Not verifiable by me: whether any voice sounds convincing. Audio quality is judged by ears; I measured loudness only. Any candidate voice must be listened to by the owner before adoption.
- Decision for now: reels stay voiceless, with on-screen captions and original sound design. If a better engine is enabled later (a connected add-on or an installable local model), rerun this test against the premium bar: natural pacing, no clipped consonants, convincing emphasis, a brand-appropriate timbre, and compare with a human recording of the same script. If an AI voice is ever adopted, disclose it with the posting tool's AI flags (`isAiGenerated`, `isAiGeneratedContent`).
- Sample for the owner (baseline only, not a candidate): `flite_slt.m4a`, delivered in chat. It is not committed to the public repo.

## Pitch lint and calendar check (2026-11-03)
Tested on the repo. `wa_cli.py pitch-lint`, `pitch-lint-pieces`, `calendar-check`. Checked: flags DM keywords, booking requests, free offers, contact/hire requests, link-in-bio pitches, scarcity and the offer names CHECK/REBUILD/BRIEF; passes save, share, questions and follow invitations. The three built sample pieces are clean (closing paragraphs and CTA fields). Known limit: it is a pattern match, so example copy for invented businesses ("Book a repair") must be reviewed by a person, and it cannot judge tone.
`calendar-check` on `content/calendar.json`: no lint hits, 14/4/2 mix, 18 network-posts in November and 18 in December, no duplicate hooks or titles against history or within the calendar.

## UNTESTED (do not rely on these)
1. **Actual publishing in either mode** (a successful draft or scheduling test does NOT prove this): manual delivery (push notification at the scheduled time) and automatic (`autoPublish: true`, API publish). Never run. The first real approved post must be monitored.
2. Reverting a scheduled post back to a draft.
3. Facebook Reel, Instagram audio selection, first comment, alt text.
4. Screenshots of the other 8 Framer projects, and Phone-breakpoint captures.
5. Fetching Pages URLs from the sandbox (blocked). Metricool ingestion is the proof instead.
6. Metricool review/approval tools (need an Advanced plan), analytics feedback loop (needs published posts).
7. How Metricool Free behaves when more than 20 network-posts are scheduled in a month (its docs say only 20 publish).
8b. Supervised browser-assisted profile editing in the owner's built-in browser (read-only look first); official profile APIs (not configured, not verified).
8c. Capturing screenshots of third-party public sites for teardown pieces (needs the owner's built-in browser or another route; the sandbox cannot reach most hosts). Not tried.
8d. Metricool Starter behaviour (unlimited-with-fair-use scheduling, LinkedIn connection, X as a paid add-on) comes from Metricool's marketing pages and third-party summaries, which disagree on figures. Check Metricool's own pricing page before the owner decides.
9. Long-term repo growth (GitHub recommends <= 1 GB). JPEG slides keep a batch to roughly 10-30 MB.

## KNOWN LIMITS
- No live-action footage and no AI video generation: reels are typographic / motion-graphic / website scroll-throughs. No licensed music (original synthesized score only). Audio is verified by levels, not by listening.
- Neue Haas Grotesk is not installed (commercial). Inter Display is the stand-in; drop licensed files into `fonts/` and edit `config/brand.json` to switch.
- Metricool MCP: no delete tool, no upload tool, one caption per post, a date is required even for drafts.
- Shell/WebFetch cannot reach github.io or static.metricool.com.
- Framer projects are unpublished; screenshots are Framer renders of the project pages.
- Pages media in folders beginning with `_` or `.` may not be served (the first carousel attempt failed that way; fixed by renaming the folder and committing `.nojekyll`; cause not isolated from deploy timing).
- Free plan: 20 published posts per calendar month for the whole brand; a post on two networks counts twice; drafts and scheduled posts do not count until published (Metricool help center, 2026-11-03; the live planner counter has not been checked).

7b. Whether the Instagram account is a Business/Creator account linked to a Facebook Page (required for API auto-publish). Not visible through the tool. Unsupported cases fall back to a notification.
7c. Whether the Metricool planner displays the two new scheduled test posts as expected (owner has not confirmed).

## Test posts currently in the Metricool planner (delete when done; Claude has no delete tool)
- Instagram carousel, SCHEDULED test (manual delivery, `autoPublish: false`, 1 June 2027 10:00 ET): https://app.metricool.com/planner/calendar?blogId=6728476&openWithPostUuid=-6781590428065772322
- Instagram Reel test DRAFT (website scroll-through, 1 June 2027 11:00 ET): https://app.metricool.com/planner/calendar?blogId=6728476&openWithPostUuid=4351194295856021551
- Instagram 7-slide carousel SCHEDULED test A (manual delivery, 2 June 2027 10:00 ET): https://app.metricool.com/planner/calendar?blogId=6728476&openWithPostUuid=4185365381692804473
- Instagram Reel SCHEDULED test B (manual delivery, 2 June 2027 10:30 ET): https://app.metricool.com/planner/calendar?blogId=6728476&openWithPostUuid=8613085067297049378
- Test posts never count against the monthly allowance unless published; none was published.
