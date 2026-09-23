# Ivory editorial design preview

Branch: `codex/ivory-editorial-redesign`. No deployment or PR.

Run from this folder:

```sh
python3 -m http.server 4175 --bind 127.0.0.1
```

Open http://127.0.0.1:4175/ . Stop with Ctrl+C.

Check desktop/mobile layouts, Menu and Escape, product tabs and arrow keys, screenshot previews and Escape, FAQ, language links, and Privacy/Terms/Report routes. Installation links open the real store. Do not submit the report form for testing: it uses the existing live endpoint.

Edit `site-src/home.template.html` and `assets/editorial.css`, then run:

```sh
python3 scripts/build-locales.py
python3 scripts/check-locales.py
```

The hero illustration `assets/editorial-shield.jpg` is a compressed AI-generated concept asset. Product screenshots are unchanged. New translated headlines are draft translations and should receive native-language review before release.
