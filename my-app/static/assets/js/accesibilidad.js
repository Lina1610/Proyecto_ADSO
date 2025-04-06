// Verificar si la biblioteca ya está cargada
if (typeof window.Accessibility === 'undefined') {
    // Crear un elemento <script> para cargar la librería de accesibilidad
    const script = document.createElement("script");
    // Usar una CDN para asegurar que se carga correctamente
    script.src = "https://cdnjs.cloudflare.com/ajax/libs/accessibility/3.0.0/accessibility.min.js";
    script.type = "text/javascript";
    document.head.appendChild(script);

    // Cuando el script se haya cargado, ejecutar configuraciones
    script.onload = function () {
        console.log("Accesibilidad cargada correctamente");
        inicializarAccesibilidad();
    };
} else {
    // Si ya está cargada, solo inicializar
    inicializarAccesibilidad();
}

function inicializarAccesibilidad() {
    try {
        window.accessibility = new Accessibility({
            language: 'es',
            icon: {
                position: 'center',
                color: 'blue',
            },
            labels: {
                resetTitle: 'Restablecer ajustes',
                closeTitle: 'Cerrar accesibilidad'
            }
        });
        console.log("Accesibilidad inicializada con éxito");
    } catch (error) {
        console.error("Error al inicializar accesibilidad:", error);
    }
}

// Inicializar también cuando el DOM esté completamente cargado
document.addEventListener('DOMContentLoaded', function() {
    if (typeof window.Accessibility !== 'undefined') {
        inicializarAccesibilidad();
    }
});