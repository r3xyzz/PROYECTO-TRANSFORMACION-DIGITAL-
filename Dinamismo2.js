/ Hoja de JavaScript/

//Menu desplegable
document.addEventListener('DOMContentLoaded', function() {
    // Para el menú desplegable
    document.querySelector('.menu-btn').addEventListener('click', function() {
        document.querySelector('.menu-content').classList.toggle('show');
    });

    // Para mostrar la fecha actual
    function mostrarFecha() {
        var fecha = new Date();
        var opciones = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
        document.getElementById('fecha').innerHTML = fecha.toLocaleDateString('es-ES', opciones);
    }
    mostrarFecha();
});