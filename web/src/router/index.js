import { createRouter, createWebHistory } from 'vue-router'
import user from './modules/user'
import admin from './modules/admin'
import others from './modules/others'

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
    component: () => import('@/layout/Admin'),
    children: [
      ...admin
    ]
  },
  ...others
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
