import { getContestList } from "@/api/contest";
import * as dayjs from "dayjs";

export default {
  namespaced: true,
  state: {
    contest_list: [],
    temp_contest_data: {
      contest_id: -1,
      contest_problem: [],
      contest_solution: [],
      contest_rank: [],
      contest_count: [],
    },
  },
  getters: {
    getContestData: (state) => (val) => {
      return state.contest_list.find(
        (contest_list) => contest_list.contest_id === +val
      );
    },
    filterContestByIdList: () => (data, val) => {
      return data.filter((item) => val.map(Number).includes(item.contest_id));
    },
    filterContestByKey: () => (data, val) => {
      return data.filter(
        (item) =>
          new RegExp(val).test(item.contest_id) ||
          new RegExp(val).test(item.contest_title)
      );
    },
    filterContestByTime: (state) => () => {
      return state.contest_list.filter((contest_list) =>
        dayjs().isBefore(dayjs(contest_list.end_time))
      );
    },
  },
  mutations: {
    setContestList(state, data) {
      state.contest_list = data;
    },
  },
  actions: {
    async getContestList({ commit }) {
      const data = await getContestList();
      // console.log(data);
      if (data.status) {
        commit("setContestList", data.message);
        return Promise.resolve(true);
      } else {
        return Promise.resolve(false);
      }
    },
  },
};
