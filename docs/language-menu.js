const languageMenu = document.querySelector('.language-switch');
if (languageMenu) {
  document.addEventListener('click', event => {
    if (!languageMenu.contains(event.target)) languageMenu.open = false;
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && languageMenu.open) {
      languageMenu.open = false;
      languageMenu.querySelector('summary').focus();
    }
  });
  languageMenu.querySelectorAll('[data-language]').forEach(link => {
    link.addEventListener('click', () => {
      link.href = link.getAttribute('href').split('#')[0] + '#top';
    });
  });
}
