import { getContestList } from "@/api/contest";
import dayjs from "dayjs";

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
  getters: {},
  mutations: {},
  actions: {},
};
