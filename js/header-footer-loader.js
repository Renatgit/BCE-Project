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
    // console.log(linkPageSub);
    if (linkPageSub === currentPage || (currentPage === "" && linkPageSub === "index.html")) {
      link.classList.add("active");
    }
  });

  const authBtns = document.querySelectorAll(".authBtn");
  if (!authBtns.length) return;
  
  // Default behaviour (Login on every page)
  let label = "Login";
  let target = "login.html";

  // On login page show Sign up
  if (currentPage === "login.html") {
    label = "Sign Up";
    target = "signUp.html";
  }
  if(currentPage === "account.html"){
    label = "My Account"
    target = "account.html";
  }
  authBtns.forEach(btn => {
    btn.textContent = label;
    btn.onclick = () => {
      window.location.href = target;
    }
  }
  );
});