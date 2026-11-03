# Creative system

## Brand
- Studio: premium digital design and marketing; websites and distinctive digital experiences. Audience: business owners, entrepreneurs, brands, prospective website and marketing clients.
- Palette (`config/brand.json`): Obsidian #101010, Graphite #252525, Dark Navy #162238, Champagne Gold #C6A66A, Ivory #F2EDE4. On ivory use `gold_deep` (#84652D) for small text and rules: brand gold fails contrast there. `wa_cli.py brand-check` must pass.
- Type: Inter Display for headlines (OFL stand-in for Neue Haas Grotesk), DM Sans for body. Tight tracking, large scale, one gold accent word per headline.
- Direction: premium, bold, editorial, cinematic, experimental, sophisticated, original. Architectural lines, generous negative space, one idea per frame.
- Voice: confident, precise, warm. Short sentences. No "unlock", "game-changer", "elevate your brand", no exclamation marks, no AI-sounding filler.

## Education first (permanent principle, 2026-11-03)
- Every piece has a ground: **education** (teaches something usable), **demonstration** (creative or portfolio work), **story** (brand storytelling, told as lesson or behind-the-scenes).
- Starting hypothesis 70/20/10. The first 20-piece test is 14/4/2. It is a test, not a limit; volume may grow (Metricool Starter under consideration).
- Topics: websites, marketing, branding, customer acquisition, conversion, AI tools, automation, business growth. Original insight over generic advice. A viewer must be able to act on it.
- Hook in the first 1-2 seconds. Plain words. High information density without overload: one idea per frame, one takeaway per piece.
- Faceless formats: kinetic typography, annotated real website examples, diagrams, screen recordings, animation. Voiceless by default (see PIPELINE_STATUS voiceover test).
- No pitch inside a piece. CHECK, REBUILD and BRIEF are optional offers on profiles and a landing page only.
- Evidence tiers per piece (`content/calendar.json`): own, invented-labelled, cited, third-party-public. A claim without its tier's evidence is cut.
- Analysing real third-party websites is allowed when the example is publicly accessible, claims are verifiable, the analysis is fair and the source is shown (URL, capture date, verbatim words under 15). Never invent performance data. Never imply a company hired us. Include examples that do the thing well, not only failures.

## Content types
| Type | Format | Template / engine | Specs |
|---|---|---|---|
| Single-image graphic (bold) | image | `slide.html.j2` kind `statement` | 1080x1350 (or 1080x1080) JPEG |
| Educational carousel | 5-8 slides | `slide.html.j2` kinds `cover`, `point`, `compare`, `cta` | 1080x1350, index/total shown |
| Brand story | 1-5 slides | kind `story`: a storytelling carousel for the FEED (4:5), not an Instagram Story | 1080x1350 |
| Website showcase | 1-4 slides | `showcase.html.j2` (browser or phone frame) with REAL screenshot | 1080x1350 |
| Before/after | carousel | kind `compare` for concepts; for real redesigns use two real screenshots side by side | label as concept |
| Animated typography reel | 8-15 s video | `reel.html.j2` beats | 1080x1920, 30 fps, h264 + AAC |
| Cinematic website walkthrough | 8-15 s video | `reel.html.j2` with `scroll` (real screenshot panned in a device frame) | 1080x1920 |
| Portfolio showcase reel | video | scroll + beats | same |

Reels are pure functions of time (`window.setT(t)`), rendered frame by frame, with an original synthesized score (`wa/audio.py`, vary `root_hz`, `bpm`, `seed` each batch; no licensed music). Instagram UI covers about the top 240 px and bottom 340 px: keep key content between.
Cinematic live-action footage or AI video generation is NOT available in this toolchain. Reels are typographic/motion-graphic. Say so instead of implying otherwise.

## Freshness rules (no repetition)
- Before writing, read `inventory/history.json`. Run `wa_cli.py dup` on every hook, headline, concept (threshold 0.5).
- Rotate across batches: theme, layout kind, hook formula, topic, featured project, score key. Do not reuse a hook formula twice in one batch.
- Hook formulas: contrarian claim; specific number from real work; before/after; myth vs reality; question the reader has; process reveal; short manifesto line; micro-lesson ("One rule for ...").
- Education topics (website craft): hierarchy, spacing, typography, first-screen clarity, trust signals, calls to action, mobile-first, speed, accessibility/contrast, photography, microcopy, pricing pages, navigation, case-study structure.
- Process content: how a page is built (wireframe -> type -> color -> motion), decisions behind a concept project, tools, mistakes found and fixed. Use real project facts only.

## Honesty rules
- Never fabricate testimonials, client names, metrics, awards or results. Every Framer portfolio site is a concept/demo project (owner confirmed 2026-11-03): use it in marketing, label it "Concept project, not client work" (`config/settings.json -> demo_label`), and never imply a real client commissioned it.
- Statistics only with a verifiable source that is named in the caption; otherwise do not use numbers.
- Before/after: label concepts as concepts. Never present a mockup as a live result.

## Captions
- Instagram: hook line first (shown before "more"), 2-6 short lines of value, then stop. End on the lesson or a genuine question; no offer. 3-8 relevant hashtags (never 30). Max 2200 chars.
- Facebook: same idea, slightly fuller sentences, 0-3 hashtags, a link only if the user supplies one.
- Threads: conversational, under 500 chars, 0-1 tag.
- YouTube Shorts: title <= 100 chars with the idea, short description, `madeForKids: false`.
- Endings (decided 2026-11-03): teach, then end naturally. Allowed: a save or share suggestion, a real question, an occasional "follow for the next one". Not allowed in any piece: DM keywords, booking or inquiry requests, offers (CHECK, REBUILD, BRIEF, free reviews), "link in bio" pitches, scarcity. Offers live on profiles and the landing page. Never every post, never forced. Check with `wa_cli.py pitch-lint`.

## QA checklist (every piece)
1. `wa_cli.py verify` passes for every network the piece goes to.
2. Looked at it: text fully readable at phone size (headline >= 80 px, body >= 32 px on 1080 wide), nothing clipped, nothing overlapping, margins consistent, brand colors only.
3. Videos: contact sheet reviewed, audio present, `wa_cli.py loudness` near -16 LUFS.
4. Showcase: screenshot is real, label present, project name correct.
5. Caption proofread; no claims that are not true; platform limits respected.

## Approved 2026-11-03
Fonts DM Serif Display and DM Mono (alongside Inter Display and DM Sans); obsidian text on champagne gold. Five visual worlds stay, executed as art-directed pieces rather than one template. Rebuilt direction: same-frame slider-wipe seam with registration marks, grayscale proof-sheet fictional "before", caption-bar labels, pin-drop for carousel changes.
