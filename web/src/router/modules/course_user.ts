export default [
  {
    path: "/courselist",
    name: "CourseList",
    component: () => import("@/views/User/Course/CourseList.vue"),
    meta: {
      title: "课程列表",
    },
  },
  {
    path: "/courseshow/:course_id",
    name: "CourseShow",
    component: () => import("@/views/User/Course/CourseShow.vue"),
    meta: {
      title: "课程展示",
    },
  },
  {
    path: "/addhomework",
    name: "AddHomework",
    component: () => import("@/views/User/Course/HomeworkAdd.vue"),
    meta: {
      title: "作业添加",
    },
  },
  {
    path: "/wecoursehome",
    name: "MyCourseList",
    component: () => import("@/views/User/Course/MyCourse.vue"),
    children: [
      {
        path: "/wecoursehome/mycourselist",
        name: "WeCourseHomeMyCourseList",
        component: () =>
          import("@/views/User/Course/MyCourse/MyCourseList.vue"),
        meta: {
          title: "我的课程列表",
        },
      },
      {
        path: "/wecoursehome/homework",
        name: "WeCourseHomeHomeWork",
        component: () => import("@/views/User/Course/MyCourse/HomeWork.vue"),
        meta: {
          title: "我的作业",
        },
      },
      {
        path: "/wecoursehome/mytest",
        name: "WeCourseHomeMyTest",
        component: () => import("@/views/User/Course/MyCourse/MyTest.vue"),
        meta: {
          title: "我的测试",
        },
      },
      {
        path: "/wecoursehome/myexam",
        name: "WeCourseHomeMyExam",
        component: () => import("@/views/User/Course/MyCourse/MyExam.vue"),
        meta: {
          title: "我的考试",
        },
      },
    ],
  },
  {
    path: "/coursedetails/:course_id/",
    name: "CourseDetails",
    component: () => import("@/views/User/Course/CourseDetails.vue"),
    children: [
      {
        path: "chapter",
        name: "CourseChapter",
        component: () =>
          import("@/views/User/Course/CourseDetails/Chapter.vue"),
        meta: {
          title: "课程目录",
        },
      },
      {
        path: "counter",
        name: "CourseCounter",
        component: () =>
          import("@/views/User/Course/CourseDetails/Counter.vue"),
        meta: {
          title: "课程统计",
        },
      },
      {
        path: "homework",
        name: "CourseHomework",
        component: () =>
          import("@/views/User/Course/CourseDetails/Homework.vue"),
        meta: {
          title: "课程作业",
        },
      },
      {
        path: "Exam",
        name: "CourseExam",
        component: () => import("@/views/User/Course/CourseDetails/Exam.vue"),
        meta: {
          title: "课程考试",
        },
      },
      {
        path: "datum",
        name: "CourseDatum",
        component: () => import("@/views/User/Course/CourseDetails/Datum.vue"),
        meta: {
          title: "课程资料",
        },
      },
      {
        path: "questionbank",
        name: "CourseQuestionBank",
        component: () =>
          import("@/views/User/Course/CourseDetails/QuestionBank.vue"),
        meta: {
          title: "课程题库",
        },
      },
      {
        path: "discuss",
        name: "CourseDiscuss",
        component: () =>
          import("@/views/User/Course/CourseDetails/Discuss.vue"),
        meta: {
          title: "课程讨论",
        },
      },
      {
        path: "dowork",
        name: "DoHomework",
        component: () => import("@/views/User/Course/DoWork.vue"),
        meta: {
          title: "做作业",
        },
      },
      {
        path: "examdetail",
        name: "ExamDetail",
        component: () => import("@//views/User/Course/ExamDetail.vue"),
        meta: {
          title: "考试情况详情",
        },
      },
      {
        path: "coursecontent",
        name: "CourseContent",
        component: () => import("@//views/User/Course/CourseContent.vue"),
        meta: {
          title: "课程内容",
        },
      },
      {
        path: "chaptereditor/:chapter_id",
        name: "ChapterEditor",
        component: () => import("@//views/User/Course/ChapterEditor.vue"),
        meta: {
          title: "章节编辑",
        },
      },
      {
        path: "joblibrary",
        name: "JobLibrary",
        component: () => import("@//views/User/Course/JobLibrary.vue"),
        meta: {
          title: "作业库",
        },
      },
      {
        path: "joblibrary/relesetask",
        name: "ReleseTask",
        component: () => import("@//views/User/Course/ReleseTask.vue"),
        meta: {
          title: "发放作业",
        },
      },
    ],
  },
];
