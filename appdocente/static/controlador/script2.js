const daysElement = $('#days');
const monthYearElement = $('#monthYear');
const prevMonthButton = $('#prevMonth');
const nextMonthButton = $('#nextMonth');
const scheduleElement = $('#schedule tbody');
const weekRangeElement = $('#weekRange');
const cloud = $("#cloud");
const barraLateral = $(".barra-lateral");
const spans = $("span");
const palanca = $(".switch");
const circulo = $(".circulo");
const menu = $(".menu");
const main = $("main");

let selectedDate = new Date();
let modalInstance;
let reservas = [];
let selectedSalaId = null;

// Cargar las reservas desde el HTML al cargar el DOM
$(document).ready(function () {
    // El código existente para inicializar el calendario y reservas
    try {
        reservas = JSON.parse($('#reservas-data').text());
    } catch (error) {
        console.error('Error al cargar las reservas:', error);
    }

    // renderCalendar(selectedDate);
    // displayWeek(startOfWeek(selectedDate));

    // ---------------------------
    // Manejo de Carga de Archivos
    // ---------------------------
    const uploadButton = $('#upload-button');
    const fileInput = $('#file-input');
    const dragDropArea = $('#drag-drop-area');
    const uploadForm = $('#upload-form');

    // Manejar clic en el botón de selección
    if (uploadButton.length) {
        uploadButton.on('click', function () {
            fileInput.click();  // Abre el selector de archivos
        });
    }

    // Mostrar nombre de archivo seleccionado
    if (fileInput.length) {
        fileInput.on('change', function () {
            if (fileInput[0].files.length > 0) {
                $('#upload-status').text(`Archivo seleccionado: ${fileInput[0].files[0].name}`);
            }
        });
    }

    // Manejar arrastrar y soltar archivos
    if (dragDropArea.length) {
        dragDropArea.on('dragover', function (event) {
            event.preventDefault();
            dragDropArea.addClass('drag-over');
        });

        dragDropArea.on('dragleave', function () {
            dragDropArea.removeClass('drag-over');
        });

        dragDropArea.on('drop', function (event) {
            event.preventDefault();
            dragDropArea.removeClass('drag-over');

            if (event.originalEvent.dataTransfer.files.length > 0) {
                fileInput[0].files = event.originalEvent.dataTransfer.files;  // Asigna los archivos seleccionados
                $('#upload-status').text(`Archivo arrastrado: ${fileInput[0].files[0].name}`);
            }
        });
    }

    // Subir archivo al hacer clic en el botón de enviar
    if (uploadForm.length) {
        uploadForm.on('submit', function (event) {
            if (fileInput[0].files.length === 0) {
                event.preventDefault();  // Evita enviar el formulario si no hay archivo seleccionado
                alert('Por favor, selecciona un archivo antes de subir.');
            }
        });
    }
});

// Función para renderizar el calendario con los días del mes actual
function renderCalendar(date) {
    daysElement.empty();
    monthYearElement.text(date.toLocaleDateString('es-ES', { month: 'long', year: 'numeric' }));

    const firstDayOfMonth = new Date(date.getFullYear(), date.getMonth(), 1).getDay();
    const daysInMonth = new Date(date.getFullYear(), date.getMonth() + 1, 0).getDate();

    let currentDay = 1 - (firstDayOfMonth === 0 ? 6 : firstDayOfMonth - 1);
    for (let i = 0; i < 42; i++) {
        const dayElement = $('<span></span>');
        if (currentDay > 0 && currentDay <= daysInMonth) {
            dayElement.text(currentDay);
            const dayDate = new Date(date.getFullYear(), date.getMonth(), currentDay);
            if (dayDate.toDateString() === selectedDate.toDateString()) {
                dayElement.addClass('selected');
            }
            dayElement.on('click', () => {
                selectedDate = dayDate;
                renderCalendar(date);
                displayWeek(startOfWeek(dayDate));
            });
        }
        daysElement.append(dayElement);
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
    scheduleElement.empty();
    const weekDates = getWeekDates(new Date(weekStartDate));
    weekRangeElement.text(`Semana del ${weekDates[0].toLocaleDateString('es-ES')} al ${weekDates[5].toLocaleDateString('es-ES')}`);

    const times = [
        "08:01 - 08:40", "08:41 - 09:20", "09:31 - 10:10", "10:11 - 10:50",
        "11:01 - 11:40", "11:41 - 12:20", "12:31 - 13:10", "13:11 - 13:50",
        "14:01 - 14:40", "14:41 - 15:20", "15:31 - 16:10", "16:11 - 16:50",
        "17:01 - 17:40", "17:41 - 18:20", "18:31 - 19:10", "19:11 - 19:50",
        "20:01 - 20:40", "20:41 - 21:20", "21:31 - 22:10", "22:11 - 22:50",
        "22:51 - 23:30"
    ];

    times.forEach(time => {
        const row = $('<tr></tr>');

        const timeCell = $('<td></td>').text(time);
        row.append(timeCell);

        weekDates.forEach((date, index) => {
            if (index < 6) {
                const dayCell = $('<td></td>').addClass('cell').attr('data-day', date.toISOString().split('T')[0]).attr('data-time', time);

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
                        dayCell.text(reserva.nombre_evento);
                        dayCell.addClass('reserved-cell');
                    }
                });

                row.append(dayCell);
            }
        });

        scheduleElement.append(row);
    });

    assignClickEventsToCells();
}

// Asignar eventos de clic a las celdas para abrir el modal de reserva
function assignClickEventsToCells() {
    const cells = $('.cell');
    modalInstance = new bootstrap.Modal($('#modalReserva')[0], {
        keyboard: false,
        backdrop: 'static'
    });
    const fechaInput = $('#fecha-ini');
    const horaInicioInput = $('#hora-inicio');
    const horaFinInput = $('#hora-fin');
    const salaInput = $('#sala');

    cells.each(function () {
        $(this).on('click', function () {
            if ($(this).hasClass('reserved-cell')) {
                alert('Este bloque de horario ya está reservado y no se pueden agregar más eventos.');
                return;
            }

            const day = $(this).attr('data-day');
            const time = $(this).attr('data-time');

            const date = new Date(day);
            if (!isNaN(date)) {
                fechaInput.val(date.toISOString().split('T')[0]);
            }

            const timeParts = time ? time.split(' - ') : [];
            if (timeParts.length === 2) {
                horaInicioInput.val(timeParts[0]);
                horaFinInput.val(timeParts[1]);
            }

            if (salaInput.length && selectedSalaId !== null) {
                const salaName = $(`[data-sala-id="${selectedSalaId}"] h2`).text();
                salaInput.val(salaName);
            }

            modalInstance.show();
        });
    });

    $('#modalReserva').on('hidden.bs.modal', function () {
        horaInicioInput.val('');
        horaFinInput.val('');
    });
}

// Manejar la selección de la sala
function selectSala(salaId) {
    selectedSalaId = salaId; // Guardar el ID de la sala seleccionada
    const salasElement = $('#salas');
    const containerElement = $('#container');
    const selectedSalaHeader = $('#selectedSalaHeader');
    const salaInput = $('#sala');
    const salaIdInput = $('#sala-id'); // Campo oculto para el ID de la sala

    if (salasElement.length) {
        salasElement.hide(); // Oculta la lista de salas
    }

    if (containerElement.length) {
        containerElement.show(); // Muestra el contenedor del horario
    }

    // Obtiene el nombre de la sala seleccionada y lo muestra
    const salaNameElement = $(`[data-sala-id="${salaId}"] h2`);
    const modalSalaNameElement = $('#modalSalaName');

    if (salaNameElement.length && selectedSalaHeader.length && modalSalaNameElement.length) {
        const salaName = salaNameElement.text();
        selectedSalaHeader.text(`Sala: ${salaName}`);
        modalSalaNameElement.text(salaName);

        // Rellena automáticamente el campo de sala en el formulario
        if (salaInput.length) {
            salaInput.val(salaName); // Cambia al nombre de la sala seleccionada
        }

        // Rellena el campo oculto con el ID de la sala seleccionada
        if (salaIdInput.length) {
            salaIdInput.val(salaId); // Cambia al ID de la sala seleccionada
        }
    }

    // Filtrar el horario por la sala seleccionada
    $.getJSON(`/api/horario/${salaId}`)
        .done(data => {
            reservas = data.reservas; // Actualiza las reservas solo con la sala seleccionada
            renderCalendar(selectedDate);
            displayWeek(startOfWeek(selectedDate));
        })
        .fail(error => {
            console.error('Error al cargar el horario:', error);
        });
}

// Navegación del calendario entre meses
prevMonthButton.on('click', () => {
    selectedDate.setMonth(selectedDate.getMonth() - 1);
    renderCalendar(selectedDate);
});

nextMonthButton.on('click', () => {
    selectedDate.setMonth(selectedDate.getMonth() + 1);
    renderCalendar(selectedDate);
});