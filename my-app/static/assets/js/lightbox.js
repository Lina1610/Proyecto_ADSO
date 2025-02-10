const images = document.querySelectorAll('.img');
const containerImage = document.querySelector('.container-img');
const imageContainer = document.querySelector('.img-show'); // Ahora es un <img>
const closeIcon = document.querySelector('.bx-x');
const copy = document.querySelector('.copy');

images.forEach(image => {
    image.addEventListener('click', () => {
        addImage(image.getAttribute('src'), image.getAttribute('alt'));
    });
});

const addImage = (src, alt) => {
    containerImage.classList.add('move'); // Muestra el contenedor
    imageContainer.classList.add('show'); // Muestra la imagen
    imageContainer.src = src; // Asigna la imagen al <img>
    copy.innerHTML = alt; // Muestra el texto del atributo alt
};

closeIcon.addEventListener('click', () => {
    containerImage.classList.remove('move'); // Oculta el contenedor
    imageContainer.classList.remove('show'); // Oculta la imagen
});
function playVideo() {
    let video = document.getElementById("tamalesVideo");
    let playBtn = document.getElementById("playBtn");

    if (video.paused) {
        video.play();
        playBtn.style.display = "none"; // Oculta el botón al reproducir
    } else {
        video.pause();
        playBtn.style.display = "block"; // Muestra el botón si se pausa
    }
}

