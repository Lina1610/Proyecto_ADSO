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