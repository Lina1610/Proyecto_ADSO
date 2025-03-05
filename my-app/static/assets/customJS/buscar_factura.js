function buscarFacturaAjax() {
    const query = document.getElementById("search_factura").value.trim();
  
    // Si la búsqueda está vacía, recargar la tabla con todas las facturas
    if (query === "") {
      fetch('/lista-de-facturas')
        .then(response => response.text())
        .then(data => {
          const parser = new DOMParser();
          const doc = parser.parseFromString(data, 'text/html');
          const newTableBody = doc.getElementById('tabla_facturas_body').innerHTML;
          document.getElementById('tabla_facturas_body').innerHTML = newTableBody;
        })
        .catch(error => console.error('Error al recargar la tabla:', error));
      return;
    }
  
    // Configurar la solicitud AJAX
    fetch('/buscando-factura', {
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
          document.getElementById('tabla_facturas_body').innerHTML = data.html;
        } else {
          // Si no hay resultados, mostrar el mensaje
          document.getElementById('tabla_facturas_body').innerHTML = data.html;
        }
      })
      .catch(error => {
        console.error('Error:', error);
        alert("Hubo un error al realizar la búsqueda.");
      });
  }
  
  function eliminarFactura(idFactura) {
    if (confirm("¿Estás seguro de que deseas eliminar esta factura?")) {
      fetch(`/eliminar-factura/${idFactura}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
        },
      })
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            // Eliminar la fila de la tabla
            const fila = document.getElementById(`factura_${idFactura}`);
            if (fila) {
              fila.remove();
            }
            alert("Factura eliminada correctamente.");
          } else {
            alert("Error al eliminar la factura.");
          }
        })
        .catch(error => {
          console.error('Error:', error);
          alert("Hubo un error al intentar eliminar la factura.");
        });
    }
  }