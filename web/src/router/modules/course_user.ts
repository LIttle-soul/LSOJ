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
    path: "/courseshow",
    name: "CourseShow",
    component: () => import("@/views/User/Course/CourseShow.vue"),
    meta: {
      title: "课程展示",
    },
  },
];
