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

// Función para procesar el pedido
function procesarPedido() {
    // Verificar si hay productos en el carrito
    if (carritoItems.length === 0) {
        mostrarNotificacion('El carrito está vacío', 'error');
        return;
    }
    
    fetch('/carrito/finalizar-compra', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            mostrarNotificacion('¡Pedido procesado con éxito!', 'success');
            // Recargar el carrito vacío
            cargarCarrito();
        } else {
            mostrarNotificacion(data.mensaje, 'error');
        }
    })
    .catch(error => {
        console.error('Error al procesar el pedido:', error);
        mostrarNotificacion('Error al procesar el pedido', 'error');
    });
}

// Función para mostrar notificaciones
function mostrarNotificacion(mensaje, tipo) {
    // Crear el elemento de notificación
    const notificacion = document.createElement('div');
    notificacion.className = `notificacion ${tipo}`;
    notificacion.textContent = mensaje;
    
    // Agregar al cuerpo del documento
    document.body.appendChild(notificacion);
    
    // Mostrar la notificación
    setTimeout(() => {
        notificacion.classList.add('mostrar');
    }, 100);
    
    // Eliminar la notificación después de 3 segundos
    setTimeout(() => {
        notificacion.classList.remove('mostrar');
        setTimeout(() => {
            document.body.removeChild(notificacion);
        }, 300);
    }, 3000);
}

// Cargar el carrito cuando se carga la página
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar el carrito
    cargarCarrito();
    
    // Añadir evento de clic al icono del carrito
    const carritoIcono = document.querySelector('.carrito-icono');
    if (carritoIcono) {
        carritoIcono.addEventListener('click', toggleCarrito);
    }
});