document.addEventListener("DOMContentLoaded", function () {
    // Elementos DOM
    const $btnExportarExcel = document.querySelector("#btnExportarExcel"),
          $btnExportarPDF = document.querySelector("#btnExportarPDF"),
          $btnImprimir = document.querySelector("#btnImprimir"),
          $tabla = document.querySelector("#tbl_direcciones"),
          $tablaBody = document.querySelector("#tabla_direcciones_body"),
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
                <td colspan="8" style="text-align:center;color: red;font-weight: bold;">
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
                    // Eliminar las últimas dos columnas (Acción Estado y Acciones)
                    const celdas = filaClonada.querySelectorAll("td");
                    if (celdas.length > 6) { // Verificar que haya más de 6 columnas
                        celdas[celdas.length - 1].remove(); // Eliminar la última celda (Acciones)
                        celdas[celdas.length - 2].remove(); // Eliminar la penúltima celda (Acción Estado)
                    }
                    tbodyClonado.appendChild(filaClonada); // Agregar la fila clonada al tbody
                });

                // Eliminar las últimas dos columnas del encabezado
                const theadClonado = tablaClonada.querySelector("thead");
                const filaEncabezado = theadClonado.querySelector("tr");
                const celdasEncabezado = filaEncabezado.querySelectorAll("th");
                if (celdasEncabezado.length > 6) { // Verificar que haya más de 6 columnas
                    celdasEncabezado[celdasEncabezado.length - 1].remove(); // Eliminar la última celda (Acciones)
                    celdasEncabezado[celdasEncabezado.length - 2].remove(); // Eliminar la penúltima celda (Acción Estado)
                }

                // Exportar el clon de la tabla
                let tableExport = new TableExport(tablaClonada, {
                    exportButtons: false,
                    filename: "Reporte_Direcciones" + (hayFiltrosActivos ? "_Filtrado" : ""),
                    sheetname: "Direcciones",
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
                
                mostrarMensaje("Archivo Excel generado correctamente", "success");
            } catch (error) {
                console.error("Error al exportar a Excel:", error);
                mostrarMensaje("Error al exportar a Excel", "danger");
            }
        });
    }

    // 🔴 Exportar a PDF
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
                const title = "Reporte de Direcciones" + (hayFiltrosActivos ? " (Filtrado)" : "");
                doc.text(title, rightTextX, 30, { align: "right" });
    
                // Fecha de generación (derecha)
                doc.setFontSize(10);
                const fechaActual = new Date();
                const fechaText = `Generado: ${fechaActual.toLocaleDateString()} ${fechaActual.toLocaleTimeString()}`;
                doc.text(fechaText, rightTextX, 36, { align: "right" });
    
                // Línea separadora
                doc.setDrawColor(200, 200, 200);
                doc.line(leftMargin, 45, pageWidth - rightMargin, 45);
    
                // Obtener encabezados excluyendo columnas de Acción
                const headers = Array.from(document.querySelectorAll("#tbl_direcciones thead th"))
                    .filter((th, index) => index < 6) // Excluir últimas dos columnas
                    .map(th => th.innerText.replace(/\s+/g, ' ').trim());
    
                // Obtener datos excluyendo columnas de Acción
                const data = [];
                const filasAExportar = hayFiltrosActivos 
                    ? filasFiltradas 
                    : document.querySelectorAll("#tbl_direcciones tbody tr.fila-datos");
                
                filasAExportar.forEach(tr => {
                    const rowData = Array.from(tr.querySelectorAll("td"))
                        .filter((td, index) => index < 6) // Excluir últimas dos columnas
                        .map(td => td.innerText.replace(/\s+/g, ' ').trim());
                    
                    if (rowData.length > 0 && rowData.some(cell => cell !== '')) {
                        data.push(rowData);
                    }
                });
    
                // Generar tabla centrada (optimizada para 6 columnas)
                doc.autoTable({
                    head: [headers],
                    body: data,
                    startY: 55, // Posición después del encabezado
                    theme: "grid",
                    styles: { 
                        fontSize: 9,
                        cellPadding: 3,
                        overflow: 'linebreak',
                        halign: 'center'
                    },
                    columnStyles: {
                        // Ajustar anchos específicos para 6 columnas
                        0: { cellWidth: 'auto' },
                        1: { cellWidth: 'auto' },
                        2: { cellWidth: 'auto' },
                        3: { cellWidth: 'auto' },
                        4: { cellWidth: 'auto' },
                        5: { cellWidth: 'auto' }
                    },
                    headStyles: { 
                        fillColor: [44, 62, 80], // Azul oscuro corporativo
                        textColor: [255, 255, 255],
                        fontStyle: 'bold',
                        cellPadding: 4
                    },
                    margin: { horizontal: 'center' }, // Centrar horizontalmente
                    tableWidth: 'wrap', // Ajustar automáticamente al ancho de contenido
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
    
                doc.save("Reporte_Direcciones_TamalesBuenSazon" + (hayFiltrosActivos ? "_Filtrado" : "") + ".pdf");
                mostrarMensaje("Archivo PDF generado correctamente", "success");
            } catch (error) {
                console.error("Error al exportar a PDF:", error);
                mostrarMensaje("Error al exportar a PDF", "danger");
            }
        });
    }

    // 🔵 Imprimir
    if ($btnImprimir) {
        $btnImprimir.addEventListener("click", function () {
            try {
                // Clonar la tabla completa
                const tablaHtml = $tabla.cloneNode(true);
                const tbodyClonado = tablaHtml.querySelector("tbody");
                tbodyClonado.innerHTML = "";
    
                // Obtener filas a imprimir (filtradas o todas)
                const filasAImprimir = hayFiltrosActivos 
                    ? filasFiltradas 
                    : $tablaBody.querySelectorAll("tr.fila-datos");
    
                // Procesar cada fila para imprimir
                filasAImprimir.forEach((fila) => {
                    const filaClonada = fila.cloneNode(true);
                    const celdas = filaClonada.querySelectorAll("td");
                    
                    // Eliminar columnas de acción (últimas dos columnas)
                    if (celdas.length > 6) {
                        celdas[celdas.length - 1].remove(); // Eliminar Acciones
                        celdas[celdas.length - 2].remove(); // Eliminar Acción Estado
                    }
                    
                    tbodyClonado.appendChild(filaClonada);
                });
    
                // Eliminar columnas de acción del encabezado
                const theadClonado = tablaHtml.querySelector("thead");
                const celdasEncabezado = theadClonado.querySelectorAll("th");
                if (celdasEncabezado.length > 6) {
                    celdasEncabezado[celdasEncabezado.length - 1].remove(); // Eliminar Acciones
                    celdasEncabezado[celdasEncabezado.length - 2].remove(); // Eliminar Acción Estado
                }
    
                // Configurar ventana de impresión con diseño profesional
                const ventanaImpresion = window.open("", "_blank", "width=1000,height=600");
                const fechaActual = new Date();
                const fechaTexto = fechaActual.toLocaleDateString() + ' ' + fechaActual.toLocaleTimeString();
                
                ventanaImpresion.document.write(`
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <title>Reporte de Direcciones - Tamales el Buen Sazón</title>
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
                                table {
                                    width: 100%;
                                    border-collapse: collapse;
                                    margin-top: 15px;
                                    font-size: 12px;
                                }
                                th {
                                    background-color: #2c3e50;
                                    color: white;
                                    padding: 10px;
                                    text-align: left;
                                    font-weight: bold;
                                }
                                td {
                                    padding: 8px;
                                    border-bottom: 1px solid #eee;
                                    vertical-align: top;
                                }
                                .address {
                                    max-width: 250px;
                                    word-wrap: break-word;
                                }
                                tr:nth-child(even) {
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
                                <div class="report-title">Reporte de Direcciones${hayFiltrosActivos ? " (Filtrado)" : ""}</div>
                                <div class="report-date">Generado: ${fechaTexto}</div>
                            </div>
                        </div>
                        
                        ${tablaHtml.outerHTML}
                        
                        <div class="footer">
                            Página 1 de 1 • ${fechaTexto}
                        </div>
                        
                        <script>
                            // Calcular número de páginas y aplicar estilos después de cargar
                            window.onload = function() {
                                // Aplicar estilo especial a direcciones largas
                                document.querySelectorAll('td:nth-child(3)').forEach(td => {
                                    td.classList.add('address');
                                });
                                
                                const pageHeight = window.innerHeight;
                                const tableHeight = document.querySelector('table').offsetHeight;
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