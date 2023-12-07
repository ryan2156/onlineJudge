import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from "../views/LoginView.vue"
import TestView from '../views/TestView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
    // meta: {
    //   needLogin: true
    // }
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView
  },
  {
    path: '/test',
    name: 'test',
    component: TestView
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
