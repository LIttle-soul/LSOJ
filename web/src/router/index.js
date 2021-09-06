import { createRouter, createWebHashHistory } from 'vue-router'
import user from './modules/user'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/layout/User'),
    children: [
      ...user
    ]
  },
  {
    path: '/admin',
    name: 'Admin',
    component: () => import('@/layout/Admin')
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
