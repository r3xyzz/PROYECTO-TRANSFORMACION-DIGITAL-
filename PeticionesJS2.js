
    function filterTable(status) {
        // Ocultar todas las filas
        var rows = document.querySelectorAll('tbody tr');
        rows.forEach(function(row) {
            row.style.display = 'none';
        });

        // Mostrar solo las filas que coincidan con el estado seleccionado
        var selectedRows = document.querySelectorAll('tbody tr.' + status);
        selectedRows.forEach(function(row) {
            row.style.display = '';
        });
    }
