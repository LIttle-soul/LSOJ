import { createRouter, createWebHashHistory } from 'vue-router'
import User from '../views/user/index.vue'

const routes = [
  {
    path: '/',
    name: 'User',
    component: User
  },
  {
    path: '/admin',
    name: 'Admin',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "admin" */ '../views/admin/index.vue')
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
