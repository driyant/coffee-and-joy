// Target navlinks
const navlinks = document.querySelector(".nav__links");
const hamburger = document.querySelector(".hamburger");

// Callback function
const toggleMenuOpen = () => {
  navlinks.classList.toggle("open");
  hamburger.classList.toggle("open");
}
hamburger.addEventListener("click", toggleMenuOpen);

const removeOpen = () => {
  setTimeout(() => {
    navlinks.classList.remove("open");
    hamburger.classList.remove("open");
  }, 400);
}
const navLists = document.querySelectorAll(".nav__links li");
navLists.forEach(navList => {
  navList.addEventListener("click", removeOpen);
});
