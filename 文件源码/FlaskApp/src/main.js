import Vue from 'vue'
import App from './App'
import router from './router'
import iView from 'iview'
import axios from 'axios'
import echarts from 'echarts'
import lodash from 'lodash'
import 'iview/dist/styles/iview.css'
Vue.use(iView)
Vue.config.productionTip = false
Vue.config.devtools = true
Vue.prototype.$http = axios.create({
  // baseURL: 'http://localhost:5000/api/'
  baseURL: 'http://10.0.0.1:5000/api/'
  // baseURL: 'http://bigdata.lius.ac.cn/api/'
})
Vue.prototype.$echarts = echarts
window._ = lodash

router.beforeEach((to, from, next) => {
  let login = localStorage.getItem('login')
  if (login !== null) {
    next()
  } else {
    if (to.name === 'login') {
      next()
    } else {
      next({
        name: 'login'
      })
    }
  }
  // if (!login) {
  //   next({ path: '/' })
  // }
  // next()
})

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  render: h => h(App)
})
