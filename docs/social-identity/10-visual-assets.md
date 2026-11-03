# Visual assets

Not yet produced. The specifications below are for approval; the renderer (`scripts/wa/render.py`, brand tokens in `config/brand.json`) can generate banners and Highlight covers once the logo file is available.

## The logo: existing approved logo only
Owner decision 2026-11-03: use the existing approved West Apadana logo. Do not invent a replacement monogram or rebrand without approval. The earlier "WA monogram" and "serif W" directions were removed from this kit.

**MISSING ASSET.** The original approved logo file has not been located:
- Repo: no logo file (assets hold portfolio.json, screenshots and textures).
- Google Drive: no logo, brand or West Apadana file found (searched 2026-11-03).
- Metricool: holds a brand logo uploaded in August 2026 (`https://static.metricool.com/brand-logo/202608/6728476-file-3671512345440253977.jpeg`). It has never been reviewed here and nobody has confirmed it is the approved logo. The sandbox cannot fetch that host.

What is needed: the owner confirms the Metricool logo is the approved one (Claude can then read it through the owner's built-in browser and store the source in the repo), or supplies the original file. Until then no profile image, banner or Highlight cover is produced.

One logo on all seven profiles. It must read at 40 px and sit inside the central 70% of the square so circular crops never cut it. Obsidian text on champagne gold is an approved pair, usable for a gold-ground alternate on banners only. No gradients, no 3D effects, no tiny text.

## Image specifications
| Platform | Profile image | Banner / cover | Notes |
|---|---|---|---|
| Instagram | Square source 1080x1080, shown as a circle | None. Four Highlight covers | Threads reuses the Instagram image according to sources |
| Facebook Page | Square, circle display (about 170 px on desktop) | Source 1640x624, safe text zone central 640x312 | Verify the live crop |
| X | 400x400 (official), circle | 1500x500 (official), text in central 1100x300 | The avatar covers the lower left |
| LinkedIn Company | 400x400 recommended, 268x268 minimum | Size reportedly changed mid-2026: confirm in the upload dialog | Logo sits bottom-left, keep it quiet |
| LinkedIn personal | See decision 4 | 1584x396 | Photo covers the left quarter |
| YouTube | 800x800, circle | 2560x1440, text in central 1546x423 | Check TV, desktop and phone previews in Studio |

## Banner design (one system, adapted per size)
- Ground: obsidian #101010, with a very light grain (the existing `assets/textures/grain.png`).
- The existing approved logo, plus one line in DM Serif Display italic, ivory #F2EDE4: "Premium websites and digital experiences." Optional second line in DM Mono: the handle.
- A thin champagne-gold rule. No stock imagery, no screenshots that imply client work.
- A concept strip variant (optional, later): one TORQ crop labeled "Concept project, not client work" at small size.
- Contrast: ivory on obsidian and gold on obsidian are approved pairs in `brand-check`.

## Highlight covers (Instagram)
Four covers: Start here, Lessons, Concepts, Ways to start. Obsidian ground, gold line icon, DM Mono label. 1080x1920 source, central circle only visible.

## Delivery
Files would be rendered into `assets/social-identity/` in the repo (public). Nothing is uploaded to a platform by Claude: the owner uploads them, or approves a supervised browser-assisted attempt (`30-tool-capability.md`).
