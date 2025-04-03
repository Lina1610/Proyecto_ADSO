// Función para manejar el envío del formulario de manera asíncrona
function setupFormSubmit() {
    const formInfoPersonal = document.getElementById("formInfoPersonal");

    if (formInfoPersonal) {
        formInfoPersonal.addEventListener("submit", function (e) {
            e.preventDefault(); // Evita el envío tradicional del formulario

            // Captura los datos del formulario
            const formData = new FormData(formInfoPersonal);

            // Envía los datos usando Fetch API
            fetch("/actualizar-datos-perfil", {
                method: "POST",
                body: formData,
            })
                .then((response) => response.json())
                .then((data) => {
                    if (data.success) {
                        alert("Datos actualizados correctamente.");
                    } else {
                        alert("Error al actualizar los datos: " + data.message);
                    }
                })
                .catch((error) => {
                    console.error("Error:", error);
                    alert("Ocurrió un error al enviar el formulario.");
                });
        });
    }
}

// Inicializamos las funciones cuando el DOM esté listo
document.addEventListener("DOMContentLoaded", function () {
    setupCollapsibles(); // Configurar colapsables
    setupHamburgerMenu(); // Configurar menú hamburguesa
    setupPasswordToggle(); // Configurar alternar contraseña
    setupFormSubmit(); // Configurar envío del formulario
});


document.addEventListener("DOMContentLoaded", function() {
    const botonAgregarDireccion = document.querySelector("[data-bs-target='#modalNuevaDireccion']");

    if (botonAgregarDireccion) {
        botonAgregarDireccion.addEventListener("click", function() {
            console.log("Abriendo modal de nueva dirección...");
        });
    } else {
        console.error("El botón para agregar dirección no se encontró.");
    }
});
