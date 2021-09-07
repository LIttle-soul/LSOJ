export default [
    {
        path: "/showproblem/:problem_id",
        name: "AdminShowProblem",
        component: () => import("@/views/User/Problem/ProblemShow.vue"),
        meta: {
          title: "查看问题",
        },
    },
]