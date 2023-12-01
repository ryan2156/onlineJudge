import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import Loginview from '../views/LoginView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
    meta: {
      needLogin: true // 是否已登入
    }
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import('../views/AboutView.vue')
  },
  {
    path: '/login',
    name: 'login',
    component: Loginview
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

import { authToken } from '@/api/login'
router.beforeResolve( async to=>{
  if(to.meta.needLogin){
      const isLogin = window.localStorage.getItem("isLogin")
      if(!isLogin) return {name: "login"}
      
      const token = window.localStorage.getItem("token")
      const authResult = await authToken(token)
      if(!authResult.status) return {name: "login"}
  }
})

export default router
