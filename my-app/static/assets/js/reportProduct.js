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
                
                // Configuración del logo (lado izquierdo)
                const logoUrl = "/static/assets/img/logose.png";
                const logoWidth = 30;
                const logoHeight = 30;
                const leftMargin = 15; // Margen izquierdo para el logo
    
                // Agregar logo (posición fija izquierda)
                try {
                    doc.addImage(logoUrl, "PNG", leftMargin, 15, logoWidth, logoHeight);
                } catch (imageError) {
                    console.error("Error al cargar la imagen del logo:", imageError);
                }
    
                // Configuración texto derecho
                const pageWidth = doc.internal.pageSize.getWidth();
                const rightMargin = 20; // Margen derecho
                const rightTextX = pageWidth - rightMargin; // Posición X para texto derecho
    
                // Nombre de la empresa (derecha)
                doc.setFontSize(14);
                doc.setFont("helvetica", "bold");
                doc.text("Tamales el Buen Sazón", rightTextX, 20, { align: "right" });
    
                // Título del reporte (derecha)
                doc.setFontSize(12);
                doc.setFont("helvetica", "normal");
                const title = "Reporte de Productos" + (hayFiltrosActivos ? " (Filtrado)" : "");
                doc.text(title, rightTextX, 30, { align: "right" });
    
                // Fecha de generación (derecha)
                doc.setFontSize(10);
                const fechaActual = new Date();
                const fechaText = `Generado: ${fechaActual.toLocaleDateString()} ${fechaActual.toLocaleTimeString()}`;
                doc.text(fechaText, rightTextX, 36, { align: "right" });
    
                // Línea separadora
                doc.setDrawColor(200, 200, 200);
                doc.line(leftMargin, 45, pageWidth - rightMargin, 45);

                // Obtener encabezados excluyendo columna de Acción
                const headers = Array.from(document.querySelectorAll("#tbl_productos thead th"))
                    .filter((th, index) => index !== 8) // Excluir columna de acción (índice 8)
                    .map(th => th.innerText.replace(/\s+/g, ' ').trim());
    
                // Obtener datos excluyendo columna de Acción
                const data = [];
                const filasAExportar = hayFiltrosActivos 
                    ? filasFiltradas 
                    : document.querySelectorAll("#tbl_productos tbody tr.fila-datos");
                
                filasAExportar.forEach(tr => {
                    const rowData = Array.from(tr.querySelectorAll("td"))
                        .filter((td, index) => index !== 8) // Excluir columna de acción
                        .map(td => td.innerText.replace(/\s+/g, ' ').trim());
                    
                    if (rowData.length > 0 && rowData.some(cell => cell !== '')) {
                        data.push(rowData);
                    }
                });
    
                // Generar tabla centrada
                doc.autoTable({
                    head: [headers],
                    body: data,
                    startY: 55, // Posición después del encabezado
                    theme: "grid",
                    styles: { 
                        fontSize: 8,
                        cellPadding: 3,
                        overflow: 'linebreak',
                        halign: 'center'
                    },
                    headStyles: { 
                        fillColor: [44, 62, 80],
                        textColor: [255, 255, 255],
                        fontStyle: 'bold',
                        cellPadding: 4
                    },
                    margin: { horizontal: 'center' }, // Centrar horizontalmente
                    didDrawPage: function(data) {
                        // Número de página (derecha abajo)
                        doc.setFontSize(8);
                        doc.text(
                            `Página ${doc.getNumberOfPages()}`,
                            pageWidth - rightMargin,
                            doc.internal.pageSize.height - 10,
                            { align: "right" }
                        );
                    }
                });
    
                doc.save("Reporte_Productos_TamalesBuenSazon" + (hayFiltrosActivos ? "_Filtrado" : "") + ".pdf");
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
                // Crear tabla temporal con estructura completa
                const tablaTemp = document.createElement('table');
                tablaTemp.className = 'table-print';
                
                // Clonar encabezados excluyendo columna de acción
                const thead = document.createElement('thead');
                const trHead = document.createElement('tr');
                
                document.querySelectorAll("#tbl_productos thead th").forEach((th, index) => {
                    if (index !== 8) { // Excluir columna de acción (índice 8)
                        const thClon = th.cloneNode(true);
                        thClon.style.backgroundColor = '#2c3e50';
                        thClon.style.color = 'white';
                        thClon.style.padding = '10px';
                        trHead.appendChild(thClon);
                    }
                });
                
                thead.appendChild(trHead);
                tablaTemp.appendChild(thead);
                
                // Clonar filas de datos excluyendo columna de acción
                const tbody = document.createElement('tbody');
                const filasAImprimir = obtenerFilasExportar();
                
                filasAImprimir.forEach(fila => {
                    const trClon = fila.cloneNode(false);
                    
                    fila.querySelectorAll("td").forEach((td, index) => {
                        if (index !== 8) { // Excluir columna de acción
                            const tdClon = td.cloneNode(true);
                            tdClon.style.padding = '8px';
                            tdClon.style.borderBottom = '1px solid #eee';
                            trClon.appendChild(tdClon);
                        }
                    });
                    
                    tbody.appendChild(trClon);
                });
                
                tablaTemp.appendChild(tbody);
                
                // Configurar ventana de impresión con estilo profesional
                const ventanaImpresion = window.open("", "_blank", "width=1000,height=600");
                const fechaActual = new Date();
                const fechaTexto = fechaActual.toLocaleDateString() + ' ' + fechaActual.toLocaleTimeString();
                
                ventanaImpresion.document.write(`
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <title>Reporte de Productos - Tamales el Buen Sazón</title>
                        <style>
                            @media print {
                                body {
                                    font-family: 'Arial', sans-serif;
                                    margin: 0;
                                    padding: 20px;
                                    color: #333;
                                }
                                .header {
                                    display: flex;
                                    justify-content: space-between;
                                    align-items: center;
                                    margin-bottom: 20px;
                                    padding-bottom: 10px;
                                    border-bottom: 1px solid #ddd;
                                }
                                .logo {
                                    height: 50px;
                                }
                                .company-info {
                                    text-align: right;
                                }
                                .company-name {
                                    font-size: 18px;
                                    font-weight: bold;
                                    color: #2c3e50;
                                    margin-bottom: 5px;
                                }
                                .report-title {
                                    font-size: 16px;
                                    margin: 5px 0;
                                }
                                .report-date {
                                    font-size: 12px;
                                    color: #666;
                                }
                                .table-print {
                                    width: 100%;
                                    border-collapse: collapse;
                                    margin-top: 15px;
                                    font-size: 12px;
                                }
                                .table-print th {
                                    background-color: #2c3e50;
                                    color: white;
                                    padding: 10px;
                                    text-align: left;
                                    font-weight: bold;
                                }
                                .table-print td {
                                    padding: 8px;
                                    border-bottom: 1px solid #eee;
                                    vertical-align: top;
                                }
                                .table-print tr:nth-child(even) {
                                    background-color: #f9f9f9;
                                }
                                .footer {
                                    margin-top: 20px;
                                    font-size: 10px;
                                    color: #666;
                                    text-align: right;
                                    padding-top: 10px;
                                    border-top: 1px solid #ddd;
                                }
                                @page {
                                    size: auto;
                                    margin: 15mm;
                                }
                            }
                        </style>
                    </head>
                    <body>
                        <div class="header">
                            <img src="/static/assets/img/logose.png" class="logo" alt="Logo">
                            <div class="company-info">
                                <div class="company-name">Tamales el Buen Sazón</div>
                                <div class="report-title">Reporte de Productos${hayFiltrosActivos ? " (Filtrado)" : ""}</div>
                                <div class="report-date">Generado: ${fechaTexto}</div>
                            </div>
                        </div>
                        
                        ${tablaTemp.outerHTML}
                        
                        <div class="footer">
                            Página 1 de 1 • ${fechaTexto}
                        </div>
                        
                        <script>
                            // Calcular número de páginas después de cargar
                            window.onload = function() {
                                const pageHeight = window.innerHeight;
                                const tableHeight = document.querySelector('.table-print').offsetHeight;
                                const totalPages = Math.ceil(tableHeight / (pageHeight - 200));
                                
                                document.querySelector('.footer').innerHTML = 
                                    \`Página 1 de \${totalPages} • ${fechaTexto}\`;
                            };
                        </script>
                    </body>
                    </html>
                `);
                
                ventanaImpresion.document.close();
                
                // Esperar a que cargue el contenido antes de imprimir
                ventanaImpresion.onload = function() {
                    setTimeout(() => {
                        ventanaImpresion.print();
                        mostrarMensaje("Documento enviado a impresión", "info");
                    }, 500);
                };
                
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