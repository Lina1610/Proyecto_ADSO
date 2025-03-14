async function buscarUsuarioAjax() {
  const search = document.getElementById("search_usuario").value;
  const url = "/buscando-usuario";
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

      if (data.success) {
          // Si hay resultados, actualiza la tabla con los datos encontrados
          document.getElementById("tabla_usuarios_body").innerHTML = data.html;
      } else {
          // Si no hay resultados, muestra el mensaje con los estilos personalizados
          document.getElementById("tabla_usuarios_body").innerHTML = `
              <tr>
                  <td colspan="7" style="text-align:center; color: red; font-weight: bold;">
                      No resultados para la búsqueda: 
                      <strong style="color: #222;">${search}</strong>
                  </td>
              </tr>
          `;
      }
  } catch (error) {
      console.error("Error:", error);
  }
}

  
  function eliminarUsuario(id) {
    if (confirm("¿Estás seguro de eliminar este usuario?")) {
      fetch(`/eliminar-usuario/${id}`, {
        method: "GET",
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            // Eliminar la fila de la tabla sin recargar la página
            const fila = document.getElementById(`usuario_${id}`);
            if (fila) {
              fila.remove();
            }
            // Mostrar mensaje de éxito
            mostrarMensaje('Felicitaciones, El Usuario fue eliminado correctamente 😁', 'success');
          } else {
            // Mostrar mensaje de error
            mostrarMensaje('Error al eliminar el usuario', 'error');
          }
        })
        .catch((error) => {
          console.error("Error:", error);
          mostrarMensaje('Error al eliminar el usuario', 'error');
        });
    }
  }
  
  function mostrarMensaje(mensaje, tipo) {
    const contenedorMensajes = document.getElementById('contenedor-mensajes');
    const alerta = document.createElement('div');
    alerta.className = `alert alert-${tipo} alert-dismissible fade show`;
    alerta.role = 'alert';
    alerta.innerHTML = `
      ${mensaje}
      <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    contenedorMensajes.appendChild(alerta);
  
    // Eliminar el mensaje después de 5 segundos
    setTimeout(() => {
      alerta.remove();
    }, 5000);
  }