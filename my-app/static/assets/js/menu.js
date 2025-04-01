document.addEventListener('DOMContentLoaded', function() {
    // Función para actualizar el contador del carrito
    function actualizarContadorCarrito(cantidad) {
        const contador = document.getElementById('carrito-count');
        if(contador) {
            contador.textContent = cantidad;
        }
    }
    
    // Ejemplo: Actualizar contador (puedes reemplazar con tu lógica)
    actualizarContadorCarrito(3);
    
    // Otras funcionalidades pueden ir aquí
});