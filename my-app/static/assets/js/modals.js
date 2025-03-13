

// Función para abrir el modal de edición
function editarDireccion(id) {
    console.log("Editando dirección con ID:", id); // Para depuración
    
    fetch(`/obtener-direccion/${id}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const direccion = data.direccion;
                
                document.getElementById('editarDireccionId').value = direccion.id;
                document.getElementById('editarNombreCompleto').value = direccion.nombre_completo;
                document.getElementById('editarBarrio').value = direccion.barrio;
                document.getElementById('editarDomicilio').value = direccion.domicilio;
                document.getElementById('editarReferencias').value = direccion.referencias || '';
                document.getElementById('editarTelefono').value = direccion.telefono;
                
                const departamentoSelect = document.getElementById('editarDepartamentoId');
                departamentoSelect.value = direccion.departamento_id;
                
                cargarMunicipiosEditar(direccion.departamento_id, direccion.municipio_id);
                
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

// Función para validar el formulario antes de enviarlo
function validarFormulario(form) {
    let valido = true;
    form.querySelectorAll("input[required], select[required]").forEach(input => {
        if (!input.value.trim()) {
            valido = false;
            input.classList.add("is-invalid");
        } else {
            input.classList.remove("is-invalid");
        }
    });
    return valido;
}

// Función para cargar municipios en el formulario de edición
function cargarMunicipiosEditar(departamentoId, municipioId) {
    const municipioSelect = document.getElementById('editarMunicipioId');
    municipioSelect.innerHTML = '<option value="">Cargando...</option>';
    
    fetch(`/obtener_municipios?departamento_id=${departamentoId}`)
        .then(response => response.json())
        .then(municipios => {
            municipioSelect.innerHTML = '<option value="">Seleccione un municipio</option>';
            municipios.forEach(municipio => {
                municipioSelect.innerHTML += `<option value="${municipio.id}">${municipio.nombre}</option>`;
            });
            if (municipioId) {
                municipioSelect.value = municipioId;
            }
        })
        .catch(error => {
            console.error('Error al cargar municipios:', error);
            municipioSelect.innerHTML = '<option value="">Error al cargar</option>';
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

// Función para actualizar dirección en la web
// 🛑 Mueve esta variable fuera de cualquier función para que sea accesible globalmente
let direccionIdAEliminar = null;

// Función para asignar el ID de la dirección al botón de confirmación
function confirmarEliminar(id) {
    direccionIdAEliminar = id;
    console.log("📌 ID seleccionado para eliminar:", direccionIdAEliminar);
}

// Evento para eliminar la dirección cuando se confirme
document.getElementById('confirmarEliminar').addEventListener('click', function () {
    if (direccionIdAEliminar) {
        fetch(`/eliminar-direccion/${direccionIdAEliminar}`, { method: 'DELETE' })
            .then(response => response.json())
            .then(data => {
                console.log("📩 Respuesta:", data);

                // 🔥 Cerrar el modal correctamente
                document.activeElement.blur(); // Quitar el foco del botón
                let modalElement = document.getElementById('eliminarDireccionModal');
                let modalEliminar = bootstrap.Modal.getInstance(modalElement);
                if (modalEliminar) modalEliminar.hide();

                modalElement.classList.remove('show');
                document.body.classList.remove('modal-open');
                document.querySelector('.modal-backdrop')?.remove();

                console.log("✅ Modal cerrado correctamente.");

                // 🚀 Recargar la página para reflejar los cambios
                setTimeout(() => location.reload(), 500);
            })
            .catch(error => console.error("❌ Error al eliminar:", error));
    } else {
        console.error("⚠️ No hay dirección seleccionada para eliminar.");
    }
});


// Función para actualizar dirección en el aplicativo
function actualizarDireccionAPI(event) {
    event.preventDefault();
    
    const form = document.getElementById('formEditarDireccionAPI');
    if (!validarFormulario(form)) return;
    
    const formData = new FormData(form);
    fetch('/actualizar-direccion-api', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message || 'Dirección actualizada correctamente');
            location.reload();
        } else {
            alert(data.error || 'Error al actualizar la dirección');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error al actualizar la dirección');
    });
}

// Manejar el envío del formulario de edición en la web
document.getElementById('formEditarDireccion').addEventListener('submit', actualizarDireccionWeb);

document.getElementById('formEditarDireccionAPI').addEventListener('submit', actualizarDireccionAPI);

// Función para confirmar la eliminación de una dirección

// Función para confirmar eliminación y mostrar modal
// Variable global para almacenar el ID de la dirección a eliminar


function actualizarDireccionWeb(event) {
    event.preventDefault(); // Evita el envío automático del formulario

    console.log("🚀 Ejecutando actualizarDireccionWeb()");

    let direccionId = document.getElementById("editarDireccionId").value; 
    let data = {
        id: direccionId,
        nombre_completo: document.getElementById("editarNombreCompleto").value,
        barrio: document.getElementById("editarBarrio").value,  // ⚠️ ¿Este campo está en el formulario?
        domicilio: document.getElementById("editarDomicilio").value,
        referencias: document.getElementById("editarReferencias").value,
        telefono: document.getElementById("editarTelefono").value,
        estado: "Activo",  // ⚠️ Agrega este campo si tu API lo espera
        costo_domicilio: 5000,  // ⚠️ Ajusta si es necesario
        municipio_id: document.getElementById("editarMunicipioId").value,
        departamento_id: document.getElementById("editarDepartamentoId").value
    };

    console.log("📩 Datos enviados:", JSON.stringify(data));

    fetch("/actualizar-direccion-web", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())  
    .then(responseData => {
        console.log("📩 Datos de respuesta:", responseData);
    
        if (responseData.mensaje) { 
            alert(responseData.mensaje);
            location.reload();
        } else {
            alert("⚠️ Error: " + (responseData.error || "Respuesta inesperada"));
        }
    })
    .catch(error => console.error("❌ Error en fetch:", error));
}

function cargarDetallesPedido(pedidoId) {
    // Realizar una solicitud AJAX para obtener los detalles del pedido
    fetch(`/obtener-detalles-pedido/${pedidoId}`)
        .then(response => response.json())
        .then(data => {
            // Construir el contenido del modal con los detalles del pedido
            const detallesContent = `
                <div class="row">
                    <div class="col-md-6">
                        <label for="fecha" class="form-label">Fecha</label>
                        <p>${data.pedido.fecha}</p>
                    </div>
                    <div class="col-md-6">
                        <label for="fechaEntrega" class="form-label">Fecha de Entrega</label>
                        <p>${data.pedido.fechaEntrega}</p>
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-6">
                        <label for="horaEntrega" class="form-label">Hora de Entrega</label>
                        <p>${data.pedido.horaEntrega}</p>
                    </div>
                    <div class="col-md-6">
                        <label for="estado" class="form-label">Estado</label>
                        <p>${data.pedido.estado}</p>
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-6">
                        <label for="usuario" class="form-label">Usuario</label>
                        <p>${data.pedido.usuario_nombre}</p>
                    </div>
                    <div class="col-md-6">
                        <label for="producto" class="form-label">Producto</label>
                        <p>${data.pedido.producto_nombre}</p>
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-6">
                        <label for="metodo_pago" class="form-label">Método de Pago</label>
                        <p>${data.pedido.metodo_pago}</p>
                    </div>
                    <div class="col-md-6">
                        <label for="tipo_entrega" class="form-label">Tipo de Entrega</label>
                        <p>${data.pedido.tipo_entrega}</p>
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-6">
                        <label for="total_pedido" class="form-label">Total del Pedido</label>
                        <p>$${(Number(data.pedido.total_pedido) || 0).toFixed(2)}</p>
                    </div>
                </div>
                <hr />
                <h4>Detalles del Pedido</h4>
                ${data.detalles_pedido.map(detalle => `
                    <div class="row mt-2">
                        <div class="col-md-6">
                            <label for="producto" class="form-label">Producto</label>
                            <p>${detalle.producto_nombre}</p>
                        </div>
                        <div class="col-md-6">
                            <label for="cantidad" class="form-label">Cantidad</label>
                            <p>${detalle.cantidad}</p>
                        </div>
                    </div>
                    <div class="row mt-2">
                        <div class="col-md-6">
                            <label for="precio_unitario" class="form-label">Precio Unitario</label>
                            <p>$${(Number(detalle.precio_unitario) || 0).toFixed(2)}</p>
                        </div>
                        <div class="col-md-6">
                            <label for="total" class="form-label">Total</label>
                            <p>$${(Number(detalle.total) || 0).toFixed(2)}</p>
                        </div>
                    </div>
                    <hr />
                `).join('')}
                <!-- Detalles de la Entrega -->
                <div class="card mb-4" style="border: none; background-color: #f8f9fa; border-radius: 10px;">
                    <div class="card-header" style="background-color: #2c3e50; color: white; font-weight: bold; border-radius: 10px 10px 0 0;">
                        <i class="bi bi-info-circle me-2"></i>Información General de la Entrega
                    </div>
                    <div class="card-body">
                        <div class="row">
                            <!-- Columna 1 -->
                            <div class="col-md-6">
                                <div class="mb-3">
                                    <label class="form-label" style="font-weight: bold; font-size: 1rem; color: #2c3e50;">
                                        <i class="bi bi-truck me-2"></i>Tipo de Entrega
                                    </label>
                                    <p style="font-size: 0.95rem; color: #495057;">${data.pedido.tipo_entrega}</p>
                                </div>
                                <div class="mb-3">
                                    <label class="form-label" style="font-weight: bold; font-size: 1rem; color: #2c3e50;">
                                        <i class="bi bi-calendar-event me-2"></i>Fecha y Hora
                                    </label>
                                    <p style="font-size: 0.95rem; color: #495057;">${data.pedido.fechaEntrega} ${data.pedido.horaEntrega}</p>
                                </div>
                                <div class="mb-3">
                                    <label class="form-label" style="font-weight: bold; font-size: 1rem; color: #2c3e50;">
                                        <i class="bi bi-geo-alt me-2"></i>ID de Dirección
                                    </label>
                                    <p style="font-size: 0.95rem; color: #495057;">${data.pedido.direccion_id || 'No disponible'}</p>
                                </div>
                            </div>
                            <!-- Columna 2 -->
                            <div class="col-md-6">
                                <div class="mb-3">
                                    <label class="form-label" style="font-weight: bold; font-size: 1rem; color: #2c3e50;">
                                        <i class="bi bi-cash-coin me-2"></i>Costo de Domicilio
                                    </label>
                                    <p style="font-size: 0.95rem; color: #495057;">
                                        ${data.pedido.costo_domicilio ? `$ ${data.pedido.costo_domicilio.toFixed(2)}` : 'No disponible'}
                                    </p>
                                </div>
                                <div class="mb-3">
                                    <label class="form-label" style="font-weight: bold; font-size: 1rem; color: #2c3e50;">
                                        <i class="bi bi-clipboard-check me-2"></i>Estado de la Entrega
                                    </label>
                                    <p style="font-size: 0.95rem; color: #495057;">${data.pedido.estado_entrega || 'No disponible'}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            `;

            // Insertar el contenido en el modal
            document.getElementById('detallesPedidoContent').innerHTML = detallesContent;
        })
        .catch(error => {
            console.error('Error al cargar los detalles del pedido:', error);
            document.getElementById('detallesPedidoContent').innerHTML = `
                <p class="text-danger">Error al cargar los detalles del pedido.</p>
            `;
        });
}

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
