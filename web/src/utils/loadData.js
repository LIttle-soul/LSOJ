import store from "@/store";

// export const loadData = () => {

// };

export const loadData = () => {
  if (sessionStorage.getItem(store)) {
    store.replaceState(
      Object.assign(
        {},
        store.state,
        JSON.parse(sessionStorage.getItem("store"))
      )
    );
  }
  store.dispatch("user/getUserList");
  store.dispatch("user/getUserInfo");
  store.dispatch("user/getTeamList");
  store.dispatch("solution/getSolutionDataList");
  store.dispatch("school/getSchoolList");
  store.dispatch("rank/getRankList");
  store.dispatch("problem/getProblemDataList");
  store.dispatch("news/getNewsList");
  store.dispatch("contest/getContestList");
  store.dispatch("address/getAddressList");
  store.dispatch("address/getProvinceList");
  store.dispatch("address/getMunicipalityList");
  window.addEventListener("beforeunload", () => {
    sessionStorage.setItem("store", JSON.stringify(store.state));
  });
};
