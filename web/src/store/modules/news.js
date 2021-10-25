import { getNewsList } from "@/api/news";

export default {
  namespaced: true,
  state: {
    news_list: [],
  },
  getters: {
    getNewsData: (state) => (val) => {
      return state.news_list.find((news_list) => news_list.news_id == val);
    },
  },
  mutations: {
    setNewsList(state, data) {
      state.news_list = data;
    },
  },
  actions: {
    async getNewsList({ commit }) {
      const data = await getNewsList();
      // console.log(data);
      if (data.status) {
        commit("setNewsList", data.message);
        return Promise.resolve(true);
      } else {
        return Promise.resolve(false);
      }
    },
  },
};
