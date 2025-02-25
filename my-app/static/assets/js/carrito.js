// Lista de productos en el carrito
let carrito = [];

// Función para agregar un producto al carrito
function agregarAlCarrito() {
    const producto = {
        nombre: "Tamal Tradicional", // Nombre del producto
        precio: 5000, // Precio del producto
        cantidad: 1, // Cantidad inicial
        imagen: "/static/assets/img/tamal.png", // Imagen del producto
    };

    // Verificar si el producto ya está en el carrito
    const productoExistente = carrito.find((item) => item.nombre === producto.nombre);

    if (productoExistente) {
        // Si el producto ya está en el carrito, incrementar la cantidad
        productoExistente.cantidad += 1;
    } else {
        // Si el producto no está en el carrito, agregarlo
        carrito.push(producto);
    }

    // Actualizar la interfaz del carrito
    actualizarCarrito();
}

// Función para actualizar la interfaz del carrito
// Función para actualizar la interfaz del carrito
function actualizarCarrito() {
    const carritoItems = document.getElementById('carrito-items');
    const carritoCount = document.getElementById('carrito-count');

    // Limpiar el contenido actual del carrito
    carritoItems.innerHTML = '';

    // Variable para almacenar el total de la compra
    let totalCompra = 0;

    // Recorrer la lista de productos en el carrito
    carrito.forEach((producto) => {
        // Calcular el subtotal del producto (precio * cantidad)
        const subtotal = producto.precio * producto.cantidad;
        totalCompra += subtotal; // Sumar al total de la compra

        const nuevoItem = document.createElement('div');
        nuevoItem.innerHTML = `
            <div class="card mb-3">
                <div class="row g-0">
                    <div class="col-md-4">
                        <img src="${producto.imagen}" class="img-fluid rounded-start" alt="${producto.nombre}">
                    </div>
                    <div class="col-md-8">
                        <div class="card-body">
                            <h5 class="card-title">${producto.nombre}</h5>
                            <p class="card-text">$${producto.precio.toLocaleString()}</p>
                            <div class="quantity-control">
                                <button class="btn btn-outline-secondary btn-sm" onclick="updateQuantity(this, -1, '${producto.nombre}')">-</button>
                                <span class="mx-3">${producto.cantidad}</span>
                                <button class="btn btn-outline-secondary btn-sm" onclick="updateQuantity(this, 1, '${producto.nombre}')">+</button>
                            </div>
                            <p class="card-text"><strong>Subtotal:</strong> $${subtotal.toLocaleString()}</p>
                        </div>
                    </div>
                </div>
            </div>
        `;
        carritoItems.appendChild(nuevoItem);
    });

    // Mostrar el total de la compra en el carrito
    const totalElement = document.createElement('div');
    totalElement.classList.add('total-compra');
    totalElement.innerHTML = `<h5 class="text-end"><strong>Total:</strong> $${totalCompra.toLocaleString()}</h5>`;
    carritoItems.appendChild(totalElement);

    // Actualizar el contador del carrito
    const totalItems = carrito.reduce((total, producto) => total + producto.cantidad, 0);
    carritoCount.textContent = totalItems;
}

// Función para actualizar la cantidad de un producto en el carrito
function updateQuantity(button, change, nombreProducto) {
    const producto = carrito.find((item) => item.nombre === nombreProducto);

    if (producto) {
        producto.cantidad += change;

        // Si la cantidad es menor a 1, eliminar el producto del carrito
        if (producto.cantidad < 1) {
            carrito = carrito.filter((item) => item.nombre !== nombreProducto);
        }

        // Actualizar la interfaz del carrito
        actualizarCarrito();
    }
}

// Función para mostrar/ocultar el carrito
function toggleCarrito() {
    const carritoContainer = document.getElementById('carrito-container');
    carritoContainer.classList.toggle('visible');
}

// Función para procesar el pedido
function procesarPedido() {
    alert('Pedido procesado con éxito.');
    carrito = []; // Vaciar el carrito
    actualizarCarrito(); // Actualizar la interfaz
}

