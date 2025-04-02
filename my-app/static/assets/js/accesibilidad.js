// Crear un elemento <script> para cargar la librería de accesibilidad
const script = document.createElement("script");
script.src = "/static/node_modules/accessibility/dist/main.bundle.js";
script.type = "text/javascript";
document.head.appendChild(script);

// Cuando el script se haya cargado, ejecutar configuraciones adicionales
script.onload = function () {
    console.log("Accesibilidad cargada correctamente");
    
    // Configuración opcional de la librería si es necesario
    if (window.accessibility) {
        window.accessibility({
            language: 'es', // Cambia el idioma si es necesario
            icon: {
                position: 'bottom-right', // Posición del icono de accesibilidad
                color: 'blue', // Color del icono
            },
            labels: {
                resetTitle: 'Restablecer ajustes',
                closeTitle: 'Cerrar accesibilidad'
            }
        });
    } else {
        console.warn("La librería de accesibilidad no se pudo inicializar.");
    }
};
