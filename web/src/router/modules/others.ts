export default [
  {
    path: "/showproblem",
    name: "AdminShowProblem",
    component: () => import("@/views/User/Problem/ProblemShow.vue"),
    meta: {
      title: "查看问题",
    },
  },
  {
    path: "/404",
    name: "404",
    component: () => import("@/views/Public/404.vue"),
  },
  {
    path: "/:pathMatch(.*)",
    redirect: "/404",
  },
  // {
  //   path: "/showcourse",
  //   name: "showcourse",
  //   component: () => import("@/views/User/Course/CourseShow.vue"),
  //   meta: {
  //     title: "课程详情",
  //   }
  // },
];
