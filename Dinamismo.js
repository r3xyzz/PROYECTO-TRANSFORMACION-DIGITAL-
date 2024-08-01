/ Hoja de JavaScript/


// Para mostrar la fecha actual
function mostrarFecha() {
    var fecha = new Date();
    var opciones = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    document.getElementById('fecha').innerHTML = fecha.toLocaleDateString('es-ES', opciones);
}
mostrarFecha();
