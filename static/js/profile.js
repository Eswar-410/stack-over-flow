let navItems = document.getElementsByClassName("nav-items");
let navElements = document.getElementsByClassName("nav-elements");

for (let index = 0; index < navElements.length; index++) {
  if (navElements[index].textContent !== "Profile") {
    navItems[index].style.color = "";
    navItems[index].style.background = "";
  } else {
    navItems[index].style.color = "blue";
    navItems[index].style.background = "skyblue";
  }
}
