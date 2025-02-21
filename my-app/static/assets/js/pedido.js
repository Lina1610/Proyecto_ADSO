

let carrito = JSON.parse(localStorage.getItem("carrito")) || [];
let total = parseFloat(localStorage.getItem("total")) || 0;

function agregarAlCarrito() {
    // Corregir la obtención de la cantidad
    let cantidad = parseInt(document.getElementById("cantidad").value);
    if (isNaN(cantidad)) {
        cantidad = 1;
    }

    if (cantidad <= 0) {
        carrito = [];
        total = 0;
        actualizarVistaCarrito();
        guardarEnLocalStorage();
        actualizarContadorCarrito();
        return;
    }

    // Resto del código sin cambios...
    const producto = {
        nombre: "Tamal de Pollo",
        precio: 9000,
        cantidad: cantidad
    };

    const existe = carrito.find(item => item.nombre === producto.nombre);
    if (existe) {
        existe.cantidad = cantidad;
    } else {
        carrito.push(producto);
    }

    total = carrito.reduce((acc, item) => acc + item.precio * item.cantidad, 0);

    actualizarVistaCarrito();
    guardarEnLocalStorage();
    actualizarContadorCarrito();
}

// Las demás funciones permanecen igual...

function actualizarVistaCarrito() {
    const listaItems = document.getElementById("lista-items");
    const totalElement = document.getElementById("total-carrito");

    listaItems.innerHTML = "";

    carrito.forEach((item) => {
        const itemHTML = `
            <div class="item-carrito">
                <span class="nombre-item">${item.nombre}</span>
                <div class="detalle-item">
                    <span class="cantidad">${item.cantidad}x</span>
                    <span class="precio">$${(item.precio * item.cantidad).toFixed(2)}</span>
                </div>
            </div>
        `;
        listaItems.insertAdjacentHTML("beforeend", itemHTML);
    });

    if (carrito.length > 0 && carrito.reduce((acc, item) => acc + item.cantidad, 0) > 0) {
        totalElement.textContent = `$${total.toFixed(2)}`;
    } else {
        totalElement.textContent = "$0.00";
    }
}
function confirmarPedido() {
    window.location.href = "{{ url_for('carritoCompras') }}";
}

document.getElementById("cantidad").addEventListener("keydown", function(event) {
    if (event.key === "-") {
        event.preventDefault();
    }
});
function guardarEnLocalStorage() {
    localStorage.setItem("carrito", JSON.stringify(carrito));
    localStorage.setItem("total", total.toString());
}

function cambiarCantidad(cambio) {
    let cantidadInput = document.getElementById("cantidad");
    let valorActual = parseInt(cantidadInput.value);

    if (isNaN(valorActual)) {
        valorActual = 1;
    }

    let nuevaCantidad = valorActual + cambio;

    if (nuevaCantidad < 1) {
        nuevaCantidad = 1;
    }

    cantidadInput.value = nuevaCantidad;
}

function actualizarContadorCarrito() {
    const contador = document.getElementById("contador-carrito");
    let totalItems = carrito.reduce((acc, item) => acc + item.cantidad, 0);
    contador.textContent = totalItems;
}

document.getElementById("cantidad").addEventListener("keydown", function(event) {
    if (event.key === "-") {
        event.preventDefault();
    }
});

actualizarContadorCarrito();