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
    path: "/about/:filer",
    name: "About",
    component: () => import("@/views/User/Home/About.vue"),
    meta: {
      title: "关于",
    },
  },
  {
    path: "/login",
    name: "Login",
    component: () => import("@/views/Public/Login.vue"),
    meta: {
      title: "登录",
    },
  },
  {
    path: "/register",
    name: "Register",
    component: () => import("@/views/Public/Register.vue"),
    meta: {
      title: "注册",
    },
  },
  {
    path: "/forgetpassword",
    name: "ForgetPassword",
    component: () => import("@/views/Public/ForgetPassword.vue"),
    meta: {
      title: "忘记密码",
    },
  },
  {
    path: "/showuserinfo",
    name: "ShowUserInfo",
    component: () => import("@/views/User/User/ShowUserInfo.vue"),
    meta: {
      title: "信息查看",
    },
  },
  {
    path: "/perfectuserinfo",
    name: "PerfectUserInfo",
    component: () => import("@/views/User/User/PerfectUserInfo.vue"),
    meta: {
      title: "信息修改",
    },
  },
  {
    path: "/userstatus/:user_id*",
    name: "UserStatus",
    component: () => import("@/views/User/User/UserStatus.vue"),
    meta: {
      title: "我的状态",
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
    path: "/contestdata/",
    name: "ContestData",
    component: () => import("@/views/User/Contest/ContestData.vue"),
    children: [
      {
        path: "problem",
        name: "ContestProblem",
        component: () => import("@/views/User/Contest/ContestData/Problem.vue"),
        meta: {
          title: "竞赛问题",
        },
      },
      {
        path: "status",
        name: "ContestStatus",
        component: () =>
          import("@/views/User/Contest/ContestData/Solution.vue"),
        meta: {
          title: "竞赛状态",
        },
      },
      {
        path: "rank",
        name: "ContestRank",
        component: () => import("@/views/User/Contest/ContestData/Rank.vue"),
        meta: {
          title: "竞赛排名",
        },
      },
      {
        path: "count",
        name: "ContestCount",
        component: () => import("@/views/User/Contest/ContestData/Count.vue"),
        meta: {
          title: "竞赛统计",
        },
      },
      {
        path: "print",
        name: "ContestPrint",
        component: () =>
          import("@/views/User/Contest/ContestData/PutContest.vue"),
        meta: {
          title: "竞赛打印",
        },
      },
    ],
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
    path: "/shownews/:news_id",
    name: "ShowNews",
    component: () => import("@/views/User/News/NewsShow.vue"),
    meta: {
      title: "新闻内容",
    },
  },
  {
    path: "/forum",
    name: "Forum",
    component: () => import("@/views/User/Forum/ForumList.vue"),
    meta: {
      title: "论坛",
    },
  },
  {
    path: "/showforum",
    name: "ShowForum",
    component: () => import("@/views/User/Forum/ForumShow.vue"),
    meta: {
      title: "帖子内容",
    },
  },
  {
    path: "/createforum",
    name: "CreateForum",
    component: () => import("@/views/User/Forum/ForumCreate.vue"),
    meta: {
      title: "创建帖子",
    },
  },
  {
    path: "/levelshow",
    name: "LevelShow",
    component: () => import("@/views/User/Level/LevelShow.vue"),
    meta: {
      title: "闯关",
    },
  },
];
