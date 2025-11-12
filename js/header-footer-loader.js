async function loadPartials() {
  const header = await fetch('/partials/header.html').then(res => res.text());
  const footer = await fetch('/partials/footer.html').then(res => res.text());

  document.getElementById('header').innerHTML = header;
  document.getElementById('footer').innerHTML = footer;

  
  document.dispatchEvent(new Event('headerLoaded'));
}

window.addEventListener('DOMContentLoaded', loadPartials);

document.addEventListener('headerLoaded', () => {
  const currentPage = window.location.pathname.split("/").pop();
  const navLinks = document.querySelectorAll(".navbar-link");

  navLinks.forEach(link => {
    const linkPage = link.getAttribute("href");
    const linkPageSub = linkPage.substring(1);
    console.log(linkPageSub);
    if (linkPageSub === currentPage || (linkPageSub === "" && linkPageSub === "index.html")) {
      link.classList.add("active");
    }
  });
});