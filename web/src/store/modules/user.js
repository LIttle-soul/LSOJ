export default {
    namespaced: true,
    state: {
        userInfo: null,
    },
    mutations: {
        setUserInfo(state, data) {
            state.userInfo = data;
        },
        clearUserInfo(state) {
            state.userInfo = null;
        },
    },
    actions: {
        async getUserInfo({ commit }) {
            const { code, data} = await this.getUserInfo()
            if (+code === 200) {
                commit('setUserInfo', data);
                return Promise.resolve(data);
            }
        }
    }
}