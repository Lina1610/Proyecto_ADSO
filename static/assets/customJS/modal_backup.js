// Variable para almacenar el nombre del backup temporalmente (alcance de ventana)
window.nombreBackupAccion = null;
window.accionBackup = null;

// Función para mostrar el modal de confirmación para restaurar
function restaurarBackup(nombre) {
  window.nombreBackupAccion = nombre;
  window.accionBackup = 'restaurar';

  try {
    if (typeof bootstrap === 'undefined') {
      throw new Error("Bootstrap no disponible");
    }

    const modalElement = document.getElementById('confirmModalBackup');
    if (!modalElement) {
      throw new Error("Modal no encontrado");
    }

    // Actualizar título y mensaje
    document.getElementById('confirmModalBackupTitle').textContent = 'Confirmar restauración';
    document.getElementById('confirmModalBackupMessage').innerHTML = 
      `¿Estás seguro de que deseas restaurar el backup <strong>${nombre}</strong>? Esto sobrescribirá todos los datos actuales.`;
    document.getElementById('confirmActionBackupButton').className = 'btn btn-warning'; // Color acorde a restaurar

    const modal = new bootstrap.Modal(modalElement);
    modal.show();
  } catch (error) {
    console.error("Error con modal:", error);
    if (confirm(`¿Estás seguro de que deseas restaurar el backup ${nombre}? Esto sobrescribirá todos los datos actuales.`)) {
      ejecutarAccionBackup(nombre, 'restaurar');
    }
  }
}

// Función para mostrar el modal de confirmación para eliminar
function eliminarBackup(nombre) {
  window.nombreBackupAccion = nombre;
  window.accionBackup = 'eliminar';

  try {
    if (typeof bootstrap === 'undefined') {
      throw new Error("Bootstrap no disponible");
    }

    const modalElement = document.getElementById('confirmModalBackup');
    if (!modalElement) {
      throw new Error("Modal no encontrado");
    }

    // Actualizar título y mensaje
    document.getElementById('confirmModalBackupTitle').textContent = 'Confirmar eliminación';
    document.getElementById('confirmModalBackupMessage').innerHTML = 
      `¿Estás seguro de que deseas eliminar el backup <strong>${nombre}</strong>?`;
    document.getElementById('confirmActionBackupButton').className = 'btn btn-danger'; // Color acorde a eliminar

    const modal = new bootstrap.Modal(modalElement);
    modal.show();
  } catch (error) {
    console.error("Error con modal:", error);
    if (confirm(`¿Estás seguro de que deseas eliminar el backup ${nombre}?`)) {
      ejecutarAccionBackup(nombre, 'eliminar');
    }
  }
}

// Función para ejecutar la acción (restaurar o eliminar)
function ejecutarAccionBackup(nombre, accion) {
  if (accion === 'restaurar') {
    window.location.href = `/restaurar_backup/${nombre}`;
  } else if (accion === 'eliminar') {
    window.location.href = `/eliminar_backup/${nombre}`;
  }
  // Limpiar las variables para evitar repeticiones
  window.nombreBackupAccion = null;
  window.accionBackup = null;
}

// Configurar el botón de confirmación cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function () {
  console.log("Modal backup: DOM cargado");

  const confirmBtn = document.getElementById('confirmActionBackupButton');
  if (confirmBtn) {
    // Remover cualquier evento previo para evitar duplicados
    confirmBtn.removeEventListener('click', handleConfirmAction);
    confirmBtn.addEventListener('click', handleConfirmAction);
  } else {
    console.error("Botón de confirmación no encontrado");
  }
});

// Función para manejar el evento de confirmación
function handleConfirmAction() {
  const nombre = window.nombreBackupAccion;
  const accion = window.accionBackup;
  if (nombre && accion) {
    ejecutarAccionBackup(nombre, accion);

    // Cerrar el modal
    try {
      const modalElement = document.getElementById('confirmModalBackup');
      const modal = bootstrap.Modal.getInstance(modalElement);
      if (modal) {
        modal.hide();
      }
    } catch (error) {
      console.error("Error al cerrar modal:", error);
    }
  }
}