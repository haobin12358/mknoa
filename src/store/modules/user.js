import {  logout, getInfo } from 'src/api/login'
import { getToken, setToken, removeToken } from 'src/utils/auth'
import {login} from 'src/service/index'
import { setStore} from "src/utils/index";
import Cookies from 'js-cookie'
import store from "../index";


const user = {
  state: {
    userInfo: {},
    token: getToken(),
    name: '',
    avatar: '',
    roles: [],
    side: [
      {
        "children": [
          {
            "power_component": "() => import('src/views/profile/index')",
            "power_id": "d325dce4-05de-11e9-80d5-5800e3119d4a",
            "power_meta": {
              "powermeta_icon": null,
              "powermeta_roles": null,
              "powermeta_title": "首页"
            },
            "power_path": "/profile",
            "power_redirect": null,
            "power_status": 41
          }
        ],
        "power_component": "Layout",
        "power_id": "46cef7f4-05de-11e9-922b-5800e3119d4a",
        "power_meta": {
          "powermeta_icon": 'homepage',
          "powermeta_roles": null,
          "powermeta_title": "首页"
        },
        "power_path": "index",
        "power_redirect": "/profile",
        "power_status": 41
      },
      {
        "children": [
          {
            "power_component": "() => import('src/views/approve/index')",
            "power_id": "41fc05d2-05e1-11e9-bc61-5800e3119d4a",
            "power_meta": {
              "powermeta_icon": null,
              "powermeta_roles": null,
              "powermeta_title": "所有审批"
            },
            "power_path": " ",
            "power_redirect": " ",
            "power_status": 41
          },
          {
            "power_component": "() => import('src/views/approve/allApprove')",
            "power_id": "5411b31a-05e1-11e9-8d62-5800e3119d4a",
            "power_meta": {
              "powermeta_icon": null,
              "powermeta_roles": null,
              "powermeta_title": "审批管理"
            },
            "power_path": "/allApprove",
            "power_redirect": " ",
            "power_status": 41
          },
          {
            "power_component": "() => import('src/views/approve/editApprove')",
            "power_id": "9f336fb0-05e1-11e9-be02-5800e3119d4a",
            "power_meta": {
              "powermeta_icon": null,
              "powermeta_roles": null,
              "powermeta_title": "新增审批流"
            },
            "power_path": "editApprove",
            "power_redirect": " ",
            "power_status": 41
          }
        ],
        "power_component": "Layout",
        "power_id": "1fdb2810-05e1-11e9-84b2-5800e3119d4a",
        "power_meta": {
          "powermeta_icon": "approve",
          "powermeta_roles": "admin",
          "powermeta_title": "审批流管理"
        },
        "power_path": "/approve",
        "power_redirect": "approve",
        "power_status": 41
      },
      {
        "children": [
          {
            "power_component": "() => import('src/views/module/index')",
            "power_id": "6b9cbbb6-05e0-11e9-894d-5800e3119d4a",
            "power_meta": {
              "powermeta_icon": null,
              "powermeta_roles": null,
              "powermeta_title": "模板列表"
            },
            "power_path": "index",
            "power_redirect": null,
            "power_status": 41
          },
          {
            "power_component": "() => import('src/views/module/editModule')",
            "power_id": "7dbef710-05e0-11e9-a47a-5800e3119d4a",
            "power_meta": {
              "powermeta_icon": null,
              "powermeta_roles": null,
              "powermeta_title": "新增模板"
            },
            "power_path": "editModule",
            "power_redirect": null,
            "power_status": 41
          }
        ],
        "power_component": "Layout",
        "power_id": "3608f18c-05e0-11e9-9456-5800e3119d4a",
        "power_meta": {
          "powermeta_icon": 'manage',
          "powermeta_roles": null,
          "powermeta_title": "模板管理"
        },
        "power_path": "/module",
        "power_redirect": "module",
        "power_status": 41
      },
      {
        "children": [
          {
            "power_component": "() => import('src/views/role/editRole')",
            "power_id": "677d1b0a-05df-11e9-a5fd-5800e3119d4a",
            "power_meta": {
              "powermeta_icon": null,
              "powermeta_roles": null,
              "powermeta_title": "新增身份"
            },
            "power_path": "editRole",
            "power_redirect": null,
            "power_status": 41
          },
          {
            "power_component": "() => import('src/views/role/index')",
            "power_id": "aeebfd40-0546-11e9-be8c-5800e3119d4a",
            "power_meta": {
              "powermeta_icon": null,
              "powermeta_roles": null,
              "powermeta_title": "所有身份"
            },
            "power_path": "index",
            "power_redirect": "",
            "power_status": 41
          }
        ],
        "power_component": "Layout",
        "power_id": "3df20bec-0545-11e9-bed2-5800e3119d4a",
        "power_meta": {
          "powermeta_icon": "headlines",
          "powermeta_roles": "admin",
          "powermeta_title": "身份管理"
        },
        "power_path": "/role",
        "power_redirect": "/role/index",
        "power_status": 41
      },
      {
        "children": [
          {
            "power_component": "() => import('src/views/product/index')",
            "power_id": "de073eae-05e0-11e9-bedf-5800e3119d4a",
            "power_meta": {
              "powermeta_icon": null,
              "powermeta_roles": null,
              "powermeta_title": "商品管理"
            },
            "power_path": "product",
            "power_redirect": null,
            "power_status": 41
          }
        ],
        "power_component": "Layout",
        "power_id": "a807a336-05e0-11e9-aff4-5800e3119d4a",
        "power_meta": {
          "powermeta_icon": "product",
          "powermeta_roles": "editor",
          "powermeta_title": "商品管理"
        },
        "power_path": "/product",
        "power_redirect": "product",
        "power_status": 41
      },
      {
        "children": [
          {
            "power_component": "() => import('src/views/account/index')",
            "power_id": "e7cd50ee-05df-11e9-a605-5800e3119d4a",
            "power_meta": {
              "powermeta_icon": null,
              "powermeta_roles": null,
              "powermeta_title": "所有账号"
            },
            "power_path": "account",
            "power_redirect": null,
            "power_status": 41
          },
          {
            "power_component": "() => import('src/views/account/editAccount')",
            "power_id": "fe832d3a-05df-11e9-8a97-5800e3119d4a",
            "power_meta": {
              "powermeta_icon": null,
              "powermeta_roles": null,
              "powermeta_title": "新增账号"
            },
            "power_path": "editAccount",
            "power_redirect": null,
            "power_status": 41
          }
        ],
        "power_component": "Layout",
        "power_id": "a940443a-05df-11e9-a4f3-5800e3119d4a",
        "power_meta": {
          "powermeta_icon": "group",
          "powermeta_roles": "admin",
          "powermeta_title": "账号管理"
        },
        "power_path": "/account",
        "power_redirect": "account",
        "power_status": 41
      },
      {
        children: [
          {
            power_component: "() => import('src/views/announcement/editAnnouncement')",
            power_id: "01dae9ba-05e2-11e9-8b24-5800e3119d4a",
            power_meta: {
              powermeta_icon: null,
              powermeta_roles: null,
              powermeta_title: "新增公告"
            },
            power_path: "editAnnouncement",
            power_redirect: " ",
            power_status: 41
          },
          {
            power_component: "() => import('src/views/announcement/index')",
            power_id: "f2d3c130-05e1-11e9-8aa9-5800e3119d4a",
            power_meta: {
              powermeta_icon: null,
              powermeta_roles: null,
              powermeta_title: "所有公告"
            },
            power_path: "announcement",
            power_redirect: " ",
            power_status: 41
          }
        ],
        power_component: "Layout",
        power_id: "d0fe2618-05e1-11e9-a74f-5800e3119d4a",
        power_meta: {
          powermeta_icon: "announcement",
          powermeta_roles: "admin",
          powermeta_title: "平台公告"
        },
        power_path: "/announcement",
        power_redirect: "announcement",
        power_status: 41
      }
    ]
  },

  mutations: {
    SET_USER_INFO: (state, userInfo) => {
      state.userInfo = userInfo
    },
    SET_TOKEN: (state, token) => {
      state.token = token
    },

    SET_NAME: (state, name) => {
      state.name = name
    },
    SET_AVATAR: (state, avatar) => {
      state.avatar = avatar
    },
    SET_ROLES: (state, roles) => {
      state.roles = roles
    },
    SET_SIDE: (state, side) =>{
      state.side = side
    },
    InitInfo:(state)=>{
      let saveUserInfo = Cookies.get('User-Info');

      if (saveUserInfo){
        state.userInfo = JSON.parse(saveUserInfo);
        // state.roles = [state.userInfo.adname]
      }
    }
  },

  actions: {
    // 登录
    Login({ commit }, userInfo) {
      console.log('action login');
      return new Promise((resolve, reject) => {
        login(userInfo.user_name, userInfo.user_password).then(response => {
          if(response.data.status == 200){
            let resData = response.data,
                data = resData.data;
            // setToken(data.token);
            setStore('token',data.token)
            commit('SET_TOKEN', data.token)
            commit('SET_SIDE', data.power_list)
            Cookies.set('User-Info',data.user_message)
            commit('SET_USER_INFO', data.user_message);
            // commit('InitInfo');
            resolve()
          }else{
            reject();
          }
        }).catch(error => {
          reject(error)
        })
      })
    },

    // 获取用户信息
    GetInfo({ commit, state }) {
      return new Promise((resolve, reject) => {
        getInfo(state.token).then(response => {
          const data = response.data
          if (data.roles && data.roles.length > 0) { // 验证返回的roles是否是一个非空数组
            commit('SET_ROLES', data.roles)
          } else {
            reject('getInfo: roles must be a non-null array !')
          }
          commit('SET_NAME', data.name)
          commit('SET_AVATAR', data.avatar)
          resolve(response)
        }).catch(error => {
          reject(error)
        })
      })
    },

    // 登出
    LogOut({ commit, state }) {
      return new Promise((resolve, reject) => {
        logout(state.token).then(() => {
          commit('SET_TOKEN', '')
          commit('SET_ROLES', [])
          removeToken()
          resolve()
        }).catch(error => {
          reject(error)
        })
      })
    },

    // 前端 登出
    FedLogOut({ commit }) {
      return new Promise(resolve => {
        commit('SET_TOKEN', '')
        removeToken()
        resolve()
      })
    }
  }
}

export default user
