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
const thumbsUp = document.querySelector(".fa-thumbs-up");

const defaultCTAButton = function () {
  buttonSubmit.innerHTML = `Yes, I want free coffee! <i class="far fa-thumbs-up"></i>`;
}

const showToastify = (text, styleBackground) => {
  Toastify({
    text: text,
    duration: 3000,
    close: false,
    gravity: "bottom", // `top` or `bottom`
    position: "right", // `left`, `center` or `right`
    stopOnFocus: true, // Prevents dismissing of toast on hover
    style: {
      background: styleBackground,
    },
  }).showToast();
}

const resetForm = () => {
  firstNameInput.value = "";
  lastNameInput.value = "";
  emailInput.value = "";
}
  
const submitHandler = (e) => {
  e.preventDefault();
  let formIsInvalid =
    firstNameInput.value === "" ||
    lastNameInput.value === "" ||
    emailInput.value === "" ||
    !emailInput.value.includes("@");
  if (formIsInvalid) {
    showToastify(
      "Sorry can not process ☹️, check your the form again!",
      "linear-gradient(to right, #aa0000, #fe0000)"
    )
    return;
  }
  thumbsUp.classList.add("d-none");
  buttonSubmit.innerHTML = `
    Processing... 
    <div id="spinner" class="spinner-border text-light spinner-border-sm" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>`;
  const csrfToken = "{{ csrf_token() }}"
  let data = {
    firstname: firstNameInput.value,
    lastname: lastNameInput.value,
    email: emailInput.value,
  };
  fetch(`${window.origin}/api/newsletter`, {
    method: "POST",
    body: JSON.stringify(data),
    headers: {
      "X-CSRFToken" : csrfToken,
      "Content-Type": "application/json",
    },
  }).then((res) => {
    if (res.ok) {
      showToastify(
        `Wohoo! ${data.firstname} 😄, you have subscribed our newsletter!`,
        "linear-gradient(to right, #00b09b, #96c93d)"
      )
      defaultCTAButton();
      resetForm();
    } else if (res.status === 409) {
      showToastify(
        `Sorry 😔, that email already exists!`,
        "linear-gradient(to right, #aa0000, #fe0000)"
      )
      defaultCTAButton();
    // } else if (res.status === 400) {
    //   showToastify(
    //     `Bad request, form is invalid! Check the input!`,
    //     "linear-gradient(to right, #aa0000, #fe0000)"
    //   )
    //   defaultCTAButton();
    } 
    else {
      defaultCTAButton();
      throw new Error("Something went wrong!");
    }
  }).catch((err)=> {
    showToastify(
      `Sorry 😔, something went wrong ${err}!`,
      "linear-gradient(to right, #aa0000, #fe0000)"
    )
    defaultCTAButton();
  });
};

buttonSubmit.addEventListener("click", submitHandler);

//  Footer Copyright
const spanCopyright = document.querySelector(".copyright");
const year = new Date().getFullYear()
spanCopyright.textContent = `© Coffee & Joy - ${year}`
