           
async function buscarDireccionAjax() {
    const search = document.getElementById("search_direccion").value.trim();
    console.log("Término de búsqueda:", search);  // 🛠️ Depuración

    const url = "/buscando-direccion";
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
        console.log("Respuesta del servidor:", data);  // 🛠️ Depuración

        if (data.success) {
            document.getElementById("tabla_direcciones_body").innerHTML = data.html;
        } else {
            // Si no hay resultados, mostrar un mensaje
            document.getElementById("tabla_direcciones_body").innerHTML = `
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