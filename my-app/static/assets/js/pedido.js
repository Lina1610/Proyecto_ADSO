let carrito = [];
let total = 0;
let historial = JSON.parse(localStorage.getItem('historial')) || [];

// Esperar a que el DOM esté completamente cargado
document.addEventListener('DOMContentLoaded', () => {
    actualizarCarrito();
});

// Agregar producto al carrito
function agregarAlCarrito() {
    const cantidadInput = document.getElementById('cantidad');
    const cantidad = parseInt(cantidadInput.value);

    if (isNaN(cantidad) || cantidad <= 0) {
        alert("Por favor, ingresa una cantidad válida.");
        return;
    }

    let productoExistente = carrito.find(p => p.nombre === 'Tamal de Pollo');

    if (productoExistente) {
        productoExistente.cantidad += cantidad;
    } else {
        const producto = {
            nombre: 'Tamal de Pollo',
            precio: 5.00,
            cantidad: cantidad
        };
        carrito.push(producto);
    }

    total += 5.00 * cantidad;
    actualizarCarrito();
}

// Actualizar carrito y contador en el menú
function actualizarCarrito() {
    const carritoLista = document.getElementById('carrito-lista');
    const totalCarrito = document.getElementById('total-carrito');
    const contador = document.querySelector('.contador');

    if (!carritoLista || !totalCarrito || !contador) {
        console.error("Elementos del carrito no encontrados en el DOM.");
        return;
    }

    carritoLista.innerHTML = '';
    let totalItems = 0;

    carrito.forEach((producto, index) => {
        totalItems += producto.cantidad;
        const li = document.createElement('li');
        li.innerHTML = `
            ${producto.nombre} x ${producto.cantidad} - $${(producto.precio * producto.cantidad).toFixed(2)}
            <button onclick="eliminarProducto(${index})">X</button>
        `;
        carritoLista.appendChild(li);
    });

    totalCarrito.textContent = total.toFixed(2);
    contador.textContent = totalItems;
}

// Eliminar producto del carrito
function eliminarProducto(index) {
    total -= carrito[index].precio * carrito[index].cantidad;
    carrito.splice(index, 1);
    actualizarCarrito();
}

// Mostrar / ocultar el carrito
function mostrarCarrito() {
    const carritoDiv = document.getElementById('carrito-container');
    carritoDiv.style.display = carritoDiv.style.display === 'block' ? 'none' : 'block';
}

// Confirmar pedido
function confirmarPedido() {
    if (carrito.length === 0) {
        alert("No hay productos en el carrito.");
        return;
    }

    const pedido = {
        id: Date.now(),
        cantidad: carrito.reduce((sum, item) => sum + item.cantidad, 0),
        total: total
    };

    historial.push(pedido);
    localStorage.setItem('historial', JSON.stringify(historial));

    carrito = [];
    total = 0;
    actualizarCarrito();

    alert("Pedido confirmado correctamente.");
    mostrarHistorial();
}

// Cargar historial de pedidos
function cargarHistorial() {
    const historialDiv = document.getElementById('historial-pedidos');
    const totalGastado = document.getElementById('total-gastado');

    if (!historialDiv || !totalGastado) return;

    historialDiv.innerHTML = '';
    let totalHistorial = 0;

    if (historial.length === 0) {
        historialDiv.innerHTML = '<p>No hay pedidos registrados.</p>';
    } else {
        historial.forEach((pedido) => {
            const pedidoDiv = document.createElement('div');
            pedidoDiv.className = 'pedido';
            pedidoDiv.innerHTML = `
                <p><strong>Pedido #${pedido.id}</strong></p>
                <p><strong>Cantidad:</strong> ${pedido.cantidad}</p>
                <p><strong>Total:</strong> $${pedido.total.toFixed(2)}</p>
            `;
            historialDiv.appendChild(pedidoDiv);
            totalHistorial += pedido.total;
        });
    }

    totalGastado.textContent = totalHistorial.toFixed(2);
}
