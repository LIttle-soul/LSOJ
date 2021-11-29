import { createStore } from "vuex";
import userSettings from "./modules/userSettings";
import admin from "./modules/admin";
import code from "./modules/code";
import problem from "./modules/problem";
import contest from "./modules/contest";
import course from "./modules/course";
import forum from "./modules/forum";
import level from "./modules/level";
import news from "./modules/news";
import solution from "./modules/solution";
import user from "./modules/user";
import address from "./modules/address";
import school from "./modules/school";
import rank from "./modules/rank";

export default createStore({
  state: {
    search_data: "",
  },
  getters: {},
  mutations: {
    set_search_data(state, val) {
      state.search_data = val;
    },
  },
  modules: {
    userSettings: userSettings,
    code: code,
    admin: admin,
    problem: problem,
    contest: contest,
    course: course,
    forum: forum,
    level: level,
    news: news,
    solution: solution,
    user: user,
    address: address,
    school: school,
    rank: rank,
  },
});
