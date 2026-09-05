#!/usr/bin/env python3
"""Generate the multilingual static site from local templates and dictionaries."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit
import hashlib, html, json, re
ROOT = Path(__file__).resolve().parents[1]
LANGUAGES = {'en':'English','hi':'हिन्दी','de':'Deutsch','es':'Español','fr':'Français','pt-BR':'Português (Brasil)','ja':'日本語','it':'Italiano','ru':'Русский','nl':'Nederlands'}
PAGES = {'home':'','privacy':'privacy/','terms':'terms/','report':'report/','404':'404.html'}
ORIGIN = 'https://blockium.pages.dev'
def route(lang, page):
    return ('/' if lang == 'en' else '/' + lang + '/') + PAGES[page]
def text_key(text):
    return 's_' + hashlib.sha256(text.strip().encode()).hexdigest()[:12]
class Renderer(HTMLParser):
    def __init__(self, lang, page, source, target):
        super().__init__(convert_charrefs=True)
        self.lang, self.page, self.source, self.target = lang, page, source, target
        self.output, self.skip = [], []
    def tr(self, value):
        clean = value.strip()
        key = text_key(clean)
        if key not in self.source: return value
        return value[:len(value)-len(value.lstrip())] + self.target[key] + value[len(value.rstrip()):]
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in ('script','style','code') or 'data-no-translate' in attrs: self.skip.append(tag)
        if not self.skip:
            for attr in ('alt','title','placeholder','aria-label'):
                if attr in attrs: attrs[attr] = self.tr(attrs[attr])
            if tag == 'meta' and (attrs.get('name') in ('description','twitter:title','twitter:description') or attrs.get('property') in ('og:title','og:description')):
                attrs['content'] = self.tr(attrs['content'])
        if tag == 'html': attrs['lang'] = self.lang
        if tag == 'body': attrs.update({'data-locale':self.lang,'data-page':self.page})
        if tag == 'option' and 'data-no-translate' in attrs:
            if attrs.get('value') == self.lang: attrs['selected'] = None
        if tag == 'a' and 'href' in attrs:
            url = urlsplit(attrs['href'])
            known = {'/':'home','/privacy':'privacy','/privacy/':'privacy','/terms':'terms','/terms/':'terms','/report':'report','/report/':'report'}
            if not url.scheme and url.path in known:
                attrs['href'] = route(self.lang,known[url.path]) + ('?'+url.query if url.query else '') + ('#'+url.fragment if url.fragment else '')
        if tag == 'a' and 'data-language-link' in attrs:
            lang = attrs['data-language-link'];attrs['href'] = route(lang,self.page)
            if lang == self.lang: attrs['aria-current'] = 'page'
        for attr in ('src',):
            if attrs.get(attr,'').startswith('assets/'): attrs[attr] = '/' + attrs[attr]
        if tag == 'link' and attrs.get('rel') == 'icon' and attrs.get('href','').startswith('assets/'):
            attrs['href'] = '/' + attrs['href']
        if tag == 'a' and attrs.get('href','').startswith('assets/'): attrs['href'] = '/' + attrs['href']
        if tag == 'link' and attrs.get('rel') == 'canonical': attrs['href'] = ORIGIN + route(self.lang,self.page)
        if tag == 'meta' and attrs.get('property') == 'og:url': attrs['content'] = ORIGIN + route(self.lang,self.page)
        self.output.append('<'+tag+''.join(' '+key if value is None else ' '+key+'="'+html.escape(value,quote=True)+'"' for key,value in attrs.items())+'>')
    def handle_endtag(self, tag):
        self.output.append('</'+tag+'>')
        if self.skip and self.skip[-1] == tag: self.skip.pop()
    def handle_data(self, value):
        self.output.append(value if self.skip else html.escape(self.tr(value),quote=False))
    def handle_comment(self, value): self.output.append('<!--'+value+'-->')
    def handle_decl(self, value): self.output.append('<!'+value+'>')
def build():
    source = json.loads((ROOT/'locales/en.json').read_text())
    urls = []
    for lang in LANGUAGES:
        target = json.loads((ROOT/'locales'/f'{lang}.json').read_text())
        if set(target) != set(source) or not all(isinstance(v,str) and v.strip() for v in target.values()):
            raise ValueError(f'{lang}: missing, extra, or empty translations')
        for page in PAGES:
            parser = Renderer(lang,page,source,target)
            parser.feed((ROOT/'site-src'/f'{page}.template.html').read_text())
            document = ''.join(parser.output)
            alternates = ''.join(f'<link rel="alternate" hreflang="{code}" href="{ORIGIN}{route(code,page)}">\n' for code in LANGUAGES)
            alternates += f'<link rel="alternate" hreflang="x-default" href="{ORIGIN}{route("en",page)}">\n'
            document = document.replace('</head>',alternates+'</head>')
            # Keep structured data aligned with the rendered locale.
            def schema(match):
                data = json.loads(match[1]);data['inLanguage'] = lang;data['url'] = ORIGIN+route(lang,page)
                desc = re.search(r'<meta name="description" content="([^"]*)"',document)
                if desc: data['description'] = html.unescape(desc[1])
                data.pop('featureList',None)
                return '<script type="application/ld+json">'+json.dumps(data,ensure_ascii=False).replace('<','\\u003c')+'</script>'
            document = re.sub(r'<script type="application/ld\+json">(.*?)</script>',schema,document,flags=re.S)
            dynamic = {text:target[text_key(text)] for text in ('Submitting...','Report Submitted','Submit Report')}
            document = document.replace('</head>','<script type="application/json" id="locale-messages">'+json.dumps(dynamic,ensure_ascii=False).replace('<','\\u003c')+'</script>\n</head>')
            # Links remain usable without scripting.
            fallback = '<noscript><nav class="language-grid" aria-label="'+html.escape(target[text_key('Website language')])+'">'+''.join(f'<a href="{route(code,page)}" lang="{code}">{label}</a>' for code,label in LANGUAGES.items())+'</nav></noscript>'
            document = document.replace('</body>',fallback+'</body>')
            document = '\n'.join(line.rstrip() for line in document.splitlines())+'\n'
            path = route(lang,page).lstrip('/')
            if path.endswith('/') or not path: path += 'index.html'
            dest = ROOT/path;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(document)
            if lang == 'en' and page in ('privacy','terms','report'): (ROOT/(page+'.html')).write_text(document)
            if page != '404': urls.append(ORIGIN+route(lang,page))
    (ROOT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join('<url><loc>'+url+'</loc></url>\n' for url in urls)+'</urlset>\n')
    print(f'Built {len(LANGUAGES)*len(PAGES)} pages in {len(LANGUAGES)} languages; no network requests.')
if __name__ == '__main__': build()
