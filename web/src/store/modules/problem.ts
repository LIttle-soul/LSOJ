import { getProblemDataList, getProblemTagAndCourse } from "@/api/problem";

export default {
  namespaced: true,
  state: {
    problem_list: [],
    problem_tag_list: [],
    problem_course_list: [],
  },
  getters: {},
  mutations: {
    setProblemTagList(state: any, data: any) {
      state.problem_tag_list = data;
    },
    setProblemCourseList(state: any, data: any) {
      state.problem_course_list = data;
    },
  },
  actions: {
    async getProblemTagList({ commit }: any) {
      const data_tag = await getProblemTagAndCourse();
      // console.log(data_tag);
      if (data_tag.status) {
        commit("setProblemTagList", data_tag.tag);
        commit("setProblemCourseList", data_tag.course);
      }
      return Promise.resolve(true);
    },
  },
};
