// Student ID: 25060488
// Name: Renat Bershadskyi
window.addEventListener('DOMContentLoaded', () => {
  highlightCurrent();
});

function highlightCurrent() {
  let path = window.location.pathname.replace(/\/+$|^$/g, '');
  if (path === '') path = '/';
  if (path === '/') path = '/index';

  const navLinks = document.querySelectorAll(".navbar-link");
  navLinks.forEach(link => {
    const href = link.getAttribute("href");
    let normHref = href.replace(/\/+$|^$/g, '');
    if (normHref === '') normHref = '/';

    if (path === normHref || (normHref !== '/' && path.startsWith(normHref + '/'))) {
      link.classList.add("active");
    }
  });
}