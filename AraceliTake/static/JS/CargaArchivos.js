// CARGA DE ARCHIVOS
const fileInput = document.getElementById('file-input');
const uploadButton = document.getElementById('upload-button');
const dragDropArea = document.getElementById('drag-drop-area');
const uploadStatus = document.getElementById('upload-status');

// Botón para seleccionar archivos
uploadButton.addEventListener('click', () => {
    fileInput.click();
});

// Cambiar el estilo al arrastrar el archivo sobre la zona
dragDropArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    dragDropArea.classList.add('dragging');
});

// Quitar el estilo cuando se deja de arrastrar
dragDropArea.addEventListener('dragleave', () => {
    dragDropArea.classList.remove('dragging');
});

// Manejar la caída del archivo en la zona
dragDropArea.addEventListener('drop', (e) => {
    e.preventDefault();
    dragDropArea.classList.remove('dragging');
    const files = e.dataTransfer.files;
    handleFiles(files);
});

// Manejar la selección de archivos desde el input
fileInput.addEventListener('change', () => {
    const files = fileInput.files;
    handleFiles(files);
});

function handleFiles(files) {
    if (files.length > 0) {
        let fileNames = [];
        for (let i = 0; i < files.length; i++) {
            fileNames.push(files[i].name);
        }
        uploadStatus.textContent = `Se han cargado ${files.length} archivo(s): ${fileNames.join(', ')}`;
        uploadStatus.classList.remove('error');
        uploadStatus.classList.add('success');
    } else {
        uploadStatus.textContent = "Error: No se pudo cargar el archivo.";
        uploadStatus.classList.remove('success');
        uploadStatus.classList.add('error');
    }
}

// MANEJO DE ERRORES
document.getElementById('file-input').addEventListener('change', function(event) {
    const fileNames = Array.from(event.target.files).map(file => file.name);

    if (fileNames.length > 0) {
        uploadStatus.textContent = `Se han cargado ${fileNames.length} archivo(s): ${fileNames.join(', ')}`;
        uploadStatus.classList.remove('error');
        uploadStatus.classList.add('success');
    } else {
        uploadStatus.textContent = "Error: No se pudo cargar el archivo.";
        uploadStatus.classList.remove('success');
        uploadStatus.classList.add('error');
    }
});

document.getElementById('drag-drop-area').addEventListener('dragover', function(e) {
    e.preventDefault();
    this.classList.add('dragging');
});

document.getElementById('drag-drop-area').addEventListener('dragleave', function() {
    this.classList.remove('dragging');
});

document.getElementById('drag-drop-area').addEventListener('drop', function(e) {
    e.preventDefault();
    this.classList.remove('dragging');

    const files = e.dataTransfer.files;
    const fileInput = document.getElementById('file-input');
    fileInput.files = files;

    const fileNames = Array.from(files).map(file => file.name);

    if (fileNames.length > 0) {
        uploadStatus.textContent = `Se han cargado ${fileNames.length} archivo(s): ${fileNames.join(', ')}`;
        uploadStatus.classList.remove('error');
        uploadStatus.classList.add('success');
    } else {
        uploadStatus.textContent = "Error: No se pudo cargar el archivo.";
        uploadStatus.classList.remove('success');
        uploadStatus.classList.add('error');
    }
});

document.getElementById('upload-button').addEventListener('click', function() {
    document.getElementById('file-input').click();
});
// MANEJO DE ERRORES END

