import { createApp } from 'vue'
import App from './App.vue'
import axios from "axios";

if(process.env.VUE_APP_BACKEND_HOST_ADDRESS){
    axios.defaults.baseURL = process.env.VUE_APP_BACKEND_HOST_ADDRESS
}
createApp(App).mount('#app')
