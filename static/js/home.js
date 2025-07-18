let navItems = document.getElementsByClassName("nav-items");
let navElements = document.getElementsByClassName("nav-elements");
let profile = document.getElementById("profile");

navItems[0].style.color = "blue";
navItems[0].style.background = "skyblue";

Array.from(navItems).forEach((item, index) => {
  item.addEventListener("click", (event) => {
    Array.from(navItems).forEach((item, index) => {
      item.style.color = "";
      item.style.background = "";
      navElements[index].style.fontWeight = "";
    });

    let e = event.target;
    let ec = event.currentTarget;
    if (e.closest(".nav-items")) {
      ec.style.color = "blue";
      ec.style.background = "skyblue";
    }
  });
});
