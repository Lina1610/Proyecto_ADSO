// Función para abrir el modal de edición
function editarDireccion(id) {
    console.log("Editando dirección con ID:", id); // Para depuración
    
    // Realizar una solicitud para obtener los datos de la dirección
    fetch(`/obtener-direccion/${id}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const direccion = data.direccion;
                
                // Llenar el formulario con los datos
                document.getElementById('editarDireccionId').value = direccion.id;
                document.getElementById('editarNombreCompleto').value = direccion.nombre_completo;
                document.getElementById('editarBarrio').value = direccion.barrio;
                document.getElementById('editarDomicilio').value = direccion.domicilio;
                document.getElementById('editarReferencias').value = direccion.referencias || '';
                document.getElementById('editarTelefono').value = direccion.telefono;
                
                // Establecer el departamento
                const departamentoSelect = document.getElementById('editarDepartamentoId');
                departamentoSelect.value = direccion.departamento_id;
                
                // Cargar los municipios y establecer el municipio seleccionado
                cargarMunicipiosEditar(direccion.departamento_id, direccion.municipio_id);
                
                // Abrir el modal
                const modal = new bootstrap.Modal(document.getElementById('editarDireccionModal'));
                modal.show();
            } else {
                alert(data.error || 'Error al cargar los datos de la dirección');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error al cargar los datos de la dirección');
        });
}

// Función para cargar municipios en el formulario de edición
function cargarMunicipiosEditar(departamentoId, municipioId) {
    fetch(`/obtener_municipios?departamento_id=${departamentoId}`)
        .then(response => response.json())
        .then(municipios => {
            const municipioSelect = document.getElementById('editarMunicipioId');
            municipioSelect.innerHTML = '<option value="">Seleccione un municipio</option>';
            
            municipios.forEach(municipio => {
                const option = document.createElement('option');
                option.value = municipio.id;
                option.textContent = municipio.nombre;
                municipioSelect.appendChild(option);
            });
            
            // Establecer el municipio seleccionado
            if (municipioId) {
                municipioSelect.value = municipioId;
            }
        })
        .catch(error => {
            console.error('Error al cargar municipios:', error);
        });
}

// Cambio de departamento en el formulario de edición
document.getElementById('editarDepartamentoId').addEventListener('change', function() {
    const departamentoId = this.value;
    if (departamentoId) {
        cargarMunicipiosEditar(departamentoId);
    } else {
        document.getElementById('editarMunicipioId').innerHTML = '<option value="">Seleccione un municipio</option>';
    }
});

// Manejar el envío del formulario de edición
document.getElementById('formEditarDireccion').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const formData = new FormData(this);
    
    fetch('/actualizar-direccion', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message || 'Dirección actualizada correctamente');
            const modal = bootstrap.Modal.getInstance(document.getElementById('editarDireccionModal'));
            modal.hide();
            location.reload(); // Recargar para ver los cambios
        } else {
            alert(data.error || 'Error al actualizar la dirección');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error al actualizar la dirección');
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