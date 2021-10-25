import { getSolutionDataList } from "@/api/solution";
import * as dayjs from "dayjs";

export default {
  namespaced: true,
  state: {
    solution_list: [],
  },
  getters: {
    getSolutionData: (state) => (val) => {
      return state.solution_list.find(
        (solution_list) => +solution_list.solution_id === +val
      );
    },
    filterListByKey: () => (data, key, val) => {
      if (key === "solution" && val != "") {
        return data.filter(
          (solution_list) => +val === solution_list.solution_id
        );
      } else if (key === "user") {
        return data.filter((solution_list) =>
          new RegExp(val).test(solution_list.user_id)
        );
      } else if (key === "problem" && val !== "") {
        return data.filter(
          (solution_list) => +val === solution_list.problem_id
        );
      } else if (key === "result" && val !== "") {
        return data.filter(
          (solution_list) => +val === solution_list.run_result
        );
      } else if (key === "language" && val !== "") {
        return data.filter(
          (solution_list) => +val === solution_list.solution_language
        );
      } else {
        return data;
      }
    },
    filterDaySolution: (state) => () => {
      return state.solution_list.filter(
        (solution_list) =>
          dayjs().get("year") ===
            dayjs(solution_list.solution_time).get("year") &&
          dayjs().get("month") ===
            dayjs(solution_list.solution_time).get("month") &&
          dayjs().get("date") === dayjs(solution_list.solution_time).get("date")
      );
    },
  },
  mutations: {
    setSolutionList(state, data) {
      state.solution_list = data;
    },
  },
  actions: {
    async getSolutionDataList({ commit }) {
      const data = await getSolutionDataList();
      if (data.status) {
        commit("setSolutionList", data.message);
        return Promise.resolve(true);
      } else {
        return Promise.resolve(false);
      }
    },
  },
};
