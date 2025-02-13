document.addEventListener("DOMContentLoaded", function () {
    const $btnExportarExcel = document.querySelector("#btnExportarExcel"),
          $btnExportarPDF = document.querySelector("#btnExportarPDF"),
          $btnImprimir = document.querySelector("#btnImprimir"),
          $tabla = document.querySelector("#tbl_empleados");
          

    // 🟢 Exportar a Excel
    $btnExportarExcel.addEventListener("click", function () {
        let tableExport = new TableExport($tabla, {
            exportButtons: false,
            filename: "Reporte_Empleados",
            sheetname: "Empleados",
        });

        let datos = tableExport.getExportData();
        let preferenciasDocumento = datos.tbl_empleados.xlsx;
        
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

    // 🔴 Exportar a PDF
  // Exportar a PDF
$btnExportarPDF.addEventListener("click", function () {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();
    
    doc.text("Reporte de Empleados", 14, 10);

    // Primero obtenemos los datos de la tabla y excluimos la última columna (columna de "Acción")
    const rows = [];
    const trs = $tabla.querySelectorAll('tbody tr');
    trs.forEach(tr => {
        const tds = tr.querySelectorAll('td');
        const row = [];
        // Excluimos la última columna (índice 5)
        for (let i = 0; i < tds.length - 1; i++) {
            row.push(tds[i].innerText.trim());
        }
        rows.push(row);
    });

    // Usamos autoTable para crear la tabla en el PDF, sin la columna de "Acción"
    doc.autoTable({
        head: [
            ['#', 'Nombre', 'Apellido', 'Sexo', 'Salario'] // Omitimos "Acción" aquí
        ],
        body: rows,
        startY: 20
    });

    doc.save("Reporte_Empleados.pdf");
});


    // 🔵 Imprimir la tabla
    $btnImprimir.addEventListener("click", function () {
        const tablaHtml = document.querySelector("#tbl_empleados");
        const ventanaImpresion = window.open('', '', 'height=800, width=1000');
        
        ventanaImpresion.document.write('<html><head><title>Imprimir Reporte</title>');
        ventanaImpresion.document.write('<style>');
        ventanaImpresion.document.write('@media print {');
        ventanaImpresion.document.write('table { width: 100%; border-collapse: collapse; margin: 20px 0; }');
        ventanaImpresion.document.write('th, td { padding: 8px; text-align: left; border: 1px solid #ddd; }');
        ventanaImpresion.document.write('th { background-color: #f4f4f4; font-weight: bold; }');
        ventanaImpresion.document.write('th:nth-child(6), td:nth-child(6) { display: none; }');
        ventanaImpresion.document.write('body { font-family: Arial, sans-serif; font-size: 12px; }');
        ventanaImpresion.document.write('@page { margin: 20mm; }');
        ventanaImpresion.document.write('}</style></head>');
        ventanaImpresion.document.write('<body>');
        ventanaImpresion.document.write('<h2>Reporte de Empleados</h2>');
        ventanaImpresion.document.write(tablaHtml.outerHTML);
        ventanaImpresion.document.write('</body></html>');
        
        ventanaImpresion.document.close();
        ventanaImpresion.print();
    });
});
