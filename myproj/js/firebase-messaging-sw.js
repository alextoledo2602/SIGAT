///////compact
// static/firebase-messaging-sw.js
// templates/firebase-messaging-sw.js
const firebaseConfig = {
  apiKey: "AIzaSyCr8L1nuuQ5rUHywyILYcIf2PIT8F5Cnwo",
  authDomain: "my-firebase-proyect-13d3e.firebaseapp.com",
  projectId: "my-firebase-proyect-13d3e",
  storageBucket: "my-firebase-proyect-13d3e.appspot.com",
  messagingSenderId: "758339320819",
  appId: "1:758339320819:web:7337bda5a37e976ccfb086"
};

// Carga los scripts de Firebase
try {
  importScripts(
    'https://www.gstatic.com/firebasejs/9.6.1/firebase-app-compat.js',
    'https://www.gstatic.com/firebasejs/9.6.1/firebase-messaging-compat.js'
  );

  // Inicializa Firebase
  firebase.initializeApp(firebaseConfig);
  const messaging = firebase.messaging();

  // Manejo de mensajes en segundo plano
messaging.onBackgroundMessage((payload) => {
  console.log('[SW] Mensaje en segundo plano:', payload);
  
  // Notificación obligatoria aunque la app esté en primer plano
  const notificationTitle = payload.notification?.title || 'Nueva notificación';
  const notificationOptions = {
    body: payload.notification?.body || 'Tienes una nueva notificación',
    icon: payload.notification?.icon || '/static/images/logo.png',
    data: payload.data || { url: '/' }
  };

  // Muestra la notificación inmediatamente
  return self.registration.showNotification(notificationTitle, notificationOptions);
});

// Manejo de mensajes en primer plano
self.addEventListener('push', (event) => {
  const payload = event.data?.json() || {};
  console.log('[SW] Mensaje push recibido:', payload);
  
  event.waitUntil(
    self.registration.showNotification(
      payload.notification?.title || 'Mensaje importante',
      {
        body: payload.notification?.body,
        icon: payload.notification?.icon,
        data: payload.data
      }
    )
  );
});

} catch (e) {
  console.error('[SW] Error inicializando Firebase:', e);
}