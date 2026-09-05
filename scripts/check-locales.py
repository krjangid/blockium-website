#!/usr/bin/env python3
"""Check generated pages without network access or dependencies."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import importlib.util, json, re, subprocess, tempfile
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('build', ROOT/'scripts/build-locales.py');build=importlib.util.module_from_spec(spec);spec.loader.exec_module(build)
class Page(HTMLParser):
 def __init__(self,text):
  super().__init__();self.ids=[];self.links=[];self.lang=None;self.alts=0;self.stack=[];self.feed(text);assert not self.stack,self.stack
 def handle_starttag(self,t,a):
  d=dict(a)
  if t=='html':self.lang=d['lang']
  if 'id' in d:self.ids.append(d['id'])
  for attr in ['href','src']:
   if attr in d:self.links.append(d[attr])
  if t=='link' and d.get('rel')=='alternate':self.alts+=1
  if t not in ['area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr']:self.stack.append(t)
 def handle_endtag(self,t):
  assert self.stack and self.stack[-1]==t,(t,self.stack[-3:]);self.stack.pop()
count=0
source=json.loads((ROOT/'locales/en.json').read_text())
for lang in build.LANGUAGES:
 dictionary=json.loads((ROOT/'locales'/f'{lang}.json').read_text());assert set(dictionary)==set(source)
 for name in build.PAGES:
  relative=build.route(lang,name).lstrip('/');relative += 'index.html' if not relative or relative.endswith('/') else ''
  file=ROOT/relative;text=file.read_text();p=Page(text)
  assert p.lang==lang and p.alts==11 and len(p.ids)==len(set(p.ids)),file
  for link in p.links:
   u=urlsplit(link)
   if u.scheme or u.netloc:continue
   target=(ROOT/u.path.lstrip('/')) if u.path.startswith('/') else (file.parent/u.path)
   if target.is_dir():target=target/'index.html'
   if not u.path:target=file
   assert target.exists(),(file,link)
   if u.fragment:assert unquote(u.fragment) in Page(target.read_text()).ids,(file,link)
  for attrs,code in re.findall(r'<script([^>]*)>(.*?)</script>',text,re.S):
   if 'json' in attrs:json.loads(code)
  if name=='home':assert text.count('class="feature-card"')==12
  count+=1
for path in (ROOT/'assets/languages.js',):subprocess.run(['node','--check',str(path)],check=True)
print(f'PASS: {count} pages; 10 complete dictionaries; local routes, assets, anchors, HTML, metadata and script syntax.')
