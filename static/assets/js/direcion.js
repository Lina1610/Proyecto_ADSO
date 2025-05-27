// Script específico para el manejo de direcciones (direcciones.js)

document.addEventListener("DOMContentLoaded", function() {
    // Listener para el cambio de departamento (carga municipios)
    const departamentoSelect = document.getElementById('registrarDepartamentoId');
    if (departamentoSelect) {
        departamentoSelect.addEventListener('change', function() {
            const departamentoId = this.value;
            cargarMunicipios(departamentoId);
        });
    }

    // Inicializar el formulario de registro de dirección
    const formRegistrarDireccion = document.getElementById('formRegistrarDireccion');
    if (formRegistrarDireccion) {
        formRegistrarDireccion.addEventListener('submit', registrarDireccion);
    }
});

// Función para cargar municipios basados en el departamento seleccionado
function cargarMunicipios(departamentoId) {
    const municipioSelect = document.getElementById('registrarMunicipioId');
    
    if (!departamentoId) {
        municipioSelect.innerHTML = '<option value="">Seleccione un municipio</option>';
        return;
    }
    
    // Mostrar cargando
    municipioSelect.innerHTML = '<option value="">Cargando municipios...</option>';
    
    // Realizar solicitud AJAX para obtener municipios
    fetch(`/obtener_municipios?departamento_id=${departamentoId}`)
        .then(response => response.json())
        .then(municipios => {
            municipioSelect.innerHTML = '<option value="">Seleccione un municipio</option>';
            municipios.forEach(municipio => {
                municipioSelect.innerHTML += `<option value="${municipio.id}">${municipio.nombre}</option>`;
            });
        })
        .catch(error => {
            console.error('Error al cargar municipios:', error);
            municipioSelect.innerHTML = '<option value="">Error al cargar municipios</option>';
        });
}

// Función para registrar una nueva dirección
function registrarDireccion(event) {
    event.preventDefault();
    
    // Obtener el formulario y sus datos
    const form = event.target;
    const formData = new FormData(form);
    
    // Validar campos requeridos
    let valido = true;
    form.querySelectorAll("input[required], select[required]").forEach(input => {
        if (!input.value.trim()) {
            valido = false;
            input.classList.add("is-invalid");
        } else {
            input.classList.remove("is-invalid");
        }
    });
    
    if (!valido) {
        mostrarNotificacion('Por favor, complete todos los campos requeridos', 'error');
        return;
    }
    
    // Enviar datos al servidor
    fetch("/registrar-direccion", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // Cerrar el modal
        const modalElement = document.getElementById('modalAgregarDireccion');
        const modal = bootstrap.Modal.getInstance(modalElement);
        if (modal) modal.hide();
        
        // Mostrar notificación según resultado
        if (data.success) {
            mostrarNotificacion(data.message || 'Dirección registrada con éxito', 'success');
            // Recargar la página después de un breve retraso
            setTimeout(() => location.reload(), 1500);
        } else {
            mostrarNotificacion(data.error || 'Error al registrar la dirección', 'error');
        }
    })
    .catch(error => {
        console.error("Error:", error);
        mostrarNotificacion('Error al procesar la solicitud', 'error');
    });
}

// Función para mostrar notificaciones
function mostrarNotificacion(mensaje, tipo) {
    // Crear elemento de notificación
    const notificacion = document.createElement('div');
    notificacion.className = `notificacion ${tipo}`;
    notificacion.textContent = mensaje;
    
    // Agregar al DOM
    document.body.appendChild(notificacion);
    
    // Mostrar con animación
    setTimeout(() => {
        notificacion.classList.add('mostrar');
    }, 100);
    
    // Ocultar después de 3 segundos
    setTimeout(() => {
        notificacion.classList.remove('mostrar');
        setTimeout(() => {
            document.body.removeChild(notificacion);
        }, 300);
    }, 3000);
}

// Función para alternar visibilidad de contraseña
function togglePassword(icon) {
    const input = icon.previousElementSibling;
    if (input.type === "password") {
        input.type = "text";
        icon.classList.remove("bx-hide");
        icon.classList.add("bx-show");
    } else {
        input.type = "password";
        icon.classList.remove("bx-show");
        icon.classList.add("bx-hide");
    }
}

function cargarMunicipios(departamentoId, municipioSelectId) {
    const municipioSelect = document.getElementById(municipioSelectId);

    if (departamentoId) {
        municipioSelect.innerHTML = '<option value="">Cargando municipios...</option>';

        fetch(`/obtener_municipios?departamento_id=${departamentoId}`)
            .then(response => response.json())
            .then(data => {
                municipioSelect.innerHTML = '<option value="">Seleccione un municipio</option>';
                data.forEach(municipio => {
                    municipioSelect.innerHTML += `<option value="${municipio.id}">${municipio.nombre}</option>`;
                });
            })
            .catch(error => {
                console.error('Error al cargar municipios:', error);
                municipioSelect.innerHTML = '<option value="">Error al cargar municipios</option>';
            });
    } else {
        municipioSelect.innerHTML = '<option value="">Seleccione un municipio</option>';
    }
}