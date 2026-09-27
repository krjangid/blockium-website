#!/usr/bin/env python3
"""
Responsive Layout and Design System Guardrail for Blockium Website.
Enforces multi-screen consistency, design tokens, viewport safety, and asset integrity.
"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

# Core design tokens that MUST remain identical across extension & website
DESIGN_TOKENS = {
    'paper': '#f2efe9',
    'surface': '#fcfbf8',
    'rust': '#a32f19',
    'ink': '#171714'
}

CSS_FILES = [
    ROOT / 'assets/editorial.css',
    ROOT / 'assets/editorial-pages.css',
]

STANDALONE_PAGES = [
    ROOT / 'site-src/home.template.html',
    ROOT / 'site-src/privacy.template.html',
    ROOT / 'site-src/terms.template.html',
    ROOT / 'site-src/report.template.html',
    ROOT / 'site-src/404.template.html',
    ROOT / 'goodbye.html',
]

failures = []

def check(name, condition, error_msg):
    if not condition:
        failures.append(f"❌ {name}: {error_msg}")
    else:
        print(f"  ✅ {name}")

print("\n🎨 Blockium Website Responsive & Design System Guardrails\n")

# 1. Design Token Parity Check
print("1. Checking Design Tokens Parity...")
for target in [ROOT / 'assets/editorial.css', ROOT / 'assets/editorial-pages.css', ROOT / 'site-src/404.template.html', ROOT / 'goodbye.html']:
    text = target.read_text(encoding='utf-8')
    for token_name, hex_val in DESIGN_TOKENS.items():
        check(
            f"{target.name} has token {token_name} ({hex_val})",
            hex_val.lower() in text.lower(),
            f"Missing required design token {hex_val}"
        )

# 2. Viewport & Container Measure Invariants
print("\n2. Checking Viewport & Container Measure Invariants...")
for f in CSS_FILES + [ROOT / 'goodbye.html', ROOT / 'site-src/404.template.html']:
    text = f.read_text(encoding='utf-8')
    
    # Check .wrap max-width is within standard measure [860px, 1440px]
    for m in re.finditer(r'(?:\.wrap|body\[[^\]]+\]\s*\.wrap)\s*\{[^}]*max-width\s*:\s*([0-9]+)px', text):
        val = int(m.group(1))
        check(
            f"{f.name} .wrap measure ({val}px)",
            860 <= val <= 1440,
            f"Container max-width {val}px is outside standard measure [860px, 1440px]"
        )

    # Check that no property declares a fixed min-width > 340px (which causes mobile overflow)
    # Strip @media declarations first so @media(min-width: 1600px) is not treated as a property
    clean_text = re.sub(r'@media[^{]+', '', text)
    for m in re.finditer(r'(?:^|[;{\s])min-width\s*:\s*([0-9]+)px', clean_text):
        val = int(m.group(1))
        check(
            f"{f.name} mobile min-width safety ({val}px)",
            val <= 340,
            f"Hardcoded min-width {val}px causes mobile horizontal scrolling on 360px viewports"
        )

# 3. Responsive Breakpoint Consistency
print("\n3. Checking Responsive Breakpoint Consistency...")
for target in CSS_FILES + [ROOT / 'goodbye.html', ROOT / 'site-src/404.template.html']:
    text = target.read_text(encoding='utf-8')
    has_mobile_bp = bool(re.search(r'@media\s*\(\s*max-width\s*:\s*(?:540|580|600|680|700|768|860)px\s*\)', text))
    check(
        f"{target.name} defines mobile media query breakpoint",
        has_mobile_bp,
        "Missing standard mobile breakpoint (@media max-width: 600px-768px)"
    )

# 4. Multi-Column Grid Collapse
print("\n4. Checking Multi-Column Grid Collapse on Mobile...")
for target in CSS_FILES + [ROOT / 'goodbye.html']:
    text = target.read_text(encoding='utf-8')
    if 'repeat(2,' in text or 'repeat(3,' in text or '1fr 1fr' in text:
        has_collapse = bool(re.search(r'grid-template-columns\s*:\s*(?:1fr|minmax\(0,\s*1fr\))', text))
        check(
            f"{target.name} collapses multi-column grids for mobile",
            has_collapse,
            "Multi-column grid does not define a single-column collapse rule in media queries"
        )

# 5. Accessibility & Asset Safety
print("\n5. Checking Accessibility & Asset Safety...")
for target in CSS_FILES + [ROOT / 'goodbye.html', ROOT / 'site-src/404.template.html']:
    text = target.read_text(encoding='utf-8')
    check(
        f"{target.name} has keyboard focus visible styles",
        ':focus-visible' in text,
        "Missing :focus-visible outline declaration for accessibility"
    )

for target in [ROOT / 'site-src/404.template.html', ROOT / 'goodbye.html']:
    text = target.read_text(encoding='utf-8')
    check(
        f"{target.name} has skip-link for keyboard users",
        'skip-link' in text,
        "Missing .skip-link navigation bypass"
    )
    # Ensure no relative ../assets/ in root HTML files
    check(
        f"{target.name} does not use brittle relative ../assets/ paths",
        '../assets/' not in text,
        "Found brittle relative '../assets/' path; use '/assets/' or inline vector"
    )


# 6. Multi-Screen & Large Display (TV/4K) Invariants
print("\n6. Checking Multi-Screen & TV/4K Invariants...")
editorial_text = (ROOT / "assets/editorial.css").read_text(encoding="utf-8")

# Header max-width capping for 4K / TV screens
header_capped = bool(re.search(r"\.site-header\s*\{[^}]*max-width\s*:\s*1440px", editorial_text))
check(
    "editorial.css .site-header capped at 1440px for 2K/4K/TV screens",
    header_capped,
    "Missing max-width: 1440px on .site-header"
)

# Header language hidden on <= 860px tablet/mobile breakpoint
lang_hidden = bool(re.search(r"@media\s*\(\s*max-width\s*:\s*860px\s*\)[^}]*\.header-language\s*\{[^}]*display\s*:\s*none\s*!important", editorial_text))
check(
    "editorial.css hides .header-language with !important at <= 860px",
    lang_hidden,
    "Missing display: none !important for .header-language under @media (max-width: 860px)"
)

# Small mobile breakpoint (<= 360px)
small_mobile_bp = bool(re.search(r"@media\s*\(\s*max-width\s*:\s*360px\s*\)", editorial_text))
check(
    "editorial.css defines ultra-small mobile breakpoint (<= 360px)",
    small_mobile_bp,
    "Missing @media (max-width: 360px) for iPhone SE 1st gen and narrow Android devices"
)

# Tablet grid accommodation (541px-860px)
tablet_grid = bool(re.search(r"@media\s*\(\s*min-width\s*:\s*541px\s*\)\s*and\s*\(\s*max-width\s*:\s*860px\s*\)", editorial_text))
check(
    "editorial.css defines tablet feature-catalog 2-column layout (541px-860px)",
    tablet_grid,
    "Missing @media (min-width: 541px) and (max-width: 860px) tablet grid rules"
)

# Grid minmax overflow safety
grid_minmax = "grid-template-columns:40px minmax(0,1fr)" in editorial_text
check(
    "editorial.css uses minmax(0, 1fr) on feature-card grid to prevent word blowout",
    grid_minmax,
    "Missing minmax(0, 1fr) on .feature-card grid-template-columns"
)

print("\n" + "=" * 50)
if failures:
    print(f"\n❌ FAILED: {len(failures)} responsive layout check(s) failed:")
    for f in failures:
        print("  " + f)
    sys.exit(1)
else:
    print("🎉 ALL RESPONSIVE LAYOUT & TOKEN INVARIANTS PASSED CLEANLY")
    print("=" * 50 + "\n")
