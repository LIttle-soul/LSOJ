export default [
    {
      path: "",
      redirect: "/home",
    },
    {
      path: "/home",
      name: "Home",
      component: () => import("@/views/User/Home/Home.vue"),
      meta: {
        title: "首页",
      },
    },
    {
      path: "/problemlist",
      name: "ProblemList",
      component: () => import("@/views/User/Problem/ProblemList.vue"),
      meta: {
        title: "问题列表",
      },
    },
    {
      path: "/ranklist",
      name: "RankList",
      component: () => import("@/views/User/Rank/RankList.vue"),
      meta: {
        title: "排名列表",
      },
    },
    {
      path: "/solutionlist",
      name: "SolutionList",
      component: () => import("@/views/User/Solution/SolutionList.vue"),
      meta: {
        title: "状态列表",
      },
    },
    {
      path: "/contestlist",
      name: "ContestList",
      component: () => import("@/views/User/Contest/ContestList.vue"),
      meta: {
        title: "竞赛列表",
      },
    },
    {
      path: "/contestshow",
      name: "ContestShow",
      component: () => import("@/views/User/Contest/ContestShow.vue"),
      meta: {
        title: "竞赛介绍",
      },
    },
    {
      path: "/contestdata",
      name: "ContestData",
      component: () => import("@/views/User/Contest/ContestData.vue"),
      meta: {
        title: "竞赛查看",
      },
    },
    {
      path: "/newslist",
      name: "NewsList",
      component: () => import("@/views/User/News/NewsList.vue"),
      meta: {
        title: "新闻列表",
      },
    },
    {
      path: "/shownews",
      name: "ShowNews",
      component: () => import("@/views/User/News/NewsShow.vue"),
      meta: {
        title: "新闻内容",
      },
    },
    // {
    //   path: "/login",
    //   name: "Login",
    //   component: () => import("@/views/User/User/Login.vue"),
    //   meta: {
    //     title: "登录",
    //   },
    // },
    // {
    //   path: "/register",
    //   name: "Register",
    //   component: () => import("@/views/User/User/Register.vue"),
    //   meta: {
    //     title: "注册",
    //   },
    // },
    // {
    //   path: "/forgetpassword",
    //   name: "ForgetPassword",
    //   component: () => import("@/views/User/User/ForgetPassword.vue"),
    //   meta: {
    //     title: "忘记密码",
    //   },
    // },
    // {
    //   path: "/showuserinfo",
    //   name: "ShowUserInfo",
    //   component: () => import("@/views/User/User/ShowUserInfo.vue"),
    //   meta: {
    //     title: "信息查看",
    //   },
    // },
    {
      path: "/perfectuserinfo",
      name: "PerfectUserInfo",
      component: () => import("@/views/User/User/PerfectUserInfo.vue"),
      meta: {
        title: "信息修改",
      },
    },
    {
      path: "/userstatus/:user_id",
      name: "UserStatus",
      component: () => import("@/views/User/User/UserStatus.vue"),
      meta: {
        title: "我的状态",
      },
    },
    {
      path: "/about/:filer",
      name: "About",
      component: () => import("@/views/User/Home/About.vue"),
      meta: {
        title: "关于",
      },
    },
    /**
     * /courseList: 课程
     */
    {
      path: "/courselist",
      name: "CourseList",
      component: () => import("@/views/User/Course/CourseList.vue"),
      meta: {
        title: "课程",
      },
    },
    /**
     * /forum: 讨论
     */
    {
      path: "/forum",
      name: "Forum",
      component: () => import("@/components/Forum/Forum.vue"),
      children: [
        // {
        //     path: 'AddDiscussion',
        //     name: 'AddDiscussion',
        //     component: () =>
        //         import ('@/components/Forum/AddDiscussion.vue'),
        //     meta: {
        //         title: "添加讨论"
        //     }
        // },
        // {
        //     path: 'discussion/:id',
        //     name: 'Discussion',
        //     component: () =>
        //         import ('@/components/Forum/Discussion.vue'),
        //     meta: {
        //         title: "讨论"
        //     }
        // },
      ],
    },
    {
      path: "/forum/AddDiscussion",
      name: "AddDiscussion",
      component: () => import("@/components/Forum/AddDiscussion.vue"),
      meta: {
        title: "添加讨论",
      },
    },
    {
      path: "/forum/MyDiscussions",
      name: "MyDiscussions",
      component: () => import("@/components/Forum/MyDiscussions.vue"),
      meta: {
        title: "添加讨论",
      },
    },
    {
      path: "/forum/discussion/:id",
      name: "Discussion",
      component: () => import("@/components/Forum/Discussion.vue"),
      meta: {
        title: "讨论",
      },
    },
    /**
     * /Level: 闯关
     */
    // {
    //   path: "/level",
    //   name: "Level",
    //   component: () => import("@/views/User/Level/Level.vue"),
    //   meta: {
    //     title: "闯关",
    //   },
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