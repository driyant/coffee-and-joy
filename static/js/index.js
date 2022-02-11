/*
 * Toggle hamburger menu for mobile and tablet screen
 */

// Target navlinks
const navlinks = document.querySelector(".nav__links");
const hamburger = document.querySelector(".hamburger");

// Callback function
const toggleMenuOpen = () => {
  navlinks.classList.toggle("open");
  hamburger.classList.toggle("open");
};
hamburger.addEventListener("click", toggleMenuOpen);

const removeOpen = () => {
  setTimeout(() => {
    navlinks.classList.remove("open");
    hamburger.classList.remove("open");
  }, 400);
};
const navLists = document.querySelectorAll(".nav__links li");
navLists.forEach((navList) => {
  navList.addEventListener("click", removeOpen);
});

/*
 * Filterlist our menu category
 */

// Filterlist
const menuLinks = document.querySelector(".menu__links");
const menuLists = menuLinks.querySelectorAll("li");
const menus = document.querySelectorAll(".menu");

menuLists.forEach((menuList) => {
  menuList.addEventListener("click", (e) => {
    e.preventDefault();
    menuLists.forEach((list) => {
      list.classList.remove("active");
      e.target.classList.add("active");
    });
    menus.forEach((menu) => {
      menu.style.display = "none";
      let singleItem = menuList.textContent.toLowerCase();
      if (
        menu.getAttribute("data-category") === singleItem ||
        singleItem == "all"
      ) {
        menu.style.display = "block";
      }
    });
  });
});

/*
 * Count down timer
 */

// Target date element
const dateEvent = document.querySelector(".date_end_event");
const timeEvent = document.querySelector(".time_end_event");

// Set the date we're counting down
const getNewDate = new Date(
  `${dateEvent.innerText} ${timeEvent.innerText}`
).getTime();

const countDown = () => {
  setInterval(() => {
    const getNow = new Date().getTime();
    const distance = getNewDate - getNow;
    const days = Math.floor(distance / (1000 * 60 * 60 * 24));
    const hours = Math.floor(
      (distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)
    );
    const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((distance % (1000 * 60)) / 1000);
    const getElementH1 = document.querySelector(".time__remaining h1");
    getElementH1.innerHTML = `${days} DAYS : ${hours} HOURS : ${minutes} MINUTES : ${seconds} SECONDS`;

    if (distance < 0) {
      clearInterval(countDown);
      getElementH1.innerHTML = `Event promo is finished!`;
    }
  });
};

if (dateEvent.innerText && timeEvent.innerText !== "") {
  countDown();
}
// Aos Scroll
AOS.init({
  once: true,
  easing: "ease",
  delay: 400,
});

// Rertieve input from Newsletter form
const firstNameInput = document.querySelector(".firstname");
const lastNameInput = document.querySelector(".lastname");
const emailInput = document.querySelector(".email");
const buttonSubmit = document.querySelector(".cta__subscribe");

const submitHandler = (e) => {
  e.preventDefault();
  let formIsInvalid = 
    firstNameInput.value === "" || 
    lastNameInput.value === "" || 
    emailInput.value === "" || 
    !emailInput.value.includes("@");
  if (formIsInvalid) {
    Toastify({
      text: `Sorry cannot process ☹️, check your the form again!`,
      duration: 3000,
      close: false,
      gravity: "bottom", // `top` or `bottom`
      position: "right", // `left`, `center` or `right`
      stopOnFocus: true, // Prevents dismissing of toast on hover
      style: {
        background: "linear-gradient(to right, #aa0000, #fe0000)",
      },
    }).showToast();
    return;
  }
  let data = {
    "firstname" : firstNameInput.value,
    "lastname" : lastNameInput.value,
    "email" : emailInput.value
  }
  console.log(data);
};

buttonSubmit.addEventListener("click", submitHandler);
