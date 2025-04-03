document.addEventListener("DOMContentLoaded", function() {
    // ==============================================
    // 1. Animación de Texto Principal
    // ==============================================
    gsap.registerPlugin(TextPlugin);
    gsap.set("#animated-text", { text: "", opacity: 0 });
    gsap.to("#animated-text", {
        duration: 2,
        opacity: 1,
        text: "TAMALES EL BUEN SAZÓN",
        ease: "power2.out",
        delay: 0.5
    });

    // ==============================================
    // 2. Comportamiento del Menú al Hacer Scroll
    // ==============================================
    const menu = document.querySelector('.menu');
    window.addEventListener('scroll', function() {
        const scrollPosition = window.scrollY;
        menu.classList.toggle('scrolled', scrollPosition > 50);
    });

    // ==============================================
    // 3. Funcionalidad del Modal de Ayuda
    // ==============================================
    const helpBtn = document.querySelector('.help-btn');
    const whatsappBtn = document.querySelector('.whatsapp-btn');
    const modal = document.getElementById('help-modal');
    const closeModal = document.querySelector('.close-modal');
    const cancelBtn = document.querySelector('.btn-cancel'); // Selecciona el botón "Cancelar"

    // Mostrar modal
    helpBtn.addEventListener('click', function(e) {
        e.preventDefault();
        modal.style.display = 'block';
    });

    // Cerrar modal con la "X"
    closeModal.addEventListener('click', function() {
        modal.style.display = 'none';
    });

    // Cerrar modal con el botón "Cancelar"
    cancelBtn.addEventListener('click', function() {
        modal.style.display = 'none';
    });

    // Cerrar al hacer click fuera del modal
    window.addEventListener('click', function(e) {
        if (e.target === modal) {
            modal.style.display = 'none';
        }
    });

    // ==============================================
    // 4. Ajuste de Posición de Botones Flotantes
    // ==============================================
    function adjustFloatingButtons() {
        const scrollPosition = window.scrollY;
        const viewportHeight = window.innerHeight;
        const bodyHeight = document.body.offsetHeight;
        const footerThreshold = 200;

        if (scrollPosition + viewportHeight > bodyHeight - footerThreshold) {
            helpBtn.style.bottom = '140px';
            whatsappBtn.style.bottom = '100px';
        } else {
            helpBtn.style.bottom = '40px';
            whatsappBtn.style.bottom = '40px';
        }
    }

    // Ejecutar al cargar y en cada scroll
    adjustFloatingButtons();
    window.addEventListener('scroll', adjustFloatingButtons);

    // ==============================================
    // 5. Envío del Formulario de Soporte
    // ==============================================
    document.getElementById('support-form').addEventListener('submit', function(e) {
        e.preventDefault();
        
        const formData = {
            nombre: document.getElementById('nombre').value,
            email: document.getElementById('email').value,
            asunto: document.getElementById('asunto').value,
            mensaje: document.getElementById('mensaje').value
        };

        const submitBtn = document.querySelector('.btn-submit');
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
                modal.style.display = 'none';
                this.reset();
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
    });

    // ==============================================
    // 6. Inicialización de AOS (Animate On Scroll)
    // ==============================================
    AOS.init({
        duration: 1000,
        once: false,
        easing: 'ease-in-out',
        mirror: true
    });
});