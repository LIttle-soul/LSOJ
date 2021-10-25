import codeData from "@/config/codeData";

export default {
  namespaced: true,
  state: {
    result_data: codeData.result_data,
    language_data: codeData.language_data,
    filter_language_data: codeData.filter_language_data,
    filter_result_data: codeData.filter_result_data,
    language: codeData.language,
    editor_config: codeData.editor_config,
  },
  mutations: {
      setResultData(state, data) {
          state.result_data = data;
      },
      setLanguageData(state, data) {
          state.language_data = data;
      },
      setLanguage(state, data) {
          state.language = data;
      },
      setCodeEditor(state, data) {
          state.editor_config = data;
      }
  },
};
