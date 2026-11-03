# Implementation plan

Nothing starts until the owner approves the kit and answers the blocking decisions in `40-decisions.md`. No live profile is changed by Claude without explicit approval of that specific platform.

## Principles
- **Apply close to launch.** Profiles promise "lessons" and concept work. Apply them within a day or two of the first post so a visitor finds content that matches the bio. First posts are planned for Monday 16 November, subject to sample approval.
- **One platform at a time, verified before the next.**
- **Save the "before".** Before each edit, record the current text in `docs/social-identity/before/<platform>.txt` (text only, no screenshots of account settings, because this repo is public).
- **Exact paste.** Copy from `recommended-set.md`. Counts are already verified; the editor's own counter is the final check.
- **Change one thing at a time after launch.** Bios are reviewed at 30 days. No A/B swaps in the first two weeks, so results mean something.

## Prerequisites (blocking)
| # | Prerequisite | Who | Status |
|---|---|---|---|
| P1 | Inquiry destination exists (page or form) | Owner decision; Claude can design and, with approval, build in Framer | Missing |
| P2 | Profile mark chosen (existing logo or direction 1 or 2) | Owner | Open |
| P3 | Public contact email decided (or "form only") | Owner | Open |
| P4 | Instagram is a Professional account linked to the Facebook Page | Owner (in the app) | Unknown |
| P5 | Current state of each profile captured | Owner sends text; Claude cannot read the sites from here | Not done |
| P6 | Handles confirmed on X, LinkedIn and YouTube | Owner | Unknown |
| P7 | Assets rendered from the approved mark | Claude (pipeline) | Waits for P2 |

## Order and per-platform steps
Estimates assume the owner pastes by hand and are rough.

### 1. Facebook Page (first, because Instagram links to it)
1. Page name, username/URL, category.
2. Intro and description from the recommended set; Long About into the Overview/More info field if offered.
3. Profile image, cover.
4. Website field; action button (Send message or Learn more).
5. Link the Instagram professional account.
**Proof:** view the Page logged out in a private window; check the intro is not truncated and the button works. About 15 minutes.

### 2. Instagram
1. Confirm Professional account type and category (P4).
2. Name field, bio (three lines, line breaks preserved), link, optional second link.
3. Profile image; four Highlight covers.
4. Contact button only if P3 allows.
**Proof:** view on a phone; the name shows the keyword, the three lines wrap cleanly, the link opens the destination with `utm_source=instagram`. About 15 minutes.

### 3. Threads
1. Check whether the bio is editable separately from Instagram. If not, stop; Instagram's bio stands.
2. If editable, apply option B. Link with `utm_source=threads`.
**Proof:** profile view on phone. About 5 minutes.

### 4. YouTube
1. Channel name, handle, description, links (three, labeled), banner, picture.
2. Contact email only if P3 allows.
3. Create four playlists once there is something to put in them.
**Proof:** preview in YouTube Studio for TV, desktop and mobile; the first 150 characters make sense alone. About 15 minutes.

### 5. LinkedIn Company Page
1. Create the Page from a personal admin account (owner).
2. Name, tagline, About, website, industry, size, specialties; location only if approved.
3. Logo, cover (confirm the current size in the upload dialog), custom button.
**Proof:** view as a non-admin. About 20 minutes.

### 6. X
1. Display name, bio, website. Header and avatar.
2. Leave location empty unless approved.
**Proof:** view logged out. About 10 minutes.

### 7. LinkedIn personal profile (optional, last)
Only after the owner decides on name and photo (decision 4). Headline, About, Featured, current position linked to the Company Page. No invented experience, skills, endorsements or recommendations. About 20 minutes.

## Launch check (the day before the first post)
- [ ] Every profile shows the same name and mark.
- [ ] Every link opens the destination and carries its own UTM tag.
- [ ] No bio claims anything in the "must never appear" list.
- [ ] Concept wording is present wherever the portfolio is mentioned.
- [ ] Instagram, Facebook and YouTube connections in Metricool still show as connected (`getBrandSettings`).
- [ ] Profile pins and highlights are placeholders or empty (no unpublished content promised).

## Rollback
Each change is reversible from the editor. The saved "before" text is the rollback. Handle and URL changes are the exception: changing an Instagram or X handle breaks existing links, so handles stay as they are.

## After launch
- **Day 14:** read profile visits, link clicks and follows in each platform's insights (Metricool analytics need published posts, so this is untested until then).
- **Day 30:** compare UTM-tagged visits and inquiries per platform. Decide whether to swap a bio option, add a link or retire X/LinkedIn front doors if they produce nothing.
- Record each change in the kit changelog.
