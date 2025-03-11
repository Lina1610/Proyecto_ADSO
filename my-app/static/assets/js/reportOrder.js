document.addEventListener("DOMContentLoaded", function () {
    const $btnExportarExcel = document.querySelector("#btnExportarExcel"),
          $btnExportarPDF = document.querySelector("#btnExportarPDF"),
          $btnImprimir = document.querySelector("#btnImprimir"),
          $tabla = document.querySelector("#tbl_pedidos");
  
    // Verificar si los elementos existen
    if (!$btnExportarExcel || !$btnExportarPDF || !$btnImprimir || !$tabla) {
      console.error("Error: No se encontraron los elementos necesarios.");
      return;
    }
  
    // 🟢 Exportar a Excel
    $btnExportarExcel.addEventListener("click", function () {
      try {
        // Clonar la tabla para no modificar la original
        const tablaClonada = $tabla.cloneNode(true);
  
        // Eliminar la columna "Acciones" del clon
        tablaClonada.querySelectorAll("tr").forEach((fila) => {
          const celdas = fila.querySelectorAll("td, th");
          if (celdas.length > 7) { // Eliminar la última celda (Acciones)
            celdas[7].remove();
          }
        });
  
        // Exportar el clon de la tabla
        let tableExport = new TableExport(tablaClonada, {
          exportButtons: false,
          filename: "Reporte_Pedidos",
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
  
    // 🔴 Exportar a PDF sin la columna "Acciones"
    $btnExportarPDF.addEventListener("click", function () {
      try {
        const { jsPDF } = window.jspdf;
        const doc = new jsPDF();
  
        doc.text("Reporte de Pedidos", 14, 10);
  
        // Obtener encabezados sin la columna "Acciones"
        const headers = [];
        document
          .querySelectorAll("#tbl_pedidos thead th")
          .forEach((th, index) => {
            if (index < 7) { // Evita la última columna (Acciones)
              headers.push(th.innerText);
            }
          });
  
        // Obtener filas sin la columna "Acciones"
        const data = [];
        document.querySelectorAll("#tbl_pedidos tbody tr").forEach((row) => {
          const rowData = [];
          row.querySelectorAll("td").forEach((td, index) => {
            if (index < 7) { // Evita la última columna (Acciones)
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
  
        doc.save("Reporte_Pedidos.pdf");
      } catch (error) {
        console.error("Error al exportar a PDF:", error);
      }
    });
  
    // 🔵 Imprimir la tabla sin la columna "Acciones"
    $btnImprimir.addEventListener("click", function () {
      try {
        const tablaHtml = document.querySelector("#tbl_pedidos");
        const ventanaImpresion = window.open("", "", "height=800, width=1000");
  
        // Crear un nuevo documento HTML solo con la tabla
        ventanaImpresion.document.write(
          "<html><head><title>Imprimir Reporte de Pedidos</title>"
        );
        ventanaImpresion.document.write("<style>");
        ventanaImpresion.document.write("@media print {");
        ventanaImpresion.document.write(
          "table { width: 100%; border-collapse: collapse; margin: 20px 0; }"
        );
        ventanaImpresion.document.write(
          "th, td { padding: 8px; text-align: left; border: 1px solid #ddd; }"
        );
        ventanaImpresion.document.write(
          "th { background-color: #f4f4f4; font-weight: bold; }"
        );
        ventanaImpresion.document.write(
          "th:nth-child(8), td:nth-child(8) { display: none; }" // Ocultar columna "Acciones"
        );
        ventanaImpresion.document.write(
          "body { font-family: Arial, sans-serif; font-size: 12px; margin: 0; padding: 0; }"
        );
        ventanaImpresion.document.write("@page { margin: 20mm; }");
        ventanaImpresion.document.write("}</style></head>");
        ventanaImpresion.document.write("<body>");
        ventanaImpresion.document.write("<h2>Reporte de Pedidos</h2>");
        ventanaImpresion.document.write(tablaHtml.outerHTML); // Solo incluir la tabla
        ventanaImpresion.document.write("</body></html>");
  
        ventanaImpresion.document.close();
  
        // Enfocar la ventana de impresión y abrir el diálogo de impresión
        ventanaImpresion.focus();
        ventanaImpresion.print();
      } catch (error) {
        console.error("Error al imprimir:", error);
      }
    });
  });