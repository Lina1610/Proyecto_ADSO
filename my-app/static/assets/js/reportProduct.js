document.addEventListener("DOMContentLoaded", function () {
  const $btnExportarExcel = document.querySelector("#btnExportarExcel"),
        $btnExportarPDF = document.querySelector("#btnExportarPDF"),
        $btnImprimir = document.querySelector("#btnImprimir"),
        $tabla = document.querySelector("#tbl_productos");

  // 🟢 Exportar a Excel
  $btnExportarExcel.addEventListener("click", function () {
    // Clonar la tabla para no modificar la original
    const tablaClonada = $tabla.cloneNode(true);

    // Eliminar la columna "Acción" del clon
    tablaClonada.querySelectorAll("tr").forEach((fila) => {
      const celdas = fila.querySelectorAll("td, th");
      if (celdas.length > 6) { // Eliminar la última celda (Acción)
        celdas[6].remove();
      }
    });

    // Asignar un ID único al clon para evitar conflictos
    tablaClonada.id = "tbl_productos_clonada";

    // Agregar el clon al DOM temporalmente
    document.body.appendChild(tablaClonada);

    // Exportar el clon de la tabla
    let tableExport = new TableExport(tablaClonada, {
      formats: ["xlsx"], // Solo exportar a Excel
      exportButtons: false,
      filename: "Reporte_Productos",
      sheetname: "Productos",
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

    // Eliminar el clon del DOM después de exportar
    document.body.removeChild(tablaClonada);
  });

  // 🔴 Exportar a PDF sin la columna "Acción"
  $btnExportarPDF.addEventListener("click", function () {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();

    doc.text("Reporte de Productos", 14, 10);

    // Obtener encabezados sin la columna "Acción"
    const headers = [];
    document
      .querySelectorAll("#tbl_productos thead th")
      .forEach((th, index) => {
        if (index < 6) { // Evita la última columna (Acción)
          headers.push(th.innerText);
        }
      });

    // Obtener filas sin la columna "Acción"
    const data = [];
    document.querySelectorAll("#tbl_productos tbody tr").forEach((row) => {
      const rowData = [];
      row.querySelectorAll("td").forEach((td, index) => {
        if (index < 6) { // Evita la última columna (Acción)
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

    doc.save("Reporte_Productos.pdf");
  });

  // 🔵 Imprimir la tabla sin la columna "Acción"
  $btnImprimir.addEventListener("click", function () {
    const tablaHtml = document.querySelector("#tbl_productos");
    const ventanaImpresion = window.open("", "", "height=800, width=1000");

    ventanaImpresion.document.write(
      "<html><head><title>Imprimir Reporte</title>"
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
      "th:nth-child(7), td:nth-child(7) { display: none; }" // Ocultar columna "Acción"
    );
    ventanaImpresion.document.write(
      "body { font-family: Arial, sans-serif; font-size: 12px; }"
    );
    ventanaImpresion.document.write("@page { margin: 20mm; }");
    ventanaImpresion.document.write("}</style></head>");
    ventanaImpresion.document.write("<body>");
    ventanaImpresion.document.write("<h2>Reporte de Productos</h2>");
    ventanaImpresion.document.write(tablaHtml.outerHTML);
    ventanaImpresion.document.write("</body></html>");

    ventanaImpresion.document.close();
    ventanaImpresion.print();
  });
});