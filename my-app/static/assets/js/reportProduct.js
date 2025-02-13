document.addEventListener("DOMContentLoaded", function () {
    const $btnExportarExcel = document.querySelector("#btnExportarExcel"),
          $btnExportarPDF = document.querySelector("#btnExportarPDF"),
          $btnImprimir = document.querySelector("#btnImprimir"),
          $tabla = document.querySelector("#tbl_productos");

    // 🟢 Exportar a Excel
    $btnExportarExcel.addEventListener("click", function () {
        let tableExport = new TableExport($tabla, {
            exportButtons: false,
            filename: "Reporte_Productos",
            sheetname: "Productos",
        });

        let datos = tableExport.getExportData();
        let preferenciasDocumento = datos.tbl_productos.xlsx;
        
        tableExport.export2file(
            preferenciasDocumento.data,
            preferenciasDocumento.mimeType,
            preferenciasDocumento.filename,
            preferenciasDocumento.fileExtension,
            preferenciasDocumento.merges,
            preferenciasDocumento.RTL,
            preferenciasDocumento.sheetname
        );
    });

    // 🔴 Exportar a PDF sin la columna "Acción"
$btnExportarPDF.addEventListener("click", function () {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();

    doc.text("Reporte de Productos", 14, 10);

    // Obtener encabezados sin la columna "Acción"
    const headers = [];
    document.querySelectorAll("#tbl_productos thead th").forEach((th, index) => {
        if (index < 9) { // Evita la última columna (Acción)
            headers.push(th.innerText);
        }
    });

    // Obtener filas sin la columna "Acción"
    const data = [];
    document.querySelectorAll("#tbl_productos tbody tr").forEach(row => {
        const rowData = [];
        row.querySelectorAll("td").forEach((td, index) => {
            if (index < 9) { // Evita la última columna (Acción)
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
        alternateRowStyles: { fillColor: [240, 240, 240] }
    });

    doc.save("Reporte_Productos.pdf");
})})

// 🔵 Imprimir la tabla sin la columna "Acción"
