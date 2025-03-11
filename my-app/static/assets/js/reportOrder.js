document.addEventListener("DOMContentLoaded", function () {
  const $btnExportarExcel = document.querySelector("#btnExportarExcel"),
        $btnExportarPDF = document.querySelector("#btnExportarPDF"),
        $btnImprimir = document.querySelector("#btnImprimir"),
        $tabla = document.querySelector("#tbl_pedidos"),
        $tablaBody = document.querySelector("#tabla_pedidos_body"),
        $columnaFiltro = document.querySelector("#columna_filtro"),
        $buscarPedido = document.querySelector("#search_pedidos"),
        $mensajeNoResultados = document.querySelector("#mensaje-no-resultados");

  let datosFiltrados = []; // Almacenará los datos filtrados

  // Función para filtrar la tabla
  function buscarPedidoAjax() {
      const columnaIndex = parseInt($columnaFiltro.value); // Índice de la columna seleccionada
      const textoBusqueda = $buscarPedido.value.toLowerCase(); // Texto de búsqueda
      const filas = $tablaBody.querySelectorAll("tr");

      datosFiltrados = []; // Reiniciar los datos filtrados
      let coincidencias = 0; // Contador de coincidencias

      filas.forEach((fila) => {
          const celdas = fila.querySelectorAll("td");
          let coincide = false;

          // Verificar solo la columna seleccionada
          if (celdas[columnaIndex].textContent.toLowerCase().includes(textoBusqueda)) {
              coincide = true;
          }

          if (coincide) {
              fila.style.display = ""; // Mostrar fila
              datosFiltrados.push(fila); // Agregar fila a los datos filtrados
              coincidencias++;
          } else {
              fila.style.display = "none"; // Ocultar fila
          }
      });

      // Mostrar u ocultar el mensaje de "No hay resultados"
      if ($mensajeNoResultados) {
          if (coincidencias === 0) {
              $mensajeNoResultados.classList.remove("d-none");
          } else {
              $mensajeNoResultados.classList.add("d-none");
          }
      }
  }

  // Evento para filtrar la tabla al escribir en el campo de búsqueda
  if ($buscarPedido) {
      $buscarPedido.addEventListener("keyup", buscarPedidoAjax);
  }

  // Evento para filtrar la tabla al cambiar la columna seleccionada
  if ($columnaFiltro) {
      $columnaFiltro.addEventListener("change", buscarPedidoAjax);
  }

  // 🟢 Exportar a Excel (solo datos filtrados)
  if ($btnExportarExcel) {
      $btnExportarExcel.addEventListener("click", function () {
          try {
              const tablaClonada = $tabla.cloneNode(true);
              const tbodyClonado = tablaClonada.querySelector("tbody");

              // Limpiar el tbody clonado y agregar solo las filas filtradas
              tbodyClonado.innerHTML = "";
              datosFiltrados.forEach((fila) => {
                  tbodyClonado.appendChild(fila.cloneNode(true));
              });

              // Eliminar la columna "Acciones" si existe
              tablaClonada.querySelectorAll("tr").forEach((fila) => {
                  const celdas = fila.querySelectorAll("td, th");
                  if (celdas.length > 7) { // Eliminar la última celda (Acciones)
                      celdas[7].remove();
                  }
              });

              // Exportar el clon de la tabla
              let tableExport = new TableExport(tablaClonada, {
                  exportButtons: false,
                  filename: "Reporte_Pedidos_Filtrado",
                  sheetname: "Pedidos",
              });

              let datos = tableExport.getExportData();
              let preferenciasDocumento = datos[tablaClonada.id].xlsx;

              tableExport.export2file(
                  preferenciasDocumento.data,
                  preferenciasDocumento.mimeType,
                  preferenciasDocumento.filename,
                  preferenciasDocumento.fileExtension,
                  preferenciasDocumento.merges,
                  preferenciasDocumento.RTL,
                  preferenciasDocumento.sheetname
              );
          } catch (error) {
              console.error("Error al exportar a Excel:", error);
          }
      });
  }

  // 🔴 Exportar a PDF (solo datos filtrados)
  if ($btnExportarPDF) {
      $btnExportarPDF.addEventListener("click", function () {
          try {
              const { jsPDF } = window.jspdf;
              const doc = new jsPDF();

              doc.text("Reporte de Pedidos Filtrado", 14, 10);

              // Obtener encabezados
              const headers = [];
              document.querySelectorAll("#tbl_pedidos thead th").forEach((th, index) => {
                  if (index < 7) { // Evitar la columna "Acciones"
                      headers.push(th.innerText);
                  }
              });

              // Obtener filas filtradas
              const data = [];
              datosFiltrados.forEach((fila) => {
                  const rowData = [];
                  fila.querySelectorAll("td").forEach((td, index) => {
                      if (index < 7) { // Evitar la columna "Acciones"
                          rowData.push(td.innerText);
                      }
                  });
                  data.push(rowData);
              });

              // Generar tabla en el PDF
              doc.autoTable({
                  head: [headers],
                  body: data,
                  startY: 20,
                  theme: "striped",
                  styles: { fontSize: 10, cellPadding: 3 },
                  headStyles: { fillColor: [44, 62, 80], textColor: [255, 255, 255] },
                  alternateRowStyles: { fillColor: [240, 240, 240] },
              });

              doc.save("Reporte_Pedidos_Filtrado.pdf");
          } catch (error) {
              console.error("Error al exportar a PDF:", error);
          }
      });
  }

  // 🔵 Imprimir (solo datos filtrados)
  if ($btnImprimir) {
      $btnImprimir.addEventListener("click", function () {
          try {
              const tablaHtml = $tabla.cloneNode(true);
              const tbodyClonado = tablaHtml.querySelector("tbody");

              // Limpiar el tbody clonado y agregar solo las filas filtradas
              tbodyClonado.innerHTML = "";
              datosFiltrados.forEach((fila) => {
                  tbodyClonado.appendChild(fila.cloneNode(true));
              });

              const ventanaImpresion = window.open("", "", "height=800, width=1000");
              ventanaImpresion.document.write(`
                  <html>
                      <head>
                          <title>Imprimir Reporte de Pedidos Filtrado</title>
                          <style>
                              @media print {
                                  table { width: 100%; border-collapse: collapse; margin: 20px 0; }
                                  th, td { padding: 8px; text-align: left; border: 1px solid #ddd; }
                                  th { background-color: #f4f4f4; font-weight: bold; }
                                  body { font-family: Arial, sans-serif; font-size: 12px; margin: 0; padding: 0; }
                                  @page { margin: 20mm; }
                              }
                          </style>
                      </head>
                      <body>
                          <h2>Reporte de Pedidos Filtrado</h2>
                          ${tablaHtml.outerHTML}
                      </body>
                  </html>
              `);
              ventanaImpresion.document.close();
              ventanaImpresion.focus();
              ventanaImpresion.print();
          } catch (error) {
              console.error("Error al imprimir:", error);
          }
      });
  }
});