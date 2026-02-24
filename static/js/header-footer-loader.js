async function loadPartials() {
  const headerElem = document.getElementById('header');
  const footerElem = document.getElementById('footer');

  // nothing to do if neither placeholder exists
  if (!headerElem && !footerElem) return;

  if (headerElem) {
    try {
      const header = await fetch('/partials/header.html').then(res => res.text());
      headerElem.innerHTML = header;
    } catch (e) {
      console.warn('could not load header partial:', e);
    }
  }

  if (footerElem) {
    try {
      const footer = await fetch('/partials/footer.html').then(res => res.text());
      footerElem.innerHTML = footer;
    } catch (e) {
      console.warn('could not load footer partial:', e);
    }
  }

  document.dispatchEvent(new Event('headerLoaded'));
}

window.addEventListener('DOMContentLoaded', () => {
  loadPartials();
  highlightCurrent();
});

document.addEventListener('headerLoaded', highlightCurrent);

function highlightCurrent() {
  // normalize current path (remove trailing slash)
  let path = window.location.pathname.replace(/\/+$|^$/g, '');
  if (path === '') path = '/';          // root
  // treat bare root and /index as same page
  if (path === '/') path = '/index';

  const navLinks = document.querySelectorAll(".navbar-link");
  navLinks.forEach(link => {
    const href = link.getAttribute("href");
    let normHref = href.replace(/\/+$|^$/g, '');
    if (normHref === '') normHref = '/';

    if (path === normHref || (normHref !== '/' && path.startsWith(normHref + '/')) ) {
      link.classList.add("active");
    }
  });

  const authBtns = document.querySelectorAll(".authBtn");
  if (!authBtns.length) return;

  // Default behaviour (Login on every page)
  let label = "Login";
  let target = "/login";

  // update depending on (normalized) path
  if (path === "/login") {
    label = "Sign Up";
    target = "/signup";
  } else if (path === "/account") {
    label = "My Account";
    target = "/account";
  }

  authBtns.forEach(btn => {
    btn.textContent = label;
    btn.onclick = () => {
      window.location.href = target;
    };
  });
}