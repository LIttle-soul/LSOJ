import { getProblemDataList } from "@/api/problem";

export default {
    namespaced: true,
    state: {
        problemList: null
    },
    getters: {
        getProblemData: (state) => (val) => {
            return state.problemList.find(problemList => problemList.problem_id == val);
        },
        filterProblemList: (state) => (val) => {
            return state.problemList.filter(problemList => (new RegExp(val).test(problemList.problem_id)));
        }
    },
    mutations: {
        setproblemList(state, data) {
            state.problemList = data
        },
    },
    actions: {
        async getProblemDataList({ commit }) {
            const data = await getProblemDataList();
            // console.log(data);
            commit('setproblemList', data);
        }
    }
}