import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";

import "element-plus/dist/index.css";

// v-md-editor
import VMdEditor from "@kangc/v-md-editor/lib/codemirror-editor";
import "@kangc/v-md-editor/lib/style/codemirror-editor.css";

// VuePressTheme
import VuePressTheme from "@kangc/v-md-editor/lib/theme/vuepress.js";
import "@kangc/v-md-editor/lib/theme/style/vuepress.css";

// prism.js
import Prism from "prismjs";

// KaTex
import createKaTexPlugin from "@kangc/v-md-editor/lib/plugins/katex/cdn";

// Mermaid
import createMermaidPlugin from "@kangc/v-md-editor/lib/plugins/mermaid/cdn";
import "@kangc/v-md-editor/lib/plugins/mermaid/mermaid.css";

// TodoList
import createTodoListPlugin from "@kangc/v-md-editor/lib/plugins/todo-list/index";
import "@kangc/v-md-editor/lib/plugins/todo-list/todo-list.css";

// LineNumber
import createLineNumberPlugin from "@kangc/v-md-editor/lib/plugins/line-number/index";

// CopyCode
import createCopyCodePlugin from "@kangc/v-md-editor/lib/plugins/copy-code/index";
import "@kangc/v-md-editor/lib/plugins/copy-code/copy-code.css";

// Align
import createAlignPlugin from "@kangc/v-md-editor/lib/plugins/align";

// CodeMirror
import Codemirror from "codemirror";
// mode
import "codemirror/mode/markdown/markdown";
import "codemirror/mode/javascript/javascript";
import "codemirror/mode/css/css";
import "codemirror/mode/htmlmixed/htmlmixed";
import "codemirror/mode/vue/vue";
// edit
import "codemirror/addon/edit/closebrackets";
import "codemirror/addon/edit/closetag";
import "codemirror/addon/edit/matchbrackets";
// placeholder
import "codemirror/addon/display/placeholder";
// active-line
import "codemirror/addon/selection/active-line";
// scrollbar
import "codemirror/addon/scroll/simplescrollbars";
import "codemirror/addon/scroll/simplescrollbars.css";
// style
import "codemirror/lib/codemirror.css";

VMdEditor.Codemirror = Codemirror;
VMdEditor.use(VuePressTheme, { Prism });
// VueMarkdownEditor.use(createTipPlugin());
VMdEditor.use(createKaTexPlugin());
VMdEditor.use(createMermaidPlugin());
VMdEditor.use(createTodoListPlugin());
VMdEditor.use(createLineNumberPlugin());
VMdEditor.use(createCopyCodePlugin());
VMdEditor.use(createAlignPlugin());

VMdEditor.xss.extend({
  whiteList: {
    source: ["iframe"],
  },
});

import initStorePersistence from "./store/store.persistence";

const app = createApp(App);
app.use(VMdEditor);
app.use(router);
app.use(store);
initStorePersistence(store);
app.mount("#app");
