import Vue from 'vue'

import 'normalize.css/normalize.css' // A modern alternative to CSS resets

import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import locale from 'element-ui/lib/locale/lang/en' // lang i18n

import '@/styles/index.scss' // global css

import App from './App'
import router from './router'
import store from './store'

import '@/icons' // icon
// import '@/permission' // permission control
Vue.use(ElementUI, { locale })

import axios from 'src/utils/myAxios';
Vue.prototype.$http = axios;

//拦截器、
import { Loading, Message, MessageBox  } from 'element-ui'
// 超时时间
axios.defaults.timeout = 60000
// http请求拦截器
var loadinginstace
axios.interceptors.request.use(config => {
  // element ui Loading方法
  if (!config.noLoading) {
    loadinginstace = Loading.service({fullscreen: true});
  }
  // console.log(loadinginstace)
  return config
}, error => {
  Message({
    message:'加载超时',
    type:'warning'
  });
  if (loadinginstace) {
    loadinginstace.close();
  }
  return Promise.reject(error)
})
// http响应拦截器
axios.interceptors.response.use(data => {// 响应成功关闭loading
  if (loadinginstace) {
    loadinginstace.close();
  }
  if(data.data.status_code == 405007 ){
    router.push('/login')
  }
  return data
}, error => {
  Message({
    message:'请求失败',
    type:'warning'
  });
  if (loadinginstace) {
    loadinginstace.close();
  }
  return Promise.reject(error)
})



import api from 'src/api/api'
Vue.prototype.$api = api;
import VueLazyload from 'vue-lazyload'
Vue.use(VueLazyload, {loading:"/src/icons/svg/spinner.svg" })

Vue.config.productionTip = false

new Vue({
  el: '#app',
  router,
  store,
  render: h => h(App)
})
