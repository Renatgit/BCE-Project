async function loadPartials() {
  const header = await fetch('/partials/header.html').then(res => res.text());
  const footer = await fetch('/partials/footer.html').then(res => res.text());

  document.getElementById('header').innerHTML = header;
  document.getElementById('footer').innerHTML = footer;
}

window.addEventListener('DOMContentLoaded', loadPartials);

window.addEventListener('load', () => {
  const currentPage = window.location.pathname.split("/").pop();
  const navLinks = document.querySelectorAll(".navbar-link");
  console.log(navLinks);
  navLinks.forEach(link => {
    const linkPage = link.getAttribute("href");
    console.log(linkPage);
    console.log(currentPage);
    if((linkPage === currentPage) || (currentPage === "" && linkPage === "index.html")){
      link.classList.add("active");
    }
  })
})