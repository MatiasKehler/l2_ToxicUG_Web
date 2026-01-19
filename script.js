const header = document.querySelector("header");
const hamburger = document.querySelector(".hamburger");
const navMenu = document.querySelector(".nav-menu");

// Evento Scroll: Cambia el diseño del header al bajar
window.addEventListener("scroll", () => {
    // Si bajamos más de 50px, agregamos la clase "scrolled"
    if (window.scrollY > 50) {
        header.classList.add("scrolled");
    } else {
        // Si volvemos arriba, quitamos la clase (vuelve al estado original)
        header.classList.remove("scrolled");
        
        // Opcional: Cerrar menú automáticamente al volver arriba
        // hamburger.classList.remove("active");
        // navMenu.classList.remove("active");
    }
});

// Toggle Menú: Abrir/Cerrar al hacer click en la hamburguesa
hamburger.addEventListener("click", () => {
    hamburger.classList.toggle("active");
    navMenu.classList.toggle("active");
});

// Cerrar menú al hacer click en un enlace (Mejora la UX)
document.querySelectorAll(".nav-link").forEach(n => n.addEventListener("click", () => {
    hamburger.classList.remove("active");
    navMenu.classList.remove("active");
}));