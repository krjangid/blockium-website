# Website languages

English remains at `/`. Translated pages use `/hi/`, `/de/`, `/es/`, `/fr/`, `/pt-BR/`, `/ja/`, `/it/`, `/ru/`, and `/nl/`.
Each language includes Home, Privacy, Terms, Report, and a 404 page. Product screenshots remain the original English screenshots with localized descriptions.

## Edit and rebuild

Edit `site-src/*.template.html` for shared markup. Edit `locales/*.json` for translations. Text keys are `s_` plus the first 12 characters of the SHA-256 hash of the trimmed English text. Add changed text to every dictionary; unchanged text keeps its key.

Run `python3 scripts/build-locales.py` from the website folder. The build uses only Python's standard library, makes no network requests, and checks dictionary parity. It writes static pages, language alternates, canonical URLs, and the sitemap. Root `.html` aliases for Privacy, Terms, and Report are kept in sync.

Run `python3 scripts/check-locales.py` for route, asset, anchor, and translation checks.

## Behavior and review

The selector preserves the current page, query string, and anchor. It stores the selected language locally. A dismissible suggestion offers the saved or browser language; no automatic redirect occurs. Native language links remain usable without JavaScript. Report submission values and destination are unchanged; only labels and messages are translated.

Translations were authored locally by the assistant, not sent to a translation service. They are complete drafts for local testing, not certified translations. Native-language review, particularly of Privacy and Terms, remains advisable before publishing. No claim of legal validation is made.
