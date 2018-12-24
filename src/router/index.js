import Vue from 'vue'
import Router from 'vue-router'

// in development-env not use lazy-loading, because lazy-loading too many pages will cause webpack hot update too slow. so only in production use lazy-loading;
// detail: https://panjiachen.github.io/vue-element-admin-site/#/lazy-loading

Vue.use(Router)

/* Layout */
import Layout from '../views/layout/Layout'

/**
 * hidden: true                   if `hidden:true` will not show in the sidebar(default is false)
 * alwaysShow: true               if set true, will always show the root menu, whatever its child routes length
 *                                if not set alwaysShow, only more than one route under the children
 *                                it will becomes nested mode, otherwise not show the root menu
 * redirect: noredirect           if `redirect:noredirect` will no redirect in the breadcrumb
 * name:'router-name'             the name is used by <keep-alive> (must set!!!)
 * meta : {
    title: 'title'               the name show in submenu and breadcrumb (recommend set)
    icon: 'svg-name'             the icon show in the sidebar,
  }
 **/
export const constantRouterMap = [
  { path: '/login', component: () => import('@/views/login/index'), hidden: true },
  { path: '/404', component: () => import('@/views/404'), hidden: true },
  {
    path: '',
    component: Layout,
    redirect: '/profile',
    children: [
      {
        path: 'profile',
        name: 'ProfileIndex',
        component: () => import('src/views/profile/index'),
        meta: { title: '首页', icon: 'homepage'}
      }
    ]
  },
  {
    path: '/role',
    component: Layout,
    redirect: '/role/index',
    meta: { title: '身份管理', icon: 'headlines',roles:['admin'] },
    children: [
      {
        path: 'index',
        name: 'ProductIndex',
        component: () => import('src/views/role/index'),
        meta: { title: '所有身份' }
      }, {
        path: 'editRole',
        name: 'editRole',
        component: () => import('src/views/role/editRole'),
        meta: { title: '新增身份' }
      }
    ]
  },

  {
    path: '/account',
    component: Layout,
    redirect: 'account',
    meta: { title: '账号管理', icon: 'group',roles:['admin'] },
    children: [
      {
        path: 'account',
        name: 'AccountIndex',
        component: () => import('src/views/account/index'),
        meta: { title: '所有账号'}
      },
      {
        path: 'editAccount',
        name: 'editAccount',
        component: () => import('src/views/account/editAccount'),
        meta: { title: '新增账号' }
      }
    ]
  },

  {
    path: '/module',
    component: Layout,
    redirect: 'module',
    meta: { title: '模板管理', icon: 'manage',roles:['admin'] },
    children: [
      {
        path: 'index',
        name: 'module',
        component: () => import('src/views/module/index'),
        meta: { title: '模板列表' }
      }, {
        path: 'editModule',
        name: 'editModule',
        component: () => import('src/views/module/editModule'),
        meta: { title: '新增模板' }
      }
    ]
  },
  {
    path: '/product',
    component: Layout,
    redirect: 'product',
    meta: { title: '商品管理', icon: 'product',roles:['editor'] },
    children: [
      {
        path: 'product',
        name: 'ProductIndex',
        component: () => import('src/views/product/index'),
        meta: { title: '商品管理'}
      }
    ]
  },
  {
    path: '/approve',
    component: Layout,
    redirect: 'approve',
    meta: { title: '审批流管理', icon: 'approve',roles:['admin'] },
    children: [
      {
        path: '',
        name: 'ApproveIndex',
        component: () => import('src/views/approve/index'),
        meta: { title: '所有审批'}
      },
      {
        path: '/allApprove',
        name: 'allApprove',
        component: () => import('src/views/approve/allApprove'),
        meta: { title: '审批管理'}
      },
      {
        path: '/approveDetail',
        name: 'approveDetail',
        hidden:true,
        component: () => import('src/views/approve/approveDetail'),
        meta: { title: '审批管理'}
      },
      {
        path: '/addApprove',
        name: 'addApprove',
        hidden:true,
        component: () => import('src/views/approve/addApprove'),
        meta: { title: '发起审批'}
      },
      {
        path: 'editApprove',
        name: 'editApprove',
        component: () => import('src/views/approve/editApprove'),
        meta: { title: '新增审批流' }
      }
    ]
  },
  {
    path: '/announcement',
    component: Layout,
    redirect: 'announcement',
    meta: { title: '平台公告', icon: 'announcement',roles:['admin'] },
    children: [
      {
        path: '',
        name: 'AnnouncementIndex',
        component: () => import('src/views/announcement/index'),
        meta: { title: '所有公告'}
      },
      {
        path: 'editAnnouncement',
        name: 'editAnnouncement',
        component: () => import('src/views/announcement/editAnnouncement'),
        meta: { title: '新增公告' }
      }
    ]
  },

  { path: '*', redirect: '/404', hidden: true }
  ]


export default new Router({
  // mode: 'history', //后端支持可开
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRouterMap
})
export const asyncRouterMap = [


]
