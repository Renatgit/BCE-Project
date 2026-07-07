// Student ID: 25060488
// Name: Renat Bershadskyi
// Wait until the page and Swiper are fully loaded
window.addEventListener("load", () => {
  const swiper = new Swiper(".swiper", {
    // Core config
    slidesPerView: 3,
    spaceBetween: 30,
    loop: true,
    centeredSlides: true,
    grabCursor: true,

    // Navigation
    navigation: {
      nextEl: ".custom-next",
      prevEl: ".custom-prev",
    },

    // Autoplay
    autoplay: {
      delay: 3000,
      disableOnInteraction: false,
    },

    // // Responsive breakpoints
    // breakpoints: {
    //   768: { slidesPerView: 2}
    // },

    // Smooth transition
    speed: 700,
    effect: "slide",
  });
});