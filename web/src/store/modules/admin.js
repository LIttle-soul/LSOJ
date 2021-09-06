import { nav_menu } from "@/config/adminNav";

export default {
  namespaced: true,
  state: {
    nav_menu: nav_menu,
  },
  mutations: {
    setUserInfo(state, data) {
      state.userInfo = data;
    },
    clearUserInfo(state) {
      state.userInfo = null;
    },
  },
  actions: {
    async getUserInfo({ commit }) {
      const { code, data } = await this.getUserInfo();
      if (+code === 200) {
        commit("setUserInfo", data);
        return Promise.resolve(data);
      }
    },
  },
};
