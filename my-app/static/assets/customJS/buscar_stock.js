function buscarStockAjax() {
    const query = document.getElementById("search_stock").value.trim();
  
    // Si la búsqueda está vacía, recargar la tabla con todos los stocks
    if (query === "") {
        fetch('/lista-de-stock')
            .then(response => response.text())
            .then(data => {
                const parser = new DOMParser();
                const doc = parser.parseFromString(data, 'text/html');
                const newTableBody = doc.getElementById('tabla_stock_body').innerHTML;
                document.getElementById('tabla_stock_body').innerHTML = newTableBody;
            })
            .catch(error => console.error('Error al recargar la tabla:', error));
        return;
    }

    // Configurar la solicitud AJAX
    fetch('/buscando-stock', {
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
                document.getElementById('tabla_stock_body').innerHTML = data.html;
            } else {
                // Si no hay resultados, mostrar el mensaje
                document.getElementById('tabla_stock_body').innerHTML = data.html;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert("Hubo un error al realizar la búsqueda.");
        });
}
function eliminarStock(idStock) {
    if (confirm("¿Estás seguro de que deseas eliminar este stock?")) {
        fetch(`/eliminar-stock/${idStock}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            },
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Eliminar la fila de la tabla
                    const fila = document.getElementById(`stock_${idStock}`);
                    if (fila) {
                        fila.remove();
                    }
                    alert("Stock eliminado correctamente.");
                } else {
                    alert("Error al eliminar el stock.");
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert("Hubo un error al intentar eliminar el stock.");
            });
    }
}