// JavaScript para manejar el modal
document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('modal');
    const closeBtn = document.querySelector('.close-btn');
    const cells = document.querySelectorAll('.cell');
    const fechaInput = document.getElementById('fecha-dia');
    const horaInicioInput = document.getElementById('hora-inicio');
    const horaFinInput = document.getElementById('hora-fin');

    // Abrir modal cuando se hace clic en una celda
    cells.forEach(cell => {
        cell.addEventListener('click', function() {
            const day = cell.getAttribute('data-day'); // Obtener el valor de data-day
            const time = cell.getAttribute('data-time'); // Obtener el valor de data-time
            console.log("Celda seleccionada:", { day, time }); // Mostrar valores en la consola
            
            if (day) {
                fechaInput.value = day;  // Asignar el día al campo de fecha
            } else {
                console.error('El atributo data-day no está definido para esta celda.');
            }
            
            const timeParts = time ? time.split(' - ') : [];
            if (timeParts.length === 2) {
                horaInicioInput.value = timeParts[0];
                horaFinInput.value = timeParts[1];
            } else {
                console.error('El formato de data-time no es correcto.');
            }

            modal.style.display = 'block';
        });
    });

    // Cerrar modal cuando se hace clic en el botón de cerrar
    closeBtn.addEventListener('click', function() {
        modal.style.display = 'none';
    });

    // Cerrar modal cuando se hace clic fuera del contenido del modal
    window.addEventListener('click', function(event) {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    });
});
