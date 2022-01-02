import { createStore } from "vuex";
import code from "./modules/code";
import user from "./modules/user";

export default createStore({
  state: {
    search_data: "",
  },
  getters: {},
  mutations: {
    set_search_data(state, val) {
      state.search_data = val;
    },
  },
  modules: {
    code: code,
    user: user,
  },
  // plugins: [createPersistedState()],
});
