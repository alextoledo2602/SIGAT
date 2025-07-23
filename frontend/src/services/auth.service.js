import axios from 'axios'

const API_URL = 'http://localhost:8000/api/auth/'

export const setCSRFToken = async () => {
  try {
    await axios.get(`${API_URL}csrf/`, { 
      withCredentials: true 
    })
  } catch (err) {
    console.error("Error obteniendo CSRF token:", err)
  }
}

export default {
  login(username, password) {
    return axios.post(`${API_URL}login/`, {
      username,
      password
    }, {
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      },
      withCredentials: true
    })
  },
  sendLoginNotification(username) {
    return axios.post(`${API_URL}send-login-notification/`, {
      username
    }, {
      withCredentials: true
    })
  }
}