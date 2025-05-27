document.addEventListener('DOMContentLoaded', function() {
    // Cargar municipios dinámicamente al cambiar departamento
    const departamentoSelect = document.getElementById('departamento_id');
    const municipioSelect = document.getElementById('municipio_id');
    
    if (departamentoSelect && municipioSelect) {
        departamentoSelect.addEventListener('change', function() {
            const departamentoId = this.value;
            
            if (departamentoId) {
                // Mostrar indicador de carga
                municipioSelect.innerHTML = '<option value="">Cargando...</option>';
                municipioSelect.disabled = true;
                
                fetch(`/obtener_municipios?departamento_id=${departamentoId}`)
                    .then(response => {
                        if (!response.ok) {
                            throw new Error('Error en la solicitud');
                        }
                        return response.json();
                    })
                    .then(data => {
                        municipioSelect.innerHTML = '<option value="">Seleccione</option>';
                        data.forEach(municipio => {
                            const option = document.createElement('option');
                            option.value = municipio.id;
                            option.textContent = municipio.nombre;
                            municipioSelect.appendChild(option);
                        });
                        municipioSelect.disabled = false;
                    })
                    .catch(error => {
                        console.error('Error al obtener municipios:', error);
                        municipioSelect.innerHTML = '<option value="">Error al cargar</option>';
                        municipioSelect.disabled = false;
                    });
            } else {
                municipioSelect.innerHTML = '<option value="">Seleccione</option>';
                municipioSelect.disabled = false;
            }
        });
    }

    // Validaciones de formulario
    const form = document.querySelector('.form-horizontal');
    if (form) {
        form.addEventListener('submit', function(event) {
            let isValid = true;
            
            // Validar campos requeridos
            const requiredFields = form.querySelectorAll('[required]');
            requiredFields.forEach(field => {
                if (!field.value) {
                    field.setCustomValidity('Este campo es obligatorio');
                    isValid = false;
                } else {
                    field.setCustomValidity('');
                }
            });

            // Validar costo domicilio
            const costoDomicilio = form.querySelector('[name="costo_domicilio"]');
            if (costoDomicilio && (isNaN(costoDomicilio.value) || costoDomicilio.value < 0)) {
                costoDomicilio.setCustomValidity('Ingrese un valor válido (número positivo)');
                isValid = false;
            }

            if (!isValid) {
                event.preventDefault();
                this.reportValidity();
            }
        });
    }

    // Inicializar Select2 si está presente
    if (window.$ && $.fn.select2) {
        $('#departamento_id, #municipio_id, #users_id').select2({
            placeholder: "Seleccione una opción",
            allowClear: true
        });
    }
});

//editar direccion



 