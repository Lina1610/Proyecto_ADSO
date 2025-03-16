// Variable para almacenar el ID del pedido temporalmente (alcance de ventana)
window.idPedidoEliminar = null;

// Función para mostrar el modal de confirmación
function eliminarPedido(idPedido) {
  // Guarda el ID para usarlo más tarde
  window.idPedidoEliminar = idPedido;

  // Intenta mostrar el modal
  try {
    // Verificar si Bootstrap está disponible
    if (typeof bootstrap === 'undefined') {
      throw new Error("Bootstrap no disponible");
    }

    // Obtener el modal
    const modalElement = document.getElementById('confirmModalPedido');
    if (!modalElement) {
      throw new Error("Modal no encontrado");
    }

    // Inicializar y mostrar el modal
    const modal = new bootstrap.Modal(modalElement);
    modal.show();

  } catch (error) {
    console.error("Error con modal:", error);
    // Usar confirm como respaldo
    if (confirm("¿Estás seguro de que deseas eliminar este pedido?")) {
      ejecutarEliminacionPedido(idPedido);
    }
  }
}

// Función para ejecutar la eliminación
function ejecutarEliminacionPedido(idPedido) {
  // Redireccionar a la ruta de eliminación
  window.location.href = `/eliminar-pedido/${idPedido}`;
}

// Configurar el botón de confirmación cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function () {
  console.log("Modal eliminar pedido: DOM cargado");

  // Configurar el botón de confirmación
  const confirmBtn = document.getElementById('confirmDeletePedidoButton');
  if (confirmBtn) {
    confirmBtn.addEventListener('click', function () {
      const idPedido = window.idPedidoEliminar;
      if (idPedido) {
        ejecutarEliminacionPedido(idPedido);

        // Cerrar el modal
        try {
          const modalElement = document.getElementById('confirmModalPedido');
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