import request from '@/utils/request'
import api from './api'

export function login(username, password) {
  console.log(username,password)
  return request({
    url: api.login,
    method: 'post',
    data: {
      user_name: username,
      user_password: password
    }
  })
}

export function getInfo(token) {
  return request({
    url: '/user/info',
    method: 'get',
    params: { token }
  })
}

export function logout() {
  return request({
    url: '/user/logout',
    method: 'post'
  })
}
