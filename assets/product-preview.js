(() => {
  const dialog = document.getElementById('screenshot-preview');
  if (!dialog || typeof dialog.showModal !== 'function') return;
  const image = document.getElementById('preview-image');
  let previousOverflow = '';
  document.querySelectorAll('.screenshot-link').forEach(link => {
    link.addEventListener('click', event => {
      if (event.button || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      const original = link.querySelector('img') || link.closest('.product-panel')?.querySelector('img');
      image.src = link.href;
      image.alt = original?.alt || document.getElementById('preview-title').textContent;
      previousOverflow = document.body.style.overflow;
      document.body.style.overflow = 'hidden';
      dialog.showModal();
    });
  });
  dialog.addEventListener('close', () => { document.body.style.overflow = previousOverflow; });
  dialog.addEventListener('click', event => {
    const rect = dialog.getBoundingClientRect();
    if (event.target === dialog && (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom)) dialog.close();
  });
})();
