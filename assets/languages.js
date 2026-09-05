(() => {
  'use strict';
  const names = {en:'English',hi:'हिन्दी',de:'Deutsch',es:'Español',fr:'Français','pt-BR':'Português (Brasil)',ja:'日本語',it:'Italiano',ru:'Русский',nl:'Nederlands'};
  const locale = document.documentElement.lang;
  const page = document.body.dataset.page;
  const paths = {home:'',privacy:'privacy/',terms:'terms/',report:'report/','404':'404.html'};
  const messages = JSON.parse(document.getElementById('locale-messages').textContent);
  window.BlockiumLanguage = {text: value => messages[value] || value};
  function read(key) { try { return localStorage.getItem(key); } catch { return null; } }
  function save(key, value) { try { localStorage.setItem(key, value); } catch {} }
  function path(lang) { return (lang === 'en' ? '/' : `/${lang}/`) + (paths[page] || '') + location.search + location.hash; }
  document.querySelectorAll('.language-select').forEach(select => {
    select.value = locale;
    select.addEventListener('change', () => {
      if (!Object.hasOwn(names, select.value)) return;
      save('blockium-language', select.value);
      location.assign(path(select.value));
    });
  });
  document.querySelectorAll('[data-language-link]').forEach(link => {
    link.href = path(link.dataset.languageLink);
    link.addEventListener('click', () => save('blockium-language', link.dataset.languageLink));
  });
  function match(value) {
    const code = (value || '').toLowerCase();
    if (code.startsWith('pt')) return 'pt-BR';
    return Object.keys(names).find(lang => lang.toLowerCase() === code) || (Object.hasOwn(names,code.split('-')[0]) ? code.split('-')[0] : null);
  }
  const preferred = match(read('blockium-language')) || (navigator.languages || [navigator.language]).map(match).find(Boolean);
  const banner = document.querySelector('.language-suggestion');
  if (banner && preferred && preferred !== locale && read('blockium-language-dismissed') !== `${locale}:${preferred}`) {
    const link = banner.querySelector('.suggested-language');
    link.textContent = names[preferred]; link.lang = preferred; link.href = path(preferred);
    link.addEventListener('click', () => save('blockium-language', preferred));
    banner.hidden = false;
    banner.querySelector('button').addEventListener('click', () => {
      save('blockium-language-dismissed', `${locale}:${preferred}`); banner.hidden = true;
    });
  }
})();
