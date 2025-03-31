class PositionIndicator {
    constructor() {
      this.tableBody = document.getElementById('tabla_usuarios_body');
      this.rowsDisplayed = document.getElementById('rows-displayed');
      this.rowsTotal = document.getElementById('rows-total');
      this.filterStatus = document.getElementById('filter-status');
      this.filterText = document.getElementById('filter-text');
      this.contextDetail = document.getElementById('context-detail');
      this.searchInput = document.getElementById('search_usuario');
      this.filterInputs = document.querySelectorAll('.filtro-campo');
      
      this.init();
    }
  
    init() {
      this.setupObservers();
      this.updateCounters();
      this.setupEventListeners();
    }
  
    setupObservers() {
      const observer = new MutationObserver(() => this.updateCounters());
      if (this.tableBody) {
        observer.observe(this.tableBody, {
          childList: true,
          subtree: true,
          attributes: true,
          attributeFilter: ['style', 'class']
        });
      }
    }
  
    setupEventListeners() {
      if (this.searchInput) {
        this.searchInput.addEventListener('input', () => this.updateCounters());
      }
  
      this.filterInputs.forEach(input => {
        input.addEventListener('input', () => this.updateCounters());
        input.addEventListener('change', () => this.updateCounters());
      });
    }
  
    updateCounters() {
      const allRows = this.tableBody.querySelectorAll('tr.fila-datos');
      const visibleRows = Array.from(allRows).filter(row => {
        return row.style.display !== 'none' && !row.classList.contains('d-none');
      });
  
      this.rowsTotal.textContent = allRows.length;
      this.rowsDisplayed.textContent = visibleRows.length;
  
      this.updateFilterStatus();
      this.updateContextMessage(visibleRows.length, allRows.length);
    }
  
    updateFilterStatus() {
      const hasSearch = this.searchInput && this.searchInput.value.trim() !== '';
      const hasFilters = Array.from(this.filterInputs).some(input => {
        return input.value !== '' && input.value !== null;
      });
  
      if (hasSearch || hasFilters) {
        this.filterStatus.className = 'filter-badge bg-info';
        this.filterText.textContent = 'Filtros aplicados';
      } else {
        this.filterStatus.className = 'filter-badge bg-secondary';
        this.filterText.textContent = 'Sin filtros';
      }
    }
  
    updateContextMessage(visible, total) {
      if (visible === 0 && total > 0) {
        this.contextDetail.textContent = 'No hay resultados que coincidan con los filtros aplicados';
      } else if (visible < total) {
        this.contextDetail.textContent = `Mostrando ${visible} de ${total} usuarios (filtrados)`;
      } else {
        this.contextDetail.textContent = `Mostrando todos los ${total} usuarios registrados`;
      }
    }
  }
  
  // Inicialización cuando el DOM esté listo
  document.addEventListener('DOMContentLoaded', () => {
    new PositionIndicator();
  });