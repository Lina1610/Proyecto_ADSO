// Variables globales
let carritoItems = [];

// Función para cargar el carrito desde la base de datos
function cargarCarrito() {
    fetch('/carrito/obtener')
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                carritoItems = data.items || [];
                actualizarInterfazCarrito();
            } else {
                console.error('Error al cargar el carrito:', data.mensaje);
            }
        })
        .catch(error => {
            console.error('Error al cargar el carrito:', error);
        });
}

// Función para agregar un producto al carrito
function agregarAlCarrito(producto_id, nombre, precio, imagen) {
    // Verificar si el usuario está conectado
    const isUserLoggedIn = document.querySelector('.user-info-container') !== null;
    
    if (!isUserLoggedIn) {
        alert('Debe iniciar sesión para agregar productos al carrito');
        window.location.href = '/login-cliente'; // Redirigir al login
        return;
    }
    
    fetch('/carrito/agregar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            producto_id: producto_id,
            cantidad: 1
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            // Actualizar carrito directamente sin mostrar notificación de texto
            cargarCarrito();
            
            // Animación sutil en el icono del carrito
            const carritoIcono = document.querySelector('.carrito-icono');
            if (carritoIcono) {
                carritoIcono.classList.add('carrito-animado');
                setTimeout(() => {
                    carritoIcono.classList.remove('carrito-animado');
                }, 500);
            }
        } else {
            // Solo mostrar notificación para errores
            mostrarNotificacion(data.mensaje, 'error');
        }
    })
    .catch(error => {
        console.error('Error al agregar al carrito:', error);
        mostrarNotificacion('Error al agregar al carrito', 'error');
    });
}

// Función para actualizar la cantidad de un producto en el carrito
function updateQuantity(carrito_id, change) {
    // Buscar el producto en el carrito
    const itemIndex = carritoItems.findIndex(item => item.id === carrito_id);
    
    if (itemIndex !== -1) {
        // Calcular la nueva cantidad
        const nuevaCantidad = carritoItems[itemIndex].cantidad + change;
        
        // No permitir cantidades menores a 1
        if (nuevaCantidad < 1) {
            eliminarDelCarrito(carrito_id);
            return;
        }
        
        // Enviar la actualización al servidor
        fetch('/carrito/actualizar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                carrito_id: carrito_id,
                cantidad: nuevaCantidad
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                // Actualizar directamente el carrito sin mostrar notificación
                cargarCarrito();
            } else {
                mostrarNotificacion(data.mensaje, 'error');
            }
        })
        .catch(error => {
            console.error('Error al actualizar cantidad:', error);
            mostrarNotificacion('Error al actualizar cantidad', 'error');
        });
    }
}

// Función para eliminar un producto del carrito
function eliminarDelCarrito(carrito_id) {
    fetch('/carrito/eliminar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            carrito_id: carrito_id
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            // Actualizar carrito sin mostrar notificación
            cargarCarrito();
        } else {
            mostrarNotificacion(data.mensaje, 'error');
        }
    })
    .catch(error => {
        console.error('Error al eliminar del carrito:', error);
        mostrarNotificacion('Error al eliminar del carrito', 'error');
    });
}

// Función para actualizar la interfaz del carrito
function actualizarInterfazCarrito() {
    const carritoItemsContainer = document.getElementById('carrito-items');
    const carritoCount = document.getElementById('carrito-count');
    
    // Limpiar el contenido actual del carrito
    carritoItemsContainer.innerHTML = '';
    
    // Variable para almacenar el total de la compra
    let totalCompra = 0;
    let totalItems = 0;
    
    // Verificar si hay productos en el carrito
    if (carritoItems.length === 0) {
        carritoItemsContainer.innerHTML = '<div class="empty-cart">Su carrito está vacío</div>';
        carritoCount.textContent = '0';
        return;
    }
    
    // Recorrer la lista de productos en el carrito
    carritoItems.forEach((producto) => {
        // Calcular el subtotal del producto (precio * cantidad)
        const subtotal = producto.precio * producto.cantidad;
        totalCompra += subtotal; // Sumar al total de la compra
        totalItems += producto.cantidad;
        
        const nuevoItem = document.createElement('div');
        nuevoItem.classList.add('carrito-item');
        nuevoItem.innerHTML = `
            <div class="item-info">
                <img src="${producto.imagen}" alt="${producto.nombre}">
                <div class="item-details">
                    <h6>${producto.nombre}</h6>
                    <p class="item-price">$${producto.precio.toLocaleString()}</p>
                    <div class="quantity-control">
                        <button class="quantity-btn" onclick="updateQuantity(${producto.id}, -1)">-</button>
                        <span class="quantity">${producto.cantidad}</span>
                        <button class="quantity-btn" onclick="updateQuantity(${producto.id}, 1)">+</button>
                    </div>
                </div>
            </div>
            <div class="item-subtotal">
                <p>$${subtotal.toLocaleString()}</p>
                <button class="delete-btn" onclick="eliminarDelCarrito(${producto.id})">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        `;
        carritoItemsContainer.appendChild(nuevoItem);
    });
    
    // Mostrar el total de la compra en el carrito
    const totalElement = document.createElement('div');
    totalElement.classList.add('carrito-total');
    totalElement.innerHTML = `<h5><strong>Total:</strong> $${totalCompra.toLocaleString()}</h5>`;
    carritoItemsContainer.appendChild(totalElement);
    
    // Agregar botón para procesar pedido
    const botonProcesar = document.createElement('div');
    botonProcesar.classList.add('carrito-footer');
    botonProcesar.innerHTML = `
        <button class="btn-procesar" onclick="procesarPedido()">
            <i class="fas fa-check-circle"></i> Procesar Pedido
        </button>
    `;
    carritoItemsContainer.appendChild(botonProcesar);
    
    // Actualizar el contador del carrito
    carritoCount.textContent = totalItems;
}

// Función para mostrar/ocultar el carrito
function toggleCarrito() {
    const carritoContainer = document.getElementById('carrito-container');
    carritoContainer.classList.toggle('visible');
}



// Función para mostrar notificaciones
function mostrarNotificacion(mensaje, tipo) {
    const notificacion = document.createElement('div');
    notificacion.className = `notificacion ${tipo}`;
    notificacion.textContent = mensaje;

    document.body.appendChild(notificacion);

    setTimeout(() => {
        notificacion.classList.add('mostrar');
    }, 100);

    setTimeout(() => {
        notificacion.classList.remove('mostrar');
        setTimeout(() => {
            document.body.removeChild(notificacion);
        }, 300);
    }, 3000);
}

// Cargar el carrito al cargar la página
document.addEventListener('DOMContentLoaded', function() {
    cargarCarrito();
    
    const carritoIcono = document.querySelector('.carrito-icono');
    if (carritoIcono) {
        carritoIcono.addEventListener('click', toggleCarrito);
    }
});

// Función para finalizar la compra
function finalizarCompra() {
    const direccionSeleccionada = document.querySelector('input[name="direccion"]:checked');
    
    if (!direccionSeleccionada) {
        mostrarNotificacion('Por favor, selecciona una dirección de envío.', 'error');
        return;
    }

    const direccionId = direccionSeleccionada.value;

    fetch('/finalizar-compra', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ direccion_id: direccionId }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            mostrarNotificacion('Pedido creado con éxito.', 'success');
            window.location.href = '/pedidos'; 
        } else {
            mostrarNotificacion('Error al finalizar la compra: ' + data.mensaje, 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        mostrarNotificacion('Ocurrió un error al finalizar la compra.', 'error');
    });
}

// Función para procesar el pedido y mostrar las direcciones
function procesarPedido() {
    if (carritoItems.length === 0) {
        mostrarNotificacion('El carrito está vacío', 'error');
        return;
    }

    // Obtener métodos de pago y tipos de entrega
    fetch('/obtener-metodos-pago-tipos-entrega')
        .then(response => response.json())
        .then(data => {
            const modalBody = document.getElementById('modal-body-procesar-pedido');
            modalBody.innerHTML = '';

            // Mostrar métodos de pago
            const metodosPagoHTML = data.metodos_pago.map(metodo => `
                <div class="form-check">
                    <input class="form-check-input" type="radio" name="metodo_pago" id="metodo_pago_${metodo.id}" value="${metodo.id}">
                    <label class="form-check-label" for="metodo_pago_${metodo.id}">
                        ${metodo.metodo}
                    </label>
                </div>
            `).join('');

            modalBody.innerHTML += `<h5>Métodos de Pago</h5>${metodosPagoHTML}`;

            // Mostrar tipos de entrega
            const tiposEntregaHTML = data.tipos_entrega.map(tipo => `
                <div class="form-check">
                    <input class="form-check-input" type="radio" name="tipo_entrega" id="tipo_entrega_${tipo}" value="${tipo}" onchange="mostrarDirecciones('${tipo}')">
                    <label class="form-check-label" for="tipo_entrega_${tipo}">
                        ${tipo}
                    </label>
                </div>
            `).join('');

            modalBody.innerHTML += `<h5 class="mt-3">Tipos de Entrega</h5>${tiposEntregaHTML}`;

            // Mostrar el modal de procesar pedido
            const modalProcesarPedido = new bootstrap.Modal(document.getElementById('modalProcesarPedido'));
            modalProcesarPedido.show();
        })
        .catch(error => {
            console.error('Error al obtener métodos de pago y tipos de entrega:', error);
            mostrarNotificacion('Error al cargar métodos de pago y tipos de entrega', 'error');
        });
}

function mostrarDirecciones(tipoEntrega) {
    if (tipoEntrega === 'Domicilio') {
        // Cerrar el modal actual (Procesar Pedido)
        const modalProcesarPedido = bootstrap.Modal.getInstance(document.getElementById('modalProcesarPedido'));
        modalProcesarPedido.hide();

        // Obtener las direcciones del usuario
        fetch('/carrito/obtener-direcciones')
            .then(response => response.json())
            .then(data => {
                const direccionesContainer = document.getElementById('contenedor-direcciones');
                direccionesContainer.innerHTML = '';

                if (data.status === 'success' && data.direcciones.length > 0) {
                    // Mostrar las direcciones disponibles
                    data.direcciones.forEach(direccion => {
                        const item = document.createElement('label');
                        item.className = 'list-group-item';
                        item.innerHTML = `
                            <input type="radio" name="direccion" value="${direccion.id}" class="form-check-input me-2">
                            <strong>${direccion.nombre_completo}</strong><br>
                            ${direccion.domicilio}, ${direccion.barrio}<br>
                            ${direccion.nombre_municipio}, ${direccion.nombre_departamento}<br>
                            Teléfono: ${direccion.telefono}
                        `;
                        direccionesContainer.appendChild(item);
                    });
                } else {
                    // Mostrar un mensaje si no hay direcciones registradas
                    direccionesContainer.innerHTML = `
                        <div class="alert alert-warning">
                            No tienes direcciones registradas. Por favor, agrega una dirección.
                        </div>
                    `;
                }

                // Agregar un botón para abrir el modal de registro de dirección
                const botonAgregarDireccion = document.createElement('button');
                botonAgregarDireccion.className = 'btn btn-primary w-100 mt-3';
                botonAgregarDireccion.innerHTML = '<i class="fas fa-plus"></i> Agregar Nueva Dirección';
                botonAgregarDireccion.onclick = () => {
                    const modalRegistrarDireccion = new bootstrap.Modal(document.getElementById('editarDireccionModal'));
                    modalRegistrarDireccion.show();
                };
                direccionesContainer.appendChild(botonAgregarDireccion);

                // Mostrar el modal de direcciones
                const modalDirecciones = new bootstrap.Modal(document.getElementById('modalDirecciones'));
                modalDirecciones.show();

                // Manejar el evento de cancelar en el modal de direcciones
                document.getElementById('modalDirecciones').addEventListener('hidden.bs.modal', () => {
                    // Volver a abrir el modal de procesar pedido
                    modalProcesarPedido.show();
                });
            })
            .catch(error => {
                console.error('Error al obtener direcciones:', error);
                mostrarNotificacion('Error al cargar direcciones', 'error');
            });
    }
}

// ==================== FUNCIONES DE DIRECCIONES ====================
async function guardarDireccion(event) {
    event.preventDefault();
    
    // Validar sesión
    if (!verificarAutenticacion()) return;

    // Obtener datos del formulario
    const formData = {
        nombre_completo: document.getElementById('registrarNombreCompleto').value.trim(),
        barrio: document.getElementById('registrarBarrio').value.trim(),
        domicilio: document.getElementById('registrarDomicilio').value.trim(),
        referencias: document.getElementById('registrarReferencias').value.trim(),
        telefono: document.getElementById('registrarTelefono').value.trim(),
        departamento_id: document.getElementById('registrarDepartamentoId').value,
        municipio_id: document.getElementById('registrarMunicipioId').value
    };

    // Validación básica
    if (!validarCamposDireccion(formData)) return;

    try {
        const response = await fetch('/guardar-direccion', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: JSON.stringify(formData)
        });

        const data = await response.json();

        if (!response.ok) throw new Error(data.error || "Error desconocido");
        
        mostrarNotificacion('¡Dirección guardada exitosamente!', 'success');
        $('#editarDireccionModal').modal('hide');
        mostrarDirecciones('Domicilio');
        
    } catch (error) {
        console.error('Error:', error);
        mostrarNotificacion(error.message || 'Error al guardar la dirección', 'error');
    }
}
// Función para cargar los departamentos en el modal
function cargarDepartamentos() {
    fetch('/obtener-departamentos')
        .then(response => response.json())
        .then(data => {
            const selectDepartamento = document.getElementById('registrarDepartamentoId');
            selectDepartamento.innerHTML = '<option value="">Seleccione un departamento</option>'; // Limpiar opciones anteriores
            data.forEach(departamento => {
                const option = document.createElement('option');
                option.value = departamento.id;
                option.textContent = departamento.nombre;
                selectDepartamento.appendChild(option);
            });
        })
        .catch(error => console.error('Error al cargar departamentos:', error));
}

// Función para cargar los municipios cuando se selecciona un departamento
function cargarMunicipios(departamentoId) {
    fetch(`/obtener_municipios?departamento_id=${departamentoId}`)
        .then(response => response.json())
        .then(data => {
            const selectMunicipio = document.getElementById('registrarMunicipioId');
            selectMunicipio.innerHTML = '<option value="">Seleccione un municipio</option>'; // Limpiar opciones anteriores
            data.forEach(municipio => {
                const option = document.createElement('option');
                option.value = municipio.id;
                option.textContent = municipio.nombre;
                selectMunicipio.appendChild(option);
            });
        })
        .catch(error => console.error('Error al cargar municipios:', error));
}

// Evento para cargar los departamentos cuando el modal se abre
document.getElementById('editarDireccionModal').addEventListener('shown.bs.modal', function () {
    cargarDepartamentos();
});

// Evento para cargar los municipios cuando se selecciona un departamento
document.getElementById('registrarDepartamentoId').addEventListener('change', function () {
    const departamentoId = this.value;
    if (departamentoId) {
        cargarMunicipios(departamentoId);
    } else {
        // Limpiar municipios si no se selecciona un departamento
        const selectMunicipio = document.getElementById('registrarMunicipioId');
        selectMunicipio.innerHTML = '<option value="">Seleccione un municipio</option>';
    }
});
// ==================== FUNCIONES AUXILIARES ====================
function handleResponse(response) {
    if (!response.ok) throw new Error('Error en la respuesta del servidor');
    return response.json();
}

function handleError(error) {
    console.error('Error:', error);
    mostrarNotificacion('Ocurrió un error inesperado', 'error');
}

function mostrarNotificacion(mensaje, tipo) {
    const notificacion = document.createElement('div');
    notificacion.className = `notificacion ${tipo}`;
    notificacion.textContent = mensaje;
    document.body.appendChild(notificacion);
    setTimeout(() => notificacion.remove(), 3000);
}

// ==================== INICIALIZACIÓN ====================
// Modificar la función de inicialización
document.addEventListener('DOMContentLoaded', () => {
    cargarCarrito();
    
    // Cargar departamentos cuando se abre el modal
    const modalDireccion = document.getElementById('editarDireccionModal');
    if (modalDireccion) {
        modalDireccion.addEventListener('show.bs.modal', () => {
            cargarDepartamentos();
            // Reiniciar municipios al abrir el modal
            const selectMunicipio = document.getElementById('registrarMunicipioId');
            selectMunicipio.innerHTML = '<option value="">Seleccione un municipio</option>';
        });
    }

    // Manejar cambio de departamento
    document.getElementById('registrarDepartamentoId')?.addEventListener('change', function() {
        cargarMunicipios(this.value);
    });
});

// ==================== FUNCIONES RESTANTES ORGANIZADAS ====================
function verificarAutenticacion() {
    const isLoggedIn = document.querySelector('.user-info-container') !== null;
    if (!isLoggedIn) {
        mostrarNotificacion('Debe iniciar sesión para esta acción', 'error');
        setTimeout(() => window.location.href = '/login-cliente', 1500);
        return false;
    }
    return true;
}

function generarHTMLCarrito() {
    let totalCompra = 0;
    let html = '';
    
    carritoItems.forEach(producto => {
        const subtotal = producto.precio * producto.cantidad;
        totalCompra += subtotal;
        
        html += `
            <div class="carrito-item">
                <div class="item-info">
                    <img src="${producto.imagen}" alt="${producto.nombre}">
                    <div class="item-details">
                        <h6>${producto.nombre}</h6>
                        <p class="item-price">$${producto.precio.toLocaleString()}</p>
                        <div class="quantity-control">
                            <button class="quantity-btn" onclick="actualizarCantidad(${producto.id}, -1)">-</button>
                            <span class="quantity">${producto.cantidad}</span>
                            <button class="quantity-btn" onclick="actualizarCantidad(${producto.id}, 1)">+</button>
                        </div>
                    </div>
                </div>
                <div class="item-subtotal">
                    <p>$${subtotal.toLocaleString()}</p>
                    <button class="delete-btn" onclick="eliminarDelCarrito(${producto.id})">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
        `;
    });

    return html + `
        <div class="carrito-total"><h5><strong>Total:</strong> $${totalCompra.toLocaleString()}</h5></div>
        <div class="carrito-footer">
            <button class="btn-procesar" onclick="procesarPedido()">
                <i class="fas fa-check-circle"></i> Procesar Pedido
            </button>
        </div>
    `;
}

function poblarSelect(data, selectId, tipo) {
    const select = document.getElementById(selectId);
    select.innerHTML = `<option value="">Seleccione un ${tipo}</option>`;
    data.forEach(item => {
        select.innerHTML += `<option value="${item.id}">${item.nombre}</option>`;
    });
}

function manejarRespuestaCarrito(data, accion) {
    if (data.status === 'success') {
        cargarCarrito();
        mostrarNotificacion(`Producto ${accion} correctamente`, 'success');
        animarIconoCarrito();
    } else {
        mostrarNotificacion(data.mensaje, 'error');
    }
}

function animarIconoCarrito() {
    const icono = document.querySelector('.carrito-icono');
    icono?.classList.add('carrito-animado');
    setTimeout(() => icono?.classList.remove('carrito-animado'), 500);
}

// Mantener las demás funciones esenciales sin duplicados
// ... (procesarPedido, mostrarDirecciones, confirmarPedido, etc)