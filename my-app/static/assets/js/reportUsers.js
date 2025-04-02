document.addEventListener("DOMContentLoaded", function () {
    // Elementos DOM
    const $btnExportarExcel = document.querySelector("#btnExportarExcel"),
          $btnExportarPDF = document.querySelector("#btnExportarPDF"),
          $btnImprimir = document.querySelector("#btnImprimir"),
          $tabla = document.querySelector("#tbl_usuarios"),
          $tablaBody = document.querySelector("#tabla_usuarios_body"),
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
                <td colspan="10" style="text-align:center;color: red;font-weight: bold;">
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
                    filename: "Reporte_Usuarios" + (hayFiltrosActivos ? "_Filtrado" : ""),
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
                const title = "Reporte de Usuarios";
                doc.text(title, rightTextX, 30, { align: "right" });
    
                // Fecha de generación (derecha)
                doc.setFontSize(10);
                const fechaActual = new Date();
                const fechaText = `Generado: ${fechaActual.toLocaleDateString()} ${fechaActual.toLocaleTimeString()}`;
                doc.text(fechaText, rightTextX, 36, { align: "right" });
    
                // Línea separadora
                doc.setDrawColor(200, 200, 200);
                doc.line(leftMargin, 45, pageWidth - rightMargin, 45);
    

                
    
                // Extraer encabezados y datos de la tabla
                const headers = Array.from(document.querySelectorAll("#tbl_usuarios thead th"))
                    .slice(0, 8)
                    .map(th => th.innerText.replace(/\s+/g, ' ').trim());
    
                const data = [];
                const filasAExportar = hayFiltrosActivos 
                    ? filasFiltradas 
                    : document.querySelectorAll("#tbl_usuarios tbody tr.fila-datos");
                
                filasAExportar.forEach(tr => {
                    const rowData = Array.from(tr.querySelectorAll("td"))
                        .slice(0, 8)
                        .map(td => td.innerText.replace(/\s+/g, ' ').trim());
                    if (rowData.length > 0) data.push(rowData);
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
                        overflow: 'linebreak'
                    },
                    headStyles: { 
                        fillColor: [44, 62, 80],
                        textColor: [255, 255, 255],
                        fontStyle: 'bold'
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
    
                doc.save("Reporte_Usuarios_TamalesBuenSazon.pdf");
                mostrarMensaje("PDF generado correctamente", "success");
            } catch (error) {
                console.error("Error al exportar PDF:", error);
                mostrarMensaje("Error al generar PDF", "danger");
            }
        });
    }
    //if ($btnImprimir) {
    $btnImprimir.addEventListener("click", function () {
        try {
            const tablaHtml = $tabla.cloneNode(true); // Clonar la tabla
            const tbodyClonado = tablaHtml.querySelector("tbody");

            // Limpiar el tbody clonado
            tbodyClonado.innerHTML = "";

            // Usar datos filtrados si hay filtros activos
            const filasAImprimir = hayFiltrosActivos 
                ? filasFiltradas 
                : $tablaBody.querySelectorAll("tr.fila-datos");

            // Clonar y procesar filas
            filasAImprimir.forEach((fila) => {
                const filaClonada = fila.cloneNode(true);
                const celdas = filaClonada.querySelectorAll("td");
                
                // Eliminar columnas de acción (últimas dos)
                if (celdas.length > 8) {
                    celdas[celdas.length - 1].remove(); // Acciones
                    celdas[celdas.length - 2].remove(); // Acción Estado
                }
                tbodyClonado.appendChild(filaClonada);
            });

            // Eliminar columnas del encabezado
            const theadClonado = tablaHtml.querySelector("thead");
            const celdasEncabezado = theadClonado.querySelectorAll("th");
            if (celdasEncabezado.length > 8) {
                celdasEncabezado[celdasEncabezado.length - 1].remove();
                celdasEncabezado[celdasEncabezado.length - 2].remove();
            }

            // Configurar ventana de impresión con estilo profesional
            const ventanaImpresion = window.open("", "", "height=800, width=1000");
            const fechaActual = new Date();
            const fechaText = `Generado: ${fechaActual.toLocaleDateString()} ${fechaActual.toLocaleTimeString()}`;
            
            ventanaImpresion.document.write(`
                <html>
                    <head>
                        <title>Reporte de Usuarios - Tamales el Buen Sazón</title>
                        <style>
                            @media print {
                                body { 
                                    font-family: Arial, sans-serif; 
                                    margin: 0; 
                                    padding: 15px;
                                }
                                .header { 
                                    display: flex; 
                                    justify-content: space-between;
                                    align-items: center;
                                    margin-bottom: 15px;
                                    border-bottom: 1px solid #ddd;
                                    padding-bottom: 10px;
                                }
                                .logo { 
                                    height: 50px; 
                                    margin-right: 15px;
                                }
                                .company-info { 
                                    flex-grow: 1;
                                }
                                .company-name { 
                                    font-size: 18px; 
                                    font-weight: bold;
                                    color: #2c3e50;
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
                                th, td { 
                                    padding: 8px; 
                                    text-align: left; 
                                    border: 1px solid #ddd; 
                                }
                                th { 
                                    background-color: #2c3e50; 
                                    color: white; 
                                    font-weight: bold;
                                }
                                tr:nth-child(even) { 
                                    background-color: #f9f9f9; 
                                }
                                .footer { 
                                    margin-top: 15px;
                                    font-size: 10px; 
                                    color: #666;
                                    text-align: right;
                                }
                                @page { 
                                    margin: 15mm; 
                                }
                            }
                        </style>
                    </head>
                    <body>
                        <div class="header">
                            <div class="company-info">
                                <div class="company-name">Tamales el Buen Sazón</div>
                                <div class="report-title">Reporte de Usuarios${hayFiltrosActivos ? " (Filtrado)" : ""}</div>
                                <div class="report-date">${fechaText}</div>
                            </div>
                            <img src="/static/assets/img/logose.png" class="logo" alt="Logo">
                        </div>
                        
                        ${tablaHtml.outerHTML}
                        
                        <div class="footer">
                            Página 1 de 1 • ${fechaText}
                        </div>
                        
                        <script>
                            // Ajustar número de páginas después de cargar
                            window.onload = function() {
                                const totalPages = Math.ceil(document.querySelector('table').offsetHeight / (window.innerHeight - 200));
                                document.querySelector('.footer').innerHTML = 
                                    \`Página 1 de \${totalPages} • ${fechaText}\`;
                            };
                        </script>
                    </body>
                </html>
            `);
            
            ventanaImpresion.document.close();
            ventanaImpresion.focus();
            
            // Retrasar ligeramente la impresión para asegurar que los estilos se apliquen
            setTimeout(() => {
                ventanaImpresion.print();
                mostrarMensaje("Documento enviado a impresión", "info");
            }, 300);
            
        } catch (error) {
            console.error("Error al imprimir:", error);
            mostrarMensaje("Error al imprimir", "danger");
        }
    });

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