const header = document.querySelector('header');
const aside = document.querySelector('aside');
const footer = document.querySelector('footer');



header.innerHTML = `
<nav class="navbar navbar-dark navbar-expand-md">
                <div class="container-fluid ms-4 me-4">
                    <a class="me-5" href="#">
                        <img class="navImg" src="imagenes/logo-duoc.png" alt="DuocUc"></img>
                    </a>
                    <div class="d-flex align-items-center ms-auto">
                        <img class="user-photo me-2 ms-1" src="imagenes/foto-logo.png" alt="Foto de Usuario">
                        <span class="user-name">Admin. Departamento Docencia</span>
                    </div>
                </div>
            </nav>
`;

footer.innerHTML = `
&copy; 2024 - Duoc UC - Todos los derechos reservados
`;

aside.innerHTML = `
<div style="text-align: center;">
                Jueves, 18 de Mayo
            </div>
            <hr>
            <a href="#" class="sidebar-item">
                <i class="bi bi-file-earmark-arrow-up-fill"></i>
                Carga de Archivos
            </a>
            <a href="#"  class="sidebar-item">
                <i class="bi bi-file-earmark-bar-graph-fill"></i>
                Reportes y Dashboards
            </a>
            <a href="#"  class="sidebar-item">
                <i class="bi bi-calendar-week-fill"></i> 
                Gestión de Reservas
            </a>
            <hr>
            <a href="#"  class="sidebar-item">
                <i class="bi bi-person-fill-add"></i>
                Creación de Usuarios
            </a>
            <a href="#" class="sidebar-item">
                <i class="bi bi-people-fill"></i>
                Administración de Usuarios
            </a>
`;




