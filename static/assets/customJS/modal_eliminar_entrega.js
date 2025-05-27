// Variable para almacenar el ID de la entrega temporalmente (alcance de ventana)
window.idEntregaEliminar = null;

// Función para mostrar el modal de confirmación
function eliminarEntrega(id) {
  // Guarda el ID para usarlo más tarde
  window.idEntregaEliminar = id;

  // Intenta mostrar el modal
  try {
    // Verificar si Bootstrap está disponible
    if (typeof bootstrap === 'undefined') {
      throw new Error("Bootstrap no disponible");
    }

    // Obtener el modal
    const modalElement = document.getElementById('confirmModalEntrega');
    if (!modalElement) {
      throw new Error("Modal no encontrado");
    }

    // Inicializar y mostrar el modal
    const modal = new bootstrap.Modal(modalElement);
    modal.show();

  } catch (error) {
    console.error("Error con modal:", error);
    // Usar confirm como respaldo
    if (confirm("¿Estás seguro de que deseas eliminar esta entrega?")) {
      ejecutarEliminacionEntrega(id);
    }
  }
}

// Función para ejecutar la eliminación
function ejecutarEliminacionEntrega(id) {
  // Redireccionar a la ruta de eliminación
  window.location.href = `/eliminar-entrega/${id}`;
}

// Configurar el botón de confirmación cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function () {
  console.log("Modal eliminar entrega: DOM cargado");

  // Configurar el botón de confirmación
  const confirmBtn = document.getElementById('confirmDeleteEntregaButton');
  if (confirmBtn) {
    confirmBtn.addEventListener('click', function () {
      const id = window.idEntregaEliminar;
      if (id) {
        ejecutarEliminacionEntrega(id);

        // Cerrar el modal
        try {
          const modalElement = document.getElementById('confirmModalEntrega');
          const modal = bootstrap.Modal.getInstance(modalElement);
          if (modal) {
            modal.hide();
          }
        } catch (error) {
          console.error("Error al cerrar modal:", error);
        }
      }
    });
  } else {
    console.error("Botón de confirmación no encontrado");
  }
});