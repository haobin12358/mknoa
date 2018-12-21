import { Loading, Message, MessageBox } from 'element-ui'
import axios from 'axios'

// 超时时间
axios.defaults.timeout = 60000
// http请求拦截器
let loadinginstace
axios.interceptors.request.use(config => {
  if (!config.noLoading) {
    loadinginstace = Loading.service({ fullscreen: true })
  }
  return config
}, error => {
  Message({
    message: '加载超时',
    type: 'warning'
  })

  return Promise.reject(error)
})
// http响应拦截器
axios.interceptors.response.use(data => {// 响应成功关闭loading
  if (loadinginstace) {
    loadinginstace.close()
  }
  if (data.data.status != 200) {
    Message.error({
      message: data.data.message,
      duration: 4500,
      showClose: true,
    })
  }
  // if (data.data.status == 405 && data.data.status_code == 405003) {
  //   location.href = location.origin;
  //   localStorage.setItem('token', '');
  //   this.$notify()
  // }

  return data
}, error => {
  Message({
    message: '请求失败',
    type: 'warning'
  })
  if (loadinginstace) {
    loadinginstace.close()
  }
  return Promise.reject(error)
})

export default axios
