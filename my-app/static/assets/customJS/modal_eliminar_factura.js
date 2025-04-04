// Variable para almacenar el ID de la factura temporalmente (alcance de ventana)
window.idFacturaEliminar = null;

// Función para mostrar el modal de confirmación
function eliminarFactura(id) {
  // Guarda el ID para usarlo más tarde
  window.idFacturaEliminar = id;

  // Intenta mostrar el modal
  try {
    // Verificar si Bootstrap está disponible
    if (typeof bootstrap === 'undefined') {
      throw new Error("Bootstrap no disponible");
    }

    // Obtener el modal
    const modalElement = document.getElementById('confirmModalFactura');
    if (!modalElement) {
      throw new Error("Modal no encontrado");
    }

    // Inicializar y mostrar el modal
    const modal = new bootstrap.Modal(modalElement);
    modal.show();

  } catch (error) {
    console.error("Error con modal:", error);
    // Usar confirm como respaldo
    if (confirm("¿Estás seguro de que deseas eliminar esta factura?")) {
      ejecutarEliminacionFactura(id);
    }
  }
}

// Función para ejecutar la eliminación
function ejecutarEliminacionFactura(id) {
  // Redireccionar a la ruta de eliminación
  window.location.href = `/eliminar-factura/${id}`;
}

// Configurar el botón de confirmación cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function () {
  console.log("Modal eliminar factura: DOM cargado");

  // Configurar el botón de confirmación
  const confirmBtn = document.getElementById('confirmDeleteFacturaButton');
  if (confirmBtn) {
    confirmBtn.addEventListener('click', function () {
      const id = window.idFacturaEliminar;
      if (id) {
        ejecutarEliminacionFactura(id);

        // Cerrar el modal
        try {
          const modalElement = document.getElementById('confirmModalFactura');
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