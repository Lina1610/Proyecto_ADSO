document.addEventListener("DOMContentLoaded", function () {
    // Elementos DOM
    const $btnExportarExcel = document.querySelector("#btnExportarExcel"),
          $btnExportarPDF = document.querySelector("#btnExportarPDF"),
          $btnImprimir = document.querySelector("#btnImprimir"),
          $tabla = document.querySelector("#tbl_entregas"),
          $tablaBody = document.querySelector("#tabla_entregas_body"),
          $toggleFiltros = document.querySelector("#toggleFiltros"),
          $panelFiltros = document.querySelector("#panelFiltros"),
          $limpiarFiltros = document.querySelector("#limpiarFiltros"),
          $numFilas = document.querySelector("#num_filas"),
          $filtrosCampos = document.querySelectorAll(".filtro-campo"),
          $filasMostradas = document.querySelector("#filas-mostradas"),
          $filasTotales = document.querySelector("#filas-totales");

    let filasFiltradas = []; // Almacenará las filas filtradas
    let hayFiltrosActivos = false; // Indica si hay filtros activos
    let filasTotales = document.querySelectorAll(".fila-datos").length;
    
    // Actualizar contador de filas totales
    $filasTotales.textContent = filasTotales;

    // Inicializar mostrando todas las filas disponibles
    actualizarFilasMostradas();

    // Función para mostrar/ocultar panel de filtros
    if ($toggleFiltros) {
        $toggleFiltros.addEventListener("click", function() {
            $panelFiltros.style.display = $panelFiltros.style.display === "none" ? "block" : "none";
        });
    }

    // Función para limpiar todos los filtros
    if ($limpiarFiltros) {
        $limpiarFiltros.addEventListener("click", function() {
            $filtrosCampos.forEach(filtro => {
                if (filtro.tagName === 'SELECT') {
                    filtro.selectedIndex = 0;
                } else {
                    filtro.value = '';
                }
            });
            
            // Restablecer la visualización de todas las filas
            const filas = $tablaBody.querySelectorAll("tr.fila-datos");
            filas.forEach(fila => {
                fila.style.display = "";
            });
            
            // Eliminar mensaje de "No hay resultados" si existe
            const mensajeNoResultados = $tablaBody.querySelector(".mensaje-no-resultados");
            if (mensajeNoResultados) {
                mensajeNoResultados.remove();
            }
            
            hayFiltrosActivos = false;
            filasFiltradas = [];
            aplicarPaginacion();
            actualizarFilasMostradas();
        });
    }

    // Función para aplicar filtros a la tabla
    function aplicarFiltros() {
        // Obtener valores de todos los filtros
        const filtros = {};
        $filtrosCampos.forEach(filtro => {
            const campo = parseInt(filtro.dataset.campo);
            const valor = filtro.value.toLowerCase();
            if (valor) {
                filtros[campo] = valor;
            }
        });

        // Verificar si hay filtros activos
        hayFiltrosActivos = Object.keys(filtros).length > 0;

        // Eliminar mensaje anterior si existe
        const mensajeNoResultadosAnterior = $tablaBody.querySelector(".mensaje-no-resultados");
        if (mensajeNoResultadosAnterior) {
            mensajeNoResultadosAnterior.remove();
        }

        // Obtener todas las filas de datos
        const filas = $tablaBody.querySelectorAll("tr.fila-datos");
        filasFiltradas = [];
        let coincidencias = 0;

        // Ocultar todas las filas primero
        filas.forEach(fila => {
            fila.style.display = "none";
        });

        // Aplicar filtros
        filas.forEach(fila => {
            const celdas = fila.querySelectorAll("td");
            let coincideTodos = true;

            // Verificar cada filtro activo
            for (const campo in filtros) {
                const valorFiltro = filtros[campo];
                let valorCelda = celdas[campo].textContent.toLowerCase();
                
                // Comprobar si la celda contiene el valor del filtro
                if (!valorCelda.includes(valorFiltro)) {
                    coincideTodos = false;
                    break;
                }
            }

            // Si coincide con todos los filtros activos, mostrar la fila
            if (coincideTodos) {
                fila.style.display = ""; // Mostrar fila
                filasFiltradas.push(fila); // Agregar a filas filtradas
                coincidencias++;
            }
        });

        // Mostrar mensaje si no hay coincidencias
        if (coincidencias === 0 && hayFiltrosActivos) {
            const filaMensaje = document.createElement("tr");
            filaMensaje.classList.add("mensaje-no-resultados");
            filaMensaje.innerHTML = `
                <td colspan="6" style="text-align:center;color: red;font-weight: bold;">
                    No se encontraron resultados con los filtros aplicados.
                </td>
            `;
            $tablaBody.appendChild(filaMensaje);
        }

        // Aplicar paginación a los resultados filtrados
        aplicarPaginacion();
        actualizarFilasMostradas();
    }

    // Función para aplicar paginación
    function aplicarPaginacion() {
        const numFilasAMostrar = parseInt($numFilas.value);
        const filas = hayFiltrosActivos ? filasFiltradas : Array.from($tablaBody.querySelectorAll("tr.fila-datos"));
        
        // Si numFilasAMostrar es 0, mostrar todas las filas
        if (numFilasAMostrar === 0) {
            filas.forEach(fila => {
                fila.style.display = "";
            });
            return;
        }
        
        // Ocultar todas las filas primero
        filas.forEach(fila => {
            fila.style.display = "none";
        });
        
        // Mostrar solo las primeras N filas (según el selector)
        for (let i = 0; i < Math.min(numFilasAMostrar, filas.length); i++) {
            filas[i].style.display = "";
        }
    }

    // Función para actualizar el contador de filas mostradas
    function actualizarFilasMostradas() {
        const filasVisibles = hayFiltrosActivos 
            ? filasFiltradas.length 
            : document.querySelectorAll(".fila-datos").length;
        
        $filasMostradas.textContent = filasVisibles;
    }

    // Añadir eventos a los filtros
    $filtrosCampos.forEach(filtro => {
        filtro.addEventListener("input", aplicarFiltros);
        filtro.addEventListener("change", aplicarFiltros);
    });

    // Evento para cambiar el número de filas a mostrar
    if ($numFilas) {
        $numFilas.addEventListener("change", function() {
            aplicarPaginacion();
            actualizarFilasMostradas();
        });
    }

    // 🟢 Exportar a Excel
    if ($btnExportarExcel) {
        $btnExportarExcel.addEventListener("click", function () {
            try {
                const tablaClonada = $tabla.cloneNode(true);
                const tbodyClonado = tablaClonada.querySelector("tbody");

                // Limpiar el tbody clonado
                tbodyClonado.innerHTML = "";

                // Usar datos filtrados si hay filtros activos, de lo contrario usar todas las filas
                const filasAExportar = hayFiltrosActivos 
                    ? filasFiltradas 
                    : $tablaBody.querySelectorAll("tr.fila-datos");

                filasAExportar.forEach((fila) => {
                    const filaClonada = fila.cloneNode(true); // Clonar la fila
                    // Eliminar la última columna (Acción)
                    const celdas = filaClonada.querySelectorAll("td");
                    if (celdas.length > 5) { // Verificar que haya más de 5 columnas
                        celdas[celdas.length - 1].remove(); // Eliminar la última celda (Acción)
                    }
                    tbodyClonado.appendChild(filaClonada); // Agregar la fila clonada al tbody
                });

                // Eliminar la última columna del encabezado
                const theadClonado = tablaClonada.querySelector("thead");
                const filaEncabezado = theadClonado.querySelector("tr");
                const celdasEncabezado = filaEncabezado.querySelectorAll("th");
                if (celdasEncabezado.length > 5) { // Verificar que haya más de 5 columnas
                    celdasEncabezado[celdasEncabezado.length - 1].remove(); // Eliminar la última celda (Acción)
                }

                // Exportar el clon de la tabla
                let tableExport = new TableExport(tablaClonada, {
                    exportButtons: false,
                    filename: "Reporte_Entregas" + (hayFiltrosActivos ? "_Filtrado" : ""),
                    sheetname: "Entregas",
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
                
                mostrarMensaje("Archivo Excel generado correctamente", "info");
            } catch (error) {
                console.error("Error al exportar a Excel:", error);
                mostrarMensaje("Error al exportar a Excel", "info");
            }
        });
    }

    // 🔴 Exportar a PDF
    if ($btnExportarPDF) {
        $btnExportarPDF.addEventListener("click", function () {
            try {
                const { jsPDF } = window.jspdf;
                const doc = new jsPDF();

                // Título del documento
                doc.text("Reporte de Entregas" + (hayFiltrosActivos ? " Filtrado" : ""), 14, 15);
                
                // Fecha y hora de generación
                const fechaActual = new Date();
                doc.setFontSize(10);
                doc.text(`Fecha de generación: ${fechaActual.toLocaleDateString()} ${fechaActual.toLocaleTimeString()}`, 14, 22);

                // Obtener encabezados sin la última columna
                const headers = [];
                document.querySelectorAll("#tbl_entregas thead th").forEach((th, index) => {
                    if (index < 5) { // Evitar la última columna (Acción)
                        headers.push(th.innerText);
                    }
                });

                // Obtener filas sin la última columna
                const data = [];
                const filasAExportar = hayFiltrosActivos 
                    ? filasFiltradas 
                    : $tablaBody.querySelectorAll("tr.fila-datos");

                filasAExportar.forEach((fila) => {
                    const rowData = [];
                    fila.querySelectorAll("td").forEach((td, index) => {
                        if (index < 5) { // Evitar la última columna (Acción)
                            rowData.push(td.innerText);
                        }
                    });
                    data.push(rowData);
                });

                // Generar tabla en el PDF
                doc.autoTable({
                    head: [headers],
                    body: data,
                    startY: 30,
                    theme: "striped",
                    styles: { fontSize: 9, cellPadding: 3 },
                    headStyles: { fillColor: [44, 62, 80], textColor: [255, 255, 255] },
                    alternateRowStyles: { fillColor: [240, 240, 240] },
                    margin: { top: 30 },
                    didDrawPage: function (data) {
                        // Agregar número de página en el pie de página
                        doc.setFontSize(8);
                        doc.text(
                            `Página ${doc.getNumberOfPages()}`,
                            data.settings.margin.left,
                            doc.internal.pageSize.height - 10
                        );
                    }
                });

                doc.save("Reporte_Entregas" + (hayFiltrosActivos ? "_Filtrado" : "") + ".pdf");
                mostrarMensaje("Archivo PDF generado correctamente", "info");
            } catch (error) {
                console.error("Error al exportar a PDF:", error);
                mostrarMensaje("Error al exportar a PDF", "info");
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

                // Usar datos filtrados si hay filtros activos, de lo contrario usar todas las filas
                const filasAImprimir = hayFiltrosActivos 
                    ? filasFiltradas 
                    : $tablaBody.querySelectorAll("tr.fila-datos");

                filasAImprimir.forEach((fila) => {
                    const filaClonada = fila.cloneNode(true); // Clonar la fila
                    // Eliminar la última columna (Acción)
                    const celdas = filaClonada.querySelectorAll("td");
                    if (celdas.length > 5) { // Verificar que haya más de 5 columnas
                        celdas[celdas.length - 1].remove(); // Eliminar la última celda (Acción)
                    }
                    tbodyClonado.appendChild(filaClonada); // Agregar la fila clonada al tbody
                });

                // Eliminar la última columna del encabezado
                const theadClonado = tablaHtml.querySelector("thead");
                const filaEncabezado = theadClonado.querySelector("tr");
                const celdasEncabezado = filaEncabezado.querySelectorAll("th");
                if (celdasEncabezado.length > 5) { // Verificar que haya más de 5 columnas
                    celdasEncabezado[celdasEncabezado.length - 1].remove(); // Eliminar la última celda (Acción)
                }

                // Abrir una ventana de impresión
                const ventanaImpresion = window.open("", "", "height=800, width=1000");
                ventanaImpresion.document.write(`
                    <html>
                        <head>
                            <title>Imprimir Reporte de Entregas${hayFiltrosActivos ? " Filtrado" : ""}</title>
                            <style>
                                @media print {
                                    table { width: 100%; border-collapse: collapse; margin: 20px 0; }
                                    th, td { padding: 8px; text-align: left; border: 1px solid #ddd; }
                                    th { background-color: #f4f4f4; font-weight: bold; }
                                    body { font-family: Arial, sans-serif; font-size: 12px; margin: 0; padding: 0; }
                                    @page { margin: 20mm; }
                                    .fecha-generacion { font-size: 10px; color: #666; margin-bottom: 15px; }
                                }
                            </style>
                        </head>
                        <body>
                            <h2>Reporte de Entregas${hayFiltrosActivos ? " Filtrado" : ""}</h2>
                            <div class="fecha-generacion">
                                Fecha de generación: ${new Date().toLocaleDateString()} ${new Date().toLocaleTimeString()}
                            </div>
                            ${tablaHtml.outerHTML}
                        </body>
                    </html>
                `);
                ventanaImpresion.document.close();
                ventanaImpresion.focus();
                ventanaImpresion.print();
                mostrarMensaje("Documento enviado a impresión", "info");
            } catch (error) {
                console.error("Error al imprimir:", error);
                mostrarMensaje("Error al imprimir", "info");
            }
        });
    }

    // Función para mostrar mensajes al usuario (todos en azul)
    function mostrarMensaje(mensaje, tipo = "info") {
        const contenedorMensajes = document.getElementById('contenedor-mensajes');
        const alertElement = document.createElement('div');
        alertElement.className = `alert alert-${tipo} alert-dismissible fade show`;
        alertElement.role = 'alert';
        
        alertElement.innerHTML = `
            ${mensaje}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Cerrar"></button>
        `;
        
        contenedorMensajes.appendChild(alertElement);
        
        // Auto-cerrar el mensaje después de 3 segundos
        setTimeout(() => {
            alertElement.classList.remove('show');
            setTimeout(() => {
                contenedorMensajes.removeChild(alertElement);
            }, 300);
        }, 3000);
    }
});