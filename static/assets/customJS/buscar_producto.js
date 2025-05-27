function buscarProductoAjax() {
  const query = document.getElementById("search_producto").value.trim();
    
  // Si la búsqueda está vacía, recargar la tabla con todos los productos
  if (query === "") {
    fetch('/lista-de-productos')
      .then(response => response.text())
      .then(data => {
        const parser = new DOMParser();
        const doc = parser.parseFromString(data, 'text/html');
        const newTableBody = doc.getElementById('tabla_productos_body').innerHTML;
        document.getElementById('tabla_productos_body').innerHTML = newTableBody;
        
        // Reconectar eventos después de recargar la tabla
        conectarEventosAcciones();
      })
      .catch(error => console.error('Error al recargar la tabla:', error));
    return;
  }
    
  // Configurar la solicitud AJAX
  fetch('/buscando-producto', {
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
        document.getElementById('tabla_productos_body').innerHTML = data.html;
        
        // Reconectar eventos después de actualizar la tabla
        conectarEventosAcciones();
      } else {
        // Si no hay resultados, mostrar el mensaje
        document.getElementById('tabla_productos_body').innerHTML = data.html;
      }
    })
    .catch(error => {
      console.error('Error:', error);
      alert("Hubo un error al realizar la búsqueda.");
    });
}

  function eliminarProducto(idProducto) {
    if (confirm("¿Estás seguro de que deseas eliminar este producto?")) {
      fetch(`/eliminar-producto/${idProducto}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
        },
      })
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            // Eliminar la fila de la tabla
            const fila = document.getElementById(`producto_${idProducto}`);
            if (fila) {
              fila.remove();
            }
            alert("Producto eliminado correctamente.");
          } else {
            alert("Error al eliminar el producto.");
          }
        })
        .catch(error => {
          console.error('Error:', error);
          alert("Hubo un error al intentar eliminar el producto.");
        });
    }
  }