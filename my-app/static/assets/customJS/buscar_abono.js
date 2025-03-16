function buscarAbonoAjax() {
    const query = document.getElementById("search_abono").value.trim();  // Asegúrate de que el ID sea "search_abono"
  
    // Si la búsqueda está vacía, recargar la tabla con todos los abonos
    if (query === "") {
        fetch('/lista-de-abonos')
            .then(response => response.text())
            .then(data => {
                const parser = new DOMParser();
                const doc = parser.parseFromString(data, 'text/html');
                const newTableBody = doc.getElementById('tabla_abonos_body').innerHTML;
                document.getElementById('tabla_abonos_body').innerHTML = newTableBody;
            })
            .catch(error => console.error('Error al recargar la tabla:', error));
        return;
    }

    // Configurar la solicitud AJAX
    fetch('/buscando-abono', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ busqueda: query }),
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Si hay resultados, actualizar la tabla
                document.getElementById('tabla_abonos_body').innerHTML = data.html;
            } else {
                // Si no hay resultados, mostrar el mensaje
                document.getElementById('tabla_abonos_body').innerHTML = data.html;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert("Hubo un error al realizar la búsqueda.");
        });
}
