import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import ElementPlus from 'element-plus'
import axios from 'axios'
import qs from 'qs'
import cookies from 'vue-cookies'
import 'element-plus/lib/theme-chalk/index.css'
import 'element-plus/lib/theme-chalk/display.css'

const app = createApp(App)
app.config.globalProperties.$http=axios
app.config.globalProperties.$qs=qs
app.config.globalProperties.$cookies=cookies
app.use(ElementPlus)
app.use(store)
app.use(router)
app.mount('#app')
