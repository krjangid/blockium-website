(() => {
  'use strict';
  const bar = document.querySelector('.mobile-install');
  const hero = document.querySelector('.hero-section');
  if (!bar || !hero || !('IntersectionObserver' in window)) return;
  const observer = new IntersectionObserver(([entry]) => {
    bar.hidden = entry.isIntersecting || entry.boundingClientRect.bottom > 0;
  });
  observer.observe(hero);
  window.addEventListener('pagehide', () => observer.disconnect());
  window.addEventListener('pageshow', event => { if (event.persisted) observer.observe(hero); });
})();
