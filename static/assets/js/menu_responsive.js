document.addEventListener("DOMContentLoaded", function () {
    const menuCheckbox = document.getElementById("menu");
    const navLinks = document.querySelectorAll(".navbar-nav .nav-link");
  
    navLinks.forEach(link => {
      link.addEventListener("click", () => {
        menuCheckbox.checked = false; // Cierra el menú al hacer clic en un enlace
      });
    });
  });
  