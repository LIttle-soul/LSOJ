import { createStore } from 'vuex';
import userSettings from './modules/userSettings';
import admin from './modules/admin';
import codeConfig from './modules/code';
import problem from './modules/problem';
import contest from './modules/contest';
import course from './modules/course';
import forum from './modules/forum';
import level from './modules/level';
import news from './modules/news';
import solution from './modules/solution';
import user from './modules/user';


export default createStore({
  state: {
    search_data: ''
  },
  getters: {

  },
  mutations: {
    set_search_data(state, val) {
      state.search_data = val;
    }
  },
  actions: {
  },
  modules: {
    userSettings: userSettings,
    admin: admin,
    codeConfig: codeConfig,
    problem: problem,
    contest: contest,
    course: course,
    forum: forum,
    level: level,
    news: news,
    solution: solution,
    user: user
  }
})
