           
function eliminarDireccion(id) {
  if (confirm("¿Estás seguro de que deseas eliminar esta dirección?")) {
      window.location.href = `/eliminar-direccion/${id}`;
  }
}

async function buscarDireccionAjax() {
    const search = document.getElementById("search_direcciones").value;
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
  
        if (data.success) {
            // Si hay resultados, actualiza la tabla con los datos encontrados
            document.getElementById("tabla_direcciones_body").innerHTML = data.html;
        } else {
            // Si no hay resultados, muestra el mensaje con los estilos personalizados
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

  