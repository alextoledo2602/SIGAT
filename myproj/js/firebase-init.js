// Configuración de Firebase (debe coincidir con tu proyecto)
const firebaseConfig = {
    apiKey: "AIzaSyCr8L1nuuQ5rUHywyILYcIf2PIT8F5Cnwo",
    authDomain: "my-firebase-proyect-13d3e.firebaseapp.com",
    projectId: "my-firebase-proyect-13d3e",
    storageBucket: "my-firebase-proyect-13d3e.appspot.com",
    messagingSenderId: "758339320819",
    appId: "1:758339320819:web:7337bda5a37e976ccfb086"
};

// Función auxiliar para obtener cookies
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

// Función principal para manejar notificaciones
async function initializeFCM() {
    try {
        // 1. Verificar soporte del navegador
        if (!('Notification' in window)) {
            console.warn('Este navegador no soporta notificaciones');
            return;
        }

        // 2. Inicializar Firebase
        if (!firebase.apps.length) {
            firebase.initializeApp(firebaseConfig);
        }

        // 3. Registrar Service Worker
        const registration = await navigator.serviceWorker.register('{% static "js/firebase-messaging-sw.js" %}');
        console.log('Service Worker registrado');

        // 4. Solicitar permisos y obtener token
        const permission = await Notification.requestPermission();
        if (permission !== 'granted') {
            console.warn('Permiso denegado');
            return;
        }

        const messaging = firebase.messaging();
        const token = await messaging.getToken({
            vapidKey: "BB_UqafsVu2Q7TmfZS2iUyj3a8Q8se4IhQ_-WzaAUViZOrG7f2-p4qdBv8MzhV8BEKVGDOyZadPzsnl3mOGCX3I",
            serviceWorkerRegistration: registration
        });

        if (!token) {
            throw new Error('No se pudo obtener el token');
        }

        // 5. Enviar token al servidor
        await saveTokenToServer(token);
        
        // 6. Configurar el manejador de mensajes en primer plano
        messaging.onMessage((payload) => {
            console.log('Mensaje recibido:', payload);
            // Mostrar notificación al usuario
            const notificationTitle = payload.notification.title;
            const notificationOptions = {
                body: payload.notification.body,
                icon: payload.notification.icon
            };
            new Notification(notificationTitle, notificationOptions);
        });

        // 7. Enviar notificación de bienvenida
        await sendWelcomeNotification();

    } catch (error) {
        console.error('Error en FCM:', error);
        showErrorUI();
    }
}

setTimeout(() => {
    new Notification("Prueba manual", {
        body: "Esto debería aparecer",
        icon: "/static/images/icon.png"
    });
}, 3000);

async function saveTokenToServer(token) {
    const response = await fetch('/save-fcm-token/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            token: token,
            device_name: navigator.userAgent
        })
    });
    return await response.json();
}

async function sendWelcomeNotification() {
    const response = await fetch('/send-welcome-notification/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    });
    return await response.json();
}

function showErrorUI() {
    const errorDiv = document.createElement('div');
    errorDiv.innerHTML = `
        <div style="position: fixed; bottom: 20px; right: 20px; padding: 15px; background: #ffebee; border: 1px solid #f44336; border-radius: 4px;">
            <p>Error al configurar notificaciones. Por favor, recarga la página.</p>
            <button onclick="initializeFCM()">Reintentar</button>
        </div>
    `;
    document.body.appendChild(errorDiv);
}

if (window.isAuthenticated) {  // Define esto en tu template
    document.addEventListener('DOMContentLoaded', () => {
        setTimeout(initializeFCM, 1000);
    });
}