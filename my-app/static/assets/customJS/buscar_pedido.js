// Función para buscar pedidos mediante AJAX
function buscarPedidoAjax() {
    const query = document.getElementById("search_pedidos").value.trim();
  
    // Si la búsqueda está vacía, recargar la tabla con todos los pedidos
    if (query === "") {
        fetch('/lista-de-pedidos')
            .then(response => response.text())
            .then(data => {
                const parser = new DOMParser();
                const doc = parser.parseFromString(data, 'text/html');
                const newTableBody = doc.getElementById('tabla_pedidos_body').innerHTML;
                document.getElementById('tabla_pedidos_body').innerHTML = newTableBody;
            })
            .catch(error => console.error('Error al recargar la tabla:', error));
        return;
    }
  
    // Configurar la solicitud AJAX
    fetch('/buscando-pedido', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ busqueda: query }),
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Si hay resultados, actualizar la tabla
                document.getElementById('tabla_pedidos_body').innerHTML = data.html;
            } else {
                // Si no hay resultados, mostrar el mensaje
                document.getElementById('tabla_pedidos_body').innerHTML = data.html;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert("Hubo un error al realizar la búsqueda.");
        });
}

// Función para eliminar un pedido
function eliminarPedido(idPedido) {
    if (confirm("¿Estás seguro de que deseas eliminar este pedido?")) {
        fetch(`/eliminar-pedido/${idPedido}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            },
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Eliminar la fila de la tabla
                    const fila = document.getElementById(`pedido_${idPedido}`);
                    if (fila) {
                        fila.remove();
                    }
                    alert("Pedido eliminado correctamente.");
                } else {
                    alert("Error al eliminar el pedido.");
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert("Hubo un error al intentar eliminar el pedido.");
            });
    }
}