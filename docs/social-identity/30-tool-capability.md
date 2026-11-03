# Can our tools update profiles? Confirmed vs untested

Investigated 2026-11-03. **Nothing was changed on any live profile.** All checks were read-only.

## Confirmed (observed in this session)
| Finding | Evidence |
|---|---|
| The Metricool MCP has **no tool that edits a network profile** (bio, name, links, photo, banner) | Its tool list: create/update/review scheduled posts, get scheduled posts, analytics metrics, best time to post, and `getBrandSettings`. None writes profile fields. |
| `getBrandSettings` is read-only and returns only the Metricool brand: label, brand logo URL, timezone, and which networks are connected | Called 2026-11-03. Connected: Facebook (page id 1247817755085630), Instagram `thewestapadana`, Threads `thewestapadana`, YouTube channel UCU_bcNXgNu9eHcJzOTBBOtA. **X and LinkedIn are not connected.** |
| No other installed connector touches social profiles | Installed: Context7 (docs), Framer (websites), Google Drive (files), Metricool. Registry search for Instagram, Facebook Page, LinkedIn, YouTube channel and profile tools found only posting, analytics, ads or research connectors, none installed. |
| The sandbox cannot read the live profiles | `instagram.com` and `youtube.com` are not on the session allowlist. **The current state of every profile is unknown to Claude.** |
| Metricool's profile-style fields do not edit the networks | Changing a Metricool brand's label or logo does not change the profile on Instagram or any other network. |

## Untested (do not rely on)
| Possibility | Status and caveats |
|---|---|
| **Supervised browser-assisted editing**: Claude drives the owner's built-in browser while the owner is signed in, and edits the profile through each network's own web editor | Untested. Needs per-site access approval and the owner to sign in themselves. Claude never types passwords and cannot pass two-factor or bot checks. Each change is an account-settings change and needs explicit per-platform approval. Some Instagram settings may be phone-only (not verified). Likely to break when a platform changes its UI. |
| **Read-only version of that browser path** (open the owner's own profile pages and read what is live now) | Untested, and a sensible first step because it writes nothing. It would fill P5 in the plan. |
| **Official APIs** (Facebook Pages API, YouTube Data API, X API, LinkedIn API) | Not configured, and from general knowledge only, **not verified in this session**: Facebook and YouTube are believed to allow some profile-field and branding updates; the Instagram Graph API is believed not to allow bio editing; LinkedIn has no personal-profile editing API; X profile updates may need a paid API tier. Using any of these means creating developer apps and storing tokens, which conflicts with "no new services" and the public-repo rule against secrets. Not recommended. |
| **Third-party connectors** (for example Typefully for X/LinkedIn posting, Taplio for LinkedIn) | Not installed, not evaluated for profile editing, and each is a new service. Not recommended for this task. |
| **Metricool inbox or review tools** for profile changes | Not applicable. They concern posts. |

## Recommendation
1. **Default: the owner pastes from the kit.** Estimated 10 to 20 minutes per platform. Copy is final and counted; there is nothing to assemble.
2. **Optional trial, one platform:** with approval, a read-only look at one live profile, then one reversible edit on the lowest-risk platform (the YouTube description is the easiest to revert). That would turn "untested" into "confirmed" or "not workable", and the result would be recorded in `docs/PIPELINE_STATUS.md`.
3. Do not set up API access or new subscriptions for profile editing. The saving is minutes, once.
