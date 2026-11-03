# Foundation

## Positioning
West Apadana is an **independent digital design studio** creating **premium websites and distinctive digital experiences**. Handle: @thewestapadana. Tagline in `config/brand.json`: "Premium websites and digital experiences."

Revised 2026-11-03 (owner review). A profile should make a stranger want to follow for valuable content, and say clearly that West Apadana builds premium websites. The message order on every profile:
1. **Lessons that can be used the same day.** Why to follow. This is the education-first content engine (websites, marketing, branding, customer acquisition, conversion, AI tools, automation, growing a business).
2. **Premium websites and digital experiences.** What we build, stated plainly every time.
3. **Concept work, always labeled.** Why to trust us. With no clients to show yet, honesty about the portfolio is the credibility.
4. **Optional ways to start.** Secondary. Short bios (Instagram, Threads, X, Facebook intro, LinkedIn tagline and headline) never carry an offer. The offers appear on the link destination and in long About text after the first paragraph (Facebook, LinkedIn, YouTube). The free homepage review is not the main message of any profile. `scripts/social_kit.py check` enforces this.

## Real services (the only ones the profiles may claim)
The studio builds premium websites and digital experiences. The three offers below are optional ways to start, secondary on every profile.
- Premium website design and distinctive digital experiences.
- **CHECK**: free, concise homepage review that identifies three improvement opportunities.
- **REBUILD**: free initial website improvement assessment. An assessment, not a promise of a redesign.
- **BRIEF**: an invitation to discuss a potential website project.

On profiles these appear as "Free homepage review", "Website improvement assessment" and "Project conversation". The internal codenames CHECK, REBUILD and BRIEF are never shown publicly. All inquiries are handled personally by the owner. No response time is promised anywhere.

Marketing, branding, SEO and AI automation are **lesson topics**, not claimed services, until the owner confirms otherwise (`40-decisions.md`, decision 3). `docs/CREATIVE_SYSTEM.md` mentions "digital design and marketing"; the profiles deliberately claim less.

## Must never appear in any bio, About or link text
- Client names, client counts, testimonials, case studies, results or statistics.
- Years in business, founding year, awards, press, certifications, partnerships.
- "Agency", "our team", team size. The studio is independent.
- A city, region or address (none is confirmed).
- A response time or turnaround, or guaranteed outcomes.
- Marketing, SEO or automation as a service (see above).
- Any suggestion that concept projects were commissioned. The wording is always "concept project, not client work".

`scripts/social_kit.py check` lints for most of these.

## Voice
Confident, precise, warm. Short sentences. No exclamation marks, no emoji in bios, none of the banned phrases in `docs/CREATIVE_SYSTEM.md`.

## Conversion path (the thing the profiles depend on)
A profile only converts if the link goes somewhere. **No studio website or inquiry page is on record, and the Framer portfolio sites are unpublished.** Every recommended bio points to "the link", so this destination is a blocking prerequisite.

Recommended minimum: one page at the studio's own address that does one job.
- Headline in the brand voice and one sentence of what the studio does.
- Lessons and concept work first (the visitor came for lessons), then three clearly separate optional ways to start: free homepage review, website improvement assessment, project conversation.
- One simple form or one public email, whichever the owner will answer personally. No promised response time.
- A strip of concept projects labeled "Concept project, not client work".
- A privacy line if a form collects data.

Each platform links with its own UTM tag so we can see which profile produces inquiries: `?utm_source=<platform>&utm_medium=bio&utm_campaign=profile`.

Building that page in Framer is a separate piece of work that would publish a live site. It needs its own approval and is not part of this kit.

## Networks not connected to Metricool
Metricool is connected to Instagram, Facebook, Threads and YouTube. **X and LinkedIn are not connected**, so the content campaign will not post there automatically. They are set up as credible, accurate front doors that point to the destination page, and are posted to manually or connected later if the owner decides.

## Education-first rule applied to profiles
Educational posts stay clean (no DM keywords, no booking requests, no promotional endings). Offers are optional, sit on the link destination or in long About text after the lessons and the premium-websites statement, and let the visitor choose. They are never the headline of a profile.

## Logo
Use the existing approved West Apadana logo. Do not invent a replacement monogram or rebrand without owner approval. **The original logo asset has not been located** (not in the repo, not in Google Drive). It is a missing asset. A brand logo exists in Metricool (uploaded August 2026) but nobody has confirmed it is the approved one. See `10-visual-assets.md`.
