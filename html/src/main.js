import router from "./router"
import message from "@/components/message/index.js";
import 'virtual:svg-icons-register'

import { createApp } from 'vue'
import App from './App.vue'
import clickOutside from "@/utils/clickoutside";

import moment from 'moment'
import 'moment/dist/locale/zh-cn'
import './app.css'

const app = createApp(App)

app.directive('focus', {
    mounted(el) {
    // 聚焦元素
        el.focus()
    },
})

app.directive('click-outside', clickOutside)


app.use(router)
app.mount("#app")
app.config.globalProperties.$message = message
