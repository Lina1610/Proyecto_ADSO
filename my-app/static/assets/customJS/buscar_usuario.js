// Solo mantén esta función para la búsqueda
async function buscarUsuarioAjax() {
  const search = document.getElementById("search_usuario").value;
  const url = "/buscando-usuario";
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
      document.getElementById("tabla_usuarios_body").innerHTML = data.html;
    } else {
      document.getElementById("tabla_usuarios_body").innerHTML = `
          <tr>
              <td colspan="10" style="text-align:center; color: red; font-weight: bold;">
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
