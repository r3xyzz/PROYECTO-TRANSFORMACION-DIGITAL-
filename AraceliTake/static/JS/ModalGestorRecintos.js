document.addEventListener('DOMContentLoaded', function() {
    const modal = new bootstrap.Modal(document.getElementById('modalReserva'));
    const cells = document.querySelectorAll('.cell');
    const fechaInput = document.getElementById('fecha-dia');
    const horaInicioInput = document.getElementById('hora-inicio');
    const horaFinInput = document.getElementById('hora-fin');
    const popup = document.getElementById('popup');
    const closeBtn = document.querySelector('.close-btn');

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

            // Mostrar el modal de Bootstrap
            modal.show();

            //VALIDACIÓN DE HORAS SELECCIONABLES EN "HORA FIN"
            horaFinInput.addEventListener('input', function() {
                const horarioPermitido = [
                    '08:40', '09:20', '10:10', '10:50', '11:40',
                    '12:20', '13:10', '13:50', '14:40', '15:20',
                    '16:10', '16:50', '17:40', '18:20', '19:10',
                    '19:50', '20:40', '21:20', '22:10', '22:50', '23:30'
                ];
                
                const inputHorario = this.value;
                if (!horarioPermitido.includes(inputHorario)) {
                    this.setCustomValidity('Introduce un valor válido. Valores válidos son: ' + horarioPermitido.join(', '));
                } else {
                    this.setCustomValidity(''); // Elimina cualquier mensaje de error si la entrada es válida
                }
            });
        });
    });

    // Mostrar el pop-up al enviar el formulario
    document.querySelector('#modalReserva form').addEventListener('submit', function(event) {
        event.preventDefault(); // Evita que el formulario se envíe y recargue la página

        // Ocultar el modal
        modal.hide();

        // Mostrar el pop-up
        popup.style.display = 'block';
    });

    // Cerrar el pop-up cuando se haga clic en el botón de cerrar
    closeBtn.addEventListener('click', function() {
        popup.style.display = 'none';
    });
});
