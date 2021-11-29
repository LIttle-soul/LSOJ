import { getSchoolList } from "@/api/school";

export default {
  namespaced: true,
  state: {
    school_list: [],
  },
  getters: {
    filterSchoolData: (state: any) => (val: any) => {
      return state.school_list.filter((school_list: any) =>
        new RegExp(val).test(school_list.school_id)
      );
    },
  },
  mutations: {
    setSchoolList(state: any, data: any) {
      state.school_list = data;
    },
  },
  actions: {
    async getSchoolList({ commit }: any) {
      const data = await getSchoolList();
      if (data.status) {
        commit("setSchoolList", data.data);
        return Promise.resolve(true);
      } else {
        return Promise.resolve(false);
      }
    },
  },
};
