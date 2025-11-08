async function loadPartials() {
  const header = await fetch('/partials/header.html').then(res => res.text());
  const footer = await fetch('/partials/footer.html').then(res => res.text());

  document.getElementById('header').innerHTML = header;
  document.getElementById('footer').innerHTML = footer;
}

window.addEventListener('DOMContentLoaded', loadPartials);