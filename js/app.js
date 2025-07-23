
document.addEventListener('DOMContentLoaded', function() {
    // 1. Verificación inicial de permisos
    checkNotificationPermission();
    
    // 2. Registrar Service Worker
    registerServiceWorker();
});

// Función para verificar permisos
function checkNotificationPermission() {
    if (!("Notification" in window)) {
        console.warn("Este navegador no soporta notificaciones");
        return;
    }

    if (Notification.permission === "granted") {
        console.log("Permisos ya concedidos");
        showWelcomeNotification();
    } else if (Notification.permission !== "denied") {
        // Solicitar permisos después de interacción del usuario
        document.getElementById('enable-notifications').addEventListener('click', function() {
            Notification.requestPermission().then(permission => {
                if (permission === "granted") {
                    console.log("Permisos concedidos");
                    showWelcomeNotification();
                }
            });
        });
    }
}

// Función para registrar Service Worker
function registerServiceWorker() {
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/firebase-messaging-sw.js')
            .then(registration => {
                console.log('SW registrado:', registration.scope);
            })
            .catch(err => console.error('Error registrando SW:', err));
    }
}

// Función para mostrar notificación de bienvenida
function showWelcomeNotification() {
    if (Notification.permission === "granted") {
        new Notification("¡Notificaciones activadas!", {
            body: "Recibirás alertas importantes",
            icon: "/static/images/logo.png"
        });
    }
}