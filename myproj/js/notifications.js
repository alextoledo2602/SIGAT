// static/js/notifications.js

// Función para verificar autenticación
async function checkAuthentication() {
    try {
        const response = await fetch('/check-auth/', {
            credentials: 'include'
        });
        const data = await response.json();
        return data.isAuthenticated === true;
    } catch (error) {
        console.error('Error verificando autenticación:', error);
        return false;
    }
}

// Función para verificar token FCM
async function checkFCMToken() {
    try {
        const response = await fetch('/check-fcm-token/', {
            credentials: 'include'
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        return data.hasToken === true;
    } catch (error) {
        console.error('Error verificando token FCM:', error);
        return false;
    }
}

// Función para obtener cookie CSRF
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

// Función para registrar token FCM
async function registerFCMToken() {
    if (!('Notification' in window) || !('serviceWorker' in navigator)) {
        console.warn('Este navegador no soporta notificaciones push');
        return false;
    }

    const permission = await Notification.requestPermission();
    if (permission !== 'granted') {
        console.warn('Permiso para notificaciones no concedido');
        return false;
    }

    try {
        const registration = await navigator.serviceWorker.register('/firebase-messaging-sw.js');
        console.log('Service Worker registrado:', registration);

        const token = await getFCMToken();
        if (!token) {
            console.error('No se pudo obtener el token FCM');
            return false;
        }

        return await saveFCMTokenToServer(token);
    } catch (error) {
        console.error('Error registrando FCM:', error);
        return false;
    }
}

// Función para enviar notificación de login
async function sendLoginNotification() {
    try {
        const hasToken = await checkFCMToken();
        if (!hasToken) {
            console.warn('El usuario no tiene token FCM registrado');
            return false;
        }
        
        const response = await fetch('/send-login-notification/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            credentials: 'include'
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Notificación enviada:', data);
        return true;
    } catch (error) {
        console.error('Error enviando notificación:', error);
        return false;
    }
}

// Función para mostrar prompt de registro
function showFCMRegistrationPrompt() {
    if (document.getElementById('fcm-prompt')) return;
    
    const prompt = document.createElement('div');
    prompt.id = 'fcm-prompt';
    prompt.innerHTML = `
        <div class="fcm-prompt-content">
            <p>Para recibir notificaciones, por favor activa los permisos</p>
            <button id="enable-notifications">Activar Notificaciones</button>
        </div>
    `;
    document.body.appendChild(prompt);
    
    document.getElementById('enable-notifications').addEventListener('click', async () => {
        const success = await registerFCMToken();
        if (success) {
            prompt.remove();
            await sendLoginNotification();
        }
    });
}

// Inicialización
document.addEventListener('DOMContentLoaded', async function() {
    const isAuthenticated = await checkAuthentication();
    
    if (isAuthenticated) {
        try {
            const tokenRegistered = await registerFCMToken();
            
            if (tokenRegistered) {
                await sendLoginNotification();
            } else {
                showFCMRegistrationPrompt();
            }
        } catch (error) {
            console.error('Error inicializando notificaciones:', error);
        }
    }
});