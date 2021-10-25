import { getRankList } from "@/api/rank";

export default {
  namespaced: true,
  state: {
    rank_list: [],
  },
  getters: {
    filterRankList: (state) => (val) => {
      return state.rank_list.filter(
        (rank_list) => (
          new RegExp(val).test(rank_list.user_id) ||
          new RegExp(val).test(rank_list.user_nick) || 
          new RegExp(val).test(rank_list.user_name)
        )
      )
    }
  },
  mutations: {
    setRankList(state, data) {
      state.rank_list = data;
    },
  },
  actions: {
    async getRankList({ commit }) {
      const data = await getRankList();
      if (data.status){
        commit("setRankList", data.message);
        return Promise.resolve(true);
    } else {
        return Promise.resolve(false);
    }
    },
  },
};
