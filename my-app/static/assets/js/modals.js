document.getElementById('formEditarDireccion').addEventListener('submit', function (event) {
    event.preventDefault();  // Evitar que el formulario se envíe de forma tradicional

    // Obtener los datos del formulario
    const formData = {
        nombre_completo: document.getElementById('editarNombreCompleto').value,
        barrio: document.getElementById('editarBarrio').value,
        domicilio: document.getElementById('editarDomicilio').value,
        referencias: document.getElementById('editarReferencias').value,
        telefono: document.getElementById('editarTelefono').value,
        departamento_id: document.getElementById('editarDepartamentoId').value,
        municipio_id: document.getElementById('editarMunicipioId').value
    };

    // Enviar los datos al backend
    fetch('/guardar-direccion', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Dirección guardada correctamente');
            // Recargar la página o actualizar la lista de direcciones
            location.reload();
        } else {
            alert(data.error || 'Error al guardar la dirección');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error al guardar la dirección');
    });
});

// Función para confirmar la eliminación de una dirección
let direccionIdAEliminar = null;

function confirmarEliminar(id) {
    direccionIdAEliminar = id;
}

document.getElementById('confirmarEliminar').addEventListener('click', function() {
    if (direccionIdAEliminar) {
        fetch(`/eliminar-direccion/${direccionIdAEliminar}`, { method: 'GET' })
            .then(response => {
                if (response.ok) {
                    location.reload(); // Recargar la página para reflejar los cambios
                } else {
                    alert('Error al eliminar la dirección');
                }
            })
            .catch(error => console.error('Error al eliminar la dirección:', error));
    }
});

// Función para mostrar/ocultar contraseña
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