import {
  getUserInfo,
  checkUserLoginStatus,
  getUserList,
  getTeamList,
} from "@/api/user";
import { user_nav, not_login, user_login, admin_login } from "@/config/userNav";
import cookies from "vue-cookies";
import { ElNotification } from "element-plus";

export default {
  namespaced: true,
  state: {
    has_login: false,
    user_info: null,
    user_nav: user_nav,
    login_nav: not_login,
    has_join_team_list: null,
    has_created_team_list: null,
    user_list: null,
    team_list: null,
  },
  getters: {},
  mutations: {
    // 设置登录后的用户菜单
    setLoginNav(state: any) {
      if (state.has_login) {
        state.login_nav =
          state.user_info?.user_power <= 2
            ? [...admin_login, ...user_login]
            : user_login;
      } else {
        state.login_nav = not_login;
      }
    },
    // 注销
    logout(state: any) {
      cookies.remove("token");
      state.has_login = false;
      state.user_info = null;
      state.user_nav = user_nav;
      state.login_nav = not_login;
    },
    // 设置登录后用户的个人信息
    setUserInfo(state: any, value: any) {
      state.has_login = true;
      state.user_info = value;
    },
    // 设置我加入的团队列表
    setMyJoinTeamList(state: any, value: any) {
      state.has_join_team_list = value;
    },
    // 设置我创建的团队列表
    setMyCreatedTeamList(state: any, value: any) {
      state.has_created_team_list = value;
    },
  },
  actions: {
    async getUserInfo({ commit }: any) {
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
    checkUserStatus({ commit }: any) {
      let checkStatus = async () => {
        let token = cookies.get("token");
        if (token) {
          let back_data = await checkUserLoginStatus();
          if (!back_data.status) {
            commit("logout");
            ElNotification({
              type: "warning",
              message: "你的登录已失效, 请重新登录",
              title: "登录提醒",
              duration: 0,
              offset: 100,
            });
          }
        }
      };
      setTimeout(checkStatus, 3000);
      setInterval(checkStatus, 30 * 60 * 1000);
    },
  },
};
