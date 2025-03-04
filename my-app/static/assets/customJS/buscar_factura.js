function eliminarFactura(idFactura) {
    if (confirm("¿Estás seguro de que deseas eliminar esta factura?")) {
        fetch(`/eliminar-factura/${idFactura}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            },
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Error en la solicitud');
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
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

// Función para eliminar una factura
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