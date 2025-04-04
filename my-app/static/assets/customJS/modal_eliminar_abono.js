// Variable para almacenar el ID del abono temporalmente (alcance de ventana)
window.idAbonoEliminar = null;

// Función para mostrar el modal de confirmación
function eliminarAbono(id) {
  // Guarda el ID para usarlo más tarde
  window.idAbonoEliminar = id;

  // Intenta mostrar el modal
  try {
    // Verificar si Bootstrap está disponible
    if (typeof bootstrap === 'undefined') {
      throw new Error("Bootstrap no disponible");
    }

    // Obtener el modal
    const modalElement = document.getElementById('confirmModalAbono');
    if (!modalElement) {
      throw new Error("Modal no encontrado");
    }

    // Inicializar y mostrar el modal
    const modal = new bootstrap.Modal(modalElement);
    modal.show();

  } catch (error) {
    console.error("Error con modal:", error);
    // Usar confirm como respaldo
    if (confirm("¿Estás seguro de que deseas eliminar este abono?")) {
      ejecutarEliminacionAbono(id);
    }
  }
}

// Función para ejecutar la eliminación
function ejecutarEliminacionAbono(id) {
  // Redireccionar a la ruta de eliminación
  window.location.href = `/eliminar-abono/${id}`;
}

// Configurar el botón de confirmación cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function () {
  console.log("Modal eliminar abono: DOM cargado");

  // Configurar el botón de confirmación
  const confirmBtn = document.getElementById('confirmDeleteAbonoButton');
  if (confirmBtn) {
    confirmBtn.addEventListener('click', function () {
      const id = window.idAbonoEliminar;
      if (id) {
        ejecutarEliminacionAbono(id);

        // Cerrar el modal
        try {
          const modalElement = document.getElementById('confirmModalAbono');
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