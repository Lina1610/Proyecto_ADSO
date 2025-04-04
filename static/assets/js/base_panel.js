// ========== FUNCIONALIDAD DEL MODAL DE AYUDA ==========
document.addEventListener('DOMContentLoaded', function() {
    // Modal de ayuda
    const helpButton = document.getElementById('helpButton');
    const helpModal = document.getElementById('helpModal');
    const closeHelp = document.getElementsByClassName('close-help')[0];
    
    if (helpButton) {
      helpButton.addEventListener('click', function(e) {
        e.preventDefault();
        helpModal.style.display = "block";
      });
    }
    
    if (closeHelp) {
      closeHelp.addEventListener('click', function() {
        helpModal.style.display = "none";
      });
    }
    
    window.addEventListener('click', function(event) {
      if (event.target == helpModal) {
        helpModal.style.display = "none";
      }
    });
  
    // ========== FUNCIONALIDAD DEL MODO OSCURO ==========
    const darkModeToggle = document.getElementById('darkModeToggle');
    if (darkModeToggle) {
      // Verificar preferencia del usuario
      const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
      const savedMode = localStorage.getItem('darkMode');
      
      if (savedMode === 'dark' || (prefersDark && savedMode !== 'light')) {
        document.body.classList.add('dark-mode');
        darkModeToggle.innerHTML = '<i class="fas fa-sun"></i>';
      }
  
      darkModeToggle.addEventListener('click', function(e) {
        e.preventDefault();
        document.body.classList.toggle('dark-mode');
        
        if (document.body.classList.contains('dark-mode')) {
          darkModeToggle.innerHTML = '<i class="fas fa-sun"></i>';
          localStorage.setItem('darkMode', 'dark');
        } else {
          darkModeToggle.innerHTML = '<i class="fas fa-moon"></i>';
          localStorage.setItem('darkMode', 'light');
        }
      });
    }
  
    // ========== INICIALIZACIÓN DE COMPONENTES ==========
    // Puedes añadir aquí inicializaciones adicionales que necesites
    console.log('Panel administrativo inicializado');
  });