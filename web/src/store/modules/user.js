import { getUserInfo, getUserList, getTeamList } from "@/api/user";
import { user_nav, not_login, user_login, admin_login } from "@/config/userNav";

export default {
  namespaced: true,
  state: {
    user_nav: user_nav,
    user_info: null,
    login_nav: not_login,
    user_list: [],
    team_list: [],
  },
  getters: {
    getMyCreateTeamList: (state) => () => {
      return state.team_list.filter(
        (team_list) => team_list.class_creator === state.user_info.user_id
      );
    },
    getMyJoinTeamList: (state) => () => {
      return state.team_list.filter((team_list) => {
        let temp_user_list = team_list.user_list.map((item) => {
          return item.user_id;
        });
        return temp_user_list.includes(state.user_info.user_id);
      });
    },
  },
  mutations: {
    setUserInfo(state, data) {
      state.user_info = data;
    },
    setUserList(state, data) {
      state.user_list = data;
    },
    setTeamList(state, data) {
      state.team_list = data;
    },
    setLoginNav(state) {
      state.login_nav =
        state.user_info == null
          ? not_login
          : state.user_info.user_power <= 2
          ? [...admin_login, ...user_login]
          : user_login;
    },
    clearUserInfo(state) {
      state.user_info = null;
      state.login_nav = not_login;
    },
  },
  actions: {
    async getUserInfo({ commit }) {
      const data = await getUserInfo();
      // console.log(data);
      if (data.status) {
        commit("setUserInfo", data.data);
        commit("setLoginNav");
        return true;
      } else {
        return false;
      }
    },
    async getUserList({ commit }) {
      const data = await getUserList();
      // console.log(data);
      if (data.status) {
        commit("setUserList", data.message);
        return Promise.resolve(true);
      } else {
        return Promise.resolve(false);
      }
    },
    async getTeamList({ commit }) {
      const data = await getTeamList();
      if (data.status) {
        commit("setTeamList", data.message);
        return Promise.resolve(true);
      } else {
        return Promise.resolve(false);
      }
    },
  },
};
