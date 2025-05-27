// Variable para almacenar el ID temporalmente (alcance de ventana)
window.idProductoEliminar = null;

// Función para mostrar el modal de confirmación
function eliminarProducto(id) {
  // Guarda el ID para usarlo más tarde
  window.idProductoEliminar = id;

  // Intenta mostrar el modal
  try {
    // Verificar si Bootstrap está disponible
    if (typeof bootstrap === 'undefined') {
      throw new Error("Bootstrap no disponible");
    }

    // Obtener el modal
    const modalElement = document.getElementById('confirmModalProducto');
    if (!modalElement) {
      throw new Error("Modal no encontrado");
    }

    // Inicializar y mostrar el modal
    const modal = new bootstrap.Modal(modalElement);
    modal.show();

  } catch (error) {
    console.error("Error con modal:", error);
    // Usar confirm como respaldo
    if (confirm("¿Estás seguro de que deseas eliminar este producto?")) {
      ejecutarEliminacionProducto(id);
    }
  }
}

// Función para ejecutar la eliminación
function ejecutarEliminacionProducto(id) {
  // Redireccionar a la ruta de eliminación
  window.location.href = `/eliminar-producto/${id}`;
}

// Configurar el botón de confirmación cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function () {
  console.log("Modal eliminar producto: DOM cargado");

  // Configurar el botón de confirmación
  const confirmBtn = document.getElementById('confirmDeleteProductoButton');
  if (confirmBtn) {
    confirmBtn.addEventListener('click', function () {
      const id = window.idProductoEliminar;
      if (id) {
        ejecutarEliminacionProducto(id);
      }
    });
  } else {
    console.error("Botón de confirmación no encontrado");
  }
});

// Configurar el botón de confirmación cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function () {
  console.log("Modal eliminar producto: DOM cargado");

  // Configurar el botón de confirmación
  const confirmBtn = document.getElementById('confirmDeleteProductoButton');
  if (confirmBtn) {
    confirmBtn.addEventListener('click', function () {
      const idProducto = window.idProductoEliminar;
      if (idProducto) {
        ejecutarEliminacionProducto(idProducto);

        // Cerrar el modal
        try {
          const modalElement = document.getElementById('confirmModalProducto');
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