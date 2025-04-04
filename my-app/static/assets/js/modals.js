

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

// Función para manejar el registro de una nueva dirección
function registrarDireccion(event) {
    event.preventDefault();
    
    const form = document.getElementById('formRegistrarDireccion');
    if (!validarFormulario(form)) return;
    
    const formData = new FormData(form);
    
    fetch('/api/registrar-direccion', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // Cerrar el modal
        let modalElement = document.getElementById('registrarDireccionModal');
        let modal = bootstrap.Modal.getInstance(modalElement);
        if (modal) modal.hide();
        
        if (data.success) {
            // Mostrar notificación de éxito
            mostrarNotificacion(data.message || 'Dirección agregada correctamente', 'success');
            // Recargar la página después de mostrar la notificación
            setTimeout(() => location.reload(), 950);
        } else {
            mostrarNotificacion(data.error || 'Error al agregar la dirección', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        mostrarNotificacion('Error al agregar la dirección', 'error');
    });
}

function actualizarPerfil(event) {
    event.preventDefault(); // Prevenir el comportamiento predeterminado
    console.log("Formulario de perfil enviado"); // Debug
    
    const form = document.getElementById('formEditarPerfil');
    if (!validarFormulario(form)) {
        console.log("Formulario no válido"); // Debug
        return;
    }
    
    const formData = new FormData(form);
    console.log("Datos del formulario:", formData); // Debug
    
    fetch('/actualizar-datos-perfil', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log("Datos de respuesta:", data); // Debug
        if (data.success) {
            mostrarNotificacion(data.message || 'Perfil actualizado correctamente', 'success');
            setTimeout(() => location.reload(), 800);
        } else {
            mostrarNotificacion(data.error || 'Error al actualizar el perfil', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        mostrarNotificacion('Error al actualizar el perfil', 'error');
    });
}

// Función para cambiar la contraseña
function cambiarContrasena(event) {
    event.preventDefault(); // Prevenir el envío del formulario

    const form = document.getElementById('formCambiarContrasena');
    if (!validarFormulario(form)) {
        mostrarNotificacion('Por favor, complete todos los campos requeridos.', 'error');
        return;
    }

    // Obtener los valores de los campos
    const nuevaContrasena = document.getElementById('new_pass_user').value;
    const confirmarContrasena = document.getElementById('repetir_pass_user').value;

    // Validar que las contraseñas coincidan
    if (nuevaContrasena !== confirmarContrasena) {
        mostrarNotificacion('Las contraseñas no coinciden.', 'error');
        return;
    }

    // Crear FormData con los datos del formulario
    const formData = new FormData(form);

    // Enviar la solicitud al servidor
    fetch('/actualizar-password', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Mostrar notificación de éxito
            mostrarNotificacion(data.message || 'Contraseña actualizada correctamente.', 'success');
            // Limpiar el formulario
            form.reset();
        } else {
            // Mostrar notificación de error
            mostrarNotificacion(data.error || 'Error al actualizar la contraseña.', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        mostrarNotificacion('Error al procesar la solicitud.', 'error');
    });
}

// Función para validar el formulario
function validarFormulario(form) {
    let valido = true;
    form.querySelectorAll("input[required]").forEach(input => {
        if (!input.value.trim()) {
            valido = false;
            input.classList.add("is-invalid");
        } else {
            input.classList.remove("is-invalid");
        }
    });
    return valido;
}

// Función para mostrar/ocultar la contraseña
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

// Agregar el evento al formulario de cambio de contraseña
document.addEventListener('DOMContentLoaded', function() {
    const formCambiarContrasena = document.getElementById('formCambiarContrasena');
    if (formCambiarContrasena) {
        formCambiarContrasena.addEventListener('submit', cambiarContrasena);
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const formEditarPerfil = document.getElementById('formEditarPerfil');
    if (formEditarPerfil) {
        formEditarPerfil.addEventListener('submit', actualizarPerfil);
    }

    const formCambiarContrasena = document.getElementById('formCambiarContrasena');
    if (formCambiarContrasena) {
        formCambiarContrasena.addEventListener('submit', cambiarContrasena);
    }
});



// Asegúrate de que el evento se asigne correctamente
document.addEventListener('DOMContentLoaded', function() {
    const formRegistrarDireccion = document.getElementById('formRegistrarDireccion');
    if (formRegistrarDireccion) {
        formRegistrarDireccion.addEventListener('submit', registrarDireccion);
    }
});

// Función para validar el formulario con notificaciones visuales
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
    
    if (!valido) {
        mostrarNotificacion('Por favor, complete todos los campos requeridos', 'error');
    }
    
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
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('registrarDepartamentoId').addEventListener('change', function() {
        const departamentoId = this.value;
        const municipioSelect = document.getElementById('registrarMunicipioId');

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
    });
});

// Cambio de departamento en el formulario de edición
document.getElementById('editarDepartamentoId').addEventListener('change', function() {
    const departamentoId = this.value;
    if (departamentoId) {
        cargarMunicipiosEditar(departamentoId);
    } else {
        document.getElementById('editarMunicipioId').innerHTML = '<option value="">Seleccione un municipio</option>';
    }
});
// Función para cargar municipios dinámicamente
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

// Escuchar cambios en el campo de departamento para todos los roles
document.addEventListener('DOMContentLoaded', function() {
    // Cliente
    const departamentoCliente = document.getElementById('departamentoIdCliente');
    if (departamentoCliente) {
        departamentoCliente.addEventListener('change', function() {
            cargarMunicipios(this.value, 'municipioIdCliente');
        });
    }

    // Administrador
    const departamentoAdmin = document.getElementById('departamentoIdAdmin');
    if (departamentoAdmin) {
        departamentoAdmin.addEventListener('change', function() {
            cargarMunicipios(this.value, 'municipioIdAdmin');
        });
    }

    // Superadmin
    const departamentoSuperadmin = document.getElementById('departamentoIdSuperadmin');
    if (departamentoSuperadmin) {
        departamentoSuperadmin.addEventListener('change', function() {
            cargarMunicipios(this.value, 'municipioIdSuperadmin');
        });
    }

    // Empleado
    const departamentoEmpleado = document.getElementById('departamentoIdEmpleado');
    if (departamentoEmpleado) {
        departamentoEmpleado.addEventListener('change', function() {
            cargarMunicipios(this.value, 'municipioIdEmpleado');
        });
    }
});

// Función para actualizar dirección en la web
// 🛑 Mueve esta variable fuera de cualquier función para que sea accesible globalmente
let direccionIdAEliminar = null;

// Función para asignar el ID de la dirección al botón de confirmación
function confirmarEliminar(id) {
    // Almacenar el ID en el campo oculto del modal
    document.getElementById('direccionIdAEliminar').value = id;
    console.log("📌 ID seleccionado para eliminar:", id);
    
    // Mostrar el modal (si no lo estás haciendo con un atributo data-bs-toggle)
    const modal = new bootstrap.Modal(document.getElementById('eliminarDireccionModal'));
    modal.show();
}

// Exponer la función en el ámbito global
window.confirmarEliminar = confirmarEliminar;

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('confirmarEliminar').addEventListener('click', function () {
        // Obtener el ID del campo oculto
        const direccionIdAEliminar = document.getElementById('direccionIdAEliminar').value;
        
        if (direccionIdAEliminar) {
            // Usar comillas invertidas (backticks) correctamente para la URL
            fetch(`/eliminar-direccion/${direccionIdAEliminar}`, { method: 'DELETE' })

                .then(response => response.json())
                .then(data => {
                    console.log("📩 Respuesta del servidor:", data);
    
                    // Cerrar el modal correctamente
                    const modalElement = document.getElementById('eliminarDireccionModal');
                    const modalEliminar = bootstrap.Modal.getInstance(modalElement);
                    if (modalEliminar) modalEliminar.hide();
    
                    // Verificar si la operación fue exitosa
                    if (data.success) {
                        // Mostrar notificación de éxito 
                        mostrarNotificacion(data.message || 'Dirección eliminada correctamente', 'success');
                        // Recargar la página después de mostrar la notificación
                        setTimeout(() => location.reload(), 950);
                    } else {
                        // Mostrar notificación de error
                        mostrarNotificacion(data.error || 'Error al eliminar la dirección', 'error');
                    }
                })
                .catch(error => {
                    console.error("❌ Error al eliminar:", error);
                    
                    // Cerrar el modal incluso si hay un error
                    const modalElement = document.getElementById('eliminarDireccionModal');
                    const modalEliminar = bootstrap.Modal.getInstance(modalElement);
                    if (modalEliminar) modalEliminar.hide();
                    
                    // Mostrar mensaje de error
                    mostrarNotificacion('Error al procesar la solicitud', 'error');
                });
        } else {
            console.error("⚠️ No hay dirección seleccionada para eliminar.");
            mostrarNotificacion("No hay dirección seleccionada para eliminar", 'error');
        }
    });
});

function mostrarNotificacion(mensaje, tipo) {
    console.log("Notificación:", mensaje, "Tipo:", tipo); // Debug

    // Crear el elemento de notificación
    const notificacion = document.createElement('div');
    notificacion.className = `notificacion ${tipo}`;
    notificacion.textContent = mensaje;

    // Añadir la notificación al cuerpo del documento
    document.body.appendChild(notificacion);

    // Mostrar la notificación después de un breve retraso
    setTimeout(() => {
        console.log("Mostrando notificación en pantalla...");
        notificacion.classList.add('mostrar');
    }, 100);

    // Ocultar y eliminar la notificación después de 3 segundos
    setTimeout(() => {
        console.log("Ocultando notificación...");
        notificacion.classList.remove('mostrar');

        // Eliminar la notificación del DOM después de la animación
        setTimeout(() => {
            console.log("Eliminando notificación del DOM...");
            document.body.removeChild(notificacion);
        }, 300); // Tiempo para la animación de desvanecimiento
    }, 3000); // Tiempo que la notificación permanece visible
}
// Función para actualizar dirección en la web
function actualizarDireccionWeb(event) {
    event.preventDefault(); // Evita el envío automático del formulario

    console.log("🚀 Ejecutando actualizarDireccionWeb()");

    let direccionId = document.getElementById("editarDireccionId").value; 
    let data = {
        id: direccionId,
        nombre_completo: document.getElementById("editarNombreCompleto").value,
        barrio: document.getElementById("editarBarrio").value,
        domicilio: document.getElementById("editarDomicilio").value,
        referencias: document.getElementById("editarReferencias").value,
        telefono: document.getElementById("editarTelefono").value,
        estado: "Activo",
        costo_domicilio: 5000,
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
    
        // Cerrar el modal correctamente
        let modalElement = document.getElementById('editarDireccionModal');
        let modal = bootstrap.Modal.getInstance(modalElement);
        if (modal) modal.hide();
        
        // Usar notificación personalizada en lugar de alert
        if (responseData.mensaje) { 
            mostrarNotificacion(responseData.mensaje, 'success');
            setTimeout(() => location.reload(), 1500);
        } else {
            mostrarNotificacion("Error: " + (responseData.error || "Respuesta inesperada"), 'error');
        }
    })
    .catch(error => {
        console.error("❌ Error en fetch:", error);
        mostrarNotificacion("Error al actualizar la dirección", 'error');
    });
}

// Función para actualizar dirección en el aplicativo
function actualizarDireccionAPI(event) {
    event.preventDefault();
    
    const form = document.getElementById('formEditarDireccionAPI');
    if (!validarFormulario(form)) {
        mostrarNotificacion('Por favor, complete todos los campos requeridos', 'error');
        return;
    }
    
    const formData = new FormData(form);
    fetch('/actualizar-direccion-api', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // Cerrar el modal correspondiente
        let modalElement = document.getElementById('editarDireccionModalAPI');
        let modal = bootstrap.Modal.getInstance(modalElement);
        if (modal) modal.hide();
        
        if (data.success) {
            mostrarNotificacion(data.message || 'Dirección actualizada correctamente', 'success');
            setTimeout(() => location.reload(), 1500);
        } else {
            mostrarNotificacion(data.error || 'Error al actualizar la dirección', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        mostrarNotificacion('Error al actualizar la dirección', 'error');
    });
}


// Manejar el envío del formulario de edición en la web
document.getElementById('formEditarDireccion').addEventListener('submit', actualizarDireccionWeb);

document.getElementById('formEditarDireccionAPI').addEventListener('submit', actualizarDireccionAPI);


// Función para actualizar dirección en la web
function actualizarDireccionWeb(event) {
    event.preventDefault(); // Evita el envío automático del formulario

    console.log("🚀 Ejecutando actualizarDireccionWeb()");

    let direccionId = document.getElementById("editarDireccionId").value; 
    let data = {
        id: direccionId,
        nombre_completo: document.getElementById("editarNombreCompleto").value,
        barrio: document.getElementById("editarBarrio").value,
        domicilio: document.getElementById("editarDomicilio").value,
        referencias: document.getElementById("editarReferencias").value,
        telefono: document.getElementById("editarTelefono").value,
        estado: "Activo",
        costo_domicilio: 5000,
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
    
        // Cerrar el modal correctamente
        let modalElement = document.getElementById('editarDireccionModal');
        let modal = bootstrap.Modal.getInstance(modalElement);
        if (modal) modal.hide();
        
        // Usar notificación personalizada en lugar de alert
        if (responseData.mensaje) { 
            mostrarNotificacion(responseData.mensaje, 'success');
            setTimeout(() => location.reload(), 1500);
        } else {
            mostrarNotificacion("Error: " + (responseData.error || "Respuesta inesperada"), 'error');
        }
    })
    .catch(error => {
        console.error("❌ Error en fetch:", error);
        mostrarNotificacion("Error al actualizar la dirección", 'error');
    });
}

function cargarDetallesPedido(pedidoId) {
    // Realizar una solicitud AJAX para obtener los detalles del pedido
    fetch(`/obtener-detalles-pedido/${pedidoId}`)
        .then(response => response.json())
        .then(data => {
            // Construir el contenido del modal con los detalles del pedido
            const detallesContent = `
                <h4>Detalles del Pedido</h4>
                ${data.detalles_pedido.map(detalle => `
                    <div class="row mt-2">
                        <div class="col-md-6">
                            <label class="form-label">Producto</label>
                            <p>${detalle.producto_nombre}</p>
                        </div>
                        <div class="col-md-6">
                            <label class="form-label">Cantidad</label>
                            <p>${detalle.cantidad}</p>
                        </div>
                        <div class="col-md-6">
                            <label class="form-label">Precio Unitario</label>
                            <p>$${(Number(detalle.precio_unitario) || 0).toFixed(2)}</p>
                        </div>
                        <div class="col-md-6">
                            <label class="form-label">Total</label>
                            <p>$${(Number(detalle.total) || 0).toFixed(2)}</p>
                        </div>
                    </div>
                    <hr />
                `).join('')}

                <h4>Información del Pedido</h4>
                <div class="row">
                    <div class="col-md-6">
                        <label class="form-label">Fecha de Entrega</label>
                        <p>${data.pedido.fechaEntrega}</p>
                    </div>
                    <div class="col-md-6">
                        <label class="form-label">Hora de Entrega</label>
                        <p>${data.pedido.horaEntrega}</p>
                    </div>
                    <div class="col-md-6">
                        <label class="form-label">Estado</label>
                        <p>${data.pedido.estado}</p>
                    </div>
                    <div class="col-md-6">
                        <label class="form-label">Método de Pago</label>
                        <p>${data.pedido.metodo_pago}</p>
                    </div>
                    <div class="col-md-6">
                        <label class="form-label">Total del Pedido</label>
                        <p>$${(Number(data.pedido.total_pedido) || 0).toFixed(2)}</p>
                    </div>
                </div>

                <h4>Información de Entrega</h4>
                <div class="row">
                    <div class="col-md-6">
                        <label class="form-label">Tipo de Entrega</label>
                        <p>${data.pedido.tipo_entrega}</p>
                    </div>
                    <div class="col-md-6">
                        <label class="form-label">Costo de Domicilio</label>
                        <p>${data.pedido.costo_domicilio ? `$ ${data.pedido.costo_domicilio.toFixed(2)}` : 'No disponible'}</p>
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
