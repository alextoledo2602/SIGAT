import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from '@/plugins/axios'
import '@/assets/dashboard.css'
import { library } from '@fortawesome/fontawesome-svg-core'
import { fas } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

library.add(fas)



const app = createApp(App);
app.use(router);
app.use(store); 
app.component('font-awesome-icon', FontAwesomeIcon)
app.config.globalProperties.$axios = axios;
app.mount('#app');