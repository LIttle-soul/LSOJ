export default [
    // {
    //     path: '/login',
    //     name: 'Login',
    //     component: () => import('@/views/User/User/Login.vue')
    // },
    {
        path: "/about/:filer",
        name: "About",
        component: () => import("@/views/User/Home/About.vue"),
        meta: {
          title: "关于",
        },
      },
]