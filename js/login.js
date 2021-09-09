const btn = document.querySelector(".btn");

const pulseOn = () => {
  btn.classList.add("animate__heartBeat");
}

const pulseOff = () => {
  btn.classList.remove("animate__heartBeat")
}

btn.addEventListener("mouseover", pulseOn);
btn.addEventListener("mouseout", pulseOff);