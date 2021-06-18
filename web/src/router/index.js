import { createRouter, createWebHistory } from 'vue-router'


const routes = [
  {
    path: '',
    name: 'User',
    component: () => import('@/views/user/index.vue'),
    children: [
      {
        path: '',
        redirect: '/home'
      },
      {
        path: '/home',
        name: 'Index',
        component: () => import('@/views/user/Home/Home.vue')
      },
      {
        path: '/problems',
        name: 'Problems',
        component: () => import('@/views/user/Problems/Problems.vue')
      },
    ]
  },
  {
    path: '/admin',
    name: 'Admin',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "admin" */ '../views/admin/index.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/user/LoginRegister.vue')
  },
  {
    path: '/:pathMatch(.*)',
    name: '404',
    component: () => import('../views/404.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
