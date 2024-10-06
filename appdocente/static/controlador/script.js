const daysElement = document.getElementById('days');
const monthYearElement = document.getElementById('monthYear');
const prevMonthButton = document.getElementById('prevMonth');
const nextMonthButton = document.getElementById('nextMonth');
const scheduleElement = document.querySelector('#schedule tbody');
const weekRangeElement = document.getElementById('weekRange');
const cloud = document.getElementById("cloud");
const barraLateral = document.querySelector(".barra-lateral");
const spans = document.querySelectorAll("span");
const palanca = document.querySelector(".switch");
const circulo = document.querySelector(".circulo");
const menu = document.querySelector(".menu");
const main = document.querySelector("main");


let selectedDate = new Date();
let modalInstance;
let reservas = [];
let selectedSalaId = null;

// Cargar las reservas desde el HTML al cargar el DOM
document.addEventListener('DOMContentLoaded', function () {
    // El código existente para inicializar el calendario y reservas
    try {
        reservas = JSON.parse(document.getElementById('reservas-data').textContent);
    } catch (error) {
        console.error('Error al cargar las reservas:', error);
    }

    // renderCalendar(selectedDate);
    // displayWeek(startOfWeek(selectedDate));

    // ---------------------------
    // Manejo de Carga de Archivos
    // ---------------------------
    const uploadButton = document.getElementById('upload-button');
    const fileInput = document.getElementById('file-input');
    const dragDropArea = document.getElementById('drag-drop-area');
    const uploadForm = document.getElementById('upload-form');

    // Manejar clic en el botón de selección
    if (uploadButton) {
        uploadButton.addEventListener('click', function () {
            fileInput.click();  // Abre el selector de archivos
        });
    }

    // Mostrar nombre de archivo seleccionado
    if (fileInput) {
        fileInput.addEventListener('change', function () {
            if (fileInput.files.length > 0) {
                document.getElementById('upload-status').innerText = `Archivo seleccionado: ${fileInput.files[0].name}`;
            }
        });
    }

    // Manejar arrastrar y soltar archivos
    if (dragDropArea) {
        dragDropArea.addEventListener('dragover', function (event) {
            event.preventDefault();
            dragDropArea.classList.add('drag-over');
        });

        dragDropArea.addEventListener('dragleave', function () {
            dragDropArea.classList.remove('drag-over');
        });

        dragDropArea.addEventListener('drop', function (event) {
            event.preventDefault();
            dragDropArea.classList.remove('drag-over');

            if (event.dataTransfer.files.length > 0) {
                fileInput.files = event.dataTransfer.files;  // Asigna los archivos seleccionados
                document.getElementById('upload-status').innerText = `Archivo arrastrado: ${fileInput.files[0].name}`;
            }
        });
    }

    // Subir archivo al hacer clic en el botón de enviar
    if (uploadForm) {
        uploadForm.addEventListener('submit', function (event) {
            if (fileInput.files.length === 0) {
                event.preventDefault();  // Evita enviar el formulario si no hay archivo seleccionado
                alert('Por favor, selecciona un archivo antes de subir.');
            }
        });
    }
});

// Función para renderizar el calendario con los días del mes actual
function renderCalendar(date) {
    daysElement.innerHTML = '';
    monthYearElement.textContent = date.toLocaleDateString('es-ES', { month: 'long', year: 'numeric' });

    const firstDayOfMonth = new Date(date.getFullYear(), date.getMonth(), 1).getDay();
    const daysInMonth = new Date(date.getFullYear(), date.getMonth() + 1, 0).getDate();

    let currentDay = 1 - (firstDayOfMonth === 0 ? 6 : firstDayOfMonth - 1);
    for (let i = 0; i < 42; i++) {
        const dayElement = document.createElement('span');
        if (currentDay > 0 && currentDay <= daysInMonth) {
            dayElement.textContent = currentDay;
            const dayDate = new Date(date.getFullYear(), date.getMonth(), currentDay);
            if (dayDate.toDateString() === selectedDate.toDateString()) {
                dayElement.classList.add('selected');
            }
            dayElement.addEventListener('click', () => {
                selectedDate = dayDate;
                renderCalendar(date);
                displayWeek(startOfWeek(dayDate));
            });
        }
        daysElement.appendChild(dayElement);
        currentDay++;
    }

    assignClickEventsToCells();
}

// Obtener el inicio de la semana (lunes)
function startOfWeek(date) {
    const day = date.getDay();
    const diff = date.getDate() - day + (day === 0 ? -6 : 1);
    return new Date(date.setDate(diff));
}

// Obtener las fechas de una semana a partir de una fecha de inicio
function getWeekDates(start) {
    let dates = [];
    for (let i = 0; i < 7; i++) {
        dates.push(new Date(start));
        start.setDate(start.getDate() + 1);
    }
    return dates;
}

// Mostrar la semana seleccionada en el horario
function displayWeek(weekStartDate) {
    scheduleElement.innerHTML = '';
    const weekDates = getWeekDates(new Date(weekStartDate));
    weekRangeElement.textContent = `Semana del ${weekDates[0].toLocaleDateString('es-ES')} al ${weekDates[5].toLocaleDateString('es-ES')}`;

    const times = [
        "08:01 - 08:40", "08:41 - 09:20", "09:31 - 10:10", "10:11 - 10:50",
        "11:01 - 11:40", "11:41 - 12:20", "12:31 - 13:10", "13:11 - 13:50",
        "14:01 - 14:40", "14:41 - 15:20", "15:31 - 16:10", "16:11 - 16:50",
        "17:01 - 17:40", "17:41 - 18:20", "18:31 - 19:10", "19:11 - 19:50",
        "20:01 - 20:40", "20:41 - 21:20", "21:31 - 22:10", "22:11 - 22:50",
        "22:51 - 23:30"
    ];

    times.forEach(time => {
        const row = document.createElement('tr');

        const timeCell = document.createElement('td');
        timeCell.textContent = time;
        row.appendChild(timeCell);

        weekDates.forEach((date, index) => {
            if (index < 6) {
                const dayCell = document.createElement('td');
                dayCell.classList.add('cell');
                dayCell.setAttribute('data-day', date.toISOString().split('T')[0]);
                dayCell.setAttribute('data-time', time);

                reservas.forEach(reserva => {
                    const reservaFecha = reserva.fecha_inicio;
                    const reservaHoraInicio = reserva.hora_inicio;
                    const reservaHoraFin = reserva.hora_fin;

                    const startDate = new Date(`${reservaFecha}T${reservaHoraInicio}`);
                    const endDate = new Date(`${reservaFecha}T${reservaHoraFin}`);

                    const [startBlock, endBlock] = time.split(' - ');
                    const blockStart = new Date(`${reservaFecha}T${startBlock}`);
                    const blockEnd = new Date(`${reservaFecha}T${endBlock}`);

                    if (
                        date.toISOString().split('T')[0] === reservaFecha &&
                        ((blockStart >= startDate && blockStart < endDate) || (blockEnd > startDate && blockEnd <= endDate))
                    ) {
                        dayCell.textContent = reserva.nombre_evento;
                        dayCell.classList.add('reserved-cell');
                    }
                });

                row.appendChild(dayCell);
            }
        });

        scheduleElement.appendChild(row);
    });

    assignClickEventsToCells();
}

// Asignar eventos de clic a las celdas para abrir el modal de reserva
function assignClickEventsToCells() {
    const cells = document.querySelectorAll('.cell');
    modalInstance = new bootstrap.Modal(document.getElementById('modalReserva'), {
        keyboard: false,
        backdrop: 'static'
    });
    const fechaInput = document.getElementById('fecha-ini');
    const horaInicioInput = document.getElementById('hora-inicio');
    const horaFinInput = document.getElementById('hora-fin');
    const salaInput = document.getElementById('sala');

    cells.forEach(cell => {
        cell.addEventListener('click', function () {
            if (cell.classList.contains('reserved-cell')) {
                alert('Este bloque de horario ya está reservado y no se pueden agregar más eventos.');
                return;
            }

            const day = cell.getAttribute('data-day');
            const time = cell.getAttribute('data-time');

            const date = new Date(day);
            if (!isNaN(date)) {
                fechaInput.value = date.toISOString().split('T')[0];
            }

            const timeParts = time ? time.split(' - ') : [];
            if (timeParts.length === 2) {
                horaInicioInput.value = timeParts[0];
                horaFinInput.value = timeParts[1];
            }

            if (salaInput && selectedSalaId !== null) {
                const salaName = document.querySelector(`[data-sala-id="${selectedSalaId}"] h2`).textContent;
                salaInput.value = salaName;
            }

            modalInstance.show();
        });
    });

    document.getElementById('modalReserva').addEventListener('hidden.bs.modal', function () {
        horaInicioInput.value = '';
        horaFinInput.value = '';
    });
}

// Manejar la selección de la sala
function selectSala(salaId) {
    selectedSalaId = salaId; // Guardar el ID de la sala seleccionada
    const salasElement = document.getElementById('salas');
    const containerElement = document.getElementById('container');
    const selectedSalaHeader = document.getElementById('selectedSalaHeader');
    const salaInput = document.getElementById('sala');
    const salaIdInput = document.getElementById('sala-id'); // Campo oculto para el ID de la sala

    if (salasElement) {
        salasElement.style.display = 'none'; // Oculta la lista de salas
    }

    if (containerElement) {
        containerElement.style.display = 'block'; // Muestra el contenedor del horario
    }

    // Obtiene el nombre de la sala seleccionada y lo muestra
    const salaNameElement = document.querySelector(`[data-sala-id="${salaId}"] h2`);
    const modalSalaNameElement = document.getElementById('modalSalaName');

    if (salaNameElement && selectedSalaHeader && modalSalaNameElement) {
        const salaName = salaNameElement.textContent;
        selectedSalaHeader.textContent = `Sala: ${salaName}`;
        modalSalaNameElement.textContent = salaName;

        // Rellena automáticamente el campo de sala en el formulario
        if (salaInput) {
            salaInput.value = salaName; // Cambia al nombre de la sala seleccionada
        }

        // Rellena el campo oculto con el ID de la sala seleccionada
        if (salaIdInput) {
            salaIdInput.value = salaId; // Cambia al ID de la sala seleccionada
        }
    }

    // Filtrar el horario por la sala seleccionada
    fetch(`/api/horario/${salaId}`)
        .then(response => response.json())
        .then(data => {
            reservas = data.reservas; // Actualiza las reservas solo con la sala seleccionada
            renderCalendar(selectedDate);
            displayWeek(startOfWeek(selectedDate));
        })
        .catch(error => {
            console.error('Error al cargar el horario:', error);
        });
}



// Navegación del calendario entre meses
prevMonthButton.addEventListener('click', () => {
    selectedDate.setMonth(selectedDate.getMonth() - 1);
    renderCalendar(selectedDate);
});

nextMonthButton.addEventListener('click', () => {
    selectedDate.setMonth(selectedDate.getMonth() + 1);
    renderCalendar(selectedDate);
});
