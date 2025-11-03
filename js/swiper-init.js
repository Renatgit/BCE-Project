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

    // Responsive breakpoints
    breakpoints: {
      0: { slidesPerView: 1, spaceBetween: 10 },
      768: { slidesPerView: 2, spaceBetween: 20 },
      1024: { slidesPerView: 3, spaceBetween: 30 },
    },

    // Smooth transition
    speed: 700,
    effect: "slide",
  });
});