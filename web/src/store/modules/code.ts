import codeData from "@/config/codeData";
export default {
  namespaced: true,
  state: {
    language_data: codeData.language_data,
    result_data: codeData.result_data,
    language: codeData.language,
    editor_config: codeData.editor_config,
  },
  mutations: {
    setResultData(state: any, data: any) {
      state.result_data = data;
    },
    setLanguageData(state: any, data: any) {
      state.language_data = data;
    },
    setLanguage(state: any, data: any) {
      state.language = data;
    },
    setCodeEditor(state: any, data: any) {
      state.editor_config = data;
    },
  },
};
