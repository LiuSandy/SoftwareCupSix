import Vue from 'vue'
import Router from 'vue-router'
Vue.use(Router)

const Main = resolve => require(['@/components/Main'], resolve)
const saleDetails = resolve => require(['@/components/saleDetails'], resolve)
const degreeDetails = resolve => require(['@/components/degreeDetails'], resolve)
const pagerankDetails = resolve => require(['@/components/pagerankDetails'], resolve)
const history = resolve => require(['@/components/history'], resolve)
const predict = resolve => require(['@/components/predict'], resolve)
const Home = resolve => require(['@/components/Home'], resolve)
const SaleShow = resolve => require(['@/components/sale/Show'], resolve)
const degreeShow = resolve => require(['@/components/sale/Degree'], resolve)
const NotFind = resolve => require(['@/components/error/404'], resolve)
const Upload = resolve => require(['@/components/Upload'], resolve)
const Login = resolve => require(['@/components/auth/Login'], resolve)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Hello',
      component: Main,
      children: [
        {
          path: '',
          component: Home
        },
        {
          path: 'sale',
          component: saleDetails
        },
        {
          path: 'sale/:id',
          name: 'saleShow',
          component: SaleShow
        },
        {
          path: 'degree/:id',
          name: 'degreeShow',
          component: degreeShow
        },
        {
          path: 'degree',
          component: degreeDetails
        },
        {
          path: 'PageRank',
          component: pagerankDetails
        },
        {
          path: 'history',
          component: history
        },
        {
          path: 'predict',
          component: predict
        },
        {
          path: 'upload',
          component: Upload
        }
      ]
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '*',
      name: '404',
      component: NotFind
    }
  ]
})
