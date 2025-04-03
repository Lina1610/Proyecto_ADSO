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
        // Mostrar notificación en lugar de alert
        mostrarNotificacion('Debe iniciar sesión para agregar productos al carrito', 'error');
        
        // Retrasar la redirección para que la notificación se muestre
        setTimeout(() => {
            window.location.href = '/login-cliente'; // Redirigir al login después de 3 segundos
        }, 3000); // 3000 ms = 3 segundos
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
            // Mostrar notificación para errores
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
    const itemIndex = carritoItems.findIndex(item => item.id === carrito_id);
    
    if (itemIndex !== -1) {
        const nuevaCantidad = carritoItems[itemIndex].cantidad + change;
        
        if (nuevaCantidad < 1) {
            eliminarDelCarrito(carrito_id);
            return;
        }
        
        // Actualizar el estado local primero
        carritoItems[itemIndex].cantidad = nuevaCantidad;
        
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
                // Actualizar la interfaz del carrito
                actualizarInterfazCarrito();
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

// Función para eliminar un producto del carrito....
function eliminarDelCarritoConfirmacion(carrito_id) {
    // Send the delete request to the server
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
            // Update cart from server
            cargarCarrito();
            
            // Update the confirmation modal
            setTimeout(() => {
                const carritoConfirmacionItems = document.getElementById('carrito-confirmacion-items');
                if (carritoConfirmacionItems) {
                    carritoConfirmacionItems.innerHTML = generarHTMLCarritoConfirmacion();
                    actualizarTotalConfirmacion();
                }
            }, 200);
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

function agregarProductoEnModal(producto_id, nombre, precio, imagen) {
    // Verificar si el usuario está conectado
    const isUserLoggedIn = document.querySelector('.user-info-container') !== null;
    
    if (!isUserLoggedIn) {
        // Mostrar notificación en lugar de alert
        mostrarNotificacion('Debe iniciar sesión para agregar productos al carrito', 'error');
        
        // Retrasar la redirección para que la notificación se muestre
        setTimeout(() => {
            window.location.href = '/login-cliente'; // Redirigir al login después de 3 segundos
        }, 3000); // 3000 ms = 3 segundos
        return;
    }
    
    // Enviar la solicitud al servidor
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
            // Actualizar carrito cargando desde el servidor
            cargarCarrito();
            
            // Después de cargar el carrito, actualizar el modal de confirmación
            setTimeout(() => {
                const carritoConfirmacionItems = document.getElementById('carrito-confirmacion-items');
                if (carritoConfirmacionItems) {
                    carritoConfirmacionItems.innerHTML = generarHTMLCarritoConfirmacion();
                    actualizarTotalConfirmacion();
                }
            }, 200); // Pequeño retraso para asegurar que cargarCarrito se complete
        } else {
            // Mostrar notificación para errores
            mostrarNotificacion(data.mensaje, 'error');
        }
    })
    .catch(error => {
        console.error('Error al agregar al carrito:', error);
        mostrarNotificacion('Error al agregar al carrito', 'error');
    });
}

// Función para mostrar notificaciones
function mostrarNotificacion(mensaje, tipo) {
    console.log("Notificación:", mensaje, "Tipo:", tipo); // Debug

    const notificacion = document.createElement('div');
    notificacion.className = `notificacion ${tipo}`;
    notificacion.textContent = mensaje;

    document.body.appendChild(notificacion);

    setTimeout(() => {
        console.log("Mostrando notificación en pantalla...");
        notificacion.classList.add('mostrar');
    }, 100);

    setTimeout(() => {
        console.log("Ocultando notificación...");
        notificacion.classList.remove('mostrar');
        setTimeout(() => {
            console.log("Eliminando notificación del DOM...");
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
// Función para finalizar la compra
async function finalizarCompra() {
    try {
        // Obtener datos del formulario
        const tipoEntrega = document.querySelector('input[name="tipo_entrega"]:checked')?.value;
        const metodoPago = document.querySelector('input[name="metodo_pago"]:checked');
        const direccion = document.querySelector('input[name="direccion"]:checked');
        
        // Validación básica
        if (!tipoEntrega || !metodoPago) {
            mostrarNotificacion('Seleccione método de pago y tipo de entrega', 'error');
            return;
        }

        if (tipoEntrega === 'Domicilio' && !direccion) {
            mostrarNotificacion('Seleccione una dirección para entrega a domicilio', 'error');
            return;
        }

        // Guardar copia de los items del carrito antes de limpiarlo
        const itemsCarrito = [...carritoItems];
        const totalCarrito = calcularTotalCarrito();

        // Mostrar carga
        mostrarNotificacion('Procesando pedido...', 'info');

        // Preparar datos
        const formData = {
            tipo_entrega: tipoEntrega,
            metodo_pago_id: metodoPago.value,
            direccion_id: tipoEntrega === 'Domicilio' ? direccion.value : null
        };

        // Enviar al servidor
        const response = await fetch('/carrito/finalizar-compra', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });

        const data = await response.json();

        if (data.status === 'success') {
            // 1. Mostrar notificación de éxito
            mostrarNotificacion(data.mensaje, 'success');
            
            // 2. Actualizar interfaz del carrito
            carritoItems = [];
            actualizarInterfazCarrito();
            
            // 3. Cerrar modales
            const modales = [
                'modalProcesarPedido',
                'modalDirecciones',
                'modalConfirmarPedido'
            ];
            
            modales.forEach(modalId => {
                const modal = bootstrap.Modal.getInstance(document.getElementById(modalId));
                if (modal) modal.hide();
            });
            
            // 4. Enviar información a WhatsApp usando la copia guardada
            enviarPedidoWhatsApp(tipoEntrega, metodoPago, direccion, itemsCarrito, totalCarrito);
            
        } else {
            mostrarNotificacion(data.mensaje || 'Error al crear pedido', 'error');
        }

    } catch (error) {
        console.error('Error:', error);
        mostrarNotificacion('Error de conexión', 'error');
    }
}

// Función para calcular el total del carrito
function calcularTotalCarrito() {
    return carritoItems.reduce((total, item) => total + (item.precio * item.cantidad), 0);
}

function enviarPedidoWhatsApp(tipoEntrega, metodoPago, direccion, itemsCarrito, totalCarrito) {
    // Obtener información del usuario
    const nombreUsuario = document.querySelector('.user-name')?.textContent || 'Cliente no identificado';
    
    // Obtener texto del método de pago
    const metodoPagoTexto = document.querySelector(`label[for="metodo_pago_${metodoPago.value}"]`)?.textContent.trim() || 'Método no especificado';
    
    // Construir mensaje con formato mejorado
    let mensaje = `*NUEVO PEDIDO - EL RINCÓN DEL TAMAL*%0A%0A`;
    
    // Información del cliente
    mensaje += `*Cliente:* ${nombreUsuario}%0A`;
    mensaje += `*Tipo de entrega:* ${tipoEntrega}%0A`;
    mensaje += `*Método de pago:* ${metodoPagoTexto}%0A%0A`;
    
    // Detalles de entrega si es domicilio
    if (tipoEntrega === 'Domicilio' && direccion) {
        const direccionElement = document.querySelector(`input[name="direccion"][value="${direccion.value}"]`)?.parentElement;
        if (direccionElement) {
            const direccionTexto = direccionElement.textContent.trim();
            
            mensaje += `*DATOS DE ENTREGA*%0A`;
            
            // Extraer componentes usando una expresión regular más robusta
            const match = direccionTexto.match(
                /(.+)\n(.+)\n(.+)\n(.+),\s*(.+)\nTeléfono:\s*(.+)/
            );
            
            if (match) {
                mensaje += `*Nombre del que recibe:* ${match[1].trim()}%0A`;
                mensaje += `*Dirección de entrega:* ${match[2].trim()}%0A`;
                mensaje += `*Barrio:* ${match[3].trim()}%0A`;
                mensaje += `*Ciudad:* ${match[4].trim()}%0A`;
                mensaje += `*Departamento:* ${match[5].trim()}%0A`;
                mensaje += `*Teléfono:* ${match[6].trim()}%0A%0A`;
            } else {
                // Formato alternativo si no coincide el regex
                const lineas = direccionTexto.split('\n').map(line => line.trim()).filter(line => line);
                
                mensaje += `*Nombre del que recibe:* ${lineas[0] || 'No especificado'}%0A`;
                mensaje += `*Dirección de entrega:* ${lineas[1] || 'No especificada'}%0A`;
                
                // Si hay más campos disponibles para mostrar
                if (lineas.length > 2 && !lineas[2].includes('Teléfono:')) {
                    mensaje += `*Ubicación adicional:* ${lineas[2] || 'No especificada'}%0A`;
                }
                
                // Buscar específicamente "Teléfono" en las líneas
                const telefonoLine = lineas.find(line => line.includes('Teléfono:'));
                const telefono = telefonoLine ? telefonoLine.replace('Teléfono:', '').trim() : 'No especificado';
                
                mensaje += `*Teléfono:* ${telefono}%0A%0A`;
            }
        }
    }
    
    // Lista de productos con precio unitario
    mensaje += `*PRODUCTOS*%0A`;
    itemsCarrito.forEach(item => {
        mensaje += `- *${item.nombre}*%0A`;
        mensaje += `  Cantidad: ${item.cantidad}%0A`;
        mensaje += `  Precio unitario: $${item.precio.toLocaleString()}%0A`;
        mensaje += `  Subtotal: $${(item.precio * item.cantidad).toLocaleString()}%0A%0A`;
    });
    
    // Total del pedido
    mensaje += `*TOTAL DEL PEDIDO:* $${totalCarrito.toLocaleString()}`;
    
    // Número de WhatsApp
    const telefonoWhatsApp = '573219063543';
    const urlWhatsApp = `https://wa.me/${telefonoWhatsApp}?text=${mensaje}`;
    window.open(urlWhatsApp, '_blank');
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
                    <input class="form-check-input" type="radio" name="metodo_pago" id="metodo_pago_${metodo.id}" value="${metodo.id}" required>
                    <label class="form-check-label" for="metodo_pago_${metodo.id}">
                        ${metodo.metodo}
                    </label>
                </div>
            `).join('');

            modalBody.innerHTML += `<h5>Métodos de Pago</h5>${metodosPagoHTML}`;

            // Mostrar tipos de entrega
            const tiposEntregaHTML = data.tipos_entrega.map(tipo => `
                <div class="form-check">
                    <input class="form-check-input" type="radio" name="tipo_entrega" id="tipo_entrega_${tipo}" value="${tipo}" required>
                    <label class="form-check-label" for="tipo_entrega_${tipo}">
                        ${tipo}
                    </label>
                </div>
            `).join('');

            modalBody.innerHTML += `<h5 class="mt-3">Tipos de Entrega</h5>${tiposEntregaHTML}`;

            // Agregar botón de confirmar
            modalBody.innerHTML += `
                <div class="d-grid gap-2 mt-4">
                    <button class="btn btn-primary" onclick="validarProcesarPedido()">Confirmar</button>
                </div>
            `;

            // Mostrar el modal de procesar pedido
            const modalProcesarPedido = new bootstrap.Modal(document.getElementById('modalProcesarPedido'));
            modalProcesarPedido.show();
        })
        .catch(error => {
            console.error('Error al obtener métodos de pago y tipos de entrega:', error);
            mostrarNotificacion('Error al cargar métodos de pago y tipos de entrega', 'error');
        });
}

function validarProcesarPedido() {
    const metodoPago = document.querySelector('input[name="metodo_pago"]:checked');
    const tipoEntrega = document.querySelector('input[name="tipo_entrega"]:checked');

    if (!metodoPago) {
        mostrarNotificacion('Por favor, selecciona un método de pago.', 'error');
        return;
    }

    if (!tipoEntrega) {
        mostrarNotificacion('Por favor, selecciona un tipo de entrega.', 'error');
        return;
    }

    // Cerrar el modal actual (Procesar Pedido)
    const modalProcesarPedido = bootstrap.Modal.getInstance(document.getElementById('modalProcesarPedido'));
    modalProcesarPedido.hide();

    if (tipoEntrega.value === 'Domicilio') {
        // Si el tipo de entrega es "Domicilio", mostrar el modal de direcciones
        mostrarDirecciones('Domicilio');
    } else {
        // Si no es "Domicilio", mostrar el modal de confirmación directamente
        mostrarModalConfirmacion();
    }
}
function mostrarModalConfirmacion() {
    // Cerrar el Modal 3 (si está abierto)
    const modalDirecciones = bootstrap.Modal.getInstance(document.getElementById('modalDirecciones'));
    if (modalDirecciones) modalDirecciones.hide();

    // Mostrar el contenido del carrito en el Modal 4
    const carritoConfirmacionItems = document.getElementById('carrito-confirmacion-items');
    carritoConfirmacionItems.innerHTML = generarHTMLCarritoConfirmacion();

    // Actualizar el total en el Modal 4
    actualizarTotalConfirmacion();

    // Mostrar el Modal 4
    const modalConfirmarPedido = new bootstrap.Modal(document.getElementById('modalConfirmarPedido'));
    modalConfirmarPedido.show();
}

function generarHTMLCarritoConfirmacion() {
    let html = '';

    carritoItems.forEach((producto) => {
        const subtotal = producto.precio * producto.cantidad;

        html += `
            <div class="carrito-item">
                <div class="item-info">
                    <img src="${producto.imagen}" alt="${producto.nombre}">
                    <div class="item-details">
                        <h6>${producto.nombre}</h6>
                        <p class="item-price">$${producto.precio.toLocaleString()}</p>
                        <div class="quantity-control">
                            <button class="quantity-btn" onclick="actualizarCantidadConfirmacion(${producto.id}, -1)">-</button>
                            <span class="quantity">${producto.cantidad}</span>
                            <button class="quantity-btn" onclick="actualizarCantidadConfirmacion(${producto.id}, 1)">+</button>
                        </div>
                    </div>
                </div>
                <div class="item-subtotal">
                    <p>$${subtotal.toLocaleString()}</p>
                    <button class="delete-btn" onclick="eliminarDelCarritoConfirmacion(${producto.id})">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
        `;
    });

    return html;
}

function actualizarCantidadConfirmacion(carrito_id, change) {
    const itemIndex = carritoItems.findIndex(item => item.id === carrito_id);
    
    if (itemIndex !== -1) {
        const nuevaCantidad = carritoItems[itemIndex].cantidad + change;
        
        if (nuevaCantidad < 1) {
            eliminarDelCarritoConfirmacion(carrito_id);
            return;
        }
        
        // Update the local state first for responsiveness
        carritoItems[itemIndex].cantidad = nuevaCantidad;
        
        // Send the update to the server
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
                // Reload the cart from server to ensure synchronization
                cargarCarrito();
                
                // Update the confirmation modal
                const carritoConfirmacionItems = document.getElementById('carrito-confirmacion-items');
                if (carritoConfirmacionItems) {
                    carritoConfirmacionItems.innerHTML = generarHTMLCarritoConfirmacion();
                    actualizarTotalConfirmacion();
                }
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

function eliminarDelCarritoConfirmacion(carrito_id) {
    // Send the delete request to the server
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
            // Update cart from server
            cargarCarrito();
            
            // Update the confirmation modal
            setTimeout(() => {
                const carritoConfirmacionItems = document.getElementById('carrito-confirmacion-items');
                if (carritoConfirmacionItems) {
                    carritoConfirmacionItems.innerHTML = generarHTMLCarritoConfirmacion();
                    actualizarTotalConfirmacion();
                }
            }, 200);
        } else {
            mostrarNotificacion(data.mensaje, 'error');
        }
    })
    .catch(error => {
        console.error('Error al eliminar del carrito:', error);
        mostrarNotificacion('Error al eliminar del carrito', 'error');
    });
}
function eliminarDelCarritoConfirmacion(producto_id) {
    // Enviar la solicitud al backend para eliminar el producto
    fetch('/carrito/eliminar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            carrito_id: producto_id
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            // Eliminar el producto del carrito principal
            carritoItems = carritoItems.filter(item => item.id !== producto_id);

            // Actualizar la interfaz del carrito principal
            actualizarInterfazCarrito();

            // Actualizar el Modal 4
            const carritoConfirmacionItems = document.getElementById('carrito-confirmacion-items');
            if (carritoConfirmacionItems) {
                carritoConfirmacionItems.innerHTML = generarHTMLCarritoConfirmacion();
                actualizarTotalConfirmacion();
            }

            mostrarNotificacion('Producto eliminado del carrito.', 'success');
        } else {
            mostrarNotificacion(data.mensaje, 'error');
        }
    })
    .catch(error => {
        console.error('Error al eliminar del carrito:', error);
        mostrarNotificacion('Error al eliminar del carrito', 'error');
    });
}
function actualizarTotalConfirmacion() {
    const total = carritoItems.reduce((sum, producto) => sum + producto.precio * producto.cantidad, 0);
    document.getElementById('total-confirmacion').textContent = total.toLocaleString();
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
                            <input type="radio" name="direccion" value="${direccion.id}" class="form-check-input me-2" required>
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

                // Agregar botón de confirmar
                const botonConfirmar = document.createElement('button');
                botonConfirmar.className = 'btn btn-success w-100 mt-3';
                botonConfirmar.innerHTML = '<i class="fas fa-check"></i> Confirmar Dirección';
                botonConfirmar.onclick = () => {
                    // Validar si se ha seleccionado una dirección
                    const direccionSeleccionada = document.querySelector('input[name="direccion"]:checked');
                    if (!direccionSeleccionada) {
                        mostrarNotificacion('Por favor, selecciona una dirección.', 'error');
                        return;
                    }
                    mostrarModalConfirmacion(); // Solo abrir el modal de confirmación si hay una dirección seleccionada
                };
                direccionesContainer.appendChild(botonConfirmar);

                // Mostrar el modal de direcciones
                const modalDirecciones = new bootstrap.Modal(document.getElementById('modalDirecciones'));
                modalDirecciones.show();
            })
            .catch(error => {
                console.error('Error al obtener direcciones:', error);
                mostrarNotificacion('Error al cargar direcciones', 'error');
            });
    }
}

async function guardarDireccion(event) {
    event.preventDefault();
    console.log("Formulario enviado"); // Depuración

    // Verificar autenticación
    if (!verificarAutenticacion()) return;

    // Recolectar datos del formulario
    const formData = {
        nombre_completo: document.getElementById('registrarNombreCompleto').value.trim(),
        barrio: document.getElementById('registrarBarrio').value.trim(),
        domicilio: document.getElementById('registrarDomicilio').value.trim(),
        referencias: document.getElementById('registrarReferencias').value.trim(),
        telefono: document.getElementById('registrarTelefono').value.trim(),
        departamento_id: document.getElementById('registrarDepartamentoId').value,
        municipio_id: document.getElementById('registrarMunicipioId').value
    };
    console.log("Datos enviados:", formData); // Depuración

    // Validar campos obligatorios
    if (!validarCamposDireccion(formData)) return;

    try {
        mostrarNotificacion('Guardando dirección...', 'info');
        
        const response = await fetch('/api/registrar-direccion', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: JSON.stringify(formData)
        });

        const data = await response.json();
        console.log("Respuesta del servidor:", data); // Depuración

        if (data.success) {
            mostrarNotificacion(data.message || '¡Dirección guardada exitosamente!', 'success');
            
            // Cerrar el modal
            const modalEl = document.getElementById('editarDireccionModal');
            if (modalEl) {
                const modal = bootstrap.Modal.getInstance(modalEl);
                if (modal) {
                    modal.hide();
                    console.log("Modal cerrado"); // Depuración
                } else {
                    console.log("No se pudo obtener instancia del modal"); // Depuración
                }
            }

            // Actualizar las direcciones
            if (typeof mostrarDirecciones === 'function') {
                mostrarDirecciones('Domicilio');
                console.log("Direcciones actualizadas"); // Depuración
            }
        } else {
            mostrarNotificacion(data.error || 'Error al guardar la dirección', 'error');
        }
    } catch (error) {
        console.error('Error en guardarDireccion:', error);
        mostrarNotificacion('Error de conexión con el servidor', 'error');
    }
}
function validarCamposDireccion(formData) {
    // Validar que todos los campos obligatorios estén llenos
    if (!formData.nombre_completo || !formData.barrio || !formData.domicilio || !formData.telefono || !formData.departamento_id || !formData.municipio_id) {
        mostrarNotificacion('Todos los campos son obligatorios.', 'error');
        return false; // Retorna false si falta algún campo
    }
    return true; // Retorna true si todos los campos están llenos
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



// ==================== INICIALIZACIÓN ====================
// Modificar la función de inicialización
document.addEventListener('DOMContentLoaded', () => {
    cargarCarrito();
    
    // Vincular el evento submit al formulario
    const form = document.getElementById('formRegistrarDireccion');
    if (form) {
        form.addEventListener('submit', guardarDireccion);
        console.log("Evento submit vinculado al formulario"); // Depuración
    }

    // Cargar departamentos cuando se abre el modal
    const modalDireccion = document.getElementById('editarDireccionModal');
    if (modalDireccion) {
        modalDireccion.addEventListener('show.bs.modal', () => {
            cargarDepartamentos();
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
            </div>
        `;
    });

    html += `
        <div class="carrito-total"><h5><strong>Total:</strong> $${totalCompra.toLocaleString()}</h5></div>
    `;

    return html;
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
function calcularTotalCarrito() {
    console.log("Productos en el carrito:", carritoItems);  // Depuración
    let total = 0;
    carritoItems.forEach(item => {
        total += item.precio * item.cantidad;
    });
    console.log("Total calculado:", total);  // Depuración
    return total;
}
async function confirmarPedido() {
    // Cerrar el modal de confirmación
    const modalConfirmarPedido = bootstrap.Modal.getInstance(document.getElementById('modalConfirmarPedido'));
    modalConfirmarPedido.hide();

    // Obtener métodos de pago y tipos de entrega
    fetch('/obtener-metodos-pago-tipos-entrega')
        .then(response => response.json())
        .then(data => {
            const modalBody = document.getElementById('modal-body-procesar-pedido');
            modalBody.innerHTML = '';

            // Mostrar métodos de pago
            const metodosPagoHTML = data.metodos_pago.map(metodo => `
                <div class="form-check">
                    <input class="form-check-input" type="radio" name="metodo_pago" id="metodo_pago_${metodo.id}" value="${metodo.id}" required>
                    <label class="form-check-label" for="metodo_pago_${metodo.id}">
                        ${metodo.metodo}
                    </label>
                </div>
            `).join('');

            modalBody.innerHTML += `<h5>Métodos de Pago</h5>${metodosPagoHTML}`;

            // Mostrar tipos de entrega
            const tiposEntregaHTML = data.tipos_entrega.map(tipo => `
                <div class="form-check">
                    <input class="form-check-input" type="radio" name="tipo_entrega" id="tipo_entrega_${tipo}" value="${tipo}" required>
                    <label class="form-check-label" for="tipo_entrega_${tipo}">
                        ${tipo}
                    </label>
                </div>
            `).join('');

            modalBody.innerHTML += `<h5 class="mt-3">Tipos de Entrega</h5>${tiposEntregaHTML}`;

            // Agregar botón de confirmar
            modalBody.innerHTML += `
                <div class="d-grid gap-2 mt-4">
                    <button class="btn btn-primary" onclick="validarProcesarPedido()">Confirmar</button>
                </div>
            `;

            // Mostrar el modal de procesar pedido
            const modalProcesarPedido = new bootstrap.Modal(document.getElementById('modalProcesarPedido'));
            modalProcesarPedido.show();
        })
        .catch(error => {
            console.error('Error al obtener métodos de pago y tipos de entrega:', error);
            mostrarNotificacion('Error al cargar métodos de pago y tipos de entrega', 'error');
        });
}