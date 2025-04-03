document.addEventListener("DOMContentLoaded", function() {
    // ==============================================
    // 1. Funcionalidad del Modal de Ayuda
    // ==============================================
    const helpBtn = document.querySelector('.help-btn');
    const modal = document.getElementById('help-modal'); // Corregido: quitado "56"
    const closeModal = document.querySelector('.close-modal');
    const cancelBtn = document.querySelector('.btn-cancel');

    // Función para mostrar el modal y bloquear scroll
    function showModal() {
        modal.style.display = 'block';
        document.body.style.overflow = 'hidden'; // Bloquea el scroll
    }

    // Función para ocultar el modal y restaurar scroll
    function hideModal() {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto'; // Restaura el scroll
    }

    if (helpBtn && modal && closeModal && cancelBtn) {
        helpBtn.addEventListener('click', function(e) {
            e.preventDefault();
            showModal();
        });

        closeModal.addEventListener('click', hideModal);
        cancelBtn.addEventListener('click', hideModal);

        window.addEventListener('click', function(e) {
            if (e.target === modal) {
                hideModal();
            }
        });

        // ==============================================
        // 2. Envío del Formulario de Soporte
        // ==============================================
        const supportForm = document.getElementById('support-form');
        if (supportForm) {
            supportForm.addEventListener('submit', function(e) {
                e.preventDefault();

                const formData = {
                    nombre: document.getElementById('nombre').value,
                    email: document.getElementById('email').value,
                    asunto: document.getElementById('asunto').value,
                    mensaje: document.getElementById('mensaje').value
                };

                const submitBtn = document.querySelector('.btn-submit');
                if (submitBtn) {
                    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Enviando...';
                    submitBtn.disabled = true;

                    fetch('/soporte/enviar-soporte', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(formData)
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            alert('Mensaje enviado con éxito');
                            hideModal();
                            supportForm.reset();
                        } else {
                            alert('Error: ' + data.message);
                        }
                    })
                    .catch(error => {
                        alert('Error de conexión');
                    })
                    .finally(() => {
                        submitBtn.innerHTML = 'Enviar';
                        submitBtn.disabled = false;
                    });
                }
            });
        }
    }

    // ==============================================
    // 3. Ajuste de Posición de Botones Flotantes
    // ==============================================
    const helpBtnFloat = document.querySelector('.help-btn');
    const whatsappBtnFloat = document.querySelector('.whatsapp-btn');

    function adjustFloatingButtons() {
        if (helpBtnFloat && whatsappBtnFloat && modal.style.display !== 'block') { // Solo ajustar si el modal no está visible
            const scrollPosition = window.scrollY;
            const viewportHeight = window.innerHeight;
            const bodyHeight = document.body.offsetHeight;
            const footerThreshold = 200;

            if (scrollPosition + viewportHeight > bodyHeight - footerThreshold) {
                helpBtnFloat.style.bottom = '140px';
                whatsappBtnFloat.style.bottom = '200px'; // Ajustado para mantener separación
            } else {
                helpBtnFloat.style.bottom = '40px';
                whatsappBtnFloat.style.bottom = '100px'; // Valor original del CSS
            }
        }
    }

    // Ejecutar al cargar y en cada scroll
    adjustFloatingButtons();
    window.addEventListener('scroll', adjustFloatingButtons);
});