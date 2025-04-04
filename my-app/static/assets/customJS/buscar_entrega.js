async function buscarEntregaAjax() {
    const search = document.getElementById("search_entrega").value.trim();
    console.log("Término de búsqueda:", search);

    // Si el campo de búsqueda está vacío, mostrar todos los registros sin recargar
    if (search === "") {
        try {
            const response = await fetch('/lista-de-entregas');
            const data = await response.text();

            // Parsear el HTML de la respuesta
            const parser = new DOMParser();
            const doc = parser.parseFromString(data, 'text/html');

            // Extraer el contenido de la tabla
            const newTableBody = doc.getElementById('tabla_entregas_body').innerHTML;

            // Actualizar la tabla en la página actual
            document.getElementById('tabla_entregas_body').innerHTML = newTableBody;
        } catch (error) {
            console.error('Error al cargar todas las entregas:', error);
        }
        return; // Salir de la función
    }

    // Si hay un término de búsqueda, realizar la búsqueda
    const url = "/buscando-entrega";
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
        console.log("Respuesta del servidor:", data);

        const tablaBody = document.getElementById("tabla_entregas_body");

        if (data.success) {
            tablaBody.innerHTML = data.html;
        } else {
            tablaBody.innerHTML = `
                <tr>
                    <td colspan="8" style="text-align:center; color: red; font-weight: bold;">
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
