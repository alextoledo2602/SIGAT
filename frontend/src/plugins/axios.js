import axios from 'axios';

// Configura Axios para incluir credenciales (cookies)
axios.defaults.withCredentials = true;

// Obtener el CSRF Token desde las cookies
function getCSRFToken() {
    const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];
    return cookieValue;
}

// Interceptor para añadir el CSRF Token a cada petición POST/PUT/DELETE
axios.interceptors.request.use(config => {
    if (['post', 'put', 'delete'].includes(config.method.toLowerCase())) {
        config.headers['X-CSRFToken'] = getCSRFToken();
    }
    return config;
}, error => {
    return Promise.reject(error);
});

export default axios;