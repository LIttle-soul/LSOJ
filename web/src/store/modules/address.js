import {getAddressList, getProvinceList, getMunicipalityList } from "@/api/address";

export default {
  namespaced: true,
  state: {
    address_list: [],
    province_list: [],
    municipality_list: [],
  },
  getters: {
    filterProvinceData: (state) => (val) => {
      return state.province_list.filter((province_list) =>
        new RegExp(val).test(province_list.province_id)
      );
    },
    filterMunicipalityData: (state) => (val) => {
      return state.municipality_list.filter((municipality_list) =>
        new RegExp(val).test(municipality_list.municipality_id)
      );
    },
    filterMunicipalityByProvince: (state) => (val) => {
      return state.municipality_list.filter((municipality_list) =>
        new RegExp(val).test(municipality_list.municipality_province)
      );
    }
  },
  mutations: {
    setAddressList(state, data) {
      state.address_list = data;
    },
    setProvinceList(state, data) {
      state.province_list = data;
    },
    setMunicipalityList(state, data) {
      state.municipality_list = data;
    },
  },
  actions: {
    async getAddressList({ commit }) {
      const data = await getAddressList();
      if(data.status) {
        commit("setAddressList", data.data);
        return  Promise.resolve(true);
      } else {
        return Promise.resolve(false);
      }
    },
    async getProvinceList({ commit }) {
      const data = await getProvinceList();
      if(data.status){
          commit("setProvinceList", data.data);
          return Promise.resolve(true);
      } else {
        return Promise.resolve(false);
      }
      
    },
    async getMunicipalityList({ commit }) {
      const data = await getMunicipalityList();
      if(data.status){
          commit("setMunicipalityList", data.data);
          return Promise.resolve(true);
      } else {
        return Promise.resolve(false);
      }
    },
  },
};
