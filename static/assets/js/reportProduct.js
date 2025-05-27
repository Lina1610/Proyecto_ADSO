document.addEventListener("DOMContentLoaded", function () {
    // Elementos DOM
    const $btnExportarExcel = document.querySelector("#btnExportarExcel"),
          $btnExportarPDF = document.querySelector("#btnExportarPDF"),
          $btnImprimir = document.querySelector("#btnImprimir"),
          $tabla = document.querySelector("#tbl_productos"),
          $tablaBody = document.querySelector("#tabla_productos_body"),
          $toggleFiltros = document.querySelector("#toggleFiltros"),
          $panelFiltros = document.querySelector("#panelFiltros"),
          $limpiarFiltros = document.querySelector("#limpiarFiltros"),
          $filtrosCampos = document.querySelectorAll(".filtro-campo");
  
    let filasFiltradas = []; // Almacenará las filas filtradas
    let hayFiltrosActivos = false; // Indica si hay filtros activos
  
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
  
            hayFiltrosActivos = false;
            filasFiltradas = [];
  
            // Eliminar mensaje de "No se encontraron resultados"
            const mensajeAnterior = $tablaBody.querySelector(".mensaje-no-resultados");
            if (mensajeAnterior) {
                mensajeAnterior.remove();
            }
  
            // Actualizar el contador de filas
            actualizarFilasMostradas();
        });
    }
  
    // Función para aplicar filtros a la tabla
    function aplicarFiltros() {
        // Eliminar mensaje anterior si existe
        const mensajeAnterior = $tablaBody.querySelector(".mensaje-no-resultados");
        if (mensajeAnterior) {
            mensajeAnterior.remove();
        }
  
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
                <td colspan="9" style="text-align:center;color: red;font-weight: bold;">
                    No se encontraron resultados con los filtros aplicados.
                </td>
            `;
            $tablaBody.appendChild(filaMensaje);
        }
  
        // Actualizar el contador de filas
        actualizarFilasMostradas();
    }
  
    // Función para actualizar el contador de filas mostradas
    function actualizarFilasMostradas() {
        const filasVisibles = hayFiltrosActivos 
            ? filasFiltradas.length 
            : document.querySelectorAll(".fila-datos").length;
        
        document.getElementById("filas-mostradas").textContent = filasVisibles;
        document.getElementById("filas-totales").textContent = document.querySelectorAll(".fila-datos").length;
    }
  
    // Añadir eventos a los filtros
    $filtrosCampos.forEach(filtro => {
        filtro.addEventListener("input", aplicarFiltros);
        filtro.addEventListener("change", aplicarFiltros);
    });
  
    // Función para obtener filas visibles (filtradas o todas)
    function obtenerFilasExportar() {
        if (hayFiltrosActivos && filasFiltradas.length > 0) {
            return filasFiltradas;
        } else {
            return Array.from($tablaBody.querySelectorAll("tr.fila-datos:not([style*='display: none'])"));
        }
    }
  
    // 🟢 Exportar a Excel
    if ($btnExportarExcel) {
        $btnExportarExcel.addEventListener("click", function () {
            try {
                // Crear una tabla temporal para la exportación
                const tablaTemp = document.createElement('table');
                tablaTemp.id = "tabla_exportacion";
                
                // Clonar encabezados sin la columna de acción
                const thead = document.createElement('thead');
                const trHead = document.createElement('tr');
                
                // Clonar encabezados excepto el último (Acción)
                document.querySelectorAll("#tbl_productos thead th").forEach((th, index) => {
                    if (index !== 8) { // Excluir columna de acción (índice 8)
                        const clonTh = th.cloneNode(true);
                        trHead.appendChild(clonTh);
                    }
                });
                
                thead.appendChild(trHead);
                tablaTemp.appendChild(thead);
                
                // Clonar filas visibles sin la columna de acción
                const tbody = document.createElement('tbody');
                const filasExportar = obtenerFilasExportar();
                
                filasExportar.forEach(fila => {
                    const clonFila = document.createElement('tr');
                    
                    fila.querySelectorAll("td").forEach((td, index) => {
                        if (index !== 8) { // Excluir columna de acción (índice 8)
                            const clonTd = td.cloneNode(true);
                            clonFila.appendChild(clonTd);
                        }
                    });
                    
                    tbody.appendChild(clonFila);
                });
                
                tablaTemp.appendChild(tbody);
                
                // Agregar la tabla temporal al DOM (oculta)
                tablaTemp.style.display = 'none';
                document.body.appendChild(tablaTemp);
                
                // Exportar la tabla temporal
                let tableExport = new TableExport(tablaTemp, {
                    formats: ["xlsx"],
                    exportButtons: false,
                    filename: "Reporte_Productos",
                    sheetname: "Productos",
                });
                
                let datos = tableExport.getExportData();
                let preferenciasDocumento = datos[tablaTemp.id].xlsx;
                
                tableExport.export2file(
                    preferenciasDocumento.data,
                    preferenciasDocumento.mimeType,
                    preferenciasDocumento.filename,
                    preferenciasDocumento.fileExtension,
                    preferenciasDocumento.merges,
                    preferenciasDocumento.RTL,
                    preferenciasDocumento.sheetname
                );
                
                // Eliminar la tabla temporal
                document.body.removeChild(tablaTemp);
  
                // Mostrar mensaje de éxito
                mostrarMensaje("Archivo Excel generado correctamente", "success");
            } catch (error) {
                console.error("Error al exportar a Excel:", error);
                mostrarMensaje("Error al exportar a Excel", "danger");
            }
        });
    }
  
    // 🔴 Exportar a PDF sin la columna "Acción"
    if ($btnExportarPDF) {
        $btnExportarPDF.addEventListener("click", function () {
            try {
                const { jsPDF } = window.jspdf;
                const doc = new jsPDF();
  
                doc.text("Reporte de Productos", 14, 10);
  
                // Obtener encabezados sin la columna "Acción"
                const headers = [];
                document
                    .querySelectorAll("#tbl_productos thead th")
                    .forEach((th, index) => {
                        if (index !== 8) { // Excluir columna de acción (índice 8)
                            headers.push(th.innerText);
                        }
                    });
  
                // Obtener filas visibles (filtradas o todas) sin la columna "Acción"
                const data = [];
                const filasExportar = obtenerFilasExportar();
                
                filasExportar.forEach(row => {
                    const rowData = [];
                    row.querySelectorAll("td").forEach((td, index) => {
                        if (index !== 8) { // Excluir columna de acción (índice 8)
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
  
                // Mostrar mensaje de éxito
                mostrarMensaje("Archivo PDF generado correctamente", "success");
            } catch (error) {
                console.error("Error al exportar a PDF:", error);
                mostrarMensaje("Error al exportar a PDF", "danger");
            }
        });
    }
  
    // 🔵 Imprimir la tabla sin la columna "Acción"
    if ($btnImprimir) {
        $btnImprimir.addEventListener("click", function () {
            try {
                // Crear una tabla temporal para imprimir
                const tablaTemp = document.createElement('table');
                tablaTemp.classList.add('table', 'table-striped', 'table-bordered');
                
                // Clonar encabezados sin la columna de acción
                const thead = document.createElement('thead');
                const trHead = document.createElement('tr');
                
                document.querySelectorAll("#tbl_productos thead th").forEach((th, index) => {
                    if (index !== 8) { // Excluir columna de acción (índice 8)
                        const clonTh = th.cloneNode(true);
                        trHead.appendChild(clonTh);
                    }
                });
                
                thead.appendChild(trHead);
                tablaTemp.appendChild(thead);
                
                // Clonar filas visibles sin la columna de acción
                const tbody = document.createElement('tbody');
                const filasExportar = obtenerFilasExportar();
                
                filasExportar.forEach(fila => {
                    const clonFila = document.createElement('tr');
                    
                    fila.querySelectorAll("td").forEach((td, index) => {
                        if (index !== 8) { // Excluir columna de acción (índice 8)
                            const clonTd = td.cloneNode(true);
                            clonFila.appendChild(clonTd);
                        }
                    });
                    
                    tbody.appendChild(clonFila);
                });
                
                tablaTemp.appendChild(tbody);
                
                // Abrir ventana de impresión
                const ventanaImpresion = window.open("", "", "height=800, width=1000");
  
                ventanaImpresion.document.write(
                    "<html><head><title>Imprimir Reporte</title>"
                );
                ventanaImpresion.document.write("<style>");
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
                    "body { font-family: Arial, sans-serif; font-size: 12px; }"
                );
                ventanaImpresion.document.write("@page { margin: 20mm; }");
                ventanaImpresion.document.write("</style></head>");
                ventanaImpresion.document.write("<body>");
                ventanaImpresion.document.write("<h2>Reporte de Productos</h2>");
                ventanaImpresion.document.write(tablaTemp.outerHTML);
                ventanaImpresion.document.write("</body></html>");
  
                ventanaImpresion.document.close();
                ventanaImpresion.print();
  
                // Mostrar mensaje de éxito
                mostrarMensaje("Documento enviado a impresión", "info");
            } catch (error) {
                console.error("Error al imprimir:", error);
                mostrarMensaje("Error al imprimir", "danger");
            }
        });
    }
  
    // Función para mostrar mensajes al usuario
    function mostrarMensaje(mensaje, tipo) {
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
