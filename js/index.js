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

// Filterlist
const menuLinks = document.querySelector(".menu__links");
const menuLists = menuLinks.querySelectorAll("li");
const menus = document.querySelectorAll(".menu");

menuLists.forEach(menuList => {
  menuList.addEventListener("click", (e) => {
     menuLists.forEach(list => {
      list.classList.remove("active");
      e.target.classList.add("active");
    });
    menus.forEach(menu => {
      menu.style.display = "none";
      let singleItem = menuList.textContent.toLowerCase();
      if(menu.getAttribute("data-category") === singleItem || singleItem == "all") {
        menu.style.display = "block";
      }
    });
  });
});


