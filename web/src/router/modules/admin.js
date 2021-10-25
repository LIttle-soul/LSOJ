// import adminCourse from './course_admin'

export default [
  {
    path: "/admin/userlist",
    name: "AdminUserList",
    component: () => import("@/views/Admin/Users/UsersList.vue"),
    meta: {
      title: "用户管理",
    },
  },
  {
    path: "/admin/teamlist",
    name: "AdminTeamList",
    component: () => import("@/views/Admin/Users/TeamList.vue"),
    meta: {
      title: "团队管理",
    },
  },
  {
    path: "/admin/problemlist",
    name: "AdminProblemList",
    component: () => import("@/views/Admin/Problem/ProblemList.vue"),
    meta: {
      title: "问题管理",
    },
  },
  {
    path: "/admin/addproblem/:problem_id*",
    name: "AdminAddProblem",
    component: () => import("@/views/Admin/Problem/ProblemAdd.vue"),
    meta: {
      title: "添加问题",
    },
  },
  // {
  //   path: "/admin/courselist",
  //   name: "AdminCourseList",
  //   component: () => import("@/views/Admin/Course/CourseList.vue"),
  //   meta: {
  //     title: "课程管理",
  //   },
  // },
  // {
  //   path: "/admin/addCourse",
  //   name: "AdminAddCourse",
  //   component: () => import("@/views/Admin/Course/CourseAdd.vue"),
  //   meta: {
  //     title: "添加课程",
  //   },
  // },
  {
    path: "/admin/newslist",
    name: "AdminNewsList",
    component: () => import("@/views/Admin/News/NewsList.vue"),
    meta: {
      title: "新闻管理",
    },
  },
  {
    path: "/admin/addnews/:news_id*",
    name: "AdminAddNews",
    component: () => import("@/views/Admin/News/NewsAdd.vue"),
    meta: {
      title: "添加新闻",
    },
  },
  // {
  //   path: "/admin/forumlist",
  //   name: "AdminForumList",
  //   component: () => import("@/views/Admin/Forum/ForumList.vue"),
  //   meta: {
  //     title: "论坛管理",
  //   },
  // },
  // {
  //   path: "/admin/sensitiveword",
  //   name: "AdminSensitiveWord",
  //   component: () => import("@/views/Admin/Forum/SensitiveWord.vue"),
  //   meta: {
  //     title: "敏感词管理",
  //   },
  // },
  {
    path: "/admin/contestlist",
    name: "AdminContestList",
    component: () => import("@/views/Admin/Contest/ContestList.vue"),
    meta: {
      title: "竞赛管理",
    },
  },
  {
    path: "/admin/addcontest/:contest_id*",
    name: "AdminAddContest",
    component: () => import("@/views/Admin/Contest/ContestAdd.vue"),
    meta: {
      title: "添加竞赛",
    },
  },
  {
    path: "/admin/contestuser",
    name: "AdminContestUser",
    component: () => import("@/views/Admin/Contest/ContestUser.vue"),
    meta: {
      title: "竞赛成员",
    },
  },
  {
    path: "/admin/contestproblem",
    name: "AdminContestProblem",
    component: () => import("@/views/Admin/Contest/ContestProblem.vue"),
    meta: {
      title: "竞赛问题",
    },
  },
  // {
  //   path: "/admin/levellist",
  //   name: "AdminLevelList",
  //   component: () => import("@/views/Admin/Level/LevelList.vue"),
  //   meta: {
  //     title: "关卡管理",
  //   },
  // },
  // {
  //   path: "/admin/addlevel",
  //   name: "AdminAddLevel",
  //   component: () => import("@/views/Admin/Level/LevelAdd.vue"),
  //   meta: {
  //     title: "添加关卡",
  //   },
  // },
  {
    path: "/admin/addresslist",
    name: "AdminAddress",
    component: () => import("@/views/Admin/Address/AddressList.vue"),
    meta: {
      title: "地址管理",
    },
  },
  {
    path: "/admin/provincelist",
    name: "AdminProvinceList",
    component: () => import("@/views/Admin/Address/ProvinceList.vue"),
    meta: {
      title: "省份管理",
    },
  },
  {
    path: "/admin/municipalitylist",
    name: "AdminMunicipalityList",
    component: () => import("@/views/Admin/Address/MunicipalityList.vue"),
    meta: {
      title: "城市管理",
    },
  },
  {
    path: "/admin/schoollist",
    name: "AdminSchoolList",
    component: () => import("@/views/Admin/School/SchoolList.vue"),
    meta: {
      title: "学校管理",
    },
  },
  // {
  //   path: "/admin/addschool",
  //   name: "AdminAddSchool",
  //   component: () => import("@/views/Admin/School/SchoolAdd.vue"),
  //   meta: {
  //     title: "添加学校",
  //   },
  // },
  // {
  //   path: "/admin/collegelist",
  //   name: "AdminCollegeList",
  //   component: () => import("@/views/Admin/School/CollegeList.vue"),
  //   meta: {
  //     title: "学院管理",
  //   },
  // },
  // {
  //   path: "/admin/addCollege",
  //   name: "AdminAddCollege",
  //   component: () => import("@/views/Admin/School/CollegeAdd.vue"),
  //   meta: {
  //     title: "添加学院",
  //   },
  // },
  // {
  //   path: "/admin/classlist",
  //   name: "AdminClassList",
  //   component: () => import("@/views/Admin/School/ClassList.vue"),
  //   meta: {
  //     title: "班级管理",
  //   },
  // },
  // {
  //   path: "/admin/addclass",
  //   name: "AdminddClass",
  //   component: () => import("@/views/Admin/School/ClassAdd.vue"),
  //   meta: {
  //     title: "添加班级",
  //   },
  // },
  // {
  //   path: "/admin/judgerlist",
  //   name: "AdminJudgerList",
  //   component: () => import("@/views/Admin/Judger/JudgerList.vue"),
  //   meta: {
  //     title: "判题机管理",
  //   },
  // },
  // {
  //   path: "/admin/addjudger",
  //   name: "AdminAddJudger",
  //   component: () => import("@/views/Admin/Judger/JudgerAdd.vue"),
  //   meta: {
  //     title: "添加判题机",
  //   },
  // },
  // ...adminCourse
];
