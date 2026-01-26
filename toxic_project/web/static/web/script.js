// ===============================================
// 1. ELEMENTOS DEL DOM
// ===============================================
const header = document.querySelector("header");
const hamburger = document.querySelector(".hamburger");
const navMenu = document.querySelector(".nav-menu");

// ===============================================
// 2. LÓGICA DE INTERFAZ (UI)
// ===============================================

// Evento Scroll
if (header) {
    window.addEventListener("scroll", () => {
        if (window.scrollY > 50) {
            header.classList.add("scrolled");
        } else {
            header.classList.remove("scrolled");
        }
    });
}

// Toggle Menú Móvil
if (hamburger && navMenu) {
    hamburger.addEventListener("click", () => {
        hamburger.classList.toggle("active");
        navMenu.classList.toggle("active");
    });

    document.querySelectorAll(".nav-link").forEach(n => n.addEventListener("click", () => {
        hamburger.classList.remove("active");
        navMenu.classList.remove("active");
    }));
}

// ===============================================
// 3. SISTEMA DE TRADUCCIÓN (I18N)
// ===============================================

const translations = {
    es: {
        // NAV
        nav_home: "Inicio",
        nav_about: "Nosotros",
        nav_events: "Eventos",
        nav_login: "Ingresar",
        // HERO
        hero_title: "¡Sé parte de nuestra comunidad!",
        hero_btn: "Unirme al Discord",
        // ORIGEN
        origin_title: "El Origen de Toxic Under Groove",
        origin_text: "Todo comenzó con un grupo de amigos cansados de la monotonía. Lo que empezó como unas simples partidas nocturnas se transformó en una hermandad. Hoy somos una comunidad consolidada buscando crear un espacio donde la competitividad y la diversión van de la mano.",
        // STAFF
        staff_title: "Nuestros Referentes",
        role_admin: "Administrador & Desarollador",
        role_team_leader: "Líder de Clan",
        role_clan_co_leader: "Colíder",
        // ROTACIÓN JUEGOS
        rotation_title: "Nuestra Rotación",
        rotation_subtitle: "Además de desarrollar, competimos y nos divertimos en:",
        game_core: "Servidores Privados",
        game_comp: "Competitivo",
        game_ranked: "Clasificatorio",
        game_waiting: "Esperando Lanzamiento",
        game_fornite: "Cero Construcción",
        // PROYECTOS
        projects_title: "Nuestros Proyectos",
        proj_l2_title: "⚔️ Próximamente: Lineage 2",
        proj_l2_desc: "Estamos desarrollando nuestro propio servidor Crónica High Five (H5).",
        proj_l2_feat1: "🔹 Files Java PTS (Mecánicas retail)",
        proj_l2_feat2: "🔹 Estabilidad garantizada",
        proj_l2_feat3: "🔹 Comunidad competitiva",
        proj_l2_status: "🛠️ En construcción",
        proj_tourney_title: "🏆 Torneos Semanales",
        proj_tourney_desc: "Organizamos copas todos los fines de semana con premios exclusivos para la comunidad.",
        proj_giveaway_title: "📢 Sorteos y Eventos",
        proj_giveaway_desc: "Participa en sorteos mensuales de items, cuentas premium y merchandising oficial.",
        // FOOTER
        footer_copy: "© 2026 Toxic Under Groove. Todos los derechos reservados.",
        
        // --- LOGIN (SIMPLIFICADO) ---
        login_title: "ACCESO",
        login_user_label: "USUARIO",
        login_user_ph: "Tu usuario...",
        login_pass_label: "CONTRASEÑA",
        login_pass_ph: "••••••",
        login_btn: "INGRESAR",
        login_back: "Volver a la portada",
        login_error: "Error de credenciales."
    },
    en: {
        // NAV
        nav_home: "Home",
        nav_about: "About Us",
        nav_events: "Events",
        nav_login: "Login",
        // HERO
        hero_title: "Be part of our community!",
        hero_btn: "Join Discord",
        // ORIGEN
        origin_title: "The Origin of Toxic Under Groove",
        origin_text: "It all started with a group of friends tired of monotony. What began as simple late-night games transformed into a brotherhood. Today we are a consolidated community looking to create a space where competitiveness and fun go hand in hand.",
        // STAFF
        staff_title: "Our Staff",
        role_admin: "Admin & Developer",
        role_team_leader: "Clan Leader",
        role_clan_co_leader: "Co-Leader",
        // ROTACIÓN JUEGOS
        rotation_title: "Our Rotation",
        rotation_subtitle: "Besides developing, we compete and have fun in:",
        game_core: "Private Servers",
        game_comp: "Competitive",
        game_ranked: "Ranked",
        game_waiting: "Waiting For Release",
        game_fornite: "Zero Build",
        // PROYECTOS
        projects_title: "Our Projects",
        proj_l2_title: "⚔️ Coming Soon: Lineage 2",
        proj_l2_desc: "We are developing our own High Five (H5) Chronicle server.",
        proj_l2_feat1: "🔹 Java PTS Files (Retail mechanics)",
        proj_l2_feat2: "🔹 Guaranteed stability",
        proj_l2_feat3: "🔹 Competitive community",
        proj_l2_status: "🛠️ Under Construction",
        proj_tourney_title: "🏆 Weekly Tournaments",
        proj_tourney_desc: "We organize cups every weekend with exclusive prizes for the community.",
        proj_giveaway_title: "📢 Giveaways and Events",
        proj_giveaway_desc: "Participate in monthly giveaways for items, premium accounts, and official merchandise.",
        // FOOTER
        footer_copy: "© 2026 Toxic Under Groove. All rights reserved.",

        // --- LOGIN (SIMPLIFIED) ---
        login_title: "LOGIN",
        login_user_label: "USERNAME",
        login_user_ph: "Your username...",
        login_pass_label: "PASSWORD",
        login_pass_ph: "••••••",
        login_btn: "ENTER",
        login_back: "Back to home",
        login_error: "Invalid credentials."
    }
};

// ===============================================
// 4. FUNCIÓN PRINCIPAL DE CAMBIO DE IDIOMA
// ===============================================
window.setLanguage = function(lang, element) {
    // 1. Guardar preferencia
    localStorage.setItem('toxic_lang', lang);

    // 2. Cambiar textos buscando elementos con 'data-i18n'
    const elements = document.querySelectorAll('[data-i18n]');
    elements.forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (translations[lang] && translations[lang][key]) {
            // DETECCIÓN INTELIGENTE
            if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
                el.placeholder = translations[lang][key];
            } else {
                el.textContent = translations[lang][key];
            }
        }
    });

    // 3. Actualizar estilo visual de las banderas
    document.querySelectorAll('.flag-btn').forEach(flag => {
        flag.classList.remove('active');
        if(flag.getAttribute('onclick') && flag.getAttribute('onclick').includes(lang)) {
            flag.classList.add('active');
        }
    });
};

// --- AUTO-INICIO ---
document.addEventListener('DOMContentLoaded', () => {
    const savedLang = localStorage.getItem('toxic_lang') || 'es';
    setLanguage(savedLang, null);
});