import settings from "@/config/settings";
import { getItem, setItem } from "@/utils/storage";

export default {
  namespaced: true,
  state: getItem("settings") || settings,
  mutations: {
    SAVE_SETTINGS(state: any, data: any) {
      Object.entries(data).forEach(([key, value]) => {
        state[key] = value;
      });
      setItem("settings", data);
    },
  },
};
