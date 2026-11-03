# west-apadana-media

Production system and public media host for West Apadana's social content.

- **Say:** "Claude, create a new batch". Claude follows `docs/BATCH_RUNBOOK.md`.
- `CLAUDE.md`: operating rules and environment facts (loaded automatically when the repo is attached).
- `docs/PIPELINE_STATUS.md`: what is verified and what is still untested.
- `docs/social-identity/`: the Social Identity Kit (profile bios, About text, links, image specs, implementation plan). DRAFT, not applied to any live profile. Check with `python3 -I scripts/social_kit.py check`.
- `docs/CREATIVE_SYSTEM.md`: brand, content types, freshness and honesty rules, QA checklist.
- `scripts/`: renderer, video engine, audio synthesis, verification, publishing, inventory, Metricool payload builder.
- `templates/`, `config/`, `fonts/` (DM Sans and Inter Display, both OFL).
- `inventory/`: every piece with files, captions, URLs, dates, Metricool draft IDs and statuses, plus creative history.
- `media/<batch>/`: published assets, served at https://thewa404.github.io/west-apadana-media/media/<batch>/<file>

This repository is public. Do not commit secrets.
