# AGENTS.md — Blockium Website

Single source of instructions for every AI coding agent working in this repository.

---

## Project Overview

**Blockium Website** is the static marketing and user portal for the Blockium Chrome Extension. Repo: `https://github.com/krjangid/blockium-website`.

- **Branch**: `feat/uninstall-goodbye-page`
- **Architecture**: Zero-runtime-dependency static site built from templates (`site-src/`) into root and localized directories (`de/`, `ru/`, `hi/`, etc.) across 10 locales.
- **Design System**: Editorial ivory aesthetic (`#f2efe9` paper, `#fcfbf8` surface, `#a32f19` rust, `#171714` ink).

---

## Responsive Display Invariants (All Screen Sizes)

Every change to CSS or templates MUST look stunning and perform flawlessly across all 7 display tiers:

1. **Ultra-Small Mobile (320px - 360px)** (e.g. iPhone SE 1st gen):
   - `scrollWidth <= clientWidth` (zero horizontal scrolling).
   - Wordmark scales to 20px, compact buttons, outer container width `calc(100% - 24px)`.
2. **Standard Mobile (375px - 428px)**:
   - Hamburger menu active, `.header-language` hidden (`display: none !important;`), single-column or horizontal cards.
3. **Phablet / Foldable (541px - 680px)**:
   - 2-column feature catalog and privacy cards.
4. **Tablet Portrait (768px - 860px)**:
   - Balanced 2-column catalog, spacious card padding (18-24px), prominent hero typography.
5. **Tablet Landscape & Compact Laptop (861px - 1024px)**:
   - Desktop nav island active with `gap: clamp(16px, 2.5vw, 40px);` to avoid element collision with language selector or install button.
6. **Laptop & Desktop (1280px - 1440px)**:
   - **Baseline Design.** NEVER break or alter desktop proportions while adjusting mobile or tablet.
7. **2K, 4K UHD & Smart TV (1920px - 3840px)**:
   - `.site-header`, `.wrap`, and footer containers MUST be capped at `max-width: 1440px; margin: 0 auto;`.
   - Content must remain centered and framed on ultra-wide / TV screens.

---

## Technical Rules

- **Grid Minmax Protection**: Always use `grid-template-columns: ... minmax(0, 1fr)` and set `min-width: 0; overflow-wrap: break-word;` on text items to prevent long international words (German, Russian) from causing horizontal overflow.
- **Header Language**: Must be explicitly hidden at `<= 860px` with `!important` to keep the header uncluttered on mobile and tablet portrait.
- **Build Before Testing**: After updating templates in `site-src/`, always run `python3 scripts/build-locales.py` to regenerate all 50 localized pages.

---

## Definition of Done

A change is done only when all 3 checks pass cleanly:

```bash
python3 scripts/check-responsive.py    # Design tokens, CSS invariants, and screen safety
node scripts/audit-viewports.js         # Automated 15-viewport headless audit (320px to 4K TV)
python3 scripts/check-locales.py       # Localized templates, links, and syntax validation
```
