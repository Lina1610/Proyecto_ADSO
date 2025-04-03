const imagenes = document.querySelector('.img');

imagenes.forEach(image =>{
    image.addEventListener('click', ()=>{
        alert("Has dado click")
    })
})