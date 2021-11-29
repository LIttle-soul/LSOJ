<template>
  <div class="code-editor" ref="container_ref"></div>
</template>

<script setup lang="ts">
import * as monaco from "monaco-editor";
import editorWorker from "monaco-editor/esm/vs/editor/editor.worker?worker";
import jsonWorker from "monaco-editor/esm/vs/language/json/json.worker?worker";
import cssWorker from "monaco-editor/esm/vs/language/css/css.worker?worker";
import htmlWorker from "monaco-editor/esm/vs/language/html/html.worker?worker";
import tsWorker from "monaco-editor/esm/vs/language/typescript/ts.worker?worker";
import { mapState, useStore } from "vuex";
import { computed, onMounted, ref, unref, watch } from "vue";

let store = useStore();
let editor_config = computed(
  mapState("code", ["editor_config"]).editor_config.bind({ $store: store })
);

let container_ref = ref();
let prop = defineProps({
  language: {
    type: String,
    default: "cpp",
  },
});

self.MonacoEnvironment = {
  getWorker(_: any, label: string) {
    if (label === "json") {
      return new jsonWorker();
    }
    if (label === "css" || label === "scss" || label === "less") {
      return new cssWorker();
    }
    if (label === "html" || label === "handlebars" || label === "razor") {
      return new htmlWorker();
    }
    if (label === "typescript" || label === "javascript") {
      return new tsWorker();
    }
    return new editorWorker();
  },
};

let monacoEditor: monaco.editor.IStandaloneCodeEditor;

onMounted(() => {
  let container = unref(container_ref);
  monacoEditor = monaco.editor.create(container, editor_config.value);
});

watch(
  () => prop.language,
  (new_val: string) => {
    changeLanguage(new_val);
  }
);

let changeLanguage = (val: string) => {
  let mod = monaco.editor.createModel("", val);
  monacoEditor.setModel(mod);
};

let getVal = () => {
  // console.log("获取值");
  let text = monacoEditor.getValue();
  return text;
};
defineExpose({
  getVal,
});
</script>

<style scoped lang="scss">
.code-editor {
  width: 100%;
  height: 100%;
}
</style>
