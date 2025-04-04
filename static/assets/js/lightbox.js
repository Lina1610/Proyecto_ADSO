// script.js

function openLightbox() {
    document.getElementById('lightbox').style.display = 'flex';
}

function closeLightbox() {
    document.getElementById('lightbox').style.display = 'none';
}

// Cerrar el Lightbox si se hace clic fuera del contenido
window.onclick = function(event) {
    const lightbox = document.getElementById('lightbox');
    if (event.target === lightbox) {
        closeLightbox();
    }
}

function checkScroll() {
    let elemento = document.querySelector(".historia-tamal");
    let posicion = elemento.getBoundingClientRect().top;
    let pantalla = window.innerHeight;
    if (posicion < pantalla * 0.8) {
      elemento.classList.add("aparece");
    }
  }
  window.addEventListener("scroll", checkScroll);
  checkScroll();
