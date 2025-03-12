document.addEventListener("DOMContentLoaded", function () {
    const $btnExportarExcel = document.querySelector("#btnExportarExcel"),
          $btnExportarPDF = document.querySelector("#btnExportarPDF"),
          $btnImprimir = document.querySelector("#btnImprimir"),
          $tabla = document.querySelector("#tbl_usuarios"),
          $tablaBody = document.querySelector("#tabla_usuarios_body"),
          $columnaFiltro = document.querySelector("#columna_filtro"),
          $buscarUsuario = document.querySelector("#search_usuarios");

    let datosFiltrados = []; // Almacenará los datos filtrados
    let hayBusqueda = false; // Indica si se ha realizado una búsqueda

    // Función para filtrar la tabla
    function buscarUsuarioAjax() {
        const columnaIndex = parseInt($columnaFiltro.value); // Índice de la columna seleccionada
        const textoBusqueda = $buscarUsuario.value.toLowerCase(); // Texto de búsqueda
        const filas = $tablaBody.querySelectorAll("tr:not(.mensaje-no-resultados)"); // Ignorar el mensaje

        datosFiltrados = []; // Reiniciar los datos filtrados
        let coincidencias = 0; // Contador de coincidencias
        hayBusqueda = textoBusqueda.trim() !== ""; // Actualizar el estado de la búsqueda

        // Eliminar el mensaje anterior si existe
        const mensajeNoResultadosAnterior = $tablaBody.querySelector(".mensaje-no-resultados");
        if (mensajeNoResultadosAnterior) {
            mensajeNoResultadosAnterior.remove();
        }

        // Ocultar todas las filas primero
        filas.forEach((fila) => {
            fila.style.display = "none";
        });

        // Mostrar solo las filas que coincidan con la búsqueda
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
            }
        });

        // Mostrar el mensaje de "No hay resultados" si no hay coincidencias
        if (coincidencias === 0 && hayBusqueda) {
            const filaMensaje = document.createElement("tr");
            filaMensaje.classList.add("mensaje-no-resultados");
            filaMensaje.innerHTML = `
                <td colspan="10" style="text-align:center;color: red;font-weight: bold;">
                    No resultados para la búsqueda: <strong style="color: #222;">${textoBusqueda}</strong>
                </td>
            `;
            $tablaBody.appendChild(filaMensaje);
        }
    }

    // Evento para filtrar la tabla al escribir en el campo de búsqueda
    if ($buscarUsuario) {
        $buscarUsuario.addEventListener("keyup", buscarUsuarioAjax);
    }

    // Evento para filtrar la tabla al cambiar la columna seleccionada
    if ($columnaFiltro) {
        $columnaFiltro.addEventListener("change", buscarUsuarioAjax);
    }

    // 🟢 Exportar a Excel
    if ($btnExportarExcel) {
        $btnExportarExcel.addEventListener("click", function () {
            try {
                const tablaClonada = $tabla.cloneNode(true);
                const tbodyClonado = tablaClonada.querySelector("tbody");

                // Limpiar el tbody clonado
                tbodyClonado.innerHTML = "";

                // Usar datos filtrados si hay búsqueda, de lo contrario usar todas las filas
                const filasAExportar = hayBusqueda ? datosFiltrados : $tablaBody.querySelectorAll("tr:not(.mensaje-no-resultados)");

                filasAExportar.forEach((fila) => {
                    const filaClonada = fila.cloneNode(true); // Clonar la fila
                    // Eliminar las últimas dos columnas (Acción Estado y Acciones)
                    const celdas = filaClonada.querySelectorAll("td");
                    if (celdas.length > 8) { // Verificar que haya más de 8 columnas
                        celdas[celdas.length - 1].remove(); // Eliminar la última celda (Acciones)
                        celdas[celdas.length - 2].remove(); // Eliminar la penúltima celda (Acción Estado)
                    }
                    tbodyClonado.appendChild(filaClonada); // Agregar la fila clonada al tbody
                });

                // Eliminar las últimas dos columnas del encabezado
                const theadClonado = tablaClonada.querySelector("thead");
                const filaEncabezado = theadClonado.querySelector("tr");
                const celdasEncabezado = filaEncabezado.querySelectorAll("th");
                if (celdasEncabezado.length > 8) { // Verificar que haya más de 8 columnas
                    celdasEncabezado[celdasEncabezado.length - 1].remove(); // Eliminar la última celda (Acciones)
                    celdasEncabezado[celdasEncabezado.length - 2].remove(); // Eliminar la penúltima celda (Acción Estado)
                }

                // Exportar el clon de la tabla
                let tableExport = new TableExport(tablaClonada, {
                    exportButtons: false,
                    filename: "Reporte_Usuarios" + (hayBusqueda ? "_Filtrado" : ""),
                    sheetname: "Usuarios",
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

    // 🔴 Exportar a PDF
    if ($btnExportarPDF) {
        $btnExportarPDF.addEventListener("click", function () {
            try {
                const { jsPDF } = window.jspdf;
                const doc = new jsPDF();

                doc.text("Reporte de Usuarios" + (hayBusqueda ? " Filtrado" : ""), 14, 10);

                // Obtener encabezados sin las últimas dos columnas
                const headers = [];
                document.querySelectorAll("#tbl_usuarios thead th").forEach((th, index) => {
                    if (index < 8) { // Evitar las últimas dos columnas (Acción Estado y Acciones)
                        headers.push(th.innerText);
                    }
                });

                // Obtener filas sin las últimas dos columnas
                const data = [];
                const filasAExportar = hayBusqueda ? datosFiltrados : $tablaBody.querySelectorAll("tr:not(.mensaje-no-resultados)");

                filasAExportar.forEach((fila) => {
                    const rowData = [];
                    fila.querySelectorAll("td").forEach((td, index) => {
                        if (index < 8) { // Evitar las últimas dos columnas (Acción Estado y Acciones)
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

                doc.save("Reporte_Usuarios" + (hayBusqueda ? "_Filtrado" : "") + ".pdf");
            } catch (error) {
                console.error("Error al exportar a PDF:", error);
            }
        });
    }

    // 🔵 Imprimir
    if ($btnImprimir) {
        $btnImprimir.addEventListener("click", function () {
            try {
                const tablaHtml = $tabla.cloneNode(true); // Clonar la tabla
                const tbodyClonado = tablaHtml.querySelector("tbody");

                // Limpiar el tbody clonado
                tbodyClonado.innerHTML = "";

                // Usar datos filtrados si hay búsqueda, de lo contrario usar todas las filas
                const filasAImprimir = hayBusqueda ? datosFiltrados : $tablaBody.querySelectorAll("tr:not(.mensaje-no-resultados)");

                filasAImprimir.forEach((fila) => {
                    const filaClonada = fila.cloneNode(true); // Clonar la fila
                    // Eliminar las últimas dos columnas (Acción Estado y Acciones)
                    const celdas = filaClonada.querySelectorAll("td");
                    if (celdas.length > 8) { // Verificar que haya más de 8 columnas
                        celdas[celdas.length - 1].remove(); // Eliminar la última celda (Acciones)
                        celdas[celdas.length - 2].remove(); // Eliminar la penúltima celda (Acción Estado)
                    }
                    tbodyClonado.appendChild(filaClonada); // Agregar la fila clonada al tbody
                });

                // Eliminar las últimas dos columnas del encabezado
                const theadClonado = tablaHtml.querySelector("thead");
                const filaEncabezado = theadClonado.querySelector("tr");
                const celdasEncabezado = filaEncabezado.querySelectorAll("th");
                if (celdasEncabezado.length > 8) { // Verificar que haya más de 8 columnas
                    celdasEncabezado[celdasEncabezado.length - 1].remove(); // Eliminar la última celda (Acciones)
                    celdasEncabezado[celdasEncabezado.length - 2].remove(); // Eliminar la penúltima celda (Acción Estado)
                }

                // Abrir una ventana de impresión
                const ventanaImpresion = window.open("", "", "height=800, width=1000");
                ventanaImpresion.document.write(`
                    <html>
                        <head>
                            <title>Imprimir Reporte de Usuarios${hayBusqueda ? " Filtrado" : ""}</title>
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
                            <h2>Reporte de Usuarios${hayBusqueda ? " Filtrado" : ""}</h2>
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