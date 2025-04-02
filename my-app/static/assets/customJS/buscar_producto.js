async function buscarProductoAjax() {
  const search = document.getElementById("search_producto").value.trim();
  console.log("Término de búsqueda:", search);

  // Si el campo de búsqueda está vacío, mostrar todos los registros sin recargar
  if (search === "") {
      try {
          const response = await fetch('/lista-de-productos');
          const data = await response.text();

          // Parsear el HTML de la respuesta
          const parser = new DOMParser();
          const doc = parser.parseFromString(data, 'text/html');

          // Extraer el contenido de la tabla
          const newTableBody = doc.getElementById('tabla_productos_body').innerHTML;

          // Actualizar la tabla en la página actual
          document.getElementById('tabla_productos_body').innerHTML = newTableBody;

          // Actualizar el mensaje de registros
          actualizarMensajeRegistros();
      } catch (error) {
          console.error('Error al cargar todos los productos:', error);
      }
      return; // Salir de la función
  }

  // Si hay un término de búsqueda, realizar la búsqueda
  const url = "/buscando-producto";
  const dataPeticion = { busqueda: search };

  try {
      const response = await fetch(url, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(dataPeticion),
      });

      if (!response.ok) {
          throw new Error("Error en la búsqueda");
      }

      const data = await response.json();
      console.log("Respuesta del servidor:", data);

      const tablaBody = document.getElementById("tabla_productos_body");

      if (data.success) {
          tablaBody.innerHTML = data.html;
      } else {
          tablaBody.innerHTML = `
              <tr>
                  <td colspan="9" style="text-align:center; color: red; font-weight: bold;">
                      No resultados para la búsqueda: 
                      <strong style="color: #222;">${search}</strong>
                  </td>
              </tr>
          `;
      }

      // Actualizar el mensaje de registros
      actualizarMensajeRegistros();
  } catch (error) {
      console.error("Error:", error);
  }
}

// Función para actualizar el mensaje de registros
function actualizarMensajeRegistros() {
  const filasVisibles = document.querySelectorAll("#tabla_productos_body tr.fila-datos:not([style*='display: none'])").length;
  const filasTotales = document.querySelectorAll("#tabla_productos_body tr.fila-datos").length;

  document.getElementById("filas-mostradas").textContent = filasVisibles;
  document.getElementById("filas-totales").textContent = filasTotales;
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