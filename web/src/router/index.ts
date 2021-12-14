import {
  createRouter,
  createWebHistory,
  RouteRecordRaw,
  RouterOptions,
} from "vue-router";
import user from "./modules/user";
import admin from "./modules/admin";
import others from "./modules/others";
import course_user from "./modules/course_user";

const routes = [
  {
    path: "/",
    name: "Home",
    component: () => import("@/layout/User.vue"),
    children: [...user, ...course_user],
  },
  {
    path: "/admin",
    name: "Admin",
    component: () => import("/src/layout/Admin.vue"),
    children: admin,
  },
  ...others,
];

const router = createRouter({
  history: createWebHistory(),
  routes: <RouteRecordRaw[]>routes,
});

export default router;
