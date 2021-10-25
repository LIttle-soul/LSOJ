import { getProblemDataList, getProblemTagAndCourse } from "@/api/problem";

export default {
  namespaced: true,
  state: {
    problem_list: [],
    problem_tag_list: [],
    problem_course_list: [],
  },
  getters: {
    getProblemData: (state) => (val) => {
      return state.problem_list.find(
        (problem_list) => +problem_list.problem_id === +val
      );
    },
    filterProblemListWithStatus: (state) => (val) => {
      return state.problem_list.filter(
        (problem_list) => problem_list.problem_status == val
      );
    },
    filterProblemByDegree: () => (data, val) => {
      return data.filter((problem_list) =>
        val.includes(problem_list.problem_difficult)
      );
    },
    filterProblemList: () => (data, val) => {
      return data.filter(
        (problem_list) =>
          new RegExp(val).test(problem_list.problem_id) ||
          new RegExp(val).test(problem_list.problem_title) ||
          new RegExp(val).test(problem_list.problem_tag) ||
          new RegExp(val).test(problem_list.problem_course)
      );
    },
  },
  mutations: {
    setProblemList(state, data) {
      state.problem_list = data;
    },
    setProblemTagList(state, data) {
      state.problem_tag_list = data;
    },
    setProblemCourseList(state, data) {
      state.problem_course_list = data;
    },
  },
  actions: {
    async getProblemDataList({ commit }) {
      const data = await getProblemDataList();
      const data_tag = await getProblemTagAndCourse();
      if (data.status) {
        commit("setProblemList", data.message);
        if (data_tag.status) {
          commit("setProblemTagList", data_tag.tag);
          commit("setProblemCourseList", data_tag.course);
        }
        return Promise.resolve(true);
      } else {
        return Promise.resolve(false);
      }
    },
  },
};
