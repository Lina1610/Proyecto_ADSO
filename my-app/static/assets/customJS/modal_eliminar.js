// Variable para almacenar el ID temporalmente (alcance de ventana)
window.idUsuarioEliminar = null;

// Función para mostrar el modal de confirmación
function eliminarUsuario(id) {
  // Guarda el ID para usarlo más tarde
  window.idUsuarioEliminar = id;

  // Intenta mostrar el modal
  try {
    // Verificar si Bootstrap está disponible
    if (typeof bootstrap === 'undefined') {
      throw new Error("Bootstrap no disponible");
    }

    // Obtener el modal
    const modalElement = document.getElementById('confirmModal');
    if (!modalElement) {
      throw new Error("Modal no encontrado");
    }

    // Inicializar y mostrar el modal
    const modal = new bootstrap.Modal(modalElement);
    modal.show();

  } catch (error) {
    console.error("Error con modal:", error);
    // Usar confirm como respaldo
    if (confirm("¿Estás seguro de que deseas eliminar este usuario?")) {
      ejecutarEliminacion(id);
    }
  }
}

// Función para ejecutar la eliminación
function ejecutarEliminacion(id) {
    fetch(`/eliminar-usuario/${id}`, {
      method: "GET"
    })
      .then(response => response.json())
      .then(data => {
        console.log("Respuesta del backend:", data);  // Más depuración
        
        // Log para ver si entra a la condición de éxito
        if (data.success === true) {  // Comprobación explícita
          console.log("Éxito - Eliminando fila y recargando");
          // Eliminar fila
          const fila = document.getElementById(`usuario_${id}`);
          if (fila) {
            fila.remove();
          }
          // Recargar la página para mostrar el mensaje de Flask
          window.location.reload();
        } else {
          console.log("Error - Recargando página");
          // Recargar la página para mostrar el mensaje de Flask
          window.location.reload();
        }
      })
      .catch(error => {
        console.error("Error:", error);
        // Recargar la página para mostrar el mensaje de Flask
        window.location.reload();
      });
}


/// Configurar el botón de confirmación
document.addEventListener('DOMContentLoaded', function () {
    const confirmBtn = document.getElementById('confirmDeleteButton');
    if (confirmBtn) {
      confirmBtn.addEventListener('click', function () {
        const id = window.idUsuarioEliminar;
        if (id) {
          // Redireccionar directamente
          window.location.href = `/eliminar-usuario/${id}`;
        }
      });
    }
  });