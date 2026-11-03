# Visual assets

Not yet produced. The specifications below are for approval; the renderer (`scripts/wa/render.py`, brand tokens in `config/brand.json`) can generate every asset once the mark is decided.

## One mark everywhere
Consistency across platforms builds recognition. Use **one** profile mark on all seven profiles.

Open question: a logo may already exist (Metricool holds a brand logo uploaded in August 2026). It has not been reviewed in this session. If one exists, the plan is to keep it and build the banners around it. If not, two directions to choose between:

| Direction | Description |
|---|---|
| 1. Monogram | "WA" in Inter Display Bold, champagne gold #C6A66A on obsidian #101010, tight tracking, generous margin |
| 2. Serif W | A single "W" in DM Serif Display, gold on obsidian, with a thin gold rule beneath |

Obsidian text on champagne gold is also an approved pair, for a gold-ground alternate used on banners only.

Rules: no gradients, no 3D effects, no tiny text. The mark must read at 40 px. Keep the mark inside the central 70% of the square so circular crops never cut it.

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
- One line in DM Serif Display italic, ivory #F2EDE4: "Premium websites and digital experiences." Optional second line in DM Mono: the handle.
- A thin champagne-gold rule. No stock imagery, no screenshots that imply client work.
- A concept strip variant (optional, later): one TORQ crop labeled "Concept project, not client work" at small size.
- Contrast: ivory on obsidian and gold on obsidian are approved pairs in `brand-check`.

## Highlight covers (Instagram)
Four covers: Start here, Lessons, Concepts, Free review. Obsidian ground, gold line icon, DM Mono label. 1080x1920 source, central circle only visible.

## Delivery
Files would be rendered into `assets/social-identity/` in the repo (public). Nothing is uploaded to a platform by Claude: the owner uploads them, or approves a supervised browser-assisted attempt (`30-tool-capability.md`).
