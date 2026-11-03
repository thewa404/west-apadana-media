# West Apadana Social Identity Kit

Version 0.1.0 (draft, 2026-11-03). **Status: for owner approval. Nothing in this kit has been applied to any live profile.**

The kit defines how every West Apadana profile presents the studio before the content campaign starts: names, bios, About text, keywords, calls to action, links, images, and the order in which to implement them. It follows the project rules in `CLAUDE.md`: no invented clients, results or credentials; portfolio pieces are always "Concept project, not client work"; offers live on profiles, not inside educational posts.

## Contents
| File | What it is |
|---|---|
| `recommended-set.md` | The one cohesive set: the recommended bio for each platform, ready to paste |
| `platforms/*.md` | Per platform: three options (premium/minimal, bold/creative, professional/conversion), limits, keywords, CTA, link strategy, photo and banner notes. **Generated** from `kit.json` |
| `kit.json` | Source of truth for all copy and limits |
| `00-foundation.md` | Positioning, real services, voice, what must never be claimed, the conversion path |
| `10-visual-assets.md` | Profile mark and banner specifications and safe zones |
| `20-implementation-plan.md` | Platform-by-platform plan, prerequisites, order, verification, rollback |
| `30-tool-capability.md` | What our connected tools can and cannot do to profiles: confirmed vs untested |
| `40-decisions.md` | What the owner needs to decide before anything goes live |

## Workflow
1. Edit `kit.json` (never the generated platform files).
2. `python3 -I scripts/social_kit.py check` verifies every option fits its limit and passes the honesty lint (no exclamation marks, no emoji, no unsourced credentials, no response-time or outcome promises, concept work labeled).
3. `python3 -I scripts/social_kit.py render` regenerates the Markdown.
4. Commit. Every change to profile copy is a commit, so the history shows what was live when.

## Limits
Character limits come from official X Help and from secondary sources for the other platforms. Where sources disagreed the lower figure was used. Every limit must be confirmed in the live editor at implementation time. Each platform file shows the confidence of every limit.

## Changelog
- 0.1.0 (2026-11-03): first draft. Seven platforms, three options each, recommended set, plan, capability audit, decisions.
